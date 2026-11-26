using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;

namespace OrgPilot.BackgroundWorker.Persistence.Migrations;

[DbContext(typeof(Stage2DbContext))]
public sealed class Stage2ModelSnapshot : ModelSnapshot
{
    protected override void BuildModel(ModelBuilder modelBuilder) => BuildV1(modelBuilder);

    internal static void BuildV1(ModelBuilder modelBuilder)
    {
        modelBuilder.HasAnnotation("ProductVersion", "10.0.11")
            .HasAnnotation("Relational:MaxIdentifierLength", 63);
        modelBuilder.UseIdentityByDefaultColumns();
        Stage2DbContext.ConfigureV1(modelBuilder);
    }
}
