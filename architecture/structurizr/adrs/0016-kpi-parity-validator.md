# 16. KPI Parity Validator

Date: 2026-11-17

## Status

Accepted

## Context

The architecture has KPI Calculator and Acceptance Test Harness, but parity between SQLite reference SQL and PostgreSQL translated SQL needs an executable contract. The user notes:

- A component in Replayer should convert SQLite SQL to PostgreSQL
- Only two functions differ: `median()` → `percentile_cont(0.5)` and date difference calculations
- Initial tests show results are correct with <1% difference

## Decision

Add `KPI Parity Validator` component in Scheduler/Replay Runner (part of Acceptance Test Harness).

Tasks:

1. Execute 55 reference SQL on SQLite
2. Execute translated PostgreSQL SQL on equivalent snapshot
3. Compare row sets
4. Compare nulls
5. Compare values within ±1% tolerance
6. Control `median` vs `percentile_cont`
7. Control time interval calculations
8. Control decimal division
9. Control timezone and date boundaries
10. Produce Parity Receipt per KPI

Important: Agent Runtime has NO role in parity. If KPI is wrong, Agent must not fix or reinterpret it.

## Consequences

- Parity is an executable contract, not just a concept
- Part of Acceptance Harness, not daily product
- Deterministic validation with receipts
- Agent completely excluded from parity

## Source

Addresses Gap 5 from architectural review: "Parity واقعی SQLite و PostgreSQL"
User's note: "ما باید یه کاپوننت جدید تو replayer داشته باشیم. که کار convert کردن SQL/ SQlite رو به postgress انجام بده"
