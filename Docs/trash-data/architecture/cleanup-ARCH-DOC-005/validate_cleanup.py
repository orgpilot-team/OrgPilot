"""Validate documentation cleanup. Do not run product tests or historical generators."""
import csv, difflib, hashlib, io, json, os, re, subprocess, sys, zipfile
from collections import Counter
from pathlib import Path
from urllib.parse import unquote
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
sys.path.insert(0,str(OUT.parent/'restructure-ARCH-DOC-004'))
from doc_links import active_text, anchors, inventory, markdown_links, resolve
A='Docs/architecture/';R=A+'registry/';OLD=A+'003-decisions-and-roadmap.md';ROAD=A+'003-roadmap.md'
snap=zipfile.ZipFile(OUT/'before-documents.zip')
manifest=json.loads((OUT/'before-manifest.json').read_text(encoding='utf-8'))
def old(p):return snap.read(p).decode('utf-8-sig').replace('\r\n','\n')
def read(p):return (ROOT/p).read_text(encoding='utf-8-sig')
def rows(name):return list(csv.DictReader((OUT/name).open(encoding='utf-8-sig')))
def save(name,data,fields=None):
    with (OUT/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(data[0]));w.writeheader();w.writerows(data)
def norm(s):
    s=re.sub(r'(?m)^(\s*)۲\. ',r'\g<1>2. ',s)
    s=re.sub(r'\]\([^\n]*?\)','](LINK)',s)
    s=re.sub(r'<a\b[^>]*></a>','',s)
    return ' '.join(s.split())
checks=[]
def check(name,result,evidence):checks.append(dict(check=name,result='PASS' if result else 'FAIL',evidence=evidence))

# Rebuild the task-start link inventory from the frozen source bytes.
# The removed file is resolved against the manifest, not the current disk.
before_links=[]
for p in snap.namelist():
    if not p.endswith('.md'):continue
    for _,url,line,kind in markdown_links(old(p)):
        v=resolve(ROOT,ROOT/p,url)
        if v['state']!='External or host URL':
            exists=v['target'] in manifest['sha256'] or any(k.startswith(v['target'].rstrip('/')+'/') for k in manifest['sha256'])
            v['state']='Resolved' if exists else 'Missing file'
            if exists and v['anchor'] and v['target'].endswith('.md') and v['target'] in snap.namelist() and v['anchor'] not in anchors(old(v['target'])):v['state']='Missing anchor'
        before_links.append(dict(source_file=p,line=line,url=url,kind=kind,**v))
save('before-links.csv',before_links)
check('Task-start broken links accounted for',sum(r['state'].startswith('Missing') for r in before_links)==64,f'{len(before_links)} task-start links; {sum(r["state"].startswith("Missing") for r in before_links)} existing failures')

road=read(ROAD)
h2=re.findall(r'^## ([^\n]+)',road,re.M)
check('Sequential Persian Roadmap headings',[h.split('.')[0] for h in h2]==list('۱۲۳۴۵') and len(re.findall(r'^### ۲\.۱\.',road,re.M))==1,str(h2))
check('Legacy Roadmap section IDs removed',not re.search(r'decisions-[468]|id="execution-gates"',road),'Descriptive roadmap-* IDs replace legacy section IDs')
current=norm(active_text(road));absent=[]
for i,line in enumerate(old(ROAD).splitlines(),1):
    if not line.strip() or re.match(r'^(?:#{1,6}\s|<a )',line):continue
    if norm(line) not in current:absent.append(i)
check('Roadmap full body preserved',not absent,f'Full body lines compared; only heading, list-digit style and link destinations normalized; missing {absent}')
for file in ['001-system-blueprint.md','002-data-architecture.md','004-reconciliation-review.md']:
    p=A+file;before=old(p)
    if file.startswith('002-'):before=before.replace('[سند 003، بخش 8]','[سند 003، بخش ۳]')
    check(file+' source body',norm(before)==norm(read(p)),'Only navigation and the moved measurement section label may change')

for file in ['decisions-registry.md','open-issues-registry.md','risk-register.md','acceptance-register.md']:
    p=R+file
    check(file+' full content',norm(old(p))==norm(read(p)),'Complete body, original source extracts, all criteria and supplements unchanged after URL normalization')
bm=list(csv.DictReader(io.StringIO(old(R+'traceability-matrix.csv'))));am=list(csv.DictReader(io.StringIO(read(R+'traceability-matrix.csv'))))
check('Matrix full semantic identity',len(am)==len(bm) and all(all(a[k]==b[k] for k in a if k not in ['source_file','source_anchor']) for a,b in zip(am,bm)),f'{len(am)} rows; only source file/anchor navigation may change')
record=[r for r in am if r['row_kind']=='record']
counts=Counter(r['record_type'] for r in record)
check('ADR/DL/AT/risk IDs',all(any(r['record_id']==f'{family}-{i:02d}' for r in record) for family,total in [('ADR',17),('DL',19),('AT',30)] for i in range(1,total+1)) and counts['Risk']==20,str(dict(counts)))
check('Open and AT states',sum(r['record_type'] in ['DL','Registry Issue'] and r['status']=='Open' for r in record)==29 and sum(r['record_type']=='AT' and r['status']=='Planned / Not Executed' for r in record)==30,'29 Open issues; 30 Planned / Not Executed ATs')
check('Unconfirmed relationships',sum(r['row_kind']=='relationship' and r['relationship_status']=='Proposed Relationship' for r in am)==2470,'2470 remain unapproved; semantic fields compared in full')
check('Accepted boundaries',counts['Decision Boundary']==5 and all(a['status']==b['status'] for a,b in zip(am,bm)),'All five boundary records and all status fields unchanged')
check('Registry draft status','Draft / Pending Review' in read(R+'README.md'),'Location approval does not approve proposed architecture or product tests')
check('Original combined-source content',all(r['result']=='PASS' for r in rows('original-content-check.csv')),'297 substantive source lines checked against readable canonical documents before deletion; heading map retained separately')
check('Obsolete file removed',not (ROOT/OLD).exists(),'The one obsolete file was deleted after migration gates passed; no stub remains')

# Check exact spelling of each existing local path, including Unicode filenames.
def case_ok(target):
    try:parts=Path(target).relative_to(ROOT).parts
    except ValueError:return True
    base=ROOT
    for part in parts:
        if part not in {p.name for p in base.iterdir()}:return False
        base=base/part
    return True
paths=[p for p in ROOT.rglob('*.md') if '.git' not in p.parts]
links=inventory(ROOT,paths)
for r in links:
    r['path_case']='Not local' if not r['target'] else 'Exact' if (ROOT/r['target']).exists() and case_ok(ROOT/r['target']) else 'Missing or wrong case'
save('link-validation.csv',links)
unresolved=[r for r in links if r['state'].startswith('Missing') or r['path_case']=='Missing or wrong case']
save('unresolved-links.csv',unresolved,list(links[0]))
check('All local Markdown paths and anchors',not unresolved,f'{len(links)} links; states {dict(Counter(r["state"] for r in links))}; exact path spelling checked')
old_incoming=[r for r in links if '003-decisions-and-roadmap.md' in unquote(r['url'])]
check('No active Markdown link to removed file',not old_incoming,f'{len(old_incoming)} remaining; includes code-fence exclusion for source quotations')

# Validate every frozen legacy-anchor mapping against the new section locations.
aliases=list(csv.DictReader(io.StringIO(old(A+'restructure-ARCH-DOC-004/legacy-anchor-map.csv'))))
sectionmap=rows('roadmap-section-map.csv')
newanchors={'decisions-4':'roadmap-prerequisites','decisions-6':'roadmap-phases','decisions-8':'roadmap-measurement','execution-gates':'roadmap-execution-gates'}
for r in sectionmap:
    for a in anchors(r['before_heading']):newanchors[a]=r['after_anchor']
for r in aliases:
    if r['target_file']==ROAD:r['target_anchor']=newanchors.get(r['target_anchor'],r['target_anchor'])
    r['result']='PASS' if r['target_anchor'] in anchors(read(r['target_file'])) else 'FAIL'
save('legacy-destinations.csv',aliases)
check('95 original anchors have exact destinations',len(aliases)==95 and all(r['result']=='PASS' for r in aliases),'Mapping retained as evidence; no redirect document')

repairs=rows('link-repairs.csv')
audit_body_failures=[]
for p in {r['source_file'] for r in repairs}:
    if p in [ROAD,R+'README.md',A+'002-data-architecture.md']:continue
    source=old(p)
    if p==A+'audit-2026-11-09/change-report.md':source=source.replace('[003-decisions-and-roadmap.md]','[Current governance records; former combined source]')
    if norm(source)!=norm(read(p)):audit_body_failures.append(p)
check('Audit and supporting findings preserved',not audit_body_failures,f'All repaired supporting documents compared after URL and one navigation-label normalization; failures {audit_body_failures}')
historical=list(csv.DictReader(io.StringIO(old(A+'restructure-ARCH-DOC-004/historical-reference-catalog.csv'))))
reconciled=[]
for h in historical:
    found=[r for r in repairs if r['source_file']==h['source_file'] and r['line']==h['source_line'] and r['old_url']==h['legacy_url']]
    valid=bool(found) and all(resolve(ROOT,ROOT/r['source_file'],r['new_url'])['state']=='Resolved' for r in found)
    reconciled.append(dict(source_file=h['source_file'],source_line=h['source_line'],old_url=h['legacy_url'],new_url=found[0]['new_url'] if found else '',actual_target=h['current_file'],result='PASS' if valid else 'FAIL'))
save('historical-64-reconciliation.csv',reconciled)
check('Historical broken references reconciled',len(reconciled)==64 and all(r['result']=='PASS' for r in reconciled),'All 64 occurrences individually matched by source file, line and original URL')
check('Repair targets resolve',all(resolve(ROOT,ROOT/r['source_file'],r['new_url'])['state']=='Resolved' for r in repairs),f'{len(repairs)} URL replacements, including quoted source URLs')
matrix_bad=[]
for r in am:
    if r['source_file']:
        v=resolve(ROOT,ROOT/'placeholder.md','/'+r['source_file']+('#'+r['source_anchor'] if r['source_anchor'] else ''))
        if v['state']!='Resolved':matrix_bad.append(r['record_id'])
check('Live matrix source paths and anchors',not matrix_bad,f'{len(am)} source locations checked; failures {matrix_bad}')

# Find undefined explicit reference-style labels. Ordinary bracketed prose is not a link.
undefined=[]
for p in paths:
    text=active_text(p.read_text(encoding='utf-8-sig'))
    definitions={m.group(1).strip().casefold() for m in re.finditer(r'^ {0,3}\[([^]]+)\]:',text,re.M)}
    for m in re.finditer(r'!?\[([^]\n]+)\]\[([^]\n]*)\]',text):
        label=(m[2] or m[1]).strip().casefold()
        if label not in definitions:undefined.append(p.relative_to(ROOT).as_posix()+':'+label)
check('Reference-style definitions',not undefined,str(undefined))

# Historical paths and original bytes are retained as evidence, not current links.
retained=[]
for p in ROOT.rglob('*'):
    if not p.is_file() or '.git' in p.parts or OUT in p.parents or p.suffix.lower() not in ['.md','.csv','.json','.py','.txt','.dsl','.diff']:continue
    for i,line in enumerate(p.read_text(encoding='utf-8-sig',errors='replace').splitlines(),1):
        if '003-decisions-and-roadmap' in line:
            retained.append(dict(file=p.relative_to(ROOT).as_posix(),line=i,context=line[:600],classification='Historical identifier, source excerpt, hash/diff, snapshot or historical utility; not active Markdown navigation'))
save('retained-historical-identifiers.csv',retained)

changed=[];removed=[];diff=[];file_rows=[]
for p,sha in manifest['sha256'].items():
    path=ROOT/p
    if not path.exists():removed.append(p);state='Removed';current_sha=''
    else:
        current_sha=hashlib.sha256(path.read_bytes()).hexdigest()
        state='Unchanged' if current_sha==sha else 'Changed'
        if state=='Changed':changed.append(p)
    file_rows.append(dict(file=p,before_sha256=sha,after_sha256=current_sha,state=state,tracking='Tracked' if p in manifest['tracked'] else 'Untracked at task start'))
    if state!='Unchanged' and p in snap.namelist():
        after=read(p) if path.exists() else ''
        diff.extend(difflib.unified_diff(old(p).splitlines(True),after.splitlines(True),fromfile='before/'+p,tofile='after/'+p))
save('file-preservation.csv',file_rows)
allowed=set(r['source_file'] for r in repairs)|{ROAD,R+'README.md',R+'traceability-matrix.csv','Docs/review/team-guide-technical-review.md'}
check('Only authorized documentation changed',set(changed)<=allowed and removed==[OLD],f'{len(manifest["sha256"])} task-start files; {len(changed)} navigation/format changes; removed {removed}; unexpected {sorted(set(changed)-allowed)}')
check('Dataset SQL PDF DSL unchanged',all(r['state']=='Unchanged' for r in file_rows if r['file'].startswith('DataSet/') or Path(r['file']).suffix.lower() in ['.sql','.pdf','.dsl']),'All task-start hashes compared; DSL historical comment retained')
(OUT/'before-after.diff').write_text(''.join(diff),encoding='utf-8')
check('Git HEAD unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==manifest['head'],manifest['head'])
check('No staged changes',subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT).returncode==0,'No commit, push or staging action')
for args,name in [(['git','status','--short','--untracked-files=all'],'git-after.txt'),(['git','diff','--binary',manifest['head']],'baseline-tracked.diff')]:
    result=subprocess.run(args,cwd=ROOT,capture_output=True);(OUT/name).write_bytes(result.stdout);assert result.returncode==0
save('validation-results.csv',checks)
summary=dict(checks=checks,total_markdown_files=len(paths),total_links=len(links),link_states=dict(Counter(r['state'] for r in links)),unresolved=len(unresolved),newly_broken=len(unresolved),historical_repaired=len(reconciled),url_replacements=len(repairs),old_003_url_replacements=sum(r['reason'].startswith('Old combined') for r in repairs),changed_files=sorted(changed),removed_files=removed,retained_historical_identifier_occurrences=len(retained))
(OUT/'validation-results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
newfiles=[]
for p in ROOT.rglob('*'):
    if not p.is_file() or '.git' in p.parts or '__pycache__' in p.parts:continue
    rel=p.relative_to(ROOT).as_posix()
    if rel not in manifest['sha256'] and p.name!='new-file-inventory.csv':newfiles.append(dict(file=rel,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),state='New; untracked'))
save('new-file-inventory.csv',sorted(newfiles,key=lambda r:r['file']))
print(json.dumps(summary,ensure_ascii=True,indent=2))
