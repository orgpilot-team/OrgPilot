namespace OrgPilot.Foundation.Configuration;

// The Configuration Service exposes only version references across the process boundary.
public sealed record KpiVersionReference(string KpiId, string DefinitionId);
public sealed record ManagerPriorityVersionReference(string ManagerId, string CandidateId);
public sealed record ConfigurationVersionReferences(int BusinessDay, string Version,
    string? OrganizationRevisionId, IReadOnlyList<KpiVersionReference> KpiVersions,
    IReadOnlyList<ManagerPriorityVersionReference> ManagerPriorities,
    IReadOnlyList<string> CandidateIds);
