# Registry semantic audit

State: **Draft / Pending Review**. Task: `ARCH-REG-002`. Date: 2026-11-09. Time zone: `Asia/Tehran`.

The audit corrects source identity and Registry extraction defects. It makes no architecture choice, closes no issue and passes no product acceptance test. The five Accepted architecture boundaries remain fixed.

## S01 source of record

Current official file: [the repository brief PDF](../../%D8%A8%D8%B1%DB%8C%D9%81%20%D9%BE%D8%B1%D9%88%DA%98%D9%87%20%D8%A8%D9%88%D8%AA%DA%A9%D9%85%D9%BE%20_%20%D8%AF%D8%B3%D8%AA%DB%8C%D8%A7%D8%B1%20%D8%A7%DB%8C%D8%AC%D9%86%D8%AA%DB%8C%DA%A9%20%D9%85%D8%AF%DB%8C%D8%B1%D8%A7%D9%86%20%D8%B3%D8%A7%D8%B2%D9%85%D8%A7%D9%86%DB%8C%20_%20%D8%AF%DB%8C%D8%AF%D8%B1%D8%A7%D9%87.pdf).

Repository path: `Docs/بریف پروژه بوتکمپ _ دستیار ایجنتیک مدیران سازمانی _ دیدراه.pdf`.

SHA-256, computed directly from the file bytes:

`f6761b4fc37145d152f2b9793b298e35f48db666d5205c4d02be0f5f13e4863b`

Previously recorded SHA-256, retained as historical provenance:

`6d68d3fcc285f6908af0d97c0429dfefb489f00b7f6538ed03573552ed6955f8`

The [current user instruction](audit-ARCH-REG-002/request.txt), section 1, establishes this existing file as the official S01 source. Source identification is resolved. The file is unchanged from both task snapshots. Only S01 provenance metadata changes in [001](../001-system-blueprint.md#system-2) and [004](../004-reconciliation-review.md). The old review claims remain historical statements; they are not newly attributed to the current byte identity.

`REG-ISS-010` stays **Open / Evidence Pending** for historical content comparison. The prior hash alone does not supply the historical PDF bytes. No comparison between the two PDF versions was performed. No semantic equality or changed requirement is claimed. PDF extraction/rendering packages were not available in the active runtime, so no fresh PDF page review is claimed. The audit uses the unchanged architecture extracts, actual dataset contracts and recorded approval evidence for its bounded semantic checks.

## Actual counts and previous report

| Item | Before this audit | After corrections |
|---|---:|---:|
| CSV rows | 4,191 | 4,586 |
| Main records | 548 | 565 |
| Evidence rows | 509 | 852 |
| Relationship rows | 3,134 | 3,169 |
| Requirement records | 339 as previously typed | 334 |
| Accepted Decision Boundary records | 0 as a separate type | 5 |
| Architecture component index records | 19 | 29 |
| Acceptance supplement index records | 0 | 7 |
| ADR / DL / AT / Risk | 17 / 19 / 30 / 20 | 17 / 19 / 30 / 20 |
| Open issues, including DLs | 29 | 29 |

The original source matrix has 339 IDs. Five are `DEC-*` Accepted choices, not Requirements. Their IDs and Accepted status are unchanged. The five Accepted ADR statement rows and the five `DEC-*` boundary records describe the same five boundaries in two indexes; they are not ten independent decisions. The numbered ADR statements remain 5 Accepted, 24 Proposed, 24 Open and 16 Requirement.

The 17 added main records index ten existing DSL endpoints and seven existing acceptance supplements. They create no component, test or requirement. The 343 added evidence rows provide 339 actual current source paths and four direct provenance/gap references. There are 40 added relationships and five removed unsupported relationships. The additions include five explicit S19-to-Accepted-statement approval links. No original record ID is removed. The original CSV columns are unchanged.

## Structural checks: exhaustive scope

Current result: **57/57 documentation checks succeeded**. All 4,586 rows and 3,169 active relationships were checked structurally. The active graph has 699 explicit-source relationships and 2,470 Proposed / Inferred relationships. There are no exact duplicate rows or repeated same-type/same-pair provenance groups. One reciprocal-reference group is reported; the membership hierarchy is acyclic. Nine source/phase/maintenance records have no graph edge and are listed for review. These counts do not establish exhaustive semantic approval.

The current check script parses every CSV row. It checks headers, row kinds, stable IDs, declared main identities, endpoint types, one-target representation, relation fields, source files, explicit anchors, local Registry locations, full-row duplicates and self links. It checks every old relationship identity against the new matrix. All five removed edges have exact before/after correction records. It also checks all 339 original source IDs against current file paths and source locators. JSON pointers and stated CSV record positions are checked where applicable.

The old checker accepted ten DSL IDs and seven supplement IDs as virtual endpoints. They now have actual main records. Source paths formerly written as `Project_berif/`, `dataset/` and lowercase `docs/` remain historical strings in `source_ref`; added evidence rows use current local paths. A historical string is not treated as a working link.

Membership links are checked for cycles. Cross-reference links and typed inverses can form cycles; they are not an execution dependency graph. The audit reports these groups in the cycle evidence file. It does not silently interpret a reciprocal ADR/DL/AT or source attribution as a circular implementation dependency. Distinct provenance rows for the same typed pair are reported separately from exact duplicate rows.

See [machine results](audit-ARCH-REG-002/validation-results.json), [source locator checks](audit-ARCH-REG-002/source-locator-checks.csv), [reference cycles](audit-ARCH-REG-002/reference-cycles.csv) and [repeated edge provenance](audit-ARCH-REG-002/repeated-edge-provenance.csv).

## Semantic review: method and limits

The review covers every high-impact record: 17 ADRs, 29 issues, 20 risks, 30 ATs and five Accepted statement rows. The [101-record review ledger](audit-ARCH-REG-002/record-review.csv) states the topic, source, finding and limits for each. The review compares the full retained source extract, the English index, status, alternatives, closure conditions and evidence boundary. It does not approve the design or test it.

All active relationships have an entry in the [relationship review ledger](audit-ARCH-REG-002/relationship-review.csv). Each row has one of these evidence classes:

- **Explicit Source Relationship:** a named gate, source attribution, source taxonomy or typed inverse supplies the association. An attribution supports the cited context; it does not approve every statement in the referenced document.
- **Proposed / Inferred Relationship:** a relevant suggested link or imported audit mapping lacks exact source proof or approval for the assignment. It remains a review aid.
- **Unsupported Relationship:** the claimed target does not address the actual source topic. The five demonstrated cases were removed from the active matrix and retained in the correction ledger.
- **Missing Relationship:** a source-backed endpoint or association was absent. These corrections are listed as added rows in the correction ledger; they are not counted as active unsupported edges.

For the high-volume requirement edges, checks are source-aware and bounded. All 339 source rows and their imported associations are checked against the original audit CSV. JSON/property, KPI, Workflow, rule, organization, input and raw-header families are inspected for source location and topic. The family mapping patterns, the umbrella requirements and obvious scope conflicts were reviewed. The remaining individual high-volume meanings are **not exhaustively verified**. Imported Requirement/Boundary-to-ADR/AT/component assignments remain Proposed. No random sample is presented as exhaustive proof. No script success is called exhaustive semantic approval.

The remaining bulk mapping candidates need review. For example, the old template links all 55 KPIs to the orders policy ADR. The source catalog identifies 33 KPI value-source sets without orders/order_events. This does not alone prove absence of an execution dependency: value sources and execution relations differ. Those candidate links remain inferred; no dependency is removed merely from equal values or a table-name check. Non-question input mappings also use broad test/component templates and need fixture-specific relevance review. Risk-to-test links remain inferred control-evidence candidates; no risk reduction is proved.

Relation meanings are bounded as follows: `part_of` is index membership; `has_criteria` attaches an existing supplement; `has_open_detail` links an ADR to an unresolved issue; `referenced_by` is a navigation inverse; `supports`/`supported_by` identify source context. `references` means topic relevance only when supported by the review class. No `requires` execution relation is introduced. Phase references apply only where the source names a phase, or must remain Proposed.

## Demonstrated corrections

Every substantive correction has before/after values, a reason and source evidence in [corrections.csv](audit-ARCH-REG-002/corrections.csv). Original file bytes are retained in [before-files.zip](audit-ARCH-REG-002/before-files.zip). The [text diff](audit-ARCH-REG-002/before-after.diff) includes changed untracked Registry files, so the comparison does not depend on ordinary Git diff.

Five unsupported active mappings were removed:

| Source record | Wrong target | Reason |
|---|---|---|
| REQ-13 | ADR-10 | Event/QA accuracy thresholds are not the model and budget choice. |
| REQ-CONF-02 | ADR-10 | Priority selection and report emphasis are not model execution budgeting. |
| REQ-INPUT-IN01 | ADR-10 | IN01 is the priority input. |
| REQ-DEL-03 | ADR-12 | Git source-history delivery is not database/archive retention. |
| REQ-JSON-QA-ROOT | ADR-14 | QA required root fields are not independent manager-report publication. |

Other corrections restore compressed ADR references, add relevant planned gates with appropriate evidence classes, add source-to-record attributions, add missing current source paths and align inverse relationship classifications. The complete set is recorded per row. The old audit evidence files are not rewritten.

Organizer classification is now precise. Eight issues have an unconditional organizer/source route: DL-02, DL-03, DL-05, DL-09, DL-10, DL-11, DL-16 and DL-17. DL-06 and DL-07 have conditional routes tied to a real source-meaning or working-hours contract gap. Model/provider/internal limits in DL-14 stay team work; final external hardware/profile remains DL-16. REG-ISS-010 needs historical comparison evidence after current identity confirmation. REG-ISS-008 is documentation maintenance, not architecture selection. Team routes total 24; engineering-evidence routes total 29. These sets overlap.

## Coverage, duplicates and orphans

All original ADR/DL/AT IDs remain. The five Accepted boundaries are backed by S19 and 003 section 1, with the relevant S16 result/body evidence. Proposed engineering mechanisms remain Proposed. A missing equivalence or benchmark result does not reopen an engine choice.

The decisions, risks and acceptance files are byte-identical to the task-start copies. All original Open-issue extract blocks are also retained. This preserves every original and supplemental AT criterion, the three-management-level content matrix and R1-R8 cases. All 30 ATs stay Planned / Not Executed. All 20 risks retain Not Assessed severity and unexecuted controls.

Potential overlaps are recommendations, not automatic deletions: REG-ISS-003 complements DL-08 by tracking stage calculation evidence rather than ownership; REG-ISS-004 complements DL-03/09 with eligibility-record evidence; REG-ISS-006 can be reviewed as AT-19 delivery evidence tracking; REG-ISS-007 bundles physical contracts and optional diagram detail; REG-ISS-008 is historical maintenance. REG-ISS-009 and DL-10 remain separate format/retrieval and receipt/timing facets. Keep them all Open pending review.

The [orphan list](audit-ARCH-REG-002/orphan-records.csv) reports records without graph edges. These records still have source locations. Inventory sources, phases without proven assignments and maintenance notes must not receive invented dependencies to eliminate an orphan count. Missing component/supplement endpoints and compressed references were corrected. Unproved phase assignments and detailed bulk mapping relevance remain review work.

## Git, files and preservation

HEAD remains `0a42950d1ce9734433d961540af9ab4be21573b2`. At task start there were 1,203 tracked files, 158 untracked files and no tracked diff. A 1,361-file hash manifest was captured before changes. All original files remain. All 158 initial untracked files remain untracked. DataSet bytes, 002 and 003 remain unchanged.

Only two tracked files change: 001 and 004, only in S01 provenance metadata. See [baseline-tracked.diff](audit-ARCH-REG-002/baseline-tracked.diff). Modified existing Registry files are README, open-issues-registry, source-inventory, traceability-matrix, extraction-summary, validation-report and the two historical build/check scripts. The old scripts now stop before regenerating the audited Registry. Existing historical validation-results, preflight, baseline-comparison and untracked dependency evidence remain unchanged.

The new semantic report and supporting audit files are inside this Registry folder. [changed-files.csv](audit-ARCH-REG-002/changed-files.csv) lists modified initial files with before/after hashes. The [final file manifest](audit-ARCH-REG-002/final-file-manifest.csv) includes new audit files separately, with a stated exclusion for its own self-referential hash. All 141 untracked source files that predate the Registry remain byte-identical. Git status is retained in the machine results. Git warns that its global ignore file is not readable; the local status/diff commands succeed.

No source dataset, prior audit, DSL, original ADR/DL/AT section, ID or filename was changed. Nothing is staged. No implementation, rename, commit or push was performed.

## Remaining approval blockers

Team review must still assess inferred bulk mappings and risk-control links, record the unresolved source/architecture answers, and supply product evidence for planned ATs. Historical S01 content comparison remains pending. The missing raw dictionary, source closure contract, official evaluation profile/hardware and product results remain source/evidence gaps. Optional model detail and historical documentation maintenance must not be mistaken for new product requirements.

Use [validate_semantic_audit.py](audit-ARCH-REG-002/validate_semantic_audit.py) for current documentation checks. Automated checks support the draft. They do not approve it.
