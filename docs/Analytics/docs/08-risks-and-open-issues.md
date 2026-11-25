# Risks and open issues

The active risk and decision record is this document together with the ADR Status sections. An open issue does not change an accepted decision. A proposed value must not be recorded as `Accepted`.

## Architecture risks

| Risk | Boundary owner | Required control |
|---|---|---|
| SQLite and PostgreSQL KPI results differ | Scheduler and Replay Runner | Parity check in Acceptance Test Harness and Parity Receipt |
| Scoped query leaks rows or columns | Backend API security boundary | Query Gateway controls and negative leakage tests |
| Agent Runtime reads unrestricted business data | Backend API and PostgreSQL boundary | Restricted role and Evidence Service path |
| Source content or an upload injects instructions | Document and agent boundary | Treat content as data and validate bounded evidence |
| A lost wake-up loses accepted work | Backend API and Agent Runtime | PostgreSQL durable job and reconciliation |
| Model latency or cost exceeds the evaluation limit | Agent Runtime and Model Gateway | Bounded calls, 30-second timeout, 2 retries, cost receipt, and two-run acceptance tests |
| A data-quality issue becomes a business signal | Background Worker | Separate issue and signal contracts |
| Output is schema-valid but semantically incomplete | Backend API | Output Validator and evidence checks |
| Export escapes `OUTPUT_DIR` or leaves a partial file | Backend API | Path containment and atomic rename |
| Telemetry exposes restricted information | All instrumented services | Data minimization and telemetry leakage tests |
| Observability failure stops core work | Runtime operations | Optional fail-open collector and Langfuse path |
| Browser cache exposes data after an identity or scope change | Web Application and Backend API security boundary | Scope-keyed cache, invalidation, request cancellation, stale-response rejection, and leakage tests |
| Unsafe report, label, tooltip, or assistant content executes in the browser | Web Application | Text-first rendering, fixed local renderers, runtime validation, length limits, and production security headers |
| Frontend wire types drift from Backend responses | Backend API and Web Application | Versioned OpenAPI authority, generated TypeScript types, runtime validation, and contract-drift checks |
| An unsupported or oversized chart changes or hides validated content | Backend API and Web Application | Finite allowlist, accepted limits, explicit unavailable state, and visualization failure isolation |
| UI framework defaults replace DIDRAH identity or weaken RTL and accessibility | Web Application | Central Design System, semantic tokens, RTL tests, accessibility gates, and UX review |
| Deferred Modern code increases Classic load or creates a hardware dependency | Web Application | No first-release Three.js dependency, lazy loading, visibility-aware rendering, resource disposal, and complete Classic fallback |
| Hardcoded behavior fails on hidden data | All deterministic services | Contract-driven processing and hidden-data tests |
| Replay reads future data | Scheduler and Replay Runner | Pinned cutoff and ordered replay tests |
| Retention or restore evidence is incomplete | Operations | ADR-0011 accepted for evaluation; production retention open |

## Open decisions

| Decision | Status | Decision location |
|---|---|---|
| Evaluation packaging: single image vs Compose | Resolved for evaluation: one image, one `docker run` | ADR-0021 |
| Ad-hoc Text-to-SQL contract | Resolved | ADR-0023 |
| Scheduler as .NET Console or Worker Service | Open | ADR-0018 |
| Final restricted Agent Runtime DB role name | Open | ADR-0019 |
| Migrate from or retain `agent_query_reader` | Open | ADR-0019 |
| Python PostgreSQL driver | Open | This document |
| Langfuse managed or self-hosted | Development only; export disabled in Evaluation (closed network) | ADR-0020, ADR-0027 |
| OTLP/gRPC or OTLP/HTTP for backend services | Configuration decision | `06-deployment-and-operations.md` |
| Model and provider | Selected: `deepseek/deepseek-v4.1-flash-1017` | ADR-0022 |
| Model call timeout | Accepted: 30-second hard limit | ADR-0022 |
| Agent Job deadline | Open | This document |
| Retry count | Accepted: at most 2 retries, bounded backoff | ADR-0022 |
| Dead-letter policy | Open | This document |
| Reconciliation cadence | Open | This document |
| Model-call fallback | Resolved: valid deterministic output with no LLM narrative | ADR-0022 |
| LangGraph node boundaries | Open | This document |
| Retention and backup frequency | Open | ADR-0011 |
| RPO and RTO | Open | ADR-0011 |
| Frontend authentication product and protocol | Open | `04-security-and-trust.md`, `09-web-application-components.md` |
| Frontend credential and token storage | Open; do not select before authentication decision | `04-security-and-trust.md` |
| Access Projection Matrix entries | Open; blocks production scoped integration | `04-security-and-trust.md` |
| Exact OpenAPI Presentation wire schema and artifact path | Open; blocks production API integration | `17-chart-presentation-contract.md` |
| Initial chart-type allowlist | Open; arbitrary types forbidden | `17-chart-presentation-contract.md` |
| Chart series, point, label, and response limits | Open; silent truncation forbidden | `17-chart-presentation-contract.md` |
| Approved numeric display contract for chart labels and tooltips | Open | `17-chart-presentation-contract.md` |
| Frontend measurement profile and numeric performance budgets | Open | `07-quality-attributes.md` |
| Accessibility conformance target | Proposed WCAG 2.2 AA; not yet accepted | `18-ux-and-design-system.md` |
| Design System tokens and detailed component specifications | Open | `18-ux-and-design-system.md` |
| Modern renderer, hardware profile, asset format, and activation policy | Deferred until Classic is complete | ADR-0029 |

## Decision rules

- An open decision does not stop work that does not depend on its value.
- Documentation states the boundary without selecting an unapproved value.
- A configuration decision remains configurable until approval selects one value.
- ADR-0011 is `Accepted` for the evaluation profile; production retention, backup, audit access, restore, RPO, and RTO remain open.
- The authoritative implementation contract is `docs/15-implementation-contract.md` (ADR-0025); DDD model is `docs/16-domain-model.md` (ADR-0024).
