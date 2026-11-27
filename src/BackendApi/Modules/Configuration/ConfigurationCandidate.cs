using System.Security.Cryptography;
using System.Text.Json;

namespace OrgPilot.BackendApi.Modules.Configuration;

public enum CandidateKind { KpiDefinition, Organization, ManagerPriority }

public sealed record KpiChange(string KpiId, string DefinitionVersion, string ParityReceiptId);
public sealed record OrganizationUnit(string Id, string? ParentId, string ManagerId);
public sealed record OrganizationTeam(string Id, string UnitId, string ManagerId);
public sealed record OrganizationManager(string Id, string ScopeId);
public sealed record OrganizationStaff(string Id, string TeamId);
public sealed record OrganizationRevision(IReadOnlyList<OrganizationUnit> Units,
    IReadOnlyList<OrganizationTeam> Teams, IReadOnlyList<OrganizationManager> Managers,
    IReadOnlyList<OrganizationStaff> Staff);
public sealed record ManagerPriority(string ManagerId, IReadOnlyList<string> OrderedKpiIds);

public sealed record ConfigurationCandidate(string Id, CandidateKind Kind, string Key,
    int SubmittedDay, int EffectiveDay, string ActorId, string CommandId, string PayloadJson);
public sealed record ConfigurationApproval(string CandidateId, string ActorId, int ApprovedDay, string ValidationReference);
public sealed record ActiveConfiguration(string Version, int BusinessDay,
    IReadOnlyList<ConfigurationCandidate> Candidates);

public static class ConfigurationFingerprint
{
    public static string Of<T>(T value) => Convert.ToHexStringLower(
        SHA256.HashData(JsonSerializer.SerializeToUtf8Bytes(value)));
}

// The implementation must come from the trusted authorization boundary. No permissive
// default is registered; Stage 4 defines how replay supplies a trusted principal.
public interface IConfigurationAuthority
{
    Task DemandAsync(string actorId, CandidateKind kind, string key, CancellationToken cancellationToken);
}
