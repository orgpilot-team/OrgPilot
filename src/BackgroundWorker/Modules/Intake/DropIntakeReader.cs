using System.Globalization;
using System.Text;
using System.Text.Json;
using Microsoft.VisualBasic.FileIO;
using OrgPilot.Foundation.Archive;

namespace OrgPilot.BackgroundWorker.Modules.Intake;

public enum SourceReadStatus
{
    ReadyForNormalization,
    Missing,
    Invalid
}

public sealed record SourceRead(
    string Source,
    int? ExpectedRowCount,
    int? ActualRowCount,
    ArchiveReference? Archive,
    SourceReadStatus Status,
    string? IssueCode);

public sealed record DropRead(
    int DropDay,
    DateOnly? BusinessDate,
    ArchiveReference Manifest,
    IReadOnlyList<SourceRead> Sources);

/// <summary>
/// Reads one explicitly pinned drop, preserving the bytes before inspecting them.
/// This is the intake boundary, not a canonical batch or a persisted receipt.
/// </summary>
public sealed class DropIntakeReader(IProtectedFileArchive archive)
{
    private static readonly string[] DailySources =
    [
        "crm_lead_events", "crm_leads", "csat", "mkt_daily", "order_events",
        "orders", "staff_availability", "task_events", "tasks", "ticket_events",
        "tickets", "web_sessions"
    ];

    public async Task<DropRead> ReadAsync(
        string dataDirectory, int dropDay, CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(dataDirectory);
        ArgumentOutOfRangeException.ThrowIfNegative(dropDay);
        var root = Path.GetFullPath(dataDirectory);
        if (!Directory.Exists(root))
            throw new DirectoryNotFoundException("The configured input dataset does not exist.");

        var dropDirectory = Path.Combine(root, "drops", $"day_{dropDay.ToString("D3", CultureInfo.InvariantCulture)}");
        var manifestReference = await ArchiveFileAsync(Path.Combine(dropDirectory, "manifest.json"), cancellationToken);
        await using var manifestStream = await archive.OpenVerifiedAsync(manifestReference, cancellationToken);
        using var manifest = await JsonDocument.ParseAsync(manifestStream, cancellationToken: cancellationToken);
        var (businessDate, counts) = ReadManifest(manifest.RootElement, dropDay);

        string[] expectedSources = dropDay == 0 ? ["crm_lead_events", "crm_leads"] : DailySources;
        var expected = expectedSources.Select(source => source + ".csv").ToHashSet(StringComparer.Ordinal);
        var sources = new List<SourceRead>();

        foreach (var source in expectedSources)
        {
            cancellationToken.ThrowIfCancellationRequested();
            var name = source + ".csv";
            var path = Path.Combine(dropDirectory, name);
            var declared = counts.TryGetValue(name, out var expectedCount);
            int? count = declared ? expectedCount : null;
            if (!File.Exists(path))
            {
                sources.Add(new(source, count, null, null, SourceReadStatus.Missing, "missing"));
                continue;
            }

            var reference = await ArchiveFileAsync(path, cancellationToken);
            if (!declared)
            {
                sources.Add(new(source, null, null, reference, SourceReadStatus.Invalid, "unlisted_source"));
                continue;
            }

            try
            {
                await using var stream = await archive.OpenVerifiedAsync(reference, cancellationToken);
                var rowCount = CountRecords(stream, cancellationToken);
                var matches = rowCount == expectedCount;
                sources.Add(new(source, count, rowCount, reference,
                    matches ? SourceReadStatus.ReadyForNormalization : SourceReadStatus.Invalid,
                    matches ? null : "manifest_row_count_mismatch"));
            }
            catch (Exception ex) when (ex is MalformedLineException or DecoderFallbackException or InvalidDataException)
            {
                sources.Add(new(source, count, null, reference, SourceReadStatus.Invalid, "invalid_csv"));
            }
        }

        // Do not resolve arbitrary paths supplied by an untrusted manifest.
        foreach (var name in counts.Keys.Where(name => !expected.Contains(name)).Order(StringComparer.Ordinal))
            sources.Add(new(name, counts[name], null, null, SourceReadStatus.Invalid, "unknown_source"));

        return new(dropDay, businessDate, manifestReference, sources.AsReadOnly());
    }

    private async Task<ArchiveReference> ArchiveFileAsync(string path, CancellationToken cancellationToken)
    {
        await using var stream = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.Read,
            81920, FileOptions.Asynchronous | FileOptions.SequentialScan);
        return await archive.StoreAsync(stream, cancellationToken);
    }

    private static (DateOnly? Date, Dictionary<string, int> Counts) ReadManifest(JsonElement root, int dropDay)
    {
        if (root.ValueKind != JsonValueKind.Object ||
            !root.TryGetProperty("drop_day", out var day) ||
            day.ValueKind != JsonValueKind.Number || !day.TryGetInt32(out var actualDay) || actualDay != dropDay ||
            !root.TryGetProperty("date", out var date) || date.ValueKind != JsonValueKind.String ||
            !root.TryGetProperty("files", out var files) || files.ValueKind != JsonValueKind.Object)
            throw new InvalidDataException("Invalid drop manifest or mismatched drop day.");

        DateOnly? businessDate = null;
        if (dropDay == 0)
        {
            if (date.GetString() != "initial_load")
                throw new InvalidDataException("The initial drop must be identified as initial_load.");
        }
        else
        {
            if (!DateOnly.TryParseExact(date.GetString(), "yyyy-MM-dd", CultureInfo.InvariantCulture,
                    DateTimeStyles.None, out var parsed))
                throw new InvalidDataException("Invalid manifest business date.");
            businessDate = parsed;
        }

        // The supplied dataset manifest contains file names and row counts, not expected SHA-256 hashes.
        // ArchiveReference carries the computed SHA-256 and size; reopening verifies the archived bytes.
        var counts = new Dictionary<string, int>(StringComparer.Ordinal);
        foreach (var file in files.EnumerateObject())
        {
            if (file.Value.ValueKind != JsonValueKind.Number || !file.Value.TryGetInt32(out var count) ||
                count < 0 || !counts.TryAdd(file.Name, count))
                throw new InvalidDataException("Invalid or duplicate manifest file entry.");
        }
        return (businessDate, counts);
    }

    private static int CountRecords(Stream stream, CancellationToken cancellationToken)
    {
        using var parser = new TextFieldParser(stream, new UTF8Encoding(false, true),
            detectEncoding: false, leaveOpen: true);
        parser.SetDelimiters(",");
        parser.HasFieldsEnclosedInQuotes = true;
        parser.TrimWhiteSpace = false;
        var header = parser.ReadFields();
        if (header is null || header.Length == 0)
            throw new InvalidDataException("CSV header is missing.");

        var count = 0;
        while (!parser.EndOfData)
        {
            cancellationToken.ThrowIfCancellationRequested();
            var fields = parser.ReadFields();
            if (fields is null || fields.Length != header.Length)
                throw new InvalidDataException("CSV field count does not match its header.");
            count = checked(count + 1);
        }
        return count;
    }
}
