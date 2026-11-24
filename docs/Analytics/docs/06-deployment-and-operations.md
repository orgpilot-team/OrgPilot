# Deployment and operations

## Runtime services and deployment profiles

DIDRAH has two deployment profiles over the same logical containers and processes. Docker Compose is the local development and UI demonstration profile. A single image with one batch entrypoint is the graded evaluation profile (ADR-0021). The professor runs only the evaluation profile.

The approved runtime has separate processes and containers:

1. **web** serves the React, TypeScript, Vite, and Apache ECharts application.
2. **backend-api** runs ASP.NET Core on .NET 10 LTS.
3. **background-worker** runs the .NET 10 Worker Service.
4. **scheduler-replay** runs a .NET 10 console or Worker Service process.
5. **agent-runtime** runs Python 3.12, LangGraph, and Pydantic.
6. **postgresql** runs PostgreSQL 18.

The Scheduler implementation remains open between a console process and a Worker Service. The selected implementation must keep a separate Scheduler process and container.

Docker Compose does not add a message broker, distributed cache, service mesh, or new microservice. Kubernetes is outside the approved scope.

## Evaluation profile: one image, one command

The graded evaluation uses one image and one non-interactive `docker run` (ADR-0021). This supersedes Compose only for evaluation packaging. The logical C4 containers are unchanged and run as separate processes inside the image, with their own database roles and contracts. The Web Application is served only by the Compose development profile; the evaluator reads contract JSON from `OUTPUT_DIR` and does not use the web interfaces.

ECharts is a Web Application build dependency. The built Web Application contains the required chart code and does not load ECharts from a run-time CDN. The Shared Chart Presentation Library is a build dependency of Backend API and Background Worker. Neither dependency changes the evaluation output paths or requires chart rendering during the graded run.

All dependencies are installed at image build time. Nothing is installed at run time. The entrypoint reads `DATA_DIR` and `OUTPUT_DIR` from environment variables, processes drops from `day_000` through `day_090` in order, applies scripted manager input on its own day, produces the morning reports for days 62 through 91, exports them below `OUTPUT_DIR`, and exits with code zero. The PostgreSQL data directory is created fresh inside the container at run time and is not baked into the image, so both evaluator runs start from identical state.

The command given to the professor is:

```powershell
docker build -t team_x .

docker run --rm `
  --cpus=4 --memory=16g `
  -v /eval/holdout/arka_dataset:/data:ro `
  -v /eval/results/team_x:/submission `
  -e LLM_API_KEY=*** -e LLM_BASE_URL=... -e LLM_MODEL=deepseek/deepseek-v4.1-flash-1017 `
  -e DATA_DIR=/data -e OUTPUT_DIR=/submission `
  team_x
```

## LLM configuration

The evaluation profile uses `deepseek/deepseek-v4.1-flash-1017` (ADR-0022). The three variables `LLM_API_KEY`, `LLM_BASE_URL`, and `LLM_MODEL` are injected at run time and declared by name in `.env.example`. No key is stored in the project or repository. `temperature` is zero. Each model call has a hard 30-second timeout and at most two retries with bounded backoff. A model failure removes only LLM narrative and leaves deterministic canonical JSON valid. Other generation parameters remain implementation configuration.

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
- Network access only to the configured LLM API
- Read-only `/data`
- Writable `/submission`
- One-command non-interactive `docker run` execution
- Dependencies installed during image build
- UTF-8 input and output
- Business timezone `Asia/Tehran`

## Operations

The system records stage duration, accepted and rejected rows, query results, KPI counts, signal changes, report results, model tokens, model cost, retries, access denials, result hashes, and artifact versions. W3C `traceparent` is propagated across REST calls. Asynchronous jobs persist trace context or use Span Links. Receipts store `trace_id` for correlation.

Failed jobs record an explicit terminal failure when the approved policy requires it. Model-call timeout, retry, and no-narrative fallback follow ADR-0022. Agent Job deadline, dead-letter policy, and reconciliation cadence remain open implementation decisions.

ADR-0011 is accepted for the Evaluation profile. Evidence required for replay and the two-run check remains available for the duration of an evaluation run. Production retention periods, backup frequency, RPO, RTO, audit access, and the restore procedure remain open.
