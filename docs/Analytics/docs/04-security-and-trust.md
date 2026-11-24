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

Ad-hoc Text-to-SQL questions use the same path with an added generation contract (ADR-0023). Scope is pinned before the model writes SQL. The model may name only approved semantic views and KPI definitions, never raw business tables, and has no database credential. The Backend injects the scope predicate so generated SQL cannot omit it. After validation the query is persisted with a new `query_id`, scope, and result hash and shown beside the answer. "Registered" for an ad-hoc query means persisted, validated, and auditable; it does not mean pre-approved in the KPI Dictionary. A number in the answer must map to a `value` and `query_id` pair. `refused_out_of_scope` is used when data exists outside the manager's subset; `data_unavailable` is used when the data is not in the system sources.

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

## Chart presentation boundary

`ChartIntent` is an optional presentation request. It can select an allowed chart type, KPI, time range, and grouping. It cannot supply chart values, widen scope, select an unapproved relation, or replace query lineage. Language-model output that contains a `ChartIntent` remains an untrusted candidate until Output Validator checks it.

`ChartSpec` is built only from pinned report evidence or a validated bounded query result. Every series carries its source references, including the applicable `query_id`. A report chart is also bound to its report version, snapshot, and manager scope. The Report and Dashboard API rechecks audience, purpose, and scope before it returns a chart. A chart identifier or report identifier never grants access by itself.

The Web Application receives only the authorized points required for the requested chart. It does not receive unrestricted facts and does not calculate a wider aggregation. ECharts options are created in the Web Application from the authorized `ChartSpec`; they are not accepted from the language model or stored as business evidence.

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
- The Document Processing Runner parses only archived bytes with an approved contract (the former Document Parser is a function inside it).
- Output Validator verifies schema, scope, and evidence before publication or export.
- Submission Exporter writes only validated contract fields to a contained path below `OUTPUT_DIR`.
- Submission Exporter excludes `ChartIntent`, `ChartSpec`, Presentation responses, and ECharts options from formal output.
- OpenTelemetry and Langfuse instrumentation must remove secrets, raw restricted business data, full documents, and unauthorized manager context.

A minimal access projection matrix is required before authorization and scoped-query implementation. It must cover Senior Manager, Unit Manager, and Team Supervisor and specify Resource, Row scope, Allowed columns, Purpose, and individual-data access. This document does not define the matrix entries and does not approve a new database-role name or a wider data projection.
