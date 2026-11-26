# 18. UX and Design System specification

## Purpose and authority

This document defines the OrgPilot visual language and shared UX guidance. It applies to all three Web Application features and to Classic and future Modern presentation modes.

This document does not define business workflows, authorization, API contracts, chart values, signal rules, or C4 boundaries. Those concerns remain in their owning architecture and contract documents.

Status: **Accepted direction; detailed tokens and component specifications remain open**.

## Visual direction

OrgPilot uses a Deep Dark visual direction:

- Near-black backgrounds with subtle navy tones.
- Dark elevated surfaces.
- Electric blue and cyan accents.
- Controlled gradients and glow effects.
- Modern Persian typography.
- Rounded surfaces.
- Minimal visual clutter.
- Smooth and purposeful interactions.
- Custom chart and infographic styling.
- Persian and RTL-first composition.

These statements describe visual direction. They do not approve exact colors, typefaces, spacing, shadows, radii, or motion values. The external visual reference defines a visual language only. It does not define OrgPilot navigation, information architecture, manager workflows, or product behavior.

## Design System ownership

The OrgPilot Design System is the presentation authority for:

- Semantic color, typography, spacing, elevation, radius, border, and motion tokens.
- Ant Design theme values and component variants.
- ECharts visual mapping.
- React Flow nodes, edges, controls, and states.
- Motion presets and reduced-motion alternatives.
- Custom CSS and SVG presentation.
- Future Three.js scene styling after Modern work is approved.

Tokens must use semantic names. A renderer can translate semantic tokens into its own configuration. Renderer-specific configuration must not leak into renderer-neutral API contracts.

Ant Design supplies component behavior and structure. Its default appearance must not determine OrgPilot visual identity. Avoid a parallel general-purpose component library.

## Information experience

The product must not become a collection of disconnected KPI cards and charts.

Each primary management view must help the user understand:

1. What happened.
2. Why it matters, using only validated content.
3. What evidence supports the statement.
4. What authorized action or follow-up is available.

Information visualization converts authorized data into clear visual patterns. Visual storytelling controls sequence and emphasis. Actionable presentation connects validated insight to a permitted manager action.

The UI must not create a cause, signal, recommendation, target, or conclusion that is absent from the validated Backend response.

## Persian and RTL rules

- Persian is the primary interface language.
- The application root uses Persian language and RTL direction.
- Mixed Persian and Latin content must use explicit bidirectional isolation where required.
- Technical identifiers, query identifiers, code, and URLs can remain left-to-right inside isolated regions.
- Typography must remain readable at supported sizes and weights.
- Numeric presentation must preserve the authorized value and follow the approved contract. The UI must not round a KPI independently.
- Fonts and icons required for core operation must be available at build time. Core presentation must not depend on a runtime CDN.

## Interaction and Motion rules

Motion must communicate state, relationship, focus, or hierarchy. Decorative motion must remain limited.

- Provide a reduced-motion alternative.
- Do not use motion as the only indication of status or change.
- Stop nonessential animation when its content is not visible.
- Avoid continuous animation in Classic Mode.
- Keep loading, success, warning, failure, forbidden, empty, and unavailable states visually distinct.
- Preserve keyboard focus during transitions.

The 30 FPS goal belongs only to deferred active 3D rendering. It does not define the speed of UI transitions.

## Visualization guidance

### ECharts

ECharts styling must use Design System tokens and the deterministic mapper defined in doc 17. Tooltips and labels must use safe text. A chart must have an accessible name and a text or tabular alternative when the information cannot be understood without the visual.

### React Flow

React Flow is for interactive presentation of Backend-supplied workflow state. Nodes and edges must preserve the Backend meaning. Layout and interaction can change, but workflow ownership, SLA, bottleneck, escalation, and evidence cannot change.

### CSS and SVG

Custom CSS and SVG are suitable for focused 2D infographics and product-specific controls. SVG text and labels are untrusted data and must not introduce executable content.

### Future Three.js

Future scenes must use the same semantic Design System. A scene must have a complete Classic fallback. A 3D scene must not hide required content or manager actions.

## Accessibility

The proposed conformance target is WCAG 2.2 AA. Final acceptance of this target remains a product decision.

The Design System must support:

- Keyboard operation.
- Visible focus.
- Screen-reader names and descriptions.
- Sufficient text and control contrast.
- Reduced motion.
- Non-color status cues.
- Scalable text.
- Accessible error and validation messages.
- Accessible alternatives for charts and workflow graphics.

Detailed quality gates and test requirements belong to doc 07.

## Responsive behavior

The exact supported viewport matrix remains open. Layouts must adapt without removing authorized information or actions. Responsive behavior must not change business meaning, scope, evidence identity, or contract values.

## Open design decisions

- Approved semantic color tokens.
- Approved Persian typeface and fallback stack.
- Spacing, elevation, radius, shadow, and glow scales.
- Motion durations and easing values.
- Supported viewport matrix.
- Detailed component variants and state specifications.
- Exact accessibility conformance target approval.
- Future 3D scene style and asset guidance.
