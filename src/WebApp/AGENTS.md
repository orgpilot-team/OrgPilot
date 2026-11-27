# DIDRAH frontend instructions

Follow the [repository instructions](../../AGENTS.md). Apply these rules to work in `src/WebApp`.

## Component ownership

- Put generic UI in `src/shared/design-system` and reusable visualizations in `src/shared/visualization`. Keep feature-specific UI, state, and business logic in the feature that owns them.
- The Design System Lab in `src/app/design-system-lab` consumes reusable components. It owns demonstration composition, mock fixtures, development controls, reference specimens, validation scenarios, and benchmark controls. Shared modules must never import from the Lab.
- Give reusable components typed public inputs. Keep presentation independent of mock fixtures, Backend transport, and feature business logic. Reuse existing components, tokens, adapters, and utilities first. Keep each shared visual recipe or behavior in its owning module so all consumers receive the same changes.

## Themes, localization, and accessibility

- Reuse the primitive and semantic tokens under `src/shared/design-system/tokens` and the providers and adapters under `src/shared/design-system/theme`. Keep both Dark Mode and Light Mode functional.
- Use scoped variants for component-family colors, gradients, shadows, and geometry. Add global tokens only for decisions that apply across the Design System. Use approved implementation source for exact rendering parameters. Preserve approved visuals unless the user authorizes a redesign.
- Use Persian and RTL by default. Reuse the approved Dastkhat typography. Preserve keyboard navigation, visible focus, meaningful labels, accessible alternatives, and reduced motion. Support applicable loading, empty, error, disabled, and interactive states.

## Performance

- Reuse the existing renderer lifecycle, animation, and resource cleanup code. Keep chart animation finite and event-driven. Stop continuous redraws at idle.
- Preserve the approved 30 FPS redraw budget for luminous Classic Mode chart motion. Apply this budget only to those charts. Match performance checks to component complexity.

## Scope and approvals

- The DIDRAH Web Application is desktop-only. Mobile and tablet layouts, breakpoints, screenshots, and device-specific validation are out of scope.
- Support resizing at supported desktop viewports. Keep keyboard access and visible focus states functional.
- Defer global typography refinement until the initial component families are complete.
- Use the [DIDRAH component workflow](.agents/skills/didrah-component-workflow/SKILL.md) for relevant component creation, reference reconstruction, visual redesign, component-family refinement, and Design System validation. Apply these architectural rules to integration and maintenance work as well.
- Complete only the authorized stage. Stop at each explicit approval gate and wait for approval before starting a subsequent component family. Get authorization before installing dependencies or changing unrelated architecture.
