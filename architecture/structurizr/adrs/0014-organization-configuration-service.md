# 14. Organization Configuration Service

Date: 2026-11-17

## Status

Accepted

## Context

The dataset includes an `org_change` on day 75 introducing M11 as the new marketing team manager. The current architecture has:

- Authorization Service
- Snapshot Service (pins org version)
- Configuration Service

But no specific component handles versioned organization changes that affect:

- Active manager
- Scope
- RLS policies
- Mandatory reports
- M11 start time
- Cache invalidation
- Conversation scope
- Query visibility
- Report recipient list

Configuration Service alone is insufficient because org changes have wider impact than KPI configuration.

## Decision

Add `Organization Configuration Service` as a separate component (or split Configuration Service into two modules: KPI Configuration and Organization Configuration).

Flow:

```
Manager Input → Authorization → Organization Configuration Service
→ inactive org revision → deterministic validation → activation at D+1
→ Snapshot pins org_version
```

Agent must NOT participate in organization changes.

## Consequences

- Org changes are versioned, validated, and activated at D+1
- Snapshot Service pins the org_version for each run
- All downstream effects (RLS, scope, recipients, cache) handled deterministically
- Clear separation from KPI configuration changes

## Source

Addresses Gap 3 from architectural review: "تغییر سازمان"
