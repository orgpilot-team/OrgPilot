namespace OrgPilot.BackgroundWorker.Modules.Intake;

public sealed record SourceSchema(
    string Source,
    string Version,
    IReadOnlyList<string> Columns,
    IReadOnlyList<string> KeyColumns);

/// <summary>
/// Explicit baseline contracts from the supplied dataset. Additional versions and aliases
/// must be registered explicitly; a changed header is never inferred.
/// </summary>
public static class SourceSchemaRegistry
{
    private static readonly IReadOnlyDictionary<string, SourceSchema> Baseline =
        new[]
        {
            Define("orders", "order_id created_at channel city category items order_value_toman customer_id campaign_id promised_by", "order_id"),
            Define("order_events", "order_id event at actor_team amount_toman", "order_id event at"),
            Define("web_sessions", "date channel sessions", "date channel"),
            Define("tickets", "ticket_id created_at category team_id order_id channel text_fa", "ticket_id"),
            Define("ticket_events", "ticket_id event at staff_id", "ticket_id event at"),
            Define("csat", "ticket_id answered_at score", "ticket_id answered_at"),
            Define("crm_leads", "lead_id source created_at", "lead_id"),
            Define("crm_lead_events", "lead_id event at contract_value_toman", "lead_id event at"),
            Define("mkt_daily", "date source spend_toman impressions clicks leads", "date source"),
            Define("tasks", "task_id team_id owner_id created_at due_date title_fa blocker_fa", "task_id"),
            Define("task_events", "task_id event at", "task_id event at"),
            Define("staff_availability", "date staff_id team_id status", "date staff_id")
        }.ToDictionary(schema => schema.Source, StringComparer.Ordinal);

    public static SourceSchema? Select(string source, IReadOnlyList<string> header)
    {
        if (!Baseline.TryGetValue(source, out var schema) || header.Count != schema.Columns.Count)
            return null;

        var actual = header.ToHashSet(StringComparer.Ordinal);
        return actual.Count == header.Count && actual.SetEquals(schema.Columns) ? schema : null;
    }

    private static SourceSchema Define(string source, string columns, string keys) =>
        new(source, "baseline-v1", Array.AsReadOnly(columns.Split(' ')), Array.AsReadOnly(keys.Split(' ')));
}
