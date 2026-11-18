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

1. Reads only validated, final reports and QA results.
2. Validates each artifact against the read-only reference JSON Schema.
3. Builds the output path by joining `OUTPUT_DIR` directly with `briefs/day_XXX/<manager_id>.json` or `qa/<question_id>.json`.
4. Resolves the final path and verifies that it remains inside `OUTPUT_DIR`.
5. Rejects absolute-path injection and `..` path traversal.
6. Writes a temporary file on the same filesystem as the final file.
7. Flushes and closes the temporary file before an atomic rename.
8. Records the content hash and an Export Receipt in PostgreSQL.
9. Records the `trace_id` and the relative artifact path in the receipt.
10. Does not write internal logs, database files, or non-contract files to `OUTPUT_DIR`.

Flow:

```
Publisher → Submission Exporter → OUTPUT_DIR/briefs/day_XXX/<manager_id>.json
Validated QA Result → Submission Exporter → OUTPUT_DIR/qa/<question_id>.json
```

## Consequences

- This is a P0 gap - required for evaluation to pass
- Publisher no longer directly responsible for filesystem output
- Submission Exporter is the single writer to `/submission`
- Atomic writes prevent evaluator seeing partial files
- For `OUTPUT_DIR=/submission`, the exporter writes directly below `/submission`. It does not create `/submission/submission`.

## Source

Addresses Gap 2 from architectural review: "خروجی `/submission`"
