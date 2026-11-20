# Agent Runtime components

## Purpose and Scope

The Agent Runtime claims durable Agent Jobs from PostgreSQL and runs bounded LangGraph graphs. It produces structured candidates only. It does not own product truth.

## Runtime Technology

Python 3.12, LangGraph, Pydantic, and a PostgreSQL driver that remains an open decision.

## Trust Boundary

The Runtime has limited database access to Agent Job, Lease, Attempt, Checkpoint, Conversation, Candidate, and job-scoped Evidence views. It gets business evidence through Backend services.

## Allowed Responsibilities

- Claim leased Agent Jobs and persist candidate or terminal failure state.
- Run bounded report, interactive, or document decision-card graphs.
- Apply model limits and store resumable checkpoints and scoped conversation turns.

## Forbidden Responsibilities

- Run arbitrary SQL against business tables.
- Calculate KPIs, change policy, run migrations, publish results, or confirm decisions.
- Treat wake-ups as durable jobs.

> **Target model note.** This document describes the **target component set** after the DDD consolidation in `16-domain-model.md` §6. `workspace.dsl` still shows the pre-consolidation inventory; it will be synchronized in the next phase. DDD rigour here is limited to the four aggregates in doc 16 §3; checkpoint state is a repository adapter, not a component.

## Component Map (target)

Agent Job Runner claims work and invokes Bounded Agent Orchestrator. The orchestrator uses Conversation Service and Model Gateway. Checkpoint persistence is a repository adapter (`ICheckpointRepository`) behind the Runner and Orchestrator, not a component.

Removed as a component: PostgreSQL Checkpoint Store (demoted to a repository adapter; `Checkpoint` is resume state, not an aggregate).

## Internal Relationships

The Runner invokes one bounded graph. The graph uses the model through Model Gateway and persists checkpoints and conversation turns through repository adapters. `ConversationSession`/`ConversationTurn` are owned here, in the Conversation Service, not in the Backend Manager Interaction context.

## External Relationships

The Runtime claims from PostgreSQL, gets evidence and validation from the Backend API, calls the Language Model Provider, and can send redacted telemetry to the optional Collector.

## Component Sections

<a id="bounded-agent-orchestrator"></a>

### Bounded Agent Orchestrator

- **DSL identifier:** `agentOrchestrator`; **Display name:** Bounded Agent Orchestrator.
- **Purpose:** Coordinate one bounded report, interactive, or decision-card graph. **Responsibilities:** Load authorized evidence, manage bounded steps, use conversation context, request model work, and return structured candidates. **Inputs:** Claimed job, scope, evidence references, and graph configuration. **Outputs:** Structured candidate or terminal graph failure.
- **Owned state:** Graph state through checkpoint records written via `ICheckpointRepository`. **Dependencies:** Evidence Service, Conversation Service, Model Gateway, and the checkpoint repository adapter. **Security boundary:** Job scope and evidence references bound every graph. **Forbidden responsibilities:** Direct business SQL, KPI calculation, publication, or decision confirmation.
- **Failure behavior:** Persist a bounded failure and resumable checkpoint where allowed. **Idempotency:** Job attempt and checkpoint state control replay. **Observability:** Record graph, node, job, attempt, model calls, and trace ID with redaction. **Related ADRs:** ADR-0005, ADR-0008, ADR-0019, ADR-0020. **Open issues:** LangGraph node boundaries remain open.

<a id="agent-job-runner"></a>

### Agent Job Runner

- **DSL identifier:** `agentJobRunner`; **Display name:** Agent Job Runner.
- **Purpose:** Claim leased jobs and persist a candidate or terminal failure. **Responsibilities:** Poll or accept a hint, claim a job, invoke the graph, validate the persisted outcome through Backend, and settle the attempt. **Inputs:** PostgreSQL Ready job or authenticated job-ID wake-up. **Outputs:** Persisted candidate, terminal failure, attempt, and validation request.
- **Owned state:** Job lease, attempt, and candidate state in PostgreSQL. **Dependencies:** PostgreSQL, Bounded Agent Orchestrator, and Backend Output Validator. **Security boundary:** A wake-up is a hint and grants no scope. **Forbidden responsibilities:** Execute an unclaimed job, carry evidence in a wake-up, or publish.
- **Failure behavior:** Persist attempt failure and allow lease recovery under policy. **Idempotency:** Claim and lease rules prevent concurrent execution. **Observability:** Record job, lease, attempt, outcome, and linked trace context. **Related ADRs:** ADR-0008, ADR-0011, ADR-0019, ADR-0020. **Open issues:** Deadline, retry count, dead-letter policy, and reconciliation cadence remain open.

<a id="conversation-service"></a>

### Conversation Service

- **DSL identifier:** `conversationService`; **Display name:** Conversation Service.
- **Purpose:** Store manager-scoped sessions and validated turns. **Responsibilities:** Append validated turns and return a bounded authorized history window. **Inputs:** Manager scope, session ID, validated turn, and history limit. **Outputs:** Stored turn receipt and bounded history.
- **Owned state:** `ConversationSession` aggregate with `ConversationTurn[]` entities in PostgreSQL. **Dependencies:** PostgreSQL. **Security boundary:** Sessions are manager-scoped and contain only validated content; history is truncated to a bounded window. This component owns conversation state; the Backend commits the job and pins the conversation reference but does not own the history. **Forbidden responsibilities:** Treat chat as business evidence or cross manager scope.
- **Failure behavior:** Return explicit storage or scope failure and omit unvalidated turns. **Idempotency:** Turn ID prevents duplicate append. **Observability:** Record session, turn ID, result, window size, and trace ID without full content. **Related ADRs:** ADR-0005, ADR-0008, ADR-0011, ADR-0019. **Open issues:** Retention remains open.

<a id="model-gateway"></a>

### Model Gateway

- **DSL identifier:** `agentModelGateway`; **Display name:** Model Gateway.
- **Purpose:** Apply token, time, retry, and cost limits to every model call. **Responsibilities:** Reserve budget, redact and send bounded input, call the provider, settle cost, and return completion or failure. **Inputs:** Authorized prompt, evidence subset, model policy, and budget. **Outputs:** Completion metadata and content or explicit failure.
- **Owned state:** Cost reservation and settlement metadata in PostgreSQL. **Dependencies:** PostgreSQL and Language Model Provider. **Security boundary:** Do not send secrets, full documents, or unauthorized business context. **Forbidden responsibilities:** Select unapproved scope, bypass limits, or treat a completion as validated product output.
- **Failure behavior:** Return bounded timeout, budget, provider, or validation failure. **Idempotency:** Call ID and reservation state prevent duplicate settlement. **Observability:** Record model metadata, tokens, cost, latency, status, and trace ID with redaction. **Related ADRs:** ADR-0008, ADR-0019, ADR-0020, ADR-0022. **Open issues:** Timeout and retry count are provisional defaults and are tuned in implementation. The evaluation model is `deepseek/deepseek-v4.1-flash-1017` with temperature zero; `LLM_API_KEY`, `LLM_BASE_URL`, and `LLM_MODEL` are injected at run time (ADR-0022). For ad-hoc SQL generation, the model names only approved semantic views and never supplies a number (ADR-0023).

## Consolidation log (target model)

The following component from the current DSL inventory is intentionally absent here. See `16-domain-model.md` §6 for the reasoning.

| Removed component | Disposition |
|---|---|
| PostgreSQL Checkpoint Store | Demoted to `ICheckpointRepository` adapter; `Checkpoint` is resume state, not an aggregate or a component |

`ModelCallReceipt` is likewise an append-only audit record inside Model Gateway, not an aggregate or a component. The job claim/lease/attempt contract is shared with the Worker stage runner through one specified durable-job contract (doc 16 §0.1), so the two runners do not duplicate that semantics.

## Container-level Open Issues

- Python PostgreSQL driver, Agent Job deadline, dead-letter policy, reconciliation cadence, fallback content, and LangGraph node boundaries remain open. The model/provider is selected in ADR-0022; timeout and retry count are provisional defaults.
