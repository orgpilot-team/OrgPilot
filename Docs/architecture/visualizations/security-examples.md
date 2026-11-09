# Security examples

Status note: source restrictions are Requirements. CONFIRMED/DERIVED are legacy evidence labels, not Accepted decisions. Candidate field projections and enforcement remain Proposed; UNRESOLVED means Open. Q IDs here are manager-input questions. See [ADR-06](../registry/decisions-registry.md#adr-06), the [policy log](../registry/open-issues-registry.md#decision-log), and the [Structurizr view catalog](../audit-2026-11-09/structurizr-gap-report.md).

These examples describe requirements and candidate projections. They do not create grants. Evidence: `dataset/org/access_matrix.csv`, the original brief pages 6, 10, 12, and 13, and each cited KPI SQL. Source paths are relative to the project root.

## M07: Warehouse supervisor

CONFIRMED: M07 can see T_WH KPIs and direct-team workload. DERIVED: the minimum workload projection can use `tasks.task_id`, `tasks.team_id`, `tasks.owner_id`, `tasks.created_at`, and `tasks.due_date`. Compute completion from `task_events.task_id`, `task_events.event`, and `task_events.at`, using `task_fact.done_at`. The row condition is `tasks.team_id = 'T_WH'`. Join `tasks.owner_id = staff.staff_id` and verify that `staff.team_id = 'T_WH'` at the applicable date. These are candidate query conditions derived from observed keys. The physical enforcement design is PROPOSED. For an as-of date, use the supplied overdue SQL time conditions, or define a separate approved open-work query. Do not count all historical tasks as open.

RESTRICTED: `tasks.title_fa` and `tasks.blocker_fa` can support work allocation, but exact text can contain personal data. A redaction policy is UNRESOLVED. Q10 requests open work per warehouse member. It does not grant access to other teams.

DERIVED internal calculation: warehouse KPIs use `orders.order_id`, `orders.category`, and selected event timestamps from `order_events.order_id`, `event`, and `at`. `K_WH_DAMAGE_BY_CAT_7D` joins `tickets.order_id = orders.order_id`, filters `tickets.category = 'کالای معیوب'`, and groups by the order product category. This is a cross-team calculation. `K_WH_INSPECT_MED` uses first-response and inspection times from `ticket_fact`. Its supplied SQL has no `team_id = 'T_WH'` filter. Do not add that filter to the formula or grant source tickets to M07. Return the authorized warehouse KPI result.

`tickets.text_fa`, `ticket_events.staff_id`, `orders.customer_id`, unrelated support cases, and other-team workload have no warehouse display grant. Keep them out of the M07 projection. Availability `staff_id` and `status` stay internal; release team capacity only. No supplied KPI uses staff_availability. A capacity formula remains UNRESOLVED.

## M03: Operations manager

CONFIRMED: allowed KPI entities are U_OPS, T_WH, and T_SHP. M03 can receive on-time delivery, picking time, warehouse damage rate, shipping metrics, and aggregate overdue counts. DERIVED: internal calculation may read task ownership to validate scope, but the result must remove `tasks.owner_id`, `staff.staff_id`, `staff.name_fa`, and `ticket_events.staff_id`. Do not group results by an employee or return a row per employee. Q11 asks for warehouse workload per person. Refuse that individual view and offer a team total. A query request cannot expand the access matrix.

PROPOSED: a reviewed aggregate projection can group work by `tasks.team_id` and business date. Exact small-group suppression limits are UNRESOLVED. A team label does not make a one-person aggregate safe.

## M01: Executive manager

CONFIRMED: the matrix includes ORG, all three units, and all seven teams. This permits organization-wide aggregate reporting, including the 55 KPI definitions, subject to team activation. It does not permit employee-level data. Remove employee identifiers from query results, evidence snippets, reports, and LLM input. Do not use employee-level pseudonyms as a substitute. Team capacity is permitted as an aggregate purpose; individual leave is prohibited. Exact capacity calculation, minimum group size, and extra drill-down columns remain UNRESOLVED.

## M11: Marketplace supervisor

CONFIRMED: the scope is T_MKT only. `K_MKT_ORDERS` filters `orders.channel = 'marketplace'`. `revenue_daily.marketplace` uses the same channel condition within the revenue calculation. The order-event calculation joins `order_events.order_id = orders.order_id`. `K_TASK_OVERDUE_T_MKT` uses `tasks.team_id = 'T_MKT'`. DERIVED: these conditions support separate marketplace aggregate and workload projections. They do not grant all Sales data. Q06 requests company revenue; ORG is outside M11 scope.

CONFIRMED: managers, teams, and E25/E26 start on day 75. UNRESOLVED: the first report is morning 75 under static dates or morning 76 under next-morning input effect. The date `2026-10-05` is supplied. The historic marketplace window also needs an explicit policy. Q05 says since team activity began. Do not grant all prior marketplace history by default. A `created_at >= '2026-10-05'` condition is a PROPOSED interpretation for that question, not a general revenue rule: refunds and paid events can refer to older orders.

## Shared orders

DERIVED: Sales uses `orders.order_value_toman`, `order_events.amount_toman`, paid/refunded events, and channel for revenue and conversion KPIs. Operations uses `orders.promised_by`, `orders.city`, `orders.category`, and selected event times for operational KPIs. Marketplace uses channel-filtered order counts and net revenue. Different KPI outputs can use the same source rows.

CONFIRMED: each output must belong to an allowed KPI entity. No `orders.team_id` exists. `order_events.actor_team` identifies an event actor; it is not an order-ownership grant. No source customer table exists for `orders.customer_id`. The exact physical source-row projection for unrestricted questions is UNRESOLVED. Use the supplied KPI formulas internally and show only allowed results. Do not expose order financial rows to Operations merely because Operations needs delivery metrics.

## Query and report boundary

CONFIRMED requirement: enforce scope and purpose in the data layer for every query, including Text-to-SQL. Apply the boundary before data enters an LLM. The same limits apply to reports, evidence, exports, and saved query results. A scoped KPI result and its raw contributors have different access rules. PROPOSED mechanism: separate calculator service identity from manager query roles and use reviewed projections. No such mechanism is implemented by this documentation.
