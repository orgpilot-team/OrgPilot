using System.Text.Json;
using OrgPilot.BackgroundWorker.Modules.Intake;
using OrgPilot.Foundation.Archive;

namespace OrgPilot.Acceptance;

internal static class IntakeFixtureChecks
{
    public static async Task RunAsync(string archiveDirectory, Action<string, bool> check)
    {
        // Never edit DATA_DIR. Construct a small isolated fixture in the test output.
        var root = Path.Combine(archiveDirectory, "fixtures", Guid.NewGuid().ToString("N"));
        var drop = Path.Combine(root, "drops", "day_001");
        Directory.CreateDirectory(drop);
        var archive = new FileSystemArchive(archiveDirectory);
        var intake = new IngestionCoordinator(archive);
        var date = new DateOnly(2026, 7, 23);
        const string ordersHeader = "order_id,created_at,channel,city,category,items,order_value_toman,customer_id,campaign_id,promised_by";
        const string order = "O1,2026-07-23 10:00:00,web,Tehran,category,1,100,C1,,2026-07-24 10:00:00";
        var ordersPath = Path.Combine(drop, "orders.csv");
        await File.WriteAllTextAsync(ordersPath, ordersHeader + "\n" + order + "\n");
        await File.WriteAllTextAsync(Path.Combine(drop, "tickets.csv"), "unknown_header\n1\n");
        await File.WriteAllTextAsync(Path.Combine(drop, "web_sessions.csv"), "date,channel,sessions\n2026-07-23,web,not-a-number\n");
        await File.WriteAllTextAsync(Path.Combine(drop, "order_events.csv"),
            "order_id,event,at,actor_team,amount_toman\nO1,paid,2026-07-24 10:00:00,T_ENT,100\n");
        await File.WriteAllTextAsync(Path.Combine(drop, "manifest.json"), JsonSerializer.Serialize(new
        {
            drop_day = 1,
            date = "2026-07-23",
            files = new Dictionary<string, int>
            {
                ["orders.csv"] = 1, ["tickets.csv"] = 1,
                ["web_sessions.csv"] = 1, ["order_events.csv"] = 1
            }
        }));
        var first = await intake.ReadAsync(root, 1, date);
        check("Invalid schema is quarantined", first.Facts.All(f => f.Source != "tickets") &&
            first.Issues.Any(i => i.Source == "tickets" && i.Code == "unknown_schema"));
        check("Invalid numeric record is quarantined", first.Facts.All(f => f.Source != "web_sessions") &&
            first.Issues.Any(i => i.Source == "web_sessions" && i.Code == "invalid_integer:sessions"));
        check("Future record cannot leak into pinned day", first.Facts.All(f => f.Source != "order_events") &&
            first.Issues.Any(i => i.Source == "order_events" && i.Code == "future_record"));
        var original = first.Facts.Single(f => f.Source == "orders");
        await File.WriteAllTextAsync(ordersPath, ordersHeader + "\n" + order.Replace(",100,", ",200,") + "\n");
        var corrected = await intake.ReadAsync(root, 1, date);
        var replacement = corrected.Facts.Single(f => f.Source == "orders");
        await using var archived = await archive.OpenVerifiedAsync(original.Archive);
        using var reader = new StreamReader(archived);
        check("Corrected drop creates a new batch and preserves original bytes", first.Id != corrected.Id &&
            original.Key == replacement.Key && original.ValuesJson != replacement.ValuesJson &&
            original.Archive.Sha256 != replacement.Archive.Sha256 &&
            (await reader.ReadToEndAsync()).Contains(",100,", StringComparison.Ordinal));
    }
}
