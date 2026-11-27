using OrgPilot.BackgroundWorker.Modules.Intake;
using OrgPilot.Foundation.Archive;

namespace OrgPilot.BackgroundWorker.Modules.Snapshots;

// Keep the individual archive addresses, not just the combined version hashes.
// A historical snapshot can therefore reopen its own inputs after a source changes.
public sealed record SnapshotInputReferences(ArchiveReference Calendar, ArchiveReference MonthlyTargets,
    ArchiveReference KpiDictionary, ArchiveReference ReferenceViews, ArchiveReference EscalationRules,
    ArchiveReference WorkflowDefinitions, ArchiveReference Units, ArchiveReference Teams,
    ArchiveReference Managers, ArchiveReference Staff, ArchiveReference AccessMatrix)
{
    public string OrganizationHash() => IntakeFingerprint.Of(new[] { Units, Teams, Managers, Staff, AccessMatrix });

    public string PolicyHash() => IntakeFingerprint.Of(new[] { ReferenceViews, EscalationRules, WorkflowDefinitions });

    public static async Task<SnapshotInputReferences> PinAsync(string dataDirectory, IProtectedFileArchive archive,
        CancellationToken cancellationToken = default)
    {
        async Task<ArchiveReference> PinFileAsync(string path)
        {
            await using var stream = File.OpenRead(Path.Combine(dataDirectory, path));
            return await archive.StoreAsync(stream, cancellationToken);
        }

        return new(await PinFileAsync("calendar/calendar_days.csv"),
            await PinFileAsync("config/monthly_targets.csv"),
            await PinFileAsync("config/kpi_dictionary.csv"),
            await PinFileAsync("config/reference_views.sql"),
            await PinFileAsync("config/escalation_rules.csv"),
            await PinFileAsync("config/workflow_definitions.csv"),
            await PinFileAsync("org/units.csv"),
            await PinFileAsync("org/teams.csv"),
            await PinFileAsync("org/managers.csv"),
            await PinFileAsync("org/staff.csv"),
            await PinFileAsync("org/access_matrix.csv"));
    }
}
