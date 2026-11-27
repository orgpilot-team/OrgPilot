# 18. UX and Design System specification

## Scope and authority

The OrgPilot Design System defines the visual language and interaction rules for the three DIDRAH management interfaces. These rules apply to Classic Mode and future Modern Mode. Use Doc 09 for application and component ownership, Doc 17 for data and chart contracts, and the frontend roadmap for stage status and approval evidence. [Web Application architecture](09-web-application-components.md) · [Chart presentation contract](17-chart-presentation-contract.md) · [Frontend roadmap](../../FRONTEND_DEVELOPMENT_STAGES.md)

The user approved the existing Design System foundation and the shared patterns below. The user gave provisional visual approval to the current implementation of phases 2.4 through 2.8. Final Design System validation is pending. [Checkpoint and approval record](../../FRONTEND_DEVELOPMENT_STAGES.md#design-system-checkpoints)

## Visual direction

Use the Deep Dark visual identity with near-black and navy surfaces, electric blue and cyan accents, rounded geometry, and controlled gradients and glow. Use clear hierarchy and limited visual effects. Keep Light Mode functional with a blue-gray canvas, clear surface edges, restrained shadows, and readable contrast. Use references for visual treatment. Product requirements govern navigation, information structure, and workflows.

### Soft Glass controls

The approved Soft Glass treatment covers Button, Input, `Input.TextArea`, InputNumber, Select, and the Select dropdown in both themes. Use restrained tint, borders, and inset highlights to define control surfaces. Distinguish primary, secondary, text, and destructive actions. Preserve visible focus, validation edges and associated messages, clear disabled and loading states, and forced-color support. Use left-to-right editing and right alignment for tracking codes and numbers. Keep effects lightweight with CSS paint and short transitions. Avoid unnecessary blur and `backdrop-filter`. [Ant Design adapter](../../../src/WebApp/src/shared/design-system/theme/ant-theme.ts) · [Soft Glass stylesheet](../../../src/WebApp/src/shared/design-system/theme/ant-controls.css) · [Approval record](../../FRONTEND_DEVELOPMENT_STAGES.md#design-system-checkpoints)

Use the shared control edge and focus treatment for selection controls. Show selection with an explicit mark, thumb position, or inset edge. Use a solid base, subtle tint, and short shadow for overlays. Align numeric table values and preserve the precision supplied for display. Show feedback status in words. Show the KPI value and its unit. Identify the period when a comparison is shown. Connect insight content to an authorized action when available. [Selection and overlay styles](../../../src/WebApp/src/shared/design-system/theme/ant-selection-overlays.css) · [Data and feedback styles](../../../src/WebApp/src/shared/design-system/theme/ant-data-feedback.css)

## Design Tokens and themes

Keep primitive values and a typed set of semantic roles for Dark and Light Mode. Use semantic roles for canvas, surfaces, borders, focus, brand, text, and status. Keep shared typography, spacing, radii, control height, and overlay elevation in the shared tokens. Add global tokens for Design System-wide rules. Keep component-specific colors, gradients, shadows, and geometry with the component. Use the source files for exact values. [Token modules](../../../src/WebApp/src/shared/design-system/tokens/)

The shared provider applies the theme to the document root. The CSS and Ant Design adapters translate the same tokens to their consumers. Renderer adapters translate semantic roles to their own configuration. Keep renderer-specific configuration outside API contracts. Ant Design supplies component behavior and structure. The Design System supplies visual styling. [Theme provider](../../../src/WebApp/src/shared/design-system/theme/DidrahThemeProvider.tsx) · [CSS adapter](../../../src/WebApp/src/shared/design-system/theme/css-variables.ts) · [Ant Design adapter](../../../src/WebApp/src/shared/design-system/theme/ant-theme.ts) · [Chart theme adapter](../../../src/WebApp/src/shared/visualization/charts/chart-theme.ts)

### Browser theme preference

Dark Mode is the default. Store only the selected Dark or Light theme in `localStorage` for this preference. If no valid preference can be read, start in Dark Mode. Theme switching must continue to work when browser storage is unavailable. This approval applies to the theme preference. Follow Doc 04 for credentials and restricted data. [Theme provider](../../../src/WebApp/src/shared/design-system/theme/DidrahThemeProvider.tsx) · [Security and trust](04-security-and-trust.md)

## Persian RTL and typography

Use Persian and RTL at the application root and in Ant Design. Use the approved Dastkhat Variable v1.220 typeface through named roles for headings, body text, controls, tables, captions, KPIs, and technical text. Use regular body text, medium action and label text, and semibold primary headings and KPI values. Use the local font and the approved fallback stack. Required fonts and icons must be available at build time. [HTML entry](../../../src/WebApp/index.html) · [Application providers](../../../src/WebApp/src/app/AppProviders.tsx) · [Typography roles](../../../src/WebApp/src/shared/design-system/tokens/typography.ts) · [Font loading](../../../src/WebApp/src/shared/design-system/styles/fonts.css) · [Font notice](../../../src/WebApp/public/licenses/dastkhat/NOTICE.txt)

Use bidirectional isolation for mixed Persian and Latin content, formatted numbers, and codes as needed. Technical identifiers, query IDs, code, and URLs can remain left-to-right within isolated regions. Preserve authorized numeric values and use the formatting rules in Doc 17. Extend the typography roles or scale only when a product requirement calls for the change. [Chart presentation contract](17-chart-presentation-contract.md) · [Frontend instructions](../../../src/WebApp/AGENTS.md)

## Component consistency

Use the shared theme, surface, focus, and state patterns in both modes. Use text or another non-color cue to distinguish loading, empty, success, warning, error, forbidden, and unavailable states as applicable. Shared components must work outside the Lab with caller-supplied inputs. Keep product behavior in the owning feature. [Component ownership](09-web-application-components.md#application-shell-and-shared-ownership) · [Panel and section header](../../../src/WebApp/src/shared/design-system/patterns/Panel.tsx) · [PanelState](../../../src/WebApp/src/shared/design-system/patterns/PanelState.tsx)

Render Ant Design overlays under the application providers. Use `App.useApp()` for programmatic dialogs, messages, and notifications so they use the active theme and Persian locale. [Application providers](../../../src/WebApp/src/app/AppProviders.tsx)

### Approved shared UI patterns

| Pattern | Durable design and interaction rules |
|---|---|
| Welcome profile | Show the manager's name, avatar or fallback, and Persian calendar date in the Tehran time zone. Make both theme controls operable with the keyboard and expose the selected theme. [WelcomeProfileCard](../../../src/WebApp/src/shared/design-system/patterns/WelcomeProfileCard.tsx) |
| Conversation history | Keep conversation history distinct from primary application navigation. Show labeled groups, local title search, and explicit empty and no-result states. Return focus when search closes. Keep the selected-row detail aligned during scrolling and resize. [NavigationHistorySidebar](../../../src/WebApp/src/shared/design-system/patterns/NavigationHistorySidebar.tsx) |
| Chat composer | Use an independent Persian RTL form. Support draft editing, attachments, Send, and Stop. Plain Enter sends when allowed, Shift+Enter adds a line break, and input method composition must not send. Announce processing and preserve focus after actions. Use a defined edge and reduced glow in Light Mode. [LuminousChatComposer](../../../src/WebApp/src/shared/design-system/patterns/LuminousChatComposer.tsx) |
| Primary navigation | Use a named Persian RTL navigation landmark with keyboard-operable actions and a clear current item. Preserve the approved blue-to-violet selected treatment in Dark Mode. Use the semantic selected surface in Light Mode and keep the current state visible in forced colors. [PrimaryNavigationMenu](../../../src/WebApp/src/shared/design-system/patterns/PrimaryNavigationMenu.tsx) |

## Information and visualization design

- **Information Visualization.** Use clear visual patterns to show what happened in the authorized data.
- **Visual Storytelling.** Use sequence and emphasis to show why validated facts matter and what evidence supports them.
- **Actionable Dashboard.** Connect validated insights to the authorized actions and follow-up available to the user.

- **ECharts.** Apply the chart theme and safe text formatting. Give each chart an accessible name and a text or tabular alternative when needed. If a renderer fails, isolate the affected chart and show its unavailable state. Keep validated content, accessible data tables, and unaffected peer charts available. [Chart presentation contract](17-chart-presentation-contract.md) · [Shared chart presentation](../../../src/WebApp/src/shared/visualization/charts/SalesChartPresentation.tsx)
- **Sales charts.** The approved Dark Mode luminous variants use edge lighting and local styling for trend strokes or horizontal bars. Keep Light Mode and the default variants static. Use the shared source for exact geometry and visual values. [Trend recipe](../../../src/WebApp/src/shared/visualization/charts/luminous-sales-trend.ts) · [Branch recipe](../../../src/WebApp/src/shared/visualization/charts/luminous-branch-sales.ts)
- **Workflow and 2D infographics.** Preserve Backend-supplied workflow meaning and evidence. Provide an accessible alternative. Keep CSS and SVG labels safe for untrusted data. The Lab uses React Flow as a specimen. The production renderer remains open. [Workflow architecture](09-web-application-components.md#workflow-control-room-ui)
- **Future 3D scenes.** Use the shared visual language and a complete Classic fallback. Keep required content and actions available. [Modern Mode](09-web-application-components.md#modern-mode)

## Rendering and motion

Use motion to communicate state, relationships, focus, or hierarchy. Keep motion finite and purposeful. Stop nonessential animation when content is hidden. Preserve focus and provide reduced-motion alternatives. Use cues other than motion for status and changes. Dispose of renderer resources when they are no longer required. [Quality attributes](07-quality-attributes.md) · [Component workflow](../../../.agents/skills/didrah-component-workflow/SKILL.md)

### Luminous chart motion

The approved default budget is **30 scheduled redraws per second per chart during motion** for the luminous variants of the existing Sales Trend and Branch Sales charts in Classic Mode. Both charts stop continuous redraws at idle. The Lab supplies a Native comparison. This budget applies only to these two luminous charts. Product-wide numeric performance budgets remain open. [Chart motion clock](../../../src/WebApp/src/shared/visualization/charts/chart-motion.ts) · [Risks and open issues](08-risks-and-open-issues.md#open-decisions)

Animate renderer geometry for compatible updates only. Apply structural changes directly. Keep tooltips and tables on accepted values throughout motion. Paint the exact final state. Apply accepted values directly for reduced motion or disabled animation. Settle to the accepted values if the page becomes hidden. Use the chart motion source for exact timings and conditions. [Sales chart motion](../../../src/WebApp/src/shared/visualization/charts/SalesChartMotion.tsx) · [Chart presentation contract](17-chart-presentation-contract.md)

## Accessibility and desktop scope

Support keyboard navigation and operation, visible focus, meaningful accessible names and descriptions, sufficient contrast, non-color status cues, scalable text, accessible validation messages, and alternatives for charts and workflow graphics. Formal WCAG conformance remains deferred. [Quality gates](07-quality-attributes.md) · [Risks and open issues](08-risks-and-open-issues.md#open-decisions)

The Web Application is desktop-only. Layouts must adapt when the user resizes a supported desktop viewport. Keep authorized information, actions, keyboard access, and focus available. Mobile and tablet layouts and validation are out of scope. The product-wide desktop viewport matrix remains open. [Risks and open issues](08-risks-and-open-issues.md#open-decisions)

## Design System Lab

The development-only Lab at `/design-system` renders the actual shared components in both themes. It owns specimens, mock data, review scenarios, and benchmark controls. Its section index supports review. Chart and Workflow examples load on demand. Keep product data and reusable component behavior in their owning modules. Use the component workflow and its checklist for design and validation. [Lab source](../../../src/WebApp/src/app/design-system-lab/DesignSystemLab.tsx) · [Component workflow](../../../.agents/skills/didrah-component-workflow/SKILL.md) · [Acceptance checklist](../../../.agents/skills/didrah-component-workflow/references/component-checklist.md)

## Future design decisions

Further Light Mode refinements and detailed designs for new component families need approval. Extensions to global tokens and general motion presets remain open. Modern scene styling and asset guidance remain deferred. [Risks and open issues](08-risks-and-open-issues.md#open-decisions) · [Frontend roadmap](../../FRONTEND_DEVELOPMENT_STAGES.md)
