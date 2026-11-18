# 19. Use PostgreSQL durable Agent Jobs and limited runtime access

Date: 2026-11-19

## Status

Accepted

## Context

Agent work can continue after the Backend API request ends. A process failure or a lost wake-up must not lose accepted work. The Agent Runtime also needs checkpoint and candidate state, but it must not receive unrestricted access to business data.

## Decision

PostgreSQL is the source of truth for durable Agent Jobs, leases, attempts, dependencies, checkpoints, conversation state, candidates, failures, and job-scoped evidence references.

The Backend API creates the Agent Job and its trusted actor, scope, policy, context, and evidence references in one committed transaction. The Backend API returns the `job_id` only after the commit. It can then send an authenticated wake-up that contains the `job_id`. This wake-up is optional and is only a hint.

The Agent Runtime claims a ready job from PostgreSQL. The claim uses a restricted database role and a concurrency-safe PostgreSQL operation. The Agent Runtime reloads the pinned actor, scope, policy, context, and evidence references before it runs the graph. It updates the lease and attempt state and records a candidate or an explicit failure.

Direct Agent Runtime database access is limited to:

- Agent Job
- Lease
- Attempt
- Dependency state needed by the claimed job
- LangGraph checkpoint
- Conversation state
- Candidate and failure state
- Job-scoped Evidence views

The Agent Runtime has no direct access to Orders, Customers, Organization, KPI fact tables, or unrestricted report data. It obtains business evidence through the Backend API Evidence Service and Query Gateway. It does not run arbitrary business SQL. It does not perform schema migration or policy changes.

## Alternatives rejected

- An in-memory queue is rejected because it cannot provide durable job state.
- The authenticated wake-up is rejected as a queue or source of truth because it can be delayed or lost.
- An unrestricted Agent Runtime database role is rejected because it would bypass scope and evidence controls.
- Direct arbitrary SQL from the Agent Runtime is rejected because it would bypass the Query Gateway.

## Consequences

Committed Agent Jobs survive process and wake-up failures. The Agent Runtime can resume bounded work from durable state. The Backend API remains the business-data and authorization boundary. PostgreSQL permissions and job-claim behavior require dedicated security and concurrency tests.

## Security impact

The Agent Runtime uses a restricted PostgreSQL role. Relation, column, row, purpose, and job-scope controls apply to its allowed state. Negative tests must prove that the role cannot read business tables or change database policies.

## Operational impact

Operators must monitor job age, lease state, attempt state, terminal failures, and unclaimed committed jobs. Wake-up failure must not stop claim and reconciliation behavior. The reconciliation cadence and dead-letter policy remain open.

## Related requirements

- A job must be durable before the Backend API returns its identifier.
- Wake-up delivery must not define job durability.
- The Agent Runtime must reload and revalidate trusted scope for each claim.
- Business evidence must pass through Backend API controls.

## Related model elements

- Backend API: Agent Runtime Gateway
- Backend API: Evidence Service
- Backend API: Query Gateway
- Backend API: Authorization Service
- Agent Runtime: Agent Job Runner
- Agent Runtime: Bounded Agent Orchestrator
- PostgreSQL

## Open decisions

- The final name of the restricted Agent Runtime database role is open.
- Migration from the existing `agent_query_reader` role, or continued use of that role, is open.
