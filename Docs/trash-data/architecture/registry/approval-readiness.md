# Architecture Registry approval readiness

State: **Draft / Pending Review**. Task: `ARCH-REG-003`. Date: 2026-11-09. Time zone: `Asia/Tehran`.

The Registry can support a team review of the source extraction. It is **not ready for unconditional use as an implementation dependency graph**. A later source-preserving document migration can proceed only after the team accepts the limits below and separately authorizes that work. No migration is done in this task.

## Review package

Use the [review queue](traceability-review-queue.csv). It has 109 review batches: 108 batches cover every existing inferred edge; one batch lists two missing-link candidates. The 180 source-specific classification groups remain available in the [2,470-row membership file](triage-ARCH-REG-003/relationship-classification.csv). A batch is a review work unit, not a single decision or approval. Source and target sets are descriptive; exact pairs are in the membership file. Do not take their cross-product. The queue display class `Proposed / Inferred Relationship` refers to the unchanged matrix value `Proposed Relationship`.

| Triage result | Existing relationships | Queue batches |
|---|---:|---:|
| P0 | 1,830 | 75, including the missing-link batch |
| P1 | 620 | 30 |
| P2 | 20 | 4 |
| Questionable existing mappings | 274 | 47 |
| Missing-link candidates | Excluded from the 2,470 count | 1 batch, 2 pairs |

The 274 questionable mappings have 186 P0, 78 P1 and 10 P2 edges. The other 2,186 defensible candidates and 10 navigation references still need confirmation. **No inferred edge is promoted or deleted.** P0 is the priority of a possible wrong interpretation. It is not a claim that 1,830 links are wrong. It is not a risk severity score.

Start with the cases below. Review the remaining defensible batches after the high-impact interpretation rules are recorded.

| First review case | What was checked | Team review action |
|---|---|---|
| All 55 KPI-to-orders-policy links | Original SQL, five reference views, the documented selected-value sources and the earlier RAW/DEDUP report. | Review 8 historically changed definitions, 14 other definitions with an orders value path, 1 shared-view-only case and 32 definitions with no inspected orders relation separately. Do not select RAW/DEDUP. |
| Manager-input test template | All 23 inputs; exact named AT lists for all 7 non-question events. | Review 20 unnamed extra test mappings. Consider the two missing pairs: `REQ-INPUT-IN05 -> AT-15` and `REQ-INPUT-IN07 -> AT-03`. Add no criterion or edge automatically. |
| Manager-input component template | The same five components are assigned to every input: 115 mappings. | Separate receipt, context read, authorized write, draft and later display. Review 40 questionable configuration/decision associations before using them for authority or execution planning. |
| Stage SLA versus KPI/Signal policy | All 12 stage rows; WF1 deadline/missing SLA; original WF2 and WF3 KPI SQL. | Review 12 stage-to-ADR-07 links and the logical `workflows` assignments. Stage SLA is not automatically a KPI threshold or a new Signal. M01 is end-to-end owner, not proof of stage team ownership. |
| Partial risk-control tests | All 38 risk-to-AT candidates against the risk control and AT criterion. | In particular, AT-23 does not prove source closure; AT-13 alone does not prove cache/RLS isolation; AT-10 alone does not specify small-group privacy checks. Keep uncovered facets visible. |
| Reference-view and event templates | Complete reference-view text and event/calendar source roles. | Three non-orders views are still linked to ADR-02. Planned events are not canonical KPI inputs or observed causes. Keep value, declared relation and context claims separate. |
| Narrative Requirement-to-ADR templates | Source families and target ADR scope. | Require an exact paragraph that addresses the requirement. Shared vocabulary or an old audit assignment is insufficient. |
| Output and access mappings | Schema property locations, the 11-manager access matrix and fixed access boundaries. | Do not make optional wire fields mandatory, invent status mapping, expose individual leave or turn read scope into write authority. |

Each exact relationship has its own reason, evidence, effect, route and action in the membership file. Absence from a named fixture list flags uncertain coverage; it does not prove that a cross-cutting negative test is useless. The team can retain such a link with a bounded rationale. No general test obligation is invented here.

## Confirmed architectural boundaries

The five Accepted boundaries remain fixed: one bounded AI Agent; PostgreSQL as the only product database engine; independent publication of valid manager reports; deterministic KPI calculation, Signal detection, authorization and final validation; human-controlled organizational decisions and actions.

Approval evidence remains [S19](../audit-2026-11-09/request.txt), section 1, and [003 section 1](README.md#decisions-1), with the relevant S16 review results. The 33 inferred boundary-to-ADR/AT/component links are trace candidates. They neither reopen those boundaries nor prove their implementation. Original approver names and dates remain absent.

Current S01 identification is already confirmed in ARCH-REG-002. [REG-ISS-010](open-issues-registry.md#reg-iss-010) concerns historical content-comparison evidence. It does not reopen the identity of the current official PDF or prove a changed requirement.

## Open choices that block affected implementation

These are existing Open facets, not new choices. A blocker applies to affected work; it need not stop independent source-preservation or documentation work. A source-preserving extraction can be approved while these choices remain Open.

- **DL-01/02/03/05:** translation/type policy and all-55 proof plan; accepted RAW/DEDUP input; source closure and release of uncertain values; valid conflict precedence or approved quarantine. PostgreSQL itself is already Accepted.
- **DL-06/07/10:** exact shared-source projections and redaction; capacity measure/privacy rules; historical scope, M11 precedence, receipt/readiness and known-at. The supplied hierarchy and direct-supervisor rule are already requirements.
- **DL-08/09:** stage responsibility/routing and unresolved Signal edge cases. Fixed R1-R8 conditions remain fixed. Stage calculation records and DQ eligibility records also need reviewed mappings in REG-ISS-003/004.
- **DL-11/17/18/19:** suppressed/ongoing, NULL/no-dimension and added-number serialization; complete Insight/content/history projection; existing-KPI editing versus the fixed 55 reference definitions; write approval, effect time and rollback.
- **DL-12/13/14/15:** MVP execution-confirmation scope; retry/timeout/fallback/failure export; model/provider/internal bounds and reservations; retention, audit access and recovery policy. Human action control and independent valid publication are already fixed.
- **REG-ISS-001/002/009:** P2/P3 Workflow milestone scope, QA context record and exact upload/retrieval contract. Do not select an alternative to make a diagram or queue look complete.

See the [Open issue records](open-issues-registry.md). All 29 remain Open. The [coverage file](triage-ARCH-REG-003/high-impact-coverage.csv) includes every ADR, issue, AT and risk, even records with no inferred edge. No missing edge is invented to eliminate an orphan.

## Organizer/source clarification

The unconditional routes from ARCH-REG-002 remain DL-02, DL-03, DL-05, DL-09, DL-10, DL-11, DL-16 and DL-17. Ask only the applicable source question: accepted orders policy; closure/release contract; equal-rank precedence; score-sensitive rule interpretation; activation/receipt precedence; official wire mapping; final evaluator profile/hardware/raw dictionary; ambiguous number/dimension representation.

DL-06 has a conditional route for unresolved manager-Q08 source meaning. DL-07 has a conditional route if an hours measure is chosen without a working-hours contract. Existing access rules need no reselection. Model/provider/gateway/internal allocation choices remain team work. Historical S01 comparison now needs evidence, not another organizer choice about current source identity.

These routes are copied from existing source questions. No message was sent and no person was appointed. The engineering-first review of a suspect link must not create an organizer dependency merely because the old template mentions a source policy.

## Engineering validation tasks

These are existing planned gates or proposed evidence checks for trace review. They are not work executed in this task and are not new acceptance requirements.

1. Attach exact source paragraphs, fields, test clauses and roles to each retained trace link. For a group confirmation, state its precise applicability and exclusions.
2. For all 55 KPIs, separate documented value sources, declared query/view relations and physical plan reads. Validate accepted-policy results, SQL types, whole row sets, NULL, rounding and replay under AT-02/03/05. A textual relation inventory is not that proof.
3. Compare each manager event with its receipt clock, role, write authority and expected result. Use AT-03/06/07/13/14/15/16/22/29/30 only where their actual criteria apply. Keep read context distinct from mutation and organizational execution.
4. Check all 12 Workflow stage populations, deadline/no-SLA behavior and query evidence under AT-12/25. Preserve canonical WF2 48h and the exact WF3 formula. Stage owner decisions remain Open.
5. Map each risk control to named positive and negative cases in existing ATs. Record partial coverage. An AT label or future pass cannot prove an entire control.
6. Preserve schema, numerical, evidence, authorization and role-content checks separately under AT-06/10/11/24/26/30. Preserve the three-level content matrix and all R1-R8 conditions.
7. Later measure bounded failure, runtime, cost, replay and restore with actual product receipts under the existing gates. Exact limits and source answers must be approved where Open. Do not mark any AT Passed now.

## Semantic coverage and evidence limits

All 2,470 inferred edges receive a deterministic primary classification, exact queue membership, semantic distinction, route and priority. The analysis partitions them into 180 source-specific groups and batches defensible work into a smaller queue. All 55 SQL strings and five view definitions are inspected for declared named relations; documented selected-value source sets are retained separately. The earlier eight-KPI RAW/DEDUP result is attributed historical evidence, not a new run.

Direct checks include five Accepted source confirmations, 55 KPI metadata/SQL records, five view texts, all 23 manager inputs, the 7 per-input test lists, 11 access rows, all 12 stages, all 38 risk-to-AT candidates and the exact existing AT rows used in those comparisons. The [risk-control coverage notes](triage-ARCH-REG-003/risk-control-coverage.csv) state each test's covered facet and remaining limits. Component-role checks are bounded source/model responsibility checks, not a proof of execution order. The 33 Accepted-boundary links stay inferred.

No SQL was executed, no query plan was measured, no product fixture was run, and no model/DSL layout was changed. No exhaustive human semantic verification is claimed. Text scanning does not prove minimal invalidation, physical execution, source closure, independent causal evidence, numerical equivalence, access enforcement or a test result. All existing acceptance execution states and risk severities remain unchanged.

Interpret each reference carefully: **value-policy applicability** is not **declared query/view relation membership**; neither proves a physical execution dependency. A **logical responsibility** is not a new service, grant or deployment. A **navigation inverse** is not a prerequisite. **Topic similarity** requires source-specific review before it can become a substantive trace claim.

## Proposed minimum approval conditions

The following conditions are proposals for team review. This document records no approval.

1. Approve the Registry as a faithful, versioned **source extraction**, with stable IDs, source locations, retained exact extracts and clearly stated limits. Do not approve unreviewed architecture choices by approving this extraction.
2. Confirm the five Accepted boundaries and keep all other statuses and source/approval distinctions intact.
3. Accept the complete inferred-edge inventory and record a rule that all 274 questionable mappings and 2 missing candidates are excluded from normative implementation/dependency claims until reviewed. The 2,186 defensible candidates also remain inferred until a bounded confirmation is recorded.
4. Assign review responsibility through a real team record. Do not infer write authority or an appointed owner from a source role, KPI owner or queue route.
5. Before using the Registry as an operational architecture reference, resolve or explicitly exclude P0 trace interpretations that could change canonical calculation, access, human action, fixed boundaries or acceptance conditions. Record exact exclusions; no hidden default business rule is permitted.
6. Preserve Open source questions and unexecuted ATs as tracked limitations. Product test success is **not** a prerequisite for approval of a faithful documentation extraction. Product acceptance and approval of proposed mechanisms need their own decisions and evidence.
7. For a later structural migration, separately authorize the exact file/link plan, preserve original meaning and all IDs/criteria/sources, validate anchors, and keep a reversible before/after record. Until that authorization, retain 001-004 and their source sections in place.

## Items that can remain Pending during later restructuring

Navigation inverses, delivery-document component hints, orphan inventory/phase records, optional model detail and historical Git/tooling maintenance can remain Pending if clearly labeled and excluded from runtime planning. REG-ISS-005 output-count evidence and REG-ISS-010 historical PDF comparison can remain pending without inventing KPI targets or claiming historical equivalence. Product measurements and planned AT execution can also remain pending during source-preserving document work.

Open business/source choices can be carried unchanged into a later layout. Restructuring must not choose RAW/DEDUP, change M11 timing, map suppressed to ongoing, appoint stage teams, rewrite the 55 reference definitions or imply that an unexecuted test passed. Moving those Open records is documentation work; silently resolving them is not.

Readiness recommendation: **ready for a bounded team review of extraction and a proposed source-preserving migration plan; not approved for migration, not ready for unqualified operational/dependency use, and not product acceptance.** A full authoritative replacement of 003 should wait for recorded team approval of authority, exclusions, ownership and the migration plan.

## Preservation and validation

Only the two requested deliverables and supporting files in `triage-ARCH-REG-003/` are new. All task-start files, including the matrix, sources 001-004, Dataset, SQL, DSL and prior audits, must remain byte-identical. The S01 metadata changes in 001/004 visible against the baseline belong to ARCH-REG-002; this task adds no tracked changes. No issue is closed. No relationship is deleted or promoted. No commit or push is performed.

See [validation results](triage-ARCH-REG-003/validation-results.json), [classification counts](triage-ARCH-REG-003/summary.json), [initial hashes](triage-ARCH-REG-003/before-manifest.json) and [file comparison](triage-ARCH-REG-003/file-comparison.csv). The checks prove coverage and preservation within their stated scope, not team approval.
