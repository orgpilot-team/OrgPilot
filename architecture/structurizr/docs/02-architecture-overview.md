# Architecture overview

DIDRAH uses a modular monolith. The Backend API, Background Worker, and Scheduler and Replay Runner use one modular codebase. They run as separate processes.

The architecture has six product containers:

1. **Web Application** provides the Persian right-to-left user interface.
2. **Backend API** authenticates requests, applies access rules, controls bounded analysis, validates results, and delivers reports.
3. **Background Worker** runs deterministic ingestion, snapshot, KPI, workflow, signal, and report-evidence jobs.
4. **Scheduler and Replay Runner** controls simulated time, replay, and acceptance tests.
5. **PostgreSQL** stores product state, analytical results, jobs, access policy, checkpoints, and audit records.
6. **Protected File Archive** stores original source files and manager uploads with their hashes and manifests.

The system uses these external dependencies:

- DIDRAH Input Dataset
- Identity Provider
- Language Model Provider

The DIDRAH Input Dataset is one versioned `DATA_DIR` package. It contains nightly drops, manifests, manager inputs, uploads, configuration, and history. Development and hidden evaluation datasets use the same structure.

The deterministic core is outside the agent. It owns KPI calculation, workflow reconstruction, signal rules, authorization, validation, and publication. The bounded agent analyzes only authorized evidence and can produce a narrative candidate or a decision-card candidate.

The main nightly path is:

```text
Scheduler and Replay Runner
  -> Backend Run Coordinator
  -> PostgreSQL job plan
  -> Background Worker stages
  -> manager-scoped Evidence Package and Canonical Report JSON
  -> bounded Agent Job
  -> deterministic validation
  -> independent publication
```
