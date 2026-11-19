# 27. Evaluation network egress: LLM API only

Date: 2026-11-19

## Status

Accepted

## Context

The TA fixes the evaluation network: only the language-model API is reachable; all other internet egress is closed. ADR-0020 introduced optional OTLP export to Langfuse, and the DSL still contains an "External Observability Egress" deployment node. If an implementation treats that export as required, startup delays or failures can break the 5-minute/day budget or the zero exit code.

## Decision

In the **Evaluation** deployment profile:

- The only permitted outbound endpoint is the configured LLM API (`LLM_BASE_URL`).
- OTLP collector and Langfuse export are **disabled**; the collector may run only as a loopback, fail-open process and must not attempt external connections.
- Telemetry is optional and fail-open everywhere; core workflows, validation, publication, and export never depend on it.
- Langfuse remains available only in the development/Compose profile, which is not used by the grader.

## Consequences

- The evaluation image has no external dependency besides the LLM provider.
- Observability is preserved in development without risking graded runs.
- The DSL deployment description and ADR-0020 are updated to state this profile constraint.

## Related

- ADR-0020 (OpenTelemetry and Langfuse), ADR-0021 (single-image entrypoint), ADR-0022 (LLM provider), `docs/15-implementation-contract.md` §2
