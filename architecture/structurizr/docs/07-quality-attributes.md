# Quality attributes

## Correctness

Published numbers come from registered deterministic queries. The system stores the SQL, result, snapshot, scope, and `query_id` for each published number. The UI, serializer, and language model do not recalculate or round a KPI.

## Security

The system must prevent data leakage across the Senior Manager, Unit Manager, and Team Supervisor scopes. Authorization is applied before model use and after model output.

## Reproducibility

Each run uses pinned inputs and an injected business clock. An identical run must produce identical numbers and signals. Published reports are immutable.

## Resilience

A missing source can reduce data completeness without stopping all publication. A model-provider failure must not stop deterministic calculation or valid canonical JSON. A manager-specific failure must not remove other valid manager reports.

## Performance and cost

The accepted control register requires at most five minutes for each processing day and at most five US dollars for the complete 30-day run. The selected model, internal budget allocation, retry limits, and fallback content remain open.

## Maintainability

A new source, KPI, organization node, or manager level should use a versioned adapter, registry entry, or configuration change. It should not require a pipeline redesign.

## Auditability

Every published result must link to its evidence, query, snapshot, configuration, policy scope, validation result, and publication receipt.
