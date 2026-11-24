# Backend API components

## Purpose and Scope

The Backend API authenticates requests, applies access policy, creates durable jobs, validates outcomes, and delivers approved results. It is one deployable ASP.NET Core application in the modular monolith.

## Runtime Technology

ASP.NET Core on .NET 10 LTS, REST/JSON, OpenAPI, EF Core, Npgsql, and the Shared Chart Presentation Library. Direct Npgsql use is limited to job claim and approved SQL execution.

## Trust Boundary

All browser, scheduler, runtime, and file input is untrusted until validation. PostgreSQL is the source of truth for durable product state. Internal calls do not bypass identity, scope, or purpose checks.

## Allowed Responsibilities

- Authenticate and authorize product requests.
- Route each request to one fixed handler.
- Create durable jobs and return persisted identifiers.
- Validate, publish, deliver, audit, and export approved results.
- Deliver internal Presentation responses with authorized `ChartSpec` values without changing the formal Submission contract.

## Forbidden Responsibilities

- Run LangGraph or model calls.
- Run deterministic daily processing or KPI calculation.
- Treat a wake-up call as a queue or source of truth.
- Change the reference output contracts.
- Accept language-model chart values or ECharts options as authoritative product data.

> **Implementation source note.** This document and `16-domain-model.md` define the Backend API boundaries used for implementation. The DSL is a visual overview. Read §6 of doc 16 for the reasoning behind each merge.

## Component Map (target)

| Group | Components |
|---|---|
| Access | Authorization Service (includes identity validation) |
| Request Routing | Configuration Service (KPI + organization); Decision and Follow-Up (includes card review); Run Coordinator |
| Bounded Analysis | Agent Runtime Gateway; Evidence Service; Query Gateway (includes SQL AST validation) |
| Validate and Deliver | Output Validator; Publisher; Submission Exporter; Report and Dashboard API (includes job status); Audit Service |
| Document Decision Flow | Document Processing Runner (includes parsing) |

Removed as separate components: Identity Boundary and Manager Request Router (functions inside Authorization Service and the fixed handlers), Organization Configuration Service (merged into Configuration Service), SQL AST Guard (module inside Query Gateway), Agent Job Status API (merged into Report and Dashboard API), Decision Confirmation Service (merged into Decision and Follow-Up), Document Parser (merged into Document Processing Runner).

## Internal Relationships

Calls are in-process unless the model states an authenticated Runtime call. The request path is Authorization Service (identity + scope), fixed handler, and persisted outcome. Routing is a function, not a component.

## External Relationships

The container uses the Identity Provider, PostgreSQL, Protected File Archive, Agent Runtime, Web Application, and Submission Output Directory. It can send redacted telemetry to the optional Collector.

## Component Sections

<a id="authorization-service"></a>

### Authorization Service

- **DSL identifier:** `authorizationService`;
- **Display name:** Authorization Service.
- **Purpose:** Validate the session, then build and verify row, column, role, purpose, and policy scope.
- **Responsibilities:** Validate identity, read grants, and check authority.
- **Inputs:** Authenticated request, identity-provider result, purpose, resource, and policy request.
- **Outputs:** Authorized scope or denial. Identity validation (`identityBoundary` in the current DSL) is a function inside this component, not a separate box.
- **Owned state:** Grants and policy in PostgreSQL.
- **Dependencies:** PostgreSQL and Identity Provider (identity validation is in-process).
- **Security boundary:** Product authorization decision point.
- **Forbidden responsibilities:** UI-only control, scope widening, and agent execution.
- **Failure behavior:** Deny when a policy fact is missing.
- **Idempotency:** Checks are stable for a pinned policy version.
- **Observability:** Record outcome, policy version, purpose, and trace ID.
- **Related ADRs:** ADR-0005, ADR-0019, ADR-0020.
- **Open issues:** Final Runtime database role names remain open.

<a id="configuration-service"></a>

### Configuration Service

- **DSL identifier:** `configurationService`;
- **Display name:** Configuration Service.
- **Purpose:** Store inactive KPI, organization, and manager-priority configuration candidates and activate only approved valid versions at D+1.
- **Responsibilities:** Check authority, persist candidates, request deterministic semantic or organization validation, require a passing Parity Receipt for a KPI definition, and control approval, scheduling, and activation state.
- **Inputs:** Authorized KPI, organization, target, threshold, or manager-priority candidate and version metadata.
- **Outputs:** Candidate ID, validation job, activation state, and the active-version pointer consumed by Snapshot Service. This component absorbs Organization Configuration Service (`organizationConfigurationService` in the current DSL); org changes are one candidate class, not a separate aggregate (ADR-0014 amended).
- **Owned state:** Versioned configuration candidates, approval state, activation schedule, manager-priority settings, and active-version pointers in PostgreSQL.
- **Dependencies:** Authorization Service, Semantic Registry, and PostgreSQL.
- **Security boundary:** Authorized configuration and organization administrators only.
- **Forbidden responsibilities:** Translate KPI SQL, issue a Parity Receipt, activate invalid candidates, perform same-day org activation, mutate history, or calculate KPIs.
- **Failure behavior:** Keep the active version and record failed validation.
- **Idempotency:** Candidate version and key prevent duplicate activation.
- **Observability:** Record version, job, receipt, status, and trace ID.
- **Related ADRs:** ADR-0011, ADR-0014, ADR-0018.
- **Open issues:** None.

<a id="decision-and-follow-up"></a>

### Decision and Follow-Up

- **DSL identifier:** `decisionTracker`;
- **Display name:** Decision and Follow-Up.
- **Purpose:** Store validated decision cards, process human review, and record confirmed decisions, signal disposition, and follow-up contracts.
- **Responsibilities:** Verify authority, release valid cards, process confirm/edit/reject commands, record authorized `CloseSignal` and `ReferSignal` commands, store decisions, owners, actions, and deadlines, and request drafts.
- **Inputs:** Validated card, authenticated review or signal-disposition command, or authorized manual decision.
- **Outputs:** Review state, signal-disposition record, revision job, and versioned decision and follow-up records. This component absorbs Decision Confirmation Service (`decisionConfirmationService` in the current DSL): card and review state belong to the `Decision` aggregate.
- **Owned state:** Card versions, review state, and decision/follow-up state in PostgreSQL.
- **Dependencies:** Authorization Service, PostgreSQL, Agent Runtime Gateway, and Document Processing Runner.
- **Security boundary:** An authorized human reviews and confirms each card.
- **Forbidden responsibilities:** Execute actions or auto-confirm drafts.
- **Failure behavior:** Reject incomplete or unauthorized input.
- **Idempotency:** Decision ID and command version prevent duplicate confirmation.
- **Observability:** Record state changes, actor, receipt, and trace ID.
- **Related ADRs:** ADR-0010, ADR-0011, ADR-0015, ADR-0017.
- **Open issues:** None.

<a id="run-coordinator"></a>

### Run Coordinator

- **DSL identifier:** `runCoordinatorV2`;
- **Display name:** Run Coordinator.
- **Purpose:** Create pinned run plans, monitor jobs, and close each run.
- **Responsibilities:** Validate control identity, pin versions, create stage jobs, and close terminal runs.
- **Inputs:** Authenticated start or status request and business date.
- **Outputs:** Run ID, plan, status, and terminal result.
- **Owned state:** Run plan, dependency, lease, and terminal state in PostgreSQL.
- **Dependencies:** Authorization Service, PostgreSQL, and Run Stage Coordinator.
- **Security boundary:** Scheduler control uses an authenticated API.
- **Forbidden responsibilities:** Use host time or run stages in the API.
- **Failure behavior:** Preserve resumable state.
- **Idempotency:** Pinned run key prevents duplicate runs.
- **Observability:** Record run ID, jobs, versions, status, and trace ID.
- **Related ADRs:** ADR-0011, ADR-0012, ADR-0018.
- **Open issues:** Scheduler process type remains open.

<a id="agent-runtime-gateway"></a>

### Agent Runtime Gateway

- **DSL identifier:** `agentGateway`;
- **Display name:** Agent Runtime Gateway.
- **Purpose:** Create or wake durable Agent Jobs without graph execution.
- **Responsibilities:** Commit the scoped job, return its ID, and send an optional job-ID wake-up.
- **Inputs:** Authorized context, scope, purpose, and workload references.
- **Outputs:** Committed job ID and optional wake-up.
- **Owned state:** Agent Job state in PostgreSQL.
- **Dependencies:** PostgreSQL and Agent Job Runner.
- **Security boundary:** Wake-up contains no evidence and grants no access.
- **Forbidden responsibilities:** Run LangGraph, carry evidence, calculate KPIs, or publish.
- **Failure behavior:** Failed wake-up does not lose the job.
- **Idempotency:** Job key prevents duplicate work.
- **Observability:** Record job ID, type, status, wake-up result, and trace context.
- **Related ADRs:** ADR-0008, ADR-0011, ADR-0019, ADR-0020.
- **Open issues:** Deadline, retry count, and dead-letter policy remain open.

<a id="evidence-service"></a>

### Evidence Service

- **DSL identifier:** `evidenceService`;
- **Display name:** Evidence Service.
- **Purpose:** Build a traceable Evidence Bundle inside authorized scope.
- **Responsibilities:** Verify scope, run registered queries, and read approved bytes.
- **Inputs:** Trusted actor, purpose, policy, scope, and evidence requests.
- **Outputs:** Evidence Bundle with citations and lineage, or failure.
- **Owned state:** Evidence references and receipts in PostgreSQL.
- **Dependencies:** Authorization Service, Query Gateway, and Protected File Archive.
- **Security boundary:** Evidence cannot exceed trusted scope.
- **Forbidden responsibilities:** Widen scope, run arbitrary SQL, or treat chat as business evidence.
- **Failure behavior:** Return explicit failure and do not fabricate evidence.
- **Idempotency:** Pinned versions make a bundle reproducible.
- **Observability:** Record references, lineage, status, and trace ID.
- **Related ADRs:** ADR-0005, ADR-0008, ADR-0011, ADR-0019.
- **Open issues:** None.

<a id="query-gateway"></a>

### Query Gateway

- **DSL identifier:** `queryGateway`;
- **Display name:** Query Gateway.
- **Purpose:** Run registered tools and scoped read-only SQL under limits and audit.
- **Responsibilities:** Load allow-lists, validate SQL (AST validation is a module inside this component), apply scope, execute, and audit.
- **Inputs:** Authorized Query Specification and trusted scope.
- **Outputs:** Bounded result and lineage, or refusal. SQL AST Guard (`sqlGuard` in the current DSL) is demoted to a stateless validator module here, not a separate component.
- **Owned state:** Query audit records in PostgreSQL.
- **Dependencies:** Authorization Service, PostgreSQL, and Audit Service.
- **Security boundary:** Scope and approved views constrain each query.
- **Forbidden responsibilities:** Unrestricted SQL, RLS bypass, and credential disclosure.
- **Failure behavior:** Deny when validation is incomplete.
- **Idempotency:** Reads repeat against pinned versions.
- **Observability:** Record definition, scope reference, limit, duration, size, and trace ID.
- **Related ADRs:** ADR-0005, ADR-0011, ADR-0019, ADR-0020, ADR-0023.
- **Open issues:** None. For ad-hoc questions, executes model-generated SQL only after AST validation and scope injection, on the pinned snapshot; persists the query with a new `query_id` and result hash (ADR-0023).

<a id="output-validator"></a>

### Output Validator

- **DSL identifier:** `outputValidator`;
- **Display name:** Output Validator.
- **Purpose:** Validate agent output before delivery, publication, review, or export.
- **Responsibilities:** Check schema, values, evidence, scope, recipient, alternatives, and response rules.
- **Inputs:** Persisted candidate, reference contract, scope, and evidence references.
- **Outputs:** Validated result, fallback instruction, or rejection.
- **Owned state:** Validation state and receipt in PostgreSQL.
- **Dependencies:** Query Gateway, Authorization Service, Evidence Service, Audit Service, and PostgreSQL.
- **Security boundary:** Unvalidated model output cannot become a product result.
- **Forbidden responsibilities:** Repair claims, change schemas, or publish.
- **Failure behavior:** Persist rejection and release the deterministic no-narrative fallback required by ADR-0022 when model content is unavailable.
- **Idempotency:** Candidate hash and validator version make results stable.
- **Observability:** Record receipt, hash, failed rule, status, and trace ID.
- **Related ADRs:** ADR-0004, ADR-0005, ADR-0008, ADR-0010, ADR-0013, ADR-0022, ADR-0023.
- **Open issues:** None. For ad-hoc answers, check that every number maps to a `value` and `query_id` pair and apply the `refused_out_of_scope` and `data_unavailable` status rules (ADR-0023). For a reported cause, require at least two independent evidence references before validation.

<a id="publisher"></a>

### Publisher

- **DSL identifier:** `publisherV2`;
- **Display name:** Publisher.
- **Purpose:** Atomically publish validated canonical JSON or deterministic fallback text.
- **Responsibilities:** Publish a new version, unlock the next job, audit, and forward valid reports for export.
- **Inputs:** Validated report package or approved fallback.
- **Outputs:** Published version and publication receipt.
- **Owned state:** Published report versions in PostgreSQL.
- **Dependencies:** PostgreSQL, Audit Service, and Submission Exporter.
- **Security boundary:** Only validated content can publish.
- **Forbidden responsibilities:** Generate content, hide source gaps, or mutate old versions.
- **Failure behavior:** Preserve the prior version and record failure.
- **Idempotency:** Version and content hash prevent duplication.
- **Observability:** Record version, hash, status, receipt, and trace ID.
- **Related ADRs:** ADR-0003, ADR-0004, ADR-0009, ADR-0011.
- **Open issues:** Reconciliation cadence remains open.

<a id="submission-exporter"></a>

### Submission Exporter

- **DSL identifier:** `submissionExporter`;
- **Display name:** Submission Exporter.
- **Purpose:** Export approved brief and QA files under `OUTPUT_DIR`.
- **Responsibilities:** Check containment, use a temporary file, flush, close, rename atomically, hash, and store a receipt.
- **Inputs:** Validated contract payload, artifact type, relative path, and trace context.
- **Outputs:** Contract file and Export Receipt.
- **Owned state:** Export Receipts in PostgreSQL and files in Submission Output Directory.
- **Dependencies:** PostgreSQL and Submission Output Directory.
- **Security boundary:** Resolved path stays under `OUTPUT_DIR`.
- **Forbidden responsibilities:** Change schemas, export internal fields, or create `OUTPUT_DIR/submission/...`.
- **Failure behavior:** Leave no partial final file.
- **Idempotency:** Path, version, and hash make retry safe.
- **Observability:** Record path, hash, receipt, status, and trace ID.
- **Related ADRs:** ADR-0011, ADR-0013, ADR-0015.
- **Open issues:** None.

<a id="report-and-dashboard-api"></a>

### Report and Dashboard API

- **DSL identifier:** `reportApi`;
- **Display name:** Report and Dashboard API.
- **Purpose:** Deliver authorized reports, dashboards, workflows, answers, chart specifications, agent job status, or failures.
- **Responsibilities:** Recheck audience and purpose, run approved reads, return bounded responses, and assemble the internal Presentation response. For a published report, read the stored `ChartSpec` records for the same immutable report version. For a validated interactive answer, use the Shared Chart Presentation Library to create a deterministic `ChartSpec` from the validated `ChartIntent` and persisted bounded query result.
- **Inputs:** Trusted scope and product read request (including job ID for status), validated content reference, stored report `ChartSpec`, or validated interactive `ChartIntent` plus bounded query result.
- **Outputs:** Authorized Presentation response, authorized status response, or explicit failure. A Presentation response contains validated content and zero or more `ChartSpec` values. This component absorbs Agent Job Status API (`agentJobStatusService` in the current DSL): job status is an authorized read with no owned state. A job ID never grants result access.
- **Owned state:** None. An interactive `ChartSpec` is a derived read record persisted with its validated answer; it is not component-owned state.
- **Dependencies:** Authorization Service, Query Gateway, PostgreSQL, Shared Chart Presentation Library, and Web Application.
- **Security boundary:** Recheck audience, purpose, and scope before delivery. Chart points and query lineage cannot exceed the authorized content scope. Do not disclose cross-scope job state.
- **Forbidden responsibilities:** Generate unvalidated answers, use language-model values as chart data, recalculate a stored report chart, bypass scope, read arbitrary tables, mutate jobs, or add presentation fields to formal Submission output.
- **Failure behavior:** Return explicit unavailable, incomplete, forbidden, or failed state.
- **Idempotency:** Reads repeat for the same version. Interactive chart construction is stable for the same validated result, `ChartIntent`, and chart-contract version.
- **Observability:** Record type, version, scope reference, result, latency, and trace ID.
- **Related ADRs:** ADR-0003, ADR-0004, ADR-0005, ADR-0009, ADR-0028.
- **Open issues:** None.

<a id="audit-service"></a>

### Audit Service

- **DSL identifier:** `auditService`;
- **Display name:** Audit Service.
- **Purpose:** Record restricted query, model, validation, cost, publication, and failure evidence.
- **Responsibilities:** Normalize audit events and persist immutable references and receipts.
- **Inputs:** Approved event and correlation context.
- **Outputs:** Audit record or failure.
- **Owned state:** Restricted audit records in PostgreSQL.
- **Dependencies:** PostgreSQL.
- **Security boundary:** Payloads exclude secrets and unauthorized raw data.
- **Forbidden responsibilities:** Change results, store full telemetry, or act as a queue.
- **Failure behavior:** Surface failure to the caller under the event policy.
- **Idempotency:** Event ID prevents duplicate records.
- **Observability:** Record audit write status and trace ID.
- **Related ADRs:** ADR-0011, ADR-0020.
- **Open issues:** Retention and backup frequency remain open.

<a id="document-processing-runner"></a>

### Document Processing Runner

- **DSL identifier:** `documentProcessingRunner`;
- **Display name:** Document Processing Runner.
- **Purpose:** Archive uploads, parse them deterministically, and create durable analysis or revision jobs.
- **Responsibilities:** Store bytes and hash, validate format/size limits, extract immutable fragments and a parse receipt, commit a scoped job, return its ID, and request wake-up.
- **Inputs:** Authorized upload or revision request and parsing policy.
- **Outputs:** Archive reference, fragments, parse receipt, job ID, and optional wake-up. This component absorbs Document Parser (`documentParser` in the current DSL): parsing is a bounded function over archived bytes, and fragments/receipts belong to this job.
- **Owned state:** Job and upload references, fragments, and receipts in PostgreSQL; bytes in archive.
- **Dependencies:** Protected File Archive, PostgreSQL, and Agent Runtime Gateway.
- **Security boundary:** Uploads stay untrusted until validation; content is data, never instructions.
- **Forbidden responsibilities:** Run a graph, trust file names, call a model, execute content, or send bytes in wake-up.
- **Failure behavior:** Record the failed stage and do not analyze an invalid parse.
- **Idempotency:** Upload hash and request key prevent duplication.
- **Observability:** Record hash, archive reference, receipt, job ID, and trace ID.
- **Related ADRs:** ADR-0008, ADR-0010, ADR-0011, ADR-0019.
- **Open issues:** None.

## Consolidation log (implementation model)

The following former components are intentionally absent from the implementation model. See `16-domain-model.md` §6 for the reasoning.

| Removed component | Disposition |
|---|---|
| Identity Boundary | Function inside Authorization Service |
| Manager Request Router | Function inside the fixed handlers |
| Organization Configuration Service | Merged into Configuration Service |
| SQL AST Guard | Module inside Query Gateway |
| Agent Job Status API | Merged into Report and Dashboard API |
| Document Parser | Merged into Document Processing Runner |
| Decision Confirmation Service | Merged into Decision and Follow-Up |

## Container-level Open Issues

- Authentication product and method remain open.
- OTLP/gRPC or OTLP/HTTP for Backend telemetry remains a configuration decision.
- Agent Job deadline, Agent Job retry policy, dead-letter policy, and reconciliation cadence remain open. Model-call timeout, retry limit, and no-narrative fallback are fixed by ADR-0022.
