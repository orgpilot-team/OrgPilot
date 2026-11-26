using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;

namespace OrgPilot.BackendApi.Modules.Configuration;

public sealed class ConfigurationRow
{
    public string Id { get; init; } = null!;
    public string CommandId { get; init; } = null!;
    public int EffectiveDay { get; init; }
    public string Payload { get; init; } = null!;
    public string TraceId { get; init; } = null!;
}

public sealed class ApprovalRow
{
    public string CandidateId { get; init; } = null!;
    public int ApprovedDay { get; init; }
    public string Payload { get; init; } = null!;
    public string TraceId { get; init; } = null!;
}

public sealed class ConfigurationDbContext(DbContextOptions<ConfigurationDbContext> options) : DbContext(options)
{
    public DbSet<ConfigurationRow> Candidates => Set<ConfigurationRow>();
    public DbSet<ApprovalRow> Approvals => Set<ApprovalRow>();

    protected override void OnModelCreating(ModelBuilder modelBuilder) => ConfigureV1(modelBuilder);

    internal static void ConfigureV1(ModelBuilder model)
    {
        model.HasDefaultSchema("configuration");
        model.Entity<ConfigurationRow>(e =>
        {
            e.ToTable("candidates");
            e.HasKey(x => x.Id);
            e.Property(x => x.Id).HasMaxLength(64);
            e.Property(x => x.CommandId).IsRequired();
            e.HasIndex(x => x.CommandId).IsUnique();
            e.HasIndex(x => x.EffectiveDay);
            e.Property(x => x.Payload).HasColumnType("jsonb").IsRequired();
            e.Property(x => x.TraceId).IsRequired();
        });
        model.Entity<ApprovalRow>(e =>
        {
            e.ToTable("approvals");
            e.HasKey(x => x.CandidateId);
            e.Property(x => x.CandidateId).HasMaxLength(64);
            e.Property(x => x.Payload).HasColumnType("jsonb").IsRequired();
            e.Property(x => x.TraceId).IsRequired();
            e.HasOne<ConfigurationRow>().WithOne().HasForeignKey<ApprovalRow>(x => x.CandidateId)
                .OnDelete(DeleteBehavior.Restrict);
        });
    }

    public static void Configure(DbContextOptionsBuilder options, string connection) =>
        options.UseNpgsql(connection, postgres => postgres.MigrationsHistoryTable("__ConfigurationMigrationsHistory", "foundation"));
}

public sealed class ConfigurationDesignTimeFactory : IDesignTimeDbContextFactory<ConfigurationDbContext>
{
    public ConfigurationDbContext CreateDbContext(string[] args)
    {
        var connection = Environment.GetEnvironmentVariable("ConnectionStrings__Product")
            ?? throw new InvalidOperationException("Set ConnectionStrings__Product for migration tooling.");
        var options = new DbContextOptionsBuilder<ConfigurationDbContext>();
        ConfigurationDbContext.Configure(options, connection);
        return new(options.Options);
    }
}
