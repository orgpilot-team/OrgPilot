using System.Globalization;
using Npgsql;
using OrgPilot.BackgroundWorker.Modules.Intake;
using OrgPilot.BackgroundWorker.Modules.Snapshots;

namespace OrgPilot.BackgroundWorker.Modules.Kpi;

public sealed record KpiPoint(DateOnly Date, string? Dimension, decimal? Value, string Status = "available");
public sealed record KpiRun(string QueryId, string SnapshotId, string DefinitionId, string KpiId,
    string Unit, int? Precision, string ProjectionHash, string Sql, IReadOnlyList<KpiPoint> Points,
    string ResultHash);

public static class KpiQuery
{
    // Used by acceptance against a candidate; product execution is gated by KpiRegistry.
    public static async Task<IReadOnlyList<KpiPoint>> ExecuteCandidateAsync(string connectionString,
        ProjectionData data, KpiDefinition definition, CancellationToken cancellationToken = default)
    {
        if (!BaselineKpiSql.Definitions.TryGetValue(definition.KpiId, out var translation) ||
            definition.ReferenceSql != translation.ReferenceSql || definition.PostgreSql != translation.PostgreSql)
            throw new InvalidDataException("Only registered baseline SQL may execute.");

        await using var connection = new NpgsqlConnection(connectionString);
        await connection.OpenAsync(cancellationToken);
        await using var transaction = await connection.BeginTransactionAsync(cancellationToken);
        await using (var settings = new NpgsqlCommand("SET TRANSACTION READ ONLY; SET LOCAL TIME ZONE 'Asia/Tehran'; SET LOCAL statement_timeout = '60s'", connection, transaction))
            await settings.ExecuteNonQueryAsync(cancellationToken);
        await using var command = new NpgsqlCommand(PostgreSqlProjection.Bind(definition.PostgreSql), connection, transaction);
        command.Parameters.AddWithValue("data", data.Json);
        await using var reader = await command.ExecuteReaderAsync(cancellationToken);
        var date = reader.GetOrdinal("d");
        var value = reader.GetOrdinal("value");
        var dimension = definition.Dimension is null ? -1 : reader.GetOrdinal("dim");
        var rows = new List<KpiPoint>();
        while (await reader.ReadAsync(cancellationToken))
        {
            var day = reader.GetFieldValue<DateOnly>(date);
            if (day > data.Snapshot.Cutoff) continue;
            rows.Add(new(day, dimension < 0 || reader.IsDBNull(dimension) ? null : reader.GetString(dimension),
                reader.IsDBNull(value) ? null : Convert.ToDecimal(reader.GetValue(value), CultureInfo.InvariantCulture)));
        }
        return rows.OrderBy(x => x.Date).ThenBy(x => x.Dimension, StringComparer.Ordinal).ToArray();
    }

    public static KpiRun CreateRun(ProjectionData data, KpiDefinition definition, IReadOnlyList<KpiPoint> raw)
    {
        // Parse only once; repeatedly reparsing the complete projection for each
        // month-to-date point is prohibitively expensive on the evaluation machine.
        using var document = System.Text.Json.JsonDocument.Parse(data.Json);
        var monthStarts = document.RootElement.GetProperty("cal").EnumerateArray().ToDictionary(
            x => DateOnly.ParseExact(x.GetProperty("d").GetString()!, "yyyy-MM-dd", CultureInfo.InvariantCulture),
            x => x.GetProperty("day_in_month").GetInt32());
        var points = raw.Select(p => IsIncomplete(data, definition, p.Date, monthStarts)
            ? p with { Value = null, Status = "data_unavailable" }
            : p.Value is null ? p with { Status = "no_population" } : p).ToList();
        // A missing source must never disappear merely because its SQL produced no row.
        foreach (var day in monthStarts.Keys.Order())
            if (!points.Any(p => p.Date == day) && IsIncomplete(data, definition, day, monthStarts))
                points.Add(new(day, null, null, "data_unavailable"));
        var sorted = points.OrderBy(p => p.Date).ThenBy(p => p.Dimension, StringComparer.Ordinal).ToArray();
        return new(IntakeFingerprint.Of(new { data.Snapshot.Id, Definition = definition.Id, data.Hash }),
            data.Snapshot.Id, definition.Id, definition.KpiId, definition.Unit, definition.Precision,
            data.Hash, definition.PostgreSql, sorted, IntakeFingerprint.Of(sorted));
    }

    private static bool IsIncomplete(ProjectionData data, KpiDefinition definition, DateOnly date,
        IReadOnlyDictionary<DateOnly, int> monthStarts)
    {
        var start = definition.Window switch
        {
            KpiWindow.Rolling7 => date.AddDays(-6),
            KpiWindow.Rolling30 => date.AddDays(-29),
            KpiWindow.History => DateOnly.MinValue,
            KpiWindow.MonthToDate => monthStarts.TryGetValue(date, out var dayOfMonth)
                ? date.AddDays(1 - dayOfMonth) : date,
            _ => date
        };
        return data.Snapshot.Issues.Any(i => (i.Type is "missing" or "invalid") &&
            definition.Dependencies.Contains(i.Source) &&
            (i.EffectiveDate is null || i.EffectiveDate >= start && i.EffectiveDate <= date));
    }

}
