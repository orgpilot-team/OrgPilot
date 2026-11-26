using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace OrgPilot.Foundation.Persistence;

public static class PersistenceRegistration
{
    public static IServiceCollection AddFoundationPersistence(this IServiceCollection services, IConfiguration configuration)
    {
        var connection = configuration.GetConnectionString("Product")
            ?? throw new InvalidOperationException("ConnectionStrings:Product must be configured.");
        services.AddDbContext<FoundationDbContext>(options => Configure(options, connection));
        return services;
    }

    internal static void Configure(DbContextOptionsBuilder options, string connection) =>
        options.UseNpgsql(connection, postgres =>
            postgres.MigrationsHistoryTable("__EFMigrationsHistory", "foundation"));
}
