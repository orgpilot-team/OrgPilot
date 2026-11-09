# Requirement traceability guide

The [CSV matrix](requirements-traceability.csv) has 339 source-backed rows. The original REQ-01 through REQ-17 remain umbrella IDs. Their children are atomic obligations or exact source records. Accepted decisions use DEC-* IDs; they are not mislabeled official requirements. Observation is an evidence category, not approval.

Each row identifies the source path/location, obligation, existing component, contract/rule, ADR, planned acceptance gate and remaining gap. A documented row is not an executed test or a complete implementation. The [acceptance-basis register](acceptance-basis.csv) separates official requirements, Accepted target boundaries and Proposed mechanisms.

| Detailed coverage | Artifact / semantic checks |
|---|---|
| R1-R8 | [Rule contracts](rule-contracts.csv): exact source text, trigger/input, output/routing, state and gates. Fixed comparisons are separate from genuine ambiguity. |
| 55 canonical KPIs | [KPI contracts](kpi-contracts.csv): every original field and SQL/hash; formula/population, clock/window, row/NULL and precision boundaries. Metadata checked against all 55 source rows. No SQL was run. |
| 12 Workflow stages | [Stage contracts](workflow-contracts.csv): every endpoint, SLA kind, median target, end-to-end owner and Open stage owner. Canonical workflow SQL remains separate. |
| Organization/access | Exact unit/team/manager/staff assignment and all 11 access-matrix records. Known/effective time and read-versus-write authority remain distinct. |
| Sources/schema | Every delivered header signature and five canonical view contracts. [Source checks](source-checks.json) compare all 91 manifests with actual counts and preserve fixture evidence. |
| Manager inputs | [All 23 records](manager-input-contracts.csv), including all 16 questions and seven non-question events. No stored numerical answers. |
| Output schemas | [Every property/constraint](output-schema-contracts.csv), exact required sets and enums. Conditional nested requirements are not promoted to unconditional fields. |
| Report/Agent/privacy/delivery | Atomic brief-derived obligations and five separately classified Accepted boundaries. Unsupported engineering details remain Proposed/Open. |

Open gaps are explicit: PostgreSQL equivalence/types and input mode; closure/publication; shared-source/privacy/capacity policies; stage owners; unspecified rule boundaries; M11/receipt timing; output mapping and candidate write authority; model limits and final organizer profile. See the [Decision Log](../registry/open-issues-registry.md#decision-log).

Optional monthly board summary, forecasting, what-if, audio, messenger integration and automatic decision-impact evaluation are not mandatory runtime dependencies. Employee ranking/surveillance, autonomous actions, real-system connectors, payroll and budgeting remain outside the brief's scope. Ten base reports do not remove the active-manager requirement.
