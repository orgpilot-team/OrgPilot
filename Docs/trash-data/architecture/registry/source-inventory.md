# Source inventory

State: **Draft / Pending Review**.

S01-S19 keep the IDs from document 001. Each listed member exists locally. Availability does not prove approval or a product test result. Directory sources retain their scope; they are not single-file contracts.

| Source | Actual local members | Authority / limits | Tracking at preflight |
|---|---|---|---|
| S01 | [بریف پروژه بوتکمپ _ دستیار ایجنتیک مدیران سازمانی _ دیدراه.pdf](../../%D8%A8%D8%B1%DB%8C%D9%81%20%D9%BE%D8%B1%D9%88%DA%98%D9%87%20%D8%A8%D9%88%D8%AA%DA%A9%D9%85%D9%BE%20_%20%D8%AF%D8%B3%D8%AA%DB%8C%D8%A7%D8%B1%20%D8%A7%DB%8C%D8%AC%D9%86%D8%AA%DB%8C%DA%A9%20%D9%85%D8%AF%DB%8C%D8%B1%D8%A7%D9%86%20%D8%B3%D8%A7%D8%B2%D9%85%D8%A7%D9%86%DB%8C%20_%20%D8%AF%DB%8C%D8%AF%D8%B1%D8%A7%D9%87.pdf) | Official requirement source; preserve its exact contract. Current official source confirmed by the user in ARCH-REG-002; SHA-256 `f6761b4fc37145d152f2b9793b298e35f48db666d5205c4d02be0f5f13e4863b`. Prior recorded SHA-256 `6d68d3fcc285f6908af0d97c0429dfefb489f00b7f6538ed03573552ed6955f8` is historical. Historical content comparison remains REG-ISS-010; no requirement change is established. | Tracked |
| S02 | [README_FA.md](../../../DataSet/arka_dataset/README_FA.md) | Official requirement source; preserve its exact contract. | Tracked |
| S03 | [kpi_dictionary.csv](../../../DataSet/arka_dataset/config/kpi_dictionary.csv) | Official requirement source; preserve its exact contract. | Tracked |
| S04 | [reference_views.sql](../../../DataSet/arka_dataset/config/reference_views.sql) | Official requirement source; preserve its exact contract. | Tracked |
| S05 | [org](../../../DataSet/arka_dataset/org); [access_matrix.csv](../../../DataSet/arka_dataset/org/access_matrix.csv) | Official requirement source; preserve its exact contract. | Directory; inspect preflight inventory; Tracked |
| S06 | [brief_schema.json](../../../DataSet/arka_dataset/output_contract/brief_schema.json); [qa_answer_schema.json](../../../DataSet/arka_dataset/output_contract/qa_answer_schema.json); [example_brief.json](../../../DataSet/arka_dataset/output_contract/example_brief.json) | Official requirement source; preserve its exact contract. | Tracked; Tracked; Tracked |
| S07 | [scripted_inputs.json](../../../DataSet/arka_dataset/manager_inputs/scripted_inputs.json); [uploads](../../../DataSet/arka_dataset/uploads) | Official requirement source; preserve its exact contract. | Tracked; Directory; inspect preflight inventory |
| S08 | [rca-001-report.md](../../review/rca-001-report.md); [rca-001-evidence.json](../../review/rca-001-evidence.json) | Historical audit Observation; no product acceptance claim. | Untracked; Untracked |
| S09 | [kpi-val-001-report.md](../../review/kpi-val-001-report.md); [kpi-val-001-evidence.json](../../review/kpi-val-001-evidence.json); [kpi-val-001-results.csv](../../review/kpi-val-001-results.csv) | Historical audit Observation; no product acceptance claim. | Untracked; Untracked; Untracked |
| S10 | [dq-001-report.md](../../review/dq-001-report.md); [dq-001-evidence.json](../../review/dq-001-evidence.json); [dq-001-kpi-impact.csv](../../review/dq-001-kpi-impact.csv) | Historical audit Observation; no product acceptance claim. | Untracked; Untracked; Untracked |
| S11 | [escalation_rules.csv](../../../DataSet/arka_dataset/config/escalation_rules.csv); [workflow_definitions.csv](../../../DataSet/arka_dataset/config/workflow_definitions.csv); [monthly_targets.csv](../../../DataSet/arka_dataset/config/monthly_targets.csv) | Official requirement source; preserve its exact contract. | Tracked; Tracked; Tracked |
| S12 | [calendar_days.csv](../../../DataSet/arka_dataset/calendar/calendar_days.csv); [events_calendar.csv](../../../DataSet/arka_dataset/calendar/events_calendar.csv) | Official requirement source; preserve its exact contract. | Tracked; Tracked |
| S13 | [history](../../../DataSet/arka_dataset/history) | Supplied historical/source data. Preserve source facts; old report definitions are not current KPI contracts. | Directory; inspect preflight inventory |
| S14 | [drops](../../../DataSet/arka_dataset/drops) | Supplied historical/source data. Preserve source facts; old report definitions are not current KPI contracts. | Directory; inspect preflight inventory |
| S15 | [DATA_MAP_FA.md](../../review/exploration/DATA_MAP_FA.md); [exploration](../../review/exploration) | Historical audit Observation; no product acceptance claim. | Untracked; Directory; inspect preflight inventory |
| S16 | [Adr.md](../sources/Adr.md) | Recorded Q01-Q17 review. The result table and body have statement-level authority. | Untracked |
| S17 | [workspace.dsl](../../../architecture/structurizr/workspace.dsl) | Existing target model. A proposal or component declaration alone is not team approval. | Untracked |
| S18 | [دیدراه-بریف-دستیار-ایجنتیک-مدیران.md](../../%D8%AF%DB%8C%D8%AF%D8%B1%D8%A7%D9%87-%D8%A8%D8%B1%DB%8C%D9%81-%D8%AF%D8%B3%D8%AA%DB%8C%D8%A7%D8%B1-%D8%A7%DB%8C%D8%AC%D9%86%D8%AA%DB%8C%DA%A9-%D9%85%D8%AF%DB%8C%D8%B1%D8%A7%D9%86.md) | Markdown conversion beside the official brief; retain PDF page references. | Untracked |
| S19 | [request.txt](../audit-2026-11-09/request.txt) | Prior audit request: explicit confirmation of five Accepted boundaries. | Untracked |

## Missing evidence

The four architecture documents explicitly report these gaps:
- Complete official raw-column dictionary and valid missing type/empty-value contracts: DL-01 and DL-16.
- Source-interval closure contract and qualified-publication answer: DL-03.
- Hidden labels, final evaluator profile and reference hardware: DL-16.
- Original decision approver names and approval dates: not supplied. S16/S19 still support the Accepted baseline.
- Actual product execution receipts for AT-01 through AT-30: not supplied.
- Inspectable evidence for the earlier claim of about 70 KPI outputs: REG-ISS-005.
- Historical PDF content-comparison evidence: REG-ISS-010. Current S01 identification is resolved by user confirmation.

The original Desktop review path is not needed for a missing-source guess. Its local S16 copy is present. Document 004 records the expected SHA-256. This extraction checks that local hash.

## Existing reference records

The ADRs, Decision Log and ATs remain in document 003. The Q review stays in S16. The prior audit traceability CSV, acceptance basis, KPI/rule/workflow/schema contracts and VQ register remain supporting evidence. This Registry is a draft extraction index. It does not establish a second approved decision source.

Several audit rows use former `Project_berif/`, `dataset/` or lowercase `docs/` paths. The matrix cites the existing audit CSV row and retains the original location in source_ref. Actual source members above use current local paths. Existing links are not changed.
