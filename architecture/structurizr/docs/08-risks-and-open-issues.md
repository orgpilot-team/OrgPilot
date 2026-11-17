# Risks and open issues

The active control register is `DIDRAH-ARCH-CONTROL-V3` in `Docs/final review/architecture-control-register-v3.md`.

The main architecture risks are:

- A parity difference between SQLite reference SQL and PostgreSQL product SQL
- A row-level security bypass in interactive SQL
- Prompt injection through source content or manager uploads
- Excess architecture complexity for the delivery team
- Model latency or cost that exceeds the evaluation limit
- A data-quality condition that is incorrectly published as a business signal
- Output that is schema-valid but semantically incomplete
- Hardcoded behavior for the development dataset
- Future-data leakage during replay

The current P0 open issues are:

- `ISSUE-V3-06`: retry, timeout, and fallback behavior
- `ISSUE-V3-07`: language model and internal budget allocation
- `ISSUE-V3-08`: detailed LangGraph node, state, checkpoint, retry, and interrupt boundary

The current P1 open issues are:

- `ISSUE-V3-01`: complete access projections for shared resources
- `ISSUE-V3-02`: null and ad hoc number contract
- `ISSUE-V3-04`: complete report lifecycle outside the top five items
- `ISSUE-V3-05`: evidence and authority for actual decision execution
- `ISSUE-V3-09`: retention, backup, audit access, and restore policy
- `ISSUE-V3-10`: KPI change approval, activation, and rollback

An open issue does not change an accepted decision. It defines a boundary that still needs a contract or a follow-up decision.
