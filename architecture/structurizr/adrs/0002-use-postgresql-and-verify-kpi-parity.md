# 2. Use PostgreSQL as the product database and verify KPI parity

Date: 2026-11-14

## Status

Accepted

## Context

DIDRAH needs one product database for runtime state, analytical results, scoped queries, jobs, checkpoints, reports, and audit records. The evaluation data includes reference KPI SQL for SQLite.

## Decision

PostgreSQL is the only product database. SQLite is only the reference oracle for KPI parity tests.

Each PostgreSQL KPI result must match the SQLite reference result within the accepted evaluation tolerance. SQLite `median()` maps to PostgreSQL `percentile_cont(0.5)`. SQLite day differences map to PostgreSQL epoch calculations with explicit conversion to hours or days. Decimal division, rounding, date types, and timezone behavior must preserve reference semantics.

The system records the SQL, result, snapshot, scope, and `query_id` for each published number. The language model, UI, and serializer do not recalculate or round KPI values.

## Consequences

The product has one operational database and one security boundary for data queries. The team must maintain a parity suite for all approved KPI definitions. A SQL translation is not accepted until its parity evidence passes.

The complete contract for ad hoc numbers remains open in `ISSUE-V3-02`.

## Source

`ADR-V3-02` in `Docs/final review/architecture-control-register-v3.md`.
