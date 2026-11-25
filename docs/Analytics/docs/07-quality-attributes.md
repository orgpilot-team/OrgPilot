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

The five-minute daily Evaluation limit does not define Web Application performance. The graded Evaluation does not execute the Web Application.

## Frontend quality attributes

Frontend quality applies to the complete Classic experience. Numeric load, navigation, chart-rendering, and memory budgets remain open until the team approves a measurement profile for ordinary office hardware, browser, network, viewport, and data size. Proposed values must not be recorded as measured results.

| Attribute | Required quality rule |
|---|---|
| Initial application load | Classic Mode does not load Three.js, 3D models, or Modern-only assets. Core fonts, icons, and required runtime assets do not depend on a runtime CDN. Measure transferred assets and time to usable content on the approved profile. |
| Navigation responsiveness | Show immediate pending feedback. Cancel old requests when possible. Ignore responses from an old session or scope. Preserve keyboard focus or move it to a documented destination. |
| Chart rendering | Validate the response before mapping. Test each supported chart type with the largest permitted series and point limits. A slow or failed chart does not block validated content. |
| Memory | Caches are bounded. Repeated route entry and exit must not retain ECharts instances, React Flow listeners, observers, subscriptions, or abandoned responses. |
| CPU and GPU | Classic Mode has no continuous render loop. Nonessential animation stops when content is hidden. Reduced-motion preferences are respected. |
| Resource disposal | Dispose ECharts instances, resize observers, subscriptions, timers, event listeners, animation controls, and future renderer resources when their owner unmounts or changes. |
| Responsive layout | Test an approved viewport matrix. A responsive change must not remove required information or actions or change business meaning. The exact matrix remains open. |
| Accessibility | Keyboard operation, visible focus, screen-reader names, non-color status cues, reduced motion, accessible errors, and text or table alternatives for charts are required. WCAG 2.2 AA is proposed in doc 18; final acceptance remains open. |
| Persian and RTL | Test Persian-first layouts, mixed-direction content, technical identifiers, numbers, long labels, truncation, and zoom. The UI does not round an authoritative KPI independently. |
| Failure isolation | A visualization error boundary isolates chart or workflow rendering failures. Validated report, answer, and allowed actions remain available. |
| Scope isolation | Cache and pending-request tests prove that identity or scope changes cannot display data from the previous principal or scope. |

Frontend quality tests must cover loading, empty, unavailable, forbidden, incomplete, validation-failed, and service-failed states. These states must not be merged into one generic empty state.

Mock-based Design System, RTL, layout, interaction, accessibility, and UX work can start before production API and authentication contracts are complete. Production contract tests, session tests, scope-isolation tests, and security-sensitive command tests wait for their owning decisions.

## Future Modern quality attributes

Modern Mode remains deferred. When approved, it must add these gates without weakening Classic Mode:

- Renderer and assets are lazy-loaded only for a selected Modern area.
- Rendering starts only when required and stops when the scene is hidden or inactive.
- A configurable initial 30 FPS target applies only to active 3D rendering.
- The target is measured with an approved profile for ordinary office hardware and browsers.
- Scene, texture, geometry, material, listener, and GPU resources are disposed.
- Unsupported hardware, browser failure, renderer failure, or asset failure returns the complete Classic experience.
- Modern code and assets are absent from the Classic initial-load path.

The 30 FPS value is a proposed target, not a measured result and not a target for React, ECharts, or Motion.

## Maintainability

A new source, KPI, organization node, or manager level should use a versioned adapter, registry entry, or configuration change. It should not require a pipeline redesign.

Backend chart contracts remain independent of ECharts. A renderer change does not change pinned chart values, lineage, authorization, or Submission schemas.

Frontend API types are generated from the versioned Backend OpenAPI contract. A build or CI check must detect contract-generation drift. Renderer-neutral types do not import frontend rendering libraries.

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
