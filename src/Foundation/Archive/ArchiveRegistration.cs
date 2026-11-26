using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace OrgPilot.Foundation.Archive;

public static class ArchiveRegistration
{
    public static IServiceCollection AddProtectedArchive(this IServiceCollection services, IConfiguration configuration)
    {
        var root = configuration["Archive:RootPath"];
        if (string.IsNullOrWhiteSpace(root) || !Path.IsPathFullyQualified(root))
            throw new InvalidOperationException("Archive:RootPath must be an absolute directory path.");

        services.AddSingleton<IProtectedFileArchive>(new FileSystemArchive(root));
        return services;
    }
}
