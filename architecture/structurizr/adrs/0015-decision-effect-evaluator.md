# 15. Decision Effect Evaluator

Date: 2026-11-17

## Status

Accepted

## Context

The current architecture has "Decision and Follow-Up" but it focuses on recording decisions, not measuring their effect. The TA requires structured effect measurement including:

- Target KPI, target value, measurement period, guardrail
- Estimation method, assumptions, confidence, confounders
- Effect direction: `improved`, `worsened`, `too_early`, or "effect not isolatable"
- `no_change` must be preserved in schema (per IMPL-GAP-V3-03)

The approved v1 behavior is:

1. At decision registration: the system **proposes** a success metric on the decision card and the manager **confirms** it. The metric contains a target KPI and target value (preferably return below the `warn` threshold or reach the dictionary `target`, not an arbitrary percentage), a measurement window of **3–5 days**, and a guardrail KPI with its limit. "10% improvement" is only a fallback default when no better metric exists.
2. At follow-up: if evaluation date not reached → `too_early`; if date reached and data sufficient → determine direction (`improved`/`worsened`/`no_change`); if data insufficient → record reason, leave result empty.
3. When the decision coincided with a campaign or other concurrent change, a simple before/after comparison is insufficient. Apply **workload normalization** (e.g. orders per picking staff) or **comparison with a similar case without the decision**, and record which method was used.
4. Store assumptions, confounders, confidence in attribution, guardrail status in separate fields. If the effect cannot be separated, the Persian report states «اثر قابل جدا کردن نیست» — never "no effect".
5. A guardrail breach is itself a business signal emitted to the Signal Engine. The permitted exported `effect_direction` values are `improved`, `worsened`, `no_change`, and `too_early`, as defined by the reference schema.

## Decision

Add `Decision Effect Evaluator` component in Background Worker (or Decision module).

Flow:

```
Confirmed Decision → Follow-up Schedule → Decision Effect Evaluator
KPI Observations → Decision Effect Evaluator
Context (Campaign/Workload/Similar Cases) → Decision Effect Evaluator
Decision Effect Evaluator → Effect Assessment (structured)
Effect Assessment → Agent (optional narrative only)
Effect Assessment → Report (Decision Follow-up)
```

Agent only uses the deterministic result for narrative; it cannot guess effect from free text.

The complete Decision Effect is an internal, versioned PostgreSQL record. It does not add fields or enum values to the read-only output contract.

Export mapping is limited to fields that the reference schema already permits:

- `evaluated` with `improved`, `worsened`, or `no_change` exports the permitted `effect_direction` value.
- `too_early` exports the permitted `too_early` value.
- `insufficient_data` or `not_isolatable` does not export `effect_direction`. The limitation can appear only in the permitted `detail_fa` field.

## Consequences

- Deterministic effect calculation, not LLM-based
- Structured fields for method, assumptions, confidence, confounders, guardrail
- The internal record can evolve without changing the reference output schema
- `brief_schema.json` remains read-only
- Closes Gap 4 and IMPL-GAP-V3-03

## Related requirements

- Decision effects must be deterministic and must keep their attribution limits.
- The output must conform to the read-only `brief_schema.json` contract.
- Internal Decision Effect fields must not be added to exported JSON.
