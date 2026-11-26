using System.Diagnostics;
using System.Text.Json;
using Microsoft.EntityFrameworkCore;

namespace OrgPilot.BackendApi.Modules.Configuration;

public sealed class ConfigurationService(ConfigurationDbContext db, IConfigurationAuthority authority,
    ConfigurationValidator validator)
{
    public async Task<ConfigurationCandidate> SubmitAsync<T>(CandidateKind kind, string key, int businessDay,
        string actorId, string commandId, T payload, CancellationToken cancellationToken = default)
    {
        if (businessDay < 1 || string.IsNullOrWhiteSpace(key) || string.IsNullOrWhiteSpace(commandId))
            throw new ArgumentException("An explicit command identity, key and business day are required.");
        await authority.DemandAsync(actorId, kind, key, cancellationToken);
        var candidate = new ConfigurationCandidate("", kind, key, businessDay, checked(businessDay + 1),
            actorId, commandId, JsonSerializer.Serialize(payload));
        candidate = candidate with { Id = ConfigurationFingerprint.Of(candidate) };
        var json = JsonSerializer.Serialize(candidate);
        await db.Database.ExecuteSqlInterpolatedAsync($"""
            INSERT INTO configuration.candidates ("Id", "CommandId", "EffectiveDay", "Payload", "TraceId")
            VALUES ({candidate.Id}, {commandId}, {candidate.EffectiveDay}, CAST({json} AS jsonb),
                {Activity.Current?.TraceId.ToString() ?? ""})
            ON CONFLICT ("CommandId") DO NOTHING
            """, cancellationToken);
        var row = await db.Candidates.AsNoTracking().SingleAsync(x => x.CommandId == commandId, cancellationToken);
        if (row.Id != candidate.Id) throw new InvalidOperationException("Command identity reused with different payload.");
        return candidate;
    }

    public async Task ApproveAsync(string candidateId, string actorId, int businessDay,
        CancellationToken cancellationToken = default)
    {
        var row = await db.Candidates.AsNoTracking().SingleAsync(x => x.Id == candidateId, cancellationToken);
        var candidate = Read(row.Payload);
        await authority.DemandAsync(actorId, candidate.Kind, candidate.Key, cancellationToken);
        if (businessDay != candidate.SubmittedDay)
            throw new InvalidOperationException("Late approval cannot retroactively activate a candidate; submit a new version.");
        var validation = await validator.ValidateAsync(candidate, cancellationToken);
        var approval = new ConfigurationApproval(candidateId, actorId, businessDay, validation);
        var json = JsonSerializer.Serialize(approval);
        await db.Database.ExecuteSqlInterpolatedAsync($"""
            INSERT INTO configuration.approvals ("CandidateId", "ApprovedDay", "Payload", "TraceId")
            VALUES ({candidateId}, {businessDay}, CAST({json} AS jsonb), {Activity.Current?.TraceId.ToString() ?? ""})
            ON CONFLICT ("CandidateId") DO NOTHING
            """, cancellationToken);
    }

    public async Task<ActiveConfiguration> ResolveAsync(int businessDay, CancellationToken cancellationToken = default)
    {
        var rows = await (from c in db.Candidates.AsNoTracking()
                          join a in db.Approvals.AsNoTracking() on c.Id equals a.CandidateId
                          where c.EffectiveDay <= businessDay && a.ApprovedDay < businessDay
                          select c.Payload).ToListAsync(cancellationToken);
        var ordered = rows.Select(Read).GroupBy(c => (c.Kind, c.Key))
            .Select(g => g.OrderByDescending(c => c.EffectiveDay).ThenByDescending(c => c.CommandId, StringComparer.Ordinal).First())
            .OrderBy(c => c.Kind).ThenBy(c => c.Key, StringComparer.Ordinal).ToArray();
        return new(ConfigurationFingerprint.Of(ordered.Select(c => c.Id).ToArray()), businessDay, Array.AsReadOnly(ordered));
    }

    private static ConfigurationCandidate Read(string payload) =>
        JsonSerializer.Deserialize<ConfigurationCandidate>(payload) ?? throw new InvalidDataException("Invalid candidate record.");
}
