# Security and trust

The following inputs are untrusted:

- Source files
- Ticket text
- Manager uploads
- User prompts
- Language-model output

Untrusted input cannot change policy, credentials, report destinations, approved numbers, or the tool allowlist.

The Backend API creates a trusted identity context. The Authorization Service derives the permitted resource, column, purpose, predicate, and organization scope. Authorization is applied before evidence reaches the language model. Output validation applies the scope again before delivery or publication.

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

The language model has no database credential. It has no direct file credential. The Model Gateway is the only external model path. It applies token, time, retry, and cost limits.

The proposed runtime roles are `ingestion_writer`, `analytics_worker`, `application_api`, `agent_query_reader`, and `audit_reader`. A separate `migration_owner` owns database objects and is not used at runtime.

The complete projection matrix for shared resources remains open in `ISSUE-V3-01`.
