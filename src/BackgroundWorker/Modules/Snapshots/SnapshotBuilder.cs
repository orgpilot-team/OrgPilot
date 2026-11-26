using OrgPilot.BackgroundWorker.Modules.Intake;

namespace OrgPilot.BackgroundWorker.Modules.Snapshots;

public sealed record PinnedVersions(string Organization, string Policy, string KpiDefinitions,
    string Configuration, string Calendar, string ManagerPriority);

public sealed record DailySnapshot(string Id, int ReportDay, DateOnly Cutoff, PinnedVersions Versions,
    IReadOnlyList<string> BatchIds, IReadOnlyList<CanonicalFact> Facts, IReadOnlyList<IntakeIssue> Issues);

public static class SnapshotBuilder
{
    public static DailySnapshot Build(int reportDay, DateOnly cutoff, PinnedVersions versions,
        IEnumerable<IngestionBatch> batches)
    {
        if (reportDay < 1) throw new ArgumentOutOfRangeException(nameof(reportDay));
        if (new[] { versions.Organization, versions.Policy, versions.KpiDefinitions, versions.Configuration,
                versions.Calendar, versions.ManagerPriority }.Any(string.IsNullOrWhiteSpace))
            throw new ArgumentException("Every version must be pinned.", nameof(versions));

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
            var arrival = facts.Where(f => f.Source == issue.Source && f.EffectiveDate == issue.EffectiveDate &&
                    f.DropDay > issue.DropDay).Select(f => (int?)f.DropDay).Min();
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
