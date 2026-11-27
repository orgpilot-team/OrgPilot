using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using OrgPilot.Foundation.Configuration;

namespace OrgPilot.BackendApi.Modules.Configuration;

public sealed class ConfigurationVersionReader(ConfigurationDbContext db)
{
    public async Task<ActiveConfiguration> ResolveAsync(int businessDay, CancellationToken cancellationToken = default)
    {
        var rows = await (from c in db.Candidates.AsNoTracking()
                          join a in db.Approvals.AsNoTracking() on c.Id equals a.CandidateId
                          where c.EffectiveDay <= businessDay && a.ApprovedDay < businessDay
                          select c.Payload).ToListAsync(cancellationToken);
        return Select(businessDay, rows.Select(json => JsonSerializer.Deserialize<ConfigurationCandidate>(json)
            ?? throw new InvalidDataException("Invalid candidate record.")));
    }

    // Only approved candidates enter this selection. Keeping it pure also enables deterministic
    // regression checks without constructing an authorization provider or a product database.
    public static ActiveConfiguration Select(int businessDay, IEnumerable<ConfigurationCandidate> approvedCandidates)
    {
        ArgumentOutOfRangeException.ThrowIfLessThan(businessDay, 1);
        var ordered = approvedCandidates.Where(c => c.EffectiveDay <= businessDay)
            .GroupBy(c => (c.Kind, c.Key))
            .Select(g => g.OrderByDescending(c => c.EffectiveDay)
                .ThenByDescending(c => c.CommandId, StringComparer.Ordinal).First())
            .OrderBy(c => c.Kind).ThenBy(c => c.Key, StringComparer.Ordinal).ToArray();
        return new(ConfigurationFingerprint.Of(ordered.Select(c => c.Id).ToArray()),
            businessDay, Array.AsReadOnly(ordered));
    }

    public static ConfigurationVersionReferences References(ActiveConfiguration active)
    {
        var kpis = active.Candidates.Where(c => c.Kind == CandidateKind.KpiDefinition)
            .Select(c =>
            {
                var change = JsonSerializer.Deserialize<KpiChange>(c.PayloadJson)
                    ?? throw new InvalidDataException("Invalid active KPI candidate.");
                return new KpiVersionReference(change.KpiId, change.DefinitionVersion);
            }).OrderBy(v => v.KpiId, StringComparer.Ordinal).ToArray();
        var priorities = active.Candidates.Where(c => c.Kind == CandidateKind.ManagerPriority)
            .Select(c => new ManagerPriorityVersionReference(c.Key, c.Id))
            .OrderBy(v => v.ManagerId, StringComparer.Ordinal).ToArray();
        return new(active.BusinessDay, active.Version,
            active.Candidates.SingleOrDefault(c => c.Kind == CandidateKind.Organization)?.Id,
            Array.AsReadOnly(kpis), Array.AsReadOnly(priorities),
            Array.AsReadOnly(active.Candidates.Select(c => c.Id).ToArray()));
    }
}
