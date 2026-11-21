# Background Worker components

## Purpose and Scope

The Background Worker runs deterministic ingestion, validation, analytics, workflow, signal, report-evidence, and decision-effect jobs. PostgreSQL supplies durable job and product state.

## Runtime Technology

.NET 10 Worker Service with shared modular-monolith libraries, EF Core, and Npgsql.

## Trust Boundary

The Worker accepts only persisted jobs and pinned dependencies. Source data is untrusted until validation and normalization pass.

## Allowed Responsibilities

- Claim deterministic jobs from PostgreSQL.
- Ingest, normalize, validate, project, calculate, and store deterministic results.
- Build pinned report evidence and decision-effect assessments.

## Forbidden Responsibilities

- Run agent graphs or model calls.
- Publish reports or process manager commands.
- Change reference KPI SQL or output contracts.

> **Implementation source note.** This document and `16-domain-model.md` define the Background Worker boundaries used for implementation. The DSL is a visual overview. The Worker is a deterministic pipeline, so most absorbed components are stateless functions or derived read models, not aggregates.

## Component Map (target)

| Area | Components |
|---|---|
| Job control | Run Stage Coordinator |
| Intake | Ingestion Coordinator (includes source adapters, normalization, data quality) |
| Projection | Snapshot Service (includes derived projections) |
| Analytics | Semantic Registry (includes KPI translation and configuration validation); KPI Calculator; Workflow Engine; Signal Engine |
| Reporting | Report Evidence Builder; Decision Effect Evaluator |

Removed as separate components: Configuration Validation Runner and KPI Definition Preprocessor (merged into Semantic Registry), Source Adapters, Normalizer, and Data Quality Service (merged into Ingestion Coordinator), Projection Service (merged into Snapshot Service).

## Internal Relationships

The Run Stage Coordinator invokes pinned stages. Components use in-process calls and persist results in PostgreSQL. Intake, translation, and projection are deterministic functions inside their owning components, not separately coordinated state.

## External Relationships

The Worker reads the DIDRAH Input Dataset, writes original bytes to the Protected File Archive, and reads and writes PostgreSQL. It can send redacted telemetry to the optional Collector.

## Component Sections

<a id="run-stage-coordinator"></a>

### Run Stage Coordinator

- **DSL identifier:** `runStageCoordinatorV2`;
- **Display name:** Run Stage Coordinator.
- **Purpose:** Claim Ready jobs and run deterministic stages.
- **Responsibilities:** Claim leases, load dependencies, invoke stages, and record terminal state.
- **Inputs:** Persisted run-stage job and pinned versions.
- **Outputs:** Stage results and durable status.
- **Owned state:** Run-stage job, lease, attempt, and dependency state in PostgreSQL.
- **Dependencies:** PostgreSQL and deterministic Worker stages.
- **Security boundary:** Only persisted valid jobs can run.
- **Forbidden responsibilities:** Create ad hoc work, run agents, or publish.
- **Failure behavior:** Record failure and release or expire the lease under policy.
- **Idempotency:** Job key and stage receipt make retry safe.
- **Observability:** Record run, job, lease, attempt, stage, and trace ID.
- **Related ADRs:** ADR-0011, ADR-0018.
- **Open issues:** Retry count and dead-letter policy remain open.

<a id="ingestion-coordinator"></a>

### Ingestion Coordinator

- **DSL identifier:** `ingestionCoordinator`;
- **Display name:** Ingestion Coordinator.
- **Purpose:** Control one atomic versioned source intake: parse, normalize, validate quality, and commit.
- **Responsibilities:** Select schema version, parse fields, archive originals, convert to canonical types/units/keys, detect missing/late/duplicate/invalid data, check manifests, hashes, source status, idempotency keys, and batch commit.
- **Inputs:** Pinned source contracts and intake job.
- **Outputs:** Committed batch with `DataIssue[]` and canonical rows, or explicit intake failure. This component absorbs Source Adapters, Normalizer, and Data Quality Service (`sourceAdapters`, `normalizer`, `dataQualityService` in the current DSL): all three are deterministic functions over the same pinned input, and `DataIssue` is an entity of the `IngestionBatch` aggregate.
- **Owned state:** Batch, source status, data issues, canonical rows, and intake receipts in PostgreSQL; original bytes in archive.
- **Dependencies:** DIDRAH Input Dataset, Protected File Archive, and PostgreSQL.
- **Security boundary:** Source files are untrusted; unknown schema/unit/key is quarantined, never guessed.
- **Forbidden responsibilities:** Fabricate missing values, turn a data issue into a business signal, calculate KPIs, or overwrite source bytes.
- **Failure behavior:** Do not expose a partial batch.
- **Idempotency:** Manifest hash and source version prevent duplicate intake.
- **Observability:** Record source, version, hash, batch, status, and trace ID.
- **Related ADRs:** ADR-0001, ADR-0004, ADR-0011.
- **Open issues:** None.

<a id="snapshot-service"></a>

### Snapshot Service

- **DSL identifier:** `snapshotService`;
- **Display name:** Snapshot Service.
- **Purpose:** Pin all versions used by one run and build the derived projections from them.
- **Responsibilities:** Pin data, organization, policy, and configuration versions, then build reproducible facts and process projections from committed events.
- **Inputs:** Run plan and committed source state.
- **Outputs:** Snapshot ID, pinned version set, and versioned projections. This component absorbs Projection Service (`projectionService` in the current DSL): projections are derived read models rebuilt from one immutable snapshot, not an aggregate or a separate component.
- **Owned state:** Snapshot metadata and versioned projections in PostgreSQL.
- **Dependencies:** PostgreSQL.
- **Security boundary:** A run cannot mix unpinned versions; only pinned committed data enters a projection.
- **Forbidden responsibilities:** Mutate source history, select versions after calculation starts, calculate unregistered KPIs, or rewrite source events.
- **Failure behavior:** Stop the run stage before projection.
- **Idempotency:** Run ID maps to one pinned snapshot.
- **Observability:** Record snapshot, versions, run, status, and trace ID.
- **Related ADRs:** ADR-0003, ADR-0011.
- **Open issues:** None.

<a id="semantic-registry"></a>

### Semantic Registry

- **DSL identifier:** `semanticRegistry`;
- **Display name:** Semantic Registry.
- **Purpose:** Own immutable KPI definition versions, SQL translation, semantic validation, and parity eligibility.
- **Responsibilities:** Apply deterministic translation rules (median, date intervals, percentage, timezone), store PostgreSQL SQL and KPI metadata, accept a Parity Receipt from the Acceptance Test Harness, and mark a definition version as eligible for activation.
- **Inputs:** Authorized KPI candidate reference, translation version, and Parity Receipt.
- **Outputs:** Validated definition version, eligibility state, and dependency checks. This component absorbs KPI Definition Preprocessor and Configuration Validation Runner (`kpiDefinitionPreprocessor`, `configurationValidationRunnerV2` in the current DSL): translation and validation produce one immutable definition version.
- **Owned state:** Semantic definition versions, translation artifacts, eligibility state, and validation receipts in PostgreSQL.
- **Dependencies:** Configuration-candidate contract, Parity Receipt contract, and PostgreSQL.
- **Security boundary:** Only validated definitions with a passing Parity Receipt are eligible for activation; reference SQL is read-only.
- **Forbidden responsibilities:** Execute SQL at registration, translate arbitrary text at calculation time, change reference SQLite SQL, or control the active-version pointer.
- **Failure behavior:** Reject the candidate version and preserve the current eligible definition. Configuration Service leaves its active-version pointer unchanged.
- **Idempotency:** Definition ID and version prevent duplicate registration.
- **Observability:** Record version, owner, eligibility, dependencies, receipt, and trace ID.
- **Related ADRs:** ADR-0002, ADR-0007, ADR-0014, ADR-0016.
- **Open issues:** None.

<a id="kpi-calculator"></a>

### KPI Calculator

- **DSL identifier:** `kpiCalculator`;
- **Display name:** KPI Calculator.
- **Purpose:** Execute the 55 approved PostgreSQL KPI queries.
- **Responsibilities:** Load approved definitions, run them against pinned projections, and store values and lineage.
- **Inputs:** Snapshot, semantic version, and approved SQL.
- **Outputs:** KPI values, QueryRun, and lineage.
- **Owned state:** KPI results and QueryRun records in PostgreSQL (`KpiResult` is a result record, not an aggregate).
- **Dependencies:** Semantic Registry and PostgreSQL.
- **Security boundary:** Only registered, parity-passed SQL can execute.
- **Forbidden responsibilities:** Generate SQL, use SQLite in product runtime, or call a model.
- **Failure behavior:** Fail the KPI or run stage and preserve explicit lineage.
- **Idempotency:** Snapshot, KPI, and definition version identify one result.
- **Observability:** Record KPI, version, duration, row count, status, and trace ID.
- **Related ADRs:** ADR-0002, ADR-0011, ADR-0016.
- **Open issues:** None.

<a id="workflow-engine"></a>

### Workflow Engine

- **DSL identifier:** `workflowEngine`;
- **Display name:** Workflow Engine.
- **Purpose:** Reconstruct WF1-WF3 and calculate deterministic workflow measures.
- **Responsibilities:** Build stage observations, SLA, backlog, and bottleneck facts.
- **Inputs:** Pinned projections, organization version, and workflow rules.
- **Outputs:** Workflow observations and metrics.
- **Owned state:** Workflow facts in PostgreSQL.
- **Dependencies:** PostgreSQL.
- **Security boundary:** Approved workflow and ownership rules control reconstruction.
- **Forbidden responsibilities:** Assign ad hoc owners, generate narrative, or publish.
- **Failure behavior:** Fail the stage and preserve prior published results.
- **Idempotency:** Snapshot and workflow-rule version identify the result.
- **Observability:** Record workflow, stage counts, rules, status, and trace ID.
- **Related ADRs:** ADR-0006, ADR-0007, ADR-0011.
- **Open issues:** None.

<a id="signal-engine"></a>

### Signal Engine

- **DSL identifier:** `signalEngine`;
- **Display name:** Signal Engine.
- **Purpose:** Maintain deterministic signal lifecycles and escalation.
- **Responsibilities:** Detect, group, suppress, rank, escalate, and close signals under approved rules.
- **Inputs:** KPI and workflow facts, signal-rule version, and manager-priority configuration.
- **Outputs:** Versioned signal episodes and recipient state.
- **Owned state:** Signal episodes and recipient state in PostgreSQL.
- **Dependencies:** PostgreSQL.
- **Security boundary:** Rules and recipient scope are deterministic and versioned.
- **Forbidden responsibilities:** Generate model content or auto-create human decisions.
- **Failure behavior:** Preserve the prior episode state and fail the stage.
- **Idempotency:** Signal key, observation, and rule version make retry stable.
- **Observability:** Record lifecycle transition, rule, recipients, status, and trace ID.
- **Related ADRs:** ADR-0006, ADR-0007, ADR-0017.
- **Open issues:** None.

<a id="report-evidence-builder"></a>

### Report Evidence Builder

- **DSL identifier:** `reportEvidenceBuilderV2`;
- **Display name:** Report Evidence Builder.
- **Purpose:** Build one pinned evidence package and canonical report per manager job.
- **Responsibilities:** Collect approved facts, signals, stored follow-up assessments, citations, and scope references. Build an internal deterministic chart specification when the UI needs a chart. The specification contains the chart type, KPI, time range, breakdown, and target line.
- **Inputs:** Pinned run results, stored Decision Effect records, and authorized manager scope.
- **Outputs:** Evidence package, canonical report, internal chart specification, and unlocked Agent Job.
- **Owned state:** Evidence package and report candidate in PostgreSQL.
- **Dependencies:** PostgreSQL and stored Decision Effect records.
- **Security boundary:** Package content cannot exceed manager scope.
- **Forbidden responsibilities:** Call a model, publish, merge managers, or add a chart field to the formal submission contract.
- **Failure behavior:** Record an incomplete package or explicit failure under policy. If model narrative is unavailable later, the deterministic canonical report remains valid without narrative.
- **Idempotency:** Run, manager, and package version identify one result.
- **Observability:** Record package, manager scope reference, source versions, status, and trace ID.
- **Related ADRs:** ADR-0004, ADR-0008, ADR-0009, ADR-0011, ADR-0022.
- **Open issues:** None.

<a id="decision-effect-evaluator"></a>

### Decision Effect Evaluator

- **DSL identifier:** `decisionEffectEvaluator`;
- **Display name:** Decision Effect Evaluator.
- **Purpose:** Evaluate KPI change and guardrails for due decisions.
- **Responsibilities:** Compare pinned before and after evidence and record a structured internal assessment.
- **Inputs:** Due decision, KPI facts, guardrails, and evaluation window.
- **Outputs:** Internal Decision Effect and follow-up evidence.
- **Owned state:** Versioned Decision Effect record in PostgreSQL.
- **Dependencies:** PostgreSQL and persisted decision, KPI, guardrail, evaluation-window, and comparison-context records.
- **Security boundary:** Assessment is deterministic and internal.
- **Forbidden responsibilities:** Change the output schema, claim causality without evidence, depend on Report Evidence Builder, or call a model.
- **Failure behavior:** Record `too_early`, `insufficient_data`, `not_isolatable`, or explicit failure as allowed.
- **Idempotency:** Decision and evidence-window versions identify one assessment.
- **Observability:** Record decision, window, result, limitation, and trace ID.
- **Related ADRs:** ADR-0010, ADR-0011, ADR-0015.
- **Open issues:** None.

## Consolidation log (implementation model)

The following former components are intentionally absent from the implementation model. See `16-domain-model.md` §6 for the reasoning.

| Removed component | Disposition |
|---|---|
| Configuration Validation Runner | Merged into Semantic Registry |
| KPI Definition Preprocessor | Merged into Semantic Registry |
| Source Adapters | Merged into Ingestion Coordinator |
| Normalizer | Merged into Ingestion Coordinator |
| Data Quality Service | Merged into Ingestion Coordinator (`DataIssue` is an entity of `IngestionBatch`) |
| Projection Service | Merged into Snapshot Service (derived read model) |

`KpiParityService` is not a Worker domain service in the implementation model; parity is owned by the Acceptance Test Harness in the Scheduler and Replay Runner (doc 12, ADR-0016).

## Container-level Open Issues

- Retry count, dead-letter policy, and reconciliation cadence remain open.
- Retention, backup frequency, RPO, and RTO remain open.
