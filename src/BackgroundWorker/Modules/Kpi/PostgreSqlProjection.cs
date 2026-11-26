using OrgPilot.BackgroundWorker.Modules.Snapshots;

namespace OrgPilot.BackgroundWorker.Modules.Kpi;

internal static class PostgreSqlProjection
{
    private const string Views = """
        order_fact AS (
          SELECT o.*, e.paid_at, e.failed_at, e.cancelled_at, e.picked_at, e.handed_over_at, e.delivered_at
          FROM orders o LEFT JOIN (
            SELECT order_id,
              MAX(CASE WHEN event='paid' THEN at END) paid_at,
              MAX(CASE WHEN event='payment_failed' THEN at END) failed_at,
              MAX(CASE WHEN event='cancelled' THEN at END) cancelled_at,
              MAX(CASE WHEN event='picked' THEN at END) picked_at,
              MAX(CASE WHEN event='handed_over' THEN at END) handed_over_at,
              MAX(CASE WHEN event='delivered' THEN at END) delivered_at
            FROM order_events GROUP BY order_id
          ) e USING(order_id)
        ),
        ticket_fact AS (
          SELECT t.*, e.first_response_at, e.inspected_at, e.resolved_at, COALESCE(e.reopened,0) reopened
          FROM tickets t LEFT JOIN (
            SELECT ticket_id,
              MIN(CASE WHEN event='first_response' THEN at END) first_response_at,
              MAX(CASE WHEN event='inspected' THEN at END) inspected_at,
              MAX(CASE WHEN event='resolved' THEN at END) resolved_at,
              MAX(CASE WHEN event='reopened' THEN 1 ELSE 0 END) reopened
            FROM ticket_events GROUP BY ticket_id
          ) e USING(ticket_id)
        ),
        lead_fact AS (
          SELECT l.*, e.first_contact_at, e.qualified_at, e.proposal_at, e.won_at, e.lost_at,
            COALESCE((SELECT x.contract_value_toman FROM crm_lead_events x
              WHERE x.lead_id=l.lead_id AND x.event='value_corrected'
              ORDER BY x.drop_day DESC, x.at DESC LIMIT 1), e.won_value) contract_value
          FROM crm_leads l LEFT JOIN (
            SELECT lead_id,
              MAX(CASE WHEN event='first_contact' THEN at END) first_contact_at,
              MAX(CASE WHEN event='qualified' THEN at END) qualified_at,
              MAX(CASE WHEN event='proposal_sent' THEN at END) proposal_at,
              MAX(CASE WHEN event='won' THEN at END) won_at,
              MAX(CASE WHEN event='lost' THEN at END) lost_at,
              MAX(CASE WHEN event='won' THEN contract_value_toman END) won_value
            FROM crm_lead_events GROUP BY lead_id
          ) e USING(lead_id)
        ),
        task_fact AS (
          SELECT t.*, e.done_at FROM tasks t LEFT JOIN (
            SELECT task_id, MAX(CASE WHEN event='done' THEN at END) done_at
            FROM task_events GROUP BY task_id
          ) e USING(task_id)
        ),
        b2c AS (
          SELECT date(e.at) d,
            SUM(CASE WHEN e.event='paid' THEN o.order_value_toman ELSE -e.amount_toman END) v,
            SUM(CASE WHEN o.channel='marketplace' THEN
              (CASE WHEN e.event='paid' THEN o.order_value_toman ELSE -e.amount_toman END) ELSE 0 END) mp
          FROM order_events e JOIN orders o USING(order_id)
          WHERE e.event IN ('paid','refunded') GROUP BY 1
        ),
        b2b AS (
          SELECT date(won_at) d, SUM(contract_value) v
          FROM lead_fact WHERE won_at IS NOT NULL GROUP BY 1
        ),
        revenue_daily AS (
          SELECT c.d, COALESCE(b2c.v,0) AS b2c, COALESCE(b2b.v,0) AS b2b,
            COALESCE(b2c.mp,0) AS marketplace FROM cal c LEFT JOIN b2c USING(d) LEFT JOIN b2b USING(d)
        )
        """;

    public static string Bind(string translatedSql)
    {
        var ctes = ProjectionData.Tables.Select(t =>
            $"{t.Name} AS (SELECT * FROM jsonb_to_recordset(CAST(@data AS jsonb)->'{t.Name}') AS r({string.Join(", ", t.Columns.Select(c => $"\"{c.Name}\" {c.PostgreSqlType}"))}))");
        var prefix = "WITH " + string.Join(",\n", ctes) + ",\n" + Views;
        return translatedSql.StartsWith("WITH ", StringComparison.OrdinalIgnoreCase)
            ? prefix + ",\n" + translatedSql[5..]
            : prefix + "\n" + translatedSql;
    }
}
