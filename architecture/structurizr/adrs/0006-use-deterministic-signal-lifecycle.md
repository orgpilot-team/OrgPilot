# 6. Use a deterministic signal lifecycle and escalation policy

Date: 2026-11-14

## Status

Accepted

## Context

DIDRAH must identify important conditions without language-model variation. It must avoid repeated alerts and must preserve escalation history.

## Decision

Signal states are `new`, `escalated`, and `ongoing`. A signal starts with the KPI owner. A value that reaches or crosses a threshold in the adverse direction activates the signal. Equality is included.

A direct critical condition creates a `new` item for the owner and an `escalated` item for the next manager. A warning that later becomes critical remains `ongoing` for the owner and preserves its escalation history. An unchanged condition does not become `new` again.

Organization and workflow warning conditions escalate to the Senior Manager. R5 signals only adverse deviation. An information KPI does not create an alert. A report shows at most five items. Signals with one root cause are grouped for the Senior Manager.

## Consequences

Signal generation is reproducible and testable. Rules, thresholds, ownership, grouping, and ranking must be versioned configuration. The language model can explain a signal but cannot create or change it.

## Related requirements

- Threshold evaluation, escalation, grouping, and ranking must be deterministic.
- Signal state must be stored per recipient as defined by ADR-0017.
- Data-quality issues must not become business signals.
