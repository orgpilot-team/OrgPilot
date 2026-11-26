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

> **Implementation source note.** This document and `16-domain-model.md` define the Scheduler and Replay Runner boundaries used for implementation. The DSL is a visual overview. This container coordinates no invariant-bearing aggregate, so the merges below remove stateless helpers and a duplicated parity owner.

## Component Map (target)

Replay Command (includes the simulation clock and evaluation profile loading), Run Status Client, Scripted Manager Input Adapter, and Acceptance Test Harness (includes KPI parity checking).

Removed as separate components: Simulation Clock and Evaluation Profile Loader (stateless helpers folded into Replay Command), KPI Parity Validator (folded into Acceptance Test Harness, which already owns the SQLite boundary).

## Internal Relationships

All internal calls are in-process. The replay command derives the pinned business date, loads the profile, starts or resumes one simulated day, and starts acceptance only after terminal product state. Parity is one check inside the harness, not a separate component.

## External Relationships

The container reads the OrgPilot Input Dataset, calls the Backend API over authenticated HTTPS/JSON, and stores acceptance results in PostgreSQL.

## Component Sections

<a id="replay-command"></a>

### Replay Command

- **DSL identifier:** `replayCommandV2`;
- **Display name:** Replay Command.
- **Purpose:** Sequence a replay range, derive the pinned business date, load the evaluation profile, and resume from the last terminal day.
- **Responsibilities:** Resolve day semantics without host clock, validate and supply the versioned profile, submit scripted input, start runs, and start terminal checks.
- **Inputs:** Versioned replay range, evaluation calendar rules, profile identifier, and evaluator command.
- **Outputs:** Ordered simulated-day execution and final replay status. This component absorbs Simulation Clock and Evaluation Profile Loader (`simulationClockV2`, `evaluationProfileLoaderV2` in the current DSL): both are stateless derivations of pinned evaluation input with no owned state.
- **Owned state:** Replay progress in persisted product and acceptance records.
- **Dependencies:** OrgPilot Input Dataset, Run Status Client, Scripted Manager Input Adapter, and Acceptance Test Harness.
- **Security boundary:** Only versioned evaluation input is accepted; profile values do not change product architecture decisions.
- **Forbidden responsibilities:** Run product stages, use host time as product time, invent missing thresholds, or change product configuration.
- **Failure behavior:** Stop at the failed day and preserve the resume point.
- **Idempotency:** Replay range and day key make resume safe.
- **Observability:** Record range, day, run ID, status, and trace ID.
- **Related ADRs:** ADR-0011, ADR-0012, ADR-0018.
- **Open issues:** Scheduler process type remains open.

<a id="run-status-client"></a>

### Run Status Client

- **DSL identifier:** `runStatusClientV2`;
- **Display name:** Run Status Client.
- **Purpose:** Start and monitor runs through the Backend Run Coordinator.
- **Responsibilities:** Send authenticated start and status requests and wait for terminal state.
- **Inputs:** Pinned day, run options, identity, and existing run ID.
- **Outputs:** Run ID and authorized run status.
- **Owned state:** None.
- **Dependencies:** Backend Run Coordinator.
- **Security boundary:** It uses the product API and does not access PostgreSQL directly.
- **Forbidden responsibilities:** Create stage jobs or infer terminal state locally.
- **Failure behavior:** Preserve the run ID and allow a later status retry.
- **Idempotency:** Start key prevents duplicate run creation.
- **Observability:** Record request, run ID, status, latency, and trace ID.
- **Related ADRs:** ADR-0011, ADR-0018.
- **Open issues:** None.

<a id="acceptance-test-harness"></a>

### Acceptance Test Harness

- **DSL identifier:** `acceptanceTestHarnessV2`;
- **Display name:** Acceptance Test Harness.
- **Purpose:** Run replay, regression, leakage, performance, contract, and KPI parity checks.
- **Responsibilities:** Load limits, verify terminal state, run suites, execute read-only reference SQL on embedded SQLite, compare against PostgreSQL results under approved tolerances, and store receipts.
- **Inputs:** Terminal run, evaluation profile, reference contracts, reference SQLite assets, and PostgreSQL results.
- **Outputs:** Acceptance results, per-KPI parity results, and Parity Receipts. This component absorbs KPI Parity Validator (`kpiParityValidator` in the current DSL): parity is one acceptance check inside the harness, which already owns the SQLite boundary. A second owner duplicated the responsibility (ADR-0016 amended).
- **Owned state:** Acceptance and parity results in PostgreSQL; temporary SQLite is inside the harness only.
- **Dependencies:** Replay Command, Run Status Client, and PostgreSQL results.
- **Security boundary:** Reference files and SQL are read-only.
- **Forbidden responsibilities:** Act as product runtime, publish product output, use SQLite in product runtime, or change reference SQL.
- **Failure behavior:** Record failed checks with evidence and keep product state unchanged.
- **Idempotency:** Run ID, suite version, and profile version identify the result.
- **Observability:** Record suite, check, result, duration, receipt, and trace ID.
- **Related ADRs:** ADR-0002, ADR-0011, ADR-0012, ADR-0016.
- **Open issues:** Performance thresholds come from the selected profile.

<a id="scripted-manager-input-adapter"></a>

### Scripted Manager Input Adapter

- **DSL identifier:** `scriptedManagerInputAdapter`;
- **Display name:** Scripted Manager Input Adapter.
- **Purpose:** Submit versioned replay inputs through the same Backend API as interactive input.
- **Responsibilities:** Read pinned manager input, create an authenticated product request, and preserve order and identity.
- **Inputs:** Versioned scripted manager input and replay day.
- **Outputs:** Backend API request and accepted result or job ID.
- **Owned state:** None.
- **Dependencies:** OrgPilot Input Dataset and Backend API.
- **Security boundary:** Scripts do not bypass authentication, authorization, or validation.
- **Forbidden responsibilities:** Write product state directly or call internal Backend components.
- **Failure behavior:** Record the rejected input and stop or continue under the evaluation profile.
- **Idempotency:** Script event ID and replay day prevent duplicate submission.
- **Observability:** Record event ID, request type, result, job ID, and trace ID.
- **Related ADRs:** ADR-0010, ADR-0011, ADR-0012, ADR-0018.
- **Open issues:** None.

## Consolidation log (implementation model)

The following former components are intentionally absent from the implementation model. See `16-domain-model.md` §6 for the reasoning.

| Removed component | Disposition |
|---|---|
| Simulation Clock | Merged into Replay Command (stateless date derivation) |
| Evaluation Profile Loader | Merged into Replay Command (stateless profile load) |
| KPI Parity Validator | Merged into Acceptance Test Harness (single owner of the SQLite boundary; ADR-0016 amended) |

## Container-level Open Issues

- The final .NET Console or Worker Service choice remains open in ADR-0018.
