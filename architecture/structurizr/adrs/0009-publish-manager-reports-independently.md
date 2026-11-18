# 9. Publish valid manager reports independently

Date: 2026-11-14

## Status

Accepted

## Context

One manager report can fail model use, validation, or artifact publication. That failure must not remove valid work for other managers.

## Decision

Each manager report is an independent publication unit. The system preserves and publishes valid reports when another manager report fails. If a required report fails, the final day status is `incomplete`. This status does not remove valid reports for that day.

A language-model API failure does not stop deterministic calculation or valid canonical JSON production.

## Consequences

Run status and report status are separate. The system needs manager-level job state, validation state, publication receipts, and daily coverage records. Publication must be atomic for the artifacts of one manager.

The exact retry count, timeout, and fallback content remain open in `ISSUE-V3-06`.

## Related requirements

- A failure for one manager must not remove valid output for another manager.
- A model failure must not stop deterministic calculation or valid canonical JSON output.
