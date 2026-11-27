# 18. UX and Design System specification

## Purpose and authority

This document defines the OrgPilot visual language and shared UX guidance. It applies to all three Web Application features and to Classic and future Modern presentation modes.

This document does not define business workflows, authorization, API contracts, chart values, signal rules, or C4 boundaries. Those concerns remain in their owning architecture and contract documents.

The approved Stage 4.5-R5.5 baseline includes the implemented Design Tokens, Dark and Light themes, Dastkhat typography, and two Dark Mode luminous sales chart variants. The approved shared UI patterns also include `WelcomeProfileCard` and `NavigationHistorySidebar`.

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

Dark Mode is the default theme. Keep Light Mode functional with the current tokens and component fallbacks. Light Mode visual refinement remains deferred. Use external references for visual treatment. OrgPilot navigation, information architecture, and workflows follow their product requirements.

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

### Global Design Tokens and themes

The shared token modules define primitive colors, one typed set of semantic color roles, and the values for each role in Dark and Light Mode. The roles cover the canvas, surfaces, borders, focus, brand, text, and status. The token modules also define shared typography, spacing, radii, control height, and overlay elevation. [Token modules](../../../src/WebApp/src/shared/design-system/tokens)

`DidrahThemeProvider` makes the active theme available to consumers and sets `data-theme` and `color-scheme` on the document root. The CSS adapter applies semantic variables to the same root. The Ant Design adapter uses the same tokens for its theme and component overrides. The ECharts adapter maps shared roles to baseline chart text, axes, legends, tooltips, and series colors. [Theme provider](../../../src/WebApp/src/shared/design-system/theme/DidrahThemeProvider.tsx) · [CSS adapter](../../../src/WebApp/src/shared/design-system/theme/css-variables.ts) · [Ant Design adapter](../../../src/WebApp/src/shared/design-system/theme/ant-theme.ts) · [ECharts adapter](../../../src/WebApp/src/shared/visualization/charts/chart-theme.ts)

Use global tokens for design decisions that apply across the Design System. Keep colors, gradients, glows, shadows, and geometry specific to a component in its owning module. Keep chart plot geometry in the chart variants. Use the approved source files for exact rendering values.

### Approved shared UI patterns

The shared Design System owns both patterns in `src/WebApp/src/shared/design-system/patterns`. The Lab consumes the patterns at `/design-system` and owns the specimens, fixtures, and controls. The component paths and public interfaces are in [doc 09](09-web-application-components.md#approved-shared-ui-patterns).

#### WelcomeProfileCard

The card uses a rounded `Panel`. The avatar is at the right and the moon and sun theme controls are at the left. The Persian weekday, day, and month appear below the controls and above the two-line greeting. The display date uses the Persian calendar and the Tehran time zone. The avatar uses a square image with rounded corners. The manager's initial appears while the image loads or if it is unavailable. A blank name uses the Persian fallback for manager. The displayed name uses bidirectional isolation.

The card fills its container up to `32rem`. Container units set the scale within these bounds:

| Parameter | Approved bounds |
|---|---|
| Panel padding and corner radius | `1.25rem` to `2rem` |
| Avatar size | `3rem` to `4.5rem` |
| Theme button size | `2.75rem` to `3.5rem` |
| Date font size | `1rem` to `1.5rem`, weight 700 |
| Greeting font size | `1.75rem` to `2.9375rem`, weight 700 |

The controls update `DidrahThemeProvider` and show the selected theme with `aria-pressed`. Dark Mode uses local surface `#11111b`, selected fill `#22222c`, date text `#bdbcca`, muted icon `#8c8da1`, and primary ink `#fff`. Light Mode uses semantic surfaces and text with a subtle inset border. Use the source for the container formulas, icon paths, focus ring, and fallback states. [Component](../../../src/WebApp/src/shared/design-system/patterns/WelcomeProfileCard.tsx) and [visual rules](../../../src/WebApp/src/shared/design-system/patterns/welcome-profile-card.css).

#### NavigationHistorySidebar

The sidebar shows AI conversation history in the Conversational Assistant UI. Primary application navigation belongs to the application shell. The sidebar has a DIDRAH brand header, a gradient New Chat button, a search control, a scrollable list of labeled conversation groups, and a Settings footer. The search field opens in the header, takes focus, and filters titles locally. The close button and Escape return focus to the search button. Long titles use ellipsis and bidirectional isolation. The sidebar has distinct status text for empty history and for a search with no results.

The sidebar is `14.25rem` wide. Its default height is `47rem` and its minimum height is `22rem`. A caller can set `--didrah-history-height` for desktop layout. The inline inset is `1.5rem`. The row and standard control height are `2.25rem`. The selected row button uses `aria-current="true"` and shows a curved cutout at its inline end, a blue edge glow and dot, and a delete control. The cutout mask is `2.25rem` wide by `5.125rem` high, with upper and lower return offsets of `1.375rem` and `1.5rem`. The `144 x 72` SVG detail is `4.5rem` wide in CSS and fills the row height.

The sidebar sets Persian RTL explicitly. Logical CSS places the row detail and delete control at inline end. The mask uses the physical left edge of this RTL layout. The component measures the selected row against the frame and scroll viewport. It updates the mask offset on selection or list changes, filtering, search expansion, scrolling, and resize. The mask appears while any part of the selected row is visible in the list. The row and its inline SVG scroll together. A bottom fade indicates more content and clears when a list control has visible focus.

Dark Mode uses the shared canvas. Its local selected and delete fills are `#22222e` and `#262835`. Its local accent is `#284aff`. The local Dark Mode brand accent is `#4c72f0`. The search border gradient, cutout path, and SVG glow settings are local to the pattern. Light Mode uses semantic surfaces, text, and borders, plus the local brand accent `#3555ba`. Both themes use the shared focus ring. [Component](../../../src/WebApp/src/shared/design-system/patterns/NavigationHistorySidebar.tsx) and [visual rules](../../../src/WebApp/src/shared/design-system/patterns/navigation-history-sidebar.css).

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

The HTML root uses `lang="fa"` and `dir="rtl"`. The Ant Design provider uses the `fa_IR` locale and RTL direction. Dastkhat Variable v1.220 is the approved typeface, with Tahoma, Segoe UI, and sans-serif fallbacks. The application preloads the local WOFF2 file and uses weights 400 to 700 through named roles for headings, body text, controls, tables, captions, KPIs, and technical text. The chart host waits for the chart fonts before drawing. [Typography tokens](../../../src/WebApp/src/shared/design-system/tokens/typography.ts) · [Font notice](../../../src/WebApp/public/licenses/dastkhat/NOTICE.txt)

Keep the approved Dastkhat typography in use. Defer global typography refinement until the initial component families are complete.

## Interaction and Motion rules

Motion must communicate state, relationship, focus, or hierarchy. Decorative motion must remain limited.

- Provide a reduced-motion alternative.
- Do not use motion as the only indication of status or change.
- Stop nonessential animation when its content is not visible.
- Avoid continuous animation in Classic Mode.
- Keep loading, success, warning, failure, forbidden, empty, and unavailable states visually distinct.
- Preserve keyboard focus during transitions.

### Luminous chart motion

The two luminous Classic Mode sales charts use an approved default budget of 30 scheduled redraws per second per chart. This budget controls chart paints during motion. The Lab has a Native comparison. Both charts have zero continuous redraws at idle.

| Event | Approved timing |
|---|---|
| Sales trend entrance | 900 ms, with the reveal in RTL direction |
| Branch sales entrance | 700 ms after a 120 ms delay, with a total stagger of 90 ms across the items when more than one item is present |
| Compatible data change | 450 ms for either chart |

The shared clock uses elapsed time. It can skip an intermediate paint so the exact final paint occurs at completion. The default chart variants and the Light Mode fallback display data without motion. Reduced motion or disabled animation applies the accepted values directly. If the page becomes hidden during motion, the charts settle to the accepted values. See the [sales chart motion implementation](../../../src/WebApp/src/shared/visualization/charts/SalesChartMotion.tsx).

The proposed 30 FPS target for future active 3D scenes remains part of deferred Modern Mode. General UI motion durations and easing remain open.

## Visualization guidance

### ECharts

ECharts styling must use Design System tokens and the deterministic mapper defined in doc 17. Tooltips and labels must use safe text. A chart must have an accessible name and a text or tabular alternative when the information cannot be understood without the visual.

#### Approved sales chart variants

Both sales charts offer `default` and opt-in `luminous` variants. Dark Mode uses the luminous card surface and edge lighting for both charts. The trend adds layered blue and cyan strokes, area fills, and halos through a local ECharts Custom Series. The branch chart uses gradient-filled horizontal bars, a lit plot surface, and a dashed target line when a target is supplied. Light Mode uses the current static chart presentation. [Shared surface](../../../src/WebApp/src/shared/visualization/charts/luminous-chart.css) · [Trend rendering](../../../src/WebApp/src/shared/visualization/charts/luminous-sales-trend.ts) · [Branch rendering](../../../src/WebApp/src/shared/visualization/charts/luminous-branch-sales.ts)

The current components take ordered typed observations, decimal strings, missing values, and presentation metadata. Compatible value changes can animate when ordered identities, missing-value positions, scale, labels, and the branch target stay compatible. Structural changes apply directly. Rapid compatible updates can start from the state currently on screen.

Intermediate values affect renderer geometry only. Tooltips and data tables use the supplied decimal strings, units, target values, and explicit missing states throughout the transition. The final paint uses the accepted values converted to renderer coordinates. The production data and numeric display rules remain in [doc 17](17-chart-presentation-contract.md).

### React Flow

React Flow is for interactive presentation of Backend-supplied workflow state. Nodes and edges must preserve the Backend meaning. Layout and interaction can change, but workflow ownership, SLA, bottleneck, escalation, and evidence cannot change.

### CSS and SVG

Custom CSS and SVG are suitable for focused 2D infographics and product-specific controls. SVG text and labels are untrusted data and must not introduce executable content.

### Future Three.js

Future scenes must use the same semantic Design System. A scene must have a complete Classic fallback. A 3D scene must not hide required content or manager actions.

## Accessibility

Phase 4 deferred adoption of a formal WCAG conformance target for this stage.

The Design System must meet these accessibility requirements.

- Keyboard navigation and operation.
- Visible focus.
- Meaningful labels and screen-reader names and descriptions.
- Sufficient text and control contrast.
- Reduced motion.
- Non-color status cues.
- Scalable text.
- Accessible error and validation messages.
- Accessible alternatives for charts and workflow graphics.

Detailed quality gates and test requirements belong to doc 07.

The shared sales charts have accessible names, keyboard-operable disclosures for their data tables, and explicit text for unavailable and missing data. Tooltips use local text formatting. Bidirectional isolation keeps technical codes and decimal strings readable in Persian context. During a renderer failure, the table remains available.

## Desktop layout and resizing

The DIDRAH Web Application is desktop-only. Mobile and tablet layouts, breakpoints, screenshots, and device-specific validation are out of scope.

Layouts must adapt at supported desktop viewports without removing authorized information or actions. Preserve business meaning, scope, evidence identity, and contract values. Check keyboard access and visible focus during desktop validation. The exact product-wide desktop viewport matrix remains open.

### Desktop and laptop validation

The frontend migration handoff (`frontend-migration-handoff.md`) records the following checks in both themes for integration commit `0bcb1adb17af52c77fc9a88d4deac4765fb749d2`. These results record the earlier desktop and laptop Lab validation.

| Browser size | Zoom | CSS viewport | Result in both themes |
|---|---:|---|---|
| 1366 × 768 | 100% | 1366 × 768 | Full validation and pixel-identical migration comparison |
| 1024 × 768 | 100% | 1024 × 768 | Layout smoke check |
| 1440 × 900 | 100% | 1440 × 900 | Layout smoke check |
| 1920 × 1080 | 100% | 1920 × 1080 | Layout smoke check |
| 1366 × 768 | 125% | 1093 × 614 | Layout smoke check |
| 1366 × 768 | 150% | 911 × 512 | Layout smoke check |

At all six settings, the four chart positions matched the checkpoint and the document fit the viewport width. The primary check covered Persian RTL, font loading, keyboard theme switching and table access, and chart names.

At 1366 × 768 and 100% zoom, entrance replay measured 28.85 trend and 28.58 branch redraws per second. Both charts stopped redrawing at idle. The handoff also records exact fixture values after updates, tooltip and table accuracy, reduced motion, failure recovery, renderer and resize observer cleanup on theme change, and passing typecheck and production build. The user approved the migrated Lab after a manual visual and behavior check.

The earlier 1440 × 960 visual comparison recorded 26 changed pixels in Dark Mode and one in Light Mode. The user accepted those differences. Their exact cause remains unknown.

## Reference reconstruction and visual approval

Inspect existing components first. When reconstruction is needed, record observed and inferred properties and build a temporary browser specimen outside production source. Compare the representative states at matching desktop browser sizes. Report visible differences and obtain human visual approval before reusable implementation for reference fidelity work or a material redesign. Use the approved browser reconstruction as the visual authority. Use Figma capture when it helps the comparison or the user requests it. [DIDRAH component workflow](../../../src/WebApp/.agents/skills/didrah-component-workflow/SKILL.md) · [Frontend instructions](../../../src/WebApp/AGENTS.md)

Implement the reusable component in its owning module and render it in the Lab. Apply the acceptance checklist to relevant states, themes, accessibility, layout, and behavior. Use focused renderer and performance checks for complex visualizations. Report evidence and stop at the requested approval gate. Give the user the absolute paths of applicable desktop artifacts for manual visual inspection.

For routine Backend integration, follow docs 09 and 17 and map accepted data to the typed component inputs. Use the design stages when the task includes component design work.

## Remaining component families

This proposed roadmap covers frontend design. The repository-wide development stages continue to govern repository implementation scope and completion criteria. Obtain separate authorization before starting each subsequent component family or any Stage 4.6 work. [Repository development stages](../../DEVELOPMENT_STAGES.md)

- Surfaces and Panels
- Navigation and Sidebar
- Buttons and Controls
- KPI and Insight Components
- AI Assistant and Chat
- Workflow Visualization
- Data Tables and Feedback
- Full Dashboard Composition

## Technical debt

| Issue | Status |
|---|---|
| Active animation callbacks | The R5.4 Lab benchmark measured about 500 application callbacks per second during motion and zero at idle. The callback count measures scheduling work separately from chart redraws. |
| Page-wide listener growth | R5.4 measured growth from 1,396 to 4,302 listeners over ten mount and disposal cycles. All 70 tracked chart and Canvas references were released. Listener ownership remains unknown. |
| Browser CPU measurement | CPU readings varied across runs, including idle samples with zero chart activity. GPU readings also varied. The source of the variation remains open. |
| Production chart mapping and API validation | Implement and validate the authorized `ChartSpec` mapping and generated OpenAPI types after approval of the doc 17 wire contract, allowlist, limits, numeric display, and compatibility policy. |
| Full-dashboard performance | Measure the full dashboard with representative data on the approved hardware, browser, and network profile when available. The current measurements cover the Lab and its sample data. |

## Open design decisions

- Visual refinement for Light Mode and detailed design for the remaining component families.
- Any extension of the global token scales or general UI motion presets.
- Exact product-wide desktop viewport matrix.
- Future 3D scene style and asset guidance.
