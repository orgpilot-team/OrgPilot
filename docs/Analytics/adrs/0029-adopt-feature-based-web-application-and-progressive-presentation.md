# 29. Adopt a feature-based Web Application with progressive presentation modes

Date: 2026-11-25

## Status

Accepted

## Context

DIDRAH needs three Persian RTL management interfaces in one Web Application: Conversational Assistant UI, Role-Based Dashboard UI, and Workflow Control Room UI. These interfaces use the same authorized Backend API, product capabilities, Design System, and internal Presentation contract.

The accepted frontend stack already includes React 19, TypeScript, Vite, and Apache ECharts. The team also needs a UI component foundation, purposeful animation, interactive workflow presentation, custom 2D presentation, and a controlled path for possible future 3D enhancement.

Without one frontend architecture, the implementation can duplicate API contracts, feature state, business rules, styling systems, or presentation modes. A separate Modern application would also add a deployment boundary without a separate business capability.

## Decision

DIDRAH uses one feature-based Web Application.

- The three existing C4 components remain the three primary frontend features.
- Features do not call or import another feature's internal implementation.
- Features own temporary presentation state only and do not share business state.
- Shared frontend modules can provide the Design System, generic UI, generated API contracts, transport, session lifecycle, scope-aware cache infrastructure, visualization adapters, Motion presets, telemetry, and focused technical utilities.
- Tactical DDD does not apply to the Web Application. Frontend aggregates, repositories, domain events, and business-rule engines are not used.

Ant Design is the UI component foundation. The DIDRAH Design System controls its visual identity and supplies shared semantic tokens to Ant Design, ECharts, React Flow, Motion, CSS, SVG, and future approved 3D scenes.

Motion supplies purposeful transitions and micro-interactions. React Flow can present Backend-supplied workflow state where it is suitable. It does not reconstruct workflows or calculate SLA, bottlenecks, or escalations.

Classic Mode is the default, mandatory, and complete product experience. It uses interactive 2D presentation and has no Three.js or 3D model dependency.

Modern Mode is a deferred future enhancement inside the same Web Application. It can add selected lazy-loaded 3D scenes after Classic Mode is functionally complete. It uses the same features, contracts, Design System, authorized state, and business capabilities. It must fall back to the complete Classic experience. It is not a C4 component, separate deployment, authorization boundary, or separate product.

Three.js, WebGPU or WebGL 2 renderer selection, 3D asset formats, hardware profiles, and Modern activation policy remain deferred. These dependencies and directories are not added until Modern development starts.

Frontend wire types are generated from the versioned Backend OpenAPI contract. Renderer-neutral contract types do not depend on ECharts, React Flow, Motion, Ant Design, or a future 3D renderer. Runtime response validation is required at the browser network boundary.

Initial frontend setup, Design System work, Persian RTL behavior, layout, accessible component states, and UX work can use clearly separated mock data before production contracts and security decisions are complete. Mock data does not become a production contract or authorization bypass. Production API integration and security-sensitive functionality wait for their owning contracts and decisions.

## Alternatives considered

### Separate Classic and Modern applications

Rejected. This would duplicate deployment, API integration, feature state, tests, and product behavior.

### Modern Mode as a C4 component

Rejected. It is a presentation capability and does not own a business capability, state boundary, or deployment unit.

### Backend-generated ECharts options

Rejected by ADR-0028. It would couple the Backend contract to one rendering library and could introduce executable presentation configuration.

### Hand-maintained TypeScript API contracts

Rejected. Independent C# and TypeScript contract definitions can drift.

### Multiple general UI or styling frameworks

Rejected. Overlapping frameworks add bundle size and inconsistent behavior without a new product requirement.

### Tactical DDD in the frontend

Rejected. Business invariants remain in the accepted Backend, Worker, and Agent Runtime boundaries.

### Add Three.js during first-release setup

Rejected. Classic Mode supplies complete required functionality and must not depend on deferred 3D work.

## Consequences

- The three accepted Web Application components remain stable.
- Frontend implementation has explicit feature and shared-module boundaries.
- The product has one visual system across its renderers.
- Classic Mode has no 3D bundle, asset, hardware, or compatibility dependency.
- Modern work can start later without duplicating business state or API contracts.
- Contract generation and runtime validation need build and test support.
- Design System and visualization mapping need focused accessibility, RTL, lifecycle, and failure-isolation tests.
- A visualization failure does not remove validated report or answer content.

## Security impact

The browser remains untrusted. Session helpers and caches do not become authorization authorities. Scope-sensitive data is isolated and invalidated under doc 04. Redacted telemetry remains fail-open under ADR-0020 and ADR-0027.

## Operational impact

There is no new service, store, deployment node, or network relationship. Classic assets are built with the Web Application. Future Modern renderer code and assets must be lazy-loaded from the same approved Web deployment and must not use a required runtime CDN.

## Related requirements

- The project brief requires three Persian RTL interfaces.
- ADR-0018 selects React, TypeScript, and Vite.
- ADR-0020 selects OpenTelemetry instrumentation and fail-open export.
- ADR-0028 selects ECharts and the internal chart presentation contract.
- `docs/04-security-and-trust.md` owns frontend security and scope isolation.
- `docs/07-quality-attributes.md` owns frontend quality gates.
- `docs/09-web-application-components.md` owns frontend architecture.
- `docs/17-chart-presentation-contract.md` owns chart and wire-contract rules.
- `docs/18-ux-and-design-system.md` owns visual and interaction guidance.

## Related model elements

- Web Application
- Conversational Assistant UI
- Role-Based Dashboard UI
- Workflow Control Room UI

## Open decisions

- Authentication product, protocol, and credential-storage method.
- Access Projection Matrix entries.
- Exact OpenAPI Presentation wire schema.
- Initial chart allowlist, limits, and numeric display contract.
- Numeric frontend performance budgets and measurement profile.
- Approved Design System tokens and detailed component specifications.
- Modern renderer, hardware profile, asset format, and activation policy.
