# 1. Use one versioned data intake and preparation pipeline

Date: 2026-11-14

## Status

Accepted

## Context

OrgPilot receives ordered data drops, manager inputs, and uploads. The system must support replay, late data, schema changes, duplicate records, conflicting records, and a fixed daily cutoff. It must not guess unknown file contracts or use future data.

## Decision

OrgPilot uses one deterministic pipeline for source intake, schema validation, normalization, data-quality checks, duplicate and conflict handling, canonical storage, and daily snapshots. It follows the DDD model in `docs/16-domain-model.md` (ADR-0024).

The system reads input only from `DATA_DIR` and writes delivery output only to `OUTPUT_DIR`. Each source has a versioned schema contract. Raw and canonical data remain separate. Invalid or conflicting data is quarantined. Each report uses a pinned snapshot. Late or corrected data causes a complete rebuild in the first version.

Canonical deduplication keys are `order_id`, `ticket_id`, `lead_id`, and `task_id`; event tables use the composite key `(entity_id, event_type, event_time)`. Duplicate export rows are byte-identical and are dropped before any KPI is computed, with a same-morning `data_issues` entry (`source: "orders"`, `type: "duplicate"`); the apparent jump is never a business signal.

Lead lifecycle: a lead with no progress after first contact is abandoned, not a bottleneck; CRM records no rejection event. `K_WF3_SLA_7D` and `K_ENT_WINRATE_30D` count only closed leads (won or lost); `K_ENT_PIPELINE` counts only opportunities with a proposal sent. The adopted rule is "no progress after 14 days = abandoned". The absence of a rejection event is one data-quality note, not a daily signal.

## Consequences

The system can reproduce a report from its pinned data and contracts. A new source normally needs an adapter and a schema registration. It does not need a new pipeline. The system must store source hashes, receipts, schema versions, data issues, and lineage. Complete rebuilds can cost more than selective recalculation.

## Related requirements

- The official input contracts define the accepted data sources and schemas.
- Evaluation must support deterministic replay without future-data leakage.
- Source hashes, receipts, schema versions, and lineage must make each result reproducible.
