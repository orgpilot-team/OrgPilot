# 13. Submission Exporter for /submission Output

Date: 2026-11-17

## Status

Accepted

## Context

The evaluator does not check the Dashboard or API; it requires specific files at:

- `/submission/briefs/day_XXX/<manager_id>.json`
- `/submission/qa/<question_id>.json`

The current architecture has Publisher writing to PostgreSQL and Report API reading from it, but no component writes to the `/submission` filesystem.

## Decision

Add a `Submission Exporter` component in the Backend API that:

1. Reads only validated, final reports and QA results
2. Validates again against JSON Schema before writing
3. Creates directory structure: `briefs/` and `qa/`
4. Uses atomic write (temp file + rename)
5. Records hash and export receipt
6. Prevents partial/incomplete output
7. Does not write internal logs, DB files, or non-contract files to `/submission`
8. Uses `OUTPUT_DIR` environment variable, not hardcoded paths

Flow:

```
Publisher → Submission Exporter → /submission/briefs/...
Validated QA Result → Submission Exporter → /submission/qa/...
```

## Consequences

- This is a P0 gap - required for evaluation to pass
- Publisher no longer directly responsible for filesystem output
- Submission Exporter is the single writer to `/submission`
- Atomic writes prevent evaluator seeing partial files

## Source

Addresses Gap 2 from architectural review: "خروجی `/submission`"
