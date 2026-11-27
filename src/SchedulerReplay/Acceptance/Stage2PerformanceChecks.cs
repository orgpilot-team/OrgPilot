using System.Diagnostics;
using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using OrgPilot.BackendApi.Modules.Configuration;
using OrgPilot.BackgroundWorker.Modules.Intake;
using OrgPilot.BackgroundWorker.Modules.Kpi;
using OrgPilot.BackgroundWorker.Modules.Snapshots;
using OrgPilot.BackgroundWorker.Persistence;
using OrgPilot.Foundation.Archive;

namespace OrgPilot.Acceptance;

// Run against an isolated copy of an accepted database. Historical intake and
// definition parity are prerequisites; SQLite is never part of a product day.
internal static class Stage2PerformanceChecks
{
    public static async Task<int> RunAsync(string dataDirectory, string archiveDirectory,
        string workerConnection, string configurationConnection, string snapshotId)
    {
        await using var services = new ServiceCollection().AddStage2Persistence(workerConnection).BuildServiceProvider();
        await using var seedScope = services.CreateAsyncScope();
        var seedDb = seedScope.ServiceProvider.GetRequiredService<Stage2DbContext>();
        var seedRow = await seedDb.Snapshots.AsNoTracking().SingleAsync(row => row.Id == snapshotId);
        var seed = JsonSerializer.Deserialize<SnapshotReference>(seedRow.Payload)
            ?? throw new InvalidDataException("Invalid benchmark snapshot.");
        if (seed.Versions.Sources is null || seed.BatchIds.Count != seed.ReportDay)
            throw new InvalidDataException("Benchmark requires an accepted snapshot with archived inputs and daily intake.");

        var archive = new FileSystemArchive(archiveDirectory);
        string? previousHash = null;
        var failed = 0;
        for (var attempt = 1; attempt <= 2; attempt++)
        {
            var timer = Stopwatch.StartNew();
            var timings = new SortedDictionary<string, double>(StringComparer.Ordinal);
            await using var scope = services.CreateAsyncScope();
            var db = scope.ServiceProvider.GetRequiredService<Stage2DbContext>();
            var batches = new IngestionBatchStore(db);
            var snapshots = new SnapshotStore(db, batches);
            var registry = new KpiRegistry(db);
            var intake = new IngestionCoordinator(archive);

            // Read/archive/normalize the new drop and reload all historical facts.
            var latest = await intake.ReadAsync(dataDirectory, seed.ReportDay - 1, seed.Cutoff);
            if (!seed.BatchIds.Contains(latest.Id, StringComparer.Ordinal))
                throw new InvalidDataException("Benchmark data differs from the accepted snapshot.");
            await batches.SaveAsync(latest);
            var history = new List<IngestionBatch>();
            foreach (var batchId in seed.BatchIds)
                history.Add(await batches.ReadAsync(batchId));
            timings.Add("IntakeAndHistorySeconds", timer.Elapsed.TotalSeconds);

            var sources = await SnapshotInputReferences.PinAsync(dataDirectory, archive);
            var definitions = await KpiDefinitionReader.ReadAsync(archive, sources.KpiDictionary);
            foreach (var definition in definitions)
                await registry.RegisterAsync(definition);
            var options = new DbContextOptionsBuilder<ConfigurationDbContext>();
            ConfigurationDbContext.Configure(options, configurationConnection);
            await using var configurationDb = new ConfigurationDbContext(options.Options);
            var active = await new ConfigurationVersionReader(configurationDb).ResolveAsync(seed.ReportDay);
            var pins = SnapshotVersionPinning.Create(seed.ReportDay, sources, definitions,
                ConfigurationVersionReader.References(active));
            var versions = pins.KpiVersions ?? throw new InvalidDataException("Benchmark has no pinned KPI definitions.");
            var snapshot = SnapshotBuilder.Build(seed.ReportDay, seed.Cutoff, pins, history);
            if (snapshot.Id != snapshotId)
                throw new InvalidDataException("Benchmark did not reproduce the accepted snapshot.");
            await snapshots.SaveAsync(snapshot);
            var restored = await snapshots.ReadAsync(snapshot.Id);
            if (IntakeFingerprint.Of(restored) != IntakeFingerprint.Of(snapshot))
                throw new InvalidDataException("Benchmark snapshot reload differs from its inputs.");
            var projection = await ProjectionData.CreateAsync(restored, archive);
            timings.Add("SnapshotAndProjectionSeconds", timer.Elapsed.TotalSeconds - timings.Values.Sum());

            var results = new List<object>();
            foreach (var version in versions.OrderBy(version => version.KpiId, StringComparer.Ordinal))
            {
                var queryTimer = Stopwatch.StartNew();
                var run = await registry.CalculateAsync(workerConnection, projection, version.DefinitionId);
                results.Add(new { run.KpiId, run.QueryId, run.ResultHash });
                Console.WriteLine(FormattableString.Invariant(
                    $"TIMING attempt={attempt} {run.KpiId}: {queryTimer.Elapsed.TotalSeconds:F3}s"));
            }
            timer.Stop();
            timings.Add("KpiSeconds", timer.Elapsed.TotalSeconds - timings.Values.Sum());
            var resultHash = IntakeFingerprint.Of(results);
            var passed = timer.Elapsed <= TimeSpan.FromMinutes(5) &&
                (previousHash is null || previousHash == resultHash) && results.Count == versions.Count;
            if (!passed) failed++;
            previousHash = resultHash;
            Console.WriteLine(JsonSerializer.Serialize(new
            {
                Check = "Stage2ProductDay", Attempt = attempt, Passed = passed,
                seed.ReportDay, seed.Cutoff, SnapshotId = snapshot.Id,
                Facts = restored.Facts.Count, Definitions = results.Count, ResultHash = resultHash,
                ElapsedSeconds = timer.Elapsed.TotalSeconds, BudgetSeconds = 300, Timings = timings,
                Processors = Environment.ProcessorCount
            }));
        }
        Console.WriteLine($"Stage 2 product-day checks: Passed: {2 - failed}, Failed: {failed}, Skipped: 0");
        return failed == 0 ? 0 : 1;
    }
}
