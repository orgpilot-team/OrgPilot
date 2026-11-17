# 5. Enforce scoped read-only queries before model use

Date: 2026-11-14

## Status

Accepted

## Context

Interactive questions and evidence assembly can expose data across manager scopes. A hierarchy position does not automatically permit access to individual employee or customer data.

## Decision

Access is based on resource, column, purpose, predicate, and organization scope. The Backend API and Query Gateway apply row and column restrictions before data reaches the language model. Only registered read-only queries are permitted. Undefined access is denied.

`customer_id` is internal only. City and aggregated city KPI values are permitted. PostgreSQL row-level security, restricted runtime roles, SQL AST validation, relation allowlists, column projections, purpose checks, evidence filtering, output validation, and audit records form one defense-in-depth control set.

## Consequences

The language model never receives unrestricted business data or a direct database credential. All query and evidence paths must carry trusted principal, purpose, policy, and snapshot context. Negative leakage tests are required for each manager role.

The complete shared-resource projection matrix remains open in `ISSUE-V3-01`.

## Source

`ADR-V3-05` in `Docs/final review/architecture-control-register-v3.md`.
