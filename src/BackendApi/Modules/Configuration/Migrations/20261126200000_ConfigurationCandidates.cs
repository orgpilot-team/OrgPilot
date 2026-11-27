using Microsoft.EntityFrameworkCore.Migrations;

namespace OrgPilot.BackendApi.Modules.Configuration.Migrations;

public sealed partial class ConfigurationCandidates : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.Sql("""
            CREATE SCHEMA configuration;
            CREATE TABLE configuration.candidates (
                "Id" varchar(64) PRIMARY KEY, "CommandId" text NOT NULL,
                "EffectiveDay" integer NOT NULL, "Payload" jsonb NOT NULL, "TraceId" text NOT NULL
            );
            CREATE UNIQUE INDEX "IX_candidates_CommandId" ON configuration.candidates ("CommandId");
            CREATE INDEX "IX_candidates_EffectiveDay" ON configuration.candidates ("EffectiveDay");
            CREATE TABLE configuration.approvals (
                "CandidateId" varchar(64) PRIMARY KEY REFERENCES configuration.candidates("Id"),
                "ApprovedDay" integer NOT NULL, "Payload" jsonb NOT NULL, "TraceId" text NOT NULL
            );
            GRANT USAGE ON SCHEMA configuration TO orgpilot_api;
            GRANT SELECT, INSERT ON configuration.candidates, configuration.approvals TO orgpilot_api;
            """);
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.Sql("""
            DROP TABLE configuration.approvals;
            DROP TABLE configuration.candidates;
            DROP SCHEMA configuration;
            """);
    }

}
