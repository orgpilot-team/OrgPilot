using OrgPilot.BackendApi.Modules.Configuration;
using OrgPilot.Foundation.Archive;
using OrgPilot.Foundation.Observability;
using OrgPilot.Foundation.Persistence;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using Microsoft.EntityFrameworkCore;
using OpenTelemetry.Trace;

if (args is ["--health-check"])
{
    // A separate, one-shot HTTP probe for the development container health check.
    var probeBuilder = Host.CreateApplicationBuilder();
    probeBuilder.Services.AddHttpClient();
    using var probeHost = probeBuilder.Build();
    using var client = probeHost.Services.GetRequiredService<IHttpClientFactory>().CreateClient();
    client.Timeout = TimeSpan.FromSeconds(3);
    try
    {
        using var response = await client.GetAsync("http://127.0.0.1:8080/health/ready");
        return response.IsSuccessStatusCode ? 0 : 1;
    }
    catch (HttpRequestException)
    {
        return 1;
    }
    catch (OperationCanceledException)
    {
        return 1;
    }
}

var migrate = args is ["--migrate"];
var builder = WebApplication.CreateBuilder(migrate ? [] : args);
builder.Services.AddFoundationObservability(builder.Logging, builder.Configuration,
    migrate ? "orgpilot-database-migrate" : "orgpilot-backend-api", tracing => tracing.AddAspNetCoreInstrumentation());
builder.Services.AddFoundationPersistence(builder.Configuration);
var productConnection = builder.Configuration.GetConnectionString("Product")!;
builder.Services.AddDbContext<ConfigurationDbContext>(options => ConfigurationDbContext.Configure(options, productConnection));
builder.Services.AddScoped(_ => new ConfigurationValidator(productConnection));
builder.Services.AddScoped<ConfigurationVersionReader>();
// ConfigurationService is instantiated with a trusted IConfigurationAuthority by the later authorized command path.

if (migrate)
{
    // Only the dedicated migration process receives schema-owner credentials.
    await using var migrationApp = builder.Build();
    await using var scope = migrationApp.Services.CreateAsyncScope();
    var db = scope.ServiceProvider.GetRequiredService<FoundationDbContext>();
    await db.Database.MigrateAsync();
    await scope.ServiceProvider.GetRequiredService<ConfigurationDbContext>().Database.MigrateAsync();
    migrationApp.Logger.LogInformation("Foundation migrations are applied.");
    return 0;
}

builder.Services.AddProtectedArchive(builder.Configuration);
builder.Services.AddProblemDetails();
builder.Services.AddOpenApi();
builder.Services.AddHealthChecks().AddCheck<DatabaseReadinessCheck>("postgresql", tags: ["ready"]);

var app = builder.Build();
app.UseExceptionHandler();
if (app.Environment.IsDevelopment())
    app.MapOpenApi();

app.MapHealthChecks("/health/live", new HealthCheckOptions { Predicate = _ => false });
app.MapHealthChecks("/health/ready", new HealthCheckOptions { Predicate = check => check.Tags.Contains("ready") });

await app.RunAsync();
return 0;
