using Microsoft.EntityFrameworkCore;

namespace OrgPilot.Foundation.Persistence;

// This context owns only the migration foundation. Business modules will own their own models.
public sealed class FoundationDbContext(DbContextOptions<FoundationDbContext> options) : DbContext(options)
{
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.HasDefaultSchema("foundation");
    }
}
