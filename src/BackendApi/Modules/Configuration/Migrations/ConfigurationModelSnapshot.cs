using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;

namespace OrgPilot.BackendApi.Modules.Configuration.Migrations;

[DbContext(typeof(ConfigurationDbContext))]
public sealed class ConfigurationModelSnapshot : ModelSnapshot
{
    protected override void BuildModel(ModelBuilder modelBuilder) => BuildV1(modelBuilder);

    internal static void BuildV1(ModelBuilder modelBuilder)
    {
        modelBuilder.HasAnnotation("ProductVersion", "10.0.11")
            .HasAnnotation("Relational:MaxIdentifierLength", 63);
        modelBuilder.UseIdentityByDefaultColumns();
        ConfigurationDbContext.ConfigureV1(modelBuilder);
    }
}
