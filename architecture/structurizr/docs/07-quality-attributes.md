# Quality attributes

## Correctness

Published numbers come from registered deterministic queries. The system stores the SQL, result, snapshot, scope, and `query_id` for each published number. The UI, serializer, and language model do not recalculate or round a KPI.

The parity check inside the Acceptance Test Harness compares PostgreSQL results with the SQLite reference oracle. It checks row sets, nulls, values, translation semantics, timezone behavior, and date boundaries. A translation needs a Parity Receipt before acceptance. Parity is owned by the harness, not a separate component (ADR-0016 amended).

## Security

The system must prevent data leakage across the Senior Manager, Unit Manager, and Team Supervisor scopes. Authorization is applied before model use and after model output.

Leakage tests must cover row, column, resource, purpose, organization, conversation, and job scope. Tests must also prove that the restricted Agent Runtime role cannot read business tables or change database policy.

## Reproducibility

Each run uses pinned inputs and an injected business clock. An identical run must produce identical numbers and signals. Published reports are immutable.

Replay must preserve source hashes, schema versions, snapshots, configuration, query identifiers, receipts, and published report versions.

## Resilience

A missing source can reduce data completeness without stopping all publication. A model-provider failure must not stop deterministic calculation or valid canonical JSON. A manager-specific failure must not remove other valid manager reports.

A lost Agent Runtime wake-up must not lose a committed job. Collector or Langfuse failure must not stop core workflows.

## Performance and cost

The evaluation requirement is at most five minutes for each processing day and at most five US dollars for the complete 30-day run (not per day). The model is selected in ADR-0022 (`deepseek/deepseek-v4.1-flash-1017`). The model call timeout is a hard 30-second limit with at most two bounded-backoff retries; on exhaustion the report is emitted with correct numbers and no LLM narrative. Two runs of the container must produce identical numbers and signals (ADR-0026). Internal budget allocation and Agent Job deadline remain open.

The Acceptance Test Harness measures replay duration, manager-output coverage, model usage, and total cost without changing the daily product path.

## Maintainability

A new source, KPI, organization node, or manager level should use a versioned adapter, registry entry, or configuration change. It should not require a pipeline redesign.

## Auditability

Every published result must link to its evidence, query, snapshot, configuration, policy scope, validation result, and publication receipt.

Run, Job, Validation Receipt, Publication Receipt, Parity Receipt, and Export Receipt records include `trace_id` correlation metadata.

## Observability

OpenTelemetry is the common instrumentation and trace-correlation standard. REST calls propagate W3C `traceparent`. Asynchronous jobs use persisted trace context or a Span Link.

Langfuse is limited to permitted agent traces, model calls, token usage, cost, agent evaluation, and permitted prompt or model metadata. Telemetry must exclude secrets, raw restricted business data, full documents, and unauthorized manager context. Telemetry export is optional and fail-open. In the graded Evaluation profile the outbound network is closed except the LLM API, so Langfuse/OTLP export is disabled (ADR-0027); it remains available only in the development profile.

PostgreSQL stores correlation metadata and architecture receipts. It does not store full spans, traces, or general telemetry logs.

## Acceptance coverage

The Acceptance Test Harness covers:

- Ordered replay and restart behavior
- SQLite-to-PostgreSQL KPI parity
- Hidden-data and regression tests
- Cross-scope leakage tests
- Output-contract validation
- Path-containment and atomic-export checks
- Performance and cost checks
- Trace-correlation checks
