# ARCH-DOC-005 cleanup report

Status: **Draft / Pending Review**. Date: 2026-11-09.

The Roadmap structure and documentation navigation are corrected. The obsolete combined file is removed. No architecture choice, source contract or acceptance state changed. This task creates no product code or architecture visualization.

## Final locations

| Document | Responsibility |
|---|---|
| [001](../001-system-blueprint.md) | System modules, flows, interfaces, authorization and trust boundaries. |
| [002](../002-data-architecture.md) | Data contracts, ingestion, snapshots, canonical calculations, lineage, quality and history. |
| [003 Roadmap](../003-roadmap.md) | P0-P5, sequence, dependencies, milestones, gates and measurement. |
| [004](../004-reconciliation-review.md) | Original review, Q01-Q17 and historical evidence. |
| [Registry](../registry/README.md) | ADR, DL, risk, AT and traceability records. |

All supporting audit, source and validation files remain. The [file preservation ledger](file-preservation.csv) records each task-start file.

## Roadmap section map

| Before | After | Body treatment |
|---|---|---|
| English document title | Persian title | Title only. |
| Section 4: prerequisite answers | [۱. اولویت پاسخ‌های لازم](../003-roadmap.md#roadmap-prerequisites) | Full body retained. |
| Section 6: implementation phases | [۲. مسیر مرحله‌ای پیاده‌سازی پس از بازبینی](../003-roadmap.md#roadmap-phases) | P0-P5 order, scope, milestones and gates retained. |
| Section 6.1: first end-to-end slice | [۲.۱. کمترین مسیر سرتاسری قابل بررسی](../003-roadmap.md#roadmap-first-slice) | Full steps retained; list digit style corrected. |
| Section 8: performance and cost | [۳. اندازه‌گیری عملکرد و هزینه](../003-roadmap.md#roadmap-measurement) | Full measurements, limits and exceptions retained. |
| English execution-gate heading | [۴. شرایط شروع اجرای محصول](../003-roadmap.md#roadmap-execution-gates) | Heading only. |
| English governance-navigation heading | [۵. مراجع حاکمیت و تحویل](../003-roadmap.md#roadmap-governance) | Heading only. |

The [machine-readable section map](roadmap-section-map.csv) records exact headings and anchors. The three legacy `decisions-*` anchors and the old execution-gate anchor are removed from the Roadmap. Incoming navigation uses descriptive anchors. No requirement paragraph was shortened or removed. Existing Registry references for the P2/P3 conflict and P5 delivery criteria remain.

## Content preservation and removal gate

The complete obsolete compatibility document and all 95 original anchor destinations were inspected. The [destination map](legacy-destinations.csv) resolves each old anchor to its exact current section. No redirect or placeholder document remains.

Before deletion, the cleanup checked 297 substantive lines from the full original combined source against current readable documents. The [content check](original-content-check.csv) records each line. Headings and formatting are covered by the section and anchor maps. Complete Registry bodies were also compared against task-start bytes after URL normalization. Full AT criteria, management-level matrix, manager-input cases, R1-R8 cases, delivery criteria, risk conditions and original alternatives remain. No essential section lacked a destination.

The original system, data and reconciliation bodies pass the same comparison. The only visible section-label correction in 002 changes its measurement reference from section 8 to section ۳. Previous audit findings and supporting explanations remain unchanged; their navigation is repaired.

## Link results

- Task-start inventory: **1,077** links; **64** broken references.
- Final inventory: **1013** links across all repository Markdown files; **zero** unresolved local paths, wrong-case paths or missing anchors.
- **88** URL replacements: **64** historical repairs, **16** old combined-document URLs and **8** Roadmap-anchor updates. The 16 include 14 active Markdown links and two URLs inside a quoted source extract.
- **33** live matrix rows have source-anchor navigation changes. All other fields remain exact.
- **Zero** new broken links. **Zero** active Markdown links to the removed file. **Zero** genuinely missing local targets remain.
- Four external or host URLs are outside the local-file check. No network validation is claimed.

Each of the 64 historical failures is individually matched by source file, original line and original URL in [historical reconciliation](historical-64-reconciliation.csv). Every replacement points to an existing file or directory. The [repair ledger](link-repairs.csv), [before inventory](before-links.csv), [final inventory](link-validation.csv) and [empty unresolved list](unresolved-links.csv) provide the evidence. Checks cover relative paths, exact capitalization, Unicode names, percent decoding, directory targets, explicit anchors, generated heading anchors and reference-style definitions.

## Registry consistency

All 17 ADRs, 19 DLs, 20 risks, 30 ATs and seven acceptance supplements remain. All 29 issues remain Open. All five Accepted boundaries remain unchanged. All 2,470 inferred relationships keep their unapproved classification. All ATs remain Planned / Not Executed. The Registry remains Draft / Pending Review. Structural approval grants no further semantic approval.

## Historical identifier limitation

No active Markdown navigation points to the removed file. Original source identifiers still occur in quoted audit findings, source-provenance fields, hash ledgers, snapshots, diffs and historical utilities. The [identifier inventory](retained-historical-identifiers.csv) lists these occurrences. They describe old source states; they are not current document links. Historical utilities were preserved and were not run. Registry README directs users to the current cleanup report.

One comment in the unchanged Structurizr DSL still contains the former filename. The task prohibits DSL changes. This task therefore does **not** claim a literal purge of the former filename from all repository bytes. It does establish zero active Markdown links to that file. Original evidence and the DSL were preserved rather than silently rewritten.

## Git and exact changes

HEAD remains `0a42950d1ce9734433d961540af9ab4be21573b2`. No staging, commit, push, reset or cleanup operation was performed. Git reports the pre-existing modifications in 001, 002 and 004, plus deletion of the tracked old 003 file. The current Roadmap, Registry and evidence remain untracked. Document 001 is unchanged by this task.

Of 1,416 task-start files, 21 existing documentation files changed and only the requested obsolete file was removed. Dataset, SQL, source contracts, original PDF, DSL, diagrams and all unrelated tracked/untracked bytes remain unchanged. Supporting visualization Markdown files receive navigation repairs only. No diagram is generated or changed.

Exact existing files changed:

```text
Docs/architecture/002-data-architecture.md
Docs/architecture/003-roadmap.md
Docs/architecture/004-reconciliation-review.md
Docs/architecture/audit-2026-11-09/audit-report.md
Docs/architecture/audit-2026-11-09/change-report.md
Docs/architecture/audit-2026-11-09/requirements-traceability.md
Docs/architecture/registry/README.md
Docs/architecture/registry/acceptance-register.md
Docs/architecture/registry/approval-readiness.md
Docs/architecture/registry/deduplication-ledger.md
Docs/architecture/registry/open-issues-registry.md
Docs/architecture/registry/traceability-matrix.csv
Docs/architecture/restructure-ARCH-DOC-004/report.md
Docs/architecture/visualizations/README.md
Docs/architecture/visualizations/open-questions.md
Docs/architecture/visualizations/proposed-entity-contracts.md
Docs/architecture/visualizations/security-examples.md
Docs/review/dq-001-report.md
Docs/review/kpi-val-001-report.md
Docs/review/rca-001-report.md
Docs/review/team-guide-technical-review.md
```

Removed: `Docs/architecture/003-decisions-and-roadmap.md`.

New files are limited to this report directory. See the [new-file inventory](new-file-inventory.csv), [Git before](git-before.txt), [Git after](git-after.txt), [task diff](before-after.diff) and [baseline tracked diff](baseline-tracked.diff). The preflight manifest and compressed source snapshot retain comparison inputs. Hash evidence describes its capture time; historical hash tables are not current-file integrity claims after link maintenance.

## Validation and use

All **31** documentation checks pass. See [results](validation-results.csv) and [machine-readable results](validation-results.json). These checks verify content preservation and navigation. They do not execute product acceptance tests or claim exhaustive human semantic verification.

The documentation can serve as a development reference within its explicit Requirement, Accepted, Open, Proposed and Evidence Pending limits. No inferred relationship establishes an approved execution dependency. Missing evaluation or source contracts still require their existing closure route.

Repeat the checks with `python -B Docs/architecture/cleanup-ARCH-DOC-005/validate_cleanup.py`. Do not run historical extraction generators against the current structure.
