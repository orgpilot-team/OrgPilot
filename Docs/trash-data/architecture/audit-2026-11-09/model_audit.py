"""Inspect existing DSL text. This is not a Structurizr parser or renderer."""
from audit_support import ROOT, OUT, read, finding, write
import csv
import hashlib
import json
import re

path = 'architecture/structurizr/workspace.dsl'
text = read(path)
lines = text.splitlines()
view_start = next(i for i, line in enumerate(lines) if line.strip() == 'views {')
elements = []
relationships = []
views = []
for i, line in enumerate(lines, 1):
    m = re.match(r'\s*(\w+) = (person|softwareSystem|container|component|element) "([^"]+)"', line)
    if m:
        elements.append(dict(identifier=m[1], kind=m[2], name=m[3], source_line=i))
    m = re.match(r'\s*(\w+) -> (\w+) "([^"]+)"', line)
    if m and i <= view_start:
        relationships.append(dict(source=m[1], target=m[2], meaning=m[3], source_line=i))
    m = re.match(r'\s*(systemContext|container|component|dynamic) (\w+) (\w+) "([^"]+)"', line)
    if m:
        views.append(dict(key=m[3], kind=m[1], scope=m[2], description=m[4], source_line=i))
    m = re.match(r'\s*custom (\w+) "([^"]+)" "([^"]+)"', line)
    if m:
        views.append(dict(key=m[1], kind='custom', scope='logical summaries', description=m[3], source_line=i))
ids = {r['identifier'] for r in elements}
assert len(ids) == len(elements)
assert len({r['key'] for r in views}) == len(views)
assert all(r['source'] in ids and r['target'] in ids for r in relationships)
for name, records in [('structurizr-elements.csv', elements), ('structurizr-relationships.csv', relationships), ('structurizr-views.csv', views)]:
    with (OUT / name).open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader(); writer.writerows(records)

finding(56, path, 'A separate original 17-question record was not found',
        'Stale source/authority notes', 'Medium',
        'The original review record now exists at docs/architecture/sources/Adr.md; Markdown brief exists beside PDF. Documents have mixed explicit statuses.',
        'Later update source notes to actual locations and explicit authority. Preserve accepted boundaries and all existing model work.',
        'No DSL edit is authorized in this task.', 'Deferred to model phase')
finding(57, path, 'all 15 view keys are retained', 'Incorrect view inventory', 'Low',
        f'Actual DSL declarations contain {len(views)} distinct view keys, including IntegratedOverview.',
        'Correct the stale count in the later model phase. Do not remove or rename a view to match the comment.',
        'No parser/render validation is implied.', 'Deferred to model phase')
finding(58, 'docs/architecture/001-system-blueprint.md', '`cause_confidence`',
        'Incomplete confidence-to-number boundary', 'High',
        'Brief pp.9,16; brief_schema.json causes.confidence is optional numeric 0..1; DSL F01 requires an approved registered-query scoring path.',
        'Use qualitative confidence until an approved numeric scoring definition has a registered-query result. Do not let the model invent a number.',
        'Scoring definition and wire mapping remain Open under ADR-09/DL-18.')
p = 'docs/architecture/001-system-blueprint.md'
s = read(p)
needle = '### ۸.۱.'
pos = s.index(needle)
s = s[:pos] + '''### Confidence and numerical claims

`Requirement`: communicate confidence and alternatives, and trace each numerical claim to a registered executed query. The existing DSL F01 keeps this boundary for confidence, capacity, baselines, cost, and estimated effect. `Proposed`: use qualitative cause confidence until an approved scoring definition and registered-query result exist. A model-generated 0-to-1 number is not execution evidence or a calibrated probability.

The output schema permits an optional numeric `causes[].confidence` between 0 and 1. It does not require a fabricated score. If confidence is qualitative, retain it in permitted report text while the exact internal/wire mapping is reviewed. Do not emit a string in the numeric property. See ADR-09, DL-18, AT-10, and AT-30.

''' + s[pos:]
write(p, s)

gaps = [
 ('SG-01', 'Revise later', 'Source authority and inventory comments', 'S01/S18/S19; AUD-056/057', 'All existing elements and all declared views', 'Update the missing-review-source assertion, the all-Proposed documentation description, and the stale 15-view count. Keep official requirements distinct from team choices and recommendations.'),
 ('SG-02', 'Add detail later', 'R1-R8 and three control points', 'REQ-R1 through REQ-R8; AT-24; document 001 section 7.1', 'signals, reportWriter, outputValidator; DeterministicAnalytics, NightlyData, NightlyBrief', 'Existing notes already name every rule. Add trace IDs and explicit fixed comparisons/unknown cases to focused detail. No separate rules runtime service is needed.'),
 ('SG-03', 'Add detail later', 'All 12 Workflow stages', 'REQ-WF-*; AT-25; workflow-contracts.csv', 'workflows, kpi; DeterministicAnalytics, NightlyData', 'Keep M01 end-to-end ownership. Show numeric SLA versus promised_by deadline, blank follow-up SLA, median targets, and WF2/WF3 KPI differences. Stage owners stay Open.'),
 ('SG-04', 'Visualization gap', 'Logical entity relationships', 'document 002 section 2; Proposed physical contracts', 'postgres, snapshots, quality; Containers, DataIntake', 'No existing view is an entity ERD. Propose a later Structurizr custom detail view or equivalent approved data-model documentation. Do not invent a current key, FK or cardinality. A missing-source incident has no mandatory SourceFile.'),
 ('SG-05', 'Visualization gap', 'Number-to-source-row lineage', 'REQ-02/REQ-05; kpi-contracts.csv; AT-02/10', 'kpi, queryGateway, evidence, audit, rawFiles; EvidenceAndAnalysis, ReportDelivery', 'Existing views show responsibility paths, not row-level value lineage. Add later detail for result/query/context/contributors/file receipt. Do not convert execution dependencies into visibility grants.'),
 ('SG-06', 'Refine only after policy', 'Shared-resource access and privacy', 'DL-06/07/17; access matrix; AT-06/30', 'access, queryGateway, evidence, insights; EvidenceAndAnalysis, InteractiveAssistant', 'Preserve current RLS/identity boundary. Exact row/column predicates, redaction, NULL-dimension mapping and small-group capacity rules remain Open. Do not add a grant to make a diagram complete.'),
 ('SG-07', 'Preserve; label unresolved detail', 'Report content, chart and state mapping', 'REQ-OUT-*; DL-11/18; AT-26/30', 'insights, reportWriter, outputValidator, publication; ReportDelivery, NightlyBrief', 'The model already submits charts/cards and uses shared Insight. Attach complete content/field trace IDs. suppressed/ongoing and internal schema remain Open. Atomic package mechanics are Proposed, independent outcomes Accepted.'),
 ('SG-08', 'Preserve; refine later', 'Failure and parent execution control', 'Accepted independent publication; DL-13/14; AT-21/28', 'requests, agent, modelGateway, jobs, publication, audit; PartialPublication', 'Preserve pre-draft failure propagation, cancellation, bounded repair, and incomplete day. Do not add guaranteed fallback success or reset parent limits. Exact limits/status export stay Open.'),
 ('SG-09', 'Preserve; no engine change', 'Canonical SQL and KPI lifecycle', 'REQ-KPI-*; DL-01/02/19; AT-02/27', 'managerConfig, kpi, worker, audit; ManagerGovernance, NightlyData', 'Preserve inactive-candidate validation and approval path and the single PostgreSQL product engine. Native SQL equivalence, types and RAW/DEDUP acceptance need proof. A reference oracle is test infrastructure, not another product container.'),
 ('SG-10', 'Preserve; clarify later', 'Upload readiness and source formats', 'REQ-INPUT-*; DL-10/19; AT-22/29', 'documents, ingestion, quality, worker, queryGateway; ManagerUpload', 'Preserve separate document and structured-data revisions. State actual CSV config/JSON manifest formats more precisely if needed. Excel format scope remains Open. Pending/failed rows never become evidence.'),
 ('SG-11', 'Preserve; refine only after policy', 'Human decision and actual execution truth', 'REQ-11; DL-12; AT-14/29', 'decisions, agent, audit; HumanDecisionFollowUp', 'Keep existing human-reported status path and no outbound action connector. Clarify confirmation evidence/fields without implying the system performs transfers or sends drafts.'),
 ('SG-12', 'Preserve; no invented schema', 'Evaluation export and cost/status evidence', 'DL-13/16; AT-15/17/18/30', 'publication, audit, modelGateway; ReportDelivery, PartialPublication', 'Existing export ownership is correct. Precise cost/status filenames and schema remain unprovided. Do not invent links or claim official evaluation from a valid schema.'),
 ('SG-13', 'Visualization gap', 'Dated organization hierarchy and grants', 'REQ-03/08/09; S05; DL-06/10', 'access, managerConfig; SystemContext, Interfaces, ManagerGovernance', 'Existing views show three role classes, not every dated unit/team/manager/staff grant. Add an appropriate later detail only after timing/historical-scope policy. Do not draw all 11 managers as active for every day.'),
 ('SG-14', 'Documentation tooling follow-up', 'Retired diagram generator', 'User visualization standard; legacy visualizations/build_documentation.py', 'No runtime component change', 'Do not run the old generator over active documentation. It still targets retired output. Later retire or adapt tooling without rebuilding or restructuring the existing Structurizr workspace.')
]

report = '''# Structurizr gap report

This report proposes later model work. It does not edit the DSL, replace views, add runtime elements, run a parser, or render a diagram.

The baseline is [workspace.dsl](../../../architecture/structurizr/workspace.dsl). Its identifiers are flat. Implicit relationships are disabled. It has one default SystemContext view, existing focused static/dynamic views, a ten-summary IntegratedOverview, and retained styles/layout directives. No associated architecture README, included DSL file, hosted-view URL, or exported view artifact was found under `architecture/`.

The text inventory is not a Structurizr syntax or layout validation. Source declarations and relationship endpoints were checked. Preserve every existing element, relationship, view key, include/exclude selection, style, and target process boundary until a later scoped change is approved.

'''
report += f"Observed inventory: {len(elements)} elements, {len(relationships)} model relationships, and {len(views)} distinct view declarations. The source comment saying 15 views is stale. The [element](structurizr-elements.csv), [relationship](structurizr-relationships.csv), and [view](structurizr-views.csv) catalogs retain exact source lines.\n\n"
report += '| Existing key | Kind / scope | DSL line | Existing purpose |\n|---|---|---|---|\n'
for v in views:
    report += f"| `{v['key']}` | {v['kind']} / `{v['scope']}` | {v['source_line']} | {v['description']} |\n"
report += '\n## Requirement-to-model review\n\nAll changes below are Proposed future work. Preserve means the target already expresses the boundary; it does not mean implemented or tested. Visualization gaps do not authorize new business rules.\n\n'
report += '| Gap ID / action | Requirement or corrected contract | Existing elements/views to preserve | Proposed later change |\n|---|---|---|---|\n'
for key, action, topic, source, existing, proposed in gaps:
    report += f'| {key} / {action} | {topic}; {source} | {existing} | {proposed} |\n'
report += '''
## Next model phase

First review these proposed changes against the corrected documentation and central Decision Log. Make small changes to existing properties or focused views where sufficient. Do not rename keys or replace the workspace to fit a new drawing. Add a view only when the stated information is absent. Validate DSL syntax and inspect rendered layout in that later phase. No model modification is authorized by this audit.
'''
(OUT / 'structurizr-gap-report.md').write_text(report, encoding='utf-8', newline='\n')
(OUT / 'structurizr-inventory.json').write_text(json.dumps(dict(elements=elements, relationships=relationships, views=views,
    source_sha256=hashlib.sha256((ROOT/path).read_bytes()).hexdigest(), parser_run=False, renderer_run=False), indent=2), encoding='utf-8')
print(json.dumps(dict(elements=len(elements), model_relationships=len(relationships), view_keys=len(views), model_modified=False)))
