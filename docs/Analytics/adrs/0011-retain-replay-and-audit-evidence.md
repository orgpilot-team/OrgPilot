# 11. Retain evidence needed for replay and recovery

Date: 2026-11-14

## Status

Accepted for the evaluation profile (production retention remains open)

## Context

OrgPilot needs replay, audit, and recovery evidence. The team has not approved the retention periods, backup frequency, audit-reader role, or complete restore policy.

## Decision

Preserve the raw data, configuration, queries, reports, and audit records that are required to replay a run. Do not put personal data in general application logs.

## Consequences

PostgreSQL backups and Archive manifests must form a consistent recovery point. A restore test must verify file hashes, snapshot reconstruction, sample query parity, and sample report reproduction.

For the evaluation profile, `ISSUE-V3-09` is closed by `docs/15-implementation-contract.md`: source hashes, pinned snapshots, queries and `query_id`s, configuration versions, published report versions, receipts, and logs remain inside the container for the duration of the run; the two-run determinism check (ADR-0026) uses this evidence. Long-term production retention, backup schedule, audit-reader role, and restore procedure remain open and do not affect the graded run.

## Related requirements

- Replay and recovery must preserve the evidence that produced a result.
- Retention periods, backup frequency, RPO, RTO, and the audit-reader role remain open decisions.
