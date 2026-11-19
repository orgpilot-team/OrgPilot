# 26. Deterministic double-run contract

Date: 2026-11-19

## Status

Accepted

## Context

The TA states that every container is executed twice and that a difference in numbers or discovered signals between the two runs reduces the score. The LLM is non-deterministic in general, and ambient time, unordered collections, or random sampling can silently change results. Numbers come from SQL (ADR-0002), but signal status and grouping are also graded for cross-run equality.

## Decision

Determinism is an acceptance gate, not a tuning goal:

- Product time comes from the injected simulation clock only; the host clock is never used as business time.
- All inputs are pinned by hash and version (source drops, KPI dictionary, organization, policy, configuration, event calendar).
- Iteration order that affects output is explicitly sorted by stable keys. No random sampling in detection, ranking, or grouping.
- LLM output never supplies a number, a signal status, or an owner. It supplies narrative candidates only, with `temperature = 0`.
- Retry and timeout are bounded; a failed model call yields the same deterministic no-narrative report on both runs.
- The Acceptance Test Harness executes the full replay twice and compares: KPI values, `data_issues`, signal IDs/statuses/owners, and all exported JSON. Any difference fails acceptance.

## Consequences

- Implementations must avoid ambient state and unstable ordering; code review checks these explicitly.
- Cost and latency remain bounded because retries cannot loop indefinitely.
- Two-run equality is verified automatically before Demo Day.

## Related

- ADR-0006 (deterministic signal lifecycle), ADR-0011 (replay evidence), ADR-0016 (parity), ADR-0022 (model configuration), `docs/15-implementation-contract.md` §2
