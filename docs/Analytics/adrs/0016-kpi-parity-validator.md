# 16. KPI Parity Validator

Date: 2026-11-17

## Status

Accepted

## Context

The architecture has KPI Calculator and Acceptance Test Harness, but parity between SQLite reference SQL and PostgreSQL translated SQL needs an executable contract. SQLite is not a product database or a runtime container. It is embedded only in the Acceptance Test Harness.

- A component in Replayer should convert SQLite SQL to PostgreSQL
- Only two functions differ: `median()` → `percentile_cont(0.5)` and date difference calculations
- Initial tests show results are correct with <1% difference

## Decision

Add `KPI Parity Validator` component in Scheduler/Replay Runner as part of the Acceptance Test Harness. The harness owns the SQLite execution boundary.

Tasks:

1. Execute 55 reference SQL on SQLite
2. Execute translated PostgreSQL SQL on equivalent snapshot
3. Compare row sets
4. Compare nulls
5. Compare values within ±1% tolerance
6. Assert `median()` maps to `percentile_cont(0.5)` and **reject `percentile_disc`**
7. Assert `julianday(b)-julianday(a)` (days) maps to `EXTRACT(EPOCH FROM b-a)/86400` with explicit conversion to the KPI unit (hours or days)
8. Assert percentages use `100.0 *` to avoid integer division
9. Assert timezone (`Asia/Tehran`), date type, and per-KPI rounding from the dictionary; ±1% is the accepted evaluation tolerance, while brief "zero tolerance" applies only to text-to-JSON number matching
10. Produce Parity Receipt per KPI

Important: Agent Runtime has NO role in parity. If KPI is wrong, Agent must not fix or reinterpret it.

## Consequences

- Parity is an executable contract, not just a concept
- Part of Acceptance Harness, not daily product
- SQLite exists only inside the Acceptance Test Harness
- Deterministic validation with receipts
- Agent completely excluded from parity

## Amendment (2026-11-20)

The standalone `KPI Parity Validator` component is **folded into the `Acceptance Test Harness`**. Every task and requirement in this ADR remains in force; only the component boundary changes. The harness already owns the SQLite execution boundary, so a separate parity component duplicated that ownership. Parity is one acceptance check inside the harness, not a product component, and `KpiParityService` is removed from the Worker domain services.

- `docs/12-scheduler-replay-components.md` and `docs/16-domain-model.md` §6.3 define the implementation boundary. The DSL is a visual overview of those documents.

## Related requirements

- The Acceptance Test Harness must execute the read-only SQLite reference SQL.
- The translated PostgreSQL SQL must run against an equivalent snapshot.
- Parity evidence must exist before a translated KPI definition is accepted.
