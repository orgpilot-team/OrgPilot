# 20. Use OpenTelemetry and Langfuse for observability

Date: 2026-11-19

## Status

Accepted

## Context

DIDRAH needs trace correlation across synchronous REST calls, asynchronous jobs, validation, publication, parity checks, and exports. Agent and model activity also needs bounded cost and evaluation visibility. Observability must not become a dependency of the core workflow or a new store for restricted business data.

## Decision

OpenTelemetry is the common instrumentation and trace-correlation standard.

- The Web Application uses the OpenTelemetry JavaScript SDK.
- The Backend API, Background Worker, and Scheduler and Replay Runner use the OpenTelemetry .NET SDK.
- The Agent Runtime uses OpenTelemetry Python instrumentation.
- REST calls propagate W3C `traceparent`.
- Asynchronous jobs use a Span Link or persisted trace context.
- Run, Job, Validation Receipt, Publication Receipt, Parity Receipt, and Export Receipt records include `trace_id` correlation metadata.

An optional `otel-collector` Docker Compose service receives OTLP telemetry and exports permitted telemetry to Langfuse in the **development profile only**. In the graded Evaluation profile, outbound network is closed except the LLM API (ADR-0027): the collector is loopback-only or disabled and no Langfuse export is attempted. Product services use fail-open behavior when the collector or Langfuse is unavailable. Collector queues and retries do not replace PostgreSQL job durability.

Langfuse is the only approved agent-observability backend. It can receive agent traces, model calls, token usage, cost, agent evaluation, and permitted prompt or model metadata. It must not receive secrets, raw restricted business data, full documents, or unauthorized manager context.

PostgreSQL stores correlation metadata and architecture receipts. It does not store full traces, spans, or general telemetry logs.

## Alternatives rejected

- A workflow dependency on Langfuse is rejected because observability must be fail-open.
- Full telemetry storage in the product PostgreSQL database is rejected because it mixes operational telemetry with product state.
- Grafana, Tempo, Jaeger, Prometheus, Loki, Datadog, and other observability backends are rejected because they are outside the approved scope.

## Consequences

The system has one trace-correlation standard across all runtime technologies. Agent cost and model activity can be inspected without changing the deterministic record. Telemetry export can fail without stopping core processing. Data minimization rules must be tested at each instrumentation boundary.

## Security impact

Instrumentation must remove or mask secrets, restricted business data, full documents, and unauthorized manager context. Access to Langfuse must follow the approved manager and operator boundaries. Telemetry configuration must not widen product-data access.

## Operational impact

The collector is an optional Compose infrastructure container. Operators must monitor export failures separately from product-job failures. Product services must continue when the collector or Langfuse is unavailable.

## Related requirements

- REST and asynchronous work must have end-to-end trace correlation.
- Receipts must include trace correlation without storing full telemetry in PostgreSQL.
- Observability failure must not stop deterministic processing, validation, publication, or export.

## Related model elements

- Web Application
- Backend API
- Background Worker
- Scheduler and Replay Runner
- Agent Runtime
- OpenTelemetry Collector
- Langfuse
- PostgreSQL receipts

## Open decisions

- Langfuse managed hosting or self-hosting is open.
- OTLP/gRPC or OTLP/HTTP for backend services is a configuration decision. This ADR does not select one.
