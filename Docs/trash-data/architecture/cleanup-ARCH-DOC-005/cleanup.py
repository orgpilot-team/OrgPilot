"""ARCH-DOC-005 navigation maintenance. Source decisions do not change."""
import csv, difflib, hashlib, io, json, os, re, subprocess, sys, zipfile
from pathlib import Path
from urllib.parse import unquote, quote
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
sys.path.insert(0,str(OUT.parent/'restructure-ARCH-DOC-004'))
from doc_links import anchors, active_text, markdown_links, inventory, resolve
ARCH='Docs/architecture/'
REG=ARCH+'registry/'
OLD=ARCH+'003-decisions-and-roadmap.md'
ROAD=ARCH+'003-roadmap.md'
SNAP=zipfile.ZipFile(OUT/'before-documents.zip')
def before(p):return SNAP.read(p).decode('utf-8-sig').replace('\r\n','\n')
def read(p):return (ROOT/p).read_text(encoding='utf-8-sig')
def put(p,s):(ROOT/p).write_text(s,encoding='utf-8',newline='\n')
def csv_out(name,rows,fields=None):
    with (OUT/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
def norm(s):
    s=re.sub(r'(?m)^(\s*)۲\. ',r'\g<1>2. ',s)
    s=re.sub(r'\]\([^\n]*?\)','](LINK)',s)
    s=re.sub(r'<a\b[^>]*></a>','',s)
    return ' '.join(s.split())

old_compat=before(OLD) # Read the complete compatibility document before removal.
legacy=list(csv.DictReader(io.StringIO(before(ARCH+'restructure-ARCH-DOC-004/legacy-anchor-map.csv'))))
legacy_map={r['legacy_anchor']:(r['target_file'],r['target_anchor']) for r in legacy}
assert anchors(old_compat)>=set(legacy_map)

heading_changes=[
 ('# ARCH-001: Implementation roadmap','# ARCH-001: نقشه راه پیاده‌سازی','roadmap-overview'),
 ('## ۴. اولویت پاسخ‌های لازم','## ۱. اولویت پاسخ‌های لازم','roadmap-prerequisites'),
 ('## ۶. مسیر مرحله‌ای پیاده‌سازی پس از بازبینی','## ۲. مسیر مرحله‌ای پیاده‌سازی پس از بازبینی','roadmap-phases'),
 ('### ۶.۱. کمترین مسیر سرتاسری قابل بررسی','### ۲.۱. کمترین مسیر سرتاسری قابل بررسی','roadmap-first-slice'),
 ('## ۸. اندازه‌گیری عملکرد و هزینه','## ۳. اندازه‌گیری عملکرد و هزینه','roadmap-measurement'),
 ('## Execution gate context retained from the former Decision Log','## ۴. شرایط شروع اجرای محصول','roadmap-execution-gates'),
 ('## Governance and delivery navigation','## ۵. مراجع حاکمیت و تحویل','roadmap-governance')]
anchor_changes={'decisions-4':'roadmap-prerequisites','decisions-6':'roadmap-phases','decisions-8':'roadmap-measurement','execution-gates':'roadmap-execution-gates'}
section_rows=[]
road=before(ROAD)
for old_heading,new_heading,new_anchor in heading_changes:
    assert old_heading in road
    for a in anchors(old_heading):anchor_changes[a]=new_anchor
    road=road.replace(old_heading,f'<a id="{new_anchor}"></a>\n\n{new_heading}',1)
    section_rows.append(dict(before_file=ROAD,before_heading=old_heading,after_file=ROAD,after_heading=new_heading,after_anchor=new_anchor,action='Heading and numbering only; body retained'))
road=re.sub(r'<a id="(?:decisions-[468]|execution-gates)"></a>\n\n','',road)
# Use one numbering style for the existing first implementation slice.
road=road.replace('\n2. مقدار `K_RSP_FRT_MED`','\n۲. مقدار `K_RSP_FRT_MED`')
put(ROAD,road)
csv_out('roadmap-section-map.csv',section_rows)

historical=list(csv.DictReader(io.StringIO(before(ARCH+'restructure-ARCH-DOC-004/historical-reference-catalog.csv'))))
historical_map={(r['source_file'],r['legacy_url']):r['current_file'] for r in historical}
repairs=[]
def new_href(origin,target,anchor=''):
    rel=os.path.relpath(ROOT/target,(ROOT/origin).parent).replace('\\','/')
    # Space encoding keeps ordinary, HTML and reference-style links parseable.
    return quote(rel,safe='/._-~()'+''.join(c for c in rel if ord(c)>127))+('#'+anchor if anchor else '')
def mapped_url(origin,url):
    if re.match(r'^(?:[A-Za-z][A-Za-z0-9+.-]*:|//)',url):return url,''
    target=resolve(ROOT,ROOT/origin,url)
    name,_,fragment=url.partition('#');fragment=unquote(fragment)
    if target['target']==OLD or unquote(name).replace('\\','/').rsplit('/',1)[-1]=='003-decisions-and-roadmap.md':
        if fragment:
            assert fragment in legacy_map,(origin,url)
            p,a=legacy_map[fragment]
        else:p,a=REG+'README.md','source-context'
        if p==ROAD:a=anchor_changes.get(a,a)
        return new_href(origin,p,a),'Old combined document: exact legacy-anchor destination'
    if target['target']==ROAD and fragment in anchor_changes:
        return new_href(origin,ROAD,anchor_changes[fragment]),'Roadmap heading or legacy section anchor'
    if (origin,url) in historical_map:
        return new_href(origin,historical_map[(origin,url)],fragment),'Previously reported historical broken reference; real target verified'
    return url,''

# Replace URL spans on each source line. Do not rewrite audit findings or code.
md_files=list(ROOT.rglob('*.md'))
for path in md_files:
    p=path.relative_to(ROOT).as_posix()
    if p==OLD or OUT in path.parents:continue
    src=read(p) if p==ROAD else before(p) if p in SNAP.namelist() else read(p)
    lines=src.splitlines(True);out=[]
    for n,line in enumerate(lines,1):
        changes=[]
        for (start,end),url,_,kind in markdown_links(line):
            new,reason=mapped_url(p,url)
            if new!=url:
                changes.append((start,end,new))
                repairs.append(dict(source_file=p,line=n,old_url=url,new_url=new,kind=kind,reason=reason))
        # A URL can be reported only once per span.
        for start,end,new in sorted(set(changes),reverse=True):line=line[:start]+new+line[end:]
        out.append(line)
    updated=''.join(out)
    # This visible section label accompanies the moved measurement destination.
    if p==ARCH+'002-data-architecture.md':updated=updated.replace('[سند 003، بخش 8]','[سند 003، بخش ۳]')
    if p==REG+'README.md':
        updated=updated.replace('The original 003 filename now serves as a compatibility index.','The former combined file has been removed after its content and references were checked. Use the current roadmap and Registry records.')
        updated+='\n## Current navigation maintenance\n\nARCH-DOC-005 repairs navigation only. Use the [cleanup report](../cleanup-ARCH-DOC-005/report.md) for current link checks and the section map. Earlier audit reports, hashes, source paths and generator scripts describe their historical snapshots. Their findings and status records remain evidence. Do not run an earlier extraction script against the current document layout.\n'
    if p=='Docs/review/team-guide-technical-review.md':
        updated=updated.replace('`docs/architecture/001-system-blueprint.md`، `002-data-architecture.md`، `003-decisions-and-roadmap.md`','[001](../architecture/001-system-blueprint.md)، [002](../architecture/002-data-architecture.md)، [Roadmap](../architecture/003-roadmap.md)، [Registry](../architecture/registry/README.md)')
    if p==ARCH+'audit-2026-11-09/change-report.md':
        updated=updated.replace('[003-decisions-and-roadmap.md]','[Current governance records; former combined source]')
    if updated!=src:put(p,updated)
csv_out('link-repairs.csv',repairs)

# The live matrix source fields are navigation. All semantic fields stay exact.
matrix=REG+'traceability-matrix.csv'
rows=list(csv.DictReader(io.StringIO(before(matrix))))
matrix_changes=[]
for i,r in enumerate(rows,2):
    p,a=r['source_file'],r['source_anchor']
    if p==OLD:
        p,a=legacy_map[a] if a else (REG+'README.md','source-context')
    if p==ROAD:a=anchor_changes.get(a,a)
    if (p,a)!=(r['source_file'],r['source_anchor']):
        matrix_changes.append(dict(row=i,record_id=r['record_id'],before_file=r['source_file'],before_anchor=r['source_anchor'],after_file=p,after_anchor=a))
        r['source_file'],r['source_anchor']=p,a
with (ROOT/matrix).open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
csv_out('matrix-navigation-changes.csv',matrix_changes)

# Verify original substantive source text against current readable documents.
original_zip=zipfile.ZipFile(ROOT/ARCH/'restructure-ARCH-DOC-004/before-documents.zip')
original=original_zip.read(OLD).decode('utf-8-sig').replace('\r\n','\n')
canonical=[ARCH+x for x in ['001-system-blueprint.md','002-data-architecture.md','003-roadmap.md','004-reconciliation-review.md']]+[REG+x for x in ['README.md','decisions-registry.md','open-issues-registry.md','risk-register.md','acceptance-register.md']]
live={p:norm(active_text(read(p))) for p in canonical}
content=[];missing=[]
for i,line in enumerate(original.splitlines(),1):
    value=norm(line)
    if not value or re.match(r'^\s*#{1,6}\s',line) or re.fullmatch(r'[| :\-]+',value):continue
    matches=[p for p,text in live.items() if value in text]
    if not matches:missing.append(i)
    content.append(dict(original_file=OLD,original_line=i,original_text=line,current_file=';'.join(matches),result='PASS' if matches else 'FAIL'))
csv_out('original-content-check.csv',content)
assert not missing,('Original content missing',missing)

# Verify all other incoming Markdown links before the requested deletion.
links=inventory(ROOT,[p for p in ROOT.rglob('*.md') if p!=ROOT/OLD])
assert not [r for r in links if r['target']==OLD], 'Incoming old-document link remains'
assert all(resolve(ROOT,ROOT/r['source_file'],r['new_url'])['state']=='Resolved' for r in repairs)
assert set(legacy_map)<=anchors(old_compat)
assert len(historical)==64

# Deletion is limited to the one obsolete file explicitly named by the task.
(ROOT/OLD).unlink(missing_ok=True)
print(json.dumps(dict(markdown_repairs=len(repairs),old_links_migrated=sum(r['reason'].startswith('Old combined') for r in repairs),historical_links_repaired=sum(r['reason'].startswith('Previously') for r in repairs),matrix_navigation_rows=len(matrix_changes),original_source_lines=len(content),obsolete_file_removed=not (ROOT/OLD).exists()),indent=2))
