from audit_support import read, write, finding
import re

doc = 'docs/architecture/002-data-architecture.md'
t = read(doc)
items = [
 (17, '```mermaid', 'Obsolete and misleading data visualization', 'High', 'User visualization standard; existing DSL has component/data-flow views, but no entity ERD or row-level lineage view.', 'Replace three active blocks with accurate Structurizr references and explicit data-model/lineage gaps. Do not imply mandatory SourceFile for a missing-source incident.'),
 (18, '| `ReportVersion` |', 'Incomplete logical entity contracts', 'Medium', 'The document uses many undefined internal entities; workspace.dsl lists shared Insights, grants, cost, manager outcomes and upload revisions.', 'Define logical grains and boundaries for the referenced entities. Keep physical keys/constraints Proposed.'),
 (19, 'S01 ص۱۴', 'Mixed and unclear time semantics', 'Medium', 'Brief p.14 Tehran time; README D-1 eligibility; raw timestamps have no offset.', 'Use one clear time contract. Preserve raw time text and reference arithmetic; distinguish operational cutoff from interactive revision.'),
 (20, '### ۳.۱.', 'Observation presented as a universal binding example', 'Medium', 'RCA CRM-02 and source L02045 rows are a development fixture. The general cutoff and replacement semantics are authoritative.', 'Label the example Observation. Do not turn a fixed lead ID/date into runtime logic.'),
 (21, '| `staff_availability` |', 'Incomplete privacy boundary', 'High', 'Brief pp.6,12-13 prohibits individual attendance monitoring; README permits direct-team capacity purpose, not general disclosure.', 'State that individual attendance/leave status is not a manager display. Capacity formula and small-group inference remain Open.'),
 (22, '### ۶.۱.', 'Count coverage without sufficient per-KPI semantics', 'High', 'All 55 SQL definitions, five reference views, owner/unit/dimension/rule metadata.', 'Add 55 source-backed semantic contracts with exact SQL/hash, date/window, formula, population/filter, NULL/row and precision semantics, plus gates.'),
 (23, '### ۶.۲.', 'Missing reference-view contract detail', 'High', 'reference_views.sql views order_fact, ticket_fact, lead_fact, task_fact, revenue_daily', 'Document selected MIN/MAX fields, correction replacement and COALESCE behavior, grouping, join multiplicity, and execution/value dependencies.'),
 (24, 'priority فقط', 'Incorrect priority scope', 'High', 'Brief pp.3,7,10,13; DSL managerConfig, signals, evidence and reportWriter', 'Allow authorized priorities to shape selection, evidence focus, and role emphasis; never formulas, grants, or unsupported facts.'),
 (25, 'jobها', 'Incomplete independent job outcomes', 'High', 'Accepted independent publication; DSL jobs/requests/publication; PartialPublication view', 'Separate technical job state, package validation/export outcome, and day coverage. Record pre-draft failure and cancellation without inventing output enums.'),
 (26, '`dim_key`', 'Unresolved dimension serialization hidden in a prose note', 'Medium', 'brief_schema.json number.dim is a string; dictionary has four dimensioned definitions; raw dimensions can have empty/NULL cases.', 'Keep no dimension distinct from a NULL dimension. Record the wire policy and test gap explicitly in the Decision Log.'),
 (27, '### ۴.۲.', 'Incomplete source and schema contract evidence', 'Medium', 'Actual delivered headers, day000/day066/day067/day070/day076/day081/day082 manifests and source rows.', 'Add a reproducible read-only source sample check and all delivered header signatures. Do not infer event IDs or customer/campaign parent registries.'),
 (28, 'در S10، هفت', 'Verified attributed source observation', 'Low', 'DQ report sections 3,5,6: 1809 unresolved keys include 1733 numbers and 76 no-row states.', 'Retain the correctly attributed counts without a substantive correction. They are historical observations, not a new calculation, completeness proof or approved hold policy.')
]
for n, needle, cat, severity, source, correction in items:
    finding(n, doc, needle, cat, severity, source, correction,
            'Referenced data and publication policies remain Open; no product test result is implied.',
            'Verified; retained' if n == 28 else 'Corrected')

t = t.replace('# ARCH-001: معماری داده، تاریخچه و محاسبه', '# ARCH-001: معماری داده، تاریخچه و محاسبه\n\nDocument key: `002-data-architecture`. Shared architecture family: `ARCH-001`.')
t = t.replace('`S01..S17`', '`S01..S18`')
texts = [
 'The existing Structurizr views `DataIntake` and `Containers` show component and storage boundaries in the [workspace](../../architecture/structurizr/workspace.dsl). They are not an entity ERD. A detailed entity/relationship visualization is a recorded gap in the [Structurizr gap report](audit-2026-11-09/structurizr-gap-report.md). The logical contracts below remain the data-model proposal. A missing delivery can have a DQ incident without a SourceFile.',
 'Use Structurizr views `DataIntake` and `NightlyData` for intake, quality, and snapshot flow. Source-row mapping and receipt-state detail are not separate existing views; keep them as contracts and record the visualization gap.',
 'Use Structurizr views `EvidenceAndAnalysis`, `ReportDelivery`, and `InteractiveAssistant` for controlled query/evidence/report paths. A number-to-source-row lineage view does not yet exist. The lineage contract is: report number -> registered query/result and context -> contributors/fact fields -> source occurrences -> original file and manifest. This text is a contract, not an invented diagram link.'
]
for body in texts:
    t = re.sub(r'```mermaid\n.*?```', body, t, count=1, flags=re.S)
t = re.sub(r'(?m)^روابط چندبه‌چند.*$', '`Proposed`: represent many-to-many links with explicit association records if the physical design needs them. The former diagram was not a source constraint. A missing-delivery DQ incident refers to ExpectedDelivery rather than a mandatory existing file.', t)
t = re.sub(r'(?m)^S01 ص۱۴.*$', '`Requirement`: source times use Tehran time (brief p.14). Preserve raw timestamp text without adding a new event date. Any standardized instant must retain its source interpretation and raw value. PostgreSQL translation must preserve reference date buckets and arithmetic. UTC conversion alone is not numerical equivalence.', t)
t = t.replace('### ۳.۱. مثال الزام‌آور اصلاح قرارداد', '### 3.1. Observation: historical correction fixture\n\nThe lead ID and amounts below are source observations. The general cutoff and replacement semantics are the contract. Never hard-code this lead, drop, or date as a runtime rule.')
t = re.sub(r'(?m)^\| `staff_availability` \|.*$', '| `staff_availability` | Observation at date/staff_id/team_id | Internal capacity purpose only. No individual attendance/leave display or surveillance. A direct-team workload exception is not an attendance grant. Formula and inference controls remain Open. |', t)
pos = t.index('`dim_key`')
t = t[:pos] + '''### 2.1a. Referenced internal records

All records in this table are Proposed logical contracts. They are not supplied dataset tables or approved physical keys. Preserve any source identifiers separately from generated internal identifiers.

| Record | Logical grain and boundary |
|---|---|
| ExpectedDelivery / DQIncident | One expected source interval and one recorded issue. A missing file needs no fabricated SourceFile. Keep issue evidence, affected dependencies, state history, and unknown closure. |
| SourceSchema | One known header/type/mapping version. Original names and parse receipts remain recoverable. |
| KpiDependency | One versioned dependency contract for a KPI definition: relation, selected value/population fields, join path, clock/window, and structural gates. |
| QueryRun / RegisteredQueryResult | One actual execution and its result at a pinned operational snapshot or interactive revision. Keep SQL/params/hash, engine/definition/type versions, principal/scope, rows, result hash, error, and source pointers. A custom result is not relabeled as a canonical KPI. |
| EvidenceRef | One authorized reference to a query/result, source group, or operational document fragment. Inherit audience and purpose restrictions. |
| SignalEpisode / SignalOccurrence | One continuing issue and one evaluated occurrence. Keep canonical series identity, rule/config versions, quality links, and recipient-specific first/last values and notifications. Reset rules remain Open. |
| InsightVersion | One common analytical source per issue and reporting context. Store eight required content sections and evidence audiences. Share only authorized role projections. Internal schema remains Open. |
| DecisionEvent / ActionDraft | One authenticated human decision and its linked draft. Owner, deadline, success metric and source report are traceable. A draft or decision is not an execution event. |
| OrgNode / OrgEdgeVersion | One organization node and one dated parent-child relationship. Keep known/effective times separate where supplied. Do not invent historical staff transfers. |
| AccessGrantVersion / AuthContext | One governed scope/purpose grant version and one server-built request identity. Access data never comes from the model's assertions. |
| ManagerConfigurationRevision | One authorized settings or KPI-candidate change. Preserve validation, approval, activation, and effective-time history. Canonical formulas remain unchanged. |
| InteractiveEvidenceRevision | One approved set of upload/config/evidence revisions combined with a permitted operational cutoff. Keep upload namespace, successful processing receipt, and audience. Never rewrite a published morning package. |
| ExecutionGrant / BudgetLedger | One bounded parent request and daily cost accounting. Child calls cannot reset limits. Exact limits and model prices remain Open. |
| ManagerJobOutcome / DayRunOutcome | One report/export outcome per required manager and one aggregate coverage record. A failed required job leaves the day incomplete even if other packages publish. |
| WorkflowStageObservation | One case/stage observation at a snapshot. Keep start/end evidence, open/unknown state, SLA kind, median target, owner mapping version, and unresolved responsibility. This is separate from a canonical workflow KPI. |

''' + t[pos:]
pos = t.index('### ۶.۱.')
t = t[:pos] + '''### 6.0. Canonical view semantics

These meanings come from the five supplied views. They are Requirements for calculation equivalence. They are not permission to expose the source rows.

| View | Exact selected behavior and important boundary |
|---|---|
| `order_fact` | `orders LEFT JOIN order_events USING(order_id)`, grouped by order ID. Selected event times are MAX for paid, payment_failed, cancelled, picked, handed_over, delivered. `o.*` must not gain internal metadata columns. Different payloads under one business ID require a conflict policy; grouped bare columns are not a documented last-row-wins rule. |
| `ticket_fact` | `tickets LEFT JOIN ticket_events USING(ticket_id)`. MIN first_response; MAX inspected and resolved; reopened is a separate MAX flag. Reopening does not replace the canonical resolved/backlog formulas with a current-lifecycle interpretation. |
| `lead_fact` | MAX first_contact, qualified, proposal_sent, won, and lost. Contract value is the latest correction by delivered `drop_day DESC`, then COALESCE fallback to MAX won amount. A correction is a replacement, not a new revenue delta. No same-drop secondary order is supplied. A latest NULL correction falls back to won; it does not silently search an earlier non-NULL correction. |
| `task_fact` | Task payload plus MAX done timestamp from a LEFT JOIN. Preserve canonical overdue comparisons and created/due/done clocks. |
| `revenue_daily` | Calendar spine. B2C uses paid order amount minus refund event amount on each event date. Marketplace is a channel subset. B2B uses contract value on won date. Missing joined totals use canonical COALESCE zero; that does not prove a missing source complete. Raw order multiplicity can change revenue joins. |

The [55-KPI semantic contracts](audit-2026-11-09/kpi-contracts.csv) retain every exact SQL statement and hash, all canonical metadata, output clock/window, formula/population meaning, and relevant gates. The existing catalog below remains a readable summary. Full SQL controls any compressed description. Execution dependency is not selected-value dependency, a minimum invalidation proof, or a visibility grant.

''' + t[pos:]
t = re.sub(r'(?m)^configهای قابل تغییر:.*$', '`Requirement`: authorized managers can configure goals, priorities, targets, thresholds, escalation rules, organization, and extensible KPI definitions without code changes. Preserve the 55 canonical definitions. `Proposed`: use the governed candidate lifecycle in document 001 and DSL managerConfig. Priorities can shape ranking/selection, authorized evidence focus, and report emphasis. They cannot change formulas, expand grants, conceal a data issue, or establish a cause.', t)
t = re.sub(r'(?m)^jobها.*$', '`Proposed`: keep technical job states, validation receipts, package/export outcomes, and day coverage separately. Record bounded retry, lease, cancellation, timeout, pre-draft failure, and final failure evidence. The exact state machine remains Open. Technical states must not become new brief/QA enum values. A retry cannot duplicate publication. Failure of one manager does not block another valid package. See ADR-14 and AT-21/28.', t)
pos = t.index('<a id="data-5">')
t = t[:pos] + '''### 4.3. Source observations and unknown contracts

The [read-only source checks](audit-2026-11-09/source-checks.json) record actual manifest counts, header signatures, representative rows, and schema aliases. They do not establish global raw uniqueness, a closed source, or new foreign keys. Event occurrence IDs and customer/campaign parent registries are not supplied. Empty optional links must not create fabricated parents.

Historical review advice to remove all exact order repeats is not a Requirement or an Accepted decision. `review/types-and-missing/report.md` recommends that normalization step, while RCA/KPI-VAL and S16 retain the input-policy question. Keep RAW preservation and the RAW/DEDUP decision separate. Likewise, that report's request to confirm a timezone does not reopen the brief's explicit Tehran-time requirement.

An empty string in CSV is not automatically SQL NULL, zero, or an invalid row. Convert only in derived inputs with a versioned type/empty-value contract. Preserve optional `order_id`, `staff_id`, `campaign_id`, `promised_by`, and correction amounts. Test the exact canonical NULL and no-row behavior. Empty end dates do not grant access or establish a deleted employee.

''' + t[pos:]
t += '\nAudit trail: [AUD-017 through AUD-028](audit-2026-11-09/audit-report.md), [source checks](audit-2026-11-09/source-checks.json), and [semantic KPI contracts](audit-2026-11-09/kpi-contracts.csv). No KPI query was executed by this audit.\n'
write(doc, t)
print('Phase 2 complete: document 002 corrected; AUD-017 through AUD-028 recorded.')
