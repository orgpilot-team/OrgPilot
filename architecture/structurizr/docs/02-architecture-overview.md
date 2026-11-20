# Architecture overview

DIDRAH uses a modular monolith. The Backend API, Background Worker, and Scheduler and Replay Runner use shared .NET libraries. They run as separate processes and containers. The Web Application and Agent Runtime also run in separate containers. Docker Compose defines the local development deployment; the graded evaluation packages all logical containers as separate processes inside one image started with one `docker run` (ADR-0021). The logical C4 model is unchanged in both profiles.

The architecture has seven product containers:

1. **Web Application** provides the Persian right-to-left user interface.
2. **Backend API** authenticates requests, applies access rules, controls bounded analysis, validates results, and delivers reports.
3. **Background Worker** runs deterministic ingestion, snapshot, KPI, workflow, signal, and report-evidence jobs.
4. **Scheduler and Replay Runner** controls simulated time, replay, and acceptance tests.
5. **PostgreSQL** stores product state, analytical results, jobs, access policy, checkpoints, and audit records.
6. **Protected File Archive** stores original source files and manager uploads with their hashes and manifests.
7. **Agent Runtime** claims durable jobs and produces bounded narrative or decision-card candidates.

The system uses these external dependencies:

- DIDRAH Input Dataset
- Submission Output Directory
- Identity Provider
- Language Model Provider
- Langfuse

The optional OpenTelemetry Collector is an infrastructure container. It is not a Product Component. Product workflows continue when the collector or Langfuse is unavailable.

The DIDRAH Input Dataset is one versioned `DATA_DIR` package. It contains nightly drops, manifests, manager inputs, uploads, configuration, and history. Development and hidden evaluation datasets use the same structure.

The deterministic core is outside the agent. It owns KPI calculation, workflow reconstruction, signal rules, authorization, validation, and publication. The bounded agent analyzes only authorized evidence and can produce a narrative candidate or a decision-card candidate.

**Component consolidation (target model).** The component inventory in docs 10–13 and the DDD model in doc 16 define a consolidated target set: stateless helpers (identity validation, request routing, SQL AST guard, simulation clock, evaluation profile loader, document parser, source adapters, normalizer, data-quality service, projection service, KPI preprocessor, configuration validation runner) are folded into their owning components; Decision Confirmation Service, Organization Configuration Service, Agent Job Status API, and KPI Parity Validator are merged into their natural owners; the Checkpoint Store is demoted to a repository adapter. The DSL and generated views still show the pre-consolidation inventory and will be synchronized in the next phase. No invariant is removed. See doc 16 §6 for the per-component reasoning.

## Technology matrix

| Element | Technology | Constraint |
|---|---|---|
| Web Application | React, TypeScript, Vite | No business calculation |
| Backend API | ASP.NET Core on .NET 10 LTS | Modular monolith process |
| Background Worker | .NET 10 Worker Service | Deterministic processing |
| Scheduler and Replay Runner | .NET 10 console or Worker Service | The implementation choice is open |
| Agent Runtime | Python 3.12, LangGraph, Pydantic | Candidate generation only |
| Product Database | PostgreSQL 18 | The only product database |
| SQLite | Embedded in Acceptance Test Harness | Reference oracle only |
| Normal .NET data access | EF Core and Npgsql | CRUD and normal transactions |
| Direct .NET SQL | Npgsql | Job claims and approved KPI SQL only |
| API | REST/JSON and OpenAPI | W3C `traceparent` propagation |
| Deployment | Compose (development); single image + one `docker run` (evaluation) | Separate processes and containers; ADR-0021 |
| Tracing | OpenTelemetry SDK and OTLP | Optional and fail-open export |
| Agent observability | Langfuse | Optional and fail-open |

Shared .NET libraries can contain:

- Domain and application contracts
- PostgreSQL persistence primitives
- OpenAPI DTOs
- Authorization primitives
- Job-state contracts
- Output-validation interfaces
- Observability conventions

A shared library does not give shared ownership of data. It does not make separate runtime processes an in-process deployment.

## API and process contracts

The Web Application calls the Backend API through HTTPS REST/JSON. The Backend API is the identity, authorization, evidence, validation, publication, and export boundary. The Background Worker owns deterministic daily processing. The Scheduler and Replay Runner owns time, replay, acceptance, and parity work. The Agent Runtime owns bounded graph execution and agent-owned job state.

All report, interactive, and document-analysis Agent Jobs use one durable PostgreSQL queue. The Backend producer commits an idempotent job with pinned actor, scope, policy, and input references before sending an optional authenticated wake-up containing only the job ID. The Agent Runtime Runner claims and leases the canonical job from PostgreSQL, executes it, and persists its outcome. A missed wake-up cannot lose work; polling and lease recovery remain authoritative. The Backend validates persisted outcomes and exposes authorized job status/results to the Web Application. The Agent Runtime Gateway produces interactive jobs; the Document Processing Runner produces document jobs only after a successful parse; an edit revision is created by the producer for that workload type.

The main nightly path is:

```text
Scheduler and Replay Runner
  -> Backend Run Coordinator
  -> PostgreSQL job plan
  -> Background Worker stages
  -> manager-scoped Evidence Package and Canonical Report JSON
  -> PostgreSQL unlocks the pinned Agent Job
  -> Agent Runtime Runner claims, executes, and persists outcome
  -> deterministic validation
  -> independent publication
```
