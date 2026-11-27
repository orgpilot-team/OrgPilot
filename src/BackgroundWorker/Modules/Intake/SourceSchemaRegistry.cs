namespace OrgPilot.BackgroundWorker.Modules.Intake;

public sealed record SourceSchema(
    string Source,
    string Version,
    IReadOnlyList<string> Columns,
    IReadOnlyList<string> KeyColumns,
    IReadOnlyDictionary<string, string>? Aliases = null)
{
    public string CanonicalColumn(string name) =>
        Aliases is not null && Aliases.TryGetValue(name, out var canonical) ? canonical : name;
}

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

    // The supplied dataset switches to these exact header versions from day 082.
    private static readonly IReadOnlyDictionary<string, SourceSchema> Alternate =
        new Dictionary<string, SourceSchema>(StringComparer.Ordinal)
        {
            ["tickets"] = WithAlias(Baseline["tickets"], "create_time", "created_at"),
            ["ticket_events"] = WithAlias(Baseline["ticket_events"], "event_time", "at")
        };

    public static SourceSchema? Select(string source, IReadOnlyList<string> header)
    {
        if (!Baseline.TryGetValue(source, out var schema) || header.Count != schema.Columns.Count)
            return null;

        var actual = header.ToHashSet(StringComparer.Ordinal);
        if (actual.Count != header.Count)
            return null;
        if (actual.SetEquals(schema.Columns))
            return schema;
        if (!Alternate.TryGetValue(source, out var alternate))
            return null;
        var expected = schema.Columns.Except(alternate.Aliases!.Values, StringComparer.Ordinal)
            .Concat(alternate.Aliases.Keys);
        return actual.SetEquals(expected) ? alternate : null;
    }

    private static SourceSchema Define(string source, string columns, string keys) =>
        new(source, "baseline-v1", Array.AsReadOnly(columns.Split(' ')), Array.AsReadOnly(keys.Split(' ')));

    private static SourceSchema WithAlias(SourceSchema schema, string alias, string canonical) =>
        schema with
        {
            Version = "baseline-v2",
            Aliases = new System.Collections.ObjectModel.ReadOnlyDictionary<string, string>(
                new Dictionary<string, string>(StringComparer.Ordinal) { [alias] = canonical })
        };
}
