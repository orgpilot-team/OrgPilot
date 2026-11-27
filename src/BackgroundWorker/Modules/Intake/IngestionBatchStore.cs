using System.Diagnostics;
using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using OrgPilot.BackgroundWorker.Persistence;

namespace OrgPilot.BackgroundWorker.Modules.Intake;

public sealed class IngestionBatchStore(Stage2DbContext db)
{
    public async Task SaveAsync(IngestionBatch batch, CancellationToken cancellationToken = default)
    {
        var payload = JsonSerializer.Serialize(batch);
        await db.Database.ExecuteSqlInterpolatedAsync($"""
            INSERT INTO intake.batches ("Id", "DropDay", "Payload", "TraceId")
            VALUES ({batch.Id}, {batch.Drop.DropDay}, CAST({payload} AS jsonb), {Activity.Current?.TraceId.ToString() ?? ""})
            ON CONFLICT ("Id") DO NOTHING
            """, cancellationToken);
    }

    public async Task<IngestionBatch> ReadAsync(string id, CancellationToken cancellationToken = default)
    {
        var record = await db.Batches.AsNoTracking().SingleAsync(x => x.Id == id, cancellationToken);
        return JsonSerializer.Deserialize<IngestionBatch>(record.Payload)
            ?? throw new InvalidDataException("Invalid persisted intake batch.");
    }
}
