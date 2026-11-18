# Proposed entity contracts

These are Proposed logical entity contracts, not implemented tables. The earlier diagram is retired. The source is `../002-data-architecture.md`, sections 1 and 2. This file does not approve physical tables or constraints.

| Entity | Defined identity or grain | Defined links and limits |
|---|---|---|
| Dataset | dataset_id | Namespace for source business identifiers. |
| SourceContract | source_id + contract_version | Source schema, schedule, and accepted mappings. |
| IngestBatch | One delivery acceptance attempt | previous_batch_id connects retries or revisions. No primary key name is specified. |
| SourceFile | One file occurrence | Batch receives files. Hash alone is not occurrence identity. |
| SourceRow | file_occurrence_id + csv_record_ordinal | Preserves original payload. |
| EntityObservation | One entity payload observation | source_row_id; business_id is not a raw occurrence key. |
| EventRecord | event_record_id | source_row_id and business_id; repeated events remain possible. |
| CorrectionLink | One correction relationship | source_row_id; conflicting correction precedence is open. |
| Snapshot | One frozen input and policy set | snapshot_id is used by downstream facts and observations. |
| SnapshotInput | A selected input in a snapshot | SourceFile and Snapshot links; final join key is unspecified. |
| FactVersion | snapshot_id + projection_id + business_id | Rebuildable fields and contributor references. |
| KpiDefinition | kpi_id + definition_version | Supplied definition and original SQL hash. |
| KpiDependency | One declared dependency | Definition link; physical key is unspecified. |
| QueryRun | One recorded calculation or query | Snapshot link; final primary key contract is unspecified. |
| KpiObservation | snapshot_id + definition_version + entity_id + dim_key + business_date | QueryRun and definition links. |
| EvidenceRef | One evidence reference | KPI observation support; no final physical key. |
| SignalEpisode / SignalOccurrence | Episode and occurrence | Proposal specifies a one-to-many conceptual link. |
| InsightVersion / ReportVersion | Versioned insight and report | Many-to-many concept; join-table schema is not defined. |
| ReportVersion | report_day + manager_id + run_id + version | Snapshot, policy, validation, and supersedes references. |
| DecisionEvent / ActionDraft | Decision event and draft | Report informs decisions; decision proposes drafts. |
| OrgNode / OrgEdgeVersion | Organization node and dated edge | AccessGrantVersion scopes nodes. Final keys remain unspecified. |
| AuthContext / access log / budget ledger | Security context and records | Logical security layer only; no final DDL. |
| DQIncident / ExpectedDelivery | Data issue and expected delivery | A missing delivery can have an issue without a SourceFile. |

The conceptual links remain Proposed physical contracts. PostgreSQL is the only product database engine, including KPI and custom-query calculation. This engine boundary is Accepted in [ADR-01](../registry/decisions-registry.md#adr-01). The former SQLite product calculator is superseded. An isolated reference test oracle is outside the product. SQL equivalence, final DDL, indexes, security roles, retention, and join-table keys remain Open or Proposed. These entities are not installed tables.

Use [document 002](../002-data-architecture.md#data-2) for the current logical grains and additional internal records. Structurizr has component views, but no detailed entity ERD. That is a [recorded visualization gap](../audit-2026-11-09/structurizr-gap-report.md), not a reason to invent a view or physical FK.
