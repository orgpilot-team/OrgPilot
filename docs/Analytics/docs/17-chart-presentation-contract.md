# 17. Chart Presentation Contract

This document defines the internal contract used to present deterministic charts in reports, chat answers, dashboards, and workflow views. It does not change the formal brief or QA output schemas.

Status: **Accepted for implementation**.

## 1. Scope

The chart presentation path has four parts:

1. A trusted product component obtains pinned report evidence or a validated bounded query result.
2. The Shared Chart Presentation Library creates and validates a library-neutral `ChartSpec`.
3. Report and Dashboard API returns an authorized internal `PresentationResponse`.
4. The Web Application maps `ChartSpec` to an ECharts option and renders it.

The Shared Chart Presentation Library is shared .NET code. It is not a Product Component, bounded context, process, service, store, authorization boundary, or source of business data.

## 2. Contract types

### ChartIntent

`ChartIntent` is an optional structured request for a chart. A fixed handler can create it from an explicit UI request. The Agent Runtime can also propose it as part of a candidate. A proposed intent is untrusted until Output Validator accepts it.

`ChartIntent` contains only:

- Requested chart type from an allowlist
- KPI or approved measure reference
- Time range
- Grouping or breakdown
- Optional comparison or target request

`ChartIntent` does not contain authoritative chart values, SQL, ECharts options, colors, fonts, or authorization data. It cannot widen the pinned scope.

### ChartSpec

`ChartSpec` is an immutable, versioned, rendering-library-neutral presentation record. It is built only from pinned report evidence or a validated bounded query result.

| Field | Rule |
|---|---|
| `schema_version` | Identifies the internal chart contract version. |
| `chart_id` | Stable identifier inside one source version. It does not grant access. |
| `source_kind` | Identifies report, answer, dashboard, or workflow presentation. |
| `source_id` | Identifies the related report, answer, or read result. |
| `source_version` | Pins the immutable source version. |
| `scope_ref` | References the authorized manager scope. |
| `snapshot_id` | Pins the business-data snapshot when applicable. |
| `type` | Uses an approved chart-type allowlist. |
| `title_fa` | Supplies the Persian chart title. It contains no new factual claim. |
| `unit` | Uses the approved KPI or measure unit. |
| `categories` | Supplies ordered category labels when the chart uses categories. |
| `series` | Supplies ordered series with approved points and source references. |
| `target_line` | Supplies an optional approved target or threshold reference and value. |
| `empty_state_fa` | Supplies an explicit Persian unavailable or empty state. |

Every series point is derived from an approved value. Every series carries applicable evidence references, including `query_id`. Missing values remain `null`; the builder does not replace them with zero or interpolate them.

`ChartSpec` does not contain an ECharts option. It does not contain executable JavaScript, a SQL statement, HTML, a model prompt, raw unrestricted rows, or visual theme values.

### PresentationResponse

`PresentationResponse` is an internal Backend API DTO for the Web Application.

It contains:

- One authorized validated content object
- `content_type` for report, answer, dashboard, or workflow content
- Content version and status
- Zero or more authorized `ChartSpec` values
- Explicit unavailable, incomplete, forbidden, or failed state when applicable

The content object remains the source of report or answer text. A chart does not add a new business claim. The response is not written to `OUTPUT_DIR`.

## 3. Shared Chart Presentation Library boundary

The shared library provides:

- Immutable `ChartIntent`, `ChartSpec`, series, point, axis, target-line, and `PresentationResponse` contract types
- Deterministic `ChartSpec` construction from approved typed input
- Contract validation
- Stable ordering
- Versioned JSON serialization
- Chart-type and result-shape compatibility checks

The shared library must not:

- Access PostgreSQL or the Protected File Archive
- Execute SQL or call Query Gateway
- Calculate a KPI or business aggregation
- Authorize a user or interpret a scope grant
- Create, claim, or update a job
- Call a language model
- Publish or export a report
- Contain React or ECharts code
- Select colors, fonts, spacing, or responsive layout

The implementation location is `src/shared-dotnet/chart-presentation`. The physical location does not make the library a C4 component.

## 4. Scheduled report chart flow

Report Evidence Builder applies a versioned report chart policy to the pinned manager evidence. It uses the Shared Chart Presentation Library to create zero or more `ChartSpec` records. It stores each record with the report candidate, snapshot, manager scope, query lineage, chart-policy version, and chart-contract version.

Output Validator validates the report candidate and its evidence. Publisher creates an immutable report version. The report-linked chart records remain internal and are associated with the same report version. A restatement creates new chart records and does not mutate the prior version.

When the Web Application requests a published report, Report and Dashboard API rechecks audience, purpose, and scope. It reads the report and only the chart records for that exact report version. It returns them in a `PresentationResponse`.

Submission Exporter reads only the formal validated brief payload. It excludes all chart-presentation fields.

## 5. Interactive answer chart flow

The manager can request a chart, for example monthly sales grouped by week. The authorized interactive path obtains a bounded result through Evidence Service and Query Gateway. The persisted result carries `query_id`, scope, snapshot, result hash, and ordered typed values.

The Agent Runtime can produce an answer candidate and an optional `ChartIntent`. It cannot produce authoritative chart values. Output Validator checks the answer, evidence references, scope, and intent.

For a validated answer, Report and Dashboard API gives the validated intent and bounded query result to the Shared Chart Presentation Library. The library creates a deterministic `ChartSpec`. The API stores it with the answer version and returns the answer and chart in a `PresentationResponse`.

If no chart is requested or the result shape does not support the requested chart, the response contains no chart or an explicit chart-unavailable state. The validated text answer remains available.

## 6. Web rendering boundary

The Web Application maps `ChartSpec` to an ECharts option. The mapping owns:

- Persian and RTL labels
- Visual theme, typography, and colors
- Tooltip and legend behavior
- Responsive layout
- Keyboard and screen-reader support
- Loading, empty, unavailable, and error states

The mapping must preserve point order, values, units, target values, and evidence identity. It must not calculate, regroup, interpolate, or correct business data.

## 7. Security and validation

The following checks are required before delivery:

- The requesting principal can read the source report or answer.
- `scope_ref` matches the authorized request scope.
- `source_version` and `snapshot_id` match the validated content.
- Every point maps to approved query lineage or pinned report evidence.
- The chart type is allowed for the result shape.
- Point and series limits are applied.
- Labels and text are treated as data and cannot execute code.
- The response contains no cross-scope series or unrestricted raw rows.

The browser is not an authorization boundary. Hidden series, disabled controls, or frontend filters do not replace Backend authorization.

## 8. Submission separation

The formal Submission contract remains unchanged:

```text
briefs/day_XXX/<manager_id>.json
qa/<question_id>.json
```

`brief_schema.json` and `qa_answer_schema.json` remain the field-level authorities for these files. `ChartIntent`, `ChartSpec`, `PresentationResponse`, and ECharts options are internal fields and are never Submission fields.

## 9. Failure and determinism

The same pinned input, validated intent, chart-policy version, and chart-contract version must produce the same `ChartSpec`. Stable ordering is mandatory. Host time, randomness, model text, and browser state cannot change chart values.

A chart construction or rendering failure does not change the canonical report or validated answer. The product returns the validated content and an explicit chart-unavailable state. A chart failure does not block formal Submission export.

## 10. Ownership summary

| Owner | Responsibility |
|---|---|
| Report Evidence Builder | Create and store report-linked `ChartSpec` records from pinned evidence. |
| Report and Dashboard API | Recheck access, deliver stored report charts, and create interactive charts from validated bounded results. |
| Shared Chart Presentation Library | Supply one deterministic internal contract, builder, validator, and serializer. |
| Web Application | Map `ChartSpec` to ECharts and render the chart. |
| Submission Exporter | Export only formal brief and QA fields. |
| Agent Runtime | Produce a candidate answer and optional `ChartIntent`; never produce authoritative chart values. |

