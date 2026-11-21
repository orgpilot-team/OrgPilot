# 16. Domain Model (scoped DDD) for the runtime components

This document defines the tactical Domain-Driven Design model for the three runtime components that carry business complexity: **Backend API**, **Background Worker**, and **Agent Runtime**. It is the implementation contract for module boundaries, aggregate invariants, ports, and domain events. It complements the C4 component inventory in docs 10, 11, and 13; where a C4 component name appears below, it is the adapter or application service implementing the named domain role.

Status: **Accepted for implementation**.

> **Implementation source note.** This document and docs 10–13 define the component and domain boundaries used for implementation. The DSL is a visual overview of these documents. It does not define a separate implementation model.

## 0. Scoping rule (read first)

Full tactical DDD is expensive. Apply it **only where an invariant is atomic, acceptance-tested, and mutated from more than one place**. Use this test:

> If you cannot complete the sentence "this must never happen, even under concurrency," the concept is not an aggregate. It is an entity inside an aggregate, a value object, a derived read model, or an append-only record.

Consequences of the rule:

- **Aggregate** → keep a root, invariants, a repository port, and domain events.
- **Entity inside an aggregate** → keep as a child of the owning root; no separate repository or component.
- **Value object / command / DTO** → keep as an immutable type; no lifecycle, no component.
- **Derived read model** → rebuild from the source of truth; no invariant, no component.
- **Append-only record** → a repository adapter writes it; it is not a domain aggregate or a component.
- **Stateless rule or parser** → a function or module inside the owning component; no ports, no events, no view node.

A component earns its own box only if it coordinates at least one invariant-bearing entity set. This rule drives every merge and elimination in §6.

## 0.1 Shared rules

- **Modular monolith, not distributed microservices.** Bounded contexts are enforced by module boundaries and explicit application-service APIs, not by network calls. Cross-context calls go through an Anti-Corruption Layer (ACL) that translates foreign models.
- **Layering inside each context:** domain (entities, value objects, domain services, domain events) → application (use cases, ports) → infrastructure (PostgreSQL repositories, adapters, messaging). Dependencies point inward.
- **Persistence:** PostgreSQL is the single product database. Repositories are interfaces in the domain/application layer; SQL lives in infrastructure. Row-level security is enforced in the database and in every query port.
- **Determinism:** the domain clock is injected; no ambient time, randomness, or unordered iteration enters a domain decision. A domain event's payload is immutable and fully derived from pinned inputs.
- **Naming convention:** a use case is `VerbObject` (e.g. `ConfirmDecision`); a domain event is past tense (e.g. `DecisionConfirmed`).
- **One job contract.** There is a single durable-job contract for claim/lease/attempt/terminal semantics, shared by the Worker stage runner and the Agent Runtime job runner. Both consume it; neither redefines it (see §6.4).

## 1. Backend API bounded contexts

| Bounded context | Responsibility | Aggregate roots | Target components |
|---|---|---|---|
| Identity & Access | Authenticated identity, row/column/purpose scope, policy grants | `AccessPolicy` (`Grant[]`) | Authorization Service; identity validation is a function inside it |
| Manager Interaction | Route an authorized request to one fixed handler | none (routing is a function) | fixed handlers inside the owning contexts |
| Analysis Coordination | Creates and leases durable agent jobs; never executes them | `AgentJob` | Agent Runtime Gateway |
| Decision Governance | Decision cards, manager confirmation, follow-up contracts | `Decision` (includes card + follow-ups) | Decision and Follow-Up (includes card review) |
| Publication & Delivery | Immutable report versions, validation receipts, export | `ReportVersion`, `ExportBatch` | Output Validator, Publisher, Submission Exporter, Report and Dashboard API (includes job status) |
| Configuration | Versioned KPI, organization, and manager-priority configuration; approval and activation at D+1 | none (versioned candidates with state machine) | Configuration Service (single, covers KPI, organization, and manager priority) |
| Audit | Append-only evidence, cost, validation, and failure records | none (append-only) | Audit Service (repository adapter) |

### Aggregates and value objects

- `AgentJob` (root): `JobId`, `JobType`, `ScopeSnapshot`, `Lease`, `Attempt[]`, `JobStatus`. Invariant: a job is claimed by at most one runner; a terminal job is immutable; wake-ups are hints and never change state.
- `Decision` (root): `DecisionCardId`, `ChosenOption`, `SuccessCriterion` (value object: target KPI, target value, measurement window 3–5 days, guardrail KPI + limit), `FollowUp[]`, `ConfirmationReceipt`, `ReviewState`. Invariant: a decision cannot be recorded without manager confirmation and a complete success criterion; the system never executes the action. The card and its review state are entities of this root, not a separate aggregate or component.
- `ReportVersion` (root): `as_reported` or `restated` state, `PublicationReceipt`, `ScopeSnapshot`, `QueryRef[]`. Invariant: published reports are immutable; a late-arrival recomputation creates a new `restated` version and never overwrites the original.
- `AccessPolicy` (root): `Grant[]` with `Scope`, `Purpose`, `Predicate` value objects. Invariant: undefined access is denied; row-level predicates are attached before any query port is called.
- `ExportBatch` (root): `OutputDir`, `FileRef[]`, `AtomicRenameReceipt`. Invariant: every path is contained in `OUTPUT_DIR`; export is atomic.
- `ManagerRequest` is a command/value object, not an aggregate: it is validated and dispatched to one fixed handler, and carries no invariant across calls.

### Application use cases

`SubmitManagerQuestion`, `SubmitUpload`, `ConfirmDecision`, `ReviewDecisionCard`, `RecordFollowUp`, `CloseSignal`, `ReferSignal`, `SetManagerPriority`, `ChangeKpiTarget`, `ChangeKpiThreshold`, `PublishReport`, `ExportSubmission`, `ActivateConfiguration`, `ActivateOrganizationRevision`, `StartRun`, `CloseRun`, `ReadJobStatus`, `ReadScopedReport`.

`CloseSignal` and `ReferSignal` enter through Decision and Follow-Up and create an authorized disposition record. `SetManagerPriority`, `ChangeKpiTarget`, and `ChangeKpiThreshold` enter through Configuration Service and follow its validation and activation rules. Manager priority is ranking input for Signal Engine. It is not part of `KpiDefinition`.

### Ports and adapters

- Ports: `IAgentJobRepository`, `IDecisionRepository`, `IReportVersionRepository`, `IAccessPolicyRepository`, `IAuditLog`, `IEvidencePort`, `IScopedQueryPort`, `IModelPort` (outbound, used only by the agent runtime through a gateway), `IClockPort`.
- Adapters: PostgreSQL repositories, `Query Gateway` (scoped read-only SQL; the AST validator is a module inside it), `Evidence Service` (ACL for evidence bundles), `Submission Exporter` (filesystem adapter), `Agent Runtime Gateway` (job enqueue + best-effort wake-up), `Model Gateway` (provider ACL).
- ACLs: (1) source/ticket text and uploaded files are treated as data, never instructions; (2) LLM output is a candidate only and is validated before entering any aggregate; (3) provider API models are translated at the Model Gateway.
- Identity validation and request routing are functions inside Authorization Service and the owning handlers; they have no ports, events, or component box.

### Domain events

`JobCommitted`, `JobLeased`, `DecisionConfirmed`, `DecisionCardReviewed`, `FollowUpDue`, `ReportValidated`, `ReportPublished`, `ReportRestated`, `ValidationRejected`, `ExportCompleted`, `ConfigurationActivated`, `OrganizationRevisionActivated`. Events are persisted with `trace_id` and consumed by application services; no direct cross-aggregate mutation.

## 2. Background Worker bounded contexts

| Bounded context | Responsibility | Aggregate roots | Target components |
|---|---|---|---|
| Intake & Data Quality | Ingest drops, deduplicate, classify issues, normalize | `IngestionBatch` (includes `DataIssue[]`) | Ingestion Coordinator (includes source adapters, normalization, quality) |
| Snapshot & Projection | Pin versions, build reproducible facts and derived projections | `Snapshot` | Snapshot Service (includes projection as a derived read model) |
| Semantic & KPI | Version KPI definitions, translate, execute deterministic SQL | `KpiDefinition` | Semantic Registry (includes preprocessing and configuration validation) |
| Workflow & Signal | Reconstruct workflows, maintain signal lifecycles | `SignalEpisode` | Workflow Engine, Signal Engine |
| Decision Effect | Evaluate due effects and guardrails without LLM | `EffectAssessment` | Decision Effect Evaluator |
| Run Orchestration | Claim deterministic stages from stored dependencies | `RunStage` | Run Stage Coordinator |

### Aggregates and value objects

- `IngestionBatch` (root): `SourceStatus`, `IntakeReceipt`, `DataIssue[]`, canonical rows. Value objects: `SourceKey`, `EventKey = (entity_id, event_type, event_time)`, `DedupKey`. Invariants: dedup by `order_id`/`ticket_id`/`lead_id`/`task_id` before any KPI; a missing source produces `null` KPIs, never `0`; a `missing` issue repeats each morning until arrival; a `late_arrival` is emitted exactly once the next morning and triggers recomputation. `DataIssue` is an entity of this root, not a separate aggregate or component.
- `Snapshot` (root): `PinnedVersions` (source hashes, schema, organization, policy, configuration, business date). Invariant: immutable and complete; all downstream computation reads one snapshot. Projections are derived read models rebuilt from the snapshot, not aggregates.
- `KpiDefinition` (root): `KpiId`, `ReferenceSql`, `TranslatedSql`, `Unit`, `Precision`, `Target`, `Warn`, `Crit`, `EscalateAfterDays`, `Direction`, `Owner`, `Dependencies`, `Version`. Invariant: a definition becomes eligible for activation only after a passing Parity Receipt; Configuration Service controls activation state and the active-version pointer; reference SQL is read-only; the translation is a value object produced by a deterministic function inside the registry. `KpiResult` is a result record (value + `QueryRun` + lineage), not an aggregate.
- `SignalEpisode` (root): `SignalId`, `Status` (`new`/`ongoing`/`escalated`), `Owner`, `Cause[]` with confidence, `History[]`, `EscalationReason`. Manager priority is a separate versioned configuration input used during ranking. Invariants: only unfavorable direction per `direction` column; no re-`new` without meaningful change; escalation requires history and reason; co-cause signals group into one Senior Manager item; guardrail breach creates a signal.
- `EffectAssessment` (root): `DecisionRef`, `SuccessMetric`, `ObservedValues`, `Method` (workload normalization or comparable case), `Confounders`, `Confidence`, `EffectDirection` (`improved`/`worsened`/`no_change`/`too_early`/internal `not_isolatable`). Invariant: "not isolatable" is never exported as "no effect".
- `RunStage` (root): `JobId`, `Dependencies`, `StageStatus`, `Receipt`. Invariant: stages run only from stored dependencies; a failed stage is terminal for that job, not for the run.

`WorkflowObservation` is a derived read model of pinned projections, not an aggregate root; it has no invariant that is mutated from more than one place. It is produced by the Workflow Engine and consumed by the Signal Engine and Report Evidence Builder.

### Domain services

`DeduplicationService`, `DataIssueClassifier`, `KpiSqlTranslationService`, `RollupService`, `WorkflowReconstructionService`, `SignalDetectionService` (rules R1–R5), `EscalationPolicyService`, `DecisionEffectService`, `ReportEvidenceAssembler`. `KpiParityService` is not a Worker domain service; parity is owned by the Acceptance Test Harness (see §6.3).

### Ports and adapters

Ports: `ISourceAdapter`, `IFileArchive`, `IKpiQueryPort`, `IReferenceOraclePort`, `ISnapshotRepository`, `ISignalRepository`, `IRunStageRepository`, `IEventPublisher`. Adapters: versioned source parsers, PostgreSQL repositories, SQLite reference oracle (test only), in-process event publisher. ACL: every source schema is translated into canonical facts at the adapter boundary; schema drift is quarantined as a data issue.

### Domain events

`SourceIngested`, `DataIssueRaised`, `LateArrivalDetected`, `SnapshotPinned`, `KpiCalculated`, `WorkflowRebuilt`, `SignalDetected`, `SignalEscalated`, `EffectAssessed`, `GuardrailBreached`, `EvidencePackageBuilt`.

## 3. Agent Runtime bounded contexts

| Bounded context | Responsibility | Aggregate roots | Target components |
|---|---|---|---|
| Job Execution | Claim leased jobs idempotently and persist candidates | `AgentJobExecution` | Agent Job Runner |
| Bounded Reasoning | Run one bounded graph per job kind; produce structured candidates only | `ReasoningSession` | Bounded Agent Orchestrator |
| Model Access | Apply token, time, retry, cost, and budget controls | `ModelReservation` | Model Gateway |
| Conversation | Manager-scoped, bounded history | `ConversationSession` | Conversation Service |

> **Ownership fix.** `ConversationSession` and `ConversationTurn` live in the Agent Runtime, not in Backend Manager Interaction. The component and the aggregate are both here. The Backend commits the job and pins the conversation reference; the Runtime owns the history window.

### Aggregates and value objects

- `AgentJobExecution` (root): `JobId`, `Lease`, `Attempt[]`, `GraphKind`, `TerminalState`. Invariant: one active execution per job; a lost wake-up never loses a committed job. Resume state is a checkpoint record written through a repository adapter, not an aggregate and not a component.
- `ReasoningSession` (root): `EvidenceBundleRef`, `GraphKind`, `Candidate[]`, `TerminationReason`. Invariant: the graph is bounded to one report/interactive/document-card task; evidence is supplied by the Backend ACL; the graph cannot invent numbers or change signal status.
- `Candidate` (value object): structured narrative/decision-card proposal with `EvidenceRef[]`, never a validated report.
- `ModelReservation` (root): `BudgetWindow` (30-day $5 ceiling), `ReservedTokens`, `SettledTokens`, `Cost`, `Timeout`, `RetryPolicy` (bounded backoff). Invariant: no call without a reservation; cost uses the provider's official rate on the evaluation day; on exhaustion or failure the runtime returns an explicit no-narrative result. `ModelCallReceipt` is an append-only audit record, not an aggregate.
- `ConversationSession` (root): `ManagerScope`, `TurnId`, `BoundedHistoryRef`, `ConversationTurn[]`. Invariant: history is scoped to the manager and truncated to a bounded window. Turns are entities of this root.

### Domain services

`JobClaimingService`, `GraphSelectionService`, `BudgetSettlementService`, `RetryPolicyService`, `CandidateValidationService` (hands off to Backend Output Validator).

### Ports and adapters

Ports: `IAgentJobRepository`, `ICheckpointRepository`, `IModelPort`, `IEvidencePort`, `IBudgetLedger`, `IClockPort`, `IConversationRepository`. Adapters: PostgreSQL job/checkpoint/conversation repositories, `Model Gateway` (provider ACL with retry/timeout), `Evidence Service` client, `Output Validator` client. ACL: provider completions are parsed into `Candidate` value objects and validated before any downstream use; prompt-injection content from documents is data. The checkpoint store is a repository adapter behind `ICheckpointRepository`, not a domain aggregate and not a component.

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

## 6. Component consolidation decisions (implementation model)

The following merges, demotions, and eliminations are accepted for implementation. They reduce the component count without removing an invariant. The DSL is a visual overview of this model.

### 6.1 Merges

| Merge | Keeping component | Absorbed component(s) | Why it is logical |
|---|---|---|---|
| `DecisionCard` → `Decision` | Decision and Follow-Up | Decision Confirmation Service | A card and its confirm/edit/reject review state share one lifecycle and one aggregate root. Splitting them created a component that owned no invariant of its own. |
| `DataIssue` → `IngestionBatch` | Ingestion Coordinator | Data Quality Service | Issues are produced inside one atomic intake; they are entities of the batch, not a separately coordinated state. |
| Source Adapters + Normalizer → Ingestion Coordinator | Ingestion Coordinator | Source Adapters, Normalizer | Parse and normalize are deterministic functions on the same pinned input; no invariant is mutated across them. |
| Configuration Service + Organization Configuration Service | Configuration Service | Organization Configuration Service | Both manage versioned candidates with activation at D+1; org config is a candidate class, not a separate aggregate. ADR-0014 is amended. |
| KPI Definition Preprocessor + Configuration Validation Runner → Semantic Registry | Semantic Registry | KPI Definition Preprocessor, Configuration Validation Runner | Translation and validation produce one immutable definition version. The registry owns parity eligibility. Configuration Service owns activation state and the active-version pointer. |
| Snapshot Service + Projection Service | Snapshot Service | Projection Service | Projection is a derived read model of one immutable snapshot; it has no invariant mutated from more than one place. |
| Document Processing Runner + Document Parser | Document Processing Runner | Document Parser | Parsing is a bounded function over archived bytes; fragments and receipts belong to the runner's job. |
| Agent Job Status API + Report and Dashboard API | Report and Dashboard API | Agent Job Status API | Both are authorized reads of persisted state with no owned state; job status is one more read handler. |

### 6.2 Demotions (function survives, component box removed)

| Demoted | Lives inside | Why |
|---|---|---|
| `Projection` | Snapshot Service | Derived read model; rebuild from source of truth. |
| `KpiResult` | Semantic Registry / KPI Calculator | Result record with lineage; no lifecycle invariant. |
| `AuditEntry` | Audit Service repository adapter | Append-only; a port writes it, not an aggregate. |
| `ManagerRequest` | owning fixed handler | Command/value object; no cross-call invariant. |
| `ModelCallReceipt` | Model Gateway | Append-only audit record; not an aggregate. |
| SQL AST Guard | Query Gateway | Stateless validator; a module inside the gateway, not a component. |
| Identity Boundary | Authorization Service | Session validation is a function producing a trusted principal. |
| Manager Request Router | owning fixed handlers | Dispatch is a function; no owned state. |
| `Checkpoint` | `ICheckpointRepository` adapter in Agent Runtime | Resume state, not an aggregate or a component. |

### 6.3 Eliminations

| Eliminated | Replaced by | Why |
|---|---|---|
| KPI Parity Validator as a standalone component | a parity check inside Acceptance Test Harness | Parity is an acceptance test, not a product component. The harness already owns the SQLite boundary; a second owner duplicated the responsibility. `KpiParityService` is removed from the Worker domain services. |
| Duplicate durable-job runner contract | one shared job contract (§0.1) | Worker stage runner and Agent Runtime runner had parallel claim/lease/attempt semantics; one specified contract removes the drift. |

### 6.4 Build-team ownership boundaries

These are the seams the build team implements against. Each row is one owner; cross-row calls go through the named port/API, never by reaching into another module's state.

| Owner | Owns (invariants) | Exposes | Must not |
|---|---|---|---|
| Authorization Service | `AccessPolicy`, `Grant`, scope/purpose/predicate | trusted scope to handlers and query ports | widen scope, execute work |
| Agent Runtime Gateway | `AgentJob` creation and wake-up | committed `job_id` | run graphs, carry evidence |
| Decision and Follow-Up | `Decision` (card, review, follow-ups), authorized signal dispositions | confirm/review/close/refer commands | execute the decision, auto-confirm, change signal rules |
| Configuration Service | versioned KPI, organization, and manager-priority candidates; approval, schedule, activation state, active-version pointer | active version reference to Snapshot | translate KPI SQL, issue a Parity Receipt, activate invalid candidates, use same-day org activation |
| Output Validator / Publisher / Submission Exporter | `ReportVersion`, `ExportBatch` | validated, published, exported artifacts | generate content, mutate old versions, escape `OUTPUT_DIR` |
| Report and Dashboard API | authorized reads (reports, dashboards, job status) | bounded responses | bypass scope, read arbitrary tables |
| Ingestion Coordinator | `IngestionBatch`, `DataIssue[]`, canonical rows | committed batch | interpret business meaning before normalization, calculate KPIs |
| Snapshot Service | `Snapshot`, derived projections | one pinned snapshot | mix unpinned versions, mutate source history |
| Semantic Registry | immutable `KpiDefinition` versions, translation, semantic validation, parity eligibility | eligible definition + SQL | control activation state, execute unregistered SQL, change reference SQL |
| Workflow Engine / Signal Engine | `SignalEpisode`, workflow read models | signals with owner + history | generate model content, auto-create decisions |
| Decision Effect Evaluator | `EffectAssessment` | internal effect record | claim causality without evidence |
| Run Stage Coordinator | `RunStage` | stage results | create ad hoc work, publish |
| Agent Job Runner | `AgentJobExecution`, lease/attempt | candidate or terminal failure | execute unclaimed jobs, publish |
| Bounded Agent Orchestrator | `ReasoningSession`, `Candidate[]` | structured candidate | invent numbers, change signal status |
| Model Gateway | `ModelReservation`, cost settlement | completion or explicit failure | bypass limits, treat completion as validated output |
| Conversation Service | `ConversationSession`, `ConversationTurn[]` | bounded history | treat chat as business evidence, cross manager scope |
| Acceptance Test Harness | parity, replay, regression, leakage, contract checks | receipts | act as product runtime, publish output |

The shared durable-job contract (claim/lease/attempt/terminal) is owned jointly by the Backend `AgentJob` aggregate and the Runtime `AgentJobExecution` aggregate through one specified interface; both runners consume it and neither redefines it.
