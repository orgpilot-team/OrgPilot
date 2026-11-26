using System.Globalization;
using System.Text;
using System.Text.Json;
using Microsoft.VisualBasic.FileIO;
using OrgPilot.Foundation.Archive;

namespace OrgPilot.BackgroundWorker.Modules.Intake;

public sealed class IngestionCoordinator(IProtectedFileArchive archive)
{
    private static readonly HashSet<string> Numeric = new(StringComparer.Ordinal)
    {
        "items", "order_value_toman", "amount_toman", "sessions", "score",
        "contract_value_toman", "spend_toman", "impressions", "clicks", "leads"
    };

    private static readonly HashSet<string> Optional = new(StringComparer.Ordinal)
    {
        "campaign_id", "amount_toman", "contract_value_toman", "order_id", "blocker_fa"
    };

    public async Task<IngestionBatch> ReadAsync(string dataDirectory, int dropDay,
        DateOnly cutoff, CancellationToken cancellationToken = default)
    {
        var drop = await new DropIntakeReader(archive).ReadAsync(dataDirectory, dropDay, cancellationToken);
        if (drop.BusinessDate > cutoff)
            throw new InvalidDataException("The drop is outside the pinned cutoff.");
        var facts = new List<CanonicalFact>();
        var issues = new List<IntakeIssue>();
        foreach (var source in drop.Sources)
        {
            if (source.Status != SourceReadStatus.ReadyForNormalization || source.Archive is null)
            {
                issues.Add(new(source.Source, source.Status == SourceReadStatus.Missing ? "missing" : "invalid",
                    dropDay, drop.BusinessDate, source.IssueCode ?? "invalid_source"));
                continue;
            }

            await using var stream = await archive.OpenVerifiedAsync(source.Archive, cancellationToken);
            using var parser = new TextFieldParser(stream, new UTF8Encoding(false, true),
                detectEncoding: false, leaveOpen: true);
            parser.SetDelimiters(",");
            parser.HasFieldsEnclosedInQuotes = true;
            parser.TrimWhiteSpace = false;
            var header = parser.ReadFields() ?? throw new InvalidDataException("Missing CSV header.");
            header[0] = header[0].TrimStart('\uFEFF');
            var schema = SourceSchemaRegistry.Select(source.Source, header)
                ?? throw new InvalidDataException("Archived schema changed.");
            var positions = header.Select((name, index) => (name, index))
                .ToDictionary(x => x.name, x => x.index, StringComparer.Ordinal);
            var recordNumber = 0;
            while (!parser.EndOfData)
            {
                cancellationToken.ThrowIfCancellationRequested();
                recordNumber++;
                var fields = parser.ReadFields() ?? throw new InvalidDataException("Invalid archived CSV.");
                try
                {
                    var values = new SortedDictionary<string, object?>(StringComparer.Ordinal);
                    foreach (var column in schema.Columns)
                        values.Add(column, Normalize(column, fields[positions[column]], schema.KeyColumns.Contains(column)));
                    var dateColumn = schema.Columns.Contains("at") ? "at" :
                        schema.Columns.Contains("created_at") ? "created_at" :
                        schema.Columns.Contains("answered_at") ? "answered_at" : "date";
                    var date = DateOnly.ParseExact(((string)values[dateColumn]!)[..10], "yyyy-MM-dd", CultureInfo.InvariantCulture);
                    if (date > cutoff || (drop.BusinessDate is { } day && date > day))
                        throw new FormatException("future_record");
                    var key = JsonSerializer.Serialize(schema.KeyColumns.Select(column => values[column]));
                    facts.Add(new(source.Source, key, date, dropDay, schema.Version, source.Archive,
                        recordNumber, JsonSerializer.Serialize(values)));
                }
                catch (FormatException ex)
                {
                    issues.Add(new(source.Source, "invalid", dropDay, drop.BusinessDate, ex.Message, recordNumber));
                }
            }
        }

        var id = IntakeFingerprint.Of(new { drop, cutoff, NormalizationVersion = "baseline-v1" });
        return new(id, drop, facts.AsReadOnly(), issues.AsReadOnly());
    }

    private static object? Normalize(string column, string value, bool key)
    {
        if (value.Length == 0)
        {
            if (!key && Optional.Contains(column)) return null;
            throw new FormatException("required_value_missing:" + column);
        }

        if (Numeric.Contains(column))
        {
            if (!long.TryParse(value, NumberStyles.AllowLeadingSign, CultureInfo.InvariantCulture, out var number))
                throw new FormatException("invalid_integer:" + column);
            if ((column == "score" && (number < 1 || number > 5)) ||
                (column != "amount_toman" && number < 0))
                throw new FormatException("invalid_range:" + column);
            return number;
        }
        if (column is "date" or "due_date")
        {
            if (!DateOnly.TryParseExact(value, "yyyy-MM-dd", CultureInfo.InvariantCulture, DateTimeStyles.None, out var date))
                throw new FormatException("invalid_date:" + column);
            return date.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture);
        }
        if (column is "created_at" or "at" or "answered_at" or "promised_by")
        {
            if (!DateTime.TryParseExact(value, "yyyy-MM-dd HH:mm:ss", CultureInfo.InvariantCulture,
                    DateTimeStyles.None, out var date))
                throw new FormatException("invalid_local_timestamp:" + column);
            // Dataset timestamps are business-local civil time (Asia/Tehran), not host-local time.
            return date.ToString("yyyy-MM-dd HH:mm:ss", CultureInfo.InvariantCulture);
        }
        return value;
    }
}
