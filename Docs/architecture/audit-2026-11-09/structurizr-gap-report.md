# Structurizr gap report

This report proposes later model work. It does not edit the DSL, replace views, add runtime elements, run a parser, or render a diagram.

The baseline is [workspace.dsl](../../../architecture/structurizr/workspace.dsl). Its identifiers are flat. Implicit relationships are disabled. It has one default SystemContext view, existing focused static/dynamic views, a ten-summary IntegratedOverview, and retained styles/layout directives. No associated architecture README, included DSL file, hosted-view URL, or exported view artifact was found under `architecture/`.

The text inventory is not a Structurizr syntax or layout validation. Source declarations and relationship endpoints were checked. Preserve every existing element, relationship, view key, include/exclude selection, style, and target process boundary until a later scoped change is approved.

Observed inventory: 46 elements, 127 model relationships, and 16 distinct view declarations. The source comment saying 15 views is stale. The [element](structurizr-elements.csv), [relationship](structurizr-relationships.csv), and [view](structurizr-views.csv) catalogs retain exact source lines.

| Existing key | Kind / scope | DSL line | Existing purpose |
|---|---|---|---|
| `IntegratedOverview` | custom / `logical summaries` | 650 | One-page unified architecture overview for team discussion. |
| `SystemContext` | systemContext / `arka` | 656 | Human management roles and external source/model boundaries. |
| `Containers` | container / `arka` | 663 | Six runtime containers; one modular codebase and one PostgreSQL database. |
| `Interfaces` | component / `web` | 669 | Three Persian RTL interfaces with API access controls. |
| `DataIntake` | component / `worker` | 675 | Structured intake, RAW preservation, data quality and snapshots. |
| `DeterministicAnalytics` | component / `worker` | 681 | Deterministic KPI/workflow analysis, signal ranking and selection. |
| `EvidenceAndAnalysis` | component / `api` | 687 | Authorized evidence, controlled SQL and a bounded investigation. |
| `ReportDelivery` | component / `api` | 693 | Role projection, validation and independent report/QA export. |
| `ManagerGovernance` | component / `api` | 704 | Authorized manager inputs and the controlled new-KPI lifecycle. |
| `NightlyReporting` | dynamic / `arka` | 718 | Scheduled data processing, selected shared analysis and independent morning reports. |
| `NightlyData` | dynamic / `worker` | 737 | D-1 intake, canonical calculations and deterministic deep-analysis selection. |
| `NightlyBrief` | dynamic / `api` | 758 | Reuse shared authorized analysis. Investigate selected gaps within limits, then validate each package. |
| `InteractiveAssistant` | dynamic / `api` | 785 | Scoped questions use D-1 data and approved upload revisions. Validate the answer and export required QA JSON. |
| `ManagerUpload` | dynamic / `api` | 812 | Document and structured paths are alternatives. Only successful authorized revisions become evidence. |
| `HumanDecisionFollowUp` | dynamic / `api` | 841 | Humans decide, approve and execute. ARKA records drafts, status and later observations. |
| `PartialPublication` | dynamic / `api` | 868 | Provider or budget failure may precede a draft. Report failures remain separate from ten-valid-report acceptance. |

## Requirement-to-model review

All changes below are Proposed future work. Preserve means the target already expresses the boundary; it does not mean implemented or tested. Visualization gaps do not authorize new business rules.

| Gap ID / action | Requirement or corrected contract | Existing elements/views to preserve | Proposed later change |
|---|---|---|---|
| SG-01 / Revise later | Source authority and inventory comments; S01/S18/S19; AUD-056/057 | All existing elements and all declared views | Update the missing-review-source assertion, the all-Proposed documentation description, and the stale 15-view count. Keep official requirements distinct from team choices and recommendations. |
| SG-02 / Add detail later | R1-R8 and three control points; REQ-R1 through REQ-R8; AT-24; document 001 section 7.1 | signals, reportWriter, outputValidator; DeterministicAnalytics, NightlyData, NightlyBrief | Existing notes already name every rule. Add trace IDs and explicit fixed comparisons/unknown cases to focused detail. No separate rules runtime service is needed. |
| SG-03 / Add detail later | All 12 Workflow stages; REQ-WF-*; AT-25; workflow-contracts.csv | workflows, kpi; DeterministicAnalytics, NightlyData | Keep M01 end-to-end ownership. Show numeric SLA versus promised_by deadline, blank follow-up SLA, median targets, and WF2/WF3 KPI differences. Stage owners stay Open. |
| SG-04 / Visualization gap | Logical entity relationships; document 002 section 2; Proposed physical contracts | postgres, snapshots, quality; Containers, DataIntake | No existing view is an entity ERD. Propose a later Structurizr custom detail view or equivalent approved data-model documentation. Do not invent a current key, FK or cardinality. A missing-source incident has no mandatory SourceFile. |
| SG-05 / Visualization gap | Number-to-source-row lineage; REQ-02/REQ-05; kpi-contracts.csv; AT-02/10 | kpi, queryGateway, evidence, audit, rawFiles; EvidenceAndAnalysis, ReportDelivery | Existing views show responsibility paths, not row-level value lineage. Add later detail for result/query/context/contributors/file receipt. Do not convert execution dependencies into visibility grants. |
| SG-06 / Refine only after policy | Shared-resource access and privacy; DL-06/07/17; access matrix; AT-06/30 | access, queryGateway, evidence, insights; EvidenceAndAnalysis, InteractiveAssistant | Preserve current RLS/identity boundary. Exact row/column predicates, redaction, NULL-dimension mapping and small-group capacity rules remain Open. Do not add a grant to make a diagram complete. |
| SG-07 / Preserve; label unresolved detail | Report content, chart and state mapping; REQ-OUT-*; DL-11/18; AT-26/30 | insights, reportWriter, outputValidator, publication; ReportDelivery, NightlyBrief | The model already submits charts/cards and uses shared Insight. Attach complete content/field trace IDs. suppressed/ongoing and internal schema remain Open. Atomic package mechanics are Proposed, independent outcomes Accepted. |
| SG-08 / Preserve; refine later | Failure and parent execution control; Accepted independent publication; DL-13/14; AT-21/28 | requests, agent, modelGateway, jobs, publication, audit; PartialPublication | Preserve pre-draft failure propagation, cancellation, bounded repair, and incomplete day. Do not add guaranteed fallback success or reset parent limits. Exact limits/status export stay Open. |
| SG-09 / Preserve; no engine change | Canonical SQL and KPI lifecycle; REQ-KPI-*; DL-01/02/19; AT-02/27 | managerConfig, kpi, worker, audit; ManagerGovernance, NightlyData | Preserve inactive-candidate validation and approval path and the single PostgreSQL product engine. Native SQL equivalence, types and RAW/DEDUP acceptance need proof. A reference oracle is test infrastructure, not another product container. |
| SG-10 / Preserve; clarify later | Upload readiness and source formats; REQ-INPUT-*; DL-10/19; AT-22/29 | documents, ingestion, quality, worker, queryGateway; ManagerUpload | Preserve separate document and structured-data revisions. State actual CSV config/JSON manifest formats more precisely if needed. Excel format scope remains Open. Pending/failed rows never become evidence. |
| SG-11 / Preserve; refine only after policy | Human decision and actual execution truth; REQ-11; DL-12; AT-14/29 | decisions, agent, audit; HumanDecisionFollowUp | Keep existing human-reported status path and no outbound action connector. Clarify confirmation evidence/fields without implying the system performs transfers or sends drafts. |
| SG-12 / Preserve; no invented schema | Evaluation export and cost/status evidence; DL-13/16; AT-15/17/18/30 | publication, audit, modelGateway; ReportDelivery, PartialPublication | Existing export ownership is correct. Precise cost/status filenames and schema remain unprovided. Do not invent links or claim official evaluation from a valid schema. |
| SG-13 / Visualization gap | Dated organization hierarchy and grants; REQ-03/08/09; S05; DL-06/10 | access, managerConfig; SystemContext, Interfaces, ManagerGovernance | Existing views show three role classes, not every dated unit/team/manager/staff grant. Add an appropriate later detail only after timing/historical-scope policy. Do not draw all 11 managers as active for every day. |
| SG-14 / Documentation tooling follow-up | Retired diagram generator; User visualization standard; legacy visualizations/build_documentation.py | No runtime component change | Do not run the old generator over active documentation. It still targets retired output. Later retire or adapt tooling without rebuilding or restructuring the existing Structurizr workspace. |

## Next model phase

First review these proposed changes against the corrected documentation and central Decision Log. Make small changes to existing properties or focused views where sufficient. Do not rename keys or replace the workspace to fit a new drawing. Add a view only when the stated information is absent. Validate DSL syntax and inspect rendered layout in that later phase. No model modification is authorized by this audit.
