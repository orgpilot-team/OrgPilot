using Microsoft.EntityFrameworkCore;

namespace OrgPilot.BackgroundWorker.Persistence;

public sealed class StoredBatch
{
    public string Id { get; init; } = null!;
    public int DropDay { get; init; }
    public string Payload { get; init; } = null!;
    public string TraceId { get; init; } = null!;
}

public sealed class StoredSnapshot
{
    public string Id { get; init; } = null!;
    public int ReportDay { get; init; }
    public string Payload { get; init; } = null!;
    public string TraceId { get; init; } = null!;
}

public sealed class StoredDefinition
{
    public string Id { get; init; } = null!;
    public string Payload { get; init; } = null!;
}

public sealed class StoredParityReceipt
{
    public string Id { get; init; } = null!;
    public string DefinitionId { get; init; } = null!;
    public string Payload { get; init; } = null!;
    public string TraceId { get; init; } = null!;
}

public sealed class StoredKpiRun
{
    public string Id { get; init; } = null!;
    public string SnapshotId { get; init; } = null!;
    public string DefinitionId { get; init; } = null!;
    public string Payload { get; init; } = null!;
    public string TraceId { get; init; } = null!;
}

public sealed class Stage2DbContext(DbContextOptions<Stage2DbContext> options) : DbContext(options)
{
    public DbSet<StoredBatch> Batches => Set<StoredBatch>();
    public DbSet<StoredSnapshot> Snapshots => Set<StoredSnapshot>();
    public DbSet<StoredDefinition> Definitions => Set<StoredDefinition>();
    public DbSet<StoredParityReceipt> ParityReceipts => Set<StoredParityReceipt>();
    public DbSet<StoredKpiRun> KpiRuns => Set<StoredKpiRun>();

    protected override void OnModelCreating(ModelBuilder modelBuilder) => ConfigureV1(modelBuilder);

    // Match the initial SQL migration, including the names PostgreSQL assigns to its constraints.
    internal static void ConfigureV1(ModelBuilder model)
    {
        model.HasDefaultSchema("intake");
        model.Entity<StoredBatch>(e =>
        {
            e.ToTable("batches", "intake");
            e.HasKey(x => x.Id).HasName("batches_pkey");
            e.Property(x => x.Id).HasMaxLength(64);
            e.Property(x => x.Payload).HasColumnType("jsonb").IsRequired();
            e.Property(x => x.TraceId).IsRequired();
            e.HasIndex(x => x.DropDay);
        });
        model.Entity<StoredSnapshot>(e =>
        {
            e.ToTable("snapshots", "snapshots");
            e.HasKey(x => x.Id).HasName("snapshots_pkey");
            e.Property(x => x.Id).HasMaxLength(64);
            e.Property(x => x.Payload).HasColumnType("jsonb").IsRequired();
            e.Property(x => x.TraceId).IsRequired();
            e.HasIndex(x => x.ReportDay);
        });
        model.Entity<StoredDefinition>(e =>
        {
            e.ToTable("definitions", "kpi");
            e.HasKey(x => x.Id).HasName("definitions_pkey");
            e.Property(x => x.Id).HasMaxLength(64);
            e.Property(x => x.Payload).HasColumnType("jsonb").IsRequired();
        });
        model.Entity<StoredParityReceipt>(e =>
        {
            e.ToTable("parity_receipts", "kpi");
            e.HasKey(x => x.Id).HasName("parity_receipts_pkey");
            e.Property(x => x.Id).HasMaxLength(64);
            e.Property(x => x.DefinitionId).HasMaxLength(64).IsRequired();
            e.Property(x => x.Payload).HasColumnType("jsonb").IsRequired();
            e.Property(x => x.TraceId).IsRequired();
            e.HasOne<StoredDefinition>().WithMany().HasForeignKey(x => x.DefinitionId)
                .OnDelete(DeleteBehavior.NoAction).HasConstraintName("parity_receipts_DefinitionId_fkey");
            e.HasIndex(x => x.DefinitionId);
        });
        model.Entity<StoredKpiRun>(e =>
        {
            e.ToTable("query_runs", "kpi");
            e.HasKey(x => x.Id).HasName("query_runs_pkey");
            e.Property(x => x.Id).HasMaxLength(64);
            e.Property(x => x.SnapshotId).HasMaxLength(64).IsRequired();
            e.Property(x => x.DefinitionId).HasMaxLength(64).IsRequired();
            e.Property(x => x.Payload).HasColumnType("jsonb").IsRequired();
            e.Property(x => x.TraceId).IsRequired();
            e.HasOne<StoredDefinition>().WithMany().HasForeignKey(x => x.DefinitionId)
                .OnDelete(DeleteBehavior.NoAction).HasConstraintName("query_runs_DefinitionId_fkey");
            e.HasOne<StoredSnapshot>().WithMany().HasForeignKey(x => x.SnapshotId)
                .OnDelete(DeleteBehavior.NoAction).HasConstraintName("query_runs_SnapshotId_fkey");
            e.HasIndex(x => x.DefinitionId);
            e.HasIndex(x => new { x.SnapshotId, x.DefinitionId }).IsUnique();
        });
    }
}
