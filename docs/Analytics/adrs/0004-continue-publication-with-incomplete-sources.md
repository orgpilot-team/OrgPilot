# 4. Continue publication when a source is incomplete

Date: 2026-11-14

## Status

Accepted

## Context

A source can be missing or late. DIDRAH must not create a value from incomplete evidence. It must also avoid stopping all valid reports when one source is unavailable.

## Decision

A missing source does not stop the complete publication run. A KPI that depends on the missing source is `null`, never zero. The system records data issues with exact literal values: `type: "missing"` on the first morning and every following morning until the file arrives (repetition is not penalized); on the morning after arrival, exactly one `type: "late_arrival"` entry, followed by recomputation of that day's KPIs. Duplicate export rows are reported the same morning with `source: "orders"`, `type: "duplicate"` after deduplication by `order_id`. A data issue does not enter the business `items` list and does not become a business signal. The sole exception is a genuine KPI signal created by the late-arrival recomputation, which is published in that same morning's report.

## Consequences

Managers can receive valid results from healthy sources. Each report must show the applicable data limitations. Downstream components must preserve `null` and must not replace it with zero or an estimate.

`DOC-GAP-V3-04` is closed by `docs/15-implementation-contract.md` §5: repeat `missing` until arrival, one `late_arrival` the next morning, recompute, and publish any resulting signal that same morning.

## Related requirements

- Missing evidence must not produce an estimated KPI value.
- A source failure must not remove valid reports that do not depend on that source.
- Data-quality issues must remain separate from business signals.
