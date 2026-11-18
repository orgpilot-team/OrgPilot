# 4. Continue publication when a source is incomplete

Date: 2026-11-14

## Status

Accepted

## Context

A source can be missing or late. DIDRAH must not create a value from incomplete evidence. It must also avoid stopping all valid reports when one source is unavailable.

## Decision

A missing source does not stop the complete publication run. A KPI that depends on the missing source is `null`. The system records missing or late data in `data_issues`. A data issue does not enter the business `items` list and does not become a business signal.

## Consequences

Managers can receive valid results from healthy sources. Each report must show the applicable data limitations. Downstream components must preserve `null` and must not replace it with zero or an estimate.

The completion criterion after backfill remains open in `DOC-GAP-V3-04`.

## Related requirements

- Missing evidence must not produce an estimated KPI value.
- A source failure must not remove valid reports that do not depend on that source.
- Data-quality issues must remain separate from business signals.
