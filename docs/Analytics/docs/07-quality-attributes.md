# Quality attributes

## Correctness

Published numbers come from registered deterministic queries. The system stores the SQL, result, snapshot, scope, and `query_id` for each published number. The UI, serializer, and language model do not recalculate or round a KPI.

Every chart point comes from pinned report evidence or a validated bounded query result. The same pinned input, validated `ChartIntent`, chart-policy version, and chart-contract version produce the same ordered `ChartSpec`. The Web Application does not regroup, interpolate, or correct chart data.

The parity check inside the Acceptance Test Harness compares PostgreSQL results with the SQLite reference oracle. It checks row sets, nulls, values, translation semantics, timezone behavior, and date boundaries. A translation needs a Parity Receipt before acceptance. Parity is owned by the harness, not a separate component (ADR-0016 amended).

## Security

The system must prevent data leakage across the Senior Manager, Unit Manager, and Team Supervisor scopes. Authorization is applied before model use and after model output.

Leakage tests must cover row, column, resource, purpose, organization, conversation, and job scope. Tests must also prove that the restricted Agent Runtime role cannot read business tables or change database policy.

Chart tests must prove that `ChartSpec` contains no cross-scope series, unrestricted raw rows, executable content, or values without approved query lineage.

## Reproducibility

Each run uses pinned inputs and an injected business clock. An identical run must produce identical numbers and signals. Published reports are immutable.

Replay must preserve source hashes, schema versions, snapshots, configuration, query identifiers, receipts, and published report versions.

## Resilience

A missing source can reduce data completeness without stopping all publication. A model-provider failure must not stop deterministic calculation or valid canonical JSON. A manager-specific failure must not remove other valid manager reports.

A chart-construction or ECharts-rendering failure must not change validated content or block formal Submission export. The UI shows an explicit chart-unavailable state.

A lost Agent Runtime wake-up must not lose a committed job. Collector or Langfuse failure must not stop core workflows.

## Performance and cost

The evaluation requirement is at most five minutes for each processing day and at most five US dollars for the complete 30-day run (not per day). The model is selected in ADR-0022 (`deepseek/deepseek-v4.1-flash-1017`). The model call timeout is a hard 30-second limit with at most two bounded-backoff retries; on exhaustion the report is emitted with correct numbers and no LLM narrative. Two runs of the container must produce identical numbers and signals (ADR-0026). Internal budget allocation and Agent Job deadline remain open.

The Acceptance Test Harness measures replay duration, manager-output coverage, model usage, and total cost without changing the daily product path.

## Maintainability

A new source, KPI, organization node, or manager level should use a versioned adapter, registry entry, or configuration change. It should not require a pipeline redesign.

Backend chart contracts remain independent of ECharts. A renderer change does not change pinned chart values, lineage, authorization, or Submission schemas.

## Auditability

Every published result must link to its evidence, query, snapshot, configuration, policy scope, validation result, and publication receipt.

Run, Job, Validation Receipt, Publication Receipt, Parity Receipt, and Export Receipt records include `trace_id` correlation metadata.

## Observability

OpenTelemetry is the common instrumentation and trace-correlation standard. REST calls propagate W3C `traceparent`. Asynchronous jobs use persisted trace context or a Span Link.

Langfuse is limited to permitted agent traces, model calls, token usage, cost, agent evaluation, and permitted prompt or model metadata. Telemetry must exclude secrets, raw restricted business data, full documents, and unauthorized manager context. Telemetry export is optional and fail-open. In the graded Evaluation profile the outbound network is closed except the LLM API, so Langfuse/OTLP export is disabled (ADR-0027); it remains available only in the development profile.

PostgreSQL stores correlation metadata and architecture receipts. It does not store full spans, traces, or general telemetry logs.

## Acceptance coverage

The Acceptance Test Harness covers:

- Ordered replay, restart behavior, and an organization change during replay without a code change.
- SQLite-to-PostgreSQL KPI parity, zero incorrect published numbers, hidden-data tests, and regression tests.
- Ten morning reports before 07:30, with no more than five items in each report.
- At least 90% of required signals detected within 24 hours, with the correct owner and cause.
- All three workflows reconstructed with SLA and bottleneck results.
- At least 85% acceptance accuracy for scoped manager questions.
- Zero cross-scope leakage and explicit prompt-injection tests for ticket, file, and upload text.
- Fairness checks that prevent unsupported individual blame and restrict individual data to an approved direct-supervisor workload purpose.
- Q03 checks for the `U_SAL` monthly target, net revenue through yesterday, and proportional target attainment.
- Output-contract validation, path containment, atomic export, and trace correlation.
- At most five minutes per processing day and at most five US dollars for the complete 30-day run.
- Equal numbers and discovered signals in two runs with the same inputs.
