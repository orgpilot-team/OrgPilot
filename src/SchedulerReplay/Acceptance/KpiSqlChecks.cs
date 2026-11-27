using System.Globalization;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.Data.Sqlite;
using Npgsql;
using OrgPilot.BackgroundWorker.Modules.Kpi;

namespace OrgPilot.Acceptance;

internal static class KpiSqlChecks
{
    public static async Task RunAsync(string connectionString)
    {
        var translation = BaselineKpiSql.Definitions["K_RSP_FRT_2H_PCT"];
        var rows = new List<TicketRow>();
        // Include the known two-hour boundary, midnight crossings, and a leap day.
        var starts = new[]
        {
            new DateTime(2026, 9, 23, 17, 20, 0),
            new DateTime(2026, 10, 10, 0, 0, 0),
            new DateTime(2026, 11, 10, 23, 30, 0),
            new DateTime(2024, 2, 29, 12, 0, 0)
        };
        foreach (var start in starts)
        {
            var offsets = new[] { 7200, 7199, 7201 };
            for (var i = 0; i < offsets.Length; i++)
            {
                var created = start.AddDays(i * 2);
                rows.Add(new(Format(created), Format(created.AddSeconds(offsets[i])), "T_RSP"));
            }
        }
        rows.Add(new("2026-09-23 17:20:00", null, "T_RSP"));
        rows.Add(new("2026-09-23 17:20:00", "2026-09-23 17:21:00", "T_CMP"));

        await using var sqlite = new SqliteConnection("Data Source=:memory:");
        await sqlite.OpenAsync();
        await using (var create = sqlite.CreateCommand())
        {
            create.CommandText = "CREATE TABLE ticket_fact (created_at TEXT, first_response_at TEXT, team_id TEXT)";
            await create.ExecuteNonQueryAsync();
        }
        foreach (var row in rows)
        {
            await using var insert = sqlite.CreateCommand();
            insert.CommandText = "INSERT INTO ticket_fact VALUES ($created, $response, $team)";
            insert.Parameters.AddWithValue("$created", row.CreatedAt);
            insert.Parameters.AddWithValue("$response", (object?)row.FirstResponseAt ?? DBNull.Value);
            insert.Parameters.AddWithValue("$team", row.TeamId);
            await insert.ExecuteNonQueryAsync();
        }
        var expected = new Dictionary<DateOnly, decimal>();
        await using (var command = sqlite.CreateCommand())
        {
            command.CommandText = translation.ReferenceSql;
            await using var reader = await command.ExecuteReaderAsync();
            while (await reader.ReadAsync())
                expected.Add(DateOnly.ParseExact(reader.GetString(0), "yyyy-MM-dd", CultureInfo.InvariantCulture),
                    Convert.ToDecimal(reader.GetValue(1), CultureInfo.InvariantCulture));
        }
        await using var postgres = new NpgsqlConnection(connectionString);
        await postgres.OpenAsync();
        await using var transaction = await postgres.BeginTransactionAsync();
        await using (var settings = new NpgsqlCommand("SET TRANSACTION READ ONLY; SET LOCAL TIME ZONE 'Asia/Tehran'", postgres, transaction))
            await settings.ExecuteNonQueryAsync();
        var actual = new Dictionary<DateOnly, decimal>();
        await using (var command = new NpgsqlCommand("""
            WITH ticket_fact AS (
              SELECT * FROM jsonb_to_recordset(CAST(@rows AS jsonb)) AS t(
                created_at timestamp without time zone,
                first_response_at timestamp without time zone, team_id text)
            )
            """ + "\n" + translation.PostgreSql, postgres, transaction))
        {
            command.Parameters.AddWithValue("rows", JsonSerializer.Serialize(rows));
            await using var reader = await command.ExecuteReaderAsync();
            while (await reader.ReadAsync())
                actual.Add(reader.GetFieldValue<DateOnly>(0), reader.GetDecimal(1));
        }
        if (expected.Count != 12 || actual.Count != expected.Count ||
            expected[new DateOnly(2026, 9, 23)] != 0 ||
            expected.Any(point => !actual.TryGetValue(point.Key, out var value) || value != point.Value))
            throw new InvalidDataException("Two-hour KPI boundary translation differs from SQLite.");
        Console.WriteLine("PASS KPI two-hour boundaries: 12 PostgreSQL/SQLite cases; null and team filters");
    }

    private static string Format(DateTime value) => value.ToString("yyyy-MM-dd HH:mm:ss", CultureInfo.InvariantCulture);

    private sealed record TicketRow(
        [property: JsonPropertyName("created_at")] string CreatedAt,
        [property: JsonPropertyName("first_response_at")] string? FirstResponseAt,
        [property: JsonPropertyName("team_id")] string TeamId);
}
