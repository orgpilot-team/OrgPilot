# 24. Adopt DDD for Backend API, Background Worker, and Agent Runtime

Date: 2026-11-19

## Status

Accepted

## Context

The three runtime components carry the real business complexity: scoped access and human decisions (Backend API), deterministic data-to-signal processing (Background Worker), and bounded agent execution with a shared cost budget (Agent Runtime). The existing C4 component inventories describe technical roles but do not define module boundaries, aggregate invariants, or ports. Without explicit domain boundaries, implementation tends toward a shared mutable model, cross-component shortcuts, and rules that are enforced only by convention — a poor fit for a system whose acceptance tests check determinism, row-level security, and auditability.

The user requires market-grade maintainability with strong design patterns, and explicitly requires DDD for these three components.

## Decision

We adopt Domain-Driven Design as the implementation model for the Backend API, Background Worker, and Agent Runtime, documented in `docs/16-domain-model.md`:

- Each component is partitioned into named **bounded contexts** with explicit application-service APIs; the deployment remains a modular monolith.
- Business state is organised into **aggregates** with named roots and invariants, **entities**, and **value objects** (for example `AgentJob`, `Decision` with `SuccessCriterion`, `ReportVersion`, `IngestionBatch`, `SignalEpisode`, `ModelReservation`).
- **Domain services** hold rules that do not belong to one entity (`SignalDetectionService`, `EscalationPolicyService`, `DecisionEffectService`, `BudgetSettlementService`).
- **Repositories** are ports in the domain/application layer; PostgreSQL implementations live in infrastructure.
- **Application use cases** are the only entry points from adapters; each fixed handler in the Backend API maps to one use case.
- **Ports and adapters** isolate PostgreSQL, source files, the LLM provider, and the filesystem. **Anti-corruption layers** translate source schemas, uploaded/ticket text (prompt injection is data), and LLM completions (candidates, never validated facts).
- **Domain events** (`DecisionConfirmed`, `SignalEscalated`, `ReportPublished`, `GuardrailBreached`, `JobCommitted`, and others) carry immutable, trace-correlated payloads between contexts through application services.

## Consequences

- Implementation has a clear module map; adding a source, KPI, or manager level touches one adapter or registry entry.
- Invariants (immutable published reports, one lease per job, no LLM-generated numbers, guardrail breach is a signal) are enforced in the domain, not only in UI text.
- More upfront structure than a flat CRUD design; justified by the correctness, determinism, and audit requirements.
- DDD names supplement, not replace, the C4 component names in the DSL and docs 10/11/13.

## Related

- `docs/16-domain-model.md` (authoritative model)
- ADR-0018 (modular monolith), ADR-0005 (scoped queries), ADR-0006 (signal lifecycle), ADR-0008 (bounded agent), ADR-0019 (durable jobs)
