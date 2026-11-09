from audit_support import ROOT, OUT, read, write, finding
import re
import shutil

doc = 'docs/architecture/004-reconciliation-review.md'
t = read(doc)
items = [
 (43, 'three architecture documents', 'Stale audit scope', 'Medium', 'Current request requires sequential audit of four numbered documents and dependent documentation.', 'Update the review scope, family/document metadata, and source range.'),
 (44, 'Document 001 formerly listed', 'Hash difference treated as a review concern without content difference', 'Medium', 'User confirms PDF highlighting/resave; PDF pp.8,10,15 match the Markdown passages checked.', 'Report content comparison and provenance. Do not classify a source-version requirement conflict.'),
 (45, 'The architecture review is complete', 'Unsupported semantic completion claim', 'High', 'Current source audit finds omitted rules, stage targets, report content, configuration and schema details.', 'Replace broad completion with scoped audit evidence and explicit unresolved gates.'),
 (46, 'All five fenced diagram', 'Obsolete visualization validation criterion', 'Medium', 'User selects Structurizr and prohibits active architecture diagrams in the retired format.', 'Retire active blocks/previews and map existing view keys; record absent views as gaps.'),
 (47, 'The set has 17 ADRs and 23', 'Stale verification result', 'Medium', 'New semantic audit adds planned gates and a reproducible backup. Earlier link counts cannot validate this run.', 'Replace old current-result counters with the new verification report. Preserve historical evidence in the backup.'),
 (48, '| Daily atomic wording', 'Proposed mechanism promoted in conflict disposition', 'High', 'ADR-14 accepts independent publication but marks atomic text/JSON commit Proposed.', 'Keep independent publication Accepted and package commit Proposed; retain incomplete-day coverage.'),
 (49, '| <a id="review-q12"', 'Incomplete question-to-rule coverage', 'High', 'Complete R1-R8 contract and AT-24; all 12 Workflow stages and AT-25.', 'Add the new granular gates/traceability references to affected question rows.'),
 (50, '| [Unified diff]', 'Non-reproducible previous comparison reference', 'Medium', 'Previous pre-edit files were outside the workspace; root diff belongs to the earlier task.', 'Keep the prior root diff historical. Supply a new in-workspace backup, manifest, unified diff, and verification procedure.')
]
for n, needle, cat, severity, source, correction in items:
    finding(n, doc, needle, cat, severity, source, correction,
            'Open architecture/source-contract choices are retained in the central Decision Log.')
finding(51, 'docs/architecture/visualizations/README.md', '| [01-source-data-erd.mmd]',
        'Retired visualization presented as active standard', 'Medium',
        'User section 6; actual Structurizr view declarations.',
        'Replace the active guide with a verified Structurizr view index. Keep old source artifacts as an archive, not active diagrams.')
finding(52, 'docs/architecture/visualizations/proposed-entity-contracts.md', 'All entities in Diagram B',
        'Obsolete diagram dependency and incomplete contracts', 'Medium',
        'Document 002 logical contracts; existing Structurizr has no entity ERD.',
        'Refer to logical contracts and the explicit entity-visualization gap. Preserve Proposed status.')
finding(53, 'docs/architecture/visualizations/open-questions.md', 'UNRESOLVED means Open',
        'Duplicate status vocabulary', 'Low', 'Requirement/Accepted/Proposed/Open convention; Observation is evidence.',
        'Use Open/Proposed in the active register. Keep VQ identifiers and source restrictions.')
finding(54, 'docs/architecture/visualizations/previews/01-source-data-erd.md', '```mermaid',
        'Active legacy preview family', 'Medium', 'All 26 previews use the retired diagram syntax; user section 6.',
        'Retire all 26 rendered previews. Point to verified Structurizr scope views and actual missing-view gaps. Preserve the raw historical files and pre-edit ZIP.')
finding(55, 'docs/architecture/visualizations/security-examples.md', 'CONFIRMED:',
        'Evidence labels can imply architecture approval', 'Low', 'Source access matrix and brief restrictions; candidate physical projections are not Accepted.',
        'Add the active status/evidence legend and link the central policy decisions. Keep correct examples.')

shutil.copyfile(
    'C:/Users/ashkriz/.codex/attachments/58b7ea88-7165-4839-afc6-66c14136597b/Pasted text.txt',
    OUT / 'request.txt')

t = t.replace('# ARKA architecture reconciliation', '# ARKA architecture reconciliation\n\nDocument key: `004-reconciliation-review`. Shared architecture family: `ARCH-001`.')
t = t.replace('the three architecture documents', 'the four numbered architecture documents and dependent documentation')
t = t.replace('for S01-S17', 'for S01-S19')
t = t.replace('The recorded team decisions are one bounded AI Agent, PostgreSQL as the only product database engine, and independent publication of valid manager reports.', 'The Accepted baseline has one bounded AI Agent with deterministic supporting modules, PostgreSQL-only product execution, independent publication of valid manager reports, deterministic KPI/signal/authorization/final-validation boundaries, and human-controlled organizational decisions. The user confirms these boundaries in the current audit request (S19).')
t = t.replace('confirms the three decisions above', 'supports these target boundaries')
a = t.index('Document 001 formerly listed'); b = t.index('\n\n', a)
t = t[:a] + 'S01 was highlighted and resaved. S18 is its Markdown conversion. The current PDF content on pages 8, 10, and 15 was checked visually against the corresponding text. These checks confirm the recurrence controls, required report content, and suppressed-status wording. Pages 13 and 16 were also checked in the earlier review of the same current PDF. No changed requirement was established from the former hash difference. Earlier numerical audits remain attributed historical evidence.' + t[b:]
t = t.replace('The architecture review is complete at the documentation level.', 'This audit corrects the documented omissions found through source comparison. The [audit report](audit-2026-11-09/audit-report.md) and [unit review ledger](audit-2026-11-09/document-review-ledger.csv) state its evidence and limits. Open decisions and unexecuted product gates remain visible.')
t = t.replace('The three Accepted topology decisions do not need to be selected again.', 'The Accepted architecture boundaries do not need to be selected again.')
t = t.replace('Resolve at the package boundary: one manager\'s text/JSON is atomic; manager outcomes are independent.', 'Accepted: manager outcomes are independent. Proposed: commit one manager\'s text/JSON together at a package boundary.')
gate_additions = {'q01':'AT-28', 'q02':'AT-29', 'q03':'AT-27', 'q04':'AT-28',
    'q09':'AT-30', 'q11':'AT-25', 'q12':'AT-24', 'q13':'AT-29',
    'q14':'AT-26, AT-30', 'q15':'AT-29', 'q16':'AT-28', 'q17':'AT-28'}
lines = t.splitlines()
for i, line in enumerate(lines):
    m = re.match(r'^\| <a id="review-(q\d{2})"', line)
    if m and m[1] in gate_additions:
        cells = line.strip('|').split('|')
        cells[-1] = cells[-1].strip() + '; ' + gate_additions[m[1]]
        lines[i] = '| ' + ' | '.join(c.strip() for c in cells) + ' |'
t = '\n'.join(lines) + '\n'
a = t.index('## File changes');b = t.index('<a id="verification">',a)
t = t[:a] + '''## Current audit outputs and file changes

- [Detailed audit report](audit-2026-11-09/audit-report.md): issue IDs, exact pre-edit locations, original claims, evidence, severity, correction status, and remaining uncertainty.
- [Requirement Traceability Matrix](audit-2026-11-09/requirements-traceability.csv): source -> granular requirement -> existing component -> contract/rule -> ADR -> planned acceptance gate.
- [KPI contracts](audit-2026-11-09/kpi-contracts.csv), [Workflow contracts](audit-2026-11-09/workflow-contracts.csv), and [manager-input contracts](audit-2026-11-09/manager-input-contracts.csv): detailed source semantics.
- [Structurizr gap report](audit-2026-11-09/structurizr-gap-report.md): actual elements, relationships, view keys, and proposed later changes. The DSL is unchanged.
- [Change and verification report](audit-2026-11-09/change-report.md): per-file changes, checks, scope limits, and remaining blockers.
- [Current unified diff](audit-2026-11-09/reconciliation.diff), [pre-edit backup](audit-2026-11-09/pre-edit.zip), and [baseline manifest](audit-2026-11-09/pre-edit-manifest.json).

The root `reconciliation.diff` belongs to the previous reconciliation and is retained unchanged. Use the current audit diff above for this task. The source record `sources/Adr.md` is unchanged. No original brief, dataset, SQL, source contract, review report, or Structurizr file was edited.

''' + t[b:]
a = t.index('## Verification record')
t = t[:a] + '''## Verification record

The prior reconciliation used link/count checks. Those results are historical and do not prove semantic correctness of the current baseline. This audit compares source meaning, rule behavior, all canonical metadata, Workflow stages, manager inputs, JSON contracts, and the existing target model. The [current verification result](audit-2026-11-09/verification.json) reports only documentation/source checks that were executed.

All AT gates remain planned. No KPI SQL, PostgreSQL equivalence, product security, replay, model, performance, restore, or cost test was run. No dependency was installed. No architecture diagram renderer was run. Existing Structurizr view keys were checked in the DSL text; no view was invented or rendered.

Git is unavailable in this workspace. The audit uses a verified pre-edit ZIP and source/file hash manifest. No commit or push was attempted. Open decisions, rather than invented answers, remain in the [Decision Log](003-decisions-and-roadmap.md#decision-log).
'''
write(doc, t)

doc1 = 'docs/architecture/001-system-blueprint.md'
s = read(doc1)
pos = s.index('\n\n', s.index('| S18 |'))
s = s[:pos] + '\n| S19 | [Current audit request](audit-2026-11-09/request.txt) | User confirmation of the five Accepted boundaries and documentation-only scope. It is not a new dataset calculation or output contract. |' + s[pos:]
write(doc1, s)

p = 'docs/architecture/visualizations/open-questions.md'
s = read(p).replace('UNRESOLVED means Open. PROPOSED means Proposed. CONFIRMED is a legacy evidence label, not proof of team approval.', 'Use Open and Proposed as decision statuses. Observation is evidence, not approval. The earlier CONFIRMED label never establishes team approval.')
s = s.replace('| UNRESOLVED |','| Open |').replace('| PROPOSED |','| Proposed |')
s += '\nThe active visualization standard is the existing Structurizr workspace. See the [view catalog and gaps](../audit-2026-11-09/structurizr-gap-report.md). No question here authorizes a new grant, engine, or Agent.\n'
write(p, s)
p = 'docs/architecture/visualizations/proposed-entity-contracts.md'
s = read(p).replace('All entities in Diagram B are PROPOSED - NOT IMPLEMENTED.', 'These are Proposed logical entity contracts, not implemented tables. The earlier diagram is retired.')
s += '\nUse [document 002](../002-data-architecture.md#data-2) for the current logical grains and additional internal records. Structurizr has component views, but no detailed entity ERD. That is a [recorded visualization gap](../audit-2026-11-09/structurizr-gap-report.md), not a reason to invent a view or physical FK.\n'
write(p, s)
p = 'docs/architecture/visualizations/security-examples.md'
s = read(p)
pos = s.index('\n\n')
s = s[:pos] + '\n\nStatus note: source restrictions are Requirements. CONFIRMED/DERIVED are legacy evidence labels, not Accepted decisions. Candidate field projections and enforcement remain Proposed; UNRESOLVED means Open. Q IDs here are manager-input questions. See [ADR-06](../003-decisions-and-roadmap.md#adr-06), the [policy log](../003-decisions-and-roadmap.md#decision-log), and the [Structurizr view catalog](../audit-2026-11-09/structurizr-gap-report.md).' + s[pos:]
write(p, s)

README = '''# ARKA architecture views and source evidence

The existing [Structurizr workspace](../../../architecture/structurizr/workspace.dsl) is the architecture visualization baseline. Preserve its identifiers, relationships and views. This documentation audit does not edit or render the model. Read the [view catalog and proposed gaps](../audit-2026-11-09/structurizr-gap-report.md).

| Existing view keys | Use |
|---|---|
| `IntegratedOverview`, `SystemContext`, `Containers` | Overall boundaries, roles, and the existing six-container target. |
| `Interfaces` | The three required Persian RTL interfaces. |
| `DataIntake`, `NightlyData` | Source intake, quality, protected archive, and snapshots. These are not an entity ERD. |
| `DeterministicAnalytics` | KPI, Workflow and signal components. It is not a complete rule decision table. |
| `EvidenceAndAnalysis`, `InteractiveAssistant` | Authorized evidence, controlled SQL and one bounded Agent. |
| `ReportDelivery`, `NightlyReporting`, `NightlyBrief` | Shared analysis, role content, validation and delivery. |
| `ManagerGovernance`, `ManagerUpload`, `HumanDecisionFollowUp` | Authorized settings/KPI lifecycle, upload paths, and human decisions. |
| `PartialPublication` | Independent outcomes and an incomplete day after a required-report failure. |

View keys are verified DSL declarations, not web URLs. No hosted viewer URL was supplied. The gap report gives source lines and exact scope. Detailed entity ERD, source-row lineage, rule/stage decision detail, and organization/access detail are visualization gaps where no matching existing view exists.

## Historical source evidence

The CSV/JSON catalogs in this directory remain useful historical observations: table/column inventory, header variants, candidate relationships, manager scopes, KPI dependencies, and earlier check receipts. Their original counts and SQL-prepare checks are not new audit results. Read [current source checks](../audit-2026-11-09/source-checks.json) and [traceability](../audit-2026-11-09/requirements-traceability.csv) for this run.

Candidate identifier matches are not enforced foreign keys. Execution dependencies are not selected-value lineage, minimum invalidation proofs, or display grants. RAW occurrences can repeat. Event occurrence IDs and customer/campaign parent registries are not supplied. Empty links remain optional until a contract says otherwise.

Source restrictions are Requirements. One bounded Agent, PostgreSQL-only product execution, independent valid-report publication, deterministic controls, and human action authority are Accepted boundaries. Physical keys, indexes, exact resource projections, capacity formulas, retention, and approval schemas remain Proposed or Open. Observation is an evidence category, not approval.

The original 26 raw diagram files remain unchanged as historical material. Their rendered previews are retired. Do not use or regenerate them as architecture views. The old build_documentation.py and its validators target that historical output; they were not run or revised. A later tooling decision must prevent their output from replacing the Structurizr baseline.

Review Q01-Q17 belongs to [S16](../sources/Adr.md). Manager Q01-Q16 belongs to the dataset inputs. VQ01-VQ10 belongs to the [legacy review register](open-questions.md). Keep these namespaces separate. Read the [central Decision Log](../003-decisions-and-roadmap.md#decision-log) for unresolved policies.
'''
write('docs/architecture/visualizations/README.md', README)
for p in (ROOT / 'docs/architecture/visualizations/previews').glob('*.md'):
    name = p.stem
    if name.startswith('06-'):
        views = '`DeterministicAnalytics` and `EvidenceAndAnalysis`'; gap = 'Detailed source-row/value lineage is not an existing view.'
    elif name.startswith('03-'):
        views = '`SystemContext`, `Interfaces`, and `ManagerGovernance`'; gap = 'The full dated organization/access hierarchy is not an existing view.'
    elif name.startswith(('04-', '05-')):
        views = '`EvidenceAndAnalysis`, `InteractiveAssistant`, and `ManagerGovernance`'; gap = 'Exact row/column permission and resource projections remain Open.'
    else:
        views = '`Containers`, `DataIntake`, and `NightlyData`'; gap = 'These component/data-flow views are not a detailed entity ERD.'
    p.write_text(f'''# Retired preview: {name}

Use the existing [Structurizr workspace](../../../../architecture/structurizr/workspace.dsl), views {views}. {gap}

This legacy rendered preview is retired. Its original content is preserved in the [pre-edit backup](../../audit-2026-11-09/pre-edit.zip). The raw historical source is unchanged. Do not treat it as the active architecture standard or an approved physical schema.

Read the [Structurizr gap report](../../audit-2026-11-09/structurizr-gap-report.md) for exact current scope and proposed later work. The model is not edited in this task.
''', encoding='utf-8', newline='\n')
print('Phase 4 complete: document 004 and related documents corrected; AUD-043 through AUD-055 recorded. Retired 26 active legacy previews.')
