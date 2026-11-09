# ARKA source-driven architecture audit

Review date: 2026-11-09, Asia/Tehran. This pack contains documentation and read-only source evidence. It is not product code or product acceptance evidence.

- [Detailed audit report](audit-report.md), [full findings](findings.csv), and [document-unit ledger](document-review-ledger.csv).
- [Traceability guide](requirements-traceability.md), [339-row matrix](requirements-traceability.csv), and [acceptance basis](acceptance-basis.csv).
- [Eight rule contracts](rule-contracts.csv), [55 KPI contracts](kpi-contracts.csv), [12 Workflow stages](workflow-contracts.csv), [23 manager inputs](manager-input-contracts.csv), and [schema properties](output-schema-contracts.csv).
- [Source checks](source-checks.json) and [brief content check](brief-content-check.json).
- [Structurizr gap report](structurizr-gap-report.md) and its [element](structurizr-elements.csv), [relationship](structurizr-relationships.csv), and [view](structurizr-views.csv) catalogs.
- [Change report](change-report.md), [current diff](reconciliation.diff), [verification](verification.json), [pre-edit ZIP](pre-edit.zip), and [baseline manifest](pre-edit-manifest.json).

## Reproduce the documentation checks

From the project root, run:

```text
python -B docs/architecture/audit-2026-11-09/verify_audit.py
```

This command reads sources, existing model text, the saved backup and audit records. It writes only this pack's verification JSON. It does not run SQL, models, applications, renderers, restore jobs, or official acceptance tests. The Python standard library is sufficient.

The phase scripts record how this audit was authored. They are not an application or a new architectural implementation. Their duplicate-finding guards prevent accidental repeated application. Do not rerun authoring phases on already-corrected documents. The source/table builders can regenerate their audit records. They do not choose an Open policy.

## Baseline and comparison

`pre-edit.zip` preserves all 79 pre-existing architecture documentation/model files. Each member is checked against `pre-edit-manifest.json`. The manifest hashes all 1,452 initial workspace files outside `.venv` and Git internals. Original source data, brief, contracts, audits, and DSL are protected by that baseline.

The unified diff compares current text with the verified pre-edit bytes and includes new audit text artifacts. It excludes itself and its own derived change-index records. The ZIP is a binary addition and is supplied separately. The previous root reconciliation.diff remains historical and unchanged. No Git repository was found. No commit or push was attempted.

All product AT gates are planned. A documented requirement, matched count, valid link, or correct schema is not proof of numerical correctness, safety, access enforcement, model quality, or final acceptance.
