# Runtime flows

## Agent Job lifecycle and persistence

PostgreSQL is the authoritative job and state store for all report, interactive, and document-analysis Agent Jobs. A job is committed before any wake-up and carries an idempotency key plus pinned actor, policy, scope, and workload-specific input references. The Agent Runtime Runner claims a Ready job under a lease and records attempts and terminal state. A wake-up may reduce latency, but polling and lease recovery prevent work from being lost. Runtime outcome persistence and deterministic validation are separate states; the UI or publisher consumes only the validated result.

## Nightly report flow

The Replay Command selects a business day, derives the pinned business date and cutoff, and loads acceptance limits and run options. In the implementation model, the former Simulation Clock and Evaluation Profile Loader are functions inside the Replay Command (doc 16 §6.1).

The Run Status Client asks the Backend Run Coordinator to create a pinned run and its complete job plan. PostgreSQL stores job dependencies, manager order, and durable job state.

The Background Worker claims ready deterministic jobs. It runs ingestion, snapshot, KPI, workflow, signal, and report-evidence stages. A Report Evidence Job creates one manager-scoped Evidence Package and Canonical Report JSON, then unlocks its preplanned Agent Job.

One PostgreSQL-backed Agent Job Runner in Agent Runtime claims and leases every Ready report, interactive, or document-analysis Agent Job. It reloads the pinned actor, scope, policy, and workload-specific inputs from PostgreSQL, runs the bounded graph, persists the candidate or explicit failure, and only then submits the outcome for deterministic validation. The bounded agent cannot change canonical numbers or widen scope.

Backend producers commit an idempotent job before optionally sending an authenticated wake-up containing only the job ID. The wake-up is a latency hint, not a payload or source of truth. Runtime polling and lease recovery find jobs even when a wake-up is lost. The Web Application receives the job ID and polls the authorized Backend status API; queued/running work remains pending, and only a persisted validated result is presented as ready for review or delivery.

The Output Validator checks schema, evidence, scope, report rules, and model failure state. The Publisher publishes valid manager reports independently. A required manager failure makes the day `incomplete`, but it does not remove valid reports for other managers.

## Validation and submission export flow

Output Validator checks the candidate against the read-only reference schema. It also checks actor scope, evidence references, path containment, and output rules. It records a Validation Receipt with `trace_id`.

Publisher records the valid product result in PostgreSQL. Submission Exporter reads only a validated final result. It directly joins `OUTPUT_DIR` with `briefs/day_XXX/<manager_id>.json` or `qa/<question_id>.json`. It resolves the path, verifies containment, rejects absolute paths and `..`, writes a temporary file on the same filesystem, flushes and closes it, and performs an atomic rename. It records the content hash, relative path, `trace_id`, and Export Receipt.

For `OUTPUT_DIR=/submission`, the exporter writes directly below `/submission`. It does not create `/submission/submission`.

The complete Decision Effect remains an internal versioned PostgreSQL record. Export uses only fields and values that the reference output schema permits.

## Interactive question and manager decision flow

The Web Application sends an authenticated request to the Backend API. The fixed handler is selected by in-process dispatch (the former Manager Request Router is a function, doc 16 §6.2) and the Authorization Service pins the permitted scope. The Agent Runtime Gateway commits an idempotent interactive Agent Job to PostgreSQL with actor, policy, scope, request, and conversation references. It returns the committed job ID to the request handler, which returns it to the UI; the Gateway may also send the Agent Runtime an authenticated wake-up containing only the job ID.

The Agent Runtime Runner claims and leases the job from PostgreSQL, reloads its canonical inputs and pinned scope, and invokes the bounded graph. Conversation and evidence tools use their explicitly authorized Backend services. The Runner persists its candidate or explicit execution failure before submitting the outcome to Output Validator. The validator persists its receipt and transitions the job to validated or rejected. The UI polls the Backend status API, which returns only the owning manager's authorized status and validated result reference. Editing an interactive decision card creates a new idempotent revision job through the Agent Runtime Gateway; confirm, edit, or reject remains a human command, and only a confirmed card enters Decision and Follow-Up.

## Document decision flow

The Document Processing Runner archives the original upload and runs deterministic parsing internally (the former Document Parser is a function inside it, doc 16 §6.1). On unsupported or invalid content, parsing returns an explicit failure and no Agent Job is created. On successful parsing, immutable fragments and a parse receipt are stored, then the Document Processing Runner commits one durable document-analysis Agent Job with pinned actor, scope, policy, and fragment references. It returns the job ID to the request handler and may request a best-effort job-ID-only wake-up through the Gateway; the Runtime Runner still claims canonical job data from PostgreSQL. The same Agent Runtime Runner claims and leases the job, executes the bounded document graph, and persists its candidate or execution failure before validation. The UI polls authorized job status. Decision and Follow-Up presents only a valid card for manager review. A manager edit creates a revision through the Document Processing Runner using the approved fragments; only a confirmed card can enter the decision record.

## Replay and evaluation

Replay runs days in order and resumes from the last terminal day. The Acceptance Test Harness runs replay, SQLite-to-PostgreSQL KPI parity, hidden-data, regression, leakage, performance, cost, and output-contract checks outside the daily publication path.

## Trace correlation

REST calls propagate W3C `traceparent`. Durable jobs persist trace context or use a Span Link when asynchronous processing starts. Run, Job, Validation Receipt, Publication Receipt, Parity Receipt, and Export Receipt records include `trace_id`. Telemetry export is optional and fail-open. It does not replace PostgreSQL job state or receipts.
