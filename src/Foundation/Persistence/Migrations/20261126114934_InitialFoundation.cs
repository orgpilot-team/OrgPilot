using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace OrgPilot.Foundation.Persistence.Migrations
{
    /// <inheritdoc />
    public partial class InitialFoundation : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.EnsureSchema(name: "foundation");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            // The bootstrap owns the schema; do not remove it when rolling back this marker migration.
        }
    }
}
