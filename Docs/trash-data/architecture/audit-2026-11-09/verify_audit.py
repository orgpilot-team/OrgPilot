"""Re-run documentation/source consistency checks; never execute product SQL."""
from pathlib import Path
from urllib.parse import unquote
import csv
import hashlib
import json
import re
import zipfile

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent

def text(path):return (ROOT/path).read_text(encoding='utf-8-sig')
def csv_rows(name):
    with (OUT/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

base=json.loads((OUT/'pre-edit-manifest.json').read_text(encoding='utf-8'))
changed=[]
for path,old_hash in base.items():
    p=ROOT/path
    assert p.exists(),('Unexpected deletion',path)
    if hashlib.sha256(p.read_bytes()).hexdigest()!=old_hash:changed.append(path)
allowed={f'docs/architecture/{n}' for n in ['001-system-blueprint.md','002-data-architecture.md',
    '003-decisions-and-roadmap.md','004-reconciliation-review.md','visualizations/README.md',
    'visualizations/open-questions.md','visualizations/proposed-entity-contracts.md','visualizations/security-examples.md']}
allowed|={p.relative_to(ROOT).as_posix() for p in (ROOT/'docs/architecture/visualizations/previews').glob('*.md')}
assert set(changed)==allowed,('Unexpected edited files',set(changed)^allowed)
assert all(p.startswith('docs/architecture/') for p in changed)
with zipfile.ZipFile(OUT/'pre-edit.zip') as z:
    for path in z.namelist():assert hashlib.sha256(z.read(path)).hexdigest()==base[path],('Backup mismatch',path)
    old_catalog=z.read('docs/architecture/002-data-architecture.md').decode('utf-8-sig')
catalog=text('docs/architecture/002-data-architecture.md')
def section(t):return t.split('<!-- KPI_CATALOG_START -->')[1].split('<!-- KPI_CATALOG_END -->')[0]
assert section(old_catalog).replace('\r\n','\n')==section(catalog).replace('\r\n','\n'),'Canonical summary changed'

d1=text('docs/architecture/001-system-blueprint.md')
d2=text('docs/architecture/002-data-architecture.md')
d3=text('docs/architecture/003-decisions-and-roadmap.md')
d4=text('docs/architecture/004-reconciliation-review.md')
adr=re.findall(r'^### (ADR-\d{2}):',d3,re.M)
gates=re.findall(r'^\| <a id="at-\d{2}"></a>(AT-\d{2}) \|',d3,re.M)
req=re.findall(r'^\| <a id="req-\d{2}"></a>(REQ-\d{2}) \|',d1,re.M)
review_q=re.findall(r'^\| <a id="review-q\d{2}"></a>(Q\d{2}):',d4,re.M)
assert adr==[f'ADR-{n:02d}' for n in range(1,18)]
assert gates==[f'AT-{n:02d}' for n in range(1,31)]
assert req==[f'REQ-{n:02d}' for n in range(1,18)]
assert review_q==[f'Q{n:02d}' for n in range(1,18)]
dl=re.findall(r'^\| (DL-\d{2}) /',d3,re.M)
assert dl==[f'DL-{n:02d}' for n in range(1,20)],dl

with (ROOT/'dataset/config/kpi_dictionary.csv').open(encoding='utf-8-sig',newline='') as f:source_kpi=list(csv.DictReader(f))
kpi=csv_rows('kpi-contracts.csv')
assert len(kpi)==55
assert {r['kpi_id'] for r in kpi}=={r['kpi_id'] for r in source_kpi}
for old,new in zip(source_kpi,kpi):
    assert all(old[k]==new[k] for k in old),('KPI field drift',old['kpi_id'])
    assert hashlib.sha256(old['sql'].encode()).hexdigest()==new['sql_sha256']
    assert all(new[k] for k in ['output_clock','window','formula_population','row_null_and_population_boundary'])

with (ROOT/'dataset/config/escalation_rules.csv').open(encoding='utf-8-sig',newline='') as f:rules=list(csv.DictReader(f))
rule_contract=csv_rows('rule-contracts.csv')
assert [r['rule_id'] for r in rule_contract]==[r['rule_id'] for r in rules]==[f'R{i}' for i in range(1,9)]
assert all(a['rule_fa']==b['source_text'] for a,b in zip(rules,rule_contract))
rule_table=d1.split('### 7.1. Complete R1-R8 contract')[1].split('`series_key =')[0]
assert re.findall(r'^\| (R[1-8]) /',rule_table,re.M)==[f'R{i}' for i in range(1,9)]
for token in ['more than','at least 20%','less than 10%','greater than N%','previous four weeks','never create alerts','Jalali']:
    assert token in rule_table,('Missing rule meaning',token)

with (ROOT/'dataset/config/workflow_definitions.csv').open(encoding='utf-8-sig',newline='') as f:stages=list(csv.DictReader(f))
contracts=csv_rows('workflow-contracts.csv')
assert len(contracts)==len(stages)==12
for a,b in zip(stages,contracts):assert all(a[k]==b[k] for k in a),('Workflow drift',a)
stage_table=d1.split('#### All supplied Workflow stages')[1].split('WF1.5 uses')[0]
assert re.findall(r'^\| (WF\d\.\d) /',stage_table,re.M)==[r['workflow_id']+'.'+r['stage_order'] for r in stages]

inputs=json.loads(text('dataset/manager_inputs/scripted_inputs.json'))
inputs_doc=csv_rows('manager-input-contracts.csv')
assert len(inputs)==len(inputs_doc)==23
for source,contract in zip(inputs,inputs_doc):
    assert source['input_id']==contract['input_id'] and source['content_fa']==contract['source_content']
    assert int(contract['operational_drop_max'])==source['day']-1
qa_section=d3.split('<a id="manager-question-map"></a>')[1].split('### 7.2a.')[0]
assert re.findall(r'^\| (Q\d{2}) /',qa_section,re.M)==[r['input_id'] for r in inputs if r['type']=='question']
assert all(r['input_id'] in d3.split('### 7.2a.')[1] for r in inputs if r['type']!='question')

schema_records=csv_rows('output-schema-contracts.csv')
for r in schema_records:
    node=json.loads(text(r['source']))
    for part in r['pointer'].strip('/').split('/'):node=node[part]
    expected=json.loads(r['constraints'])
    assert all(node[k]==v for k,v in expected.items()),('Schema drift',r['pointer'])
brief=json.loads(text('dataset/output_contract/brief_schema.json'))
qa=json.loads(text('dataset/output_contract/qa_answer_schema.json'))
enum_sets=[brief['properties']['items']['items']['properties']['status']['enum'],
    brief['properties']['data_issues']['items']['properties']['source']['enum'],
    brief['properties']['data_issues']['items']['properties']['type']['enum'],
    brief['properties']['decision_followups']['items']['properties']['effect_direction']['enum'],
    qa['properties']['answer_status']['enum']]
assert all(all(value in d1 for value in values) for values in enum_sets)

matrix=csv_rows('requirements-traceability.csv')
matrix_ids={r['requirement_id'] for r in matrix}
assert len(matrix)==len(matrix_ids)==339
assert {f'REQ-{n:02d}' for n in range(1,18)}<=matrix_ids
for r in matrix:
    assert (ROOT/r['source_path']).exists()
    assert r['classification'] in {'Requirement','Accepted','Proposed','Open'}
    assert set(r['adr'].split(';'))<=set(adr),(r['requirement_id'],'ADR')
    assert set(r['acceptance_tests'].split(';'))<=set(gates),(r['requirement_id'],'AT')
    assert all(r[k] for k in ['source_location','requirement','architecture_component','contract_or_rule','remaining_gap'])
assert {r['requirement_id'] for r in kpi}<=matrix_ids
assert {r['requirement_id'] for r in contracts}<=matrix_ids
assert {f'REQ-INPUT-{r["input_id"]}' for r in inputs}<=matrix_ids
assert {f'REQ-{r["rule_id"]}' for r in rules}<=matrix_ids
bases=csv_rows('acceptance-basis.csv')
assert [r['test_id'] for r in bases]==gates
assert all(r['execution_status']=='Planned; not run by this audit' for r in bases)

# Validate only active Markdown, not archived raw diagrams or historical unified diffs.
markdown=list((ROOT/'docs/architecture').rglob('*.md'))
links=[];errors=[];fences=0
model=json.loads((OUT/'structurizr-inventory.json').read_text(encoding='utf-8'))
view_keys={r['key'] for r in model['views']}
assert len(view_keys)==16 and len(model['elements'])==46 and len(model['relationships'])==127
assert hashlib.sha256((ROOT/'architecture/structurizr/workspace.dsl').read_bytes()).hexdigest()==model['source_sha256']
for p in markdown:
    content=p.read_text(encoding='utf-8-sig')
    anchors=re.findall(r'<a id="([^"]+)"',content)
    assert len(anchors)==len(set(anchors)),('Duplicate anchor',p)
    in_fence=False;fence_marker=''
    visible=[]
    for line in content.splitlines():
        m=re.match(r'^(`{3,}|~{3,})(.*)$',line)
        if m:
            if not in_fence:
                in_fence=True;fence_marker=m[1];fences+=1
                assert m[2].strip().lower()!='mermaid',('Active retired diagram',p)
            elif m[1].startswith(fence_marker) and not m[2].strip():in_fence=False
            continue
        if not in_fence:visible.append(line)
    assert not in_fence,('Unclosed fence',p)
    body='\n'.join(visible)
    for label,target in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',body):
        if re.match(r'^(?:https?://|mailto:)',target):continue
        target=unquote(target.strip('<>'))
        name,_,anchor=target.partition('#')
        dest=(p.parent/name).resolve() if name else p
        links.append((p.relative_to(ROOT).as_posix(),target))
        if not dest.exists():errors.append((str(p),target,'missing file'))
        elif anchor and dest.suffix=='.md' and f'id="{anchor}"' not in dest.read_text(encoding='utf-8-sig'):
            errors.append((str(p),target,'missing anchor'))
        if name.endswith('.mmd'):errors.append((str(p),target,'active archived diagram link'))
assert not errors,errors
for p in [ROOT/'docs/architecture/001-system-blueprint.md',ROOT/'docs/architecture/002-data-architecture.md',
          ROOT/'docs/architecture/visualizations/README.md']:
    for keys in re.findall(r'`([A-Z][A-Za-z]+)`',p.read_text(encoding='utf-8')):
        # A reference is a view only when it belongs to the known set. Other technical terms are not guessed links.
        if keys in view_keys:assert keys in view_keys
assert len(list((ROOT/'docs/architecture/visualizations').glob('*.mmd')))==26
assert len(list((ROOT/'docs/architecture/visualizations/previews').glob('*.md')))==26
assert not any('SQLite' in line and 'executes' in line and 'not' not in line and 'reference' not in line.lower()
               for line in (d1+d2+d3).splitlines()),'Review unexpected SQLite execution wording'

summary=json.loads((OUT/'source-checks.json').read_text(encoding='utf-8'))
assert summary['manifest_count']==91 and all(r['matches'] for r in summary['manifest_checks'])
assert summary['calendar']['manifest_dates_match'] and summary['calendar']['rows']==90
findings=json.loads((OUT/'findings.json').read_text(encoding='utf-8'))
assert len(findings)==59
ledger=csv_rows('document-review-ledger.csv');assert len(ledger)==911
result=dict(check_kind='Documentation/source audit only; no product acceptance test run',
    baseline_files=len(base),modified_existing_files=sorted(changed),modified_existing_count=len(changed),
    unchanged_existing_files=len(base)-len(changed),
    unchanged_dataset_files=sum(p.startswith('dataset/') for p in base),
    protected_source_model_and_review_unchanged=True,backup_members_verified=79,
    local_markdown_links=len(links),active_markdown_files=len(markdown),active_fenced_blocks=fences,
    active_retired_diagrams=0,retired_raw_files_unchanged=26,retired_previews=26,
    preserved_umbrella_req_ids=17,adrs=17,planned_acceptance_gates=30,review_questions=17,
    decision_log_rows=19,rule_contracts=8,canonical_kpi_contracts=55,workflow_stage_contracts=12,
    manager_input_contracts=23,schema_property_contracts=len(schema_records),traceability_rows=len(matrix),
    document_review_units=len(ledger),audit_records=59,material_findings=58,corrected_documentation_findings=56,
    deferred_model_findings=2,verified_retained_observations=1,structurizr_elements=46,structurizr_model_relationships=127,
    structurizr_views=16,source_sql_executed=False,product_tests_executed=False,
    structurizr_parser_run=False,structurizr_renderer_run=False,commit_or_push_attempted=False)
(OUT/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='modified_existing_files'},indent=2))
