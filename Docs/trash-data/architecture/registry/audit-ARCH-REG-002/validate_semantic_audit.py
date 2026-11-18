"""Check all Registry rows and write audit evidence. No source or product edits."""
from pathlib import Path
from collections import Counter, defaultdict
import ast, csv, difflib, hashlib, io, json, re, subprocess, sys, zipfile
from urllib.parse import unquote

sys.stdout.reconfigure(encoding='utf-8')
AUD=Path(__file__).resolve().parent;REG=AUD.parent;ROOT=REG.parents[2]
BASE='0a42950d1ce9734433d961540af9ab4be21573b2'
PREFIX='Docs/architecture/registry/'
D1='Docs/architecture/001-system-blueprint.md';D2='Docs/architecture/002-data-architecture.md'
D3='Docs/architecture/003-decisions-and-roadmap.md';D4='Docs/architecture/004-reconciliation-review.md'
PDF='Docs/بریف پروژه بوتکمپ _ دستیار ایجنتیک مدیران سازمانی _ دیدراه.pdf'
CURRENT='f6761b4fc37145d152f2b9793b298e35f48db666d5205c4d02be0f5f13e4863b'
OLD='6d68d3fcc285f6908af0d97c0429dfefb489f00b7f6538ed03573552ed6955f8'
pre=json.loads((AUD/'before-manifest.json').read_text(encoding='utf-8'))
archive=zipfile.ZipFile(AUD/'before-files.zip')
def text(p):return p.read_text(encoding='utf-8-sig')
def before(name):return archive.read(name).decode('utf-8-sig').replace('\r\n','\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write_csv(p,rows,fields=None):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
def git(*args):
    p=subprocess.run(['git','-c','core.quotepath=false',*args],capture_output=True,text=True,encoding='utf-8',cwd=ROOT)
    return dict(code=p.returncode,out=p.stdout,err=p.stderr)
def strip(s):return re.sub(r'^```[^\n]*\n.*?^```\s*$', '',s,flags=re.M|re.S)
def anchors(p):return set(re.findall(r'<a\s+id="([^"]+)"',strip(text(p)))) if p.suffix.lower()=='.md' else set()
def sect(s,id):
    start=s.index(f'<a id="{id}"></a>');m=re.search(r'\n<a id="[^\"]+"></a>',s[start+1:])
    return s[start:start+1+m.start()] if m else s[start:]
checks=[]
def check(name,condition,detail=''):
    checks.append(dict(name=name,ok=bool(condition),detail=detail))

raw=text(REG/'traceability-matrix.csv')
reader=csv.DictReader(io.StringIO(raw));rows=list(reader);fields=reader.fieldnames
oldreader=csv.DictReader(io.StringIO(before(PREFIX+'traceability-matrix.csv')));oldrows=list(oldreader)
check('Unchanged CSV schema',fields==oldreader.fieldnames,fields)
check('All CSV rows have the declared fields',all(set(r)==set(fields) and all(v is not None for v in r.values()) for r in rows))
check('Allowed row kinds',all(r['row_kind'] in ['record','evidence','relationship'] for r in rows))
main={r['record_id']:r for r in rows if r['row_kind']=='record'}
check('Unique main IDs',len(main)==sum(r['row_kind']=='record' for r in rows))
check('Stable valid ID syntax',all(re.fullmatch(r'[A-Za-z0-9_]+(?:[-.][A-Za-z0-9_]+)*',r['record_id']) for r in rows))
check('All former record IDs retained',{r['record_id'] for r in oldrows if r['row_kind']=='record'}<=set(main))
check('Every row refers to its declared record',all(r['record_id'] in main and r['record_type']==main[r['record_id']]['record_type'] for r in rows))
check('Every row status agrees with its main record',all(r['status']==main[r['record_id']]['status'] for r in rows))
edges=[r for r in rows if r['row_kind']=='relationship']
check('Every relationship endpoint has a main record',all(r['target_id'] in main and r['target_type']==main[r['target_id']]['record_type'] for r in edges))
check('Every relationship has a known type',all(r['relationship_type'] in ['references','part_of','supported_by','supports','has_open_detail','referenced_by','has_criteria'] for r in edges))
check('Every relationship has a declared evidence class',all(r['relationship_status'] in ['Documented','Proposed Relationship'] for r in edges))
domains={'part_of':{('Requirement','Requirement'),('Decision Statement','ADR')},
         'supported_by':{('ADR','Source')},'supports':{('Source','ADR'),('Source','Decision Statement')},
         'has_open_detail':{('ADR','DL')},'referenced_by':{('AT','ADR'),('AT','DL'),('AT','Registry Issue')},
         'has_criteria':{('AT','Acceptance Supplement')}}
check('Typed relation directions match their declared meaning',all((r['record_type'],r['target_type']) in domains[r['relationship_type']] for r in edges if r['relationship_type'] in domains))
check('One target per edge',all(r['target_id'] and not re.search(r'[;,\n]',r['target_id']) for r in edges))
check('Typed relation fields agree with target',all(not r[f] or r[f]==r['target_id'] for r in edges for f in ['related_adr','related_dl','related_at','related_risk','roadmap_phase','architecture_component']))
check('No duplicate full rows',len(rows)==len({tuple(r[f] for f in fields) for r in rows}))
check('No self relationships',not any(r['record_id']==r['target_id'] for r in edges))
badloc=[]
for r in rows:
    p=ROOT/r['source_file']
    if not r['source_file'] or not p.exists():badloc.append((r['record_id'],'source file',r['source_file']))
    elif r['source_anchor'] and r['source_anchor'] not in anchors(p):badloc.append((r['record_id'],'source anchor',r['source_anchor']))
    if r['registry_file']:
        q=REG/r['registry_file']
        if not q.exists() or r['registry_anchor'] not in anchors(q):badloc.append((r['record_id'],'Registry anchor',r['registry_anchor']))
check('Every row source and Registry location resolves',not badloc,badloc[:10])

# Inspect both acyclic membership links and cyclic cross-reference groups.
def scc(selected):
    graph=defaultdict(list)
    for r in selected:graph[r['record_id']].append(r['target_id'])
    index={};low={};stack=[];active=set();result=[]
    def visit(v):
        index[v]=low[v]=len(index);stack.append(v);active.add(v)
        for w in graph[v]:
            if w not in index:visit(w);low[v]=min(low[v],low[w])
            elif w in active:low[v]=min(low[v],index[w])
        if low[v]==index[v]:
            comp=[]
            while True:
                w=stack.pop();active.remove(w);comp.append(w)
                if w==v:break
            if len(comp)>1:result.append(sorted(comp))
    for v in list(main):
        if v not in index:visit(v)
    return result
membership_cycles=scc([r for r in edges if r['relationship_type'] in ['part_of','has_criteria']])
reference_cycles=scc(edges)
check('Membership hierarchy is acyclic',not membership_cycles,membership_cycles)
cycles=[dict(group=f'REF-CYCLE-{i:02d}',members=json.dumps(c),interpretation='Typed cross-references/inverses; not an execution dependency graph. No requires edge exists.') for i,c in enumerate(reference_cycles,1)]
if cycles:write_csv(AUD/'reference-cycles.csv',cycles)
dup_groups=defaultdict(list)
for n,r in enumerate(rows,2):
    if r['row_kind']=='relationship':dup_groups[(r['record_id'],r['target_id'],r['target_type'],r['relationship_type'])].append(n)
repeat_pairs=[dict(source=k[0],target=k[1],target_type=k[2],relationship_type=k[3],matrix_rows=json.dumps(v),disposition='Retained distinct provenance rows; compare source_file/anchor/ref. Not parallel decisions.') for k,v in dup_groups.items() if len(v)>1]
write_csv(AUD/'repeated-edge-provenance.csv',repeat_pairs,['source','target','target_type','relationship_type','matrix_rows','disposition'])

for typ,expected in [('ADR',17),('DL',19),('Registry Issue',10),('AT',30),('Risk',20),('Requirement',334),('Decision Boundary',5),('Source',19)]:
    check(typ+' coverage',sum(r['record_type']==typ for r in main.values())==expected)
check('Accepted statements remain five',sum(r['record_type']=='Decision Statement' and r['status']=='Accepted' for r in main.values())==5)
check('All ATs remain Planned / Not Executed',all(r['status']=='Planned / Not Executed' for r in main.values() if r['record_type']=='AT'))
check('All issues remain Open',all(r['status']=='Open' for r in main.values() if r['record_type'] in ['DL','Registry Issue']))
for name in ['decisions-registry.md','risk-register.md','acceptance-register.md']:
    check(name+' exact file retained',sha(REG/name)==pre['sha256'][PREFIX+name])
    check(name+' full source extract blocks retained',re.findall(r'^```text\n(.*?)^```',text(REG/name),re.M|re.S)==re.findall(r'^```text\n(.*?)^```',before(PREFIX+name),re.M|re.S))
check('Open issue extracts unchanged',re.findall(r'^```text\n(.*?)^```',text(REG/'open-issues-registry.md'),re.M|re.S)==re.findall(r'^```text\n(.*?)^```',before(PREFIX+'open-issues-registry.md'),re.M|re.S))
risk=text(REG/'risk-register.md')
check('All risk severities Not Assessed',risk.count('Severity: **Not Assessed**.')==20)
check('Controls remain evidence pending',risk.count('Control status: **Evidence Pending**.')==20)
d3=text(ROOT/D3)
accepted=text(ROOT/'Docs/architecture/audit-2026-11-09/request.txt')
check('Five boundaries explicitly confirmed by S19',all(x in accepted for x in ['One bounded AI Agent','PostgreSQL as the only product database engine','Independent publication of valid manager reports','Deterministic KPI calculation','Human-controlled organizational decisions']))
check('S01 bytes match current identity',sha(ROOT/PDF)==CURRENT)
check('001 and 004 retain current and historical S01 hashes',all(CURRENT in text(ROOT/p) and OLD in text(ROOT/p) for p in [D1,D4]))
check('REG-ISS-010 stays Open with resolved identity subpart','Resolved subpart:' in sect(text(REG/'open-issues-registry.md'),'reg-iss-010') and main['REG-ISS-010']['status']=='Open')

# Compare original relationship identities, including missing/lost edges.
def key(r):return tuple(r[x] for x in ['record_id','target_id','target_type','relationship_type','source_file','source_anchor','source_ref'])
oldedge={key(r) for r in oldrows if r['row_kind']=='relationship'};newedge={key(r) for r in edges}
removed=oldedge-newedge
corrections=list(csv.DictReader((AUD/'corrections.csv').open(encoding='utf-8',newline='')))
removed_corrections=[r for r in corrections if r['kind']=='Unsupported edge removed']
check('Every removed edge has an explicit before/after correction',len(removed)==len(removed_corrections)==5,dict(removed=len(removed),documented=len(removed_corrections)))
review=list(csv.DictReader((AUD/'relationship-review.csv').open(encoding='utf-8',newline='')))
check('Every active edge has a review entry',sum(bool(r['matrix_row']) for r in review)==len(edges))
check('All 339 original IDs have current source locator checks',len(list(csv.DictReader((AUD/'source-locator-checks.csv').open(encoding='utf-8',newline=''))))==339)

# Record-level semantic review notes. This is a bounded topic/authority review;
# it is not represented as an exhaustive proof of all prose or all product claims.
issue_notes={
 'DL-01':'Accepted engine is fixed. Translation/type choices and all-55 proof stay separate; engineering evidence is not engine reselection.',
 'DL-02':'RAW/DEDUP has real source authority uncertainty. Preserve both input options and official expected-result route.',
 'DL-03':'Missing/empty/backfill cannot prove closure. Current null, dated prior context and release policy remain distinct.',
 'DL-04':'Full/selective rebuild and restatement are distinct facets. Restored ADR-05 compressed reference.',
 'DL-05':'No supplied secondary same-drop precedence. No current correction tie is claimed.',
 'DL-06':'Hierarchy is fixed. Exact projections/redaction need engineering/team review; organizer route is conditional on actual source meaning.',
 'DL-07':'Headcount/hours/privacy alternatives stay open. Missing work-hours contract creates only a conditional source route.',
 'DL-08':'M01 end-to-end ownership does not settle stage owners. AT-25 relation is a proposed cross-reference.',
 'DL-09':'Fixed R1-R8 comparisons remain fixed; only unresolved equality/baseline/reset choices remain open.',
 'DL-10':'M11 day 75 versus next-morning effect remains unresolved. Upload readiness and known-at are separate timing facets.',
 'DL-11':'Suppressed/ongoing source conflict needs authority. Internal schema and independence-storage details need team design.',
 'DL-12':'Human-only action authority is fixed. Confirmation/actor/history evidence details remain open; AT-29 is proposed.',
 'DL-13':'Accepted independent publication does not approve retry, fallback, export or whole-day success.',
 'DL-14':'Model/provider/gateway/internal bounds are team choices. External final hardware/profile belongs to DL-16.',
 'DL-15':'Retention and backup periods are not supplied; restore is an unexecuted engineering gate.',
 'DL-16':'Official profile, hardware and missing raw contracts still need source/evaluation evidence. Do not invent labels.',
 'DL-17':'Actual NULL dimension, no dimension and empty string stay separate until an approved wire mapping exists.',
 'DL-18':'Complete content is required. Candidate/Open/Published/history/Top-5 mapping is open; suppression is a separate DL-11 facet.',
 'DL-19':'Existing KPI modification and new KPI extension are separate tests; fixed 55 reference definitions stay preserved.',
 'REG-ISS-001':'Real P2/P3 source scope conflict. Do not select a milestone alternative; ADR-15 association is inferred.',
 'REG-ISS-002':'Source explicitly notes the QA context record gap. Its proposed AT links are relevant review aids, not declared source assignments.',
 'REG-ISS-003':'Source explicitly notes stage calculation population/query gap. Keep separate from DL-08 ownership.',
 'REG-ISS-004':'Source explicitly notes DQ-to-observation-to-eligibility record gap. Keep source release and rule choices in DL-03/09.',
 'REG-ISS-005':'Evidence-only claim about 70 outputs. Not an architecture choice or a target count.',
 'REG-ISS-006':'Delivery evidence coverage follow-up. The source supplement already lists requirements; consider AT-19 tracking at team review, without automatic closure.',
 'REG-ISS-007':'Broad record bundles physical-design approval and optional visualization gaps. Recommend later facet review; no diagram requirement is invented.',
 'REG-ISS-008':'Historical Git statement is not a same-time authority conflict. Keep as maintenance follow-up, remove team architecture-decision route.',
 'REG-ISS-009':'Upload format/retrieval design remains open. Receipt/effect time stays in DL-10; optional PDF/RAG are not requirements.',
 'REG-ISS-010':'User resolves current S01 identity. Historical PDF content comparison remains unverified. Keep record Open and remove unconditional organizer route.'}
record_review=[]
for id,r in main.items():
    typ=r['record_type']
    if typ not in ['ADR','DL','Registry Issue','AT','Risk'] and not (typ=='Decision Statement' and r['status']=='Accepted'):continue
    if typ=='ADR':note='Reviewed the complete ADR extract and numbered status index against 003. Accepted/Requirement/Proposed/Open are statement-level. Source roles and unexecuted gates stay explicit.'
    elif typ in ['DL','Registry Issue']:note=issue_notes[id]
    elif typ=='AT':note='Original criteria file and supplemental matrices are byte-identical. Reviewed test goal, authority basis and stated evidence; no product execution or extra acceptance threshold is claimed.'
    elif typ=='Risk':note='Reviewed stated cause/effect/control against the cited source topic. Control remains unexecuted; severity Not Assessed. ADR/DL/AT links remain inferred review aids, not proven mitigation.'
    else:note='Explicit five-boundary confirmation in S19 and 003 section 1 supports Accepted. S16 body/result supports the relevant topology/engine/publication choice. No approver name/date is invented.'
    record_review.append(dict(record_id=id,record_type=typ,title=r['title'],scope='Targeted complete-record topic/authority review',finding=note,
                              source_file=r['source_file'],source_anchor=r['source_anchor'],limit='Not a product test, formal semantic proof or team approval.'))
write_csv(AUD/'record-review.csv',record_review)
check('All 101 high-impact records have targeted review notes',len(record_review)==101)

# Link checks cover current Registry Markdown and original active source anchors.
# Do not treat old URLs inside verbatim extracts or archived files as new links.
links=[];badlinks=[]
for p in REG.glob('*.md'):
    for url in re.findall(r'\[[^\]\n]*\]\(([^\s)]+(?:\)[^\s)]*)?)\)',strip(text(p))):
        if re.match(r'\w+://',url):continue
        name,_,a=url.partition('#');dest=(p.parent/unquote(name)).resolve() if name else p
        links.append(url)
        if not dest.exists() or (a and unquote(a) not in anchors(dest)):badlinks.append((p.name,url))
check('All active Registry Markdown links resolve',not badlinks,badlinks)

allowed={D1,D4};unexpected=[];changes=[]
for name,h in pre['sha256'].items():
    p=ROOT/name;after=sha(p) if p.exists() else ''
    if after!=h:
        changes.append(dict(path=name,before_sha256=h,after_sha256=after,change='Modified',scope='S01 provenance only' if name in allowed else 'Registry correction'))
        if name not in allowed and not name.startswith(PREFIX):unexpected.append(name)
check('Only Registry and authorized S01 files changed',not unexpected,unexpected)
check('All initial tracked/untracked files preserved',all((ROOT/name).is_file() for name in pre['sha256']))
check('All dataset bytes unchanged',all(sha(ROOT/name)==h for name,h in pre['sha256'].items() if name.startswith('DataSet/')))
check('002 and 003 unchanged',all(sha(ROOT/p)==pre['sha256'][p] for p in [D2,D3]))
check('Only two tracked files differ from baseline',set(git('diff','--name-only',BASE)['out'].splitlines())==allowed)
check('Index remains unstaged',not git('diff','--cached','--name-only')['out'].strip())
check('HEAD remains local baseline',git('rev-parse','HEAD')['out'].strip()==BASE)
now=set(git('ls-files','--others','--exclude-standard','-z')['out'].strip('\0').split('\0'))
check('All 158 initial untracked files remain untracked',set(pre['untracked'])<=now)
original_pre=json.loads((REG/'preflight.json').read_text(encoding='utf-8'))
check('All 141 pre-Registry untracked source files remain byte-identical',all(sha(ROOT/p)==original_pre['sha256'][p] for p in original_pre['existing_untracked_files']))
check('Every new untracked file is inside Registry',all(x.startswith(PREFIX) for x in now-set(pre['untracked'])))

# Prove that only the reviewed exact metadata patch changed in 001/004. Full
# before/after text is retained below. The diff is small enough for direct review.
diffs=[]
for name in sorted(set([r['path'] for r in changes])):
    diffs.extend(difflib.unified_diff(before(name).splitlines(True),text(ROOT/name).splitlines(True),fromfile='before/'+name,tofile='after/'+name))
(AUD/'before-after.diff').write_text(''.join(diffs),encoding='utf-8')
(AUD/'baseline-tracked.diff').write_text(git('diff',BASE,'--',D1,D4)['out'],encoding='utf-8')
write_csv(AUD/'changed-files.csv',changes)
degree=Counter()
for r in edges:degree[r['record_id']]+=1;degree[r['target_id']]+=1
orphans=[dict(record_id=id,record_type=r['record_type'],title=r['title'],source_file=r['source_file'],disposition='Source location exists. No graph edge; retain inventory/phase/maintenance identity. No execution dependency is implied.') for id,r in main.items() if not degree[id]]
if orphans:write_csv(AUD/'orphan-records.csv',orphans)

counts=dict(rows=len(rows),kinds=dict(Counter(r['row_kind'] for r in rows)),records=dict(Counter(r['record_type'] for r in main.values())),
            relationship_classes=dict(Counter(r['relationship_status'] for r in edges)),source_locations=len(rows),active_links=len(links),
            reference_cycle_groups=len(reference_cycles),repeated_provenance_groups=len(repeat_pairs),orphan_records=len(orphans))
errors=[c for c in checks if not c['ok']]
result=dict(state='Draft / Pending Review',checks=checks,errors=errors,counts=counts,
            review_limits='Structural checks cover every row and endpoint. Source locators cover all 339 original IDs. Topic/authority review covers 101 high-impact records and five Accepted statements. High-volume imported edges remain inferred; this is not exhaustive semantic verification.',
            pdf_current_sha256=CURRENT,pdf_historical_sha256=OLD,product_tests_executed=False,
            git_status=git('status','--porcelain=v1','-uall'),modified_initial_files=changes)
(AUD/'validation-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(ok=not errors,checks=len(checks),errors=errors,counts=counts,changed_files=len(changes)),ensure_ascii=False,indent=2))
raise SystemExit(1 if errors else 0)
