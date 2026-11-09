from audit_support import read, write, finding

finding(59, 'docs/architecture/001-system-blueprint.md', '`submission/briefs/day_XXX',
    'Incomplete schema-required and enum enumeration', 'High',
    'brief_schema.json root/item/number required sets and all enums; qa_answer_schema.json required sets/statuses.',
    'Add exact wire required sets, nullable value rule, confidence bound, and all follow-up effect directions. Keep schema and semantic requirements distinct.',
    'suppressed mapping, extra-query IDs and complete content mapping remain Open.')
p='docs/architecture/001-system-blueprint.md';t=read(p)
pos=t.index('### Last valid value and report failure')
t=t[:pos]+'''### Exact wire-schema boundaries

Read the [complete property/pointer register](audit-2026-11-09/output-schema-contracts.csv) for every supplied field. These schema rules do not replace narrative, numerical, or access requirements.

| Scope | Exact source constraint | Additional semantic boundary |
|---|---|---|
| Brief root | Required: `report_day, manager_id, items, numbers, data_issues, text_fa`. | Check active roster, cutoff, Persian content and required report sections. An integer report_day alone proves no valid replay day. |
| Each item | Required: `item_id, status, kpi_id, entity_id, dim, kpi_date, value, causes, owner_manager_id`. At most five items. | Correct owner, cause support and recurrence are separate checks. An empty causes array can pass schema but does not prove a supported cause or official event detection. |
| Number / evidence entry | Required: `kpi_id, entity_id, dim, kpi_date, value`. `value` is numeric or null. `query_id` is schema-optional. | The brief still requires a registered query for every reported number. Check date, unit, precision, snapshot/revision and scope. |
| Item status | `new, escalated, ongoing`. | The brief's `suppressed` conflict stays Open. Never invent a fourth wire enum or silently relabel an item. |
| Cause confidence | Optional numeric `confidence`, minimum 0, maximum 1. | It cannot contain a qualitative string or an invented/calibrated-probability claim. Use the reviewed confidence boundary above. |
| Decision follow-up effect | `improved, worsened, no_change, too_early`. | Evidence must support the stated observation. An enum is not proof of execution or causality. |
| QA root/status | Required: `question_id, manager_id, answer_status, answer_fa`. Status: `answered, refused_out_of_scope, refused_individual_data, data_unavailable, clarification_requested`. | Refusals need no fabricated rows or SQL. A technical job failure is not a new QA enum. Actual rows/SQL/definition are shown when valid and permitted. |
| Optional structures | `open_items`, `decision_followups`, `mentioned_staff_ids`, chart/card-related content and QA rows have the supplied property/type rules. | Optional wire fields do not remove the brief's required content or named-staff registration. Extra fields permitted by the schema are not automatic evaluator approval. |

''' + t[pos:]
write(p,t)
print('Cross-document schema omissions corrected; AUD-059 recorded.')
