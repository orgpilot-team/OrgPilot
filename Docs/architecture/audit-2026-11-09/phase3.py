from audit_support import read, write, finding
import re

doc = 'docs/architecture/003-decisions-and-roadmap.md'
t = read(doc)
items = [
 (29, '# ARCH-001:', 'Ambiguous family/document identity', 'Low', 'Shared prefix in the four files; stable unique filename keys.', 'Keep ARCH-001 as family metadata and add the unique document key.'),
 (30, '**Status:** Requirement: R1-R8.', 'Incomplete boundary precision', 'High', 'escalation_rules.csv R2-R5,R7-R8; brief p.8 controls at three points.', 'Link the complete rule contract. Add missing-warn and R4 reference ambiguities without reopening explicit comparisons.'),
 (31, 'clarification/data_unavailable', 'Invalid enum shorthand', 'Medium', 'qa_answer_schema.json /properties/answer_status/enum', 'Use clarification_requested or data_unavailable; do not publish clarification as a status.'),
 (32, '### 7.2.', 'Missing non-question input coverage', 'High', 'scripted_inputs.json has 23 events: 16 questions and seven other inputs across five types.', 'Add all seven non-question contracts and all-23 receipt tests, plus close/referral requirements from the brief.'),
 (33, '| <a id="at-08"', 'Incomplete acceptance coverage', 'High', 'R1-R8, all Workflow stages, report content, KPI lifecycle, execution grants, JSON schema properties.', 'Preserve AT-01..23. Add AT-24..30 for the uncovered contracts. Mark every product gate planned, not passed.'),
 (34, 'All rows below are `Open`.', 'Decision Log lacks exact source and closure evidence', 'High', 'Each DL row relies on distinct brief pages, CSV records, JSON pointers, and recorded decisions.', 'Retain DL-01..16; add source-location and closure-evidence columns. Add missing dimension/content/config decisions.'),
 (35, '| پیچیدگی دو dialect', 'Obsolete runtime risk wording', 'Medium', 'Accepted PostgreSQL-only product engine; ADR-01 permits a separate test oracle.', 'State translation/oracle maintenance risk; do not imply two product query engines.'),
 (36, 'fallback قطعی، گزارش قابل استفاده', 'Proposed fallback stated as mandatory success', 'High', 'S16 Q16 and ADR-14; failure may precede a draft and remain a failed required report.', 'Condition fallback acceptance on selection and validation. Otherwise retain explicit failure and incomplete day.'),
 (37, '**Gate:** AT-08 and AT-12', 'Missing stage-contract test', 'Medium', '12 workflow_definitions.csv stages; canonical WF2/WF3 differ from full stage SLA.', 'Add AT-25 and retain Open owner mapping. Do not imply an official missing-owner policy.'),
 (38, 'The three architecture documents are reconciled', 'Verification scope too broad', 'Medium', 'Previous review checked links/counts; the current audit finds semantic omissions.', 'Replace general completion wording with evidence-linked audit, traceability, and current verification scope.'),
 (39, '| <a id="at-19"', 'Mixed requirement and engineering gate authority', 'Medium', 'Brief p.18 requires Docker delivery; backup/restore specifics are engineering proposals.', 'Add an acceptance-basis register. Separate official requirements, Accepted boundaries, and Proposed mechanisms.'),
 (40, '**Gate:** AT-14. Product owns', 'Human execution status ambiguity', 'Medium', 'Brief pp.11-12; existing HumanDecisionFollowUp view records human-reported status, never execution by ARKA.', 'Preserve the target lifecycle, but keep actual confirmation schema/authority Open. No source decision proves execution.'),
 (41, 'Sources S01-S17', 'Stale source enumeration', 'Low', 'Discovered Markdown brief S18 and current accepted-decision confirmation.', 'Update the source range and identify the audit request as confirmation, not a replacement requirement specification.'),
 (42, 'مرور سه سند', 'Stale review/delivery scope', 'Low', 'Current task audits four numbered documents and dependent documentation.', 'Keep the roadmap Proposed; update P0 review and clarify P2 is not complete without required content and workflows.')
]
for n, needle, cat, severity, source, correction in items:
    finding(n, doc, needle, cat, severity, source, correction,
            'Policies in the Decision Log remain unresolved. Listed owners are roles for review, not invented named assignees.')

t = t.replace('# ARCH-001: تصمیم‌ها، ریسک‌ها و مسیر پیاده‌سازی', '# ARCH-001: تصمیم‌ها، ریسک‌ها و مسیر پیاده‌سازی\n\nDocument key: `003-decisions-and-roadmap`. Shared architecture family: `ARCH-001`.')
t = t.replace('Sources S01-S17', 'Sources S01-S19')
t = t.replace('The recorded team decisions are one bounded AI Agent, PostgreSQL as the only product database engine, and independent publication of valid reports.', 'The user confirms five Accepted boundaries: one bounded AI Agent with deterministic modules; PostgreSQL-only product execution; independent valid-report publication; deterministic calculation, signal detection, authorization, and final validation; and human-controlled organizational decisions.')
t = t.replace('clarification/data_unavailable', '`clarification_requested` or `data_unavailable`')
pos = t.index('قواعد اصلی R1-R8')
t = t[:pos] + '''Read the [complete R1-R8 contract](001-system-blueprint.md#system-7) and [rule traceability](audit-2026-11-09/requirements-traceability.csv). R2 explicitly uses more than the escalation duration and deterioration at least 20% from the first report. R5 explicitly uses deviation greater than N%. R4 explicitly forbids a new repeat below 10% change. R7 never alerts. R8 gates on Jalali day 8. These are not open choices.

The remaining ambiguity includes the R4 comparison reference, recovery/reset, and R3 when a baseline-rule KPI has no numeric warn. Do not invent a warning threshold for that case. Source-defined comparisons and the three control points must remain unchanged. See AT-24.

''' + t[pos:]
t = t.replace('| پیچیدگی دو dialect | خطای مسیر query و هزینهٔ نگهداری | interface واحد، reference result authoritative و ثبت engine هر query. |', '| Translation and reference-oracle maintenance | Different SQL behavior can change rounded values or row sets. | One PostgreSQL product path; separate versioned test oracle and translation receipts. |')
t = re.sub(r'(?m)^\*\*شرط تصویب:\*\* روز پرترافیک.*$', '**Gate:** include all daily reports, selected analysis, scripted QA, retries, and bounded repairs in cost/time measurements. If a template fallback is selected, it must pass all validators. Otherwise record an explicit failed manager job. Do not require an unapproved fallback to succeed. Infrastructure costs are reported separately from the LLM cap.', t)
t = t.replace('**Gate:** AT-08 and AT-12, including an unmapped stage and a unit actor.', '**Gate:** AT-08, AT-12, and AT-25, including every supplied stage, an unmapped stage, and a unit actor.')
t = t.replace('**Gate:** AT-14. Product owns lifecycle details.', '**Gate:** AT-14 and AT-29. The existing HumanDecisionFollowUp view preserves a human-reported status path. Exact confirmation fields, authority, and evidence remain Open. Product owns these details. A decision or a written task never proves that the organization executed it.')
t = t.replace('مرور سه سند', 'review all four numbered documents and dependent contracts')
pos = t.index('در هر مرحله، CSVهای audit')
t = t[:pos] + '''A P2 full-day milestone includes all required report content, chart specifications, decision cards where required, three Workflow summaries, JSON twins, and active-manager coverage. If any are absent, label the milestone partial. P3 adds historical depth and edge-case coverage; it does not excuse a missing mandatory P2 output. The roadmap is Proposed, not evidence of completed work or fixed team capacity.

''' + t[pos:]
pos = t.index('\n\n', t.index('| <a id="at-23"'))
t = t[:pos] + '''
| <a id="at-24"></a>AT-24 | Complete R1-R8 | Test each rule separately and in composition at detection, report construction, and final validation. Preserve explicit comparisons, ownership, history, holiday exemption, info-only behavior, and Jalali day gate. Name unresolved cases; do not silently choose them. |
| <a id="at-25"></a>AT-25 | All Workflow stages | Test all 12 stage definitions, endpoints, SLA kinds, and median targets. WF1.4 is a deadline; WF1.5 has no SLA. Preserve WF2 48h and WF3 canonical predicates separately from stage observations. Unknown stage owner remains unresolved. |
| <a id="at-26"></a>AT-26 | Full report content | Check the eight Insight sections, item title/target/owner/suggested question, chart type/metric/range/breakdown/target line, required decision-card fields, health, pending decisions, open actions, dashboard link, and read/decision/referral state. Monthly summary remains optional. |
| <a id="at-27"></a>AT-27 | Governed configuration and KPI extension | Validate authorized changes without code edits. Preserve the 55 canonical definitions. Test inactive candidate registration, SQL/type/unit/scope/rollup checks, approval and versioned activation using an approved lifecycle policy. Priorities cannot alter facts or grants. |
| <a id="at-28"></a>AT-28 | Parent execution grant | Child model, tool, query, retry, upload-processing and repair work cannot reset parent limits. Test timeout, cancellation, exhausted budget and failure propagation before/after a draft. Keep technical failure states separate from output enums. Exact limits need approval. |
| <a id="at-29"></a>AT-29 | Manager input lifecycle | Exercise all 23 supplied events through authorized operations with receipt/effective times and idempotency. Verify all 16 QA files and seven non-question effects. Test authorized close/referral with separate fixtures; never mutate original data or treat upload text as a decision. |
| <a id="at-30"></a>AT-30 | Exact output contracts | Validate all schema-required fields, nested types, maxItems, date/value representation and every enum. Apply stronger source traceability checks separately. An example file or schema pass is not numerical, semantic, or authorization acceptance. |''' + t[pos:]
pos = t.index('### ۷.۱.')
t = t[:pos] + '''Every AT row is a planned product gate. No AT row passed in this audit. The [acceptance-basis register](audit-2026-11-09/acceptance-basis.csv) states the source and Requirement/Accepted/Proposed basis for each gate. Engineering mechanisms such as restore, exact retry behavior, atomic package commit, and candidate approval need their own approved policy before a pass can be asserted.

#### Rule-specific cases for AT-24

| Rule | Minimum planned source-backed cases | Unresolved case treatment |
|---|---|---|
| R1 | New signal routes to canonical owner; no owner substitution or grant expansion. | Inactive/unmapped owner remains a routing issue. |
| R2 | Beyond-crit value; duration equal to N versus greater than N; deterioration exactly 20% from first report. Preserve reasons/history. | Exact crit equality, zero first value, unknown days, and multi-level clock need approved policy. |
| R3 | Workflow/ORG indicator beyond warn reaches M01 with authorized evidence. | Missing numeric warn is Open; do not synthesize one from a baseline percentage. |
| R4 | Same recipient with less than 10% change is not new and remains open. | Exactly 10% does not automatically prove a new item; comparison reference/reset remain Open. |
| R5 | Four previous same-weekday observations; median baseline; deviation greater than N; official-holiday exemption. | Missing samples, zero baseline, direction, and historical holiday population need approved policy. |
| R6 | More than five candidates still produces at most five items. Supported same-cause groups preserve authorized series/owner history. | Ranking weights and evidence-group algorithm remain Proposed. |
| R7 | K_ENT_CONTRACT_MTD, K_DIG_SPEND, and K_MKT_REV can display but never alert. | Data availability still applies; info is not an access or source-quality exemption. |
| R8 | Same eligible threshold value on Jalali day 7 and day 8: no early threshold alert, then normal evaluation. | Threshold equality remains named policy; the day-8 gate itself is fixed. |

''' + t[pos:]
pos = t.index('### ۷.۳.')
t = t[:pos] + '''### 7.2a. Non-question manager inputs

Source: S07. These are requirement fixtures, not runtime hard-coded IDs. Their exact input records, days, actor, content and expected boundary are retained in the [manager-input contracts](audit-2026-11-09/manager-input-contracts.csv).

| Input | Required effect and boundary | Planned gates |
|---|---|---|
| IN01, day 62, M01, priority | Store focus on delivery and customer experience for later authorized selection, evidence, and report emphasis. It changes no formula or permission. | AT-07, AT-29 |
| IN02, day 68, M04, decision DE-01 | Record temporary staff-transfer decision and approved drafts/follow-up. Do not perform a transfer or fabricate a dated staff assignment. Later fixed replay data is the observation source. | AT-14, AT-29 |
| IN03, day 69, M04, decision DE-02 | Record FAQ publication decision and drafts/follow-up. ARKA does not publish to a real site. | AT-14, AT-29 |
| IN04, day 73, M01, upload | Register meeting minutes as untrusted evidence. Embedded instructions and meeting text do not change grants, numbers, recipients, or action authority. | AT-13, AT-22, AT-29 |
| IN05, day 75, M01, org_change | Version T_MKT/M11/E25/E26 change without code edits. Static effective day versus next-morning precedence remains ADR-08. | AT-07, AT-15, AT-29 |
| IN06, day 78, M04, threshold_change | After authority checks, version K_RSP_FRT_MED warn from 3h to 4h for morning 79. Preserve prior rules and canonical formula. Read access alone does not establish write authority. | AT-07, AT-29 |
| IN07, day 80, M02, upload | Register external sales CSV after receipt and successful processing. Do not infer its definition from two values or read it early for manager Q09. | AT-03, AT-22, AT-29 |

The brief also requires authorized close/referral operations, goal/target changes, and configurable KPI definitions. They are not all present as supplied fixture types. Test them separately without editing S07. For a question on day D, operational drops stop at D-1; same-day uploaded evidence needs an authorized ready revision and must not rewrite the morning report.

''' + t[pos:]
sources = {
 'DL-01':'S16 Q03 body/result; S03 records 2-56; S04 views; S02 KPI contract.',
 'DL-02':'S03; day_076/orders.csv and manifest; RCA ORD-01..03; KPI-VAL sections 2-5; S16 Q05.',
 'DL-03':'S02 unavailable-value rule; DQ sections 3/6; S16 Q06 result; S17 reportWriter.',
 'DL-04':'S02 cutoff; S04; S16 Q07; S17 snapshots; ADR-03/05.',
 'DL-05':'S04 lead_fact ORDER BY drop_day DESC and grouped bare payloads; RCA CRM-03; S16 Q08.',
 'DL-06':'S05 access_matrix records 2-12; S01/S18 pp.5,10,13; manager Q03/Q08 in S07.',
 'DL-07':'S01/S18 pp.6,9,12-13; staff_availability/staff/calendar; S16 Q10.',
 'DL-08':'workflow_definitions.csv records 2-13; kpi_dictionary workflow rows; S16 Q11.',
 'DL-09':'escalation_rules.csv records 2-9; KPI direction/rule metadata; S01/S18 p.8; S16 Q12.',
 'DL-10':'S05 M11/T_MKT/E25/E26 day 75; S07 IN05 and manager Q09/IN07; S02 input timing.',
 'DL-11':'S01/S18 pp.9-10,15-16; S06 item.status and number/query fields; S16 Q14.',
 'DL-12':'S01/S18 pp.11-12,15; S07 IN02/IN03; S17 HumanDecisionFollowUp.',
 'DL-13':'S16 Q16 result; S17 PartialPublication; S02 active-manager coverage; S06 output schemas.',
 'DL-14':'S16 Q01/Q17; S17 requests/modelGateway; S01/S18 pp.14,16,19.',
 'DL-15':'S17 rawFiles/postgres/audit; ADR-12 engineering proposal; no supplied interval contract.',
 'DL-16':'S01/S18 pp.14,16-19; S02 hidden evaluation; missing official raw-column dictionary.'
}
lines = t.splitlines()
for i, line in enumerate(lines):
    if line.startswith('| ID / review |'):
        lines[i] = '| ID / review | Source locations | Conflict or missing choice | Options and architectural effects | Owner / gate | Closure evidence needed |'
        lines[i+1] = '|---|---|---|---|---|---|'
    m = re.match(r'^\| (DL-\d{2}) /', line)
    if m:
        c = [s.strip() for s in line.strip('|').split('|')]
        key = m[1]
        closure = 'Recorded policy/source answer plus the named implementation-gate evidence. No pass is asserted here.'
        if key == 'DL-16': closure = 'Organizer profile/hardware and official evaluation evidence; dictionary or documented missing-contract disposition.'
        lines[i] = '| ' + ' | '.join([c[0], sources[key], c[1], c[2], c[3], closure]) + ' |'
t = '\n'.join(lines) + '\n'
pos = t.index('Implementation remains outside this task.')
t = t[:pos] + '''| DL-17 / output | S06 number.dim string and optional query_id; S02 number trace rule; S03 dimension metadata. | NULL dimension versus no dimension; added-query/evidence wire identifiers. | Keep internal distinctions; confirm serialization and reference mapping. Do not invent a sentinel that changes a canonical dimension. | Product/organizer; ADR-09; AT-02, AT-30 | Approved mapping and fixtures for no-dimension, NULL, empty string, new dimensions, and ad hoc results. |
| DL-18 / content | S01/S18 pp.9-12; S06 permissive decision_card/causes/extra-field structure. | Required chart, card and state content has no complete prescribed internal/wire schema. | Use an internal validated content contract or a compatible documented extension. Schema permissiveness does not make required content optional. | Product; ADR-09, ADR-17; AT-26, AT-30 | Reviewed field mapping and full-content validation evidence. |
| DL-19 / configuration | S01/S18 p.13; S02 extensible KPI rule; S17 managerConfig/ManagerGovernance. | Approval roles, write authority, candidate activation and rollback policy. | Version inactive candidates and require authorized approval/validation, or defer activation while preserving the requirement. Do not infer write authority from read scope. | Product/security/data; ADR-01, ADR-06, ADR-08; AT-27, AT-29 | Approved lifecycle/authority and tests for rejected/approved candidates without canonical edits. |

''' + t[pos:]
# New rows must stay in the same table: remove the single blank before DL-17.
t = t.replace('|\n\n| DL-17 / output', '|\n| DL-17 / output')
t = t.replace('Threshold equality, sparse baseline, zero denominator, unknown days, and reset.', 'Threshold equality, R4 comparison reference, R3 missing warn, sparse baseline, zero denominator, unknown days, and reset.')
t = t.replace('The three architecture documents are reconciled with the supplied review record.', 'The four numbered architecture documents are subject to the current source-driven audit. Read the detailed findings and traceability evidence before treating documentation coverage as complete.')
t = t.replace('A saved pre-edit file baseline is used for the [unified diff](reconciliation.diff).', 'The [reproducible pre-edit backup](audit-2026-11-09/pre-edit.zip) and [baseline manifest](audit-2026-11-09/pre-edit-manifest.json) support the [current unified diff](audit-2026-11-09/reconciliation.diff). The root reconciliation.diff is historical.')
write(doc, t)
print('Phase 3 complete: document 003 corrected; AUD-029 through AUD-042 recorded.')
