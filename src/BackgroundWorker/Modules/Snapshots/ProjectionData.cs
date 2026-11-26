using System.Globalization;
using System.Text;
using System.Text.Json;
using Microsoft.VisualBasic.FileIO;
using OrgPilot.BackgroundWorker.Modules.Intake;
using OrgPilot.Foundation.Archive;

namespace OrgPilot.BackgroundWorker.Modules.Snapshots;

public sealed record ProjectionColumn(string Name, string PostgreSqlType, string SqliteType);
public sealed record ProjectionTable(string Name, IReadOnlyList<ProjectionColumn> Columns);

public sealed class ProjectionData
{
    public static IReadOnlyList<ProjectionTable> Tables { get; } = Array.AsReadOnly(new[]
    {
        Table("orders", "order_id created_at:t channel city category items:n order_value_toman:n customer_id campaign_id promised_by:t"),
        Table("order_events", "order_id event at:t actor_team amount_toman:n"),
        Table("web_sessions", "date:d channel sessions:n"),
        Table("tickets", "ticket_id created_at:t category team_id order_id channel text_fa"),
        Table("ticket_events", "ticket_id event at:t staff_id"),
        Table("csat", "ticket_id answered_at:t score:n"),
        Table("crm_leads", "lead_id source created_at:t"),
        Table("crm_lead_events", "lead_id event at:t contract_value_toman:n drop_day:n"),
        Table("mkt_daily", "date:d source spend_toman:n impressions:n clicks:n leads:n"),
        Table("tasks", "task_id team_id owner_id created_at:t due_date:d title_fa blocker_fa"),
        Table("task_events", "task_id event at:t"),
        Table("staff_availability", "date:d staff_id team_id status"),
        Table("cal", "d:d day_idx:n jdate jmonth day_in_month:n mdays:n iwd:n is_holiday:n"),
        Table("monthly_targets", "jmonth scope target_million_toman:n")
    });

    public DailySnapshot Snapshot { get; }
    public string Json { get; }
    public string Hash { get; }

    private ProjectionData(DailySnapshot snapshot, string json)
    {
        Snapshot = snapshot;
        Json = json;
        Hash = IntakeFingerprint.Of(json);
    }

    public static async Task<ProjectionData> CreateAsync(DailySnapshot snapshot, IProtectedFileArchive archive,
        ArchiveReference calendar, ArchiveReference monthlyTargets, CancellationToken cancellationToken = default)
    {
        if (snapshot.Versions.Calendar != calendar.Sha256 || snapshot.Versions.Configuration != monthlyTargets.Sha256)
            throw new InvalidDataException("Calendar or baseline target version is not pinned by the snapshot.");

        var rows = Tables.ToDictionary(t => t.Name, _ => new List<SortedDictionary<string, object?>>(), StringComparer.Ordinal);
        foreach (var fact in snapshot.Facts)
        {
            cancellationToken.ThrowIfCancellationRequested();
            var values = JsonSerializer.Deserialize<SortedDictionary<string, object?>>(fact.ValuesJson)
                ?? throw new InvalidDataException("Invalid canonical fact.");
            if (fact.Source == "crm_lead_events") values["drop_day"] = fact.DropDay;
            rows[fact.Source].Add(values);
        }
        rows["cal"] = await ReadConfigAsync(archive, calendar, Tables.Single(t => t.Name == "cal"), cancellationToken);
        rows["cal"] = rows["cal"].Where(r => DateOnly.ParseExact((string)r["d"]!, "yyyy-MM-dd",
            CultureInfo.InvariantCulture) <= snapshot.Cutoff).OrderBy(r => (string)r["d"]!, StringComparer.Ordinal).ToList();
        if (snapshot.ReportDay > 1 && (rows["cal"].Count != snapshot.ReportDay - 1 ||
            !rows["cal"].Select(r => Convert.ToInt32(r["day_idx"], CultureInfo.InvariantCulture))
                .SequenceEqual(Enumerable.Range(1, snapshot.ReportDay - 1)) ||
            (string)rows["cal"][^1]["d"]! != snapshot.Cutoff.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture)))
            throw new InvalidDataException("Calendar and report cutoff disagree.");
        rows["monthly_targets"] = await ReadConfigAsync(archive, monthlyTargets,
            Tables.Single(t => t.Name == "monthly_targets"), cancellationToken);
        var relevantMonths = rows["cal"].Select(r => (string)r["jmonth"]!).ToHashSet(StringComparer.Ordinal);
        rows["monthly_targets"] = rows["monthly_targets"].Where(r => relevantMonths.Contains((string)r["jmonth"]!))
            .OrderBy(r => (string)r["jmonth"]!, StringComparer.Ordinal)
            .ThenBy(r => (string)r["scope"]!, StringComparer.Ordinal).ToList();
        return new(snapshot, JsonSerializer.Serialize(rows));
    }

    private static async Task<List<SortedDictionary<string, object?>>> ReadConfigAsync(IProtectedFileArchive archive,
        ArchiveReference reference, ProjectionTable table, CancellationToken cancellationToken)
    {
        await using var stream = await archive.OpenVerifiedAsync(reference, cancellationToken);
        using var parser = new TextFieldParser(stream, new UTF8Encoding(false, true), false, true);
        parser.SetDelimiters(",");
        parser.HasFieldsEnclosedInQuotes = true;
        parser.TrimWhiteSpace = false;
        var header = parser.ReadFields() ?? throw new InvalidDataException("Missing configuration header.");
        header[0] = header[0].TrimStart('\uFEFF');
        if (table.Name == "cal")
            header = header.Select(n => n == "date" ? "d" : n).ToArray();
        var names = table.Columns.Select(c => c.Name).ToHashSet(StringComparer.Ordinal);
        if (header.Length != names.Count || !names.SetEquals(header))
            throw new InvalidDataException("Unexpected configuration schema.");
        var rows = new List<SortedDictionary<string, object?>>();
        while (!parser.EndOfData)
        {
            cancellationToken.ThrowIfCancellationRequested();
            var fields = parser.ReadFields() ?? throw new InvalidDataException("Malformed configuration row.");
            if (fields.Length != header.Length) throw new InvalidDataException("Malformed configuration row.");
            var row = new SortedDictionary<string, object?>(StringComparer.Ordinal);
            for (var i = 0; i < header.Length; i++)
            {
                var column = table.Columns.Single(c => c.Name == header[i]);
                row.Add(column.Name, column.PostgreSqlType == "numeric"
                    ? decimal.Parse(fields[i], NumberStyles.Number, CultureInfo.InvariantCulture)
                    : fields[i]);
            }
            rows.Add(row);
        }
        return rows;
    }

    private static ProjectionTable Table(string name, string specification) => new(name,
        Array.AsReadOnly(specification.Split(' ').Select(s =>
        {
            var parts = s.Split(':');
            return new ProjectionColumn(parts[0], parts.ElementAtOrDefault(1) switch
            {
                "n" => "numeric", "d" => "date", "t" => "timestamp without time zone", _ => "text"
            }, parts.ElementAtOrDefault(1) == "n" ? "NUMERIC" : "TEXT");
        }).ToArray()));
}
