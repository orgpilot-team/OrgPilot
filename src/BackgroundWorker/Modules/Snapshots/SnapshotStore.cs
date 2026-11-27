using System.Diagnostics;
using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using OrgPilot.BackgroundWorker.Modules.Intake;
using OrgPilot.BackgroundWorker.Persistence;

namespace OrgPilot.BackgroundWorker.Modules.Snapshots;

public sealed record SnapshotReference(string Id, int ReportDay, DateOnly Cutoff,
    PinnedVersions Versions, IReadOnlyList<string> BatchIds);

public sealed class SnapshotStore(Stage2DbContext db, IngestionBatchStore batches)
{
    public async Task SaveAsync(DailySnapshot snapshot, CancellationToken cancellationToken = default)
    {
        // Persist immutable batch references, not another complete copy of every historical row.
        var reference = new SnapshotReference(snapshot.Id, snapshot.ReportDay, snapshot.Cutoff,
            snapshot.Versions, snapshot.BatchIds);
        var payload = JsonSerializer.Serialize(reference);
        await db.Database.ExecuteSqlInterpolatedAsync($"""
            INSERT INTO snapshots.snapshots ("Id", "ReportDay", "Payload", "TraceId")
            VALUES ({snapshot.Id}, {snapshot.ReportDay}, CAST({payload} AS jsonb), {Activity.Current?.TraceId.ToString() ?? ""})
            ON CONFLICT ("Id") DO NOTHING
            """, cancellationToken);
    }

    public async Task<DailySnapshot> ReadAsync(string id, CancellationToken cancellationToken = default)
    {
        var row = await db.Snapshots.AsNoTracking().SingleAsync(x => x.Id == id, cancellationToken);
        var reference = JsonSerializer.Deserialize<SnapshotReference>(row.Payload)
            ?? throw new InvalidDataException("Invalid snapshot reference.");
        var source = new List<IngestionBatch>();
        foreach (var batchId in reference.BatchIds)
            source.Add(await batches.ReadAsync(batchId, cancellationToken));
        var result = SnapshotBuilder.Build(reference.ReportDay, reference.Cutoff, reference.Versions, source);
        if (result.Id != id) throw new InvalidDataException("Snapshot identity mismatch.");
        return result;
    }
}
