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

## Component Map

| Area | Components |
|---|---|
| Job control | Run Stage Coordinator; Configuration Validation Runner |
| Intake | Ingestion Coordinator; Source Adapters; Normalizer; Data Quality Service |
| Projection | Snapshot Service; Projection Service |
| Analytics | Semantic Registry; KPI Definition Preprocessor; KPI Calculator; Workflow Engine; Signal Engine |
| Reporting | Report Evidence Builder; Decision Effect Evaluator |

## Internal Relationships

The Run Stage Coordinator invokes pinned stages. The Configuration Validation Runner invokes configuration-only validation. Components use in-process calls and persist results in PostgreSQL.

## External Relationships

The Worker reads the DIDRAH Input Dataset, writes original bytes to the Protected File Archive, and reads and writes PostgreSQL. It can send redacted telemetry to the optional Collector.

## Component Sections

<a id="run-stage-coordinator"></a>

### Run Stage Coordinator

- **DSL identifier:** `runStageCoordinatorV2`; **Display name:** Run Stage Coordinator.
- **Purpose:** Claim Ready jobs and run deterministic stages. **Responsibilities:** Claim leases, load dependencies, invoke stages, and record terminal state. **Inputs:** Persisted run-stage job and pinned versions. **Outputs:** Stage results and durable status.
- **Owned state:** Run-stage job, lease, attempt, and dependency state in PostgreSQL. **Dependencies:** PostgreSQL and deterministic Worker stages. **Security boundary:** Only persisted valid jobs can run. **Forbidden responsibilities:** Create ad hoc work, run agents, or publish.
- **Failure behavior:** Record failure and release or expire the lease under policy. **Idempotency:** Job key and stage receipt make retry safe. **Observability:** Record run, job, lease, attempt, stage, and trace ID. **Related ADRs:** ADR-0011, ADR-0018. **Open issues:** Retry count and dead-letter policy remain open.

<a id="configuration-validation-runner"></a>

### Configuration Validation Runner

- **DSL identifier:** `configurationValidationRunnerV2`; **Display name:** Configuration Validation Runner.
- **Purpose:** Validate configuration jobs without activating configuration. **Responsibilities:** Claim validation jobs, check dependencies, translate KPI candidates, and store receipts. **Inputs:** Versioned configuration candidate. **Outputs:** Validation Receipt and approved or rejected state.
- **Owned state:** Validation job and receipt in PostgreSQL. **Dependencies:** PostgreSQL, KPI Definition Preprocessor, and Semantic Registry. **Security boundary:** Candidate data cannot become active without approval. **Forbidden responsibilities:** Activate configuration or run daily processing.
- **Failure behavior:** Keep the current active version. **Idempotency:** Candidate version and validator version identify the result. **Observability:** Record candidate, job, receipt, rule result, and trace ID. **Related ADRs:** ADR-0011, ADR-0014, ADR-0018. **Open issues:** None.

<a id="ingestion-coordinator"></a>

### Ingestion Coordinator

- **DSL identifier:** `ingestionCoordinator`; **Display name:** Ingestion Coordinator.
- **Purpose:** Control one atomic versioned source intake. **Responsibilities:** Check manifests, hashes, source status, idempotency keys, and batch commit. **Inputs:** Pinned source contracts and intake job. **Outputs:** Committed batch or explicit intake failure.
- **Owned state:** Batch, source status, and intake receipts in PostgreSQL. **Dependencies:** DIDRAH Input Dataset, Source Adapters, and PostgreSQL. **Security boundary:** Source files are untrusted. **Forbidden responsibilities:** Interpret business meaning before adapters and normalization.
- **Failure behavior:** Do not expose a partial batch. **Idempotency:** Manifest hash and source version prevent duplicate intake. **Observability:** Record source, version, hash, batch, status, and trace ID. **Related ADRs:** ADR-0001, ADR-0004, ADR-0011. **Open issues:** None.

<a id="source-adapters"></a>

### Source Adapters

- **DSL identifier:** `sourceAdapters`; **Display name:** Source Adapters.
- **Purpose:** Parse versioned source schemas and preserve source bytes and headers. **Responsibilities:** Select the schema version, parse fields, archive originals, and pass parsed values to normalization. **Inputs:** Versioned CSV or JSON source. **Outputs:** Parsed fields and archive reference.
- **Owned state:** Original bytes and hashes in Protected File Archive. **Dependencies:** Protected File Archive and Normalizer. **Security boundary:** Parsers use fixed schema and size limits. **Forbidden responsibilities:** Normalize business values, calculate KPIs, or overwrite source bytes.
- **Failure behavior:** Quarantine an invalid source and return a parse error. **Idempotency:** Source hash and adapter version identify one parse. **Observability:** Record adapter version, hash, counts, errors, and trace ID. **Related ADRs:** ADR-0001, ADR-0011. **Open issues:** None.

<a id="normalizer"></a>

### Normalizer

- **DSL identifier:** `normalizer`; **Display name:** Normalizer.
- **Purpose:** Convert parsed fields to canonical types, units, identifiers, and time semantics. **Responsibilities:** Apply approved deterministic mappings and send rows for quality checks. **Inputs:** Parsed source fields and mapping version. **Outputs:** Canonical rows or normalization errors.
- **Owned state:** None; normalized records persist after quality control. **Dependencies:** Source Adapters and Data Quality Service. **Security boundary:** Only approved mappings can change field meaning. **Forbidden responsibilities:** Infer missing business facts or calculate KPIs.
- **Failure behavior:** Reject or quarantine the affected row under data-quality policy. **Idempotency:** Source value and mapping version give the same result. **Observability:** Record mapping version, counts, error classes, and trace ID. **Related ADRs:** ADR-0001, ADR-0011. **Open issues:** None.

<a id="data-quality-service"></a>

### Data Quality Service

- **DSL identifier:** `dataQualityService`; **Display name:** Data Quality Service.
- **Purpose:** Record source quality facts and control accepted or quarantined records. **Responsibilities:** Detect missing, late, duplicate, corrected, changed, and invalid data. **Inputs:** Canonical rows and source metadata. **Outputs:** Accepted records, quarantine results, and quality issues.
- **Owned state:** Data-quality records and accepted source records in PostgreSQL. **Dependencies:** PostgreSQL. **Security boundary:** Quality rules are versioned and deterministic. **Forbidden responsibilities:** Fabricate missing values or hide source failures.
- **Failure behavior:** Preserve the issue and apply the approved incomplete-source policy. **Idempotency:** Source identity and rule version prevent duplicate issues. **Observability:** Record issue class, counts, source version, status, and trace ID. **Related ADRs:** ADR-0001, ADR-0004, ADR-0011. **Open issues:** None.

<a id="snapshot-service"></a>

### Snapshot Service

- **DSL identifier:** `snapshotService`; **Display name:** Snapshot Service.
- **Purpose:** Pin all versions used by one run. **Responsibilities:** Pin data, organization, policy, and configuration versions and start reproducible projection. **Inputs:** Run plan and committed source state. **Outputs:** Snapshot ID and pinned version set.
- **Owned state:** Snapshot metadata in PostgreSQL. **Dependencies:** PostgreSQL and Projection Service. **Security boundary:** A run cannot mix unpinned versions. **Forbidden responsibilities:** Mutate source history or select versions after calculation starts.
- **Failure behavior:** Stop the run stage before projection. **Idempotency:** Run ID maps to one pinned snapshot. **Observability:** Record snapshot, versions, run, status, and trace ID. **Related ADRs:** ADR-0003, ADR-0011. **Open issues:** None.

<a id="projection-service"></a>

### Projection Service

- **DSL identifier:** `projectionService`; **Display name:** Projection Service.
- **Purpose:** Build reproducible facts and process projections from committed source events. **Responsibilities:** Read pinned events, apply approved projection logic, and store versioned projections. **Inputs:** Snapshot ID and committed events. **Outputs:** Analytical facts and process projections.
- **Owned state:** Versioned projections in PostgreSQL. **Dependencies:** Snapshot Service and PostgreSQL. **Security boundary:** Only pinned committed data can enter a projection. **Forbidden responsibilities:** Calculate unregistered KPIs or rewrite source events.
- **Failure behavior:** Keep the prior valid projection and fail the stage. **Idempotency:** Snapshot and projection version identify the result. **Observability:** Record versions, row counts, duration, status, and trace ID. **Related ADRs:** ADR-0001, ADR-0002, ADR-0011. **Open issues:** None.

<a id="semantic-registry"></a>

### Semantic Registry

- **DSL identifier:** `semanticRegistry`; **Display name:** Semantic Registry.
- **Purpose:** Version approved KPI definitions and their execution metadata. **Responsibilities:** Store PostgreSQL SQL, units, precision, targets, ownership, and dependencies. **Inputs:** Validated KPI definition. **Outputs:** Approved version for calculation and dependency checks.
- **Owned state:** Semantic versions in PostgreSQL. **Dependencies:** PostgreSQL. **Security boundary:** Only validated approved definitions can become active. **Forbidden responsibilities:** Translate arbitrary text at calculation time or change reference SQLite SQL.
- **Failure behavior:** Keep the last active version and reject invalid registration. **Idempotency:** Definition ID and version prevent duplicate registration. **Observability:** Record version, owner, status, dependencies, and trace ID. **Related ADRs:** ADR-0002, ADR-0007, ADR-0014, ADR-0016. **Open issues:** None.

<a id="kpi-definition-preprocessor"></a>

### KPI Definition Preprocessor

- **DSL identifier:** `kpiDefinitionPreprocessor`; **Display name:** KPI Definition Preprocessor.
- **Purpose:** Translate approved KPI definitions into versioned PostgreSQL SQL before registration. **Responsibilities:** Apply deterministic translation rules and produce a validation candidate. **Inputs:** Approved KPI definition and translation version. **Outputs:** PostgreSQL SQL candidate and translation receipt.
- **Owned state:** Translation artifact and receipt in PostgreSQL. **Dependencies:** Configuration Validation Runner and Semantic Registry. **Security boundary:** Translation occurs before approval and registration. **Forbidden responsibilities:** Execute SQL, alter reference SQL, or activate a candidate.
- **Failure behavior:** Reject the candidate and preserve the active definition. **Idempotency:** Definition and translator versions identify the artifact. **Observability:** Record versions, status, receipt, and trace ID. **Related ADRs:** ADR-0002, ADR-0014, ADR-0016. **Open issues:** None.

<a id="kpi-calculator"></a>

### KPI Calculator

- **DSL identifier:** `kpiCalculator`; **Display name:** KPI Calculator.
- **Purpose:** Execute the 55 approved PostgreSQL KPI queries. **Responsibilities:** Load approved definitions, run them against pinned projections, and store values and lineage. **Inputs:** Snapshot, semantic version, and approved SQL. **Outputs:** KPI values, QueryRun, and lineage.
- **Owned state:** KPI results and QueryRun records in PostgreSQL. **Dependencies:** Semantic Registry and PostgreSQL. **Security boundary:** Only registered SQL can execute. **Forbidden responsibilities:** Generate SQL, use SQLite in product runtime, or call a model.
- **Failure behavior:** Fail the KPI or run stage and preserve explicit lineage. **Idempotency:** Snapshot, KPI, and definition version identify one result. **Observability:** Record KPI, version, duration, row count, status, and trace ID. **Related ADRs:** ADR-0002, ADR-0011, ADR-0016. **Open issues:** None.

<a id="workflow-engine"></a>

### Workflow Engine

- **DSL identifier:** `workflowEngine`; **Display name:** Workflow Engine.
- **Purpose:** Reconstruct WF1-WF3 and calculate deterministic workflow measures. **Responsibilities:** Build stage observations, SLA, backlog, and bottleneck facts. **Inputs:** Pinned projections, organization version, and workflow rules. **Outputs:** Workflow observations and metrics.
- **Owned state:** Workflow facts in PostgreSQL. **Dependencies:** PostgreSQL. **Security boundary:** Approved workflow and ownership rules control reconstruction. **Forbidden responsibilities:** Assign ad hoc owners, generate narrative, or publish.
- **Failure behavior:** Fail the stage and preserve prior published results. **Idempotency:** Snapshot and workflow-rule version identify the result. **Observability:** Record workflow, stage counts, rules, status, and trace ID. **Related ADRs:** ADR-0006, ADR-0007, ADR-0011. **Open issues:** None.

<a id="signal-engine"></a>

### Signal Engine

- **DSL identifier:** `signalEngine`; **Display name:** Signal Engine.
- **Purpose:** Maintain deterministic signal lifecycles and escalation. **Responsibilities:** Detect, group, suppress, rank, escalate, and close signals under approved rules. **Inputs:** KPI and workflow facts and signal-rule version. **Outputs:** Versioned signal episodes and recipient state.
- **Owned state:** Signal episodes and recipient state in PostgreSQL. **Dependencies:** PostgreSQL. **Security boundary:** Rules and recipient scope are deterministic and versioned. **Forbidden responsibilities:** Generate model content or auto-create human decisions.
- **Failure behavior:** Preserve the prior episode state and fail the stage. **Idempotency:** Signal key, observation, and rule version make retry stable. **Observability:** Record lifecycle transition, rule, recipients, status, and trace ID. **Related ADRs:** ADR-0006, ADR-0007, ADR-0017. **Open issues:** None.

<a id="report-evidence-builder"></a>

### Report Evidence Builder

- **DSL identifier:** `reportEvidenceBuilderV2`; **Display name:** Report Evidence Builder.
- **Purpose:** Build one pinned evidence package and canonical report per manager job. **Responsibilities:** Collect approved facts, signals, follow-up assessments, citations, and scope references. **Inputs:** Pinned run results and authorized manager scope. **Outputs:** Evidence package, canonical report, and unlocked Agent Job.
- **Owned state:** Evidence package and report candidate in PostgreSQL. **Dependencies:** PostgreSQL and Decision Effect Evaluator. **Security boundary:** Package content cannot exceed manager scope. **Forbidden responsibilities:** Call a model, publish, or merge managers.
- **Failure behavior:** Record an incomplete package or explicit failure under policy. **Idempotency:** Run, manager, and package version identify one result. **Observability:** Record package, manager scope reference, source versions, status, and trace ID. **Related ADRs:** ADR-0004, ADR-0008, ADR-0009, ADR-0011. **Open issues:** Fallback content remains open.

<a id="decision-effect-evaluator"></a>

### Decision Effect Evaluator

- **DSL identifier:** `decisionEffectEvaluator`; **Display name:** Decision Effect Evaluator.
- **Purpose:** Evaluate KPI change and guardrails for due decisions. **Responsibilities:** Compare pinned before and after evidence and record a structured internal assessment. **Inputs:** Due decision, KPI facts, guardrails, and evaluation window. **Outputs:** Internal Decision Effect and follow-up evidence.
- **Owned state:** Versioned Decision Effect record in PostgreSQL. **Dependencies:** PostgreSQL and Report Evidence Builder. **Security boundary:** Assessment is deterministic and internal. **Forbidden responsibilities:** Change the output schema, claim causality without evidence, or call a model.
- **Failure behavior:** Record `too_early`, `insufficient_data`, `not_isolatable`, or explicit failure as allowed. **Idempotency:** Decision and evidence-window versions identify one assessment. **Observability:** Record decision, window, result, limitation, and trace ID. **Related ADRs:** ADR-0010, ADR-0011, ADR-0015. **Open issues:** None.

## Container-level Open Issues

- Retry count, dead-letter policy, and reconciliation cadence remain open.
- Retention, backup frequency, RPO, and RTO remain open.
