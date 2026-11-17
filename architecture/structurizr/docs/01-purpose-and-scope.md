# Purpose and scope

DIDRAH is a bounded management assistant. It produces traceable management reports from supplied organization data. It also supports scoped questions, manager decisions, and follow-up work.

The system has these primary goals:

- Process the supplied nightly data in the correct business-date order.
- Calculate approved KPIs with registered SQL.
- Reconstruct three business workflows and their stage status.
- Detect, rank, and escalate deterministic signals.
- Publish a validated report for each active manager.
- Support scoped interactive questions and document decision cards.
- Preserve evidence for replay, audit, and evaluation.

The first delivery has these limits:

- The system does not execute an organization decision.
- The system does not send a manager message on behalf of a user.
- The language model does not calculate KPIs or create access policy.
- The language model does not have direct database or file access.
- PostgreSQL is the only product database.
- SQLite is only a reference oracle for KPI parity tests.

The architecture status is `Proposed`. Accepted decisions and open boundaries are in the architecture decision records and the active control register.

Sources:

- `Docs/final review/architecture-control-register-v3.md`
- `Docs/final review/proposed-architecture.md`
- `Docs/final review/to-be-architecture.md`
- `architecture/structurizr/workspace.dsl`
