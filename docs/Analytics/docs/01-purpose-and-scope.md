# Purpose and scope

OrgPilot is a bounded management assistant. It produces traceable management reports from supplied organization data. It also supports scoped questions, manager decisions, and follow-up work.

## Source policy

The active architecture sources are:

- `docs/Analytics/workspace.dsl`
- `docs/Analytics/docs/`
- `docs/Analytics/adrs/`

The official project brief, TA clarifications, and machine-readable evaluation contracts verify these sources. A historical document is not an active architecture source. An unclear statement becomes an open decision. It does not become an accepted requirement.

The ADR Status field controls each decision. This documentation does not change an ADR status.

## In scope

- Process supplied nightly data in business-date order.
- Validate schemas and normalize accepted source records.
- Calculate approved KPIs with registered SQL.
- Reconstruct three business workflows and their stage status.
- Detect, rank, and escalate deterministic signals.
- Publish a validated report for each active manager.
- Support scoped interactive questions and document decision cards.
- Record human-confirmed decisions and deterministic follow-up evidence.
- Export validated contract output below `OUTPUT_DIR`.
- Preserve evidence for replay, audit, recovery, and evaluation.
- Correlate runtime work with OpenTelemetry and optional Langfuse telemetry.

## Out of scope

- Automated execution of an organization decision or action
- Sending a manager message without explicit human action
- KPI calculation, authorization, publication, or configuration activation by the language model
- Arbitrary Agent Runtime SQL on business data
- A product SQLite database or SQLite runtime container
- A new microservice, message broker, Kubernetes deployment, or service mesh
- An observability backend other than OpenTelemetry and Langfuse

## Agent Runtime boundary

The deterministic core owns KPI calculation, workflow reconstruction, signal rules, authorization, validation, publication, and export. The bounded agent can analyze authorized evidence and create a narrative or decision-card candidate. It cannot widen scope, confirm a decision, activate configuration, publish output, or change database policy.

The Backend API commits a durable Agent Job to PostgreSQL before it returns `job_id`. An authenticated wake-up is optional and is only a latency hint. The Agent Runtime claims the job from PostgreSQL, reloads the pinned scope and evidence references, and records a candidate or explicit failure. Business evidence is obtained through the Backend API Evidence Service and Query Gateway.

## Data and contract boundaries

PostgreSQL 18 is the only product database. SQLite runs only inside the Acceptance Test Harness as the reference oracle for KPI parity. The reference SQL, KPI Dictionary, input contracts, and output contracts are read-only architecture constraints.
