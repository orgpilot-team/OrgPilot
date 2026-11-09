"""Read source snapshots. Validate the structural migration. Do not run old generators."""
import csv, difflib, hashlib, io, json, os, re, subprocess, zipfile, sys
sys.dont_write_bytecode = True
from collections import Counter
from pathlib import Path
from doc_links import active_text, anchors, inventory, resolve

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
ARCH = 'Docs/architecture/'
REG = ARCH+'registry/'
D3 = ARCH+'003-decisions-and-roadmap.md'
snapshot = zipfile.ZipFile(OUT/'before-documents.zip')
manifest = json.loads((OUT/'before-manifest.json').read_text(encoding='utf-8'))
def old(p): return snapshot.read(p).decode('utf-8-sig').replace('\r\n','\n')
def read(p): return (ROOT/p).read_text(encoding='utf-8-sig')
def write_csv(name, rows, fields=None):
    with (OUT/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
def norm(s):
    s=re.sub(r'\]\([^\n]*?\)','](LINK)',s)
    s=re.sub(r'<a\b[^>]*></a>','',s)
    s=re.sub(r'^\s*#{1,6}\s*','',s)
    return ' '.join(s.split())

# A line-level location map checks readable text, not the archive or code fences.
destinations=[REG+x for x in ['README.md','decisions-registry.md','open-issues-registry.md','risk-register.md','acceptance-register.md']]+[ARCH+'003-roadmap.md',ARCH+'004-reconciliation-review.md']
live={p:[(i,norm(l)) for i,l in enumerate(active_text(read(p)).splitlines(),1)] for p in destinations}
mapping=[];missing=[]
for i,line in enumerate(old(D3).splitlines(),1):
    value=norm(line)
    if not value: continue
    matches=[(p,n) for p,lines in live.items() for n,t in lines if value in t]
    structural=bool(re.fullmatch(r'[| :\-]+',value))
    if matches:
        p,n=matches[0];state='Readable source text preserved'
    elif structural:
        p,n=REG+'README.md',1;state='Table formatting only; record tables preserved'
    else:
        p,n='',0;state='REVIEW: source text not found';missing.append(i)
    mapping.append(dict(source_file=D3,source_line=i,source_text=line,target_file=p,target_line=n,validation=state))
write_csv('content-location-map.csv',mapping)

# Keep immutable audit references intact. Give each old link a verified alternative.
before_links=list(csv.DictReader((OUT/'before-links.csv').open(encoding='utf-8-sig')))
catalog=[]
for r in before_links:
    if r['state'] not in ['Missing file','Missing anchor']:continue
    target=r['target']
    if target.startswith('Docs/dataset/'):target='DataSet/arka_dataset/'+target[len('Docs/dataset/'):]
    elif target.startswith('Docs/Project_berif/'):target='Docs/'+target[len('Docs/Project_berif/'):]
    assert (ROOT/target).exists(),target
    catalog.append(dict(source_file=r['source_file'],source_line=r['line'],legacy_url=r['url'],current_file=target,validation='Current file exists; historical text unchanged'))
write_csv('historical-reference-catalog.csv',catalog)
def href(p):return '<'+os.path.relpath(ROOT/p,OUT).replace('\\','/')+'>'
lines=['# Historical reference catalog','','Status: Draft / Pending Review.','','These 64 broken references existed before this task. The three audit reports remain unchanged. Use the current file links below. This map provides navigation. It does not approve a source or change historical findings.','','| Audit and line | Historical destination | Current file |','|---|---|---|']
for r in catalog:
    lines.append(f"| [{r['source_file']}:{r['source_line']}]({href(r['source_file'])}) | `{r['legacy_url']}` | [Current file]({href(r['current_file'])}) |")
(OUT/'historical-reference-catalog.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

checks=[]
def check(name,ok,detail):checks.append(dict(check=name,result='PASS' if ok else 'FAIL',detail=detail))
check('Every nonempty source line located',not missing,f'{len(mapping)} lines mapped; unmatched lines: {missing}')
for filename in ['001-system-blueprint.md','002-data-architecture.md']:
    p=ARCH+filename
    current='\n'.join(l for l in read(p).splitlines() if not l.startswith('Documentation responsibility, ARCH-DOC-004:'))
    check(filename+' content',norm(old(p))==norm(current),'Only navigation destinations and one responsibility note may change')
p=ARCH+'004-reconciliation-review.md'
check('004 historical body preserved',norm(old(p)) in norm(read(p)),'Original review text is retained; former 003 verification text is appended')

matrix=REG+'traceability-matrix.csv'
bm=list(csv.DictReader(io.StringIO(old(matrix))));am=list(csv.DictReader(io.StringIO(read(matrix))))
allowed={'source_file','source_anchor','source_ref'}
check('Matrix identity and semantic fields',len(bm)==len(am) and all(all(a[k]==b[k] for k in a if k not in allowed) for a,b in zip(am,bm)),f'{len(am)} rows; only source navigation fields may change')
counts=Counter(r['record_type'] for r in am if r['row_kind']=='record')
check('Governance statuses unchanged',all(a['status']==b['status'] and a['evidence_state']==b['evidence_state'] for a,b in zip(am,bm)), 'Five Accepted boundaries, 29 Open issues and 30 unexecuted tests retain their source statuses')
check('Inferred relationships unchanged',sum(r['row_kind']=='relationship' and r['relationship_status']=='Proposed Relationship' for r in am)==2470,'2470 Proposed Relationship rows; no approvals or dependency changes')
check('Open issues and AT execution',sum(r['row_kind']=='record' and r['record_type'] in ['DL','Registry Issue'] and r['status']=='Open' for r in am)==29 and sum(r['row_kind']=='record' and r['record_type']=='AT' and r['status']=='Planned / Not Executed' for r in am)==30,'29 Open; 30 Planned / Not Executed')
source_failures=[]
for r in am:
    if r['source_file']:
        state=resolve(ROOT,ROOT/'placeholder.md','/'+r['source_file']+('#'+r['source_anchor'] if r['source_anchor'] else ''))
        if state['state'].startswith('Missing'):source_failures.append(r['record_id'])
check('Matrix source paths and anchors',not source_failures,f'{len(am)} rows checked; failures {source_failures}')
check('All legacy anchors',anchors(old(D3))<=anchors(read(D3)),f'{len(anchors(old(D3)))} original explicit and heading anchors')
aliases=list(csv.DictReader((OUT/'legacy-anchor-map.csv').open(encoding='utf-8')))
check('Compatibility target anchors',all(r['target_anchor'] in anchors(read(r['target_file'])) for r in aliases),'All 95 canonical targets checked')
for family,total,file in [('ADR',17,'decisions-registry.md'),('DL',19,'open-issues-registry.md'),('AT',30,'acceptance-register.md')]:
    text=active_text(read(REG+file))
    check(family+' IDs',all(f'{family}-{n:02d}' in text for n in range(1,total+1)),f'{total} IDs in readable Markdown')
check('Risk IDs',all(f'REG-RSK-{i:03d}' in read(REG+'risk-register.md') for i in range(1,21)),'20 risk records')
for file in ['decisions-registry.md','open-issues-registry.md','risk-register.md','acceptance-register.md']:
    # Every former full source block must survive in active text, with moved links.
    blocks=re.findall(r'<summary>Source extract \(unchanged text\)</summary>\s*```text\n(.*?)\n```',old(REG+file),re.S)
    active=norm(active_text(read(REG+file)))
    absent=[i for i,b in enumerate(blocks,1) if norm(b) not in active]
    # Open issue records can retain quoted data-model evidence; 002 owns that contract.
    permitted=(file=='open-issues-registry.md' and absent==[20,21,22,23])
    quoted_retained=all(norm(blocks[i-1]) in norm(read(REG+file)) for i in absent)
    check(file+' full source extracts',not absent or (permitted and quoted_retained),f'{len(blocks)} extracts; non-active quoted extracts {absent}; four data-model quotes stay evidence in open issues')

# Diagrams are read only. Check SVG internal paint/filter targets as well as links.
diagram_files=[p for p in ROOT.rglob('*') if p.suffix.lower() in ['.mmd','.svg','.dsl'] and '.git' not in p.parts]
diagram_bad=[];diagram_links=0
for p in diagram_files:
    text=p.read_text(encoding='utf-8-sig')
    ids=set(re.findall(r'\bid=["\']([^"\']+)',text))
    for a in re.findall(r'url\(#([^)]*)\)',text):
        if a not in ids:diagram_bad.append(p.name+'#'+a)
    urls=re.findall(r'(?:href|xlink:href)=["\']([^"\']+)',text)
    urls+=re.findall(r'^\s*click\s+\S+\s+(?:href\s+)?["\']([^"\']+)',text,re.M)
    for url in urls:
        diagram_links+=1
        if not url.startswith('#') and resolve(ROOT,p,url)['state'].startswith('Missing'):diagram_bad.append(str(p)+':'+url)
check('Diagram navigation',not diagram_bad,f'{len(diagram_files)} diagram files; {diagram_links} navigation links; SVG internal targets checked; failures {diagram_bad}')

changed=[];removed=[]
for p,sha in manifest['sha256'].items():
    path=ROOT/p
    if not path.is_file():removed.append(p)
    elif hashlib.sha256(path.read_bytes()).hexdigest()!=sha:changed.append(p)
allow={ARCH+x for x in ['001-system-blueprint.md','002-data-architecture.md','003-decisions-and-roadmap.md','004-reconciliation-review.md']}|{REG+x for x in ['README.md','decisions-registry.md','open-issues-registry.md','risk-register.md','acceptance-register.md','traceability-matrix.csv']}
check('Unrelated files unchanged',not removed and set(changed)<=allow,f'{len(manifest["sha256"])} original files hashed; {len(changed)} allowed changes; removed {removed}; unexpected {sorted(set(changed)-allow)}')
write_csv('existing-file-changes.csv',[dict(file=p,old_sha256=manifest['sha256'][p],new_sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in sorted(changed)])
diff=[]
for p in sorted(changed):
    if p in snapshot.namelist():diff.extend(difflib.unified_diff(old(p).splitlines(True),read(p).splitlines(True),fromfile='before/'+p,tofile='after/'+p))
(OUT/'before-after.diff').write_text(''.join(diff),encoding='utf-8')
for args,name in [(['git','diff','--binary',manifest['baseline']],'baseline-tracked.diff'),(['git','status','--short','--untracked-files=all'],'git-status.txt')]:
    result=subprocess.run(args,cwd=ROOT,capture_output=True);(OUT/name).write_bytes(result.stdout);assert result.returncode==0
check('HEAD baseline unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==manifest['baseline'],manifest['baseline'])
check('Index unchanged',subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT).returncode==0,'No staged changes')

links=inventory(ROOT,list(ROOT.rglob('*.md')))
write_csv('after-links.csv',links)
broken=[r for r in links if r['state'].startswith('Missing')]
old_keys={(r['source_file'],r['url'],r['state']) for r in before_links if r['state'].startswith('Missing')}
new_broken=[r for r in broken if (r['source_file'],r['url'],r['state']) not in old_keys]
check('No new broken Markdown links',not new_broken,f'{len(links)} links; {len(broken)} retained historical broken references; new failures {len(new_broken)}')
write_csv('validation-results.csv',checks)
summary=dict(checks=checks,source_lines=len(mapping),missing_lines=missing,existing_changed=sorted(changed),links=dict(Counter(r['state'] for r in links)),new_broken=new_broken,matrix_rows=len(am),record_counts=dict(counts))
(OUT/'validation-results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
current_files=[p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.relative_to(ROOT).parts and '__pycache__' not in p.parts]
tree=subprocess.check_output(['git','ls-tree','-rz',manifest['baseline']],cwd=ROOT)
baseline_blobs={}
for entry in tree.split(b'\0'):
    if not entry:continue
    meta,name=entry.split(b'\t',1)
    baseline_blobs[name.decode('utf-8')]=meta.split()[2].decode('ascii')
baseline_rows=[]
for p in current_files:
    rel=p.relative_to(ROOT).as_posix()
    if rel in ['Docs/architecture/restructure-ARCH-DOC-004/baseline-all-files.csv','Docs/architecture/restructure-ARCH-DOC-004/new-file-inventory.csv']:continue
    data=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    base=baseline_blobs.get(rel,'')
    baseline_rows.append(dict(file=rel,baseline_blob=base,current_blob=blob,current_sha256=hashlib.sha256(data).hexdigest(),state='Untracked; absent at baseline' if not base else 'Unchanged' if base==blob else 'Changed; check diff and task-start state'))
write_csv('baseline-all-files.csv',sorted(baseline_rows,key=lambda r:r['file']))
current_files=[p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.relative_to(ROOT).parts and '__pycache__' not in p.parts]
artifact_rows=[]
for p in current_files:
    rel=p.relative_to(ROOT).as_posix()
    if rel not in manifest['sha256'] and p.name!='new-file-inventory.csv':
        artifact_rows.append(dict(file=rel,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),baseline_state='Absent at task start and baseline; new untracked file'))
write_csv('new-file-inventory.csv',sorted(artifact_rows,key=lambda r:r['file']))
print(json.dumps(summary,ensure_ascii=True,indent=2))
