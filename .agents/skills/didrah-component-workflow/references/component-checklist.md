# Component acceptance checklist

Complete every applicable check and record the evidence. Mark checks that do not apply. Report any blocked check before you claim completion.

## All reusable components

- [ ] The correct shared or feature module owns the component. Its typed public inputs work with callers outside the Lab.
- [ ] Review imports. Shared code has no dependency on Lab code or fixtures. Reusable presentation has no dependency on Backend transport or feature business logic.
- [ ] The Lab imports and renders the actual reusable component. Fixtures and controls exercise its public interface.
- [ ] Check visuals against the approved source. Use existing tokens, adapters, and shared recipes. Keep family-specific variants local.
- [ ] Check Persian RTL, Dastkhat, supported viewport sizes, Dark Mode, and Light Mode.
- [ ] Check accessible names, meaningful status text, and accessible alternatives where applicable. Exercise loading, empty, error, and disabled states where supported.
- [ ] Record the results of the applicable typecheck and production build checks.

## Interactive components

- [ ] Exercise pointer and keyboard interaction. Check focus order, visible focus, and activation. Check focus restoration where applicable.
- [ ] Verify the applicable hover, focus, active, selected, and disabled states. Check that status and selection remain clear without color alone.

## Animated components

- [ ] Exercise triggers, interruption, and completion. Check that the component reaches the correct final state.
- [ ] Enable reduced motion and verify that content and controls stay usable. Check animation cleanup when the component is removed.

## Complex visualizations

- [ ] Exercise dynamic data, compatible updates, and structural changes. Check numeric values, units, missing values, and tooltips against the input. Check the accessible data alternative.
- [ ] Check synchronization where charts share a clock. Verify exact final values after motion and disposal of renderer instances, listeners, observers, and animation callbacks.
- [ ] Cause a failure in one chart and verify that other charts remain usable. Check its fallback and recovery where applicable.
- [ ] Measure actual redraws during motion and at idle. For luminous Classic Mode charts, verify the default 30 FPS redraw budget and zero continuous redraws at idle. Record the scenario and CPU and GPU use where measurable.

## Reference work and visual approval

- [ ] If the user supplied a reference, record what you can see and what you infer. Check the representative states in the Lab at relevant desktop sizes.
- [ ] Give the user the Lab route and the steps for interactive review. Include focused screenshots if requested or if they help explain a specific visual issue.
- [ ] Record the user's visual approval at the applicable gate. After stage approval and technical validation, make a dedicated Git commit for that stage.
