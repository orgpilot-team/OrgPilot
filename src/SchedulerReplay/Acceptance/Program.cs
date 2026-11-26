using System.Diagnostics;
using System.Globalization;
using System.Text;
using Microsoft.Extensions.DependencyInjection;
using OrgPilot.Acceptance;
using OrgPilot.BackgroundWorker.Modules.Intake;
using OrgPilot.BackgroundWorker.Modules.Kpi;
using OrgPilot.BackgroundWorker.Modules.Snapshots;
using OrgPilot.BackgroundWorker.Persistence;
using OrgPilot.Foundation.Archive;

if (args is not ["--report-day", var reportDayText, "--cutoff", var cutoffText] ||
    !int.TryParse(reportDayText, CultureInfo.InvariantCulture, out var reportDay) || reportDay < 2 ||
    !DateOnly.TryParseExact(cutoffText, "yyyy-MM-dd", CultureInfo.InvariantCulture, DateTimeStyles.None, out var cutoff))
{
    Console.Error.WriteLine("Usage: --report-day N --cutoff yyyy-MM-dd");
    return 2;
}

static string Required(string name) => Environment.GetEnvironmentVariable(name)
    ?? throw new InvalidOperationException($"Missing environment variable {name}.");

var dataDirectory = Required("DATA_DIR");
var archive = new FileSystemArchive(Required("Archive__RootPath"));
var workerConnection = Required("ConnectionStrings__Product");
var acceptanceConnection = Required("ConnectionStrings__Parity");
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

async Task<ArchiveReference> PinAsync(string path)
{
    await using var stream = File.OpenRead(Path.Combine(dataDirectory, path));
    return await archive.StoreAsync(stream);
}
var calendar = await PinAsync("calendar/calendar_days.csv");
var targets = await PinAsync("config/monthly_targets.csv");
var dictionary = await PinAsync("config/kpi_dictionary.csv");
var views = await PinAsync("config/reference_views.sql");
var organization = new List<ArchiveReference>();
foreach (var path in new[] { "org/units.csv", "org/teams.csv", "org/managers.csv", "org/staff.csv", "org/access_matrix.csv" })
    organization.Add(await PinAsync(path));
var policy = new List<ArchiveReference> { views };
foreach (var path in new[] { "config/escalation_rules.csv", "config/workflow_definitions.csv" })
    policy.Add(await PinAsync(path));
var pins = new PinnedVersions(IntakeFingerprint.Of(organization), IntakeFingerprint.Of(policy),
    dictionary.Sha256, targets.Sha256, calendar.Sha256, IntakeFingerprint.Of(Array.Empty<string>()));
var snapshot = SnapshotBuilder.Build(reportDay, cutoff, pins, batches);
await snapshotStore.SaveAsync(snapshot);
var restored = await snapshotStore.ReadAsync(snapshot.Id);
var projection = await ProjectionData.CreateAsync(restored, archive, calendar, targets);
await using var viewStream = await archive.OpenVerifiedAsync(views);
using var viewReader = new StreamReader(viewStream, new UTF8Encoding(false, true));
await using var oracle = new SqliteReferenceOracle();
await oracle.InitializeAsync(projection, await viewReader.ReadToEndAsync());
var definitions = await KpiDefinitionReader.ReadAsync(archive, dictionary);
var failed = 0;
foreach (var definition in definitions)
{
    await registry.RegisterAsync(definition);
    try
    {
        var expected = await oracle.QueryAsync(definition, cutoff);
        var actual = await KpiQuery.ExecuteCandidateAsync(workerConnection, projection, definition);
        var receipt = ParityCheck.Compare(projection, definition, expected, actual);
        await ParityCheck.PersistAsync(acceptanceConnection, receipt);
        Console.WriteLine($"{definition.KpiId}: {(receipt.Passed ? "PASS" : "FAIL")} {receipt.Id}");
        if (!receipt.Passed) failed++;
        else await registry.CalculateAsync(workerConnection, projection, definition.Id);
    }
    catch (Exception ex)
    {
        failed++;
        Console.Error.WriteLine($"{definition.KpiId}: {ex.GetType().Name}; no passing receipt.");
    }
}
Console.WriteLine($"Snapshot: {snapshot.Id}; definitions: {definitions.Count}; failed: {failed}");
return failed == 0 ? 0 : 1;
