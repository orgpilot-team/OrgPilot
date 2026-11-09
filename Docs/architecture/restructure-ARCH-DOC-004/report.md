# ARCH-DOC-004 structural migration report

Status: **Draft / Pending Review**. Date: 2026-11-09.

The team approved documentation locations. This task changes no architecture choice or product contract. The Registry remains subject to semantic review. No Open issue is closed. No acceptance test is Passed. No inferred relationship is approved.

## Content locations

| Original content | Current location | Preservation action |
|---|---|---|
| 001 system architecture | [001](../001-system-blueprint.md) | Keep all body content. Change navigation and add one responsibility note. |
| 002 data architecture | [002](../002-data-architecture.md) | Keep all contracts and explanations. Change navigation and add one responsibility note. |
| 003 title, authority, sections 1 and 2 | [Registry source context](../registry/README.md#source-context) | Keep original readable text and historical metadata. |
| 003 section 3, ADR-01 through ADR-17 | [Decision records](../registry/decisions-registry.md) | Make all 17 full original records readable. Keep statuses, options and consequences. |
| 003 sections 4, 6 and 8 | [Roadmap](../003-roadmap.md) | Keep prerequisites, P0-P5, milestones, gates, sequence and performance/cost context. |
| P2/P3 conflict paragraph | [REG-ISS-001](../registry/open-issues-registry.md#reg-iss-001) | Keep the full paragraph. Roadmap links to this unresolved issue. |
| P5 supplemental delivery paragraph | [Delivery checklist](../registry/acceptance-register.md#delivery-checklist) | Keep the full paragraph. Roadmap links to the criterion. |
| 003 section 5 | [Risk register](../registry/risk-register.md) | Keep 13 original source rows in 12 source extracts and their conditions. Retain all 20 existing risk records. |
| 003 section 7, AT-01 through AT-30 | [Acceptance register](../registry/acceptance-register.md) | Keep full criteria, seven shared supplements, authority notes, three-level content matrix, R1-R8 and manager-input cases. |
| 003 section 9 | [Historical verification](../004-reconciliation-review.md#decisions-9) | Append unchanged historical text. Explain its historical Git context. |
| 003 section 10, DL-01 through DL-19 | [Open issue records](../registry/open-issues-registry.md) | Keep original rows, intro, alternatives and qualifications. Keep ten existing Registry issues. |
| Final execution-scope paragraph | [Execution gates](../003-roadmap.md#roadmap-execution-gates) | Keep original conditions. Add no dependency. |
| Old 003 file and anchors | [Compatibility document](../registry/README.md#source-context) | Keep 95 legacy explicit and heading anchors with current navigation. Keep no duplicate decision bodies. |
| Original 004 reconciliation | [004](../004-reconciliation-review.md) | Keep all original evidence, Q01-Q17, authority and conclusions. Change active navigation only. |

The [complete line map](content-location-map.csv) locates all 346 non-empty original 003 lines in current readable documents. The [source promotion ledger](source-extract-promotion.csv) records 85 source extracts made readable. Four quoted data-model extracts remain evidence in the issue register. Document 002 remains their data-contract location. No unique section was left without a current location.

The source archive is a check artifact, not a second authority. Current records are readable without opening the archive. The archive retains original bytes for inspection.

## Content and status checks

The [validation results](validation-results.csv) check source preservation, source paths, anchors and unchanged status fields. The checks preserve:

- 17 ADRs, 19 DLs, 20 risks and all 30 ATs with their full criteria.
- Five Accepted boundaries: one bounded Agent; PostgreSQL-only product execution; independent valid-report publication; deterministic calculation, Signal, authorization and final validation; human-controlled organizational decisions.
- All 29 Open issues, Proposed mechanisms and missing-evidence limits.
- All 2,470 Proposed Relationship rows. They provide no approved implementation dependency.
- All 4,586 matrix rows. Only source navigation fields change in 657 rows. The [navigation ledger](matrix-navigation-changes.csv) shows each change. Original source references remain in `source_ref`. `source_tracking` retains original extraction provenance; current Registry files are untracked.

Checks compare full source text after link-destination and formatting normalization. They also compare matrix fields. These checks support content preservation. They do not claim exhaustive human semantic verification or product execution.

## Links and retained limitation

All 95 legacy anchors and their current targets resolve. All 4,586 matrix source paths and anchors resolve. The repository Markdown scan finds no new broken link. The 29 diagram files have no document navigation links; their SVG internal targets resolve. Four external or host URLs are outside the local-link check.

The universal repository direct-link condition has one retained blocker: **64 pre-existing broken references** in three historical audit reports. Those reports are immutable evidence. They refer to old Dataset or brief locations. This task does not edit them to normalize links. The [historical reference catalog](historical-reference-catalog.md) provides a verified current file or directory for every occurrence. The [before](before-links.csv) and [after](after-links.csv) inventories show the retained failures. No content migration is blocked by these references. Direct historical links still need a separately approved repair if the team requires zero broken links across immutable reports.

## Git and file preservation

HEAD remains `0a42950d1ce9734433d961540af9ab4be21573b2`. No commit, push or staging operation was performed. Git reports four modified tracked architecture files. The new roadmap, Registry and inspection artifacts remain untracked. Two preflight source-provenance edits in 001 and 004 were already present before this task; they are not attributed to this migration.

All 1,393 task-start files were hashed. Exactly ten existing files changed: the four architecture documents, Registry README, four governance registers and the live traceability CSV. All other tracked and untracked files retain their bytes. No original file was removed. Dataset, SQL, DSL, diagrams and previous audit/triage artifacts are unchanged.

Use the [existing file ledger](existing-file-changes.csv), [new file inventory](new-file-inventory.csv), [all-file baseline comparison](baseline-all-files.csv), [task before/after diff](before-after.diff), [baseline tracked diff](baseline-tracked.diff) and [Git status](git-status.txt) for review. The [preflight manifest](before-manifest.json) and `before-documents.zip` retain comparison inputs. The baseline comparison includes existing untracked sources and new deliverables. Hash ledgers exclude themselves and each other to avoid circular hashes.

## Use as a development reference

The document locations are ready for use within their stated limits. Requirement and Accepted text retain their authority. Open choices require the existing team/source/engineering route. Proposed mechanisms and inferred links require review before they can set implementation scope. Acceptance criteria remain planned tests until actual product evidence exists. The historical-link blocker remains explicit. This migration grants no semantic approval beyond the team's structural approval.

Run `python -B Docs/architecture/restructure-ARCH-DOC-004/validate_restructure.py` to repeat the checks. Do not rerun historical Registry generators to validate this migration; those scripts can overwrite current records.
