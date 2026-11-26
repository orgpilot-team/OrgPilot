# 10. Require human control of decisions and actions

Date: 2026-11-14

## Status

Accepted

## Context

OrgPilot can identify conditions and propose options. An automated organization action could create operational or governance risk.

## Decision

OrgPilot creates suggestions and drafts. A human manager makes the decision and sends or executes the action. The system does not send a message, move staff, or execute an organization action.

The system proposes a success criterion on the decision card and the manager confirms it. The criterion contains a target KPI and target value (preferably return below the `warn` threshold or reach the dictionary `target`, not an arbitrary percentage), a measurement window of 3–5 days, and a guardrail KPI with its limit; "10% improvement" is only a fallback default. Follow-up results state the method (workload normalization or comparable case without the decision), assumptions, confidence, and confounding factors. If the effect cannot be isolated, the Persian result states «اثر قابل جدا کردن نیست», not "no effect". Exported effect direction is `improved`, `worsened`, `no_change`, or `too_early`; a guardrail breach is itself a business signal.

## Consequences

Decision cards need explicit confirmation before they enter the decision record. Decision and Follow-Up records decisions and observed results but does not execute the decision.

The authorized confirmer and evidence of actual execution remain open in `ISSUE-V3-05`.

## Related requirements

- OrgPilot can propose a decision, but a human manager must confirm it.
- OrgPilot must not send or execute an organization action.
- Decision Effect evaluation must follow ADR-0015 without changing the output contract.
