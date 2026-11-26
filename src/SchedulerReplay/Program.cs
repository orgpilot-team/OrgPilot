using OrgPilot.Foundation.Observability;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

var checkOnly = args is ["--check"];
var builder = Host.CreateApplicationBuilder(checkOnly ? [] : args);
builder.Services.AddFoundationObservability(builder.Logging, builder.Configuration, "orgpilot-scheduler-replay");
var backendUrl = builder.Configuration["Backend:BaseUrl"];
if (!Uri.TryCreate(backendUrl, UriKind.Absolute, out var backendUri) ||
    backendUri.Scheme is not ("http" or "https"))
    throw new InvalidOperationException("Backend:BaseUrl must be an absolute HTTP or HTTPS URL.");

builder.Services.AddHttpClient("backend", client =>
{
    client.BaseAddress = backendUri;
    client.Timeout = TimeSpan.FromSeconds(5);
});

using var host = builder.Build();
await host.StartAsync();
using (var activity = FoundationObservability.Activities.StartActivity("scheduler.foundation.check"))
{
    using var client = host.Services.GetRequiredService<IHttpClientFactory>().CreateClient("backend");
    using var response = await client.GetAsync("/health/ready");
    response.EnsureSuccessStatusCode();
    host.Services.GetRequiredService<ILoggerFactory>().CreateLogger("SchedulerStartup")
        .LogInformation("Scheduler foundation ready: Backend API readiness check passed.");
}

// The replay command and scheduling policy are intentionally not implemented in this stage.
if (checkOnly)
    await host.StopAsync();
else
    await host.WaitForShutdownAsync();
