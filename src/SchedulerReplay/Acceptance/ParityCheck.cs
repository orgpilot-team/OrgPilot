using System.Diagnostics;
using System.Globalization;
using System.Text.Json;
using Npgsql;
using OrgPilot.BackgroundWorker.Modules.Intake;
using OrgPilot.BackgroundWorker.Modules.Kpi;
using OrgPilot.BackgroundWorker.Modules.Snapshots;

namespace OrgPilot.Acceptance;

public static class ParityCheck
{
    public static ParityReceipt Compare(ProjectionData projection, KpiDefinition definition,
        IReadOnlyList<KpiPoint> reference, IReadOnlyList<KpiPoint> product)
    {
        var differences = new List<string>();
        var expected = reference.GroupBy(x => (x.Date, x.Dimension)).ToDictionary(x => x.Key, x => x.ToArray());
        var actual = product.GroupBy(x => (x.Date, x.Dimension)).ToDictionary(x => x.Key, x => x.ToArray());
        foreach (var key in expected.Keys.Union(actual.Keys).OrderBy(k => k.Date).ThenBy(k => k.Dimension, StringComparer.Ordinal))
        {
            var label = key.Date.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture) + ":" + key.Dimension;
            if (!expected.TryGetValue(key, out var left) || !actual.TryGetValue(key, out var right) ||
                left.Length != 1 || right.Length != 1)
            {
                differences.Add(label + ":population");
                continue;
            }
            var a = left[0].Value;
            var b = right[0].Value;
            if (a is null || b is null)
            {
                if (a != b) differences.Add(label + ":null");
            }
            else if (Math.Abs(a.Value - b.Value) > Math.Abs(a.Value) * 0.01m)
                differences.Add(label + ":tolerance");
        }
        if (reference.Count == 0 && product.Count == 0)
            differences.Add("no_population_for_acceptance");
        var receipt = new ParityReceipt("", definition.Id, projection.Snapshot.Id, projection.Hash,
            IntakeFingerprint.Of(definition.ReferenceSql), IntakeFingerprint.Of(definition.PostgreSql),
            reference.Count, product.Count, differences.Count == 0, differences.AsReadOnly(),
            IntakeFingerprint.Of(reference), IntakeFingerprint.Of(product), Activity.Current?.TraceId.ToString() ?? "");
        return receipt with { Id = IntakeFingerprint.Of(receipt with { TraceId = "" }) };
    }

    // Acceptance-only credential: must not be the Worker/API runtime principal.
    public static async Task PersistAsync(string connectionString, ParityReceipt receipt,
        CancellationToken cancellationToken = default)
    {
        await using var connection = new NpgsqlConnection(connectionString);
        await connection.OpenAsync(cancellationToken);
        await using var command = new NpgsqlCommand("""
            INSERT INTO kpi.parity_receipts ("Id", "DefinitionId", "Payload", "TraceId")
            VALUES (@id, @definition, CAST(@payload AS jsonb), @trace)
            ON CONFLICT ("Id") DO NOTHING
            """, connection);
        command.Parameters.AddWithValue("id", receipt.Id);
        command.Parameters.AddWithValue("definition", receipt.DefinitionId);
        command.Parameters.AddWithValue("payload", JsonSerializer.Serialize(receipt));
        command.Parameters.AddWithValue("trace", receipt.TraceId);
        await command.ExecuteNonQueryAsync(cancellationToken);
    }
}
