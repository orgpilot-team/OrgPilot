# Extraction and validation report

State: **Draft / Pending Review**. Task: `ARCH-REG-001`. Date: 2026-11-09. Time zone: `Asia/Tehran`.

## Result

- ADR coverage: 17/17. Numbered statements: 5 Accepted, 24 Proposed, 24 Open and 16 Requirement.
- Open issue records: 29; 19 original DLs and ten temporary Registry IDs.
- Required work: 25 team decisions, 12 organizer/source clarifications and 29 engineering evidence items. These sets overlap.
- Risks: 20. All severities are Not Assessed. Controls have Evidence Pending.
- AT coverage: 30/30. All Planned / Not Executed. Full supplements, three-level matrix, rule matrix and delivery criteria are retained.
- Duplicate placements attached to main records: 42. The [ledger](deduplication-ledger.md) defines this count and preserves bundled differences.
- Existing requirement IDs indexed: 339. The [CSV](traceability-matrix.csv) has 4191 record/evidence/relationship rows with one target per relationship.

## Missing evidence and remaining conflicts

No main ADR, issue, risk or AT lacks a source location. Product evidence remains pending. Missing contracts include the full raw dictionary and input types, source closure, hidden labels, final organizer profile/hardware, and original decision approver names/dates. The claim of about 70 KPI outputs has no inspectable result. See [source inventory](source-inventory.md).

**S01 provenance discrepancy:** actual PDF SHA-256 is `f6761b4fc37145d152f2b9793b298e35f48db666d5205c4d02be0f5f13e4863b`; 001/004 record `6d68d3fcc285f6908af0d97c0429dfefb489f00b7f6538ed03573552ed6955f8`. The PDF is unchanged from this task's initial inventory. REG-ISS-010 is Open / Evidence Pending. This byte difference does not establish a requirement change. A source-version/content comparison is still required before applying the old visual-review claim to this exact file.

Conflicts remain Open: RAW/DEDUP; closure/release and dated prior values; equal-rank correction precedence; shared-source row/column/purpose grants; capacity/privacy; stage ownership and stage calculation records; Signal equality/baseline/reset; M11 mornings 75/76 and same-day attachment timing; suppressed/ongoing; NULL/no-dimension and extra-number wire mapping; complete Insight/content/history contracts; existing-KPI editing versus fixed reference definitions; P2/P3 scope; failure/retry/fallback/status export; bounded model execution; retention/restore. Registry issues also retain the QA context record, DQ eligibility record, delivery evidence, model detail and stale workspace/tooling context.

No Accepted boundary is reopened. No Proposed mechanism is promoted. Risk-to-record links and extra test links without explicit source IDs are marked Proposed Relationship. Blank phase cells do not imply a phase assignment.

## Documentation checks

Result: **PASS** for this documentation check run. 29/29 checks succeeded. These are document/source checks. They do not pass any AT.

The check compares complete ADR/DL/AT extracts and all original risk rows. It checks active links and source anchors, ID coverage, duplicate identities, one-target relationship rows, actual DSL component IDs, source hashes and Git scope. Exact source text retains the original numbers and exceptions. English index statements and route classes remain draft extraction work that needs team review.

## Git and preservation

HEAD: `0a42950d1ce9734433d961540af9ab4be21573b2`. Baseline: `0a42950d1ce9734433d961540af9ab4be21573b2`.

Initial state: no tracked changes and 141 untracked files. All 1344 initial file hashes remain unchanged. All 141 prior untracked files remain unchanged and untracked. Tracked diff against baseline is empty. New untracked files are confined to `Docs/architecture/registry/`.

Untracked dependencies: 16 direct source files and 7 directory-source members. The [dependency list](untracked-source-dependencies.csv) also lists every other preserved prior untracked file. A later commit must review these sources separately, including S08-S10, S15-S19, the Q review, audit tables and DSL. Nothing is staged here.

The [baseline comparison](baseline-comparison.csv) covers every initial file and every new Registry file, including untracked additions. Self-referential check output files are listed as Added without an embedded self hash; all other new file hashes are recorded. This avoids an impossible self-hash cycle. The final Git check also counts every new file as a whole-file addition against the baseline.

Git warning: the global ignore file is not readable. Local Git status/diff commands succeed. This warning did not remove or alter any source file.

## Next authorized review stage

Review the draft statuses, routes and Proposed Relationships. Then record team/source answers and product evidence. In a later separately authorized content task, decide how to transfer material from 003, update links, correct stale Git/path/DSL count notes and retire/adapt the old generator. Keep stable ADR/DL/AT IDs. Do not move or rename sources before that review. No implementation, commit or push was done.


## ARCH-REG-002 superseding audit note

The results above describe the ARCH-REG-001 extraction snapshot. They do not establish semantic correctness. Read [semantic-audit-report.md](semantic-audit-report.md) for current counts, S01 identity, corrected mappings and remaining review limits. The current S01 identity is confirmed; historical content comparison remains Open. The old validation-results.json and baseline-comparison.csv are retained unchanged as historical evidence.
