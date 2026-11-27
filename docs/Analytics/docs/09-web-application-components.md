# Web Application components and frontend architecture

## Purpose and scope

The DIDRAH Web Application supplies the three Persian RTL management interfaces in desktop browsers. It displays authorized data and sends user actions to the Backend API.

DIDRAH is desktop-only. Mobile and tablet layouts, breakpoints, screenshots, and device-specific validation are out of scope. The frontend must support resizing at supported desktop viewports, keyboard access, and visible focus states. The exact desktop viewport matrix remains open. Keep the approved Dastkhat typography in use. Defer global typography refinement until the initial component families are complete.

This document is the architecture source for the Web Application. It owns the frontend technology stack, feature boundaries, presentation-mode policy, Design System boundary, shared-module rules, session responsibilities, target directory structure, and implementation boundaries.

It does not redefine these concerns:

- Security, session isolation, and scope-aware caching are defined in `04-security-and-trust.md`.
- Frontend quality attributes and quality gates are defined in `07-quality-attributes.md`.
- Chart, Presentation response, OpenAPI wire, validation, and ECharts mapping rules are defined in `17-chart-presentation-contract.md`.
- Visual identity, design tokens, typography, and interaction guidance are defined in `18-ux-and-design-system.md`.

## Runtime technology

The accepted frontend technologies are:

| Technology | Responsibility |
|---|---|
| React 19 | Web Application framework and component composition |
| TypeScript | Static type safety and generated API contract consumption |
| Vite | Build and development tooling |
| Ant Design | UI component foundation under the OrgPilot Design System |
| Motion | Purposeful transitions and micro-interactions |
| Apache ECharts | Deterministic rendering of authorized `ChartSpec` values |
| React Flow | Interactive workflow presentation where it is suitable |
| CSS and SVG | Custom interfaces and interactive 2D infographics |
| OpenTelemetry JavaScript | Optional redacted trace correlation and fail-open telemetry export |

Ant Design does not define the product visual identity. The OrgPilot Design System controls tokens, component variants, RTL behavior, accessibility, and renderer styling.

No additional general UI framework, global state framework, query-cache framework, or styling framework is approved by this document. A new dependency needs a concrete requirement and must not duplicate an accepted responsibility.

Three.js, 3D assets, and WebGPU or WebGL 2 renderer selection are deferred. They are not first-release dependencies.

## Trust boundary

The browser is not trusted. The Backend API authenticates and authorizes every request. The UI does not make access decisions.

The Web Application can manage a server-validated session context and temporary presentation state. It cannot act as an authentication or authorization authority. Authentication product, protocol, and credential-storage decisions remain open.

Detailed session, cache, stale-request, content-rendering, and telemetry rules are in `04-security-and-trust.md`.

## Presentation modes

### Classic Mode

Classic Mode is the default and mandatory product experience. It supplies complete functional coverage with interactive 2D presentation.

Classic Mode can use Ant Design, ECharts, React Flow, Motion, CSS, SVG, gradients, shadows, glow, and depth effects. It does not load Three.js, 3D models, or Modern-only assets.

#### Classic chart redraw budget

The approved default is 30 redraws per second per chart during scheduled motion for the two luminous Classic Mode sales charts. Both charts stop continuous redraws at idle. The Lab provides a Native comparison for validation. See [doc 18](18-ux-and-design-system.md#luminous-chart-motion) for timing, motion behavior, and measurement evidence.

### Modern Mode

Modern Mode is a deferred future enhancement. It can add selected 3D scenes only after Classic Mode is functionally complete.

Modern Mode must:

- Use the same Web Application, Design System, features, API contracts, and authorized state as Classic Mode.
- Use lazy loading for its renderer code and assets.
- Limit 3D to selected visualization areas.
- Continue to use ECharts and 2D components where they are suitable.
- Fall back to the complete Classic experience when 3D is unavailable or fails.
- Avoid becoming a dependency of Classic Mode.

The initial 30 FPS goal for active 3D rendering remains a proposal. The renderer, browser, hardware, model format, and asset delivery decisions remain open.

### Shared mode rules

- There is one Web Application and one deployment unit.
- There is one Design System and one product UX.
- There is one set of business capabilities and API contracts.
- Features do not duplicate business logic or authorized state for each mode.
- Modern Mode is not a C4 component, service, route family, or authorization boundary.

## Feature-based architecture

The Web Application uses a lightweight feature-based architecture. The three features match the accepted C4 components:

| DSL identifier | Feature directory | Component |
|---|---|---|
| `chatUi` | `features/assistant` | Conversational Assistant UI |
| `dashboardUi` | `features/dashboard` | Role-Based Dashboard UI |
| `workflowUi` | `features/workflow-control` | Workflow Control Room UI |

Each feature owns its page composition, feature-specific presentation state, view models, and UI behavior. A feature must not import another feature's internal implementation. A feature must not call another feature or use another feature as a business-state store.

Shared code is permitted only when it has more than one real consumer or when it implements one accepted cross-cutting boundary. Shared code can include:

- The OrgPilot Design System and generic UI components.
- Generated renderer-neutral API types and runtime response validation.
- The HTTP client and request-cancellation support.
- Session lifecycle and scope-aware cache infrastructure.
- `ChartSpec` to ECharts mapping and chart lifecycle support.
- Generic React Flow presentation primitives.
- Shared Motion presets.
- Redacted telemetry.
- Focused technical utilities.

The shared area must not become a general dumping area. Feature-specific types, components, hooks, and state stay in their feature.

Tactical DDD does not apply to the Web Application. Do not create frontend aggregates, repositories, domain events, business-rule engines, or a duplicate domain model.

## Target repository structure

The structure below is a target shape. Create a directory only when it contains required code. Empty directories and speculative wrappers are not required.

```text
src/WebApp/
├── public/                         # Assets that require public URLs
├── src/
│   ├── app/                        # Composition, routes, providers, and configuration
│   ├── features/
│   │   ├── assistant/
│   │   ├── dashboard/
│   │   └── workflow-control/
│   ├── shared/
│   │   ├── api/                    # Generated client/types, transport, validation
│   │   ├── design-system/          # Tokens, theme, shared component variants
│   │   ├── visualization/
│   │   │   ├── charts/             # ECharts mappers and lifecycle
│   │   │   └── workflow/           # Generic React Flow presentation
│   │   ├── session/
│   │   └── observability/
│   └── main.tsx
├── e2e/                            # Add when end-to-end tests start
├── index.html
├── package.json
├── package-lock.json
├── tsconfig.json
└── vite.config.ts
```

Tests should stay next to the code they verify unless they are end-to-end tests. Do not create generic `utils`, `types`, `hooks`, or `state` directories without a concrete owner and use.

Generated API types must have one location. Do not hand-maintain a second TypeScript copy of Backend wire contracts. Renderer-neutral contract types must not import ECharts, React Flow, Motion, Ant Design, or a future 3D library.

### Current frontend paths

The approved Stage 4.5-R5.5 baseline and the approved shared patterns are in `src/WebApp`. The table lists paths relative to that directory.

| Path | Responsibility |
|---|---|
| `src/main.tsx` and `src/app/AppProviders.tsx` | Application entry point and provider composition |
| `src/app/design-system-lab/` | Development-only Lab at `/design-system`, with specimens, fixtures, and validation controls |
| `src/shared/design-system/tokens/` | Global Design Tokens |
| `src/shared/design-system/theme/` and `src/shared/design-system/styles/` | Theme provider and adapters, font, and global styles |
| `src/shared/design-system/patterns/` | Reusable UI patterns |
| `src/shared/visualization/charts/` | Reusable ECharts components, renderer lifecycle, chart theme, and chart motion |
| `src/shared/visualization/workflow/` | Reusable React Flow presentation such as `WorkflowNode.tsx` |
| `public/fonts/dastkhat/` and `public/licenses/dastkhat/` | Local Dastkhat font, notice, and license |
| `AGENTS.md` and `.agents/skills/didrah-component-workflow/` | Frontend rules, component workflow, and acceptance checklist |

Use PascalCase for React component names and their filenames, such as `SalesTrendChart.tsx` and `AppProviders.tsx`. Keep internal directory names lowercase and use kebab-case for multiword feature directories. See the [repository coding conventions](../../CODING_CONVENTIONS.md).

## Design System architecture

The OrgPilot Design System is an internal shared module. It is not a C4 component, service, store, or deployment unit.

It supplies shared tokens and presentation rules to:

- Ant Design theme configuration and component variants.
- ECharts mappers.
- React Flow nodes and edges.
- Motion presets.
- Custom CSS and SVG.
- Future Modern scenes when that work is approved.

The Design System can define visual and interaction behavior. It cannot define business status, authorization, KPI meaning, chart values, workflow ownership, signal state, or decision rules.

The approved token architecture and visual scope are in [doc 18](18-ux-and-design-system.md).

### Reusable component ownership and the Lab

- The shared Design System owns generic UI such as `Panel`, `SectionHeader`, and `PanelState`. Shared visualization owns reusable charts and workflow primitives. The owning feature supplies feature-specific composition and temporary UI state. Business decisions remain with their accepted Backend owners.
- Reusable components accept typed inputs and work with callers outside the Lab. Keep transport, mock fixtures, and feature business logic outside reusable presentation.
- The Design System Lab consumes the actual reusable components. It owns specimen composition, mock fixtures, reference specimens, validation scenarios, and development and benchmark controls. Shared modules must never import from the Lab.
- Follow the permanent frontend rules and use the DIDRAH component workflow and checklist for applicable component design, implementation, and validation. [Frontend AGENTS.md](../../../src/WebApp/AGENTS.md) · [DIDRAH component workflow](../../../src/WebApp/.agents/skills/didrah-component-workflow/SKILL.md) · [Acceptance checklist](../../../src/WebApp/.agents/skills/didrah-component-workflow/references/component-checklist.md)

### Approved shared UI patterns

The shared Design System owns the patterns below. Their TypeScript modules define the public interfaces. Their local CSS files and SVG define the approved visual details. See [Doc 18 for the visual specifications and approval record](18-ux-and-design-system.md#approved-shared-ui-patterns).

| Component | Canonical modules under `src/WebApp` | Public interface |
|---|---|---|
| `WelcomeProfileCard` | `src/shared/design-system/patterns/WelcomeProfileCard.tsx` and `src/shared/design-system/patterns/welcome-profile-card.css` | `WelcomeProfileCardProps` has required `managerName: string` and `date: Date`, and optional `avatarSrc?: string`. Supply a valid date. The card formats the local day in Tehran. |
| `NavigationHistorySidebar` | `src/shared/design-system/patterns/NavigationHistorySidebar.tsx` and `src/shared/design-system/patterns/navigation-history-sidebar.css` | `NavigationHistorySidebarProps` has `groups: readonly NavigationHistoryGroup[]`, `activeItemId: string \| null`, `onSelect(itemId: string)`, `onDelete(itemId: string)`, `onNewChat()`, and `onSettings()`. Each callback returns `void`. |
| `LuminousChatComposer` | [Component](../../../src/WebApp/src/shared/design-system/patterns/LuminousChatComposer.tsx) and [CSS](../../../src/WebApp/src/shared/design-system/patterns/luminous-chat-composer.css) | `LuminousChatComposerProps` requires `value: string`, `attachments: readonly LuminousChatAttachment[]`, `onChange(value: string)`, `onFilesSelected(files: readonly File[])`, `onRemoveAttachment(id: string)`, `onSubmit(value: string, attachments: readonly LuminousChatAttachment[])`, and `onStop()`. Optional props are `placeholder?: string`, `accept?: string`, `disabled?: boolean`, and `processing?: boolean`. Each callback returns `void`. |
| `PrimaryNavigationMenu` | [Component](../../../src/WebApp/src/shared/design-system/patterns/PrimaryNavigationMenu.tsx) and [CSS](../../../src/WebApp/src/shared/design-system/patterns/primary-navigation-menu.css) | Readonly `PrimaryNavigationMenuProps` requires `items: readonly PrimaryNavigationItem[]`, `activeItemId: string \| null`, and `onNavigate(itemId: string): void`. Optional `ariaLabel?: string` sets the navigation landmark name. |

A `NavigationHistoryGroup` has a string `id`, a string `label`, and an `items` field of type `readonly NavigationHistoryItem[]`. Each item has a string `id` and a string `title`. The group and item fields are readonly. Use stable group IDs and unique, stable item IDs. The caller supplies the groups and controls the active item. A null active ID means no selection.

The sidebar presents AI conversation history for the Conversational Assistant UI. The application shell owns primary navigation. The Assistant feature owns conversation data, grouping, selection state, and the effects of the callbacks. The sidebar owns temporary title search, list scrolling, and selected-row rendering. It filters the supplied groups locally.

`WelcomeProfileCard` uses `Panel` and reads and updates the shared theme through `useDidrahTheme`. The sidebar reads root `data-theme` and semantic CSS variables. The sidebar aligns its local CSS mask and SVG detail with the visible selected row when the caller or the desktop layout changes.

A `LuminousChatAttachment` has `id: string`, `name: string`, and optional `imagePreviewUrl?: string`. Use unique, stable attachment IDs. The composer is an independent form. It owns the editor, file picker, attachment display and controls, keyboard handling, and focus behavior. The default placeholder is `پیام خود را بنویسید…`. The `disabled` and `processing` props default to `false`. The caller owns draft text, attachment data, preview URL lifetime, processing state, and the effects of send and stop. The Assistant feature owns the surrounding conversation layout and connects the callbacks to transport as needed. The form takes its width from the caller's layout.

A readonly `PrimaryNavigationItem` has `id: string`, `label: string`, `icon: ReactNode`, and optional `disabled?: boolean`. Use unique, stable IDs and decorative icons. The label gives the button its accessible name. The default landmark name is `ناوبری اصلی`. The application shell supplies the permitted items and controls selection with `activeItemId`. A null ID or an ID absent from the list leaves all items unselected. The component displays the list and sends enabled button activations to `onNavigate`. The caller owns navigation effects and integration with the router and authorized application state.

The composer and menu use Persian RTL, Dastkhat, root `data-theme`, and semantic CSS variables from `DidrahThemeProvider`. Each component keeps its visual rules in its local stylesheet. Both components can render under the application providers independently of the Lab.

The development-only Lab route `/design-system` renders the shared patterns. The Lab owns the fixtures and controls for `WelcomeProfileSpecimen.tsx`, `NavigationHistorySpecimen.tsx`, and the two baseline specimens. [Composer specimen](../../../src/WebApp/src/app/design-system-lab/LuminousChatComposerSpecimen.tsx) · [Primary navigation specimen](../../../src/WebApp/src/app/design-system-lab/PrimaryNavigationSpecimen.tsx)

## Information presentation principles

The Web Application uses three product principles:

1. Information visualization converts authorized business data into understandable visual patterns.
2. Visual storytelling presents validated facts, their importance, and their evidence in a clear order.
3. Actionable presentation connects validated insights, signals, decisions, and follow-up state to authorized manager actions.

These principles apply to Classic and Modern modes. They do not permit the browser to detect signals, infer causes, create business conclusions, or change evidence. Detailed UX rules belong to `18-ux-and-design-system.md`.

## Allowed responsibilities

- Display authorized reports, metrics, workflow state, decision state, and explicit response states.
- Map authorized `ChartSpec` values to ECharts options and render them.
- Present Backend-supplied workflow state with React Flow when useful.
- Collect scoped questions, uploads, and manager commands.
- Send requests to the Backend API over HTTPS/JSON.
- Own temporary browser and presentation state.
- Apply the Design System, RTL behavior, desktop layout resizing, accessibility behavior, and reduced-motion behavior.
- Initialize, update, resize, isolate, and dispose visualization resources.

## Forbidden responsibilities

- Run business rules, KPI calculations, workflow reconstruction, signal detection, or agent graphs.
- Calculate, round, regroup, aggregate, interpolate, complete, or correct chart data.
- Replace `null` with zero or change point order, units, targets, or evidence identity.
- Read PostgreSQL, the protected archive, or input contracts directly.
- Treat hidden UI state as an authorization control.
- Accept executable chart options, HTML, callbacks, or formatter code from Backend or model output.
- Infer business causes or conclusions independently.
- Execute an organizational decision or send an unconfirmed action.

## Component map

| DSL identifier | Component | Primary users |
|---|---|---|
| `chatUi` | Conversational Assistant UI | Senior Manager, Unit Manager, Team Supervisor |
| `dashboardUi` | Role-Based Dashboard UI | Senior Manager, Unit Manager, Team Supervisor |
| `workflowUi` | Workflow Control Room UI | Senior Manager |

## Internal relationships

The three components share the same Web Application runtime. They do not call each other and do not share business state.

They can use the shared infrastructure in this document. Shared infrastructure does not become a fourth business feature.

## External relationships

Each component calls the Backend API over HTTPS/JSON. The Web Application can send redacted telemetry to the optional OpenTelemetry Collector. Core UI behavior remains available when telemetry is disabled or unavailable.

## Chart and Presentation response boundary

The Web Application receives the internal Presentation response defined in doc 17. It contains validated content and zero or more authorized `ChartSpec` values. A frontend mapping function converts each supported `ChartSpec` to an ECharts option.

Doc 17 owns the wire contract, version compatibility, allowlist, limits, runtime validation, unsupported-type behavior, safe labels, mapping tests, and chart lifecycle rules. This document does not duplicate those rules.

Chart capability is mandatory for the product. A specific response can contain zero charts when no chart is requested, the result shape is incompatible, or chart construction fails. Validated content remains available.

### Shared sales chart implementation

`SalesTrendChart` displays ordered current and prior sales observations with stable observation IDs. `BranchSalesChart` displays ordered branch sales with stable branch codes and a nullable target value. Each chart can run under the application providers on its own. A view can use `ChartMotionGroup` to share a clock. [SalesTrendChart.tsx](../../../src/WebApp/src/shared/visualization/charts/SalesTrendChart.tsx) · [BranchSalesChart.tsx](../../../src/WebApp/src/shared/visualization/charts/BranchSalesChart.tsx)

`echarts-runtime.ts` registers the shared ECharts renderer and modules. `chart-theme.ts` adapts the Design System for charts. `SalesChartPresentation.tsx` supplies common sales chart types, panel and state presentation, and text-safe tooltip helpers. `SalesChartMotion.tsx` uses the shared clock in `chart-motion.ts` for finite, event-driven motion and exact final paints.

`ChartHost` waits for the chart fonts and a container with nonzero dimensions. It initializes, updates, and resizes the Canvas renderer. When the host unmounts or the theme changes, it disconnects the resize observer, removes renderer listeners, cancels pending chart motion, and disposes the instance. On an initialization, update, or deferred frame failure, it isolates the affected chart and shows its unavailable state. The table remains available and peer charts can finish. A later valid update or replay can recover the failed chart. [ChartHost.tsx](../../../src/WebApp/src/shared/visualization/charts/ChartHost.tsx)

The current typed component inputs serve local presentation. Production integration still needs generated OpenAPI types, runtime response validation before caching or rendering, and a mapper from authorized `ChartSpec` to the component inputs. Doc 17 governs values, `null`, order, units, targets, evidence identity, numeric display, supported types, and limits.

## Session and browser-state responsibilities

Shared session infrastructure can manage current authenticated-user information, login and logout presentation state, session expiration, Backend-supplied scope context, and invalidation triggers.

It cannot decide authentication, authorization, role grants, row scope, column scope, resource permission, or purpose permission.

Features own temporary local presentation state. They do not share business state. Scope-sensitive cache and request rules are defined in doc 04.

## Component sections

<a id="conversational-assistant-ui"></a>

### Conversational Assistant UI

- **DSL identifier:** `chatUi`
- **Display name:** Conversational Assistant UI
- **Purpose:** Display reports and bounded answers and collect scoped manager input.
- **Responsibilities:** Show briefs and bounded answers, render authorized `ChartSpec` values beside their related message or report item, submit questions, upload documents, submit `CloseSignal`, `ReferSignal`, `SetManagerPriority`, `ChangeKpiTarget`, and `ChangeKpiThreshold` operations, and show job or review state.
- **Inputs:** User actions and authorized Backend API Presentation responses.
- **Outputs:** Authenticated HTTPS/JSON requests and rendered results.
- **Owned state:** Temporary browser view state only.
- **Dependencies:** Backend API, server-validated session context, and approved shared frontend modules.
- **Security boundary:** Treat all browser input as untrusted and do not store secrets in client state.
- **Forbidden responsibilities:** KPI or chart-data calculation, evidence access, authorization, agent execution, and publication.
- **Failure behavior:** Show an explicit error or persisted job state. Do not invent an answer.
- **Idempotency:** Use server-issued identifiers and idempotency data for repeated commands.
- **Observability:** Emit redacted UI request and error telemetry when collection is active.
- **Related ADRs:** ADR-0005, ADR-0008, ADR-0010, ADR-0019, ADR-0020, ADR-0029.
- **Open issues:** Authentication product and method remain open.

<a id="role-based-dashboard-ui"></a>

### Role-Based Dashboard UI

- **DSL identifier:** `dashboardUi`
- **Display name:** Role-Based Dashboard UI
- **Purpose:** Display authorized KPIs, targets, trends, drill-downs, decisions, and open actions.
- **Responsibilities:** Request and render role-scoped management data, deterministic `ChartSpec` values, and direct-workload detail when allowed.
- **Inputs:** Server-validated session context and authorized report or dashboard responses.
- **Outputs:** HTTPS/JSON read requests and rendered management views.
- **Owned state:** Temporary filters and presentation state only.
- **Dependencies:** Backend Report and Dashboard API and approved shared frontend modules.
- **Security boundary:** The Backend API enforces row, column, role, purpose, and policy scope.
- **Forbidden responsibilities:** Direct database access, access-policy decisions, KPI or chart-data calculation, and data correction.
- **Failure behavior:** Show an explicit unavailable or forbidden state. Do not reuse data from another scope.
- **Idempotency:** Read operations are safe to repeat.
- **Observability:** Emit redacted page, request, latency, and error telemetry when collection is active.
- **Related ADRs:** ADR-0002, ADR-0005, ADR-0009, ADR-0020, ADR-0028, ADR-0029.
- **Open issues:** No component-specific open issue.

<a id="workflow-control-room-ui"></a>

### Workflow Control Room UI

- **DSL identifier:** `workflowUi`
- **Display name:** Workflow Control Room UI
- **Purpose:** Display WF1-WF3, stage SLA, bottlenecks, escalations, and pending decisions.
- **Responsibilities:** Present Backend-supplied executive workflow state, use React Flow or custom 2D presentation when suitable, and request authorized workflow drill-downs.
- **Inputs:** Senior Manager actions and authorized workflow responses.
- **Outputs:** HTTPS/JSON read requests and rendered workflow views.
- **Owned state:** Temporary filters and presentation state only.
- **Dependencies:** Backend Report and Dashboard API and approved shared frontend modules.
- **Security boundary:** Access is for the Senior Manager role. The Backend API verifies the role on each request.
- **Forbidden responsibilities:** Workflow reconstruction, SLA calculation, bottleneck detection, escalation calculation, authorization, and direct database access.
- **Failure behavior:** Show an explicit unavailable or forbidden state and clear stale scoped data.
- **Idempotency:** Read operations are safe to repeat.
- **Observability:** Emit redacted workflow-view latency and error telemetry when collection is active.
- **Related ADRs:** ADR-0005, ADR-0006, ADR-0007, ADR-0020, ADR-0029.
- **Open issues:** No component-specific open issue.

## Implementation sequencing

Initial frontend setup can start before production contracts and authentication decisions are complete. The following work can use clearly separated mock data:

- Vite and React application setup.
- Design System foundations.
- Ant Design theme integration.
- Persian and RTL behavior.
- Desktop layouts, navigation prototypes, and shells that adapt when the desktop viewport changes.
- Accessible component states.
- Motion patterns and reduced-motion behavior.
- Feature page composition and UX testing.
- Renderer prototypes that use non-production mock contracts.

Mock work must not become an alternative production contract or an authorization bypass. Production API integration, generated API types, runtime response validation, authenticated session handling, scope-aware caching, and security-sensitive commands remain blocked until their owning contracts or decisions are approved.

## Container-level open issues

- Authentication product, protocol, and credential-storage method remain open.
- Access Projection Matrix entries remain open.
- The exact OpenAPI Presentation wire schema remains open.
- Initial chart allowlist, point and series limits, and numeric display contract remain open.
- Product-wide frontend performance budgets and full-dashboard validation remain open. The approved chart redraw budget applies to the two luminous Classic Mode sales charts described above.
- Modern renderer, hardware profile, asset format, and activation policy remain deferred.
- The Web-to-Collector transport is OTLP/HTTP when optional telemetry export is active.
