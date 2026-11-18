# 17. Signal Episode Contract and Recipient State

Date: 2026-11-17

## Status

Accepted

## Context

The current Signal Engine component exists but the state machine for signals needs precise contracts. TA provides deterministic rules:

- Owner on first Crit crossing gets `new` that morning
- Senior manager same morning gets `escalated`
- Warn then Crit has escalation history
- Staying beyond `escalate_after_days` causes escalation
- Workflow/org KPI at warn escalates to senior manager
- Co-causal signals grouped for senior manager
- Unchanged item does not become `new` again
- Data errors don't enter `items`

Key insight: A signal can have different statuses for different recipients simultaneously:

```
Owner: new
Senior Manager: escalated
```

Therefore `status` cannot be stored on the Signal itself; it must be on Recipient View or Delivery State.

## Decision

Finalize these contracts:

- `SignalEpisode` - the ongoing business issue
- `SignalOccurrence` - a specific detection event
- `SignalRecipientView` - per-recipient state (new/escalated/ongoing)
- `EscalationEvent` - escalation record with reason and history
- `SuppressionDecision` - explicit suppression with reason
- `GroupedExecutiveItem` - grouped co-causal signals for senior manager

Signal Engine component already exists; these contracts make its output precise and testable.

## Consequences

- Status is per-recipient, not per-signal
- Escalation history preserved
- Grouping for senior manager explicit
- No re-creation of `new` for unchanged conditions
- Data quality issues separated from business signals

## Source

Addresses Gap 6 from architectural review: "قرارداد دقیق Signal Episode"
