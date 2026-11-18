# Deployment and operations

## Docker Compose services

DIDRAH uses Docker Compose on the reference evaluation host. The approved runtime has separate processes and containers:

1. **web** serves the React, TypeScript, and Vite application.
2. **backend-api** runs ASP.NET Core on .NET 10 LTS.
3. **background-worker** runs the .NET 10 Worker Service.
4. **scheduler-replay** runs a .NET 10 console or Worker Service process.
5. **agent-runtime** runs Python 3.12, LangGraph, and Pydantic.
6. **postgresql** runs PostgreSQL 18.

The Scheduler implementation remains open between a console process and a Worker Service. The selected implementation must keep a separate Scheduler process and container.

Docker Compose does not add a message broker, distributed cache, service mesh, or new microservice. Kubernetes is outside the approved scope.

## Network and security boundaries

Web can call only the Backend API. Web has no direct database connection. PostgreSQL and Protected File Archive are not public services. API, Worker, Scheduler, and Agent Runtime use only their required PostgreSQL permissions. Agent Runtime permissions follow ADR-0019.

## Volumes and filesystem boundaries

Compose mounts or defines:

- Read-only `DATA_DIR`
- Writable `OUTPUT_DIR`
- Protected File Archive volume
- PostgreSQL 18 data volume
- Service-specific configuration and secrets

Input data remains read-only. Submission Exporter is the only writer of contract output. It resolves and contains every target path below `OUTPUT_DIR` before an atomic write.

## Optional observability profile

The optional observability profile adds `otel-collector` as an infrastructure container. Product services send OTLP to the collector when the profile is active. The collector exports permitted agent and model telemetry to Langfuse.

Langfuse is external unless a later decision approves self-hosting. The managed or self-hosted choice remains open. OTLP/gRPC or OTLP/HTTP for backend services is a configuration decision.

Observability is fail-open. Product services continue their core work when the collector or Langfuse is unavailable. Collector queues and retries do not replace PostgreSQL durable jobs. No additional observability backend is in scope.

## Evaluation operating constraints

- Four CPU cores
- Sixteen GB RAM
- No GPU
- Network access only for approved external services
- Read-only `/data`
- Writable `/submission`
- One-command Docker Compose execution
- Dependencies installed during image build
- UTF-8 input and output
- Business timezone `Asia/Tehran`

## Operations

The system records stage duration, accepted and rejected rows, query results, KPI counts, signal changes, report results, model tokens, model cost, retries, access denials, result hashes, and artifact versions. W3C `traceparent` is propagated across REST calls. Asynchronous jobs persist trace context or use Span Links. Receipts store `trace_id` for correlation.

Failed jobs record an explicit terminal failure when the approved policy requires it. Retry count, model call timeout, Agent Job deadline, dead-letter policy, reconciliation cadence, and fallback content remain open. Documentation must not assign values to these decisions.

Retention periods, backup frequency, RPO, RTO, audit access, and the restore procedure remain open. ADR-0011 remains Proposed.
