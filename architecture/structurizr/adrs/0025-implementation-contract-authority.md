# 25. Implementation contract from TA clarifications is authoritative

Date: 2026-11-19

## Status

Accepted

## Context

The project brief contains several values that were later corrected by the instructor Q&A (`ta.txt`): the per-day time budget (15 vs 5 minutes), the cost ceiling (per day vs the whole 30-day run), the KPI parity tolerance (zero vs ±1%), and the treatment of signals created by late-arrival recomputation. Leaving both versions active would let an implementer follow the wrong one and fail acceptance.

## Decision

`docs/15-implementation-contract.md` is the authoritative implementation contract for all rules clarified in `ta.txt`. It wins over older brief statements where they disagree. Specifically:

- **5 minutes** maximum processing per day, not 15.
- **$5 for the entire 30-day run**, not per day; cost = logged tokens × provider's official rate on evaluation day, reconciled with the provider dashboard.
- **±1%** KPI parity tolerance; "zero tolerance" applies only to matching report-text numbers to JSON `value`/`query_id` pairs.
- A late-arrival recomputation that creates a genuine signal publishes it that same morning; the data issue itself is never a business signal.
- All other TA rules (dedup keys, missing-file cadence, abandoned leads, direction-based R5, workflow stage owners, Q03 `U_SAL` target, `data_unavailable` vs `refused_out_of_scope`, decision-effect confounders and success metrics) are captured verbatim in the contract.

The brief was updated to remove the contradictions. Gaps `ISSUE-V3-02`, `DOC-GAP-V3-04`, and `ISSUE-V3-09` are closed for the Evaluation profile by this contract. `ISSUE-V3-01` remains open only for the access projection matrix entries required by `docs/04-security-and-trust.md`.

## Consequences

- One source of truth for implementation values; acceptance tests cite the contract.
- Documentation conflicts are resolved rather than averaged.
- Any future instructor clarification requires a new ADR and a contract update.

## Related

- `docs/15-implementation-contract.md`, ADR-0002, ADR-0008, ADR-0016, ADR-0021, ADR-0022
