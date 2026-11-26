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

Chart capability is mandatory for the product. A specific response can contain zero charts when no chart is requested, the result shape is incompatible, or chart construction or rendering fails. Validated content remains available.

The exact versioned JSON wire schema for `PresentationResponse`, `ChartSpec`, series, points, targets, states, and lineage must be published through the Backend OpenAPI contract before production frontend integration. This document defines semantic authority. OpenAPI defines exact wire names, required fields, nullability, formats, enumerations, and compatibility metadata.

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

The repository location and folder layout are pending a separate architecture decision. The library remains a build-time dependency of Backend API and Background Worker. Its future physical location will not make it a C4 component.

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
- ECharts initialization, update, resize, failure isolation, and disposal

The mapping must preserve point order, values, units, target values, and evidence identity. It must not calculate, regroup, interpolate, or correct business data.

The mapping must not round an authoritative KPI. If a tooltip, label, or table needs formatted numeric text, it uses the approved display representation or formatting metadata from the accepted wire contract. The exact numeric display contract remains open.

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
- The OpenAPI response version is supported by the Web Application.
- The complete response passes runtime validation before it enters a cache or renderer.

The browser is not an authorization boundary. Hidden series, disabled controls, or frontend filters do not replace Backend authorization.

If one chart fails browser validation, the Web Application isolates that chart and shows its explicit unavailable state. It preserves the validated content and any other independently valid chart. Browser validation does not replace Backend validation or authorization.

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

## 11. OpenAPI wire contract and TypeScript generation

The Backend owns one versioned OpenAPI contract for Web Application requests and responses. The contract includes `PresentationResponse` and every nested chart type that crosses the HTTP boundary.

Frontend TypeScript request and response types are generated from that contract. Do not maintain an independent handwritten TypeScript copy of `ChartIntent`, `ChartSpec`, `PresentationResponse`, series, point, target, or response-state wire types.

Static TypeScript types do not validate network data. The Web Application must use runtime validation derived from the same accepted machine-readable contract before a Presentation response enters scope-sensitive cache or rendering code. The exact generator and validation library are implementation decisions. They must not create a second contract authority.

The Shared Chart Presentation Library remains the semantic and deterministic construction authority for Backend and Worker code. The OpenAPI artifact is the exact Web wire authority. Contract tests must prove that serialized .NET responses conform to the published OpenAPI schema.

Renderer-neutral generated types must not import React, Ant Design, Motion, ECharts, React Flow, or a future 3D renderer. ECharts-specific types begin only at the frontend mapper boundary.

A build or CI check must detect a changed Backend wire contract that has not produced the corresponding generated frontend artifacts and contract tests.

The exact OpenAPI file path, generation command, schema version value, and compatibility window remain open until the Backend API project structure exists. This document does not invent those values.

## 12. Chart-type policy, structures, and limits

The chart-type allowlist is finite and versioned. It uses OrgPilot semantic chart types, not arbitrary ECharts series names. An unlisted type is unsupported.

Each allowlisted type must define:

- Compatible result shapes.
- Required category, time, series, point, target, and lineage semantics.
- Null behavior.
- Ordering rules.
- Whether stacking, comparison, targets, thresholds, or multiple axes are permitted.
- Its fixed local mapper and accessible alternative.

An ECharts Custom Series is permitted only behind an approved semantic chart type. Custom rendering code is fixed frontend code. A response cannot supply JavaScript, callbacks, drawing commands, HTML, or ECharts option fragments.

The exact initial allowlist remains open. It must be derived from approved manager scenarios before production chart integration. The frontend must not accept an arbitrary type while this decision is open.

Exact limits are also open and must be accepted before production integration:

- Maximum charts per response.
- Maximum series per chart.
- Maximum points per series and per chart.
- Maximum categories, targets, lineage references, and label lengths.
- Maximum response size where applicable.

Limits are enforced during construction, before persistence, before delivery, and during browser validation. The frontend does not silently truncate, sample, regroup, or aggregate an oversized chart. The product returns an explicit chart-unavailable state unless an approved Backend policy creates a new valid bounded specification from authorized data.

The exact series and point wire structures belong to OpenAPI. They must include stable identity, ordered values, nullability, unit or approved display semantics, and applicable evidence lineage. This document does not invent field names that are not yet approved.

## 13. Compatibility and unsupported behavior

The wire contract must define a supported-version policy before production integration. An unknown incompatible version is not mapped by best effort. It produces an explicit chart-unavailable state while validated content remains visible.

An unsupported chart type is not changed automatically to another type because that change can alter meaning. The response produces an explicit unsupported state. A different chart type requires a new valid `ChartSpec` from an approved Backend policy.

Additive compatibility, required-field changes, enumerations, and version retirement rules belong to the accepted OpenAPI contract. Their exact values remain open.

## 14. Safe labels, tooltips, and mapping tests

Labels, titles, series names, categories, empty-state text, evidence labels, and tooltip values are untrusted text.

- Use fixed local tooltip and label formatters.
- Treat response strings as text, not HTML.
- Do not use raw HTML or executable formatter content from a response.
- Apply approved length limits.
- Preserve bidirectional isolation for mixed Persian and technical identifiers.
- Do not create a new factual statement in a label, legend, tooltip, annotation, or accessible description.

Frontend mapping tests are required for every allowlisted chart type. They must prove:

- Input immutability.
- Stable point and series order.
- Exact preservation of values, `null`, units, targets, and evidence identity.
- No browser-side KPI calculation, rounding, regrouping, interpolation, or aggregation.
- Safe behavior for unknown versions, unsupported types, invalid labels, oversized input, and renderer failure.
- Loading, empty, unavailable, forbidden, incomplete, and error states.
- Keyboard and screen-reader behavior.
- Correct initialization, update, resize, and disposal without retained renderer resources.

Production API integration and mapping against real responses remain blocked until the OpenAPI schema, allowlist, limits, numeric display contract, and compatibility policy are approved. Mapper prototypes can use clearly separated non-production mock contracts and must not establish an alternative wire authority.

