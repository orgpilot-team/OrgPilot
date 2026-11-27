using OrgPilot.BackgroundWorker.Modules.Intake;
using OrgPilot.BackgroundWorker.Modules.Kpi;
using OrgPilot.Foundation.Configuration;

namespace OrgPilot.BackgroundWorker.Modules.Snapshots;

public static class SnapshotVersionPinning
{
    public static PinnedVersions Create(int reportDay, SnapshotInputReferences sources, IEnumerable<KpiDefinition> baseline,
        ConfigurationVersionReferences active)
    {
        if (active.BusinessDay != reportDay || IntakeFingerprint.Of(active.CandidateIds) != active.Version)
            throw new InvalidDataException("Configuration must be resolved for the pinned report day.");
        var dictionary = sources.KpiDictionary.Sha256;
        var versions = baseline.ToDictionary(d => d.KpiId, d =>
        {
            if (d.DictionaryHash != dictionary)
                throw new InvalidDataException("Definition does not belong to the pinned baseline dictionary.");
            return new KpiVersionReference(d.KpiId, d.Id);
        }, StringComparer.Ordinal);
        foreach (var change in active.KpiVersions)
        {
            if (!versions.ContainsKey(change.KpiId))
                throw new InvalidDataException("Configuration references an unknown baseline KPI.");
            versions[change.KpiId] = change;
        }
        var ordered = Array.AsReadOnly(versions.Values.OrderBy(v => v.KpiId, StringComparer.Ordinal).ToArray());
        return new(active.OrganizationRevisionId ?? sources.OrganizationHash(), sources.PolicyHash(), IntakeFingerprint.Of(ordered),
            active.Version, sources.Calendar.Sha256, IntakeFingerprint.Of(active.ManagerPriorities))
        {
            KpiDictionary = dictionary,
            MonthlyTargets = sources.MonthlyTargets.Sha256,
            KpiVersions = ordered,
            ActiveConfiguration = active,
            Sources = sources
        };
    }
}
