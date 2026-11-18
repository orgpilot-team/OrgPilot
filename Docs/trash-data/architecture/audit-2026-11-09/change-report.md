# File change report

The audit corrects the documentation and preserves the five accepted architecture boundaries. It does not implement the product. It records 58 material findings: 56 document corrections and two deferred model comment changes. One further record confirms source counts that were already correct.

No Git repository exists at the project root or in its parent directories. `git status --short` returned that error. The comparison therefore uses the verified [pre-edit ZIP](pre-edit.zip) and [baseline manifest](pre-edit-manifest.json). No commit or push was attempted.

## Changed existing files

All 34 changed existing files are Markdown under `docs/architecture/`. No original file was deleted. Original content is available in the backup. The 26 preview files now contain short retirement notices. This removes active Mermaid architecture references while preserving the original raw diagrams and generators for history.

| Existing file | Change |
|---|---|
| [001-system-blueprint.md](../001-system-blueprint.md) | Complete R1-R8 and Workflow contracts; report content; source authority; parent execution and input contracts; Proposed mechanisms; Structurizr references. |
| [002-data-architecture.md](../002-data-architecture.md) | Source grains and clocks; exact reference-view semantics; Proposed internal entities; privacy, priority, and output mapping; preserve the KPI catalog. |
| [Current governance records; former combined source](../registry/README.md#source-context) | Preserve ADR-01 through ADR-17; add AT-24 through AT-30; keep every gate planned; expand the Decision Log to 19 source-backed Open rows. |
| [004-reconciliation-review.md](../004-reconciliation-review.md) | Keep the Q01-Q17 mapping and stable anchors; reconcile evidence status, gates, independent publication, and current audit links. |
| [visualizations/README.md](../visualizations/README.md) | Use the 16 actual Structurizr view keys; state missing views; retire legacy preview navigation. |
| [visualizations/open-questions.md](../visualizations/open-questions.md) | Preserve VQ identifiers and unresolved policy; align status and Decision Log references. |
| [visualizations/previews/01-source-calendar-history-detail.md](../visualizations/previews/01-source-calendar-history-detail.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/01-source-configuration-detail.md](../visualizations/previews/01-source-configuration-detail.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/01-source-crm-detail.md](../visualizations/previews/01-source-crm-detail.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/01-source-data-erd.md](../visualizations/previews/01-source-data-erd.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/01-source-marketing-detail.md](../visualizations/previews/01-source-marketing-detail.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/01-source-orders-detail.md](../visualizations/previews/01-source-orders-detail.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/01-source-organization-detail.md](../visualizations/previews/01-source-organization-detail.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/01-source-support-detail.md](../visualizations/previews/01-source-support-detail.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/01-source-workload-detail.md](../visualizations/previews/01-source-workload-detail.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/02-proposed-database-erd.md](../visualizations/previews/02-proposed-database-erd.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/02-proposed-layers.md](../visualizations/previews/02-proposed-layers.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/03-organization-hierarchy.md](../visualizations/previews/03-organization-hierarchy.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/04-management-access-graph.md](../visualizations/previews/04-management-access-graph.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/05-column-access-overview.md](../visualizations/previews/05-column-access-overview.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/06-kpi-data-lineage.md](../visualizations/previews/06-kpi-data-lineage.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/06-lineage-ORG.md](../visualizations/previews/06-lineage-ORG.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/06-lineage-T_CMP.md](../visualizations/previews/06-lineage-T_CMP.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/06-lineage-T_DIG.md](../visualizations/previews/06-lineage-T_DIG.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/06-lineage-T_ENT.md](../visualizations/previews/06-lineage-T_ENT.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/06-lineage-T_MKT.md](../visualizations/previews/06-lineage-T_MKT.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/06-lineage-T_RSP.md](../visualizations/previews/06-lineage-T_RSP.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/06-lineage-T_SHP.md](../visualizations/previews/06-lineage-T_SHP.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/06-lineage-T_WH.md](../visualizations/previews/06-lineage-T_WH.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/06-lineage-U_OPS.md](../visualizations/previews/06-lineage-U_OPS.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/06-lineage-U_SAL.md](../visualizations/previews/06-lineage-U_SAL.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/previews/06-lineage-U_SUP.md](../visualizations/previews/06-lineage-U_SUP.md) | Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview. |
| [visualizations/proposed-entity-contracts.md](../visualizations/proposed-entity-contracts.md) | Align Proposed entity contracts with document 002; do not claim an existing ERD. |
| [visualizations/security-examples.md](../visualizations/security-examples.md) | Keep useful examples; state evidence and approval limits. |

## Added audit files

Each file below belongs to this audit folder. The Python files support documentation checks and authoring. They do not implement product behavior. Do not rerun authoring phases over the corrected documents. Use the check command in [README](README.md).

| Added file | Purpose |
|---|---|
| [README.md](README.md) | Audit index, evidence limits, and check command. |
| [acceptance-basis.csv](acceptance-basis.csv) | Requirement or decision basis for all 30 planned gates. |
| [audit-report.md](audit-report.md) | Full issue records, source evidence, corrections, and limits. |
| [audit-summary.json](audit-summary.json) | Finding counts and document review unit counts. |
| [audit_support.py](audit_support.py) | Documentation authoring helpers and duplicate-finding guards. |
| [brief-content-check.json](brief-content-check.json) | PDF content checks; a resaved hash does not imply changed requirements. |
| [build_audit_report.py](build_audit_report.py) | Build findings tables, detailed report, and review-unit ledger. |
| [build_traceability.py](build_traceability.py) | Build source contracts and the traceability matrix. |
| [change-report.md](change-report.md) | File-by-file changes, checks, and implementation blockers. |
| [cross_document_fixes.py](cross_document_fixes.py) | Cross-document contract and reference corrections. |
| [diff-summary.json](diff-summary.json) | Diff scope, line counts, exclusions, and SHA-256. |
| [document-review-ledger.csv](document-review-ledger.csv) | All 911 pre-edit review units, source context, and dispositions. |
| [file-changes.csv](file-changes.csv) | Complete file index with change kind, purpose, and line counts. |
| [finalize_audit.py](finalize_audit.py) | Build this report and the backup-based diff; does not restore files. |
| [findings.csv](findings.csv) | Full findings in table form; original claims and pre-edit locations. |
| [findings.json](findings.json) | Structured findings; includes the retained source observation. |
| [kpi-contracts.csv](kpi-contracts.csv) | All 55 source definitions, SQL hashes, and calculation semantics. |
| [manager-input-contracts.csv](manager-input-contracts.csv) | All 23 supplied inputs, effects, timing, and access limits. |
| [model_audit.py](model_audit.py) | Read-only model inventory and proposed gap report. |
| [output-schema-contracts.csv](output-schema-contracts.csv) | Exact property constraints and status enums from both schemas. |
| [phase1.py](phase1.py) | Source-backed changes to document 001. |
| [phase2.py](phase2.py) | Source-backed changes to document 002. |
| [phase3.py](phase3.py) | Source-backed changes to document 003. |
| [phase4.py](phase4.py) | Source-backed changes to document 004 and dependent documentation. |
| [pre-edit-manifest.json](pre-edit-manifest.json) | SHA-256 baseline for all 1,452 initial workspace files. |
| [pre-edit.zip](pre-edit.zip) | Verified backup of all 79 pre-existing architecture and model files. |
| [reconciliation.diff](reconciliation.diff) | Current unified text diff and binary backup notice. |
| [request.txt](request.txt) | Verbatim task supplied by the user. |
| [requirements-traceability.csv](requirements-traceability.csv) | 339 granular source-to-component, ADR, and gate records. |
| [requirements-traceability.md](requirements-traceability.md) | Traceability scope, coverage, and remaining evidence gaps. |
| [rule-contracts.csv](rule-contracts.csv) | Exact R1-R8 source text and rule-specific behavior. |
| [source-checks.json](source-checks.json) | Read-only manifests, headers, row counts, calendar, and source fixtures. |
| [source_audit.py](source_audit.py) | Read-only source extraction and fixture checks. |
| [structurizr-elements.csv](structurizr-elements.csv) | 46 existing model elements with source locations. |
| [structurizr-gap-report.md](structurizr-gap-report.md) | 14 proposed model follow-ups with existing element and view mappings. |
| [structurizr-inventory.json](structurizr-inventory.json) | Model text inventory and protected DSL hash. |
| [structurizr-relationships.csv](structurizr-relationships.csv) | 127 existing model relationships with source locations. |
| [structurizr-views.csv](structurizr-views.csv) | 16 existing view declarations with exact keys and locations. |
| [traceability-summary.json](traceability-summary.json) | Traceability counts by source and classification. |
| [verification.json](verification.json) | Results of documentation checks; no product acceptance asserted. |
| [verify_audit.py](verify_audit.py) | Repeatable standard-library documentation and source checks. |
| [workflow-contracts.csv](workflow-contracts.csv) | All 12 source stages, clocks, deadlines, and ownership gaps. |

## Checks and limits

The [verification record](verification.json) gives the final check results. It checks the pre-edit ZIP against its manifest, all original file hashes, the unchanged 55-KPI summary and source SQL, stable identifiers, local links and anchors, all eight rule source texts, all 12 Workflow stages, all 23 manager inputs, schema constraints, and the traceability references. The source checks compare all 91 manifests with delivered files and counts. The model text inventory covers 46 elements, 127 relationships, and 16 views.

The 339-row matrix records source meaning as well as counts. Dedicated tables preserve formula populations, clocks, NULL behavior, rule comparisons, Workflow deadlines, manager timing, and exact schema enums. The review ledger covers 911 units in the four original documents. Its inherited section context is not independent proof of each sentence. Source checks and links do not establish product correctness.

All 1,193 original dataset files remain unchanged. The brief, Markdown brief, recorded discussion, source contracts, reference SQL, KPI dictionary, previous review files, raw diagrams, and Structurizr DSL remain unchanged. There are 1,418 unchanged original files and 34 changed existing Markdown files. New audit artifacts are listed above. The previous root reconciliation diff remains unchanged and historical.

No KPI SQL, PostgreSQL equivalence check, model call, product test, restore test, official evaluation, Structurizr parser, or Structurizr renderer was run. All 30 product acceptance gates remain planned. Two DSL comment corrections are deferred with the other proposed model work. See [model gaps](structurizr-gap-report.md).

## Decisions that still constrain implementation

The [Decision Log](../registry/open-issues-registry.md#decision-log) records exact evidence, proposed owner roles, options, effects, and closure gates. The roles need team assignment. This report does not invent named owners or approved answers.

| Open matter | Required decision or evidence | Implementation effect |
|---|---|---|
| DL-01, DL-02: canonical calculation | Approve source types, PostgreSQL translation and equivalence evidence, and RAW versus exact-payload DEDUP policy. | Blocks release of canonical calculations. PostgreSQL remains the only product engine. |
| DL-03, DL-05: source closure and corrections | Define eligible current values, source precedence, and correction ties. | Blocks affected value release. A prior valid report cannot fill a current value slot. |
| DL-04: recalculation and restatement | Review full rebuild versus selective work and notification/approval. | Blocks a final correction/replay contract; selective work needs equivalence proof. |
| DL-06, DL-07, DL-19: authority and privacy | Approve row/column/purpose projections, capacity formula, small-group rules, write authority, and candidate activation. | Blocks access to undefined shared resources and governed configuration writes. Read access does not imply write access. |
| DL-08, DL-09: routing and rules | Approve stage owners and genuinely unspecified rule edges, including R3 missing warn, R4 reference/reset, and sparse or zero baselines. | Blocks final affected signal/routing behavior. Preserve all fixed source rule clauses. |
| DL-10: dated organization and uploads | Resolve M11 start timing and record upload receipt/readiness and event knowledge time. | Blocks exact replay coverage and attachment eligibility. Do not select 316 or 317 reports without authority. |
| DL-11, DL-17, DL-18: report and output mapping | Resolve suppressed/ongoing, number/query identifiers, NULL dimensions, and required chart/card/content mapping. | Blocks the final internal and wire contracts. A permissive schema does not remove required content. |
| DL-12: decision and execution records | Define human confirmation and execution evidence. | Blocks claims about completed organizational action. Human control remains Accepted. |
| DL-13, DL-14: bounded execution and failure | Select limits, model/provider, retries, failure export, and any validated fallback. | Blocks runtime limit and failure contracts. Independent valid-report publication remains Accepted. |
| DL-15: retention and restore | Approve retention, audit readers, backup interval, and restore procedure. | Blocks final operations readiness. Retain replay evidence in the meantime. |
| DL-16: official evaluation inputs | Obtain the organizer profile, reference hardware, hidden labels, and missing raw-column dictionary or an approved missing-contract disposition. | Blocks final acceptance claims. It does not prohibit all independent engineering preparation. |

These gaps do not reopen the one-Agent, PostgreSQL, deterministic controls, independent publication, or human-control decisions. They block affected implementation contracts or final acceptance; they are not a claim that all engineering work must stop. Product implementation was outside this task.

## Diff

The [unified diff](reconciliation.diff) compares each changed original with verified backup bytes. It also includes all new text artifacts except itself and the two derived change-index files. The ZIP is a separate binary addition. The [file index](file-changes.csv) lists every changed or added file. The [diff summary](diff-summary.json) records line counts, exclusions, and the diff hash. Line endings in text comparisons are normalized to LF; the baseline hashes preserve the exact original bytes.
