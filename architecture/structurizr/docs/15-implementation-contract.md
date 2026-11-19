# 15. Implementation Contract (authoritative TA clarifications)

This document is the single implementation-ready contract derived from the instructor Q&A in `ta.txt`. Where an older brief statement disagrees with this document, **this document wins**. It closes the open gaps `ISSUE-V3-01`, `ISSUE-V3-02`, `DOC-GAP-V3-04`, and `ISSUE-V3-09` for the evaluation profile.

Status: **Accepted for implementation**. Every rule below is testable by the Acceptance Test Harness.

## 1. KPI numbers and SQL parity

- The reference number of every KPI is produced by executing the metric-dictionary SQL on **SQLite**. A different engine is allowed only if results are identical.
- SQLite `median()` is equivalent to PostgreSQL `percentile_cont(0.5)`, **not** `percentile_disc`.
- `julianday(b) - julianday(a)` is in **days**; PostgreSQL `EXTRACT(EPOCH FROM b - a)` returns seconds and must be converted explicitly to the KPI unit (hours or days).
- Percentages use `100.0 *` to avoid integer division.
- Rounding, date types, and timezone (`Asia/Tehran`) can move a record to another day. Per-KPI rounding follows the KPI dictionary.
- Compare output with the reference SQL on the dev dataset. **±1% is the accepted KPI-parity/evaluation tolerance.** The brief's "zero tolerance" applies only to matching a number in the report text to a `value`/`query_id` pair in JSON, not to KPI computation.
- A Parity Receipt is required before a translated KPI is accepted.

## 2. Reference machine, network, and determinism

| Item | Required value |
|---|---|
| CPU | 4 cores |
| RAM | 16 GB |
| GPU | None |
| Network | **Only the LLM API**; all other internet egress is closed |
| Data mount | `/data` read-only |
| Time budget | **At most 5 minutes per processing day** |
| Dependencies | All installed at image build time; no install at run time |
| Local LLM | Not permitted (no GPU, would exceed the time budget) |
| Model calls | Retry with bounded backoff and a finite timeout; on failure emit the report with correct numbers and no LLM narrative |
| Temperature | `0` for stable text |
| Repeated runs | The container is executed **twice**; numbers and discovered signals must be identical across runs |

Determinism rules: no host clock in product time, no unordered iteration affecting output, no random sampling, pinned input hashes and configuration, stable sort keys, and LLM text never used as a source of numbers or signal status.

## 3. LLM provider, cost, and secrets

- Provider is free as long as it is reachable through an API. The model and version are declared in ADR-0022.
- **The $5 ceiling covers the entire 30-day replay run, not a single day.**
- Cost = logged input tokens + logged output tokens × the provider's official rate on the evaluation day. Every call logs provider, model, token counts, latency, status, and trace context. The computed total is reconciled with the provider dashboard.
- No API key in the project or repository. Only `.env.example` with `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL`. The key is injected as an environment variable, delivered to the instructor over a private channel, and revoked after Demo Day.
- Langfuse/OTLP export is disabled in the graded Evaluation profile because outbound network is closed. Telemetry is optional and fail-open.

## 4. Docker entrypoint and paths

- `/data`: hidden data with the same structure as `arka_dataset`, read-only.
- `/submission`: writable; contains `briefs/day_XXX/<manager_id>.json` and `qa/<question_id>.json`.
- One command performs the whole run: process drops night-by-night from `day_000` through `day_090`, apply `manager_inputs` on their own day, and produce reports for mornings `day_062` through `day_091`. No manual or interactive step.
- Read paths from `DATA_DIR` and `OUTPUT_DIR` environment variables; never hardcode them.
- Exit code must be zero on success. The internal database, logs, and dashboard remain inside the container; nothing is written outside `OUTPUT_DIR`.

## 5. Data issues

`data_issues` entries carry `type` and `source` with these exact literal values:

| Situation | Required behavior |
|---|---|
| File missing on first morning | One `data_issues` entry with `type: "missing"`; dependent KPIs are `null`, never `0` |
| File still missing | Repeat `missing` every morning until arrival; never in `items`; no penalty for repetition |
| File arrives | On the next morning, exactly one entry with `type: "late_arrival"`; recompute that day's KPIs; if recomputation creates a signal, include it in that same morning's report |
| Duplicate export row | Deduplicate first; same morning `data_issues` with `source: "orders"`, `type: "duplicate"`; the apparent order-count/revenue jump must not become an `item` |

Canonical deduplication keys: `order_id`, `ticket_id`, `lead_id`, `task_id`. Event tables use the composite key `(entity_id, event_type, event_time)`. Duplicate rows are byte-identical.

A data issue is not a business signal. The only exception is a genuine KPI signal created by recomputation after a late arrival, which is published that same morning.

## 6. Lead lifecycle and KPI populations

- A lead with no progress after first contact is **abandoned**, not a bottleneck. CRM records no "rejection" event.
- `K_WF3_SLA_7D` and `K_ENT_WINRATE_30D` count only **closed** leads (won or lost).
- `K_ENT_PIPELINE` counts only opportunities for which a proposal was sent.
- Adopted rule: no progress after **14 days** = abandoned.
- The absence of a rejection event is reported once as a data-quality note, not as a daily signal.

## 7. Signal lifecycle and direction

- Signal types: target deviation, abnormal trend, sudden change, workflow slowdown, backlog, monthly-target risk.
- Importance criteria: deviation size, customer impact, financial impact, cross-unit effect, statistical confidence, manager-declared priority.
- Every signal has one owner, assigned to the lowest level able to resolve it. At most five items per manager report.
- `dow_baseline`: only deviation in the **unfavorable** direction is a signal. The KPI dictionary `direction` column defines favorable direction: `1` = more is better, `-1` = less is better. `K_SUP_TICKETS` has `direction = -1`: a decrease is not a signal; an increase beyond N% is. A large favorable deviation is not an alert and may be shown outside `items`.
- Rule R5, exact text: «انحراف بیش از N٪ در جهت نامطلوب (طبق direction) سیگنال است.»
- A KPI that crosses `crit` on its first day is `new` for the owner and `escalated` for the higher manager the same morning. If it passes `warn` first and then `crit`: day one is `new`, then `ongoing` with escalation history; on the day it becomes `crit`, or when time above `warn` exceeds `escalate_after_days`, it is `escalated`.
- A workflow KPI or organization-level KPI crossing `warn` is also `escalated` for the Senior Manager. Co-cause signals are aggregated into one Senior Manager item.
- A signal without meaningful change must not reappear as `new`; repetition is penalized. Escalation is allowed only with explicit history and reason.
- Escalation defaults live in the KPI dictionary and are editable: team supervisor 2 days, unit manager 3 days.

## 8. Workflow stage ownership

`workflow_definitions.csv` `owner` is the whole-workflow owner (Senior Manager). A stage's owner is the owner of the KPI measuring that stage.

| Workflow | Stage | Owner |
|---|---|---|
| WF1 order-to-delivery | registration → payment | U_SAL (M02) |
| WF1 | payment → picking | T_WH (M07) |
| WF1 | picking → handover to shipping | T_SHP (M08) |
| WF1 | shipping → customer delivery | T_SHP (M08) |
| WF1 | follow-up and complaint | T_RSP (M09) |
| WF2 complaint-to-resolution | registration → first response | T_CMP (M10) |
| WF2 | first response → warehouse inspection | T_WH (M07) |
| WF2 | inspection → resolution | T_CMP (M10) |
| WF3 lead-to-contract | lead generation | T_DIG (M06) |
| WF3 | first contact, qualification, proposal, close | T_ENT (M05) |

A stage bottleneck goes first to the stage owner. If the whole-workflow KPI (`K_WF*`) crosses `warn`, it escalates to the Senior Manager.

## 9. Scoped monthly target (Q03)

- The monthly revenue target belongs to `U_SAL`; the corrected `config/monthly_targets.csv` contains `scope = U_SAL` rows with the same value as the organization target. Replace the file with the corrected version. Hidden evaluation data has the same structure.
- The sales manager has access to this target. Q03 answer = net monthly revenue up to yesterday plus proportional target attainment percentage.
- `refused_out_of_scope` means the data exists but is outside the manager's scope. `data_unavailable` means the data is not in the system, is not ingested, or has not arrived (salaries, USD price, tickets for a missing-day file). The Persian answer states explicitly that the data does not exist in the system sources; no guessing and no external source.

## 10. Decision effect and success metrics

- Measure effect with the decision's own success metric, but account for concurrent factors. A simple before/after comparison is insufficient when a campaign coincided. Use either workload normalization (e.g. orders per picking staff) or comparison with a similar case without the decision.
- Every effect result states: whether the success metric was met; the effect estimate with method and assumptions; confidence level and confounding factors. If data cannot separate the effect, say «اثر قابل جدا کردن نیست» — not "no effect".
- The system proposes a success metric on the decision card; the manager confirms it at decision time. "10% improvement" is only a fallback default when no better metric exists.
- Success metric components: target KPI and target value (preferably return below the `warn` threshold or reach the dictionary `target`, not an arbitrary percentage); measurement window (3–5 days); guardrail KPI with its limit.
- Track both target and guardrail on following days. `decision_followups` reports effect direction as `improved`, `worsened`, or `too_early`. A guardrail breach is itself a business signal.

## 11. Output contract

One JSON file per manager per day with `date`, `manager_id`, and `items[]`. Each item carries `signal_id`, `kpi_id`, `entity`, `value`, `query_id`, `owner`, `cause`, `confidence`, and `status`. Statuses are exactly `new`, `escalated`, `ongoing`. Reports and UI are Persian and RTL.

## 12. Design quality bar

Backend API, Background Worker, and Agent Runtime follow the DDD model in `16-domain-model.md`: explicit bounded contexts, aggregates and invariants, value objects, domain services, repositories as ports, application use cases, ports-and-adapters at every external boundary, domain events, and anti-corruption layers for source data, LLM output, and provider APIs. Performance budget, determinism, row-level security, and fail-open behavior are non-negotiable acceptance gates, not tuning items.
