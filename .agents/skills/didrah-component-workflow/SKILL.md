---
name: didrah-component-workflow
description: >-
  Develop and validate DIDRAH frontend components in src/WebApp. Use for reference
  reconstruction, new reusable components, visual redesign, component-family refinement,
  changes to reusable interactions or animation, and Design System integration or
  visual validation.
---

# DIDRAH component workflow

Read the [frontend instructions](../../../src/WebApp/AGENTS.md) before work in `src/WebApp`. Do only the work in the approved stage. For routine Backend API or authentication integration, follow the feature and API boundaries in [doc 09](../../../docs/Analytics/docs/09-web-application-components.md) and [doc 17](../../../docs/Analytics/docs/17-chart-presentation-contract.md). Map accepted data to the existing typed inputs. Use the design workflow when the task includes component design.

## Discovery and reference analysis

Inspect the current components, variants, tokens, theme adapters, and related code. Reuse an existing implementation if its public interface can support the change. Identify the shared or feature module that owns the component.

If the user supplies a reference, identify the component and its relevant states. Examine composition, geometry, typography, spacing, color, gradients, shadows, and lighting. Record what you can see and what you infer.

## Implementation and Lab review

Implement the component directly in its owning module in `src/WebApp`. Define typed public inputs. Keep the component usable outside the Lab. Keep reusable presentation independent of mock fixtures, Backend transport, and feature business logic. Keep component-specific styles and behavior in the owning module.

Render the actual component in the Design System Lab at `/design-system`. Use representative fixtures and controls for supported states and interactions. Keep specimens, fixtures, and controls in the Lab. Shared modules must never import Lab code.

Use the Lab for interactive visual review. Make an external prototype only if the user requests one. Use approved implementation source for exact rendering values. Follow the desktop scope, theme, Persian RTL, Dastkhat, and accessibility rules in the frontend instructions.

## Interaction and animation

Reuse the existing animation code. Use ECharts and the shared chart motion code for charts. Use Motion when it helps UI interactions and transitions. Preserve keyboard access, visible focus, and reduced motion. Apply chart redraw limits only where the frontend instructions specify them.

## Technical validation

Use the [component acceptance checklist](references/component-checklist.md). Select checks for the paths and behaviors that changed. For component code changes, run `npm run typecheck` from `src/WebApp`. Run `npm run build` when changes can affect the production build or when the stage requires it.

For complex visualizations, check applicable data updates, numeric and tooltip accuracy, synchronization, resource disposal, failure isolation, idle behavior, and redraw rates. Measure CPU and GPU use when relevant and measurable. Reserve performance benchmarks for changes that can affect performance.

Use targeted automated browser checks where they verify behavior. Capture screenshots only if the user requests them or if they help explain a specific visual issue. Avoid extensive screenshot matrices and pixel comparisons.

## Approval and completion

Give the user the Lab route and the steps to exercise the relevant states. Report the changed paths, public interface changes, technical validation results, and known issues. If you generate review artifacts, give their absolute paths.

The user does the manual visual review and gives visual approval. Ask for that approval at the applicable gate and wait for it. After each implementation stage receives the required approval and passes its technical checks, make a dedicated Git commit with a message that identifies the work. Include only changes for that stage. Start a subsequent stage only when the user authorizes it.

## Approved chart examples

Use [SalesTrendChart](../../../src/WebApp/src/shared/visualization/charts/SalesTrendChart.tsx) and [BranchSalesChart](../../../src/WebApp/src/shared/visualization/charts/BranchSalesChart.tsx) as examples of typed dynamic inputs and Dark Mode luminous variants. Reuse the [chart host](../../../src/WebApp/src/shared/visualization/charts/ChartHost.tsx) and [shared sales chart presentation](../../../src/WebApp/src/shared/visualization/charts/SalesChartPresentation.tsx) where applicable. Use the [trend recipe](../../../src/WebApp/src/shared/visualization/charts/luminous-sales-trend.ts) and [branch recipe](../../../src/WebApp/src/shared/visualization/charts/luminous-branch-sales.ts) for exact rendering values.

Preserve the [shared animation clock](../../../src/WebApp/src/shared/visualization/charts/chart-motion.ts), the default 30 FPS redraw budget, exact final values, reduced motion, failure isolation, and zero continuous redraws at idle. Keep intermediate animation values in the renderer. Follow [sales chart motion](../../../src/WebApp/src/shared/visualization/charts/SalesChartMotion.tsx) for the approved timing. The trend entrance takes 900 ms. The branch entrance takes 700 ms after a 120 ms delay. The stagger spans 90 ms across multiple branch items. Compatible data transitions take 450 ms. Keep these settings specific to the approved charts.
