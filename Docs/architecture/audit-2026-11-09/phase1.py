from audit_support import read, write, finding, replace_span
import re

doc = 'docs/architecture/001-system-blueprint.md'
t = read(doc)
items = [
 (1, '| R1 |', 'Incomplete rule enumeration', 'High', 'dataset/config/escalation_rules.csv records R1-R8; brief pp.6-8', 'Replace the partial rule table with all eight rules, inputs, triggers, outcomes, routing, state, and gates.'),
 (2, '```mermaid', 'Obsolete visualization standard', 'Medium', 'User audit instruction section 6; workspace.dsl views IntegratedOverview, NightlyReporting, NightlyData, NightlyBrief', 'Remove two active diagram blocks. Cite verified Structurizr view keys.'),
 (3, '# ARCH-001:', 'Ambiguous document identifier', 'Low', 'The four files share the ARCH-001 prefix; no separate document-ID specification was found.', 'Retain ARCH-001 as the architecture-family label. Add an explicit unique document key; do not migrate stable IDs.'),
 (4, '| S01 |', 'Missing source discovery', 'High', 'Project_berif contains the PDF and its Markdown conversion.', 'Add S18 for the Markdown brief. Verify important passages against the PDF.'),
 (5, 'Current S01 SHA-256:', 'Misleading source-version emphasis', 'Medium', 'User confirms highlighting/resave; current PDF pp.8,10,15 agree with corresponding Markdown content.', 'Keep the current hash as provenance. Do not report a requirement conflict from a file hash.'),
 (6, '| `InsightBrief` |', 'Missing execution and revision contracts', 'High', 'workspace.dsl requests, documents, queryGateway, modelGateway and InteractiveAssistant/ManagerUpload views', 'Add Proposed execution-grant and interactive-evidence contracts. Map document terms to actual DSL IDs.'),
 (7, '| F: `ManagementInputService`', 'Incomplete configuration lifecycle', 'High', 'Brief p.13 configuration; README KPI extension; workspace.dsl managerConfig and ManagerGovernance', 'Document governed goals, thresholds, priorities, organization, and new inactive KPI validation/activation.'),
 (8, 'هر علت قابل انتشار', 'Unqualified evidence interpretation', 'Medium', 'Brief p.9 requires two independent witnesses, confidence, and alternative causes; no independence algorithm is supplied.', 'Keep the requirement. Mark evidence grouping and independence heuristics Proposed.'),
 (9, 'cache شامل', 'Unapproved fallback stated as guaranteed behavior', 'High', 'S16 Q16 accepts independent publication, while fallback details remain Open; workspace.dsl PartialPublication', 'Label template fallback Proposed. Preserve explicit failure and incomplete-day reporting.'),
 (10, 'سه صفحهٔ اصلی', 'Implementation recommendation presented as scope', 'Low', 'Brief pp.11-12,18 requires three interfaces, not exactly three pages.', 'Distinguish required interfaces from Proposed page layout.'),
 (11, '### ۹.۱.', 'Incomplete report contract', 'High', 'Brief pp.9-11: report item, chart specification, decision card, health, open actions, read/decision/referral state', 'Add complete content requirements and separate internal representation from permissive wire schemas.'),
 (12, '`data_issues.source`', 'Undeclared schema mapping', 'Medium', 'brief_schema.json data_issues source/type enums; no source-family alias contract supplied', 'List exact enums. Label detailed-file to source-family mapping Proposed.'),
 (13, 'نسخهٔ اول به message broker', 'Unapproved infrastructure exclusion', 'Low', 'S16 Q01 accepts one Agent; no source mandates the other named infrastructure choices.', 'Keep one Agent Accepted. Mark infrastructure deferral Proposed.'),
 (14, 'هر مقایسه فقط', 'Incomplete rule boundary inventory', 'Medium', 'R2 explicitly uses more than escalate_after_days and worsening >=20%; R4 does not define its change comparand; R3 can lack a numeric warn.', 'Separate explicit source comparisons from genuinely Open edge cases.'),
 (15, 'گردکردن در خود SQL', 'Missing governed KPI extension detail', 'Medium', 'README permits additions and prohibits changing existing definitions; brief p.13 requires configurable KPIs.', 'Preserve canonical definitions. Describe inactive candidate registration, validation, human approval, and versioned activation as Proposed mechanism.'),
 (16, 'مالک انتهابه‌انتهای', 'Incomplete workflow-stage coverage', 'High', 'workflow_definitions.csv has 12 stages, targets, numeric SLA, deadline reference, and one blank SLA.', 'Add all 12 stage records and distinguish workflow owner, stage owner, median target, SLA, and canonical KPI.')
]
for n, needle, cat, severity, source, correction in items:
    finding(n, doc, needle, cat, severity, source, correction,
            'See the referenced ADR and Decision Log for unresolved policy details.' if n in {1,6,7,8,9,12,14,15,16} else 'None.')

t = t.replace('# ARCH-001: طرح معماری سیستم ARKA', '# ARCH-001: طرح معماری سیستم ARKA\n\nDocument key: `001-system-blueprint`. `ARCH-001` is the retained architecture-family label. It is not a unique document ID.')
row = '| S18 | [Markdown brief](../../Project_berif/دیدراه-بریف-دستیار-ایجنتیک-مدیران.md) | Text source beside S01. Page comments retain the PDF page numbers. Important passages were checked against S01. Highlighting and resaving do not establish changed requirements. |'
pos = t.index('\n\n', t.index('| S17 |'))
t = t[:pos] + '\n' + row + t[pos:]
t = re.sub(r'(?m)^Current S01 SHA-256:.*$', 'S01 provenance hash: `6d68d3fcc285f6908af0d97c0429dfefb489f00b7f6538ed03573552ed6955f8`. The current PDF and S18 agree on the checked requirements. No requirement conflict is established by the earlier file-hash difference.', t)
replacements = [
 'Use the existing [Structurizr workspace](../../architecture/structurizr/workspace.dsl), view keys `IntegratedOverview`, `Containers`, `DataIntake`, `DeterministicAnalytics`, and `EvidenceAndAnalysis`. These keys exist in the DSL. They identify target views, not installed components. See the [view catalog and gaps](audit-2026-11-09/structurizr-gap-report.md).',
 'The existing Structurizr views `NightlyReporting`, `NightlyData`, and `NightlyBrief` show the scheduled path. `InteractiveAssistant` and `ManagerUpload` show the interactive path. `PartialPublication` shows independent failure outcomes. Use the [view catalog](audit-2026-11-09/structurizr-gap-report.md) to locate each declaration.'
]
for replacement in replacements:
    t = re.sub(r'```mermaid\n.*?```', replacement, t, count=1, flags=re.S)

pos = t.index('### Input and document boundary')
t = t[:pos] + '''### Configuration and execution ownership

`Requirement`: authorized managers can change goals, priorities, targets, warning thresholds, escalation rules, and organization without code changes. Additions to the KPI dictionary are permitted. The existing 55 definitions remain unchanged. A preference cannot expand access or change a numeric result.

`Proposed mechanism`, consistent with DSL `managerConfig`: register a new inactive KPI version; validate SQL safety, inputs, units, reference rounding, scope, rollups, and deterministic execution; record a human approval; then activate the approved version at a governed effective time. Preserve the previous version. Approval roles and exact activation rules remain Open. Do not turn a request to change a canonical formula into an unrecorded overwrite. See ADR-01, ADR-06, ADR-08, and AT-27.

The DSL `requests` controller owns the whole execution grant. It covers investigation steps, tools, elapsed time, retries, cancellation, and the parent request. The DSL `modelGateway` owns individual model calls and shared daily cost enforcement. Neither boundary can reset the parent's limits. Exact limits remain Open under ADR-10. See AT-20 and AT-28.

| Document term | Existing DSL identifier | Boundary |
|---|---|---|
| SourceAdapter / IngestionCoordinator | `ingestion`, `quality` | Structured intake and data issues. |
| SnapshotService / ProjectionService | `snapshots` | Versioned eligible inputs and derived observations. |
| SemanticRegistry / ReferenceCalculator | `managerConfig`, `kpi` | Definition governance and deterministic PostgreSQL calculation. |
| SignalEngine / WorkflowEngine | `signals`, `workflows` | Separate deterministic rules and process reconstruction. |
| AnalysisCoordinator | `requests`, `agent`, `evidence`, `insights` | One bounded Agent and controlled common analysis. |
| ManagementInputService | `requests`, `managerConfig`, `documents`, `decisions` | Authorized settings, uploads, decisions, and lifecycle. |
| Publisher / QueryGateway | `publication`, `reportWriter`, `outputValidator`, `queryGateway` | Role content, validation, independent delivery, and controlled queries. |
| ReplayRunner | `jobs`, `audit` | Scheduled execution and evidence of outcomes. |

These mappings preserve existing elements. They do not add runtime components. The API handles both runtime paths. The worker handles deterministic processing in the same modular codebase.

''' + t[pos:]
pos = t.index('\n\n', t.index('| `DecisionEvent`'))
t = t[:pos] + '''
| `ExecutionGrant` | Proposed internal contract: parent request, trusted principal, permitted tools, pinned snapshot/evidence revision, cost reservation, step/token/time/retry limits, deadline, and cancellation state. Exact limits remain Open. |
| `InteractiveEvidenceRevision` | Proposed internal contract: operational drop cutoff plus successful authorized upload/config revisions and their receipt/readiness. It never changes an immutable morning report. |
| `ManagerJobOutcome` | Proposed internal contract: manager/report key, state, validation/export outcome, safe failure reason, and retry/version references. Record failure even if no draft exists. Day coverage is a separate result. |''' + t[pos:]
t = t.replace('### ۷.۱. قواعد قطعی و سابقهٔ مخاطب', '### 7.1. Complete R1-R8 contract\n\nThe source is `dataset/config/escalation_rules.csv`, records R1-R8. Each rule below is a Requirement. State-field names and the storage mechanism are Proposed. Rule routing never creates a new access grant.')
a = t.index('قواعد S11 به‌صورت داده'); b = t.index('`series_key =', a)
t = t[:a] + '''Use canonical KPI metadata, the eligible snapshot, calendar fields, and recipient history as inputs. Keep source quality separate from the business state. A data issue is not a business signal. R7 forbids alerts for `info` metrics. R8 gates `threshold_from_day8` before threshold evaluation.

| Rule / source record | Exact source meaning and trigger | Inputs | Output and routing | State and planned gates |
|---|---|---|---|---|
| R1 / 2 | Each signal first reaches the lowest responsible level named by `owner_manager_id`. | Canonical owner, active organization, eligible signal. | Route to that owner. An inactive or unresolved owner is a routing issue; do not guess a replacement. | Proposed: unrouted to owned. Preserve the canonical owner. AT-08, AT-24. |
| R2 / 3 | Escalate upward if `crit` is crossed, warning lasts **more than** `escalate_after_days`, or deterioration is **at least 20%** relative to the first report. | Direction, warn/crit, duration, first reported value, recipient history, hierarchy. | An escalated occurrence with explicit reason and history. Use the higher level; exact multi-level timing remains Open. | Proposed: owned/open to escalated for the recipient. Keep earlier recipient history. AT-08, AT-24. |
| R3 / 4 | Escalate a Workflow or organization-level indicator to M01 when it crosses warn. | Indicator kind/entity, numeric warn if supplied, eligible value, direction. | Executive escalation with its reason. It does not authorize disclosure of restricted source evidence. | Preserve prior owner history. Behavior when the selected rule has no numeric warn remains Open. AT-08, AT-24. |
| R4 / 5 | A signal with less than 10% meaningful change must not be reported again as new; it remains in the open list. | Same signal, recipient history, comparable values. | Suppress a new repeat for the same recipient. Retain open state. Wire representation remains ADR-09. | Preserve history, not a new episode. The comparison reference, zero denominator, and recovery/reset details remain Open. AT-08, AT-24. |
| R5 / 6 | `dow_baseline:N` compares with the median of the same weekday in the previous four weeks. Deviation **greater than N%** is a signal. Official holidays are exempt. | Eligible same-weekday observations, `N`, supplied calendar weekday/holiday, snapshot. | A supported deviation and baseline receipt, or an explicit unavailable evaluation. Initial routing uses R1. | Missing/zero baseline, minimum observations, direction interpretation, and treatment of historical holiday samples remain Open. Do not call unknown normal. AT-03, AT-09, AT-24. |
| R6 / 7 | At most five important items per report. Signals with the same cause across teams/systems form one item. | Eligible signals, cause evidence, priority context, recipient scope. | At most five recipient-authorized items. Preserve the grouped series and owners internally. | Proposed grouping and ranking need evidence; a guessed cause cannot merge owners away. Exact weights remain Open. AT-08, AT-10, AT-11, AT-24. |
| R7 / 8 | `info` metrics are for display only and never create alerts. | Canonical `rule=info`, value, scope. | Display eligible information. No alert occurrence or escalation is created from this metric. | A displayed value does not enter an alert episode. Other eligible metrics can still alert. AT-02, AT-24. |
| R8 / 9 | `threshold_from_day8` is threshold logic evaluated only from day 8 of each Jalali month. | Supplied `cal.day_in_month`, threshold metadata, eligible value. | Before day 8: no threshold alert. From day 8: use the threshold path and normal ownership. | Keep month/knowledge versions. Do not use Gregorian day-of-month or guessed calendar corrections. AT-03, AT-07, AT-24. |

Source distinctions are fixed: R2 uses `> escalate_after_days` and `>=20%`; R5 uses `>N%`; R4 excludes a new repeat for `<10%`. The source does not settle every equality or zero-baseline case. ADR-07 retains only those remaining choices. Candidate formulas, baseline sample rules, episode recovery, and the R3 missing-warn case must be named and approved before use.

The brief p.8 requires recurrence/escalation checks at three points: detection, report construction, and final validation. Use the same rule and recipient-history versions at all three points. A later check must not create a second occurrence. AT-24 covers each rule and each control point.

''' + t[b:]
pos = t.index('projection فرآیند')
t = t[:pos] + '''#### All supplied Workflow stages

The following 12 records come from `workflow_definitions.csv`. Every workflow has end-to-end owner `M01`. That fact does not establish a stage owner. Duration targets are median targets, not substitutes for SLA. Stage-to-team responsibility remains Open under ADR-15.

| Stage / CSV record | From | To | SLA | Median target, hours |
|---|---|---|---|---|
| WF1.1 / 2 | `created_at` | `paid` | 1 hour | 0.25 |
| WF1.2 / 3 | `paid` | `picked` | 12 hours | 4 |
| WF1.3 / 4 | `picked` | `handed_over` | 6 hours | 3 |
| WF1.4 / 5 | `handed_over` | `delivered` | `promised_by` deadline reference | 24 |
| WF1.5 / 6 | `delivered` | ticket with follow-up category | Not supplied | Not supplied |
| WF2.1 / 7 | `created_at` | `first_response` | 8 hours | 4 |
| WF2.2 / 8 | `first_response` | `inspected` | 36 hours | 18 |
| WF2.3 / 9 | `inspected` | `resolved` | 24 hours | 8 |
| WF3.1 / 10 | `created_at` | `first_contact` | 24 hours | 8 |
| WF3.2 / 11 | `first_contact` | `qualified` | 72 hours | 48 |
| WF3.3 / 12 | `qualified` | `proposal_sent` | 120 hours | 96 |
| WF3.4 / 13 | `proposal_sent` | `won/lost` | 720 hours | 400 |

WF1.5 uses the source label `ticket پیگیری سفارش`, not a supplied order-event type. Its exact ticket-category/time projection remains an implementation contract to specify. Missing SLA is not zero. `promised_by` is a deadline field, not a duration of 24 hours.

Canonical workflow KPIs are separate: WF1 checks its four SQL conditions; WF2 checks resolved-minus-created within 48 hours; WF3 uses a rolling seven-day closed-lead population and checks first contact, qualified-to-proposal, and proposal-to-close. Its SQL does not include the WF3.2 72-hour test. Do not add that stage test to the canonical formula. Stage-level observations still include all four WF3 stages. See AT-12 and AT-25.

''' + t[pos:]
t = t.replace('هر علت قابل انتشار باید حداقل دو گروه شاهد مستقل داشته باشد.', '`Requirement`: every published cause needs at least two independent witnesses, confidence, and alternative causes (brief p.9). `Proposed`: use lineage-aware evidence groups to implement that check. The independence test itself is not supplied as an approved algorithm.')
t = re.sub(r'(?m)^cache شامل.*$', '`Proposed`: key caches by snapshot, query/result hash, scope, policy, model, prompt, and evidence revision. A template fallback can use only validated numbers and supported content. Fallback selection, timeout, and repair limits remain Open. If it cannot pass validation, record report failure. Independent publication is Accepted; it is not a promise that every failed model call can be replaced successfully.', t)
t = re.sub(r'(?m)^سه صفحهٔ اصلی.*$', '`Requirement`: provide a Persian RTL conversational assistant, a role-based BI dashboard, and an executive-only Workflow control room. `Proposed`: these can share a frontend and page layout. Exactly three pages is not a source requirement. Decision/action history and permitted query drill-down must remain available.', t)
pos = t.index('### ۹.۱.')
t = t[:pos] + '''### Complete report content

The following content is required by brief pp.9-12. The supplied JSON schema does not define every field below. `Proposed`: keep these fields in an internal validated content model. Final wire placement remains Open where the schema does not prescribe it. Do not change source schemas.

| Output | Required fields or behavior | Source / gate |
|---|---|---|
| Morning item | Title, number and target, possible cause, owner, suggested question. | p.10; AT-26 |
| Chart specification | Chart type, metric, time range, breakdown, target line. Charts are required output, not optional architecture diagrams. | pp.10-11; AT-26 |
| Important/escalated decision card | Problem, options, supported estimated effect, cost, risk, confidence, execution owner, deadline, success criterion, and supporting evidence. No invented estimate. | pp.10-12; AT-10, AT-14, AT-26 |
| Common package | Health of scope, at most five important items, pending decisions, open actions and deadlines, observed decision effects, dashboard link. | pp.10-11; AT-11, AT-26 |
| State and operations | Read state, recorded decision, referral; authorized close/referral operations in conversation. These do not execute organizational actions. | pp.3,11-12; AT-14, AT-29 |
| Executive content | Five key health indicators, all three workflows and stage bottlenecks, escalations, pending decisions, prior decision effects. | pp.5,11; AT-12, AT-26 |
| Unit/supervisor content | Authorized unit/team health; direct-team work and blockers only where individually permitted. Upper roles get aggregates. | pp.5,10,13; AT-06, AT-26 |
| Monthly board summary | Optional at month end. It is not a daily acceptance dependency. | p.10; AT-26 scope check |

Internal Insight fields must cover all eight brief sections: summary/impact; metric/deviation; breakdown; possible causes/confidence; decision options; history/prior decisions; proposed owner; registered queries. Use authorized projections of the shared analytical source. Do not repeat unrestricted deep analysis per manager. The exact internal schema remains Open under ADR-09.

''' + t[pos:]
t = re.sub(r'(?m)^`data_issues.source`.*$', '`Requirement`: `data_issues.source` is one of `orders, tickets, crm, tasks, marketing, sessions, availability`. `data_issues.type` is one of `missing, late_arrival, duplicate, schema_change, late_correction, other`. `Proposed`: map csat/ticket-event issues to the tickets family and retain the actual file in an authorized detail. This alias mapping is not a supplied per-file contract. Do not add enum values. See AT-30.', t)
t = re.sub(r'(?m)^نسخهٔ اول به message broker.*$', '`Accepted`: use one bounded AI Agent. `Proposed`: defer a broker, Kubernetes, graph/vector databases, and other infrastructure until a measured need supports a separate ADR. The source does not prohibit these technologies. PostgreSQL remains the only product database engine.', t)
t += '\nAudit trail: [detailed findings](audit-2026-11-09/audit-report.md), [traceability matrix](audit-2026-11-09/requirements-traceability.csv), and [Structurizr gaps](audit-2026-11-09/structurizr-gap-report.md). All product acceptance gates remain planned.\n'
write(doc, t)
print('Phase 1 complete: document 001 corrected; AUD-001 through AUD-016 recorded.')
