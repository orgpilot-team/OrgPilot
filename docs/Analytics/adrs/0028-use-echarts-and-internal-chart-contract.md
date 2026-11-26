# 28. Use ECharts with an internal chart presentation contract

Date: 2026-11-24

## Status

Accepted

## Context

OrgPilot must present charts in the Web Application for reports, chat answers, dashboards, and workflow views. The graded evaluation does not run the Web Application and accepts only the formal brief and QA JSON files below `OUTPUT_DIR`. The formal schemas do not contain chart fields.

The Web Application is forbidden to calculate KPI or chart data. Report Evidence Builder already owns deterministic report evidence. Query Gateway already owns bounded query execution for interactive answers. Backend API and Background Worker both use .NET 10 and can consume one shared .NET contract.

Without one internal contract, report and interactive chart paths can drift in field names, ordering, validation, scope handling, and serialization. Returning ECharts options from Backend would also couple product data contracts to one frontend library.

## Decision

Apache ECharts is the Web Application chart renderer. It runs only in the Web Application and is installed at build time.

The product uses three internal types:

- `ChartIntent` describes an optional requested chart without authoritative values.
- `ChartSpec` contains deterministic authorized chart data and lineage in a rendering-library-neutral format.
- `PresentationResponse` combines validated content with zero or more `ChartSpec` values for the Web Application.

One Shared Chart Presentation Library supplies these types, deterministic construction, validation, stable serialization, and contract versioning. It is shared by Background Worker and Backend API. It is not a C4 component or data owner.

Report Evidence Builder creates and stores report-linked chart specifications from pinned manager evidence. Report and Dashboard API reads and delivers those stored specifications. For a validated interactive answer, Report and Dashboard API uses the same library to create a chart specification from the validated `ChartIntent` and persisted bounded query result.

The Agent Runtime can propose `ChartIntent`. It cannot supply authoritative chart values. The Web Application maps `ChartSpec` to an ECharts option and owns only presentation behavior.

Submission Exporter excludes every internal chart-presentation field. `brief_schema.json`, `qa_answer_schema.json`, and the two formal output paths remain unchanged.

## Consequences

Report and interactive charts use one versioned contract and one deterministic construction rule. Stored report charts remain aligned with immutable report versions and restatements. Interactive charts remain aligned with validated query results and `query_id` lineage.

Backend code is independent of ECharts. A later renderer change does not require a business-data contract change. ECharts failure does not change canonical report or answer content and does not block formal export.

The product must add contract validation, point and series limits, chart-policy versioning, scoped persistence, frontend mapping, RTL presentation rules, and explicit chart-unavailable behavior.

## Related requirements

- The Web Application does not calculate KPI or chart data.
- Every chart value maps to pinned report evidence or a validated bounded query result.
- Backend authorization is applied before chart delivery.
- Formal Submission output contains no internal chart field.
- Evaluation succeeds without the Web Application.

## Related model elements

- Web Application
- Conversational Assistant UI
- Role-Based Dashboard UI
- Backend API
- Report and Dashboard API
- Background Worker
- Report Evidence Builder
- PostgreSQL
- Submission Exporter

