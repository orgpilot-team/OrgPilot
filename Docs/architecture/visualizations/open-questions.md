# Open questions and review points

Review date: 2026-11-09. No item below changes the supplied access matrix or an Accepted architecture decision. These are diagram review IDs, now prefixed VQ. They are not the S16 architecture questions or S07 manager-input questions. Read the [Q01-Q17 map](../004-reconciliation-review.md#question-map) and [central Decision Log](../registry/open-issues-registry.md#decision-log).

Use Open and Proposed as decision statuses. Observation is evidence, not approval. The earlier CONFIRMED label never establishes team approval.

| ID | Status | Question or review point | Evidence | Review owner |
|---|---|---|---|---|
| VQ01 | Open | Is M11 first active for a report on morning 75 or 76? Static start is day 75. The next-morning input rule conflicts with it. | managers.csv; teams.csv; scripted_inputs IN05; README; ADR-08 | Project owner |
| VQ02 | Open | Which historic marketplace rows can M11 query? How does “since activity began” apply to paid/refund dates and old orders? | Manager Q05; K_MKT_ORDERS; K_MKT_REV | Data and security owners |
| VQ03 | Open | Define exact allowed raw text fragments for direct-team title/blocker evidence. Define customer-data redaction. No general raw-column grant exists. | Brief pp.10,12,13; tasks and tickets headers | Security owner |
| VQ04 | Open | Define source-row projections for shared orders and cross-team tickets for queries beyond supplied KPI results. No order team key exists. | reference SQL; access matrix | Data and security owners |
| VQ05 | Open | Define team capacity from availability status, working days, and staff effective dates. Specify minimum group size and prevention of individual inference. | Brief pp.6,12,13; staff_availability; calendar | Product and security owners |
| VQ06 | Open | Confirm accepted RAW or exact-payload dedup input for orders. Current duplicate keys can multiply joins. | day_076; KPI-VAL-001; ADR-02 | Project owner |
| VQ07 | Open | PostgreSQL-only execution is Accepted. Complete versioned translations for all 55 KPIs, equivalence proof, input types, RLS roles, and safe query projections. Embedded SQLite product calculation is superseded. | S16 Q03; S17; ADR-01,06; DL-01,06 | Engineering and security team |
| VQ08 | Proposed | Complete physical keys, nullable FKs, indexes, many-to-many tables, and audit access for the conceptual model. | Architecture 002 section 2 | Data architecture team |
| VQ09 | Open | Define missing-delivery publication, source closure, correction ties, restatement, retention, and source-calendar known-at rules. | ADR-04,05,08,11,12 | Project and architecture owners |
| VQ10 | Open | A complete official raw data dictionary is absent. Customer/campaign registries and event occurrence IDs are absent. Do not invent their FKs. | Observed CSV headers; brief p.14 | Source owner |

CONFIRMED restrictions are not open questions: upper managers receive aggregates only; direct supervisors have a workload-purpose exception for their team; attendance is not for individual monitoring; every query is scoped before LLM access. A dependency never creates a permission.

The active visualization standard is the existing Structurizr workspace. See the [view catalog and gaps](../audit-2026-11-09/structurizr-gap-report.md). No question here authorizes a new grant, engine, or Agent.
