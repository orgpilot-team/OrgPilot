# 1. Use one versioned data intake and preparation pipeline

Date: 2026-11-14

## Status

Accepted

## Context

DIDRAH receives ordered data drops, manager inputs, and uploads. The system must support replay, late data, schema changes, duplicate records, conflicting records, and a fixed daily cutoff. It must not guess unknown file contracts or use future data.

## Decision

DIDRAH uses one deterministic pipeline for source intake, schema validation, normalization, data-quality checks, duplicate and conflict handling, canonical storage, and daily snapshots.

The system reads input only from `DATA_DIR` and writes delivery output only to `OUTPUT_DIR`. Each source has a versioned schema contract. Raw and canonical data remain separate. Invalid or conflicting data is quarantined. Each report uses a pinned snapshot. Late or corrected data causes a complete rebuild in the first version.

## Consequences

The system can reproduce a report from its pinned data and contracts. A new source normally needs an adapter and a schema registration. It does not need a new pipeline. The system must store source hashes, receipts, schema versions, data issues, and lineage. Complete rebuilds can cost more than selective recalculation.

## Source

`ADR-V3-01` in `Docs/final review/architecture-control-register-v3.md`.
