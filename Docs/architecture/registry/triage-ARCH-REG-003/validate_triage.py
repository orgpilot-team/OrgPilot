"""Validate triage coverage and task preservation. No product tests run."""
from pathlib import Path
from collections import Counter
from urllib.parse import unquote
import csv, hashlib, io, json, re, subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).resolve().parent;REG=OUT.parent;ROOT=REG.parents[2]
PREFIX='Docs/architecture/registry/'
pre=json.loads((OUT/'before-manifest.json').read_text(encoding='utf-8'))
def read(p):return p.read_text(encoding='utf-8-sig')
def csvread(p):return list(csv.DictReader(io.StringIO(read(p))))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):
    p=subprocess.run(['git','-c','core.quotepath=false',*args],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
    return dict(code=p.returncode,out=p.stdout,err=p.stderr)
def writecsv(path,rows,fields=None):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
checks=[]
def check(name,ok,detail=''):
    checks.append(dict(name=name,ok=bool(ok),detail=detail))
matrix=csvread(REG/'traceability-matrix.csv')
expected={n:r for n,r in enumerate(matrix,2) if r['row_kind']=='relationship' and r['relationship_status']=='Proposed Relationship'}
members=csvread(OUT/'relationship-classification.csv');queue=csvread(REG/'traceability-review-queue.csv')
summary=json.loads(read(OUT/'summary.json'));main={r['record_id']:r for r in matrix if r['row_kind']=='record'}
check('Exactly 2470 inferred relationships in the input',len(expected)==2470)
check('Exactly one member per inferred row',len(members)==2470 and {int(m['matrix_row']) for m in members}==set(expected))
check('Unique stable triage relationship IDs',len({m['relationship_id'] for m in members})==2470)
check('Every member matches its actual matrix pair/type/class',all(all(m[out]==expected[int(m['matrix_row'])][field] for out,field in [('source_id','record_id'),('target_id','target_id'),('source_type','record_type'),('target_type','target_type'),('relationship_type','relationship_type'),('current_evidence_class','relationship_status')]) for m in members))
check('Every endpoint remains a declared Registry record',all(m['source_id'] in main and m['target_id'] in main for m in members))
check('All members remain Pending Review',all(m['status']=='Pending Review' for m in members))
check('All queue items remain Pending Review',all(q['current_status']=='Pending Review' for q in queue))
check('Only declared priorities used',all(m['priority'] in ['P0','P1','P2'] for m in members))
check('No inferred link treated as an execution dependency',all(m['execution_dependency']=='Not established by this reference' for m in members))
check('All rows have a substantive reason, impact, action, route and evidence',all(all(m[f] for f in ['semantic_class','reason_for_uncertainty','potential_impact','recommended_review_action','route','relevant_source_evidence']) for m in members))
check('Queue group IDs are unique',len({q['review_id'] for q in queue})==len(queue))
by_group={q['review_id']:q for q in queue}
check('Every existing edge belongs to an existing-edge queue batch',all(m['group_id'] in by_group and by_group[m['group_id']]['scope']=='Existing inferred relationships' for m in members))
bad_groups=[]
for q in queue:
    ms=[m for m in members if m['group_id']==q['review_id']]
    if len(ms)!=int(q['relationship_count']):bad_groups.append(q['review_id'])
    if ms and any(m['priority']!=q['priority'] or m['disposition']!=q['disposition'] or m['semantic_class']!=q['semantic_class'] for m in ms):bad_groups.append(q['review_id']+' mixed semantics/priority/disposition')
    if ms and (set(json.loads(q['source_ids']))!={m['source_id'] for m in ms} or set(json.loads(q['target_ids']))!={m['target_id'] for m in ms}):bad_groups.append(q['review_id']+' wrong endpoint sets')
check('Queue counts and homogeneous semantic batches match exact members',not bad_groups,bad_groups)
check('Existing-edge queue counts sum to 2470',sum(int(q['relationship_count']) for q in queue)==2470)
check('Detailed classification partitions are retained',len({m['classification_key'] for m in members})==summary['source_specific_classification_groups']==180)
check('Queue totals match summary',len(queue)==summary['queue_groups']==109 and sum(q['scope']=='Existing inferred relationships' for q in queue)==summary['existing_edge_groups']==108)
check('Priority counts match summary',dict(Counter(m['priority'] for m in members))==summary['priorities_relationships'] and dict(Counter(q['priority'] for q in queue))==summary['priorities_queue_groups'])
check('Questionable count is precise',sum(m['disposition']=='Questionable' for m in members)==summary['questionable_relationships']==274)
check('Questionable batches are counted without missing candidates',sum(q['disposition']=='Questionable' and int(q['relationship_count'])>0 for q in queue)==summary['questionable_existing_groups']==47)

kpi=csvread(OUT/'kpi-policy-evidence.csv')
canonical=csvread(ROOT/'DataSet/arka_dataset/config/kpi_dictionary.csv')
check('Every one of 55 canonical KPIs has evidence and exactly one orders link',len(kpi)==55 and {k['kpi_id'] for k in kpi}=={k['kpi_id'] for k in canonical} and all(sum(m['source_id']=='REQ-KPI-'+k['kpi_id'] and m['target_id']=='ADR-02' for m in members)==1 for k in kpi))
check('Canonical SQL hashes agree with source bytes as parsed',all(k['canonical_sql_sha256']==hashlib.sha256(next(c['sql'] for c in canonical if c['kpi_id']==k['kpi_id']).encode('utf-8')).hexdigest() for k in kpi))
check('Orders cases separate selected value from declared relations',Counter(k['orders_policy_case'] for k in kpi)=={'value-orders':22,'declared-execution-only':1,'no-orders-relation':32})
check('The shared-view-only KPI is specifically K_ENT_CONTRACT_MTD',[k['kpi_id'] for k in kpi if k['orders_policy_case']=='declared-execution-only']==['K_ENT_CONTRACT_MTD'])
check('Eight historical sensitive KPIs remain attributed observations',sum(int(k['historical_full_different_keys'])>0 for k in kpi)==8 and all(k['historical_evidence'].startswith('Docs/review/') for k in kpi))
check('All source info KPIs remain no-alert gates',len([k for k in kpi if k['rule']=='info'])==3 and all(any(m['source_id']=='REQ-KPI-'+k['kpi_id'] and m['target_id']=='ADR-07' and 'info' in m['classification_key'] for m in members) for k in kpi if k['rule']=='info'))

missing=csvread(OUT/'missing-link-candidates.csv')
check('Only the two exact source-backed missing candidates are listed',{(r['source_id'],r['target_id']) for r in missing}=={('REQ-INPUT-IN05','AT-15'),('REQ-INPUT-IN07','AT-03')})
check('Missing candidates do not inflate 2470 membership',not any(m['source_id']==r['source_id'] and m['target_id']==r['target_id'] for m in members for r in missing))
check('Twenty non-question test extras are flagged for review',sum(m['source_id'].startswith('REQ-INPUT-IN') and m['target_type']=='AT' and m['disposition']=='Questionable' for m in members)==20)
coverage=csvread(OUT/'high-impact-coverage.csv')
coverage_counts=Counter(r['record_type'] for r in coverage)
check('All high-impact sets are covered, including zero-inferred records',coverage_counts=={'ADR':17,'DL':19,'Registry Issue':10,'AT':30,'Risk':20,'Decision Boundary':5,'Canonical KPI':55,'Workflow Stage':12,'Manager Input':23,'Manager Access Scope':11},dict(coverage_counts))
boundary=[m for m in members if m['source_type']=='Decision Boundary']
check('All 33 boundary mappings remain P0 inferred candidates',len(boundary)==33 and {m['source_id'] for m in boundary}=={r['record_id'] for r in matrix if r['row_kind']=='record' and r['record_type']=='Decision Boundary'} and all(m['priority']=='P0' and m['current_evidence_class']=='Proposed Relationship' for m in boundary))
confirmation=read(ROOT/'Docs/architecture/audit-2026-11-09/request.txt')
check('Actual S19 still supplies the five Accepted confirmations',all(s in confirmation for s in ['One bounded AI Agent','PostgreSQL as the only product database engine','Independent publication of valid manager reports','Deterministic KPI calculation','Human-controlled organizational decisions']))
grants=csvread(ROOT/'DataSet/arka_dataset/org/access_matrix.csv')
check('Actual upper-manager grants are aggregate-only',all(not g['individual_level_data_team'] for g in grants if g['manager_id'] in ['M01','M02','M03','M04']))
check('All 12 Workflow stages retain M01 end-to-end owner',len(csvread(ROOT/'DataSet/arka_dataset/config/workflow_definitions.csv'))==12 and all(s['owner']=='M01' for s in csvread(ROOT/'DataSet/arka_dataset/config/workflow_definitions.csv')))
stage=csvread(ROOT/'DataSet/arka_dataset/config/workflow_definitions.csv')
check('Deadline and missing SLA remain distinct',next(s['sla_hours'] for s in stage if s['workflow_id']=='WF1' and s['stage_order']=='4')=='promised_by' and next(s['sla_hours'] for s in stage if s['workflow_id']=='WF1' and s['stage_order']=='5')=='')
check('All 38 risk-to-AT links have exact criterion/control notes',len(csvread(OUT/'risk-control-coverage.csv'))==38 and {r['relationship_id'] for r in csvread(OUT/'risk-control-coverage.csv')}=={m['relationship_id'] for m in members if m['source_type']=='Risk' and m['target_type']=='AT'})
check('Risk-control notes retain pending execution and unassessed severity',all(r['risk_severity']=='Not Assessed' and r['control_state']=='Evidence Pending / Not Executed' for r in csvread(OUT/'risk-control-coverage.csv')))
check('All 29 issues remain Open in unchanged matrix',sum(r['row_kind']=='record' and r['record_type'] in ['DL','Registry Issue'] and r['status']=='Open' for r in matrix)==29)
check('All 30 ATs remain Planned / Not Executed',sum(r['row_kind']=='record' and r['record_type']=='AT' and r['status']=='Planned / Not Executed' for r in matrix)==30)

# Source locations in every classification and queue evidence item must exist.
locs=set();bad=[]
for item in members+queue:
    for ev in json.loads(item['relevant_source_evidence']):locs.add((ev['file'],ev.get('anchor','')))
for p,a in sorted(locs):
    f=ROOT/p
    if not f.exists():bad.append((p,a,'missing file'))
    elif a and a not in set(re.findall(r'<a\s+id="([^"]+)"',read(f))):bad.append((p,a,'missing explicit anchor'))
check('All triage evidence files and anchors exist',not bad,bad)
for p in [OUT/'file-comparison.csv',OUT/'validation-results.json']:
    if not p.exists():p.write_text('Pending final output.\n',encoding='utf-8')
md_bad=[];link_count=0
for p in [REG/'approval-readiness.md']:
    for url in re.findall(r'\[[^\]\n]*\]\(([^\s)]+)\)',read(p)):
        f,_,a=url.partition('#');dest=(p.parent/unquote(f)).resolve();link_count+=1
        if not dest.exists() or a and a not in set(re.findall(r'<a\s+id="([^"]+)"',read(dest))):md_bad.append(url)
check('All readiness links and anchors resolve',not md_bad,dict(links=link_count,errors=md_bad))

changed=[];comparison=[]
for name,h in pre['sha256'].items():
    p=ROOT/name;actual=sha(p) if p.exists() else ''
    if actual!=h:changed.append(name)
    comparison.append(dict(path=name,state='Unchanged' if actual==h else 'Changed or missing',before_sha256=h,after_sha256=actual))
check('Every one of 1380 task-start files remains byte-identical',len(pre['sha256'])==1380 and not changed,changed)
check('Existing tracked baseline diff is unchanged',git('diff','--binary',pre['baseline'])['out']==pre['tracked_diff']['out'])
check('HEAD remains baseline',git('rev-parse','HEAD')['out'].strip()==pre['baseline'])
check('No staged changes',not git('diff','--cached','--name-only')['out'].strip())
untracked=set(git('ls-files','--others','--exclude-standard','-z')['out'].strip('\0').split('\0'))
check('All 177 existing untracked files remain untracked',len(pre['untracked'])==177 and set(pre['untracked'])<=untracked)
added=sorted(untracked-set(pre['untracked']))
check('Only the two deliverables and triage support files are new',all(p in [PREFIX+'approval-readiness.md',PREFIX+'traceability-review-queue.csv'] or p.startswith(PREFIX+'triage-ARCH-REG-003/') for p in added),added)
check('Matrix is unchanged; no relationship was deleted or promoted',sha(REG/'traceability-matrix.csv')==pre['sha256'][PREFIX+'traceability-matrix.csv'])
for name in added:
    p=ROOT/name
    comparison.append(dict(path=name,state='Added',before_sha256='',after_sha256='' if p.name in ['file-comparison.csv','validation-results.json'] else sha(p)))
writecsv(OUT/'file-comparison.csv',comparison)
errors=[x for x in checks if not x['ok']]
result=dict(state='Draft / Pending Review',checks=checks,errors=errors,summary=summary,all_source_locations_checked=len(locs),
            existing_files_changed=changed,new_files=added,git_status=git('status','--porcelain=v1','-uall'),
            note='All original bytes and inferred classes are preserved. Output self-hashes for file-comparison/validation-results are omitted to avoid a cycle. Checks establish full-set classification/preservation, not exhaustive human semantics or team approval.',
            product_tests_executed=False)
(OUT/'validation-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(ok=not errors,checks=len(checks),errors=errors,source_locations=len(locs),new_files=len(added),summary=summary),ensure_ascii=False,indent=2))
raise SystemExit(1 if errors else 0)
