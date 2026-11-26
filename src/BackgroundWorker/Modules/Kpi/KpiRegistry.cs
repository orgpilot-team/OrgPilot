using System.Diagnostics;
using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using OrgPilot.BackgroundWorker.Modules.Intake;
using OrgPilot.BackgroundWorker.Modules.Snapshots;
using OrgPilot.BackgroundWorker.Persistence;

namespace OrgPilot.BackgroundWorker.Modules.Kpi;

public sealed record ParityReceipt(string Id, string DefinitionId, string SnapshotId,
    string ProjectionHash, string ReferenceSqlHash, string PostgreSqlHash,
    int ReferenceCount, int ProductCount, bool Passed, IReadOnlyList<string> Differences,
    string ReferenceResultHash, string ProductResultHash, string TraceId);

public sealed class KpiRegistry(Stage2DbContext db)
{
    public async Task RegisterAsync(KpiDefinition definition, CancellationToken cancellationToken = default)
    {
        if (definition.Id != IntakeFingerprint.Of(definition with { Id = "" }) ||
            !BaselineKpiSql.Definitions.TryGetValue(definition.KpiId, out var translation) ||
            definition.ReferenceSql != translation.ReferenceSql || definition.PostgreSql != translation.PostgreSql)
            throw new InvalidDataException("Unregistered or modified definition.");
        var payload = JsonSerializer.Serialize(definition);
        await db.Database.ExecuteSqlInterpolatedAsync($"""
            INSERT INTO kpi.definitions ("Id", "Payload") VALUES ({definition.Id}, CAST({payload} AS jsonb))
            ON CONFLICT ("Id") DO NOTHING
            """, cancellationToken);
    }

    public async Task<KpiRun> CalculateAsync(string connectionString, ProjectionData data,
        string definitionId, CancellationToken cancellationToken = default)
    {
        var row = await db.Definitions.AsNoTracking().SingleAsync(x => x.Id == definitionId, cancellationToken);
        var definition = JsonSerializer.Deserialize<KpiDefinition>(row.Payload)
            ?? throw new InvalidDataException("Invalid registered KPI.");
        if (definition.DictionaryHash != data.Snapshot.Versions.KpiDefinitions)
            throw new InvalidDataException("KPI definition is not pinned by this snapshot.");
        var receipts = await db.ParityReceipts.AsNoTracking().Where(x => x.DefinitionId == definitionId)
            .Select(x => x.Payload).ToListAsync(cancellationToken);
        if (!receipts.Select(x => JsonSerializer.Deserialize<ParityReceipt>(x)).Any(r =>
                r is not null && r.Passed && r.DefinitionId == definition.Id &&
                r.ReferenceSqlHash == IntakeFingerprint.Of(definition.ReferenceSql) &&
                r.PostgreSqlHash == IntakeFingerprint.Of(definition.PostgreSql)))
            throw new InvalidOperationException("KPI has no passing parity receipt.");

        var raw = await KpiQuery.ExecuteCandidateAsync(connectionString, data, definition, cancellationToken);
        var run = KpiQuery.CreateRun(data, definition, raw);
        var payload = JsonSerializer.Serialize(run);
        await db.Database.ExecuteSqlInterpolatedAsync($"""
            INSERT INTO kpi.query_runs ("Id", "SnapshotId", "DefinitionId", "Payload", "TraceId")
            VALUES ({run.QueryId}, {run.SnapshotId}, {definition.Id}, CAST({payload} AS jsonb), {Activity.Current?.TraceId.ToString() ?? ""})
            ON CONFLICT ("Id") DO NOTHING
            """, cancellationToken);
        return run;
    }
}
