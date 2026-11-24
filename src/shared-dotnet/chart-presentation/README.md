# Shared Chart Presentation Library

This directory is reserved for the shared .NET chart-presentation contract used by Backend API and Background Worker.

The library contains only:

- Internal contract types such as `ChartIntent`, `ChartSpec`, and `PresentationResponse`
- Deterministic chart-specification construction
- Contract validation
- Versioned JSON serialization

The library does not contain persistence, authorization, query execution, KPI calculation, job control, React, or ECharts code.

The directories have these boundaries:

- `contracts`: immutable contract and value types
- `building`: deterministic construction rules
- `validation`: contract and compatibility validation
- `serialization`: versioned JSON serialization

