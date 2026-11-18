"""Move documentation by source slice. Do not run product code or old generators."""
from pathlib import Path
from urllib.parse import unquote, quote
import csv, hashlib, io, json, os, re, sys, zipfile
from doc_links import anchors, active_text

sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];ARCH=OUT.parent;REG=ARCH/'registry'
D1='Docs/architecture/001-system-blueprint.md';D2='Docs/architecture/002-data-architecture.md'
D3='Docs/architecture/003-decisions-and-roadmap.md';D4='Docs/architecture/004-reconciliation-review.md'
ROAD='Docs/architecture/003-roadmap.md';RR='Docs/architecture/registry/'
pre=json.loads((OUT/'before-manifest.json').read_text(encoding='utf-8'))
backup=zipfile.ZipFile(OUT/'before-documents.zip')
def before(p):return backup.read(p).decode('utf-8-sig').replace('\r\n','\n')
def put(p,s):(ROOT/p).write_text(s.rstrip()+'\n',encoding='utf-8')
def source_sha(s):return hashlib.sha256(s.encode('utf-8')).hexdigest()
src=before(D3)
def cut(a,b=None):
    start=src.index(f'<a id="{a}"></a>')
    end=src.index(f'<a id="{b}"></a>',start+1) if b else len(src)
    return src[start:end].strip()
sections={f'decisions-{n}':cut(f'decisions-{n}',f'decisions-{n+1}' if n<9 else 'decision-log' if n==9 else None) for n in range(1,11)}
sections['decisions-10']=cut('decision-log')
preface=src[:src.index('<a id="decisions-1"></a>')].strip()
canonical={
 'decisions-1':(RR+'README.md','decisions-1'),'decisions-2':(RR+'README.md','decisions-2'),
 'decisions-3':(RR+'decisions-registry.md','decisions-3'),'decisions-4':(ROAD,'decisions-4'),
 'decisions-5':(RR+'risk-register.md','decisions-5'),'decisions-6':(ROAD,'decisions-6'),
 'decisions-7':(RR+'acceptance-register.md','decisions-7'),'manager-question-map':(RR+'acceptance-register.md','manager-question-map'),
 'decisions-8':(ROAD,'decisions-8'),'decisions-9':(D4,'decisions-9'),
 'decision-log':(RR+'open-issues-registry.md','decision-log'),'decisions-10':(RR+'open-issues-registry.md','decisions-10')}
canonical.update({f'adr-{n:02d}':(RR+'decisions-registry.md',f'adr-{n:02d}') for n in range(1,18)})
canonical.update({f'at-{n:02d}':(RR+'acceptance-register.md',f'at-{n:02d}') for n in range(1,31)})

def href(origin,p,a=''):
    rel=Path(os.path.relpath(ROOT/p,(ROOT/origin).parent)).as_posix()
    return quote(rel,safe='/._-()')+('#'+a if a else '')

def rewrite_old_links(s,origin):
    """Change active destinations only. Quoted code/evidence stays byte-for-byte."""
    result=[];fenced=False
    for line in s.splitlines(True):
        if re.match(r'^\s*```',line):fenced=not fenced;result.append(line);continue
        if fenced:result.append(line);continue
        def sub(m):
            p,a=m[1],m[2] or ''
            resolved=((ROOT/origin).parent/unquote(p)).resolve()
            if resolved!=(ROOT/D3).resolve():return m[0]
            target=canonical.get(a,(ROAD,''))
            return href(origin,*target)
        line=re.sub(r'(?<=\]\()([^\s)]*003-decisions-and-roadmap\.md)(?:#([^\s)]+))?(?=\))',sub,line)
        result.append(line)
    return ''.join(result)

def moved_links(s,origin):
    # Relative links in retained source were written relative to old 003.
    def sub(m):
        url=m[1]
        if re.match(r'\w+:|//',url):return m[0]
        name,_,a=url.partition('#')
        p=(ARCH/unquote(name)).resolve() if name else ROOT/D3
        if p==ROOT/D3:
            target=canonical.get(a,(ROAD,''));return ']('+href(origin,*target)+')'
        return ']('+href(origin,p.relative_to(ROOT).as_posix(),a)+')'
    return re.sub(r'\]\(([^)\s]+)\)',sub,s)

extract_changes=[]
def readable(name,kind):
    original=before(RR+name)
    seen=set(re.findall(r'<a id="([^"]+)"',active_text(original)))
    def sub(m):
        raw=m[1]
        if kind=='DL' and not re.match(r'\s*\| DL-\d{2}',raw):return m[0]
        # Data-model and other source quotes remain evidence, not a second data contract.
        body=moved_links(raw,RR+name)
        def uniq(a):
            id=a[1]
            if id in seen:return ''
            seen.add(id);return a[0]
        body=re.sub(r'<a id="([^"]+)"></a>',uniq,body)
        if re.match(r'\s*\|',body):
            if kind=='AT':head='| شناسه | آزمون | معیار پذیرش |\n|---|---|---|\n'
            elif kind=='Risk':head='| ریسک | اثر | اقدام و نشانهٔ کنترل |\n|---|---|---|\n'
            else:head='| شناسه و بازبینی | محل منابع | تعارض یا انتخاب مفقود | گزینه‌ها و اثر معماری | مالک و آزمون پذیرش | Evidence لازم برای بسته‌شدن |\n|---|---|---|---|---|---|\n'
            body=head+body
        extract_changes.append(dict(registry_file=RR+name,source_kind=kind,source_text_sha256=source_sha(raw),source_characters=len(raw),
                                    action='Promoted exact source text to readable Markdown; links rebased; duplicate explicit source anchors removed.'))
        return '\n### Full source record and conditions\n\n'+body.strip()+'\n'
    pattern=r'<details><summary>Source extract \(unchanged text\)</summary>\s*\n```text\n(.*?)\n```\s*\n</details>'
    updated=re.sub(pattern,sub,original,flags=re.S)
    expected={'ADR':17,'AT':37,'DL':19,'Risk':12}[kind]
    actual=sum(x['registry_file']==RR+name for x in extract_changes)
    assert actual==expected,(name,actual,expected)
    note=('\nDocumentation location: team-designated governance record. State: **Draft / Pending Review**. '
          'The full source records and criteria below are readable Markdown. English text is an index. '
          'The structural approval changes no decision, source rule, risk assessment or acceptance result.\n')
    updated=updated.replace('\n\n','\n'+note+'\n',1)
    return rewrite_old_links(updated,RR+name)

# Make all governance records usable before touching original 003.
docs={
 RR+'decisions-registry.md':readable('decisions-registry.md','ADR'),
 RR+'open-issues-registry.md':readable('open-issues-registry.md','DL'),
 RR+'risk-register.md':readable('risk-register.md','Risk'),
 RR+'acceptance-register.md':readable('acceptance-register.md','AT')}
adr_intro=sections['decisions-3'][:sections['decisions-3'].index('<a id="adr-01"></a>')]
docs[RR+'decisions-registry.md']+='\n\n'+moved_links(adr_intro,RR+'decisions-registry.md')+'\n'
docs[RR+'risk-register.md']+='\n\n<a id="decisions-5"></a>\n\n## ۵. ریسک‌های عمده و اقدام کنترل\n\nThe original 13 source risk rows are retained in the 20 risk records above. The two SQL/oracle rows share REG-RSK-004. No control is implemented and every severity remains Not Assessed.\n'

# Preserve strategy/authority paragraphs that were not part of individual AT rows.
s7=sections['decisions-7'];first=s7.index('| <a id="at-01"></a>')
strategy=s7[:first]
lastline=next(l for l in s7.splitlines() if l.startswith('| <a id="at-30"></a>'))
after_rows=s7[s7.index(lastline)+len(lastline):s7.index('#### تکمیل معیارهای آزمون موجود')]
docs[RR+'acceptance-register.md']+='\n\n'+moved_links(strategy,RR+'acceptance-register.md')+'\n\n<a id="acceptance-authority-notes"></a>\n\n'+moved_links(after_rows,RR+'acceptance-register.md')+'\n'
# A header with no rows at the end of the strategy is not a second AT table.
docs[RR+'acceptance-register.md']=docs[RR+'acceptance-register.md'].replace('| شناسه | آزمون | معیار پذیرش |\n|---|---|---|\n\n\n<a id="acceptance-authority-notes">','<a id="acceptance-authority-notes">')
docs[RR+'acceptance-register.md']=docs[RR+'acceptance-register.md'].replace('### ۷.۳. آزمون‌های مرزی و خصمانه','<a id="boundary-cases"></a>\n\n### ۷.۳. آزمون‌های مرزی و خصمانه')

# Full open-scope paragraph belongs to the existing issue, not a new ADR.
s6=sections['decisions-6']
scope_para=next(p for p in s6.split('\n\n') if p.startswith('برچسب بررسی `Open Decision`:'))
delivery_para=next(p for p in s6.split('\n\n') if p.startswith('تکمیل شرط تحویل P5'))
issue_path=RR+'open-issues-registry.md'
insertion='\n\n### Full source context for REG-ISS-001\n\n'+moved_links(scope_para,issue_path)+'\n\n'
pos=docs[issue_path].index('<a id="reg-iss-002"></a>')
docs[issue_path]=docs[issue_path][:pos]+insertion+docs[issue_path][pos:]
log=sections['decisions-10'];log_intro=log[:log.index('| شناسه و بازبینی |')]
docs[issue_path]+='\n\n'+moved_links(log_intro,issue_path)+'\n\nRead the full DL-01 through DL-19 records above. Their source rows retain all original options, roles and gates. The roles remain proposed roles, not appointed people.\n'

readme=before(RR+'README.md')
readme=readme.replace('This Registry extracts decisions, Open issues, risks and acceptance criteria from the local ARKA architecture baseline. It makes no architecture choice and grants no implementation authority. Document 003 and the existing source records remain in place. Team review must occur before any content transfer or reference migration.',
 'The team designates this Registry as the documentation location for architecture decisions, unresolved issues, risks, acceptance tests and traceability. ARCH-DOC-004 approves a source-preserving structural reorganization only. This designation approves no Open choice, Proposed mechanism, inferred link, missing contract or product test result. The original 003 filename now serves as a compatibility index.')
readme=readme.replace('English text provides the Registry index. Exact source extracts retain the supplied Persian text, all numbers, conditions and exceptions. Text inside source extract blocks is quoted evidence. Its old link strings are inert. The active Source Evidence link points to the real original file and existing anchor. Do not interpret text inside a quoted extract as a new Registry instruction or status change.',
 'English text provides the Registry index. Full ADRs, DL source rows, risk conditions, AT criteria and supplemental matrices are now readable Markdown. Their original source language, numbers, conditions and exceptions are retained. Relative navigation links are rebased. Other quoted data-model extracts remain historical evidence; 002 keeps the data contracts. Former source links through 003 use its compatibility anchors. The before snapshot and content-location map preserve exact origin evidence.')
readme=readme.replace('For ARCH-REG-002, only the S01 provenance metadata in 001 and 004 can change outside this folder. All other original source bytes remain unchanged. Before bytes, exact corrections and after hashes are retained in audit-ARCH-REG-002/. No implementation, source rewrite, rename, commit or push is part of this task.',
 'ARCH-REG-002 provenance checks and ARCH-REG-003 triage are historical snapshots. ARCH-DOC-004 changes documentation locations and active navigation only. All original records, source conditions and limitations remain. No product implementation, Dataset/SQL/DSL change, commit or push is part of the reorganization.')
readme=readme.replace('The ARCH-REG-001 build/check scripts are frozen as historical tools. Use [validate_semantic_audit.py](audit-ARCH-REG-002/validate_semantic_audit.py) for current read-only checks. No old generator should replace this reviewed extraction.',
 'All earlier generators, audit scripts and validation outputs belong to their recorded snapshots. Do not run an old generator over the reorganized sources. Use the [ARCH-DOC-004 validation](../restructure-ARCH-DOC-004/validate_restructure.py) for the current structure. No old verification result approves the current layout or product.')
readme=rewrite_old_links(readme,RR+'README.md')
source_context=moved_links(preface+'\n\n'+sections['decisions-1']+'\n\n'+sections['decisions-2'],RR+'README.md')
source_context=source_context.replace('# ARCH-001:', '### Former 003 source title: ARCH-001:',1)
readme+='''\n\n## Current document responsibilities

| Location | Responsibility |
|---|---|
| [001](../001-system-blueprint.md) | System architecture, modules, Workflows, interfaces and security. |
| [002](../002-data-architecture.md) | Data model, intake, snapshots, canonical calculations and lineage. |
| [003 roadmap](../003-roadmap.md) | Proposed phases, milestones, gates, measured execution and delivery sequence. |
| [004](../004-reconciliation-review.md) | Historical reconciliation, source authority and Q01-Q17 evidence. |
| This Registry | Governance records, full acceptance criteria and traceability. |

Location designation is approved. Record state remains **Draft / Pending Review**. The five Accepted boundaries remain fixed. All 29 issues stay Open. All 30 ATs stay Planned / Not Executed. All 20 risk severities stay Not Assessed. All 2,470 inferred links stay unconfirmed. Source/evaluation contracts are not invented. A navigation update is not an implementation dependency.

The [triage queue](traceability-review-queue.csv), [readiness note](approval-readiness.md) and previous audit reports retain their historical conclusions. The present user approval supersedes only the earlier structural-authorization prerequisite. It does not approve their unresolved semantic content. No earlier audit evidence file is edited.

Read the [reorganization report](../restructure-ARCH-DOC-004/report.md), [complete content-location map](../restructure-ARCH-DOC-004/content-location-map.csv) and [historical reference catalog](../restructure-ARCH-DOC-004/historical-reference-catalog.md).

<a id="source-context"></a>

## Retained source context

The following original text preserves source rules, boundaries and metadata from the former 003. Its document identifier and references to the audit describe that source snapshot. The current Decision Log is [here](open-issues-registry.md#decision-log). The current roadmap is [here](../003-roadmap.md).
\n'''+source_context+'\n'
docs[RR+'README.md']=readme

# Full roadmap with references to the single designated governance records.
road_sections=s6.replace(scope_para,'The P2/P3 scope remains Open in [REG-ISS-001](registry/open-issues-registry.md#reg-iss-001). Its full original alternatives, source pages and closure conditions are retained there. No phase choice is made by this structural task.')
road_sections=road_sections.replace(delivery_para,'The complete P5 delivery supplement is retained as [the AT-19 delivery checklist](registry/acceptance-register.md#delivery-checklist). It includes all required UI, source-history, guide, cost and Demo Day items. The phase table and delivery gate remain Proposed as originally stated.')
last_scope=log.splitlines()[-1]
roadmap='''# ARCH-001: Implementation roadmap

Document key: `003-roadmap`. Date: 2026-11-09. Time zone: `Asia/Tehran`.

Status: **Proposed roadmap; Open choices retained**. The team approves this documentation location, not a phase choice, technical mechanism or test result. Implementation and acceptance have not been demonstrated here.

This document contains phases, milestones, prerequisite questions, exit gates, the first end-to-end slice and measurement/delivery sequence. The [Registry](registry/README.md) contains ADRs, issues, risks and full acceptance criteria. Use [001](001-system-blueprint.md) and [002](002-data-architecture.md) for the system and data contracts. [004](004-reconciliation-review.md) retains historical reconciliation evidence.

No phase or execution dependency is inferred from unconfirmed traceability links. The P0 design gates below apply only to affected work. The Accepted Agent, database, publication, deterministic and human-action boundaries are not reopened.

'''+sections['decisions-4']+'\n\n'+road_sections+'\n\n'+sections['decisions-8']+'''\n\n<a id="execution-gates"></a>

## Execution gate context retained from the former Decision Log

'''+last_scope+'''\n\n## Governance and delivery navigation

- [Architecture decisions](registry/decisions-registry.md).
- [Open choices and missing evidence](registry/open-issues-registry.md).
- [Risk controls](registry/risk-register.md).
- [All 30 acceptance tests and full supplemental criteria](registry/acceptance-register.md).
- [Historical verification statement from former 003](004-reconciliation-review.md#decisions-9).

The AT-26 three-level matrix and R1-R8 acceptance cases remain mandatory where the source requires them. Monthly board summary remains optional. Reference definitions and all original numerical limits remain unchanged. A document check is not product acceptance.
'''
docs[ROAD]=rewrite_old_links(roadmap,ROAD)

for p in [D1,D2]:
    updated=rewrite_old_links(before(p),p)
    role=('System architecture, modules, Workflows, interfaces and security remain in this document.' if p==D1 else
          'Data model, ingestion, snapshots, canonical calculations and lineage remain in this document.')
    note='\nDocumentation responsibility, ARCH-DOC-004: '+role+' Use the [Registry](registry/README.md) for governance records and [003 roadmap](003-roadmap.md) for execution phases. This structural navigation changes no contract or status.\n'
    first_blank=updated.index('\n\n')
    updated=updated[:first_blank]+ '\n'+note+updated[first_blank:]
    docs[p]=updated
review=rewrite_old_links(before(D4),D4)
review+='''\n\n## Historical verification text retained from former 003

The following is historical source evidence from the former combined document. Statements about Git refer to that review context. They do not describe the current repository. Only navigation destinations are updated. No audit conclusion is rewritten.
\n'''+rewrite_old_links(sections['decisions-9'],D4)+'\n'
docs[D4]=review

# Before deleting anything, prove the original records exist as active Markdown.
def norm(s):
    s=re.sub(r'\]\(([^)\s]+)\)','](LINK)',s)
    s=re.sub(r'<a id="[^"]+"></a>','',s)
    return ' '.join(s.split())
for n in range(1,18):
    id=f'adr-{n:02d}';chunk=cut(id,f'adr-{n+1:02d}' if n<17 else 'decisions-4')
    assert norm(chunk) in norm(active_text(docs[RR+'decisions-registry.md'])),id
for line in src.splitlines():
    if line.startswith('| DL-'):assert norm(line) in norm(active_text(docs[issue_path])),line[:10]
    if re.match(r'\| <a id="at-\d{2}',line):assert norm(line) in norm(active_text(docs[RR+'acceptance-register.md'])),line[:40]
for p,s in docs.items():put(p,s)

# Legacy explicit and implicit anchors remain as navigation only.
legacy=anchors(src)
explicit=re.findall(r'<a id="([^"]+)"',src)
def location_for_line(line_number):
    line=src.splitlines()[line_number-1]
    before_line='\n'.join(src.splitlines()[:line_number]);current=None
    ids=re.findall(r'<a id="([^"]+)"',before_line)
    current=ids[-1] if ids else None
    if line==scope_para:return issue_path,'reg-iss-001'
    if line==delivery_para:return RR+'acceptance-register.md','delivery-checklist'
    if line==last_scope:return ROAD,'execution-gates'
    # Within section 7, use the exact shared criterion section instead of at-30.
    if src.index('<a id="decisions-7">')<=len(before_line)<src.index('<a id="decisions-8">'):
        offset=len(before_line)
        marks=[('#### تکمیل معیارهای آزمون موجود','supplement-tests'),('#### ماتریس محتوای اختصاصی','role-matrix'),
               ('#### موارد اختصاصی قواعد','rule-matrix'),('### ۷.۱.','oracle-boundaries'),('<a id="manager-question-map">','manager-question-map'),
               ('### ۷.۳.','boundary-cases')]
        selected=[(src.index(marker),a) for marker,a in marks if src.index(marker)<=offset]
        if selected:return RR+'acceptance-register.md',max(selected)[1]
    return canonical.get(current,(RR+'README.md','source-context'))

alias_targets={a:canonical[a] for a in explicit}
for i,line in enumerate(src.splitlines(),1):
    if re.match(r'^#{1,6}\s',line):
        for a in anchors(line):alias_targets.setdefault(a,location_for_line(i))
assert set(alias_targets)==legacy,(set(alias_targets)^legacy)
compat=['# 003 compatibility navigation','',
        'This file preserves historical file and anchor links. It contains no active ADR, issue, risk, test or phase record. Use the designated locations below.',
        '', 'Former document key: `003-decisions-and-roadmap`. Architecture family: `ARCH-001`.',
        '', 'The team approves documentation locations only. All Open/Proposed limitations remain. See the [roadmap](003-roadmap.md) and [Registry](registry/README.md).',
        '', '| Legacy anchor | Designated documentation location |','|---|---|']
for a in sorted(legacy):
    p,target=alias_targets[a]
    compat.append(f'| <a id="{a}"></a>`{a}` | [Open current location]({href(D3,p,target)}) |')
put(D3,'\n'.join(compat))

# Update live matrix source locations only. Pair identities, types, statuses and
# all 2,470 unconfirmed relationship classes remain unchanged.
oldmatrix=list(csv.DictReader(io.StringIO(before(RR+'traceability-matrix.csv'))));newmatrix=[];nav_changes=[]
for old in oldmatrix:
    r=dict(old)
    if r['source_file']==D3:
        p,a=canonical.get(r['source_anchor'],(ROAD,''))
        if r['record_id']=='REG-ISS-001' and r['source_anchor']=='decisions-6':p,a=issue_path,'reg-iss-001'
        if r['record_id']=='REG-ISS-006' and r['source_anchor']=='decisions-6':p,a=RR+'acceptance-register.md','delivery-checklist'
        if r['record_type']=='Risk' and r['source_anchor']=='decisions-5':p,a=RR+'risk-register.md',r['record_id'].lower()
        r['source_file']=p;r['source_anchor']=a
        r['source_ref']=f'ARCH-DOC-004 source location; original {old["source_file"]}#{old["source_anchor"]}; '+old['source_ref']
        nav_changes.append(dict(record_id=r['record_id'],row_kind=r['row_kind'],old_file=old['source_file'],old_anchor=old['source_anchor'],new_file=p,new_anchor=a))
    newmatrix.append(r)
with (ROOT/RR/'traceability-matrix.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(oldmatrix[0]));w.writeheader();w.writerows(newmatrix)

for filename,rows in [('source-extract-promotion.csv',extract_changes),('matrix-navigation-changes.csv',nav_changes)]:
    with (OUT/filename).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with (OUT/'legacy-anchor-map.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['legacy_file','legacy_anchor','target_file','target_anchor']);w.writeheader()
    for a,(p,target) in sorted(alias_targets.items()):w.writerow(dict(legacy_file=D3,legacy_anchor=a,target_file=p,target_anchor=target))
print(json.dumps(dict(readable_source_blocks=len(extract_changes),legacy_anchors=len(legacy),matrix_navigation_rows=len(nav_changes),files_written=list(docs)+[D3,RR+'traceability-matrix.csv']),indent=2))
