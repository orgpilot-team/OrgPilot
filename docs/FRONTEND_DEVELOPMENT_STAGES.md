# Frontend development stages

This roadmap records implementation progress, approval, and the next frontend gates. Use the Web Application architecture, chart contract, Design System policies, and decision register for accepted rules and unresolved decisions. Backend delivery has a separate plan. [Doc 09](Analytics/docs/09-web-application-components.md) · [Doc 17](Analytics/docs/17-chart-presentation-contract.md) · [Doc 18](Analytics/docs/18-ux-and-design-system.md) · [Doc 08](Analytics/docs/08-risks-and-open-issues.md#open-decisions) · [Backend development stages](DEVELOPMENT_STAGES.md)

## Current implementation

The Vite entry, application providers, shared Design System, and reusable visualizations are in place. The development-only Design System Lab at `/design-system` uses mock data. The application shows a placeholder outside the Lab. The product Application Shell, Assistant, Dashboard, Workflow Control Room, and authenticated Backend integration are pending. [Frontend setup](../README.md#frontend-development-setup) · [Implementation status](Analytics/docs/09-web-application-components.md#current-implementation)

## Design System checkpoints

| Checkpoint | Commit | Status and evidence |
|---|---|---|
| Frontend foundation | `21e80382` | React and Vite scaffold and accepted frontend architecture. |
| Design System baseline | `0bcb1adb`, integrated in `e469db15` | The user approved the migrated Lab after manual visual and behavior review. The approved baseline includes shared tokens, both themes, Dastkhat, and the two luminous Classic sales chart variants. `e469db15` also includes the welcome profile and conversation history patterns. |
| Phase 2.2, reference components and primary navigation | `445a16b1` | The user approved the independent chat composer and its input controls, and the primary navigation appearance with its blue-to-violet selected row, after the Phase 2.1 audit. |
| Phase 2.3, Soft Glass controls | `6d47722b` | The user approved the covered buttons, fields, and Select dropdown in both themes on 2026-11-27. |
| Phase 2.4, selection and overlays | `9aefaea2` | Implementation complete. Provisional visual approval. |
| Phase 2.5, data display and feedback | `c790f4e1` | Implementation complete. Provisional visual approval. |
| Phase 2.6, typography | `b451f4ab` | Implementation complete. Provisional visual approval. |
| Phase 2.7, Light Mode | `fe2d5810` | Implementation complete. Provisional visual approval. |
| Phase 2.8, Lab navigation | `a9da2d74` | Implementation complete. Provisional visual approval. |
| Phase 2.4 through 2.8 consolidation | `d417b43d` | Type checking, production build, and Git diff whitespace checks were recorded as passing. Targeted desktop browser checks covered keyboard navigation, overlay focus return, table states, KPI precision, on-demand loading, saved theme selection, and a 1024 px viewport. |

The user explicitly approved local browser storage for the selected Dark or Light theme. The provisional visual approvals apply to the current Phase 2.4 through 2.8 implementation. Final Design System validation is pending. [Browser theme policy](Analytics/docs/18-ux-and-design-system.md#browser-theme-preference)

The earlier migration record covers both themes, a full Lab review at 1366 × 768 at 100% zoom, and five additional layout smoke checks. It records 28.85 trend and 28.58 branch redraws per second during entrance replay at the primary viewport, and no continuous redraws at idle. It also records the user's acceptance of small pixel differences in an earlier comparison at 1440 × 960. These historical results apply to that Lab checkpoint and its sample data. For the original scope and measurements, see Doc 18 in `d417b43d`, lines 243–260.

## Known issues and pending decisions

- **Workflow resizing.** The Lab specimen has a known resize issue. Evaluate it during Workflow technology review. The specimen uses React Flow. Production renderer selection is open.
- **Chart and dashboard performance.** The historical R5.4 Lab benchmark recorded approximately 500 application callbacks per second during motion and zero at idle. The callback count measures scheduling work separately from chart redraws. The page-wide listener count grew from 1,396 to 4,302 over ten mount and disposal cycles. The benchmark recorded release of all 70 tracked chart and Canvas references. Listener ownership and the cause of variable CPU and GPU readings remain open. Recheck applicable items with the full dashboard and representative data when the measurement profile is approved. The original observations are in Doc 18 in `d417b43d`, lines 283–291.
- **Production contracts.** Authentication, credential storage, the Access Projection Matrix, the Presentation OpenAPI schema and compatibility policy, validation failure isolation, and the initial chart policy remain open. Production chart mapping and API validation are pending. [Decision register](Analytics/docs/08-risks-and-open-issues.md#open-decisions) · [Chart contract](Analytics/docs/17-chart-presentation-contract.md)
- **DatePicker calendar contract.** Open. Confirm the product calendar, date input and display rules, and how selected dates map to the applicable Backend contract. The Lab specimen uses Ant Design DatePicker with Persian locale labels. [DatePicker specimen](../src/WebApp/src/app/design-system-lab/AntSpecimens.tsx)
- **Product design and quality.** Detailed designs for new component families, general motion presets, the desktop viewport matrix, and product-wide performance budgets remain open. Modern Mode and formal WCAG conformance are deferred. The earlier 30 FPS target for active 3D rendering is a proposal. Practical accessibility is required. [Design policies](Analytics/docs/18-ux-and-design-system.md) · [Quality attributes](Analytics/docs/07-quality-attributes.md)

## Delivery sequence and exit gates

The order below is established. The product breakdown under Stage 4 and the detailed scope of later stages are proposed. Start the next stage only after the applicable approval.

| Stage | Scope | Exit gate |
|---|---|---|
| 1. Frontend documentation consolidation | Align the README, Docs 08, 09, and 18, and this roadmap. | Check links, anchors, consistency, and whitespace. Give the user the complete unstaged patch for manual review and approval. |
| 2. Workflow technology evaluation and redesign | Evaluate React Flow and a custom 2D option against the accepted Workflow scope, desktop resize, keyboard access, accessible alternatives, and rendering cost. Use mock data until the Backend contract is available. | The user approves the technology direction before redesign and reviews the redesigned specimen. Address the known resize issue in the approved design. |
| 3. Final Design System validation | Review the approved components and Workflow specimen in both themes. Check Persian RTL, keyboard access, focus, desktop resizing, component states, and applicable renderer behavior. | Record the targeted technical evidence and obtain final user visual approval. [Acceptance checklist](../.agents/skills/didrah-component-workflow/references/component-checklist.md) |
| 4. Application Shell and product pages | Build the Classic Mode shell and compose the three features with isolated mock data where needed. | Review navigation, feature ownership, and applicable loading, empty, forbidden, error, and unavailable states. |
| 5. Backend integration | Connect the approved session and scoped API paths as Backend capabilities become available. Generate applicable wire types, validate responses, and map authorized charts. | Verify contract compatibility, authorized states and actions, scope invalidation, and safe failure for each integrated path. |
| 6. Integration testing and optimization | Exercise complete Classic flows with representative data. Check scope transitions, chart failure isolation, keyboard access, desktop resizing, and renderer performance. | Pass the applicable quality gates. Record product-wide measurements against the approved profile and budgets when they are available. [Quality gates](Analytics/docs/07-quality-attributes.md) |

### Proposed product breakdown within Stage 4

1. **Application Shell.** Compose providers, primary navigation, shared layout, routes, and temporary presentation state.
2. **Role-Based Dashboard.** Compose brief, KPI, trend, and authorized drill-down views with the shared panels, charts, tables, and feedback states.
3. **Conversational Assistant.** Compose conversation history, brief and answer cards, composer and uploads, job states, and confirmed manager action views.
4. **Workflow Control Room.** Apply the renderer selected in Stage 2. Compose the Senior Manager view for WF1–WF3, SLA, bottlenecks, escalations, pending decisions, and authorized drill-downs.

Extend the approved panels, navigation, form controls, KPI and insight patterns, tables, and feedback only where the product pages need them.

## Backend delivery dependencies

| Frontend capability | Required Backend delivery or decision |
|---|---|
| Role-scoped shell and all production pages | Accepted authentication and credential storage approach, trusted session context, and Access Projection Matrix. [Security and trust](Analytics/docs/04-security-and-trust.md) |
| Dashboard and Workflow | Versioned KPI and snapshot results for the Dashboard. Backend-provided executive workflow state and drill-downs for the Workflow Control Room. Authorized delivery through Report and Dashboard API. The Backend intake and workflow stages supply upstream results. [Backend stages](DEVELOPMENT_STAGES.md) · [Backend API](Analytics/docs/10-backend-api-components.md) |
| Assistant | Authorized report and question delivery, upload and command handlers, and persisted job and review states. Keep Agent Runtime access behind the Backend API. [Runtime flows](Analytics/docs/05-runtime-flows.md) · [Backend API](Analytics/docs/10-backend-api-components.md) |
| Production charts | Approved versioned OpenAPI artifact and compatibility policy, authorized `ChartSpec` delivery, and the allowlist, limits, numeric display, and validation rules in Doc 17. [Presentation contract](Analytics/docs/17-chart-presentation-contract.md) |

Record stage completion with its checkpoint and evidence after its exit gate passes. Keep new decisions in their owning architecture documents and decision register. Documentation changes remain uncommitted until manual user review and approval.
