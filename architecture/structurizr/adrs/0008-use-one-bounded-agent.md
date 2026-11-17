# 8. Use one bounded agent outside the deterministic core

Date: 2026-11-14

## Status

Accepted

## Context

DIDRAH needs language analysis and Persian narrative generation. It also needs reproducible numbers, signals, authorization, validation, and publication.

## Decision

DIDRAH uses one bounded agent. LangGraph coordinates only agent work. The deterministic core owns KPI calculation, signal rules, workflow reconstruction, authorization, validation, and publication.

The agent can analyze authorized evidence and create a narrative or decision-card candidate. It cannot calculate a KPI, widen scope, confirm a decision, activate configuration, or publish an unvalidated result.

The system records token use, retry count, cache use, model, model version, and cost. Identical runs must produce identical numbers and signals. The accepted limits are at most five minutes for each processing day and at most five US dollars for the complete 30-day run.

## Consequences

Model variation cannot change the deterministic management record. The Model Gateway and Output Validator are mandatory boundaries. A model failure can remove optional narrative text, but it cannot invalidate deterministic canonical JSON.

The selected model and budget allocation remain open in `ISSUE-V3-07`. Detailed LangGraph nodes, state, checkpoints, retries, and interrupts remain open in `ISSUE-V3-08`.

## Source

`ADR-V3-08` in `Docs/final review/architecture-control-register-v3.md`.
