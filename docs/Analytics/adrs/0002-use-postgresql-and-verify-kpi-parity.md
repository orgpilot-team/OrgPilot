# 2. Use PostgreSQL as the product database and verify KPI parity

Date: 2026-11-14

## Status

Accepted

## Context

OrgPilot needs one product database for runtime state, analytical results, scoped queries, jobs, checkpoints, reports, and audit records. The evaluation data includes reference KPI SQL for SQLite. SQLite is not a product database or a runtime container.

## Decision

PostgreSQL 18 is the selected product database (the TA permits any engine whose results are identical). SQLite runs only as an embedded reference oracle inside the Acceptance Test Harness.

Each PostgreSQL KPI result must match the SQLite reference result within the accepted evaluation tolerance of **±1%**. Exact translation rules: SQLite `median()` maps to PostgreSQL `percentile_cont(0.5)`, **not** `percentile_disc`; `julianday(b)-julianday(a)` is in days and maps to `EXTRACT(EPOCH FROM b-a)/86400` with explicit conversion to the KPI unit (hours or days); percentages use `100.0 *` to avoid integer division; timezone (`Asia/Tehran`), date type, and per-KPI rounding must preserve reference semantics. The brief's "zero tolerance" applies only to matching report-text numbers to JSON `value`/`query_id` pairs, not to KPI computation.

The system records the SQL, result, snapshot, scope, and `query_id` for each published number. The language model, UI, and serializer do not recalculate or round KPI values.

## Consequences

The product has one operational database and one security boundary for data queries. The team must maintain a parity suite for all approved KPI definitions. A SQL translation is not accepted until its parity evidence passes. SQLite is not available to the product runtime.

The contract for ad hoc numbers is defined in [ADR-0023](0023-adhoc-text-to-sql-contract.md), which closes `ISSUE-V3-02`.

## Related requirements

- PostgreSQL 18 is the only product database.
- The reference SQL and KPI Dictionary are read-only evaluation contracts.
- The Acceptance Test Harness must compare PostgreSQL results with the SQLite reference results.
