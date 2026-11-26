using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;

namespace OrgPilot.Foundation.Persistence;

public sealed class FoundationDesignTimeFactory : IDesignTimeDbContextFactory<FoundationDbContext>
{
    public FoundationDbContext CreateDbContext(string[] args)
    {
        var connection = Environment.GetEnvironmentVariable("ConnectionStrings__Product")
            ?? throw new InvalidOperationException("Set ConnectionStrings__Product for EF migration tooling.");
        var options = new DbContextOptionsBuilder<FoundationDbContext>();
        PersistenceRegistration.Configure(options, connection);
        return new FoundationDbContext(options.Options);
    }
}
