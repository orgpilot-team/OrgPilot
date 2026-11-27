---
name: didrah-component-workflow
description: >-
  Develop and validate DIDRAH frontend components. Use for reference reconstruction,
  new reusable components, visual redesign, component-family refinement, changes to
  reusable interactions or animation, and Design System integration or visual validation.
  Skip the full workflow for Backend API or authentication integration, routine business
  logic changes, unrelated bug fixes, infrastructure, and deployment.
---

# DIDRAH component workflow

Read the frontend [AGENTS.md](../../../AGENTS.md) for permanent rules. Use only the stages that apply to the authorized task. For Backend integration, follow the feature and API boundaries in [doc 09](../../../../../docs/Analytics/docs/09-web-application-components.md) and [doc 17](../../../../../docs/Analytics/docs/17-chart-presentation-contract.md). Map accepted data to the existing typed inputs. Use the design stages only if the user also requests component design work.

## Desktop scope

DIDRAH supports desktop browsers only. Mobile and tablet layouts, breakpoints, screenshots, and device-specific validation are out of scope. Check resizing at supported desktop viewports. Keep keyboard access and visible focus states functional.

Use the approved Dastkhat typography. Defer global typography refinement until the initial component families are complete.

## A. Discovery and reuse

Inspect the current source for relevant components, variants, tokens, theme adapters, and related implementations. Identify what to reuse. Decide which shared or feature module owns the component and define its public interface. Extend an existing implementation where its contract can support the change.

## B. Reference analysis

If the user supplies a reference, identify the representative component and its visible states. Inspect composition, geometry, typography, spacing, color, gradients, shadows, and lighting. Identify reusable patterns. Record which properties you can observe and which properties you infer.

## C. Reconstruction and visual approval

When a reconstruction is necessary, use HTML, CSS, and SVG as appropriate. Keep temporary specimens outside production source. Capture equivalent desktop browser views for comparison and report any visible differences. Use Figma capture only if it helps the comparison or the user requests it. Use the approved browser reconstruction as the implementation authority. For reference fidelity work or a material redesign, present the comparison and wait for visual approval before reusable implementation.

## D. Reusable implementation

Implement the component in its shared or feature module from the start. Define typed public inputs and keep presentation independent of data transport and business logic. Reuse the Design System and keep behavior specific to the component in its own module.

## E. Design System Lab

Render the actual reusable component in the Lab at `/design-system`. Use representative fixtures and controls to demonstrate supported states and behaviors. Keep specimen composition and controls in the Lab.

## F. Interaction and animation

Implement the interactions that the component needs. Reuse the existing animation infrastructure. Use ECharts and the shared chart motion code for chart rendering and chart motion. Use Motion for UI interactions and transitions that benefit from it. Preserve keyboard access and reduced motion. Apply chart redraw limits only where the frontend rules specify them.

## G. Validation

Use the [component acceptance checklist](references/component-checklist.md) for the applicable checks. Check the public inputs, dependency direction, Lab use, visuals, supported states, accessibility, RTL, typography, layout and resizing at supported desktop viewports, and both themes. Run `npm run typecheck` and `npm run build` from `src/WebApp` for component implementation work. For complex visualizations, also verify dynamic data, numeric and tooltip accuracy, synchronization, disposal, failure isolation, idle behavior, actual redraw rates, and CPU and GPU use where measurable. Match the checks to the component. Simple static components need no performance benchmark.

## H. Approval and completion

Report the implemented component and its public interface, exact changed paths, applicable screenshots and comparisons, validation results, known limitations, unresolved technical debt, and proposed documentation changes. Stop at the requested approval gate. Obtain user approval for visual decisions at that gate. Start subsequent work only when authorized.

### Artifact delivery and visual inspection

Generate the required artifacts. Use available tools within existing permissions to do automated technical and visual checks. Use automated browser tests, headless browser rendering, screenshot capture, and visual regression tests as applicable.

Apply this policy at each approval gate and at completion. Give the exact absolute filesystem path of each generated output. The user opens the artifacts and does the manual visual inspection.

Do not open Windows File Explorer or output directories. Do not launch the user's interactive browser. Do not open generated screenshots, HTML previews, or reports on the user's desktop. Do not request elevated permissions solely for these actions.

## Approved chart examples

Use [SalesTrendChart](../../../src/shared/visualization/charts/SalesTrendChart.tsx) and [BranchSalesChart](../../../src/shared/visualization/charts/BranchSalesChart.tsx) as examples of typed dynamic inputs and Dark Mode luminous variants. Reuse the [chart host](../../../src/shared/visualization/charts/ChartHost.tsx) and [shared sales chart presentation](../../../src/shared/visualization/charts/SalesChartPresentation.tsx) where applicable. Use the [trend recipe](../../../src/shared/visualization/charts/luminous-sales-trend.ts) and [branch recipe](../../../src/shared/visualization/charts/luminous-branch-sales.ts) for exact rendering values.

Preserve the [shared animation clock](../../../src/shared/visualization/charts/chart-motion.ts), the default 30 FPS redraw budget, exact final values, reduced motion, failure isolation, and zero continuous redraws at idle. Keep intermediate animation values in the renderer. Follow [sales chart motion](../../../src/shared/visualization/charts/SalesChartMotion.tsx) for the approved timing. The trend entrance takes 900 ms. The branch entrance takes 700 ms after a 120 ms delay. The stagger spans 90 ms across multiple branch items. Compatible data transitions take 450 ms. Keep these settings specific to the approved charts.
