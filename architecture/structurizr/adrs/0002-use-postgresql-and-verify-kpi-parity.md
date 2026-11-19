# 2. Use PostgreSQL as the product database and verify KPI parity

Date: 2026-11-14

## Status

Accepted

## Context

DIDRAH needs one product database for runtime state, analytical results, scoped queries, jobs, checkpoints, reports, and audit records. The evaluation data includes reference KPI SQL for SQLite. SQLite is not a product database or a runtime container.

## Decision

PostgreSQL 18 is the only product database. SQLite runs only as an embedded reference oracle inside the Acceptance Test Harness.

Each PostgreSQL KPI result must match the SQLite reference result within the accepted evaluation tolerance. SQLite `median()` maps to PostgreSQL `percentile_cont(0.5)`. SQLite day differences map to PostgreSQL epoch calculations with explicit conversion to hours or days. Decimal division, rounding, date types, and timezone behavior must preserve reference semantics.

The system records the SQL, result, snapshot, scope, and `query_id` for each published number. The language model, UI, and serializer do not recalculate or round KPI values.

## Consequences

The product has one operational database and one security boundary for data queries. The team must maintain a parity suite for all approved KPI definitions. A SQL translation is not accepted until its parity evidence passes. SQLite is not available to the product runtime.

The contract for ad hoc numbers is defined in [ADR-0023](0023-adhoc-text-to-sql-contract.md), which closes `ISSUE-V3-02`.

## Related requirements

- PostgreSQL 18 is the only product database.
- The reference SQL and KPI Dictionary are read-only evaluation contracts.
- The Acceptance Test Harness must compare PostgreSQL results with the SQLite reference results.
