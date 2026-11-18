# 11. Retain evidence needed for replay and recovery

Date: 2026-11-14

## Status

Proposed

## Context

DIDRAH needs replay, audit, and recovery evidence. The team has not approved the retention periods, backup frequency, audit-reader role, or complete restore policy.

## Decision

Preserve the raw data, configuration, queries, reports, and audit records that are required to replay a run. Do not put personal data in general application logs.

## Consequences

PostgreSQL backups and Archive manifests must form a consistent recovery point. A restore test must verify file hashes, snapshot reconstruction, sample query parity, and sample report reproduction.

This decision remains proposed. `ISSUE-V3-09` must define the retention matrix, backup schedule, audit access, and restore procedure before acceptance.

## Related requirements

- Replay and recovery must preserve the evidence that produced a result.
- Retention periods, backup frequency, RPO, RTO, and the audit-reader role remain open decisions.
