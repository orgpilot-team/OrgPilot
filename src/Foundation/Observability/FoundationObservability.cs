using System.Diagnostics;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;

namespace OrgPilot.Foundation.Observability;

public static class FoundationObservability
{
    public const string SourceName = "OrgPilot.Foundation";
    public static readonly ActivitySource Activities = new(SourceName);

    public static void AddFoundationObservability(this IServiceCollection services, ILoggingBuilder logging,
        IConfiguration configuration, string serviceName, Action<TracerProviderBuilder>? configureTracing = null)
    {
        logging.ClearProviders();
        logging.AddJsonConsole(options => options.IncludeScopes = true);
        logging.Configure(options => options.ActivityTrackingOptions = ActivityTrackingOptions.TraceId |
            ActivityTrackingOptions.SpanId | ActivityTrackingOptions.ParentId);

        services.AddOpenTelemetry()
            .ConfigureResource(resource => resource.AddService(serviceName))
            .WithTracing(tracing =>
            {
                tracing.AddSource(SourceName).AddHttpClientInstrumentation();
                configureTracing?.Invoke(tracing);

                // Export is opt-in; the SDK exports asynchronously and core work does not await it.
                if (configuration.GetValue<bool>("Observability:ExportEnabled"))
                    tracing.AddOtlpExporter();
            });
    }
}
