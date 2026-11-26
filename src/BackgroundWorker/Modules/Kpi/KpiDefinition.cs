using System.Globalization;
using System.Text;
using Microsoft.VisualBasic.FileIO;
using OrgPilot.BackgroundWorker.Modules.Intake;
using OrgPilot.Foundation.Archive;

namespace OrgPilot.BackgroundWorker.Modules.Kpi;

public sealed record KpiDefinition(string Id, string KpiId, string EntityId, string Name, string Unit,
    int Direction, string Rule, decimal? Target, decimal? Warn, decimal? Crit, int EscalateAfterDays,
    string? Dimension, string Owner, int? Precision, string ReferenceSql, string PostgreSql,
    IReadOnlyList<string> Dependencies, KpiWindow Window, string DictionaryHash);

public static class KpiDefinitionReader
{
    public static async Task<IReadOnlyList<KpiDefinition>> ReadAsync(IProtectedFileArchive archive,
        ArchiveReference dictionary, CancellationToken cancellationToken = default)
    {
        await using var stream = await archive.OpenVerifiedAsync(dictionary, cancellationToken);
        using var parser = new TextFieldParser(stream, new UTF8Encoding(false, true), false, true);
        parser.SetDelimiters(",");
        parser.HasFieldsEnclosedInQuotes = true;
        parser.TrimWhiteSpace = false;
        var header = parser.ReadFields() ?? throw new InvalidDataException("Missing KPI dictionary header.");
        header[0] = header[0].TrimStart('\uFEFF');
        var expected = "kpi_id name_fa entity_id unit direction rule target warn crit escalate_after_days sql dim owner_manager_id".Split(' ');
        if (!header.SequenceEqual(expected)) throw new InvalidDataException("Unknown KPI dictionary schema.");
        var definitions = new List<KpiDefinition>();
        var ids = new HashSet<string>(StringComparer.Ordinal);
        while (!parser.EndOfData)
        {
            cancellationToken.ThrowIfCancellationRequested();
            var row = parser.ReadFields() ?? throw new InvalidDataException("Invalid KPI row.");
            if (row.Length != expected.Length || !ids.Add(row[0]) ||
                !BaselineKpiSql.Definitions.TryGetValue(row[0], out var translation) ||
                translation.ReferenceSql != row[10])
                throw new InvalidDataException("Unregistered or changed KPI reference SQL.");
            var direction = int.Parse(row[4], CultureInfo.InvariantCulture);
            var escalation = int.Parse(row[9], CultureInfo.InvariantCulture);
            if (direction is not (1 or -1) || escalation < 0) throw new InvalidDataException("Invalid KPI metadata.");
            var match = System.Text.RegularExpressions.Regex.Match(row[10], @",\s*(\d+)\)\s+value\b", System.Text.RegularExpressions.RegexOptions.IgnoreCase);
            int? precision = match.Success ? int.Parse(match.Groups[1].Value, CultureInfo.InvariantCulture) :
                row[10].Contains("COUNT(", StringComparison.OrdinalIgnoreCase) ? 0 : null;
            var definition = new KpiDefinition("", row[0], row[2], row[1], row[3], direction, row[5],
                DecimalOrNull(row[6]), DecimalOrNull(row[7]), DecimalOrNull(row[8]), escalation,
                row[11].Length == 0 ? null : row[11], row[12], precision, row[10], translation.PostgreSql,
                Array.AsReadOnly(translation.Dependencies.ToArray()), translation.Window, dictionary.Sha256);
            definitions.Add(definition with { Id = IntakeFingerprint.Of(definition) });
        }
        return definitions.OrderBy(x => x.KpiId, StringComparer.Ordinal).ToArray();
    }

    private static decimal? DecimalOrNull(string value) =>
        value.Length == 0 ? null : decimal.Parse(value, CultureInfo.InvariantCulture);
}
