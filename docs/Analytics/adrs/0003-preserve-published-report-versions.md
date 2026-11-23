# 3. Preserve published report versions

Date: 2026-11-14

## Status

Accepted

## Context

Late data, corrected data, or resolved conflicts can change a report after its first publication. An overwrite would remove the evidence that a manager originally received.

## Decision

A published report is immutable. The system labels the first version `as_reported`. A complete rebuild creates a new `restated` version. The new version links to the original version and records the reason for the change.

## Consequences

The system preserves the historical management record. Consumers must select the correct report version for their purpose. Storage and APIs must support version links and cannot use destructive report updates.

## Related requirements

- Late or corrected data must not overwrite a published management record.
- A restated report must link to the original report and state the restatement reason.
