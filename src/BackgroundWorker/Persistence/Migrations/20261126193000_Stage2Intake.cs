using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;

namespace OrgPilot.BackgroundWorker.Persistence.Migrations;

[DbContext(typeof(Stage2DbContext))]
[Migration("20261126193000_Stage2Intake")]
public sealed class Stage2Intake : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.Sql("""
            CREATE SCHEMA intake;
            CREATE SCHEMA snapshots;
            CREATE SCHEMA kpi;
            CREATE TABLE intake.batches (
                "Id" varchar(64) PRIMARY KEY, "DropDay" integer NOT NULL,
                "Payload" jsonb NOT NULL, "TraceId" text NOT NULL
            );
            CREATE INDEX "IX_batches_DropDay" ON intake.batches ("DropDay");
            CREATE TABLE snapshots.snapshots (
                "Id" varchar(64) PRIMARY KEY, "ReportDay" integer NOT NULL,
                "Payload" jsonb NOT NULL, "TraceId" text NOT NULL
            );
            CREATE INDEX "IX_snapshots_ReportDay" ON snapshots.snapshots ("ReportDay");
            CREATE TABLE kpi.definitions ("Id" varchar(64) PRIMARY KEY, "Payload" jsonb NOT NULL);
            CREATE TABLE kpi.parity_receipts (
                "Id" varchar(64) PRIMARY KEY, "DefinitionId" varchar(64) NOT NULL REFERENCES kpi.definitions("Id"),
                "Payload" jsonb NOT NULL, "TraceId" text NOT NULL
            );
            CREATE INDEX "IX_parity_receipts_DefinitionId" ON kpi.parity_receipts ("DefinitionId");
            CREATE TABLE kpi.query_runs (
                "Id" varchar(64) PRIMARY KEY, "SnapshotId" varchar(64) NOT NULL REFERENCES snapshots.snapshots("Id"),
                "DefinitionId" varchar(64) NOT NULL REFERENCES kpi.definitions("Id"),
                "Payload" jsonb NOT NULL, "TraceId" text NOT NULL
            );
            CREATE INDEX "IX_query_runs_DefinitionId" ON kpi.query_runs ("DefinitionId");
            CREATE UNIQUE INDEX "IX_query_runs_SnapshotId_DefinitionId" ON kpi.query_runs ("SnapshotId", "DefinitionId");
            GRANT USAGE ON SCHEMA intake, snapshots, kpi TO orgpilot_worker;
            GRANT SELECT, INSERT ON intake.batches, snapshots.snapshots, kpi.definitions, kpi.query_runs TO orgpilot_worker;
            GRANT SELECT ON kpi.parity_receipts TO orgpilot_worker;
            GRANT USAGE ON SCHEMA kpi TO orgpilot_api;
            GRANT SELECT ON kpi.definitions, kpi.parity_receipts TO orgpilot_api;
            """);
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.Sql("""
            DROP TABLE kpi.query_runs;
            DROP TABLE kpi.parity_receipts;
            DROP TABLE kpi.definitions;
            DROP TABLE snapshots.snapshots;
            DROP TABLE intake.batches;
            DROP SCHEMA kpi;
            DROP SCHEMA snapshots;
            DROP SCHEMA intake;
            """);
    }

    protected override void BuildTargetModel(ModelBuilder modelBuilder) => Stage2ModelSnapshot.BuildV1(modelBuilder);
}
