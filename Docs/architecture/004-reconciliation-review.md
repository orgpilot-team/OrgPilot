# ARKA architecture reconciliation

Document key: `004-reconciliation-review`. Shared architecture family: `ARCH-001`.

Review date: 2026-11-09. Time zone: `Asia/Tehran`.

This review reconciles the four numbered architecture documents and dependent documentation with the official brief, dataset contracts, and the supplied Q01-Q17 review record. It changes documentation only. It does not claim product implementation, numerical equivalence, security, performance, or acceptance results.

The Accepted baseline has one bounded AI Agent with deterministic supporting modules, PostgreSQL-only product execution, independent publication of valid manager reports, deterministic KPI/signal/authorization/final-validation boundaries, and human-controlled organizational decisions. The user confirms these boundaries in the current audit request (S19). The previous embedded SQLite product calculator is superseded. SQLite remains permissible as an isolated reference test oracle. It is outside the product execution path.

## Sources and authority

Read the [source register](001-system-blueprint.md#system-2) for S01-S19. The official brief and dataset contracts define requirements. A team decision selects an architecture within those requirements. A Codex proposal alone does not establish approval.

The user identified `C:/Users/ashkriz/Desktop/Adr.md` as the requested review file. An [unchanged source copy](sources/Adr.md) is retained in this documentation set. Its question text and final result table were both checked. The original decision approvers and approval dates are not supplied. This review does not invent them.

The [existing Structurizr model](../../architecture/structurizr/workspace.dsl) supports these target boundaries. Its authority notes and relevant component contracts were checked. It is an existing target model, not proof of implementation. It was not changed.

| Source | SHA-256 at this review |
|---|---|
| S16 review record and exact source copy | `0c7cea554016930366100cb1138ada6ace7f05e918e274ee24f0a89e465639df` |
| S01 current brief PDF | `6d68d3fcc285f6908af0d97c0429dfefb489f00b7f6538ed03573552ed6955f8` |

S01 was highlighted and resaved. S18 is its Markdown conversion. The current PDF content on pages 8, 10, and 15 was checked visually against the corresponding text. These checks confirm the recurrence controls, required report content, and suppressed-status wording. Pages 13 and 16 were also checked in the earlier review of the same current PDF. No changed requirement was established from the former hash difference. Earlier numerical audits remain attributed historical evidence.

Use exactly four decision statuses:

- `Requirement`: an explicit brief or dataset contract rule.
- `Accepted`: a recorded team decision.
- `Proposed`: a design choice without approval evidence.
- `Open`: an unresolved choice or source conflict.

`Observation` is verified source or audit evidence. It is not an approval status.

A question can contain more than one status. For example, Q03 has an Accepted engine choice and an Open equivalence gate. Do not give the whole question one status that hides this distinction. The review source's count of explicit, partial, and absent brief answers is a source summary. It is not an approval count.

<a id="question-map"></a>

## Q01-Q17 mapping

These IDs refer only to the architecture review in S16. [Manager questions Q01-Q16](003-decisions-and-roadmap.md#manager-question-map) belong to S07. Diagram review questions use the `VQ` prefix in [their register](visualizations/open-questions.md).

All acceptance gates below are planned. They were not executed in this documentation task.

| Review question | Requirement and decision status | ADRs | Document sections | Acceptance gates and open log |
|---|---|---|---|---|
| <a id="review-q01"></a>Q01: Agent topology | `Accepted`: one bounded AI Agent plus deterministic modules; S16 Q01 result table explicitly records a team decision. `Open`: execution limits. | [ADR-13](003-decisions-and-roadmap.md#adr-13), [ADR-10](003-decisions-and-roadmap.md#adr-10) | [001: system](001-system-blueprint.md#system-1), [modules](001-system-blueprint.md#system-4) | [AT-20](003-decisions-and-roadmap.md#at-20), AT-17/18; DL-14; AT-28 |
| <a id="review-q02"></a>Q02: files and intake | `Requirement`: structured sources, manager input, and uploads; S01 pp.3,12-14 and S02/S07. `Proposed`: separate document registration and structured intake. `Open`: exact formats, including Excel, and retrieval. | [ADR-16](003-decisions-and-roadmap.md#adr-16), ADR-08 | [001: modules](001-system-blueprint.md#system-4), [002: ingestion](002-data-architecture.md#data-4) | [AT-22](003-decisions-and-roadmap.md#at-22), AT-03/13; DL-10; AT-29 |
| <a id="review-q03"></a>Q03: 55 KPIs in PostgreSQL | `Accepted`: PostgreSQL only; S16 Q03 body/result and S17. `Requirement`: canonical results unchanged; S02-S04 and S01 p.16. `Proposed`: versioned translations. `Open`: proof for all 55 definitions. | [ADR-01](003-decisions-and-roadmap.md#adr-01) | [002: calculation](002-data-architecture.md#data-6), [engine boundary](002-data-architecture.md#data-10) | [AT-02](003-decisions-and-roadmap.md#at-02), AT-03/05/17; DL-01; AT-27 |
| <a id="review-q04"></a>Q04: natural-language queries | `Requirement`: read-only, registered SQL with data-layer row controls; S01 pp.9,13. `Proposed`: predefined tools first, then validated custom SQL. `Open`: exact allowlists and limits. Free SQL is incompatible with the required boundary. | [ADR-06](003-decisions-and-roadmap.md#adr-06), ADR-10 | [001: security](001-system-blueprint.md#system-10), [002: query path](002-data-architecture.md#data-10) | [AT-06](003-decisions-and-roadmap.md#at-06), AT-10/16/20; DL-06/14; AT-28 |
| <a id="review-q05"></a>Q05: duplicate orders | `Requirement`: report duplicates as data issues; preserve original dataset and SQL. `Open`: accepted RAW/DEDUP calculation policy. S16's two-mode comparison is Proposed, not organizer approval. | [ADR-02](003-decisions-and-roadmap.md#adr-02) | [002: ingestion](002-data-architecture.md#data-4), [calculation](002-data-architecture.md#data-6) | AT-02, [AT-05](003-decisions-and-roadmap.md#at-05); DL-02 |
| <a id="review-q06"></a>Q06: incomplete data | `Requirement`: continue reports, identify missing sources, and use null for unavailable current values; S01 pp.13-14,17 and S02. S16 summary/S17 retain dated last-valid context. `Open`: release conditions, age, closure, and wire mapping. | [ADR-04](003-decisions-and-roadmap.md#adr-04) | [002: quality](002-data-architecture.md#data-5), [001: output](001-system-blueprint.md#system-9) | [AT-04](003-decisions-and-roadmap.md#at-04), [AT-23](003-decisions-and-roadmap.md#at-23); DL-03 |
| <a id="review-q07"></a>Q07: historical correction | `Requirement`: cutoff eligibility and canonical results; S02-S04. Preserve the existing versioned snapshot/report design. `Proposed`: full rebuild as the correctness baseline. `Open`: selective calculation and restatement notices. | [ADR-03](003-decisions-and-roadmap.md#adr-03), [ADR-05](003-decisions-and-roadmap.md#adr-05) | [002: time](002-data-architecture.md#data-3), [recalculation](002-data-architecture.md#data-7), [lineage](002-data-architecture.md#data-8) | AT-02/03/05; DL-04 |
| <a id="review-q08"></a>Q08: conflicting records | `Requirement`: preserve source facts and report data issues. `Proposed`: conflict state and quarantine. `Open`: a valid precedence rule. No last-row-wins rule is supplied. | [ADR-11](003-decisions-and-roadmap.md#adr-11) | [002: time](002-data-architecture.md#data-3), [ingestion](002-data-architecture.md#data-4) | AT-05; DL-05 |
| <a id="review-q09"></a>Q09: access | `Requirement`: supplied hierarchy, row controls for every query, individual workload data only for a direct supervisor; S01 pp.5,10,13 and S05. `Proposed`: policy catalog. `Open`: shared-source predicates and columns. | [ADR-06](003-decisions-and-roadmap.md#adr-06) | [001: security](001-system-blueprint.md#system-10), [002: organization](002-data-architecture.md#data-9) | AT-06/07/13; DL-06; AT-30 |
| <a id="review-q10"></a>Q10: capacity and personal data | `Requirement`: aggregate team capacity, no individual attendance monitoring; S01 pp.6,9,12-13. `Proposed`: a headcount measure. `Open`: formula, hours contract, small-group inference, and text redaction. | [ADR-06](003-decisions-and-roadmap.md#adr-06) | [001: analysis](001-system-blueprint.md#system-8), [002: organization](002-data-architecture.md#data-9) | AT-06/10; DL-07 |
| <a id="review-q11"></a>Q11: three workflows | `Requirement`: actual event reconstruction, stage SLA, and supplied M01 workflow ownership; S01 pp.5-6,16 and S11. `Proposed`: stage catalog. `Open`: stage owners and routing. | [ADR-15](003-decisions-and-roadmap.md#adr-15), ADR-07 | [001: workflows](001-system-blueprint.md#system-7), [002: entities](002-data-architecture.md#data-2) | [AT-12](003-decisions-and-roadmap.md#at-12), AT-08; DL-08; AT-25 |
| <a id="review-q12"></a>Q12: signals and escalation | `Requirement`: deterministic detection and R1-R8; S01 pp.6-8,13 and S11. `Proposed`: strict crossing and named unknown states. `Open`: equality, baseline, zero denominator, warning-day count, and reset. | [ADR-07](003-decisions-and-roadmap.md#adr-07) | [001: signals](001-system-blueprint.md#system-7), [002: quality](002-data-architecture.md#data-5) | [AT-08](003-decisions-and-roadmap.md#at-08), AT-09; DL-09; AT-24 |
| <a id="review-q13"></a>Q13: organization and receipt time | `Requirement`: Tehran time, cutoff, next-report input effect, dynamic structure; S01 p.14, S02/S05/S07. `Open`: M11 morning 75/76, historic scope, same-day receipt, calendar known-at. Morning 76 in S16 is Proposed. | [ADR-08](003-decisions-and-roadmap.md#adr-08), ADR-16 | [001: replay](001-system-blueprint.md#system-5), [002: time](002-data-architecture.md#data-3), [organization](002-data-architecture.md#data-9) | AT-03/07/15/22; DL-10; AT-29 |
| <a id="review-q14"></a>Q14: role reports and shared analysis | `Requirement`: one Insight Brief as report source and role-specific access; S01 pp.9-10. `Open`: internal schema and suppressed/ongoing mapping. Shared evidence is never a new grant. | [ADR-09](003-decisions-and-roadmap.md#adr-09), ADR-06 | [001: analysis](001-system-blueprint.md#system-8), [output](001-system-blueprint.md#system-9), [002: report versions](002-data-architecture.md#data-8) | AT-06/10/11; DL-11; AT-26, AT-30 |
| <a id="review-q15"></a>Q15: decisions and action | `Requirement`: human decision, drafts only, no automatic execution; S01 pp.11-12 and S02. `Proposed`: separate decision, draft, and execution-confirmation states. `Open`: actual execution tracking in MVP. | [ADR-17](003-decisions-and-roadmap.md#adr-17) | [001: modules](001-system-blueprint.md#system-4), [analysis](001-system-blueprint.md#system-8), [002: report history](002-data-architecture.md#data-8) | [AT-14](003-decisions-and-roadmap.md#at-14); DL-12; AT-29 |
| <a id="review-q16"></a>Q16: LLM failure | `Accepted`: independent valid-report publication and failed-report records; S16 Q16 result table and S17. `Requirement`: every active manager still needs a valid report. `Proposed`: template fallback. `Open`: retry, timeout, status export, replacement rules. | [ADR-14](003-decisions-and-roadmap.md#adr-14), ADR-10 | [001: replay](001-system-blueprint.md#system-5), [output](001-system-blueprint.md#system-9), [002: operations](002-data-architecture.md#data-11) | [AT-21](003-decisions-and-roadmap.md#at-21), AT-11/15/18; DL-13; AT-28 |
| <a id="review-q17"></a>Q17: models and limits | `Requirement`: USD 5 per whole day, 15 minutes, and report deadline; S01 pp.14,16,19. `Proposed`: provider-neutral gateway, reservations, tool/token limits, tracing, and QA share. `Open`: model, provider, products, prices, and exact limits. | [ADR-10](003-decisions-and-roadmap.md#adr-10), ADR-13 | [001: analysis](001-system-blueprint.md#system-8), [003: measurement](003-decisions-and-roadmap.md#decisions-8) | [AT-17](003-decisions-and-roadmap.md#at-17), [AT-18](003-decisions-and-roadmap.md#at-18), AT-20; DL-14/16; AT-28 |

## Important conflicts and disposition

The [Decision Log](003-decisions-and-roadmap.md#decision-log) retains options, effects, owners, and gates. No Open row is silently closed by this review.

| Conflict | Disposition |
|---|---|
| Old dual-engine proposal versus recorded PostgreSQL-only decision | Resolved by explicit S16 Q03 decision, confirmed by S17. Update product and interactive paths. Keep original SQL and an isolated test oracle. Numerical proof remains Open. |
| Unqualified Proposed/Open banner versus recorded team decisions | Resolved by statement-level statuses. Add ADR-13 and ADR-14. Preserve unapproved design details as Proposed. |
| Daily atomic wording versus independent publication | Accepted: manager outcomes are independent. Proposed: commit one manager's text/JSON together at a package boundary. Incomplete required coverage cannot pass the day. Retry and fallback remain Open. |
| Q06 prior value versus current null contract | Preserve a historical display with the actual date. Never reuse that value as current. Exact wire mapping, eligibility, and age remain DL-03. |
| Q13 provisional morning 76 versus conflicting static metadata | Keep both scenarios. Neither the Codex proposal nor a calculated report count approves precedence. DL-10 remains Open. |
| Generic precision examples versus KPI-specific SQL | Use canonical definition and rounding. Registered ad hoc queries are permitted. Added-number wire representation remains Open. |
| Brief suppressed versus schema ongoing | Preserve both sources and suppression history. Do not change the dataset schema or invent a mapping. DL-11 remains Open. |
| Shared Insight versus recipient access | Reuse the analytical source with authorized projections. Restricted evidence and its derived claims cannot leak through shared prompts or cache. The internal schema remains Open. |

## Decisions needed before implementation

This audit corrects the documented omissions found through source comparison. The [audit report](audit-2026-11-09/audit-report.md) and [unit review ledger](audit-2026-11-09/document-review-ledger.csv) state its evidence and limits. Open decisions and unexecuted product gates remain visible. Product implementation is outside this task. The team must resolve or explicitly approve named temporary policies for these P0 design choices before affected work starts:

1. Q03: translation/type contract and the all-55 equivalence plan. Proof is an implementation acceptance gate, not a result available now.
2. Q05/Q06/Q08: calculation input mode, invalid-data publication, dated prior-value mapping, and conflict handling. Organizer answers are needed where the source contract is incomplete.
3. Q04/Q09/Q10: shared-source row/column grants, privacy rules, capacity definition, and custom-query limits.
4. Q11/Q12/Q13: stage owners, signal edge rules, and time precedence for organization changes and attachments.
5. Q14/Q16/Q17: output-status contract, shared Insight representation, failure/status policy, and bounded model execution.

Retention and execution-confirmation details remain in DL-12/DL-15. Final hardware, hidden labels, and organizer limits block final acceptance, not independent documentation or authorized source-preservation work. The Accepted architecture boundaries do not need to be selected again.

## Current audit outputs and file changes

- [Detailed audit report](audit-2026-11-09/audit-report.md): issue IDs, exact pre-edit locations, original claims, evidence, severity, correction status, and remaining uncertainty.
- [Requirement Traceability Matrix](audit-2026-11-09/requirements-traceability.csv): source -> granular requirement -> existing component -> contract/rule -> ADR -> planned acceptance gate.
- [KPI contracts](audit-2026-11-09/kpi-contracts.csv), [Workflow contracts](audit-2026-11-09/workflow-contracts.csv), and [manager-input contracts](audit-2026-11-09/manager-input-contracts.csv): detailed source semantics.
- [Structurizr gap report](audit-2026-11-09/structurizr-gap-report.md): actual elements, relationships, view keys, and proposed later changes. The DSL is unchanged.
- [Change and verification report](audit-2026-11-09/change-report.md): per-file changes, checks, scope limits, and remaining blockers.
- [Current unified diff](audit-2026-11-09/reconciliation.diff), [pre-edit backup](audit-2026-11-09/pre-edit.zip), and [baseline manifest](audit-2026-11-09/pre-edit-manifest.json).

The root `reconciliation.diff` belongs to the previous reconciliation and is retained unchanged. Use the current audit diff above for this task. The source record `sources/Adr.md` is unchanged. No original brief, dataset, SQL, source contract, review report, or Structurizr file was edited.

<a id="verification"></a>

## Verification record

The prior reconciliation used link/count checks. Those results are historical and do not prove semantic correctness of the current baseline. This audit compares source meaning, rule behavior, all canonical metadata, Workflow stages, manager inputs, JSON contracts, and the existing target model. The [current verification result](audit-2026-11-09/verification.json) reports only documentation/source checks that were executed.

All AT gates remain planned. No KPI SQL, PostgreSQL equivalence, product security, replay, model, performance, restore, or cost test was run. No dependency was installed. No architecture diagram renderer was run. Existing Structurizr view keys were checked in the DSL text; no view was invented or rendered.

Git is unavailable in this workspace. The audit uses a verified pre-edit ZIP and source/file hash manifest. No commit or push was attempted. Open decisions, rather than invented answers, remain in the [Decision Log](003-decisions-and-roadmap.md#decision-log).
