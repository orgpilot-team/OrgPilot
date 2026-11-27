using Microsoft.EntityFrameworkCore;
using OrgPilot.BackendApi.Modules.Configuration;
using OrgPilot.BackgroundWorker.Modules.Kpi;

namespace OrgPilot.Acceptance;

// Explicitly invoked acceptance fixture. All candidate/approval writes are rolled back,
// and the fixture authority is never registered in the Backend API.
internal static class ConfigurationChecks
{
    public static async Task RunAsync(ConfigurationDbContext db, string connection, int day,
        KpiDefinition definition, ParityReceipt receipt)
    {
        const string actor = "stage2-acceptance-fixture";
        await using var transaction = await db.Database.BeginTransactionAsync();
        var service = new ConfigurationService(db, new FixtureAuthority(actor), new ConfigurationValidator(connection));
        void Require(bool condition, string name)
        {
            if (!condition) throw new InvalidDataException("Configuration check failed: " + name);
            Console.WriteLine("PASS " + name);
        }
        var initial = await service.ResolveAsync(day);
        var initialTomorrow = await service.ResolveAsync(day + 1);
        var command = "stage2-acceptance:" + Guid.NewGuid().ToString("N");
        var kpi = await service.SubmitAsync(CandidateKind.KpiDefinition, definition.KpiId, day, actor,
            command + ":kpi", new KpiChange(definition.KpiId, definition.Id, receipt.Id));
        var same = await service.SubmitAsync(CandidateKind.KpiDefinition, definition.KpiId, day, actor,
            command + ":kpi", new KpiChange(definition.KpiId, definition.Id, receipt.Id));
        Require(same.Id == kpi.Id, "Configuration command is idempotent");
        var org = await service.SubmitAsync(CandidateKind.Organization, "ORG", day, actor, command + ":org",
            new OrganizationRevision([new("ORG", null, "M01")], [], [new("M01", "ORG")], []));
        var priority = await service.SubmitAsync(CandidateKind.ManagerPriority, "M01", day, actor,
            command + ":priority", new ManagerPriority("M01", [definition.KpiId]));
        Require((await service.ResolveAsync(day + 1)).Version == initialTomorrow.Version,
            "Unapproved candidates do not activate");
        foreach (var candidate in new[] { kpi, org, priority })
            await service.ApproveAsync(candidate.Id, actor, day);
        Require((await service.ResolveAsync(day)).Version == initial.Version, "No same-day activation");
        var tomorrow = ConfigurationVersionReader.References(await service.ResolveAsync(day + 1));
        Require(tomorrow.CandidateIds.Contains(kpi.Id) && tomorrow.OrganizationRevisionId == org.Id &&
            tomorrow.ManagerPriorities.Any(p => p.CandidateId == priority.Id), "Approved revisions activate at D+1");

        var invalid = await service.SubmitAsync(CandidateKind.KpiDefinition, definition.KpiId, day, actor,
            command + ":invalid", new KpiChange(definition.KpiId, definition.Id, new string('0', 64)));
        var rejected = false;
        try { await service.ApproveAsync(invalid.Id, actor, day); }
        catch (InvalidDataException) { rejected = true; }
        Require(rejected && !(await service.ResolveAsync(day + 1)).CandidateIds().Contains(invalid.Id),
            "KPI without a passing receipt remains inactive");
        var malformed = await service.SubmitAsync(CandidateKind.Organization, "ORG", day, actor,
            command + ":invalid-org", new OrganizationRevision([], [], [], []));
        rejected = false;
        try { await service.ApproveAsync(malformed.Id, actor, day); }
        catch (InvalidDataException) { rejected = true; }
        Require(rejected && (await service.ResolveAsync(day + 1)).Version == tomorrow.Version,
            "Invalid organization leaves active configuration unchanged");
        await transaction.RollbackAsync();
    }

    private static IEnumerable<string> CandidateIds(this ActiveConfiguration active) => active.Candidates.Select(c => c.Id);

    private sealed class FixtureAuthority(string actor) : IConfigurationAuthority
    {
        public Task DemandAsync(string actorId, CandidateKind kind, string key, CancellationToken cancellationToken) =>
            actorId == actor ? Task.CompletedTask : throw new UnauthorizedAccessException("Not the fixture principal.");
    }
}
