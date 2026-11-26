using System.Text.Json;
using Npgsql;

namespace OrgPilot.BackendApi.Modules.Configuration;

public sealed class ConfigurationValidator(string connectionString)
{
    public async Task<string> ValidateAsync(ConfigurationCandidate candidate, CancellationToken cancellationToken)
    {
        switch (candidate.Kind)
        {
            case CandidateKind.KpiDefinition:
            {
                var change = Read<KpiChange>(candidate.PayloadJson);
                if (change.KpiId != candidate.Key)
                    throw new InvalidDataException("Candidate key differs from KPI ID.");
                await using var connection = new NpgsqlConnection(connectionString);
                await connection.OpenAsync(cancellationToken);
                await using var command = new NpgsqlCommand("""
                    SELECT d."Payload"::text, p."Payload"::text
                    FROM kpi.definitions d JOIN kpi.parity_receipts p ON p."DefinitionId" = d."Id"
                    WHERE d."Id"=@version AND p."Id"=@receipt
                    """, connection);
                command.Parameters.AddWithValue("version", change.DefinitionVersion);
                command.Parameters.AddWithValue("receipt", change.ParityReceiptId);
                await using var reader = await command.ExecuteReaderAsync(cancellationToken);
                if (!await reader.ReadAsync(cancellationToken))
                    throw new InvalidDataException("KPI version or parity receipt is absent.");
                using var definition = JsonDocument.Parse(reader.GetString(0));
                using var receipt = JsonDocument.Parse(reader.GetString(1));
                var d = definition.RootElement;
                var p = receipt.RootElement;
                if (!p.GetProperty("Passed").GetBoolean() ||
                    p.GetProperty("DefinitionId").GetString() != change.DefinitionVersion ||
                    d.GetProperty("KpiId").GetString() != change.KpiId)
                    throw new InvalidDataException("KPI version is not eligible.");
                var direction = d.GetProperty("Direction").GetInt32();
                var warn = Number(d, "Warn");
                var crit = Number(d, "Crit");
                var target = Number(d, "Target");
                if (direction is not (1 or -1) || (warn is null) != (crit is null) ||
                    (warn is { } w && crit is { } c && direction * (w - c) < 0) ||
                    (target is { } t && warn is { } warning && direction * (t - warning) < 0))
                    throw new InvalidDataException("Thresholds contradict KPI direction.");
                return change.ParityReceiptId;
            }
            case CandidateKind.Organization:
                if (candidate.Key != "ORG") throw new InvalidDataException("Organization revision must use ORG key.");
                ValidateOrganization(Read<OrganizationRevision>(candidate.PayloadJson));
                break;
            case CandidateKind.ManagerPriority:
            {
                var priority = Read<ManagerPriority>(candidate.PayloadJson);
                if (priority.ManagerId != candidate.Key || priority.OrderedKpiIds.Count == 0 ||
                    priority.OrderedKpiIds.Any(string.IsNullOrWhiteSpace) ||
                    priority.OrderedKpiIds.Distinct(StringComparer.Ordinal).Count() != priority.OrderedKpiIds.Count)
                    throw new InvalidDataException("Invalid manager priority.");
                await using var connection = new NpgsqlConnection(connectionString);
                await connection.OpenAsync(cancellationToken);
                foreach (var id in priority.OrderedKpiIds)
                {
                    await using var command = new NpgsqlCommand("""
                        SELECT EXISTS (SELECT 1 FROM kpi.definitions WHERE "Payload"->>'KpiId' = @id)
                        """, connection);
                    command.Parameters.AddWithValue("id", id);
                    if (await command.ExecuteScalarAsync(cancellationToken) is not true)
                        throw new InvalidDataException("Unknown manager priority KPI.");
                }
                break;
            }
            default: throw new InvalidDataException("Unknown candidate kind.");
        }
        return ConfigurationFingerprint.Of(new { candidate.Id, Validator = "configuration-v1" });
    }

    private static decimal? Number(JsonElement element, string name) =>
        element.GetProperty(name).ValueKind == JsonValueKind.Null ? null : element.GetProperty(name).GetDecimal();

    private static T Read<T>(string json) => JsonSerializer.Deserialize<T>(json)
        ?? throw new InvalidDataException("Missing candidate payload.");

    private static void ValidateOrganization(OrganizationRevision revision)
    {
        var units = revision.Units.ToDictionary(u => u.Id, StringComparer.Ordinal);
        var teams = revision.Teams.ToDictionary(t => t.Id, StringComparer.Ordinal);
        var managers = revision.Managers.ToDictionary(m => m.Id, StringComparer.Ordinal);
        var staff = revision.Staff.ToDictionary(s => s.Id, StringComparer.Ordinal);
        if (!units.TryGetValue("ORG", out var root) || root.ParentId is not null ||
            units.Keys.Intersect(teams.Keys, StringComparer.Ordinal).Any() ||
            units.Keys.Concat(teams.Keys).Concat(managers.Keys).Concat(staff.Keys).Any(string.IsNullOrWhiteSpace))
            throw new InvalidDataException("Invalid organization root or identifiers.");
        foreach (var unit in units.Values)
        {
            var seen = new HashSet<string>(StringComparer.Ordinal);
            var current = unit;
            while (current.ParentId is { } parent)
            {
                if (!seen.Add(current.Id) || !units.TryGetValue(parent, out var next))
                    throw new InvalidDataException("Invalid unit hierarchy.");
                current = next;
            }
            if (current.Id != "ORG" || !managers.TryGetValue(unit.ManagerId, out var manager) || manager.ScopeId != unit.Id)
                throw new InvalidDataException("Invalid unit manager.");
        }
        foreach (var team in teams.Values)
            if (!units.ContainsKey(team.UnitId) || !managers.TryGetValue(team.ManagerId, out var manager) ||
                manager.ScopeId != team.Id)
                throw new InvalidDataException("Invalid team or supervisor.");
        foreach (var member in staff.Values)
            if (!teams.ContainsKey(member.TeamId)) throw new InvalidDataException("Invalid staff team.");
        foreach (var manager in managers.Values)
            if (!units.ContainsKey(manager.ScopeId) && !teams.ContainsKey(manager.ScopeId))
                throw new InvalidDataException("Invalid manager scope.");
    }
}
