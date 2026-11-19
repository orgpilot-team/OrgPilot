# 16. Domain Model (DDD) for the runtime components

This document defines the tactical Domain-Driven Design model for the three runtime components that carry business complexity: **Backend API**, **Background Worker**, and **Agent Runtime**. It is the implementation contract for module boundaries, aggregate invariants, ports, and domain events. It complements the C4 component inventory in docs 10, 11, and 13; where a C4 component name appears below, it is the adapter or application service implementing the named domain role.

Status: **Accepted for implementation**.

## 0. Shared rules

- **Modular monolith, not distributed microservices.** Bounded contexts are enforced by module boundaries and explicit application-service APIs, not by network calls. Cross-context calls go through an Anti-Corruption Layer (ACL) that translates foreign models.
- **Layering inside each context:** domain (entities, value objects, domain services, domain events) → application (use cases, ports) → infrastructure (PostgreSQL repositories, adapters, messaging). Dependencies point inward.
- **Persistence:** PostgreSQL is the single product database. Repositories are interfaces in the domain/application layer; SQL lives in infrastructure. Row-level security is enforced in the database and in every query port.
- **Determinism:** the domain clock is injected; no ambient time, randomness, or unordered iteration enters a domain decision. A domain event's payload is immutable and fully derived from pinned inputs.
- **Naming convention:** a use case is `VerbObject` (e.g. `ConfirmDecision`); a domain event is past tense (e.g. `DecisionConfirmed`).

## 1. Backend API bounded contexts

| Bounded context | Responsibility | Key aggregate roots |
|---|---|---|
| Identity & Access | Authenticated identity, row/column/purpose scope, policy grants | `Grant`, `AccessPolicy` |
| Manager Interaction | Routes a manager request to one fixed handler and keeps scoped conversation state | `ManagerRequest`, `ConversationSession` |
| Analysis Coordination | Creates and leases durable agent jobs; never executes them | `AgentJob` |
| Decision Governance | Decision cards, manager confirmation, follow-up contracts | `DecisionCard`, `Decision` |
| Publication & Delivery | Immutable report versions, validation receipts, export | `ReportVersion`, `ExportBatch` |
| Audit | Append-only evidence, cost, validation, and failure records | `AuditEntry` |

### Aggregates and value objects

- `AgentJob` (root): `JobId`, `JobType`, `ScopeSnapshot`, `Lease`, `Attempt[]`, `JobStatus`. Invariant: a job is claimed by at most one runner; a terminal job is immutable; wake-ups are hints and never change state.
- `Decision` (root): `DecisionCardId`, `ChosenOption`, `SuccessCriterion` (value object: target KPI, target value, measurement window 3–5 days, guardrail KPI + limit), `FollowUp[]`, `ConfirmationReceipt`. Invariant: a decision cannot be recorded without manager confirmation and a complete success criterion; the system never executes the action.
- `ReportVersion` (root): `as_reported` or `restated` state, `PublicationReceipt`, `ScopeSnapshot`, `QueryRef[]`. Invariant: published reports are immutable; a late-arrival recomputation creates a new `restated` version and never overwrites the original.
- `AccessPolicy` (root): `Grant[]` with `Scope`, `Purpose`, `Predicate` value objects. Invariant: undefined access is denied; row-level predicates are attached before any query port is called.
- `ExportBatch` (root): `OutputDir`, `FileRef[]`, `AtomicRenameReceipt`. Invariant: every path is contained in `OUTPUT_DIR`; export is atomic.

### Application use cases

`SubmitManagerQuestion`, `SubmitUpload`, `ConfirmDecision`, `RecordFollowUp`, `PublishReport`, `ExportSubmission`, `ActivateConfiguration`, `ActivateOrganizationRevision`, `StartRun`, `CloseRun`, `ReadJobStatus`, `ReadScopedReport`.

### Ports and adapters

- Ports: `IAgentJobRepository`, `IDecisionRepository`, `IReportVersionRepository`, `IAccessPolicyRepository`, `IAuditLog`, `IEvidencePort`, `IScopedQueryPort`, `IModelPort` (outbound, used only by the agent runtime through a gateway), `IClockPort`.
- Adapters: PostgreSQL repositories, `QueryGateway` + `SQL AST Guard` (scoped read-only SQL), `Evidence Service` (ACL for evidence bundles), `Submission Exporter` (filesystem adapter), `Agent Runtime Gateway` (job enqueue + best-effort wake-up), `Model Gateway` (provider ACL).
- ACLs: (1) source/ticket text and uploaded files are treated as data, never instructions; (2) LLM output is a candidate only and is validated before entering any aggregate; (3) provider API models are translated at the Model Gateway.

### Domain events

`JobCommitted`, `JobLeased`, `DecisionConfirmed`, `FollowUpDue`, `ReportValidated`, `ReportPublished`, `ReportRestated`, `ValidationRejected`, `ExportCompleted`, `ConfigurationActivated`, `OrganizationRevisionActivated`. Events are persisted with `trace_id` and consumed by application services; no direct cross-aggregate mutation.

## 2. Background Worker bounded contexts

| Bounded context | Responsibility | Key aggregate roots |
|---|---|---|
| Intake & Data Quality | Ingest drops, deduplicate, classify data issues | `IngestionBatch`, `DataIssue` |
| Snapshot & Projection | Pin versions, build reproducible facts and process projections | `Snapshot`, `Projection` |
| Semantic & KPI | Version KPI definitions, execute deterministic SQL, record lineage | `KpiDefinition`, `KpiResult` |
| Workflow & Signal | Reconstruct workflows, maintain signal lifecycles | `WorkflowObservation`, `SignalEpisode` |
| Decision Effect | Evaluate due effects and guardrails without LLM | `EffectAssessment` |
| Run Orchestration | Claim deterministic stages from stored dependencies | `RunStage` |

### Aggregates and value objects

- `IngestionBatch` (root): `SourceStatus`, `IntakeReceipt`, `DataIssue[]`. Value objects: `SourceKey`, `EventKey = (entity_id, event_type, event_time)`, `DedupKey`. Invariants: dedup by `order_id`/`ticket_id`/`lead_id`/`task_id` before any KPI; a missing source produces `null` KPIs, never `0`; a `missing` issue repeats each morning until arrival; a `late_arrival` is emitted exactly once the next morning and triggers recomputation.
- `Snapshot` (root): `PinnedVersions` (source hashes, schema, organization, policy, configuration, business date). Invariant: immutable and complete; all downstream computation reads one snapshot.
- `KpiResult` (root): `KpiId`, `Value`, `Unit`, `QueryRun` (SQL + `query_id` + result hash), `Lineage`. Invariant: value comes only from the registered SQL; parity receipt required; rounding per dictionary.
- `WorkflowObservation` (root): `WorkflowId`, `StageTiming[]`, `SlaPercent`, `Bottleneck`, `StageOwner`. Invariant: stage owner is the owner of the measuring KPI; whole-workflow owner is the Senior Manager.
- `SignalEpisode` (root): `SignalId`, `Status` (`new`/`ongoing`/`escalated`), `Owner`, `Cause[]` with confidence, `History[]`, `EscalationReason`. Invariants: only unfavorable direction per `direction` column; no re-`new` without meaningful change; escalation requires history and reason; co-cause signals group into one Senior Manager item; guardrail breach creates a signal.
- `EffectAssessment` (root): `DecisionRef`, `SuccessMetric`, `ObservedValues`, `Method` (workload normalization or comparable case), `Confounders`, `Confidence`, `EffectDirection` (`improved`/`worsened`/`too_early`/internal `not_isolatable`). Invariant: "not isolatable" is never exported as "no effect".
- `RunStage` (root): `JobId`, `Dependencies`, `StageStatus`, `Receipt`. Invariant: stages run only from stored dependencies; a failed stage is terminal for that job, not for the run.

### Domain services

`DeduplicationService`, `DataIssueClassifier`, `KpiParityService`, `RollupService`, `WorkflowReconstructionService`, `SignalDetectionService` (rules R1–R5), `EscalationPolicyService`, `DecisionEffectService`, `ReportEvidenceAssembler`.

### Ports and adapters

Ports: `ISourceAdapter`, `IFileArchive`, `IKpiQueryPort`, `IReferenceOraclePort`, `ISnapshotRepository`, `ISignalRepository`, `IRunStageRepository`, `IEventPublisher`. Adapters: versioned source parsers, PostgreSQL repositories, SQLite reference oracle (test only), in-process event publisher. ACL: every source schema is translated into canonical facts at the adapter boundary; schema drift is quarantined as a data issue.

### Domain events

`SourceIngested`, `DataIssueRaised`, `LateArrivalDetected`, `SnapshotPinned`, `KpiCalculated`, `WorkflowRebuilt`, `SignalDetected`, `SignalEscalated`, `EffectAssessed`, `GuardrailBreached`, `EvidencePackageBuilt`.

## 3. Agent Runtime bounded contexts

| Bounded context | Responsibility | Key aggregate roots |
|---|---|---|
| Job Execution | Claim leased jobs idempotently and persist candidates | `AgentJobExecution`, `Checkpoint` |
| Bounded Reasoning | Run one bounded graph per job kind; produce structured candidates only | `ReasoningSession`, `Candidate` |
| Model Access | Apply token, time, retry, cost, and budget controls | `ModelReservation`, `ModelCallReceipt` |
| Conversation | Manager-scoped, bounded history | `ConversationTurn` |

### Aggregates and value objects

- `AgentJobExecution` (root): `JobId`, `Lease`, `Attempt[]`, `GraphKind`, `TerminalState`. Invariant: one active execution per job; a lost wake-up never loses a committed job; checkpoints make retries idempotent.
- `ReasoningSession` (root): `EvidenceBundleRef`, `GraphKind`, `Candidate[]`, `TerminationReason`. Invariant: the graph is bounded to one report/interactive/document-card task; evidence is supplied by the Backend ACL; the graph cannot invent numbers or change signal status.
- `Candidate` (value object): structured narrative/decision-card proposal with `EvidenceRef[]`, never a validated report.
- `ModelReservation` (root): `BudgetWindow` (30-day $5 ceiling), `ReservedTokens`, `SettledTokens`, `Cost`, `Timeout`, `RetryPolicy` (bounded backoff). Invariant: no call without a reservation; cost uses the provider's official rate on the evaluation day; on exhaustion or failure the runtime returns an explicit no-narrative result.
- `ConversationTurn` (root): `ManagerScope`, `TurnId`, `BoundedHistoryRef`. Invariant: history is scoped to the manager and truncated to a bounded window.

### Domain services

`JobClaimingService`, `GraphSelectionService`, `BudgetSettlementService`, `RetryPolicyService`, `CandidateValidationService` (hands off to Backend Output Validator).

### Ports and adapters

Ports: `IAgentJobRepository`, `ICheckpointStore`, `IModelPort`, `IEvidencePort`, `IBudgetLedger`, `IClockPort`. Adapters: PostgreSQL job/checkpoint repositories, `Model Gateway` (provider ACL with retry/timeout), `Evidence Service` client, `Output Validator` client. ACL: provider completions are parsed into `Candidate` value objects and validated before any downstream use; prompt-injection content from documents is data.

### Domain events

`JobClaimed`, `CheckpointSaved`, `ModelCallReserved`, `ModelCallSettled`, `CandidateProduced`, `ModelCallFailed`, `JobCompleted`, `JobFailedTerminal`.

## 4. Cross-context event flow (summary)

`SourceIngested` → `DataIssueRaised` → `SnapshotPinned` → `KpiCalculated` → `WorkflowRebuilt` → `SignalDetected`/`SignalEscalated` → `EvidencePackageBuilt` → `JobCommitted` → `JobClaimed` → `CandidateProduced` → `ReportValidated` → `ReportPublished` → `ExportCompleted`. `DecisionConfirmed` → `FollowUpDue` → `EffectAssessed` → (`GuardrailBreached` → `SignalDetected`) or `ReportRestated`.

Each transition crosses a context boundary through an application service and an ACL. No aggregate is mutated directly by another context.

## 5. Quality attributes enforced by this model

- **Performance:** the worker computes KPIs in one pinned snapshot pass; the agent runtime uses bounded graphs and a single budget ledger. Target ≤5 min/day on 4 CPU / 16 GB / no GPU.
- **Scalability:** job leasing and immutable snapshots allow horizontal workers and runners without changing domain invariants; the evaluation profile runs them as processes in one image.
- **Maintainability:** new sources/KPIs/manager levels are new adapters or registry entries, not pipeline rewrites; DDD module boundaries keep changes local.
- **Testability:** domain services and value objects are pure and deterministic; parity, determinism, leakage, and cost checks are acceptance tests against domain contracts.
