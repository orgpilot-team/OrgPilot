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

## Amendment (2026-11-20): scope DDD rigour to where invariants live

This ADR is refined, not reversed. Full tactical DDD applies **only where an invariant is atomic, acceptance-tested, and mutated from more than one place**. Derived read models, append-only records, stateless validators, and persistence wrappers are folded into their owning components rather than modelled as aggregates or given their own C4 box. `docs/16-domain-model.md` §0 states the test and §6 lists every merge, demotion, and elimination with its reasoning.

Key consequences of the refinement:

- Aggregate roots are kept only for genuine invariants (`AccessPolicy`, `AgentJob`, `Decision`, `ReportVersion`, `IngestionBatch`, `Snapshot`, `KpiDefinition`, `SignalEpisode`, `EffectAssessment`, `RunStage`, `ReasoningSession`, `ModelReservation`, `ConversationSession`, `ExportBatch`).
- `DataIssue`, `DecisionCard`, follow-ups, and conversation turns are entities inside their roots; `Projection`, `KpiResult`, `WorkflowObservation`, `ManagerRequest`, `ModelCallReceipt`, and `Checkpoint` are derived/value/append-only records, not aggregates.
- Stateless helpers and duplicate owners are removed as components (see doc 16 §6); the Worker stage runner and the Agent Runtime job runner share one durable-job contract.
- The target component set is documented in docs 10–13 and 16. `workspace.dsl` still shows the pre-consolidation inventory and will be synchronized in the next phase.

## Related

- `docs/16-domain-model.md` (authoritative model)
- ADR-0018 (modular monolith), ADR-0005 (scoped queries), ADR-0006 (signal lifecycle), ADR-0008 (bounded agent), ADR-0019 (durable jobs)
