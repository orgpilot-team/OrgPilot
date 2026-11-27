# Backend development stages

This is the ordered implementation plan for the **first four stages only**. It is a progress record, not a new architecture decision or a replacement for the accepted contracts in `Analytics/docs/15-implementation-contract.md`, `Analytics/docs/16-domain-model.md`, and the ADRs. Update a stage's status and evidence links when work is completed; extend the table only when later stages are planned.

The first four stages build the deterministic backend and its replay mechanism. They do not claim that the complete evaluation submission, authenticated product API, Agent Runtime, or Web Application is finished.

The repository [completion criteria](CODING_CONVENTIONS.md#completion-criteria) govern each stage from design through its exit gate.

| No. | Stage | Main implementation scope | Completion evidence | Status |
|---:|---|---|---|---|
| 1 | Foundation and persistence (Walking Skeleton) | Minimal runnable .NET processes; module boundaries; PostgreSQL 18; migrations; shared contracts and infrastructure conventions | The foundational services start together, database connectivity and migrations work, and module/process boundaries are visible in code | Historical completion recorded on 2026-11-26 |
| 2 | Intake, snapshots, and KPIs | Versioned source intake; protected raw archive; canonical facts; data issues; immutable snapshots; KPI definitions, calculations, and SQLite parity | Pinned-day ingestion is repeatable; missing/late/duplicate cases behave correctly; every activated KPI translation has a passing Parity Receipt | Functional acceptance passed. Architecture and skill conformance review pending. |
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

**Historical verification evidence (2026-11-26):**

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

**Verification evidence (2026-11-27; initial implementation):**

- .NET SDK 10.0.303: solution build passed with zero warnings and errors. Both Stage 2 contexts report no pending EF Core model changes, and both idempotent SQL migration scripts were generated successfully. The existing migration DDL and migration IDs remain unchanged.
- The development regression harness (`--check-dev-dataset`) passed all 86 checks with zero failures on two executions: all 91 drop manifests and their listed records normalize; day 66 missing sources, day 67 late arrival, day 70 CRM correction, day 76 duplicate orders, and day 82 schema aliases behave as expected. The final snapshot contains 223,558 deduplicated canonical facts; all 55 SQLite reference queries execute repeatably. The harness also checks the accepted parity comparison tolerance, nulls, and row populations.
- The Configuration Service now exposes approved active version references for the report day. Snapshot pinning records the exact KPI-definition IDs, organization revision, configuration candidate IDs, separate manager-priority versions, and baseline dictionary/calendar/target hashes. Regression checks confirmed same-day exclusion, D+1 selection, and creation of a distinct immutable snapshot when configuration changes.
- Additional isolated fixtures passed: invalid schema and numeric records, future-dated records, changed source bytes with preservation of the original archive, and a late source containing invalid records that must remain missing.
- Docker Compose configuration validation passed. On 2026-11-27, the Stage 2 migrations were applied; rebuilt `database-migrate` and `worker-database-migrate` jobs both exited with code 0, and the corrected Worker image started successfully. A migration audit found exactly one known and applied migration per context (Foundation, Configuration, Stage2), no unknown or pending migrations, and no pending model changes. The three independent history tables remain in the migrator-owned `foundation` schema; no extra migration or history table was found.
- The first persisted acceptance run exposed one boundary mismatch in `K_RSP_FRT_2H_PCT`. Ticket `TK004530` (day-63 source files) runs from 17:20 to 19:20 on 2026-09-23. SQLite computed `2.0000000037252903` hours and included 22 of 79 responses (27.8%); the original PostgreSQL translation computed `1.99999999999999999992` and included 23 (29.1%). Focused diagnostics reproduced both original result hashes across all 90 dates. The historical SQLite inspection file and comparison are under `test-results/kpi-rsp-diagnostic-20261127/`.
- `BaselineKpiSql` now preserves SQLite's separate binary64 Julian-day conversions for that threshold comparison, using PostgreSQL `EXTRACT(JULIAN)` with the noon-origin adjustment. Twelve database-backed regression cases passed, covering below/equal/above two hours, midnight crossings, a leap day, null responses, and team filtering. The reference SQL is unchanged. The new definition is `d425102fa7405a77701193ef1eb1648d5535e81c8c5b16f41bae63bf7041b0a7`; the previous version and its failing receipt remain historical evidence.
- The corrected persisted acceptance run exited with code 0: all 55 baseline KPIs have passing receipts and query runs for snapshot `11911b19bb2444b950ca83c998159e75514607a6f3a4931c7f262487809b5264`, repeated PostgreSQL calculations matched, and all six persisted configuration checks passed (idempotency, unapproved exclusion, same-day exclusion, D+1 activation, missing-receipt rejection, and invalid-organization rejection). Fixture candidate and approval writes were rolled back. The existing 91 intake batches were reused. Evidence: `test-results/stage2-db-20261127/acceptance-corrected.log` and `test-results/migration-audit-20261127/evidence.json`.

To rerun the development regression checks without PostgreSQL:

```powershell
$env:DATA_DIR = (Resolve-Path docs/arka_dataset).Path
$env:Archive__RootPath = Join-Path (Get-Location).Path ('test-results/stage2-dev-' + [guid]::NewGuid().ToString('N'))
dotnet run --project src/SchedulerReplay/Acceptance -- --check-dev-dataset
```

For database acceptance, start the development Compose stack with migrations applied. From the repository root set `DATA_DIR` and `Archive__RootPath` as above and supply `ConnectionStrings__Product` (Worker credentials), `ConnectionStrings__Configuration` (Backend API credentials), and `ConnectionStrings__Parity` (acceptance-only write credential; never an API or Worker runtime principal). In a local development database the separate migrator credential can be used for acceptance receipt writes. Run:

```powershell
dotnet run --project src/SchedulerReplay/Acceptance -- --report-day 91 --cutoff 2026-10-20 --check-configuration
```

The persisted acceptance path re-ingests and reloads the immutable snapshot, checks all 55 baseline definitions and any pinned replacements against SQLite, writes receipts, compares repeated PostgreSQL calculation results, and runs a rolled-back D+1 approval/validation fixture. Its fixture authority exists only in the acceptance project, not the product API.

For the focused PostgreSQL/SQLite two-hour boundary regression, set the Worker `ConnectionStrings__Product` and run `dotnet run --project src/SchedulerReplay/Acceptance -- --check-kpi-sql`. This check uses read-only PostgreSQL CTEs and an in-memory SQLite fixture.

The product-day timing check uses [`deploy/compose.stage2-check.yaml`](../deploy/compose.stage2-check.yaml). Both PostgreSQL and the acceptance process share CPUs 0-3, with separate 2 GiB and 12 GiB limits and no additional swap, GPU, or internet access. It clones the development business schemas into a temporary PostgreSQL instance. Given a passing snapshot, `--check-performance SNAPSHOT_ID` ingests the latest drop, reloads historical batches, pins configuration, rebuilds and reloads the snapshot, builds its projection, and calculates every pinned KPI through the receipt-gated product path. It repeats that path twice, requires identical result hashes, and fails if either pass exceeds 300 seconds. Historical ingestion and parity certification are prerequisites rather than daily work; SQLite is excluded from this timing.

To repeat the isolated timing check from the repository root after persisted acceptance succeeds (stop if any Docker command fails):

```powershell
$env:STAGE2_EVIDENCE_DIR = (New-Item -ItemType Directory -Force test-results/stage2-timing).FullName
$env:STAGE2_DATA_DIR = (Resolve-Path docs/arka_dataset).Path
$env:STAGE2_ARCHIVE_DIR = (Resolve-Path test-results/stage2-db-20261127/archive).Path
$env:STAGE2_SNAPSHOT_ID = '0f338c1976e4f7cfb65eed0668525c1230b5d12f33d162554dca27a70a1e0b6b'
docker compose exec -T postgresql pg_dump -U orgpilot_admin -d orgpilot --no-owner --no-comments --schema=configuration --schema=intake --schema=snapshots --schema=kpi | Set-Content -Encoding utf8 (Join-Path $env:STAGE2_EVIDENCE_DIR 'database.sql')
$benchmarkCompose = @('--env-file', '.env', '-p', 'orgpilot-stage2-check', '-f', 'deploy/compose.stage2-check.yaml')
docker compose @benchmarkCompose config --quiet
docker compose @benchmarkCompose build acceptance
docker compose @benchmarkCompose up -d --wait postgresql
docker compose @benchmarkCompose exec -T postgresql psql -X -q -v ON_ERROR_STOP=1 -U orgpilot_admin -d orgpilot -f /seed/database.sql
docker compose @benchmarkCompose up --no-build --no-deps --abort-on-container-exit --exit-code-from acceptance acceptance
docker compose @benchmarkCompose down
```

The timing database is held in `tmpfs` and discarded when the isolated stack stops; the original database and raw archive remain available. This measures Stage 2 on the largest supplied snapshot, including all historical KPI points. Later workflow, model, and publication stages must fit within the remaining daily budget when implemented.

**Follow-up verification (2026-11-27):**

- Review identified that the combined organization and policy hashes did not retain the individual archive addresses needed to reconstruct historical inputs. New snapshots now persist all eleven named archive references (organization, policy, KPI dictionary, calendar, and monthly targets). Projection and reference SQL are restored from those pinned inputs; the original snapshot format and IDs remain readable. No database migration, reference SQL or source data changes were necessary.
- Rebuilt Debug (non-incremental) and Release with zero warnings and errors. All 90 development regression checks passed in 98 seconds on the local host, including the four additional checks for serialized snapshot references, hash-verified reopening of all eleven inputs, new snapshot identity after a policy change, and rejection of inconsistent pins. The 223,558 deduplicated canonical facts and all 55 repeatable SQLite queries remain unchanged. Evidence: `test-results/stage2-review-20261127/regression.log`.
- All three EF Core contexts reported no pending model changes, and their idempotent migration SQL scripts were generated successfully. Docker Compose configuration validation passed. At this earlier follow-up attempt, live Docker API access was denied and Npgsql connection to the configured local PostgreSQL port 5432 failed with Windows socket error 10013 before authentication. The completion run below subsequently resolved the environment-access block and verified the extended snapshot format against PostgreSQL.

**Functional acceptance evidence (2026-11-27):**

- Durable summary: [`verification/stage2-20261127.json`](verification/stage2-20261127.json). It records counts, snapshot and result hashes, enforced resource limits, per-phase timings, and SHA-256 hashes of the raw evidence. The local raw artifacts remain excluded from Git.
- Renewed PostgreSQL acceptance after the archive-reference correction passed with exit code 0. Snapshot `0f338c1976e4f7cfb65eed0668525c1230b5d12f33d162554dca27a70a1e0b6b` has all eleven archived input references, 55 passing Parity Receipts and 55 stored Query Runs; the six D+1 configuration checks passed and the fixture candidates and approvals were rolled back. The twelve focused PostgreSQL/SQLite boundary cases also passed. Evidence: `test-results/stage2-completion-20261127/acceptance.log`, `acceptance-summary.json`, and `persisted-evidence.txt` in that evidence directory.
- The isolated Docker performance check on the largest supplied pinned day (report day 91, 223,558 canonical facts and 55 KPIs) completed twice in **201.090 seconds and 178.702 seconds**, both below the 300-second budget, with identical result hashes and exit code 0. The local reference-resource simulation shared four logical CPUs and capped total container memory at 14 GiB without swap, GPU, or external network; this is not a measurement on the instructor's physical host. Evidence: `test-results/stage2-completion-20261127/performance.log`, `performance-exit.json`, and `resources.json` in that evidence directory.
- The slowest KPI, `K_WH_DAMAGE_BY_CAT_7D`, took 51.27 and 41.97 seconds. The remaining Stage 2 budget on the slower run is about 99 seconds; later stages must re-verify the entire product-day budget, including workflow reconstruction, agent and publication work. Original missing-file row counts are not available in the supplied manifests; a later valid file is arrival evidence, but arbitrary partial late coverage cannot be proven from those manifests alone.
- The acceptance-only Docker target published successfully after excluding referenced API/Worker `appsettings.json` files from the harness output. API, Worker, and migration images rebuilt successfully; API and Worker were restarted with the corrected code. API readiness is healthy and Worker database/archive startup checks passed. Existing database/archive volumes were preserved; no new schema migration was introduced or needed.

Stage 2 passed its recorded functional, parity, and performance checks for the supplied development dataset. The architecture and skill conformance review is pending.

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
