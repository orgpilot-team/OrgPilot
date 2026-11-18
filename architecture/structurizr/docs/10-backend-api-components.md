# Backend API components

This document provides the detailed contracts for Backend API components. The short descriptions remain in the C4 model; each component URL points to its matching section here.

<a id="agent-runtime-gateway"></a>

## Agent Runtime Gateway

- **Purpose:** Create or wake durable Agent Jobs without executing an agent graph.
- **Input:** Authorized request context, pinned scope and workload-specific references.
- **Output:** Committed Agent Job identifier and an optional job-ID-only wake-up.
- **Source of truth:** PostgreSQL Agent Job state.
- **Forbidden responsibilities:** Running LangGraph, carrying evidence in the wake-up payload, calculating KPIs or publishing results.
- **Failure behavior:** A failed wake-up does not lose the committed job; polling and lease recovery remain authoritative.

<a id="evidence-service"></a>

## Evidence Service

- **Purpose:** Build a traceable Evidence Bundle inside the already-authorized scope.
- **Input:** Trusted actor, purpose, policy and scope plus registered evidence requests.
- **Output:** Evidence Bundle with citations and lineage references.
- **Source of truth:** Authorized PostgreSQL projections accessed through Query Gateway.
- **Forbidden responsibilities:** Widening scope, executing arbitrary SQL or treating conversation text as business evidence.
- **Failure behavior:** Return an explicit evidence failure; do not fabricate missing evidence.

<a id="query-gateway"></a>

## Query Gateway

- **Purpose:** Execute registered tools and scoped read-only SQL under deterministic limits and audit.
- **Input:** Authorized Query Specification and trusted scope.
- **Output:** Bounded query result, lineage and audit receipt, or explicit refusal.
- **Source of truth:** PostgreSQL approved views and registered query definitions.
- **Forbidden responsibilities:** Accepting unrestricted SQL, bypassing RLS or exposing database credentials to the model.
- **Failure behavior:** Deny by default when scope, purpose or query validation is incomplete.

<a id="sql-ast-guard"></a>

## SQL AST Guard

- **Purpose:** Validate that an interactive SQL request is one approved read-only statement.
- **Input:** Candidate SQL and the applicable query policy.
- **Output:** Approval with constraints or a deterministic refusal reason.
- **Source of truth:** SQL policy and allow-list configuration.
- **Forbidden responsibilities:** Executing SQL, authorizing business scope or rewriting unsafe statements into executable queries.
- **Failure behavior:** Parse or policy uncertainty results in rejection.
