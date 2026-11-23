# 7. Assign workflow and stage owners from KPI ownership

Date: 2026-11-14

## Status

Accepted

## Context

DIDRAH reconstructs three workflows. Each stage needs one responsible manager. Workflow-level conditions also need one escalation owner.

## Decision

Manager `M01` owns the complete WF1, WF2, and WF3 workflows. The owner of each stage is the owner of the KPI for that stage. A workflow KPI that reaches or crosses its warning threshold in the adverse direction escalates to the Senior Manager.

The accepted stage ownership is:

| Workflow | Stage | Owner |
|---|---|---|
| WF1 | Registration to payment | M02 / U_SAL |
| WF1 | Payment to collection | M07 / T_WH |
| WF1 | Collection to shipping handoff | M08 / T_SHP |
| WF1 | Shipping to customer delivery | M08 / T_SHP |
| WF1 | Follow-up and complaint | M09 / T_RSP |
| WF2 | Registration to first response | M10 / T_CMP |
| WF2 | First response to warehouse inspection | M07 / T_WH |
| WF2 | Inspection to resolution | M10 / T_CMP |
| WF3 | Lead generation | M06 / T_DIG |
| WF3 | First contact to close | M05 / T_ENT |

## Consequences

Every workflow observation and escalation has a deterministic owner. `workflow_definitions.csv.owner` stores the workflow owner. The stage owner is derived from the owner of the KPI that measures the stage, as defined by the active KPI dictionary. A stage owner is not duplicated in `workflow_definitions.csv`.

## Related requirements

- Workflow stage ownership must follow the official KPI ownership data.
- The active workflow definition contract stores the workflow owner and derives each stage owner from active KPI ownership.
