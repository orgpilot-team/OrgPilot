# Backend development stages

This is the ordered implementation plan for the **first four stages only**. It is a progress record, not a new architecture decision or a replacement for the accepted contracts in `Analytics/docs/15-implementation-contract.md`, `Analytics/docs/16-domain-model.md`, and the ADRs. Update a stage's status and evidence links when work is completed; extend the table only when later stages are planned.

The first four stages build the deterministic backend and its replay mechanism. They do not claim that the complete evaluation submission, authenticated product API, Agent Runtime, or Web Application is finished.

| No. | Stage | Main implementation scope | Completion evidence | Status |
|---:|---|---|---|---|
| 1 | Foundation and persistence (Walking Skeleton) | Minimal runnable .NET processes; module boundaries; PostgreSQL 18; migrations; shared contracts and infrastructure conventions | The foundational services start together, database connectivity and migrations work, and module/process boundaries are visible in code | Completed — 2026-11-26 |
| 2 | Intake, snapshots, and KPIs | Versioned source intake; protected raw archive; canonical facts; data issues; immutable snapshots; KPI definitions, calculations, and SQLite parity | Pinned-day ingestion is repeatable; missing/late/duplicate cases behave correctly; every activated KPI translation has a passing Parity Receipt | In progress — build and acceptance pending |
| 3 | Workflows, signals, and report evidence | WF1–WF3 reconstruction; deterministic signal lifecycle, ownership, escalation, ranking; internal canonical report and evidence packages | Repeated pinned inputs produce the same workflow facts, signals, owners, ranking, numbers, and evidence references | Not started |
| 4 | Durable execution and replay | PostgreSQL job plans and stage jobs; claim/lease/attempt/terminal state; Backend Run Coordinator; Worker stage runner; ordered replay and recovery | A deterministic replay resumes safely, survives a lost wake-up or interrupted worker, and does not read future data | Not started; job policy decision required |

## 1. Foundation and persistence (Walking Skeleton)

The objective is a minimal runnable system that verifies the architecture, process connectivity, and persistence infrastructure end to end. Implement only the foundation needed to start and extend the application in subsequent stages.

**Implement**

- Create the .NET 10 solution, Backend API, Background Worker, and Scheduler/Replay project shells, with shared libraries only for contracts and infrastructure used across process boundaries. Keep the accepted modular-monolith ownership boundaries from domain-model doc 16; do not make every documented concept a separate project or aggregate.
- Establish dependency direction within modules, configuration loading, environment-specific startup, structured logging and trace correlation, and the injected business clock interface. Runtime telemetry export remains optional and fail-open.
- Bring up PostgreSQL 18 and the .NET processes through a local Docker Compose development profile. Establish controlled migrations, database connection configuration, and separate process credentials. Define only the tables needed as subsequent stages are implemented; do not freeze the still-open job state machine or access projection schema here.
- Establish persistence conventions for immutable versions, source hashes, idempotency keys, receipts, and query lineage, plus the protected file archive interface. Keep SQLite outside product runtime.
- Make the development process topology compatible with the later single-image evaluation entrypoint: API, Worker, Scheduler/Replay, Agent Runtime, and PostgreSQL remain separate logical processes even when packaged together.

**Scope boundary:** The Identity & Access module is a structural boundary only. Authentication providers, JWT or other token handling, authorization rules, the Access Projection Matrix, and business features belong to subsequent stages. Stage 1 does not introduce placeholder security behavior or business endpoints.

**Exit gate:** A clean checkout can build the solution, start the foundational services together, verify health and configuration, apply migrations to an empty PostgreSQL database, and verify process connectivity and the database and archive adapters with a small smoke check. No business-output claim is made at this stage.

**Completion evidence (2026-11-26):**

| Check | Result |
|---|---|
| [`OrgPilot.slnx`](../OrgPilot.slnx) restore and build with .NET SDK 10.0.303 | Passed; zero build warnings and errors |
| [`compose.yaml`](../compose.yaml) validation, Linux image builds, and fresh-volume startup | Passed; PostgreSQL 18.7 and Backend API healthy; Worker and Scheduler processes running |
| Initial EF Core migration | Passed; `20261126114934_InitialFoundation` persisted in `foundation.__EFMigrationsHistory`; repeat startup succeeded |
| Separate database principals | Passed; API and Worker are non-superuser, non-owner roles without `BYPASSRLS`, role-creation, database-creation, or migration-schema access |
| Backend health and development OpenAPI | Passed; `/health/live` and `/health/ready` returned `Healthy`; `/openapi/v1.json` returned an OpenAPI 3.1.1 document |
| Worker database and archive smoke check | Passed; database connection, hash-verified round trip, repeated storage, and isolated fixture cleanup |
| Scheduler-to-Backend HTTP check | Passed; Scheduler reached Backend readiness over the Compose network |
| Structured logs and trace IDs | Passed; Worker and Scheduler smoke logs included W3C trace and span IDs; optional external export remained disabled |

The repeatable startup and smoke-check procedure is documented in the [Backend Development Setup](../README.md#backend-development-setup-stage-1). The Scheduler uses a Generic Host console shell; its final scheduling policy and process-type decision remain open. The evaluation image and application-level authentication remain outside this completed stage.

The source directory naming refactor under [Coding conventions](CODING_CONVENTIONS.md) was also verified: the .NET solution rebuilt with zero warnings or errors, the React production build passed, and Docker Compose rebuilt and restarted the existing development stack successfully. Database and archive volumes were preserved.

The subsequent OrgPilot naming refactor was verified with another clean .NET build, React build, local Structurizr validation, and Docker Compose startup against a fresh database. The initial migration and least-privilege runtime roles were present, and the Worker and Scheduler startup checks passed. The obsolete verification database volume was removed after the new database passed its checks.

## 2. Intake, snapshots, and KPIs

**Implement**

- Read `DATA_DIR` without modifying the input. Check each drop manifest and file hash; archive original bytes; select a versioned schema contract; parse and normalize source rows into canonical facts with source lineage. Unknown or invalid structures produce explicit issues rather than inferred data.
- Deduplicate by the accepted entity and event keys before KPI calculation. Record missing, late-arriving, duplicate, invalid, and corrected data with the contract's timing and `null` behavior. A late or corrected source triggers a complete rebuild and a new snapshot, never an overwrite of prior evidence.
- Pin source, organization, policy, KPI-definition, configuration, calendar, and business-date versions for each run. Build derived projections from one immutable snapshot. Implement the Configuration Service's versioned candidate validation and D+1 activation for KPI thresholds, organization revisions, and manager priority; manager priority remains separate from KPI definitions. Stage 4 will feed scripted changes into these handlers.
- Register immutable KPI-definition versions, translate the reference SQLite SQL to PostgreSQL, and calculate approved KPI results with `query_id`, SQL/result lineage, units, precision, and status. Preserve the reference SQL unchanged.
- Build the **minimal Acceptance Test Harness parity path now**, not at the end of the project. Run the reference SQL in harness-only SQLite against equivalent pinned data, compare PostgreSQL results using the accepted ±1% KPI tolerance and exact null/population rules, and issue a Parity Receipt before a translated definition becomes eligible for activation.

**Exit gate:** Re-ingesting the same drop is idempotent; the same pinned inputs produce the same canonical facts, snapshot and KPI results; missing/late/duplicate fixtures meet doc 15; all baseline KPI translations used by the product have passing parity evidence. The harness is an acceptance tool, not a product database or daily runtime stage.

**Remaining work (2026-11-26; implementation in progress):**

- Complete active configuration version selection and pinning in Snapshot Service.
- Complete and verify schema-version/alias handling, late-arrival coverage, correction handling, and data-issue timing and null behavior.
- Restore/build the .NET solution, apply the new EF Core migrations to PostgreSQL, and run intake, snapshot, and D+1 configuration checks.
- Execute the Acceptance Harness for all 55 baseline KPIs, resolve parity failures, and verify repeatability and passing Parity Receipts before activation.

Stage 2 code is committed, but its exit gate has not been verified. Build and test execution are deferred to a separate session.

## 3. Workflows, signals, and report evidence

**Implement**

- Reconstruct WF1–WF3 from pinned canonical events, including stage durations, SLA, backlog, and bottleneck observations. Apply the accepted workflow-stage owner mapping and organization version.
- Detect and persist deterministic signal episodes using the approved KPI direction, thresholds, trend rules, owner assignment, co-cause grouping, suppression, priority ranking, and escalation history. Keep data-quality issues separate from business signals. Enforce at most five items per manager report.
- Assemble internal, deterministic canonical report candidates and evidence packages from KPI results, workflow facts, signal episodes, approved follow-up facts when available, and source/query references. Preserve a manager and scope reference so the later authorization boundary can validate delivery. No model-generated number, owner, or signal status enters these artifacts.
- Keep report-evidence assembly callable through an application service so stage 4 can invoke it from durable jobs. A direct deterministic harness may invoke it in this stage; that harness is not the final scheduler.

**Boundary for this stage:** The dataset's organization hierarchy can be used to assemble manager-specific **internal candidates**. The Access Projection Matrix is still required before production scoped-query enforcement, authorized evidence delivery, or publication. Chart capability is required for the finished product, but chart policy, allowlist, limits, and OpenAPI wire details remain open; do not treat a temporary chart shape as an approved contract. The first four stages can verify canonical evidence and reports without completing chart delivery.

**Exit gate:** On fixed snapshots, WF1–WF3 results and signal IDs, states, owners, ordering, and evidence references are reproducible. Tests cover unfavorable direction, `new`/`ongoing`/`escalated` transitions, late-data recomputation, co-cause grouping, and the five-item limit. The artifacts remain internal and unpublished.

## 4. Durable execution and replay

**Required decision before implementing the job schema:** Approve one shared lifecycle contract for Worker stage jobs and later Agent Jobs: job deadline, job-level retry/attempt policy, lease duration and expiry recovery, reconciliation cadence, terminal/dead-letter behavior, idempotency and dependency semantics. The accepted 30-second timeout and at most two retries apply to **model calls**, not automatically to a whole job. The policy must fit the five-minute-per-processing-day evaluation limit. Do not record proposed numeric values as accepted until decided.

**Required before routing scripted inputs through the Backend API:** Define how a versioned evaluation `manager_id` becomes a trusted principal for replay. The scripted adapter must use the same authorization and validation path as an interactive request; it cannot bypass the Backend API or assume that an untrusted manager ID grants access. This evaluation identity contract can be established without selecting the later production UI authentication product.

**Implement after that decision**

- Persist a run plan, business-day cutoff, ordered stage dependencies, stage jobs, leases, attempts, receipts, and terminal day state in PostgreSQL. Backend Run Coordinator creates a pinned, idempotent run; the Worker claims ready deterministic stages and records outcomes. Wake-ups may improve latency but are never the source of truth.
- Implement the Replay Command and Run Status Client with injected simulated time, stable ordering, cutoff rules, day-range selection, status checks, and resume from the last terminal day. `day_000` through `day_090` are processed in order; morning D sees only data and manager input through D-1.
- Feed the deterministic scripted input kinds needed by stages 2–3 (configuration, priority, and organization changes) through the Backend API using the approved evaluation identity path, explicit handlers, and version selection. Preserve the order and identity of other scripted inputs for the later question, upload, and decision flows; do not pretend those later handlers exist.
- Add reconciliation for committed but unclaimed work and expired leases, plus idempotent stage re-execution after interruption. A failed manager or stage has an explicit terminal/incomplete state without erasing other durable results.
- Exercise the deterministic replay with the stage-2 and stage-3 checks, including a restart, lost wake-up, late source, organization change, and no-future-data check. Leave model calls, final Output Validator/Publisher, Submission Exporter, and full two-run submission acceptance to later stages.

**Exit gate:** An interrupted replay resumes without duplicate effects, completes the deterministic stage graph in day order, records failures explicitly, and reproduces KPI, workflow, signal, and internal evidence results from pinned inputs. This gate does **not** certify complete evaluation output.

## References and change control

- Accepted implementation rules: `Analytics/docs/15-implementation-contract.md`.
- Domain and component ownership: `Analytics/docs/16-domain-model.md` and docs 10–12.
- Data and replay flow: `Analytics/docs/03-data-and-processing.md` and `Analytics/docs/05-runtime-flows.md`.
- Open decisions and their status: `Analytics/docs/08-risks-and-open-issues.md` and the ADR Status sections.
- Formal evaluation output schemas: `arka_dataset/output_contract/`. This plan does not alter them.

When implementation exposes a conflict, update the owning contract or ADR through the project's decision process; record stage progress here only after its exit gate has evidence.
