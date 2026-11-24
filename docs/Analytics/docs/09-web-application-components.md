# Web Application components

## Purpose and Scope

The Web Application supplies the three Persian RTL management interfaces. It displays authorized data and sends user actions to the Backend API.

## Runtime Technology

React 19, TypeScript, Vite, and Apache ECharts.

## Trust Boundary

The browser is not trusted. The Backend API authenticates and authorizes every request. The UI does not make access decisions.

## Allowed Responsibilities

- Display authorized reports, metrics, workflow state, and decision state.
- Map authorized `ChartSpec` values to ECharts options and render them.
- Collect scoped questions, uploads, and manager commands.
- Send requests to the Backend API over HTTPS/JSON.

## Forbidden Responsibilities

- Run business rules, KPI calculations, or agent graphs.
- Calculate, regroup, complete, or correct chart data.
- Read PostgreSQL, the protected archive, or input contracts directly.
- Treat hidden UI state as an authorization control.

## Component Map

| DSL identifier | Component | Primary users |
|---|---|---|
| `chatUi` | Conversational Assistant UI | Senior Manager, Unit Manager, Team Supervisor |
| `dashboardUi` | Role-Based Dashboard UI | Senior Manager, Unit Manager, Team Supervisor |
| `workflowUi` | Workflow Control Room UI | Senior Manager |

## Internal Relationships

The three components share the same Web Application runtime. They do not call each other and do not share business state.

## External Relationships

Each component calls the Backend API over HTTPS/JSON. The Web Application can send redacted telemetry to the optional OpenTelemetry Collector.

## Chart Rendering Boundary

The Web Application receives the internal Presentation response defined in doc 17. It contains validated content and zero or more `ChartSpec` values. A frontend mapping function converts each `ChartSpec` to an ECharts option. The mapping owns layout, RTL labels, typography, color, tooltip, legend, responsive behavior, and accessible text. It does not own chart values, KPI rules, grouping, targets, evidence, or authorization.

The frontend mapping function is not part of the Shared Chart Presentation Library because that library is .NET and contains no ECharts or React code. The `ChartSpec` contract remains independent of the rendering library.

## Component Sections

<a id="conversational-assistant-ui"></a>

### Conversational Assistant UI

- **DSL identifier:** `chatUi`
- **Display name:** Conversational Assistant UI
- **Purpose:** Display reports and bounded answers and collect scoped manager input.
- **Responsibilities:** Show briefs and bounded answers, render authorized `ChartSpec` values beside their related message or report item, submit questions, upload documents, submit `CloseSignal`, `ReferSignal`, `SetManagerPriority`, `ChangeKpiTarget`, and `ChangeKpiThreshold` operations, and show job or review state.
- **Inputs:** User actions and authorized Backend API Presentation responses.
- **Outputs:** Authenticated HTTPS/JSON requests and rendered results.
- **Owned state:** Temporary browser view state only.
- **Dependencies:** Backend API and the trusted browser session.
- **Security boundary:** Treat all browser input as untrusted and do not store secrets in client state.
- **Forbidden responsibilities:** KPI or chart-data calculation, evidence access, authorization, agent execution, and publication.
- **Failure behavior:** Show an explicit error or persisted job state. Do not invent an answer.
- **Idempotency:** Use server-issued identifiers and idempotency data for repeated commands.
- **Observability:** Emit redacted UI request and error telemetry when collection is active.
- **Related ADRs:** ADR-0005, ADR-0008, ADR-0010, ADR-0019, ADR-0020.
- **Open issues:** Authentication product and method remain open.

<a id="role-based-dashboard-ui"></a>

### Role-Based Dashboard UI

- **DSL identifier:** `dashboardUi`
- **Display name:** Role-Based Dashboard UI
- **Purpose:** Display authorized KPIs, targets, trends, drill-downs, decisions, and open actions.
- **Responsibilities:** Request and render role-scoped management data, deterministic `ChartSpec` values, and direct-workload detail when allowed.
- **Inputs:** Trusted session context and authorized report or dashboard responses.
- **Outputs:** HTTPS/JSON read requests and rendered dashboards.
- **Owned state:** Temporary filters and presentation state only.
- **Dependencies:** Backend Report and Dashboard API.
- **Security boundary:** The Backend API enforces row, column, role, purpose, and policy scope.
- **Forbidden responsibilities:** Direct database access, access-policy decisions, KPI or chart-data calculation, and data correction.
- **Failure behavior:** Show an explicit unavailable or forbidden state. Do not reuse data from another scope.
- **Idempotency:** Read operations are safe to repeat.
- **Observability:** Emit redacted page, request, latency, and error telemetry when collection is active.
- **Related ADRs:** ADR-0002, ADR-0005, ADR-0009, ADR-0020.
- **Open issues:** No component-specific open issue.

<a id="workflow-control-room-ui"></a>

### Workflow Control Room UI

- **DSL identifier:** `workflowUi`
- **Display name:** Workflow Control Room UI
- **Purpose:** Display WF1-WF3, stage SLA, bottlenecks, escalations, and pending decisions.
- **Responsibilities:** Present executive workflow state and request authorized workflow drill-downs.
- **Inputs:** Senior Manager actions and authorized workflow responses.
- **Outputs:** HTTPS/JSON read requests and rendered workflow views.
- **Owned state:** Temporary filters and presentation state only.
- **Dependencies:** Backend Report and Dashboard API.
- **Security boundary:** Access is for the Senior Manager role. The Backend API verifies the role on each request.
- **Forbidden responsibilities:** Workflow reconstruction, escalation calculation, authorization, and direct database access.
- **Failure behavior:** Show an explicit unavailable or forbidden state and clear stale scoped data.
- **Idempotency:** Read operations are safe to repeat.
- **Observability:** Emit redacted workflow-view latency and error telemetry when collection is active.
- **Related ADRs:** ADR-0005, ADR-0006, ADR-0007, ADR-0020.
- **Open issues:** No component-specific open issue.

## Container-level Open Issues

- The authentication product and method remain open.
- The Web-to-Collector transport is OTLP/HTTP when optional telemetry is active.
