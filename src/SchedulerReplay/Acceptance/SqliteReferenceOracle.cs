using System.Globalization;
using System.Text.Json;
using Microsoft.Data.Sqlite;
using OrgPilot.BackgroundWorker.Modules.Kpi;
using OrgPilot.BackgroundWorker.Modules.Snapshots;

namespace OrgPilot.Acceptance;

public sealed class SqliteReferenceOracle : IAsyncDisposable
{
    private readonly SqliteConnection _connection = new("Data Source=:memory:");

    public async Task InitializeAsync(ProjectionData projection, string referenceViews,
        CancellationToken cancellationToken = default)
    {
        await _connection.OpenAsync(cancellationToken);
        _connection.CreateAggregate<double?, List<double>, double?>("median", [],
            (values, value) =>
            {
                // Never mutate the seed shared by groups.
                if (value is null) return values;
                var result = new List<double>(values) { value.Value };
                return result;
            },
            values =>
            {
                if (values.Count == 0) return null;
                values.Sort();
                var middle = values.Count / 2;
                return values.Count % 2 == 0 ? (values[middle - 1] + values[middle]) / 2 : values[middle];
            });

        using var json = JsonDocument.Parse(projection.Json);
        await using var transaction = (SqliteTransaction)await _connection.BeginTransactionAsync(cancellationToken);
        foreach (var table in ProjectionData.Tables)
        {
            await using (var create = _connection.CreateCommand())
            {
                create.Transaction = transaction;
                create.CommandText = $"CREATE TABLE {table.Name} ({string.Join(", ", table.Columns.Select(c => $"\"{c.Name}\" {c.SqliteType}"))})";
                await create.ExecuteNonQueryAsync(cancellationToken);
            }
            await using var insert = _connection.CreateCommand();
            insert.Transaction = transaction;
            insert.CommandText = $"INSERT INTO {table.Name} VALUES ({string.Join(", ", table.Columns.Select((_, i) => "$p" + i))})";
            foreach (var column in table.Columns)
                insert.Parameters.Add(new SqliteParameter("$p" + insert.Parameters.Count, DBNull.Value));
            foreach (var row in json.RootElement.GetProperty(table.Name).EnumerateArray())
            {
                for (var i = 0; i < table.Columns.Count; i++)
                {
                    var value = row.GetProperty(table.Columns[i].Name);
                    insert.Parameters[i].Value = value.ValueKind switch
                    {
                        JsonValueKind.Null => DBNull.Value,
                        JsonValueKind.Number when value.TryGetInt64(out var integer) => integer,
                        JsonValueKind.Number => value.GetDouble(),
                        JsonValueKind.String => value.GetString()!,
                        _ => throw new InvalidDataException("Unexpected canonical value type.")
                    };
                }
                await insert.ExecuteNonQueryAsync(cancellationToken);
            }
        }
        await using (var views = _connection.CreateCommand())
        {
            views.Transaction = transaction;
            views.CommandText = referenceViews;
            await views.ExecuteNonQueryAsync(cancellationToken);
        }
        await transaction.CommitAsync(cancellationToken);
    }

    public async Task<IReadOnlyList<KpiPoint>> QueryAsync(KpiDefinition definition, DateOnly cutoff,
        CancellationToken cancellationToken = default)
    {
        if (!BaselineKpiSql.Definitions.TryGetValue(definition.KpiId, out var known) ||
            known.ReferenceSql != definition.ReferenceSql)
            throw new InvalidDataException("Only registered reference SQL is accepted.");
        await using var command = _connection.CreateCommand();
        command.CommandText = definition.ReferenceSql;
        await using var reader = await command.ExecuteReaderAsync(cancellationToken);
        var date = reader.GetOrdinal("d");
        var value = reader.GetOrdinal("value");
        var dim = definition.Dimension is null ? -1 : reader.GetOrdinal("dim");
        var rows = new List<KpiPoint>();
        while (await reader.ReadAsync(cancellationToken))
        {
            var day = DateOnly.ParseExact(reader.GetString(date), "yyyy-MM-dd", CultureInfo.InvariantCulture);
            if (day > cutoff) continue;
            rows.Add(new(day, dim < 0 || reader.IsDBNull(dim) ? null : reader.GetString(dim),
                reader.IsDBNull(value) ? null : Convert.ToDecimal(reader.GetValue(value), CultureInfo.InvariantCulture)));
        }
        return rows.OrderBy(x => x.Date).ThenBy(x => x.Dimension, StringComparer.Ordinal).ToArray();
    }

    public ValueTask DisposeAsync() => _connection.DisposeAsync();
}
