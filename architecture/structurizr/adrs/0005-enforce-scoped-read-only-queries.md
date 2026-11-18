# 5. Enforce scoped read-only queries before model use

Date: 2026-11-14

## Status

Accepted

## Context

Interactive questions and evidence assembly can expose data across manager scopes. A hierarchy position does not automatically permit access to individual employee or customer data.

## Decision

Access is based on resource, column, purpose, predicate, and organization scope. The Backend API Evidence Service and Query Gateway apply row and column restrictions before business data reaches the language model. Only registered read-only queries are permitted. Undefined access is denied.

`customer_id` is internal only. City and aggregated city KPI values are permitted. PostgreSQL row-level security, restricted runtime roles, SQL AST validation, relation allowlists, column projections, purpose checks, evidence filtering, output validation, and audit records form one defense-in-depth control set.

The Agent Runtime database role is limited to Agent Job, Lease, Attempt, Checkpoint, Conversation, Candidate, and job-scoped Evidence state. It has no direct access to Orders, Customers, Organization, or KPI fact tables. The Agent Runtime does not perform migrations or policy changes.

## Consequences

The language model never receives unrestricted business data or a credential that can read business tables. All business query and evidence paths go through the Backend API. They must carry trusted principal, purpose, policy, and snapshot context. Negative leakage tests are required for each manager role.

The complete shared-resource projection matrix remains open in `ISSUE-V3-01`.

## Related requirements

- Manager scope must be enforced before evidence reaches the model.
- The Agent Runtime must not run arbitrary SQL on business data.
- Direct Agent Runtime database access must remain limited to durable job and agent-owned state.
