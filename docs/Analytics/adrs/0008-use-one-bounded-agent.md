# 8. Use one bounded agent outside the deterministic core

Date: 2026-11-14

## Status

Accepted

## Context

OrgPilot needs language analysis and Persian narrative generation. It also needs reproducible numbers, signals, authorization, validation, and publication.

## Decision

OrgPilot uses one bounded agent. LangGraph coordinates only agent work. The deterministic core owns KPI calculation, signal rules, workflow reconstruction, authorization, validation, and publication.

The agent can analyze authorized evidence and create a narrative or decision-card candidate. It cannot calculate a KPI, widen scope, confirm a decision, activate configuration, or publish an unvalidated result.

The Backend API commits each Agent Job to PostgreSQL before it returns the `job_id`. After the commit, the Backend API can send an authenticated wake-up that contains the `job_id`. The wake-up is optional and is only a hint. It is not a queue or a source of truth.

The Agent Runtime claims ready jobs from PostgreSQL. For each claim, it reloads the pinned actor, scope, context, policy, and evidence references. It records the candidate or an explicit failure in PostgreSQL. Business evidence is obtained through the Backend API Evidence Service and Query Gateway. The Agent Runtime does not run arbitrary SQL on business data.

The system records token use, retry count, cache use, model, model version, and cost. Identical runs must produce identical numbers and signals. The accepted limits are at most five minutes for each processing day and at most five US dollars for the complete 30-day run.

## Consequences

Model variation cannot change the deterministic management record. PostgreSQL is the durable source of truth for Agent Job, Lease, Attempt, Dependency, Checkpoint, Candidate, and Failure state. The Model Gateway and Output Validator are mandatory boundaries. A failed wake-up does not lose a committed job. A model failure can remove optional narrative text, but it cannot invalidate deterministic canonical JSON.

ADR-0022 selects the evaluation model and fixes the model-call timeout, retry limit, and no-narrative fallback. Internal budget allocation remains open in `ISSUE-V3-07`. Detailed LangGraph nodes, state, checkpoints, and interrupts remain open in `ISSUE-V3-08`.

## Related requirements

- The bounded agent must remain outside the deterministic calculation and publication core.
- Durable Agent Jobs must survive a failed process or a failed wake-up.
- ADR-0019 defines the durable job protocol and the limited database-access boundary.
