using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;
using Microsoft.Extensions.DependencyInjection;

namespace OrgPilot.BackgroundWorker.Persistence;

public static class Stage2Persistence
{
    public static IServiceCollection AddStage2Persistence(this IServiceCollection services, string connection) =>
        services.AddDbContext<Stage2DbContext>(options => Configure(options, connection));

    internal static void Configure(DbContextOptionsBuilder options, string connection) =>
        options.UseNpgsql(connection, postgres => postgres.MigrationsHistoryTable("__Stage2MigrationsHistory", "foundation"));
}

public sealed class Stage2DesignTimeFactory : IDesignTimeDbContextFactory<Stage2DbContext>
{
    public Stage2DbContext CreateDbContext(string[] args)
    {
        var connection = Environment.GetEnvironmentVariable("ConnectionStrings__Product")
            ?? throw new InvalidOperationException("Set ConnectionStrings__Product for migration tooling.");
        var options = new DbContextOptionsBuilder<Stage2DbContext>();
        Stage2Persistence.Configure(options, connection);
        return new(options.Options);
    }
}
