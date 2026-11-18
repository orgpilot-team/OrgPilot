# 10. Require human control of decisions and actions

Date: 2026-11-14

## Status

Accepted

## Context

DIDRAH can identify conditions and propose options. An automated organization action could create operational or governance risk.

## Decision

DIDRAH creates suggestions and drafts. A human manager makes the decision and sends or executes the action. The system does not send a message, move staff, or execute an organization action.

A success criterion contains a target KPI, target value, measurement period, and guardrail. Follow-up results state the method, assumption, confidence, and confounding factor. If the effect cannot be isolated, the result states that limitation. Effect direction is `improved`, `worsened`, or `too_early`.

## Consequences

Decision cards need explicit confirmation before they enter the decision record. Decision and Follow-Up records decisions and observed results but does not execute the decision.

The authorized confirmer and evidence of actual execution remain open in `ISSUE-V3-05`.

## Related requirements

- DIDRAH can propose a decision, but a human manager must confirm it.
- DIDRAH must not send or execute an organization action.
- Decision Effect evaluation must follow ADR-0015 without changing the output contract.
