# Scheduler and Replay Runner components

## Purpose and Scope

The Scheduler and Replay Runner controls simulated time, replay ranges, evaluation profiles, and acceptance checks. It uses the Backend API for product run control.

## Runtime Technology

.NET 10 Console or Worker Process. The final process type remains open in ADR-0018.

## Trust Boundary

Replay input and evaluation configuration are versioned inputs. The Scheduler does not write product state directly except for acceptance results defined by the harness.

## Allowed Responsibilities

- Sequence replay days and pin the simulated clock.
- Start and monitor product runs through the Backend API.
- Run acceptance, regression, leakage, performance, contract, and KPI parity checks.

## Forbidden Responsibilities

- Replace product job durability or call Worker components directly.
- Use SQLite as a product database.
- Bypass the Backend API for scripted manager input.

## Component Map

Replay Command coordinates Simulation Clock, Evaluation Profile Loader, Run Status Client, Scripted Manager Input Adapter, and Acceptance Test Harness. The harness uses KPI Parity Validator.

## Internal Relationships

All internal calls are in-process. The replay command starts or resumes one simulated day and starts acceptance only after terminal product state.

## External Relationships

The container reads the DIDRAH Input Dataset, calls the Backend API over authenticated HTTPS/JSON, and stores acceptance results in PostgreSQL.

## Component Sections

<a id="replay-command"></a>

### Replay Command

- **DSL identifier:** `replayCommandV2`; **Display name:** Replay Command.
- **Purpose:** Sequence a replay range and resume from the last terminal day. **Responsibilities:** Load range, pin time and profile, submit scripted input, start runs, and start terminal checks. **Inputs:** Versioned replay range and evaluator command. **Outputs:** Ordered simulated-day execution and final replay status.
- **Owned state:** Replay progress in persisted product and acceptance records. **Dependencies:** Simulation Clock, Evaluation Profile Loader, Run Status Client, Scripted Manager Input Adapter, and Acceptance Test Harness. **Security boundary:** Only versioned evaluation input is accepted. **Forbidden responsibilities:** Run product stages or use host time as product time.
- **Failure behavior:** Stop at the failed day and preserve the resume point. **Idempotency:** Replay range and day key make resume safe. **Observability:** Record range, day, run ID, status, and trace ID. **Related ADRs:** ADR-0011, ADR-0012, ADR-0018. **Open issues:** Scheduler process type remains open.

<a id="simulation-clock"></a>

### Simulation Clock

- **DSL identifier:** `simulationClockV2`; **Display name:** Simulation Clock.
- **Purpose:** Derive the pinned business date and source cutoff. **Responsibilities:** Resolve evaluation day semantics without host-clock dependence. **Inputs:** Replay day and evaluation calendar rules. **Outputs:** Business date and source cutoff.
- **Owned state:** None. **Dependencies:** Replay Command. **Security boundary:** Pinned evaluation input is authoritative. **Forbidden responsibilities:** Read product state or advance time by wall clock.
- **Failure behavior:** Reject an invalid or ambiguous day. **Idempotency:** Same day and rules give the same result. **Observability:** Record input day, derived cutoff, rule version, and trace ID. **Related ADRs:** ADR-0011, ADR-0012. **Open issues:** None.

<a id="evaluation-profile-loader"></a>

### Evaluation Profile Loader

- **DSL identifier:** `evaluationProfileLoaderV2`; **Display name:** Evaluation Profile Loader.
- **Purpose:** Load selected evaluation limits, thresholds, and run options. **Responsibilities:** Validate and supply one versioned profile. **Inputs:** Profile identifier and versioned evaluation data. **Outputs:** Validated evaluation profile or rejection.
- **Owned state:** None. **Dependencies:** DIDRAH Input Dataset. **Security boundary:** Profile values do not change product architecture decisions. **Forbidden responsibilities:** Invent missing thresholds or change product configuration.
- **Failure behavior:** Stop the command when the profile is missing or invalid. **Idempotency:** Profile ID and version identify one result. **Observability:** Record profile version, validation result, and trace ID. **Related ADRs:** ADR-0011, ADR-0012, ADR-0016. **Open issues:** None.

<a id="run-status-client"></a>

### Run Status Client

- **DSL identifier:** `runStatusClientV2`; **Display name:** Run Status Client.
- **Purpose:** Start and monitor runs through the Backend Run Coordinator. **Responsibilities:** Send authenticated start and status requests and wait for terminal state. **Inputs:** Pinned day, run options, identity, and existing run ID. **Outputs:** Run ID and authorized run status.
- **Owned state:** None. **Dependencies:** Backend Run Coordinator. **Security boundary:** It uses the product API and does not access PostgreSQL directly. **Forbidden responsibilities:** Create stage jobs or infer terminal state locally.
- **Failure behavior:** Preserve the run ID and allow a later status retry. **Idempotency:** Start key prevents duplicate run creation. **Observability:** Record request, run ID, status, latency, and trace ID. **Related ADRs:** ADR-0011, ADR-0018. **Open issues:** None.

<a id="acceptance-test-harness"></a>

### Acceptance Test Harness

- **DSL identifier:** `acceptanceTestHarnessV2`; **Display name:** Acceptance Test Harness.
- **Purpose:** Run replay, regression, leakage, performance, contract, and parity checks. **Responsibilities:** Load limits, verify terminal state, run suites, and store receipts. **Inputs:** Terminal run, evaluation profile, reference contracts, and reference SQLite assets. **Outputs:** Acceptance results and receipts.
- **Owned state:** Acceptance results in PostgreSQL; temporary SQLite is inside the harness only. **Dependencies:** Evaluation Profile Loader, Run Status Client, PostgreSQL, and KPI Parity Validator. **Security boundary:** Reference files are read-only. **Forbidden responsibilities:** Act as product runtime or publish product output.
- **Failure behavior:** Record failed checks with evidence and keep product state unchanged. **Idempotency:** Run ID, suite version, and profile version identify the result. **Observability:** Record suite, check, result, duration, receipt, and trace ID. **Related ADRs:** ADR-0002, ADR-0011, ADR-0012, ADR-0016. **Open issues:** Performance thresholds come from the selected profile.

<a id="kpi-parity-validator"></a>

### KPI Parity Validator

- **DSL identifier:** `kpiParityValidator`; **Display name:** KPI Parity Validator.
- **Purpose:** Compare 55 SQLite reference results with PostgreSQL results. **Responsibilities:** Run read-only reference SQL in the harness, compare values under approved tolerances, and store receipts. **Inputs:** Reference SQLite data and SQL, PostgreSQL results, and tolerance profile. **Outputs:** Per-KPI parity results and Parity Receipt.
- **Owned state:** Parity Receipts in PostgreSQL; temporary SQLite state stays in the harness. **Dependencies:** Acceptance Test Harness and PostgreSQL results. **Security boundary:** Reference SQL and data are read-only. **Forbidden responsibilities:** Use SQLite in product runtime or change reference SQL.
- **Failure behavior:** Mark parity failure with exact KPI evidence. **Idempotency:** Dataset, SQL, result, and validator versions identify one comparison. **Observability:** Record KPI, versions, difference, tolerance, result, and trace ID. **Related ADRs:** ADR-0002, ADR-0011, ADR-0016. **Open issues:** None.

<a id="scripted-manager-input-adapter"></a>

### Scripted Manager Input Adapter

- **DSL identifier:** `scriptedManagerInputAdapter`; **Display name:** Scripted Manager Input Adapter.
- **Purpose:** Submit versioned replay inputs through the same Backend API as interactive input. **Responsibilities:** Read pinned manager input, create an authenticated product request, and preserve order and identity. **Inputs:** Versioned scripted manager input and replay day. **Outputs:** Backend API request and accepted result or job ID.
- **Owned state:** None. **Dependencies:** DIDRAH Input Dataset and Backend API. **Security boundary:** Scripts do not bypass authentication, authorization, or validation. **Forbidden responsibilities:** Write product state directly or call internal Backend components.
- **Failure behavior:** Record the rejected input and stop or continue under the evaluation profile. **Idempotency:** Script event ID and replay day prevent duplicate submission. **Observability:** Record event ID, request type, result, job ID, and trace ID. **Related ADRs:** ADR-0010, ADR-0011, ADR-0012, ADR-0018. **Open issues:** None.

## Container-level Open Issues

- The final .NET Console or Worker Service choice remains open in ADR-0018.
