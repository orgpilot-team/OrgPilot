# Security and trust

The following inputs are untrusted:

- Source files
- Ticket text
- Manager uploads
- User prompts
- Language-model output

Untrusted input cannot change policy, credentials, report destinations, approved numbers, or the tool allowlist.

The Backend API creates a trusted identity context. The Authorization Service derives the permitted resource, column, purpose, predicate, and organization scope. Authorization is applied before evidence reaches the language model. Output validation applies the scope again before delivery or publication.

## Business-data query path

The Agent Runtime requests business evidence from the Backend API Evidence Service. The Evidence Service sends approved query requests to the Query Gateway. The Query Gateway validates and executes the registered read-only operation. It returns only evidence that is inside the trusted actor, purpose, policy, snapshot, row, and column scope.

The query path uses defense in depth:

- Registered read-only queries
- Relation allowlists
- Column projections
- SQL AST validation
- Purpose checks
- PostgreSQL row-level security
- `FORCE ROW LEVEL SECURITY`
- Non-owner runtime roles
- No `SUPERUSER` or `BYPASSRLS` role in runtime paths
- Scope-aware caching
- Query and access audit records
- Negative leakage tests for each manager role

The language model has no database credential. It has no direct file credential. The Model Gateway is the only external model path. It applies the approved token, time, retry, and cost controls.

## Agent Runtime database boundary

ADR-0019 permits a restricted Agent Runtime PostgreSQL role. The final role name is open. Migration from the existing `agent_query_reader` role, or continued use of that role, is also open.

The restricted role can access only job-scoped agent state:

| Allowed state | Purpose |
|---|---|
| Agent Job | Claim and inspect the assigned durable job |
| Lease and Attempt | Control concurrent execution and recovery |
| Dependency state | Confirm that the claimed job is ready |
| LangGraph checkpoint | Resume bounded graph execution |
| Conversation state | Read and write manager-scoped bounded history |
| Candidate and failure state | Persist the runtime outcome |
| Job-scoped Evidence view | Reload references already approved for the job |

Direct access to these data areas is forbidden:

- Orders and operational facts
- Customers and customer identifiers
- Organization and authorization policy tables
- KPI facts and unrestricted report data
- Database migration metadata
- Row-level security policy administration

The Agent Runtime does not perform migrations, grant permissions, change policies, or execute arbitrary business SQL.

## Other trust boundaries

- Protected uploads are treated as data, not instructions.
- The Document Parser reads only archived bytes with an approved contract.
- Output Validator verifies schema, scope, and evidence before publication or export.
- Submission Exporter writes only validated contract fields to a contained path below `OUTPUT_DIR`.
- OpenTelemetry and Langfuse instrumentation must remove secrets, raw restricted business data, full documents, and unauthorized manager context.

The complete projection matrix for shared resources remains open. This document does not approve a new database-role name or a wider data projection.
