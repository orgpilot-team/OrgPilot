# ARKA architecture views and source evidence

The existing [Structurizr workspace](../../../architecture/structurizr/workspace.dsl) is the architecture visualization baseline. Preserve its identifiers, relationships and views. This documentation audit does not edit or render the model. Read the [view catalog and proposed gaps](../audit-2026-11-09/structurizr-gap-report.md).

| Existing view keys | Use |
|---|---|
| `IntegratedOverview`, `SystemContext`, `Containers` | Overall boundaries, roles, and the existing six-container target. |
| `Interfaces` | The three required Persian RTL interfaces. |
| `DataIntake`, `NightlyData` | Source intake, quality, protected archive, and snapshots. These are not an entity ERD. |
| `DeterministicAnalytics` | KPI, Workflow and signal components. It is not a complete rule decision table. |
| `EvidenceAndAnalysis`, `InteractiveAssistant` | Authorized evidence, controlled SQL and one bounded Agent. |
| `ReportDelivery`, `NightlyReporting`, `NightlyBrief` | Shared analysis, role content, validation and delivery. |
| `ManagerGovernance`, `ManagerUpload`, `HumanDecisionFollowUp` | Authorized settings/KPI lifecycle, upload paths, and human decisions. |
| `PartialPublication` | Independent outcomes and an incomplete day after a required-report failure. |

View keys are verified DSL declarations, not web URLs. No hosted viewer URL was supplied. The gap report gives source lines and exact scope. Detailed entity ERD, source-row lineage, rule/stage decision detail, and organization/access detail are visualization gaps where no matching existing view exists.

## Historical source evidence

The CSV/JSON catalogs in this directory remain useful historical observations: table/column inventory, header variants, candidate relationships, manager scopes, KPI dependencies, and earlier check receipts. Their original counts and SQL-prepare checks are not new audit results. Read [current source checks](../audit-2026-11-09/source-checks.json) and [traceability](../audit-2026-11-09/requirements-traceability.csv) for this run.

Candidate identifier matches are not enforced foreign keys. Execution dependencies are not selected-value lineage, minimum invalidation proofs, or display grants. RAW occurrences can repeat. Event occurrence IDs and customer/campaign parent registries are not supplied. Empty links remain optional until a contract says otherwise.

Source restrictions are Requirements. One bounded Agent, PostgreSQL-only product execution, independent valid-report publication, deterministic controls, and human action authority are Accepted boundaries. Physical keys, indexes, exact resource projections, capacity formulas, retention, and approval schemas remain Proposed or Open. Observation is an evidence category, not approval.

The original 26 raw diagram files remain unchanged as historical material. Their rendered previews are retired. Do not use or regenerate them as architecture views. The old build_documentation.py and its validators target that historical output; they were not run or revised. A later tooling decision must prevent their output from replacing the Structurizr baseline.

Review Q01-Q17 belongs to [S16](../sources/Adr.md). Manager Q01-Q16 belongs to the dataset inputs. VQ01-VQ10 belongs to the [legacy review register](open-questions.md). Keep these namespaces separate. Read the [central Decision Log](../registry/open-issues-registry.md#decision-log) for unresolved policies.
