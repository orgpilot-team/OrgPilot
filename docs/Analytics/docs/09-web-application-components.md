# Web Application components and frontend architecture

## Scope and authority

The DIDRAH Web Application is one desktop application with three Persian RTL management interfaces. It presents authorized data and sends manager requests to the Backend API. [Structurizr workspace](../workspace.dsl) · [ADR-0029](../adrs/0029-adopt-feature-based-web-application-and-progressive-presentation.md)

This document owns the frontend architecture. Use the owning documents for security, quality gates, chart and wire contracts, design policies, and stage progress. [Doc 04](04-security-and-trust.md) · [Doc 07](07-quality-attributes.md) · [Doc 17](17-chart-presentation-contract.md) · [Doc 18](18-ux-and-design-system.md) · [Frontend roadmap](../../FRONTEND_DEVELOPMENT_STAGES.md)

## Accepted target architecture

React 19 and TypeScript supply the application runtime and types. Vite supplies development and build tooling. Ant Design supplies the UI foundation. Motion supplies purposeful transitions, ECharts renders charts, and React Flow is an option for suitable workflow views. CSS and SVG support custom 2D presentation. The Design System supplies the product visual identity across these technologies. [WebApp dependencies](../../../src/WebApp/package.json) · [ADR-0029](../adrs/0029-adopt-feature-based-web-application-and-progressive-presentation.md)

Each feature owns its pages, view models, feature-specific presentation behavior, and temporary view state. Features must not call each other, import each other's internal code, or share business state. Shared code must serve more than one real consumer or implement an accepted boundary. Put business rules and domain state in their accepted Backend, Worker, or Agent Runtime boundaries. Frontend aggregates, repositories, domain events, and business-rule engines are prohibited. [Domain model](16-domain-model.md)

Add dependencies only for a concrete requirement. Avoid frameworks that duplicate accepted UI, styling, state, or query-cache responsibilities.

The Web Application is for the development and demonstration profile. The graded batch run does not use it. [Deployment profiles](06-deployment-and-operations.md)

## Current implementation

| Area | Available now |
|---|---|
| Application entry and providers | Vite entry, shared theme and Ant Design providers, and a placeholder outside the Lab. [Entry point](../../../src/WebApp/src/main.tsx) · [AppProviders](../../../src/WebApp/src/app/AppProviders.tsx) |
| Design System | Shared tokens, Dark and Light Mode, local Dastkhat typography, Ant Design styles, and reusable UI patterns. [Design policies and source links](18-ux-and-design-system.md) |
| Visualizations | Two reusable ECharts sales charts with Lab data and a React Flow specimen with a fixed workflow fixture. [Chart sources](../../../src/WebApp/src/shared/visualization/charts/) · [Workflow specimen](../../../src/WebApp/src/app/design-system-lab/WorkflowSpecimen.tsx) |
| Design System Lab | Development-only route at `/design-system`. It renders reusable components and supplies their specimens, mock data, and review controls. [Lab](../../../src/WebApp/src/app/design-system-lab/DesignSystemLab.tsx) |
| Product pages and integration | The three feature directories and the shared API, session, and observability directories are placeholders. The product Application Shell and authenticated Backend integration are planned. [Frontend source](../../../src/WebApp/src/) · [Frontend roadmap](../../FRONTEND_DEVELOPMENT_STAGES.md) |

## Application Shell and shared ownership

The Application Shell owns application composition, routing, primary navigation, and provider setup. It presents navigation based on Backend-supplied access context. The Assistant owns conversation history, the draft and attachment data, and the effects of conversation and composer actions. Reusable navigation and composer components present the state supplied by their callers.

| Owner | Responsibility |
|---|---|
| Shared Design System | Tokens, theme adapters, generic UI, Ant Design variants, and shared interaction styling. [Shared Design System](../../../src/WebApp/src/shared/design-system/) · [Doc 18](18-ux-and-design-system.md) |
| Shared visualization | Reusable charts, chart mapping and lifecycle, theme adapters, and reusable workflow presentation primitives. [Shared visualization](../../../src/WebApp/src/shared/visualization/) |
| Shared integration and utilities | Generated API types, response validation, HTTP transport and request cancellation, session lifecycle, scope-aware cache support, optional redacted telemetry, and focused technical utilities. |
| Design System Lab | Specimen composition, mock data, reference examples, review scenarios, and development and benchmark controls. [Lab responsibilities](18-ux-and-design-system.md#design-system-lab) |

The Design System must not define business rules, authorization, KPI meaning, workflow ownership, or decision rules.

Reusable components accept typed inputs. Keep mock data, transport, and feature business logic in their owning modules. Shared modules must not import the Lab. The Design System and Lab are internal modules within the same Web Application deployment. The three features below are the C4 components. [Frontend rules](../../../src/WebApp/AGENTS.md)

## Component map

| DSL identifier | Feature directory under `src` | Component | Primary users |
|---|---|---|---|
| `chatUi` | `features/assistant/` | [Conversational Assistant UI](#conversational-assistant-ui) | Senior Manager, Unit Manager, Team Supervisor |
| `dashboardUi` | `features/dashboard/` | [Role-Based Dashboard UI](#role-based-dashboard-ui) | Senior Manager, Unit Manager, Team Supervisor |
| `workflowUi` | `features/workflow-control/` | [Workflow Control Room UI](#workflow-control-room-ui) | Senior Manager |

The following sections describe product responsibilities. All three product pages are planned.

<a id="conversational-assistant-ui"></a>

### Conversational Assistant UI

Display briefs, bounded answers, and associated authorized charts. Collect scoped questions and uploads. Submit explicit, confirmed manager actions for `CloseSignal`, `ReferSignal`, `SetManagerPriority`, `ChangeKpiTarget`, and `ChangeKpiThreshold`. Display persisted job and review states or an explicit error. Use server-issued identifiers and idempotency data for repeated commands. The Backend owns evidence access, job execution, validation, and publication. [Runtime flows](05-runtime-flows.md) · [Backend API](10-backend-api-components.md)

<a id="role-based-dashboard-ui"></a>

### Role-Based Dashboard UI

Request and present authorized KPIs, targets, trends, drill-downs, decisions, and open actions. Show direct workload details only where the Backend permits them. Own temporary filters and view state. Use repeatable reads via Report and Dashboard API. Show explicit unavailable or forbidden states and apply scope invalidation. [Security and trust](04-security-and-trust.md) · [Backend API](10-backend-api-components.md)

<a id="workflow-control-room-ui"></a>

### Workflow Control Room UI

Present Backend-supplied WF1–WF3 state, stage SLA, bottlenecks, escalations, and pending decisions for the Senior Manager. Use repeatable reads for authorized drill-downs. Show explicit unavailable or forbidden states and clear stale scoped data. Workflow reconstruction and calculations remain with the Backend and Worker. React Flow or custom 2D presentation can be used when suitable. The production renderer remains open. [Backend API](10-backend-api-components.md) · [Background Worker](11-background-worker-components.md) · [Open decisions](08-risks-and-open-issues.md#open-decisions)

## Backend integration and trust

The browser is untrusted. Each feature calls the Backend API over HTTPS/JSON. The Backend validates the session and authorizes each request. It owns role, resource, row, column, purpose, organization, and policy scope. The browser must not execute organizational decisions or submit unconfirmed manager actions. It must not accept executable HTML, chart options, callbacks, or formatter code from the Backend or model output. Hidden controls do not enforce access. The browser does not read PostgreSQL, protected archives, or input contracts directly. [Security and trust](04-security-and-trust.md)

Shared session infrastructure can manage the validated user context, login and logout presentation, expiration, and scope invalidation. Follow Doc 04 for cache isolation, stale requests, restricted storage, and safe content. Authentication product, protocol, and credential storage remain open. The Access Projection Matrix is required before production scoped integration. [Security and trust](04-security-and-trust.md) · [Open decisions](08-risks-and-open-issues.md#open-decisions)

Generate frontend wire types in one location from versioned Backend OpenAPI. Do not maintain a manual copy of Backend wire types. Keep contract types independent of renderers and UI libraries. Validate the response at runtime before it reaches scope-sensitive caches or renderers, under Doc 17. Production integration and security-sensitive actions wait for their approved contracts and decisions. Use isolated mock data for early layout and UX work. Mock data must never grant access or define a production wire contract. [Chart presentation contract](17-chart-presentation-contract.md)

Optional browser telemetry is redacted. When export is active, it uses OTLP/HTTP to the OpenTelemetry Collector. The application remains usable when telemetry is disabled or unavailable. [Security and trust](04-security-and-trust.md) · [Structurizr workspace](../workspace.dsl)

## Visualization architecture

The Backend supplies validated content and authorized, renderer-neutral `ChartSpec` values in the Presentation response. The browser maps supported specifications to ECharts options. Chart capability is required, and individual responses can contain zero charts. Doc 17 governs value preservation, missing values, ordering, units, targets, evidence identity, approved numeric presentation, safe text, and failure isolation. The browser must not compute KPI or chart data, infer business causes, or detect signals. [Chart presentation contract](17-chart-presentation-contract.md)

The reusable sales charts currently take typed component inputs. Production still needs the approved wire contract, generated types, runtime validation, and the authorized `ChartSpec` mapper. The chart host owns initialization, updates, resize, rendering failure isolation, and disposal. [Sales trend chart](../../../src/WebApp/src/shared/visualization/charts/SalesTrendChart.tsx) · [Branch sales chart](../../../src/WebApp/src/shared/visualization/charts/BranchSalesChart.tsx) · [ChartHost](../../../src/WebApp/src/shared/visualization/charts/ChartHost.tsx)

Workflow visuals and custom infographics present authorized facts. Layout and interaction can help the user interpret those facts. The visualization cannot change workflow ownership, escalation, evidence, or SLA meaning. [Visualization design policies](18-ux-and-design-system.md#information-and-visualization-design)

## Presentation modes

### Classic Mode

Classic Mode is the default, mandatory, and complete 2D product experience. It uses local build assets and has no Three.js or 3D asset dependency. [Motion and chart redraw policy](18-ux-and-design-system.md#luminous-chart-motion)

### Modern Mode

Modern Mode is deferred until Classic is functionally complete. It can add selected 3D views with lazy-loaded code and assets from the same Web deployment. Use the same features, Design System, API contracts, authorized state, and business behavior. Use 2D presentation where suitable and fall back to the complete Classic experience when 3D is unavailable or fails. Modern adds no deployment, service, route family, or authorization boundary. The renderer, browser and hardware profiles, asset choices, and activation policy remain deferred. [ADR-0029](../adrs/0029-adopt-feature-based-web-application-and-progressive-presentation.md)

## Target directory structure

Paths are relative to `src/WebApp`. Add code and subdirectories when their owners need them. Do not add generic `utils`, `hooks`, `types`, or `state` directories without a concrete owner and use. Keep tests near the code they verify, with end-to-end tests in `e2e/`. Use the repository conventions for naming. [Coding conventions](../../CODING_CONVENTIONS.md)

| Path | Owner or purpose |
|---|---|
| `src/main.tsx`, `src/app/` | Entry point, Application Shell, routes, providers, and configuration |
| `src/app/design-system-lab/` | Development-only Lab |
| `src/features/{assistant,dashboard,workflow-control}/` | Three feature boundaries |
| `src/shared/design-system/` | Tokens, themes, shared styles, and UI patterns |
| `src/shared/visualization/{charts,workflow}/` | Chart and workflow presentation |
| `src/shared/api/` | Generated API client and types, HTTP transport, and response validation |
| `src/shared/session/`, `src/shared/observability/` | Session and scope lifecycle, and optional browser telemetry |
| `public/`, `e2e/` | Assets that need public URLs, and end-to-end tests when required |
