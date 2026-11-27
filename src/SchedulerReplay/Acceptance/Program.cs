using System.Diagnostics;
using System.Globalization;
using System.Text;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.EntityFrameworkCore;
using OrgPilot.Acceptance;
using OrgPilot.BackendApi.Modules.Configuration;
using OrgPilot.BackgroundWorker.Modules.Intake;
using OrgPilot.BackgroundWorker.Modules.Kpi;
using OrgPilot.BackgroundWorker.Modules.Snapshots;
using OrgPilot.BackgroundWorker.Persistence;
using OrgPilot.Foundation.Archive;

if (args is ["--check-dev-dataset"])
    return await DevDatasetChecks.RunAsync(Required("DATA_DIR"), Required("Archive__RootPath"));

if (args is ["--check-kpi-sql"])
{
    await KpiSqlChecks.RunAsync(Required("ConnectionStrings__Product"));
    return 0;
}

if (args is ["--check-performance", var snapshotId])
    return await Stage2PerformanceChecks.RunAsync(Required("DATA_DIR"), Required("Archive__RootPath"),
        Required("ConnectionStrings__Product"), Required("ConnectionStrings__Configuration"), snapshotId);

var checkConfiguration = args.LastOrDefault() == "--check-configuration";
if (checkConfiguration) args = args[..^1];
if (args is not ["--report-day", var reportDayText, "--cutoff", var cutoffText] ||
    !int.TryParse(reportDayText, CultureInfo.InvariantCulture, out var reportDay) || reportDay < 2 ||
    !DateOnly.TryParseExact(cutoffText, "yyyy-MM-dd", CultureInfo.InvariantCulture, DateTimeStyles.None, out var cutoff))
{
    Console.Error.WriteLine("Usage: --report-day N --cutoff yyyy-MM-dd [--check-configuration] | --check-dev-dataset | --check-kpi-sql | --check-performance SNAPSHOT_ID");
    return 2;
}

static string Required(string name) => Environment.GetEnvironmentVariable(name)
    ?? throw new InvalidOperationException($"Missing environment variable {name}.");

var dataDirectory = Required("DATA_DIR");
var archive = new FileSystemArchive(Required("Archive__RootPath"));
var workerConnection = Required("ConnectionStrings__Product");
var acceptanceConnection = Required("ConnectionStrings__Parity");
var configurationConnection = Required("ConnectionStrings__Configuration");
await KpiSqlChecks.RunAsync(workerConnection);
using var activity = new Activity("stage2.acceptance").Start();
await using var services = new ServiceCollection().AddStage2Persistence(workerConnection).BuildServiceProvider();
await using var scope = services.CreateAsyncScope();
var db = scope.ServiceProvider.GetRequiredService<Stage2DbContext>();
var intake = new IngestionCoordinator(archive);
var batchStore = new IngestionBatchStore(db);
var snapshotStore = new SnapshotStore(db, batchStore);
var registry = new KpiRegistry(db);
var batches = new List<IngestionBatch>();
for (var day = 0; day < reportDay; day++)
{
    var batch = await intake.ReadAsync(dataDirectory, day, cutoff);
    await batchStore.SaveAsync(batch);
    batches.Add(batch);
}

var sources = await SnapshotInputReferences.PinAsync(dataDirectory, archive);
var definitions = await KpiDefinitionReader.ReadAsync(archive, sources.KpiDictionary);
foreach (var definition in definitions)
    await registry.RegisterAsync(definition);
var configurationOptions = new DbContextOptionsBuilder<ConfigurationDbContext>();
ConfigurationDbContext.Configure(configurationOptions, configurationConnection);
await using var configurationDb = new ConfigurationDbContext(configurationOptions.Options);
var active = await new ConfigurationVersionReader(configurationDb).ResolveAsync(reportDay);
var pins = SnapshotVersionPinning.Create(reportDay, sources, definitions,
    ConfigurationVersionReader.References(active));
var snapshot = SnapshotBuilder.Build(reportDay, cutoff, pins, batches);
await snapshotStore.SaveAsync(snapshot);
await batchStore.SaveAsync(batches[0]);
await snapshotStore.SaveAsync(snapshot);
var restored = await snapshotStore.ReadAsync(snapshot.Id);
if (IntakeFingerprint.Of(restored) != IntakeFingerprint.Of(snapshot))
    throw new InvalidDataException("Persisted snapshot differs from the original.");
var projection = await ProjectionData.CreateAsync(restored, archive);
await using var viewStream = await archive.OpenVerifiedAsync(restored.Versions.Sources!.ReferenceViews);
using var viewReader = new StreamReader(viewStream, new UTF8Encoding(false, true));
await using var oracle = new SqliteReferenceOracle();
await oracle.InitializeAsync(projection, await viewReader.ReadToEndAsync());
// Check every baseline translation, plus any approved replacement pinned for this day.
var candidates = definitions.ToDictionary(d => d.Id, StringComparer.Ordinal);
foreach (var version in pins.KpiVersions!)
    if (!candidates.ContainsKey(version.DefinitionId))
        candidates.Add(version.DefinitionId, await registry.ReadAsync(version.DefinitionId));
var failed = 0;
KpiDefinition? fixtureDefinition = null;
ParityReceipt? fixtureReceipt = null;
foreach (var definition in candidates.Values.OrderBy(d => d.KpiId, StringComparer.Ordinal).ThenBy(d => d.Id, StringComparer.Ordinal))
{
    try
    {
        var expected = await oracle.QueryAsync(definition, cutoff);
        var actual = await KpiQuery.ExecuteCandidateAsync(workerConnection, projection, definition);
        var receipt = ParityCheck.Compare(projection, definition, expected, actual);
        await ParityCheck.PersistAsync(acceptanceConnection, receipt);
        Console.WriteLine($"{definition.KpiId}: {(receipt.Passed ? "PASS" : "FAIL")} {receipt.Id}");
        if (!receipt.Passed) failed++;
        else if (pins.KpiVersions.Any(v => v.DefinitionId == definition.Id))
        {
            var run = await registry.CalculateAsync(workerConnection, projection, definition.Id);
            if (run.ResultHash != KpiQuery.CreateRun(projection, definition, actual).ResultHash)
                throw new InvalidDataException("Repeated PostgreSQL calculation did not reproduce the result.");
            if (definition.KpiId == "K_ORG_ONTIME")
            {
                fixtureDefinition = definition;
                fixtureReceipt = receipt;
            }
        }
    }
    catch (Exception ex)
    {
        failed++;
        Console.Error.WriteLine($"{definition.KpiId}: {ex.GetType().Name}; acceptance or calculation failed.");
    }
}
if (checkConfiguration && failed == 0)
    await ConfigurationChecks.RunAsync(configurationDb, configurationConnection, reportDay,
        fixtureDefinition ?? throw new InvalidDataException("Configuration fixture KPI is absent."),
        fixtureReceipt ?? throw new InvalidDataException("Configuration fixture receipt is absent."));
Console.WriteLine($"Snapshot: {snapshot.Id}; definitions: {candidates.Count}; failed: {failed}");
return failed == 0 ? 0 : 1;
