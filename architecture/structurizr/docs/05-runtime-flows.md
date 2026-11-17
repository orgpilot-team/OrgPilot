# Runtime flows

## Nightly report flow

The Replay Command selects a business day. The Simulation Clock supplies the business date and cutoff. The Evaluation Profile Loader supplies acceptance limits and run options.

The Run Status Client asks the Backend Run Coordinator to create a pinned run and its complete job plan. PostgreSQL stores job dependencies and manager order.

The Background Worker claims ready deterministic jobs. It runs ingestion, snapshot, KPI, workflow, signal, and report-evidence stages. A Report Evidence Job creates one manager-scoped Evidence Package and Canonical Report JSON.

The Agent Job Runner claims one ready Agent Job. It reloads the pinned manager scope. The bounded agent can produce a Persian narrative candidate. It cannot change the canonical numbers or widen the scope.

The Output Validator checks schema, evidence, scope, report rules, and model failure state. The Publisher publishes valid manager reports independently. A required manager failure makes the day `incomplete`, but it does not remove valid reports for other managers.

## Interactive question flow

The Web Application sends an authenticated request to the Backend API. The Manager Request Router selects the fixed request handler. The Authorization Service defines the permitted scope. The Evidence Service and Query Gateway retrieve authorized evidence. The SQL AST Guard rejects unsafe SQL. The Output Validator checks the answer before delivery.

## Document decision flow

The Document Processing Runner stores the original upload and calls the deterministic Document Parser. After a successful parse, it creates a Document Analysis Job. The bounded agent produces a decision-card candidate. The Output Validator checks the candidate. The Decision Confirmation Service stores the valid card for manager review. Only a confirmed card can enter Decision and Follow-Up.

## Replay and evaluation

Replay runs days in order and resumes from the last terminal day. The Acceptance Test Harness runs replay, hidden-data, regression, leakage, performance, cost, and output-contract checks outside the daily publication path.
