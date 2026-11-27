using OrgPilot.BackgroundWorker.Modules.Intake;
using OrgPilot.Foundation.Configuration;
using System.Text.Json.Serialization;

namespace OrgPilot.BackgroundWorker.Modules.Snapshots;

public sealed record PinnedVersions(string Organization, string Policy, string KpiDefinitions,
    string Configuration, string Calendar, string ManagerPriority)
{
    // The additional references distinguish the active version set from the baseline
    // dictionary and target files. Omitted fields preserve older snapshot identities.
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public string? KpiDictionary { get; init; }
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public string? MonthlyTargets { get; init; }
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public IReadOnlyList<KpiVersionReference>? KpiVersions { get; init; }
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public ConfigurationVersionReferences? ActiveConfiguration { get; init; }
    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public SnapshotInputReferences? Sources { get; init; }
}

public sealed record DailySnapshot(string Id, int ReportDay, DateOnly Cutoff, PinnedVersions Versions,
    IReadOnlyList<string> BatchIds, IReadOnlyList<CanonicalFact> Facts, IReadOnlyList<IntakeIssue> Issues)
{
    // Keep historical quality evidence for calculation and audit, but report duplicates only
    // on their affected morning (doc 15). Missing issues remain visible until the source arrives.
    public IReadOnlyList<IntakeIssue> ReportIssues => Issues
        .Where(issue => issue.Type != "duplicate" || issue.DropDay == ReportDay - 1)
        .ToArray();
}

public static class SnapshotBuilder
{
    public static DailySnapshot Build(int reportDay, DateOnly cutoff, PinnedVersions versions,
        IEnumerable<IngestionBatch> batches)
    {
        if (reportDay < 1) throw new ArgumentOutOfRangeException(nameof(reportDay));
        if (new[] { versions.Organization, versions.Policy, versions.KpiDefinitions, versions.Configuration,
                versions.Calendar, versions.ManagerPriority }.Any(string.IsNullOrWhiteSpace))
            throw new ArgumentException("Every version must be pinned.", nameof(versions));
        if (versions.ActiveConfiguration is { } active &&
            (active.BusinessDay != reportDay || active.Version != versions.Configuration ||
             IntakeFingerprint.Of(active.CandidateIds) != active.Version ||
             IntakeFingerprint.Of(active.ManagerPriorities) != versions.ManagerPriority ||
             versions.KpiVersions is null || IntakeFingerprint.Of(versions.KpiVersions) != versions.KpiDefinitions ||
             active.KpiVersions.Any(v => !versions.KpiVersions.Contains(v)) ||
             (active.OrganizationRevisionId is not null && active.OrganizationRevisionId != versions.Organization)))
            throw new InvalidDataException("Active configuration and snapshot versions disagree.");
        if (versions.Sources is { } sources &&
            (versions.Organization != (versions.ActiveConfiguration?.OrganizationRevisionId ?? sources.OrganizationHash()) ||
             versions.Policy != sources.PolicyHash() || versions.Calendar != sources.Calendar.Sha256 ||
             versions.KpiDictionary != sources.KpiDictionary.Sha256 ||
             versions.MonthlyTargets != sources.MonthlyTargets.Sha256))
            throw new InvalidDataException("Archived inputs and snapshot versions disagree.");

        var ordered = batches.OrderBy(b => b.Drop.DropDay).ToArray();
        if (!ordered.Select(b => b.Drop.DropDay).SequenceEqual(Enumerable.Range(0, reportDay)))
            throw new InvalidDataException("Exactly one version per drop through report day minus one is required.");
        if (ordered.Any(b => b.Drop.BusinessDate > cutoff))
            throw new InvalidDataException("A future drop cannot enter a snapshot.");

        var issues = ordered.SelectMany(b => b.Issues).Where(i => i.Type != "missing").ToList();
        var facts = new List<CanonicalFact>();
        foreach (var group in ordered.SelectMany(b => b.Facts)
                     .GroupBy(f => (f.Source, f.Key))
                     .OrderBy(g => g.Key.Source, StringComparer.Ordinal)
                     .ThenBy(g => g.Key.Key, StringComparer.Ordinal))
        {
            var candidates = group.OrderBy(f => f.DropDay).ThenBy(f => f.RecordNumber).ToArray();
            if (candidates.Any(f => f.EffectiveDate > cutoff))
                throw new InvalidDataException("Future canonical fact in snapshot.");
            if (candidates.Select(f => f.ValuesJson).Distinct(StringComparer.Ordinal).Count() != 1)
            {
                // Do not silently choose between conflicting rows. Explicit correction events have their own keys.
                issues.Add(new(group.Key.Source, "invalid", candidates[^1].DropDay,
                    candidates[^1].EffectiveDate, "conflicting_key"));
                continue;
            }
            facts.Add(candidates[0]);
            foreach (var duplicateDrop in candidates.Skip(1).GroupBy(f => f.DropDay))
                issues.Add(new(group.Key.Source, "duplicate", duplicateDrop.Key,
                    duplicateDrop.First().EffectiveDate, "duplicate_key"));
        }

        foreach (var issue in ordered.SelectMany(b => b.Issues).Where(i => i.Type == "missing"))
        {
            // Baseline drop format declares row counts, not original missing-day coverage.
            // Treat observed later records for the missing source/date as arrival evidence.
            // A later file with invalid records or conflicting canonical keys is not
            // evidence of a successful arrival. The manifest does not supply the
            // original missing-file count, so complete coverage cannot be inferred.
            var invalidDrops = issues.Where(i => i.Source == issue.Source && i.Type == "invalid")
                .Select(i => i.DropDay).ToHashSet();
            var arrival = facts.Where(f => f.Source == issue.Source && f.EffectiveDate == issue.EffectiveDate &&
                    f.DropDay > issue.DropDay && !invalidDrops.Contains(f.DropDay))
                .Select(f => (int?)f.DropDay).Min();
            if (arrival is null)
                issues.Add(issue);
            else if (arrival == reportDay - 1)
                issues.Add(issue with { Type = "late_arrival", DropDay = arrival.Value, Code = "late_source_records" });
        }

        var ids = ordered.Select(b => b.Id).ToArray();
        var id = IntakeFingerprint.Of(new { reportDay, cutoff, versions, ids });
        var stableIssues = issues.Distinct().OrderBy(i => i.DropDay).ThenBy(i => i.Source, StringComparer.Ordinal)
            .ThenBy(i => i.Type, StringComparer.Ordinal).ThenBy(i => i.RecordNumber).ToArray();
        return new(id, reportDay, cutoff, versions, Array.AsReadOnly(ids),
            facts.AsReadOnly(), Array.AsReadOnly(stableIssues));
    }
}
