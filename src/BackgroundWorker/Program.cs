using OrgPilot.Foundation.Archive;
using OrgPilot.Foundation.Observability;
using OrgPilot.Foundation.Persistence;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

var smokeOnly = args is ["--smoke"];
var builder = Host.CreateApplicationBuilder(smokeOnly ? [] : args);
builder.Services.AddFoundationObservability(builder.Logging, builder.Configuration, "orgpilot-background-worker");
builder.Services.AddFoundationPersistence(builder.Configuration);
builder.Services.AddProtectedArchive(builder.Configuration);

using var host = builder.Build();
var logger = host.Services.GetRequiredService<ILoggerFactory>().CreateLogger("WorkerStartup");
await host.StartAsync();

await using (var scope = host.Services.CreateAsyncScope())
{
    using var activity = FoundationObservability.Activities.StartActivity("worker.foundation.check");
    var db = scope.ServiceProvider.GetRequiredService<FoundationDbContext>();
    if (!await db.Database.CanConnectAsync())
        throw new InvalidOperationException("Worker cannot connect to the product database.");

    await ArchiveSmokeCheck.RunAsync(builder.Configuration["Archive:RootPath"]!);
    logger.LogInformation("Worker foundation ready: database and archive checks passed.");
}

if (smokeOnly)
    await host.StopAsync();
else
    await host.WaitForShutdownAsync();
