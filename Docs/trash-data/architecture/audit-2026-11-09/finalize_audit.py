"""Build the file change report and a diff from the verified pre-edit backup."""
from pathlib import Path
import csv
import difflib
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
PREFIX = OUT.relative_to(ROOT).as_posix() + '/'
base = json.loads((OUT/'pre-edit-manifest.json').read_text(encoding='utf-8'))
derived = {'reconciliation.diff', 'file-changes.csv', 'diff-summary.json'}
purposes = {
    'README.md': 'Audit index, evidence limits, and check command.',
    'audit-report.md': 'Full issue records, source evidence, corrections, and limits.',
    'audit-summary.json': 'Finding counts and document review unit counts.',
    'findings.csv': 'Full findings in table form; original claims and pre-edit locations.',
    'findings.json': 'Structured findings; includes the retained source observation.',
    'document-review-ledger.csv': 'All 911 pre-edit review units, source context, and dispositions.',
    'requirements-traceability.csv': '339 granular source-to-component, ADR, and gate records.',
    'requirements-traceability.md': 'Traceability scope, coverage, and remaining evidence gaps.',
    'traceability-summary.json': 'Traceability counts by source and classification.',
    'rule-contracts.csv': 'Exact R1-R8 source text and rule-specific behavior.',
    'kpi-contracts.csv': 'All 55 source definitions, SQL hashes, and calculation semantics.',
    'workflow-contracts.csv': 'All 12 source stages, clocks, deadlines, and ownership gaps.',
    'manager-input-contracts.csv': 'All 23 supplied inputs, effects, timing, and access limits.',
    'output-schema-contracts.csv': 'Exact property constraints and status enums from both schemas.',
    'acceptance-basis.csv': 'Requirement or decision basis for all 30 planned gates.',
    'source-checks.json': 'Read-only manifests, headers, row counts, calendar, and source fixtures.',
    'brief-content-check.json': 'PDF content checks; a resaved hash does not imply changed requirements.',
    'structurizr-gap-report.md': '14 proposed model follow-ups with existing element and view mappings.',
    'structurizr-elements.csv': '46 existing model elements with source locations.',
    'structurizr-relationships.csv': '127 existing model relationships with source locations.',
    'structurizr-views.csv': '16 existing view declarations with exact keys and locations.',
    'structurizr-inventory.json': 'Model text inventory and protected DSL hash.',
    'pre-edit-manifest.json': 'SHA-256 baseline for all 1,452 initial workspace files.',
    'pre-edit.zip': 'Verified backup of all 79 pre-existing architecture and model files.',
    'request.txt': 'Verbatim task supplied by the user.',
    'change-report.md': 'File-by-file changes, checks, and implementation blockers.',
    'reconciliation.diff': 'Current unified text diff and binary backup notice.',
    'file-changes.csv': 'Complete file index with change kind, purpose, and line counts.',
    'diff-summary.json': 'Diff scope, line counts, exclusions, and SHA-256.',
    'verification.json': 'Results of documentation checks; no product acceptance asserted.',
    'verify_audit.py': 'Repeatable standard-library documentation and source checks.',
    'audit_support.py': 'Documentation authoring helpers and duplicate-finding guards.',
    'phase1.py': 'Source-backed changes to document 001.',
    'phase2.py': 'Source-backed changes to document 002.',
    'phase3.py': 'Source-backed changes to document 003.',
    'phase4.py': 'Source-backed changes to document 004 and dependent documentation.',
    'cross_document_fixes.py': 'Cross-document contract and reference corrections.',
    'source_audit.py': 'Read-only source extraction and fixture checks.',
    'build_traceability.py': 'Build source contracts and the traceability matrix.',
    'model_audit.py': 'Read-only model inventory and proposed gap report.',
    'build_audit_report.py': 'Build findings tables, detailed report, and review-unit ledger.',
    'finalize_audit.py': 'Build this report and the backup-based diff; does not restore files.',
}
existing_purposes = {
    '001-system-blueprint.md': 'Complete R1-R8 and Workflow contracts; report content; source authority; parent execution and input contracts; Proposed mechanisms; Structurizr references.',
    '002-data-architecture.md': 'Source grains and clocks; exact reference-view semantics; Proposed internal entities; privacy, priority, and output mapping; preserve the KPI catalog.',
    '003-decisions-and-roadmap.md': 'Preserve ADR-01 through ADR-17; add AT-24 through AT-30; keep every gate planned; expand the Decision Log to 19 source-backed Open rows.',
    '004-reconciliation-review.md': 'Keep the Q01-Q17 mapping and stable anchors; reconcile evidence status, gates, independent publication, and current audit links.',
    'visualizations/README.md': 'Use the 16 actual Structurizr view keys; state missing views; retire legacy preview navigation.',
    'visualizations/open-questions.md': 'Preserve VQ identifiers and unresolved policy; align status and Decision Log references.',
    'visualizations/proposed-entity-contracts.md': 'Align Proposed entity contracts with document 002; do not claim an existing ERD.',
    'visualizations/security-examples.md': 'Keep useful examples; state evidence and approval limits.',
}

with zipfile.ZipFile(OUT/'pre-edit.zip') as archive:
    originals = {name: archive.read(name) for name in archive.namelist()}
for name, data in originals.items():
    assert hashlib.sha256(data).hexdigest() == base[name], name
changed = sorted(name for name, digest in base.items()
                 if hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != digest)
assert len(changed) == 34
assert all(name in originals and name.startswith('docs/architecture/') for name in changed)
for name in derived:
    (OUT/name).touch(exist_ok=True)
new = sorted(p.name for p in OUT.iterdir() if p.is_file())
assert set(new) == set(purposes), (set(new)-set(purposes), set(purposes)-set(new))

report = '''# File change report

The audit corrects the documentation and preserves the five accepted architecture boundaries. It does not implement the product. It records 58 material findings: 56 document corrections and two deferred model comment changes. One further record confirms source counts that were already correct.

No Git repository exists at the project root or in its parent directories. `git status --short` returned that error. The comparison therefore uses the verified [pre-edit ZIP](pre-edit.zip) and [baseline manifest](pre-edit-manifest.json). No commit or push was attempted.

## Changed existing files

All 34 changed existing files are Markdown under `docs/architecture/`. No original file was deleted. Original content is available in the backup. The 26 preview files now contain short retirement notices. This removes active Mermaid architecture references while preserving the original raw diagrams and generators for history.

| Existing file | Change |
|---|---|
'''
for name in changed:
    short = name.removeprefix('docs/architecture/')
    purpose = existing_purposes.get(short)
    if purpose is None:
        assert short.startswith('visualizations/previews/')
        purpose = 'Retire the active legacy preview; refer to actual Structurizr views and explicit visualization gaps. The backup preserves the old preview.'
    report += f'| [{short}](../{short}) | {purpose} |\n'
report += '''
## Added audit files

Each file below belongs to this audit folder. The Python files support documentation checks and authoring. They do not implement product behavior. Do not rerun authoring phases over the corrected documents. Use the check command in [README](README.md).

| Added file | Purpose |
|---|---|
'''
for name in new:
    report += f'| [{name}]({name}) | {purposes[name]} |\n'
report += '''
## Checks and limits

The [verification record](verification.json) gives the final check results. It checks the pre-edit ZIP against its manifest, all original file hashes, the unchanged 55-KPI summary and source SQL, stable identifiers, local links and anchors, all eight rule source texts, all 12 Workflow stages, all 23 manager inputs, schema constraints, and the traceability references. The source checks compare all 91 manifests with delivered files and counts. The model text inventory covers 46 elements, 127 relationships, and 16 views.

The 339-row matrix records source meaning as well as counts. Dedicated tables preserve formula populations, clocks, NULL behavior, rule comparisons, Workflow deadlines, manager timing, and exact schema enums. The review ledger covers 911 units in the four original documents. Its inherited section context is not independent proof of each sentence. Source checks and links do not establish product correctness.

All 1,193 original dataset files remain unchanged. The brief, Markdown brief, recorded discussion, source contracts, reference SQL, KPI dictionary, previous review files, raw diagrams, and Structurizr DSL remain unchanged. There are 1,418 unchanged original files and 34 changed existing Markdown files. New audit artifacts are listed above. The previous root reconciliation diff remains unchanged and historical.

No KPI SQL, PostgreSQL equivalence check, model call, product test, restore test, official evaluation, Structurizr parser, or Structurizr renderer was run. All 30 product acceptance gates remain planned. Two DSL comment corrections are deferred with the other proposed model work. See [model gaps](structurizr-gap-report.md).

## Decisions that still constrain implementation

The [Decision Log](../003-decisions-and-roadmap.md#decision-log) records exact evidence, proposed owner roles, options, effects, and closure gates. The roles need team assignment. This report does not invent named owners or approved answers.

| Open matter | Required decision or evidence | Implementation effect |
|---|---|---|
| DL-01, DL-02: canonical calculation | Approve source types, PostgreSQL translation and equivalence evidence, and RAW versus exact-payload DEDUP policy. | Blocks release of canonical calculations. PostgreSQL remains the only product engine. |
| DL-03, DL-05: source closure and corrections | Define eligible current values, source precedence, and correction ties. | Blocks affected value release. A prior valid report cannot fill a current value slot. |
| DL-04: recalculation and restatement | Review full rebuild versus selective work and notification/approval. | Blocks a final correction/replay contract; selective work needs equivalence proof. |
| DL-06, DL-07, DL-19: authority and privacy | Approve row/column/purpose projections, capacity formula, small-group rules, write authority, and candidate activation. | Blocks access to undefined shared resources and governed configuration writes. Read access does not imply write access. |
| DL-08, DL-09: routing and rules | Approve stage owners and genuinely unspecified rule edges, including R3 missing warn, R4 reference/reset, and sparse or zero baselines. | Blocks final affected signal/routing behavior. Preserve all fixed source rule clauses. |
| DL-10: dated organization and uploads | Resolve M11 start timing and record upload receipt/readiness and event knowledge time. | Blocks exact replay coverage and attachment eligibility. Do not select 316 or 317 reports without authority. |
| DL-11, DL-17, DL-18: report and output mapping | Resolve suppressed/ongoing, number/query identifiers, NULL dimensions, and required chart/card/content mapping. | Blocks the final internal and wire contracts. A permissive schema does not remove required content. |
| DL-12: decision and execution records | Define human confirmation and execution evidence. | Blocks claims about completed organizational action. Human control remains Accepted. |
| DL-13, DL-14: bounded execution and failure | Select limits, model/provider, retries, failure export, and any validated fallback. | Blocks runtime limit and failure contracts. Independent valid-report publication remains Accepted. |
| DL-15: retention and restore | Approve retention, audit readers, backup interval, and restore procedure. | Blocks final operations readiness. Retain replay evidence in the meantime. |
| DL-16: official evaluation inputs | Obtain the organizer profile, reference hardware, hidden labels, and missing raw-column dictionary or an approved missing-contract disposition. | Blocks final acceptance claims. It does not prohibit all independent engineering preparation. |

These gaps do not reopen the one-Agent, PostgreSQL, deterministic controls, independent publication, or human-control decisions. They block affected implementation contracts or final acceptance; they are not a claim that all engineering work must stop. Product implementation was outside this task.

## Diff

The [unified diff](reconciliation.diff) compares each changed original with verified backup bytes. It also includes all new text artifacts except itself and the two derived change-index files. The ZIP is a separate binary addition. The [file index](file-changes.csv) lists every changed or added file. The [diff summary](diff-summary.json) records line counts, exclusions, and the diff hash. Line endings in text comparisons are normalized to LF; the baseline hashes preserve the exact original bytes.
'''
(OUT/'change-report.md').write_text(report, encoding='utf-8', newline='\n')

chunks = []
rows = []
totals = {'added_lines': 0, 'removed_lines': 0, 'text_files_in_diff': 0}
for name in changed + [PREFIX+n for n in new]:
    added = name not in base
    p = ROOT/name
    old = b'' if added else originals[name]
    current = p.read_bytes()
    excluded = added and p.name in derived
    binary = p.suffix == '.zip'
    plus = minus = 0
    if not excluded and not binary:
        before = old.decode('utf-8-sig').splitlines(keepends=True)
        after = current.decode('utf-8-sig').splitlines(keepends=True)
        before = [line.replace('\r\n', '\n') for line in before]
        after = [line.replace('\r\n', '\n') for line in after]
        diff = list(difflib.unified_diff(before, after,
                    fromfile='/dev/null' if added else 'a/'+name, tofile='b/'+name))
        plus = sum(line.startswith('+') and not line.startswith('+++') for line in diff)
        minus = sum(line.startswith('-') and not line.startswith('---') for line in diff)
        for line in diff:
            chunks.append(line if line.endswith('\n') else line+'\n\\ No newline at end of file\n')
        totals['added_lines'] += plus
        totals['removed_lines'] += minus
        totals['text_files_in_diff'] += 1
    elif binary:
        chunks.append(f'Binary files /dev/null and b/{name} differ\n')
    short = name.removeprefix('docs/architecture/')
    purpose = purposes[p.name] if added else existing_purposes.get(short, 'Retire legacy preview; preserve original in the backup.')
    rows.append(dict(path=name, change='Added' if added else 'Modified', purpose=purpose,
                     diff_scope='Derived index; excluded' if excluded else 'Binary notice' if binary else 'Unified text',
                     added_lines='' if excluded or binary else plus, removed_lines='' if excluded or binary else minus))
diff_bytes = ''.join(chunks).encode('utf-8')
(OUT/'reconciliation.diff').write_bytes(diff_bytes)
with (OUT/'file-changes.csv').open('w', encoding='utf-8-sig', newline='') as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
summary = dict(modified_existing_files=len(changed), added_audit_files=len(new),
               deleted_original_files=0, **totals, diff_bytes=len(diff_bytes),
               diff_sha256=hashlib.sha256(diff_bytes).hexdigest(), binary_additions=['pre-edit.zip'],
               excluded_derived_files=sorted(derived), comparison='Verified pre-edit ZIP; LF-normalized text',
               git_available=False, commit_or_push_attempted=False)
(OUT/'diff-summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2))
