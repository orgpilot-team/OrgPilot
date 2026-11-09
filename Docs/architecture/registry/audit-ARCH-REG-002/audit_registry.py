"""Narrow Registry corrections and source-aware documentation checks.

Run from the repository root. Original before bytes are in before-files.zip.
No product code or acceptance test is executed.
"""
from pathlib import Path
from collections import Counter, defaultdict
import ast, copy, csv, difflib, hashlib, json, re, subprocess, sys, zipfile
from urllib.parse import unquote

sys.stdout.reconfigure(encoding='utf-8')
AUD=Path(__file__).resolve().parent
REG=AUD.parent
ROOT=REG.parents[2]
BASE='0a42950d1ce9734433d961540af9ab4be21573b2'
D1='Docs/architecture/001-system-blueprint.md'
D2='Docs/architecture/002-data-architecture.md'
D3='Docs/architecture/003-decisions-and-roadmap.md'
D4='Docs/architecture/004-reconciliation-review.md'
PDF='Docs/بریف پروژه بوتکمپ _ دستیار ایجنتیک مدیران سازمانی _ دیدراه.pdf'
OLD='6d68d3fcc285f6908af0d97c0429dfefb489f00b7f6538ed03573552ed6955f8'
CURRENT=hashlib.sha256((ROOT/PDF).read_bytes()).hexdigest()
assert CURRENT=='f6761b4fc37145d152f2b9793b298e35f48db666d5205c4d02be0f5f13e4863b'
pre=json.loads((AUD/'before-manifest.json').read_text(encoding='utf-8'))
archive=zipfile.ZipFile(AUD/'before-files.zip')
def original(path): return archive.read(path).decode('utf-8-sig').replace('\r\n','\n')
def text(path): return (ROOT/path).read_text(encoding='utf-8-sig')
def put(path,content): (ROOT/path).write_text(content.rstrip()+'\n',encoding='utf-8')
def regpath(name): return 'Docs/architecture/registry/'+name
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def dump_csv(path,data,fields=None):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(data[0]));w.writeheader();w.writerows(data)
def git(*args):
    p=subprocess.run(['git','-c','core.quotepath=false',*args],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
    return dict(code=p.returncode,out=p.stdout,err=p.stderr)
def strip_quotes(s): return re.sub(r'^```[^\n]*\n.*?^```\s*$', '',s,flags=re.M|re.S)
def sect(s,id):
    start=s.index(f'<a id="{id}"></a>');m=re.search(r'\n<a id="[^\"]+"></a>',s[start+1:])
    return s[start:start+1+m.start()] if m else s[start:]
def expand_ids(s,prefix):
    result=set()
    for m in re.finditer(r'\b'+prefix+r'-(\d{2}(?:\s*[/,،]\s*\d{2})*)',s):
        result.update(prefix+'-'+n for n in re.findall(r'\d{2}',m.group(1)))
    return result

corrections=[]
def correction(kind,id,before,after,reason,source):
    corrections.append(dict(correction_id=f'COR-{len(corrections)+1:04d}',kind=kind,record_id=id,
                            before=before,after=after,reason=reason,source_evidence=source))

# Change only the current/historical provenance metadata in the two protected files.
d1=original(D1)
oldline=next(x for x in d1.splitlines() if x.startswith('hash منشأ S01:'))
newline=(f'S01 current official PDF SHA-256: `{CURRENT}`. ARCH-REG-002: the user confirms the existing local PDF as the source of record. '
         f'Historical recorded SHA-256: `{OLD}`. The earlier review attributed content agreement to its reviewed PDF and S18. '
         'That historical comparison has not been verified for these exact current bytes. Different hashes do not establish changed requirements. REG-ISS-010 retains the historical comparison evidence gap.')
put(D1,d1.replace(oldline,newline))
correction('Provenance metadata','S01 / 001',oldline,newline,'Use the user-confirmed local PDF identity; preserve the old hash and the historical-comparison limit.','ARCH-REG-002 request section 1; direct PDF byte hash')
d4=original(D4)
oldrow=f'| S01 current brief PDF | `{OLD}` |'
newrow=(f'| S01 current official brief PDF, confirmed in ARCH-REG-002 | `{CURRENT}` |\n'
        f'| S01 historical hash recorded by the prior review | `{OLD}` |')
assert oldrow in d4
note=('\nS01 provenance metadata, ARCH-REG-002: the user confirms the existing local PDF as the current source of record. '
      'The PDF review statements below describe historical review work. They are not a fresh content comparison for the current byte identity. '
      'The historical PDF version has not been recovered for comparison. A hash difference alone does not establish a requirement change. REG-ISS-010 remains Open for that evidence gap.\n')
put(D4,d4.replace(oldrow,newrow).replace('\nS01 was highlighted and resaved.',note+'\nS01 was highlighted and resaved.'))
correction('Provenance metadata','S01 / 004',oldrow,newrow+note,'Distinguish the current source identity from the historical review claim.','ARCH-REG-002 request section 1; direct PDF byte hash')

path=regpath('traceability-matrix.csv')
oldrows=list(csv.DictReader(original(path).splitlines()))
fields=list(oldrows[0]);rows=copy.deepcopy(oldrows)
before_counts=dict(rows=len(rows),kinds=dict(Counter(r['row_kind'] for r in rows)),records=dict(Counter(r['record_type'] for r in rows if r['row_kind']=='record')))
for r in rows:
    if r['record_id'].startswith('DEC-') and r['record_type']=='Requirement':
        before=r['record_type'];r['record_type']='Decision Boundary'
        correction('Record classification',r['record_id'],before,r['record_type'],'The source classification is Accepted. A team choice is not a Requirement. Only the record type changes; ID and status stay fixed.',r['source_file']+' / '+r['source_ref'])

def main(id): return next(r for r in rows if r['record_id']==id and r['row_kind']=='record')
def newrow(id,typ,title,status,p,a='',ref='',kind='record',**kw):
    r=dict.fromkeys(fields,'');r.update(record_id=id,record_type=typ,title=title,status=status,source_file=p,source_anchor=a,source_ref=ref,
                                    row_kind=kind,evidence_state='Evidence Pending',source_tracking='Untracked at audit start' if p in pre['untracked'] else 'Tracked baseline')
    r.update(kw);return r
def add(r,reason):
    if r not in rows:
        rows.append(r);correction('Added index row',r['record_id'],'Missing',json.dumps(r,ensure_ascii=False),reason,r['source_file']+'#'+r['source_anchor']+' / '+r['source_ref'])
def edge(source,target,typ,p,a,ref,rel='references',proposed=False):
    rec=main(source)
    kw=dict(target_id=target,target_type=typ,relationship_type=rel,relationship_status='Proposed Relationship' if proposed else 'Documented')
    f={'ADR':'related_adr','DL':'related_dl','AT':'related_at','Risk':'related_risk','Architecture Component':'architecture_component','Roadmap Phase':'roadmap_phase'}.get(typ)
    if f:kw[f]=target
    return newrow(source,rec['record_type'],rec['title'],rec['status'],p,a,ref,'relationship',**kw)
def has_edge(s,t,typ):return any(r['row_kind']=='relationship' and r['record_id']==s and r['target_id']==t and r['target_type']==typ for r in rows)

# Add actual main records for endpoints that the old checker accepted as virtual IDs.
known={r['record_id'] for r in rows if r['row_kind']=='record'}
component_ids={r['target_id'] for r in rows if r['target_type']=='Architecture Component'}
dslpath='architecture/structurizr/workspace.dsl';dsl=text(dslpath)
for id in sorted(component_ids-known):
    m=re.search(r'^\s*'+re.escape(id)+r'\s*=\s*(component|container|softwareSystem)\b[^\n]*',dsl,re.M)
    assert m,id
    add(newrow(id,'Architecture Component',id,'Target model; not implemented',dslpath,ref=f'Line {dsl[:m.start()].count(chr(10))+1}; {m.group(0).strip()}',evidence_state='Model documented'),
        'Declare the existing DSL endpoint in the index. Do not create or change a model element.')
sup={'supplement-tests':('AT supplements','decisions-7'),'role-matrix':('Three-level content matrix','decisions-7'),
     'rule-matrix':('R1-R8 cases','decisions-7'),'oracle-boundaries':('Oracle boundaries','decisions-7'),
     'input-and-negative-cases':('Manager inputs and negative cases','manager-question-map'),
     'measurement':('Performance and cost measurement','decisions-8'),'delivery-checklist':('P5 delivery checklist','decisions-6')}
for id,(title,a) in sup.items():
    add(newrow(id,'Acceptance Supplement',title,'Planned / Not Executed',D3,a,title,registry_file='acceptance-register.md',registry_anchor=id),
        'Declare the existing local supplement endpoint. The criteria already exist; no new acceptance gate is created.')

# Imported audit mappings are documentary suggestions, not proof of substantive
# dependency. Retain their provenance, but remove the blanket approval implication.
reqpath='Docs/architecture/audit-2026-11-09/requirements-traceability.csv'
for r in rows:
    if r['row_kind']=='relationship' and r['source_file']==reqpath and r['relationship_type']=='references':
        r['relationship_status']='Proposed Relationship'
        correction('Relationship classification',r['record_id'],r['target_id']+' / Documented',
                   r['target_id']+' / Proposed Relationship',
                   'The audit CSV supplies a proposed mapping. ID presence and source location alone do not prove that this ADR/test/component addresses the exact requirement.',
                   reqpath+' / '+r['record_id']+' -> '+r['target_id'])

# Remove only clear wrong mappings. Keep all removed rows with before bytes in
# the correction ledger. Record identities and source extracts are never removed.
wrong={('REQ-13','ADR-10'):'Accuracy thresholds are not addressed by the model/budget ADR.',
       ('REQ-CONF-02','ADR-10'):'Priority selection/report emphasis is not the model/budget choice.',
       ('REQ-INPUT-IN01','ADR-10'):'IN01 is a priority input, not a model or cost policy.',
       ('REQ-DEL-03','ADR-12'):'Git source history delivery is not data retention/backup.',
       ('REQ-JSON-QA-ROOT','ADR-14'):'The QA root field schema is not independent manager-report publication.'}
unsupported=[]
retained=[]
for r in rows:
    key=(r['record_id'],r['target_id'])
    if r['row_kind']=='relationship' and key in wrong:
        unsupported.append(r)
        correction('Unsupported edge removed',r['record_id'],json.dumps(r,ensure_ascii=False),'Removed from active matrix; retained in audit ledger',wrong[key],reqpath+'; '+D3+'#'+r['target_id'].lower())
    else:retained.append(r)
rows=retained

# Restore compressed ADR references by looking only in each actual DL row,
# rather than scanning an entire section for ID co-occurrence.
d3=text(D3);dlraw={}
for line in d3.splitlines():
    if re.match(r'\| DL-\d{2}',line):dlraw[line[2:7]]=line
for id,raw in dlraw.items():
    for adr in expand_ids(raw,'ADR'):
        if not has_edge(id,adr,'ADR'):
            add(edge(id,adr,'ADR',D3,'decision-log',id+'; explicit compressed ADR list'), 'Restore a compressed ADR reference from this exact DL row.')
        if not has_edge(adr,id,'DL'):
            add(edge(adr,id,'DL',D3,'decision-log',id+'; explicit compressed ADR list','has_open_detail'),'Restore the ADR-to-unresolved-detail inverse.')

# Every high-impact record has a reviewed topic and mapping. These source sections
# name the same subject. Issue references that only co-occur in a broad section
# remain inferred instead of being treated as explicit semantic proof.
for r in rows:
    if r['record_type']=='Registry Issue' and r['row_kind']=='relationship' and r['relationship_status']=='Documented':
        if r['record_id'] not in ['REG-ISS-001','REG-ISS-006','REG-ISS-009']:
            before=r['relationship_status'];r['relationship_status']='Proposed Relationship'
            correction('Relationship classification',r['record_id'],r['target_id']+' / '+before,r['target_id']+' / Proposed Relationship',
                       'The issue is an extraction finding. The cited broad source section does not explicitly assign every endpoint to this new issue ID.',r['source_file']+'#'+r['source_anchor'])
        if r['record_id']=='REG-ISS-001' and r['target_type']=='ADR':
            r['relationship_status']='Proposed Relationship'
            correction('Relationship classification','REG-ISS-001','ADR-15 / Documented','ADR-15 / Proposed Relationship','The P2/P3 note names AT-12/15/25/26 but does not explicitly assign ADR-15.',D3+'#decisions-6')

# Add missing acceptance links only from source passages which exercise the issue.
# They remain review aids when the source does not explicitly give this issue ID.
missing_tests=[('ADR-13','AT-28',D1,'system-4',False),
 ('DL-08','AT-25',D3,'adr-15',True),('DL-09','AT-24',D3,'adr-07',True),
 ('DL-12','AT-29',D3,'adr-17',True),('DL-13','AT-28',D3,'at-28',True),
 ('DL-14','AT-28',D1,'system-4',True),('DL-19','AT-27',D3,'decision-log',False)]
for s,t,p,a,inferred in missing_tests:
    if not has_edge(s,t,'AT'):
        add(edge(s,t,'AT',p,a,'Specific contract and acceptance criterion','references',inferred),'Restore the relevant explicit gate or label the proposed issue-to-test cross-reference.')

# Add direct actual-source evidence for every original source-matrix record.
qrows=list(csv.DictReader((ROOT/reqpath).open(encoding='utf-8-sig',newline='')))
def actual(p):
    if p.startswith('dataset/'):return 'DataSet/arka_dataset/'+p[len('dataset/'):]
    if p.startswith('Project_berif/'):return 'Docs/'+p[len('Project_berif/'):]
    if p.startswith('docs/'):return 'Docs/'+p[len('docs/'):]
    return p
source_checks=[]
for q in qrows:
    p=actual(q['source_path']);assert (ROOT/p).is_file(),p
    rec=main(q['requirement_id'])
    add(newrow(rec['record_id'],rec['record_type'],rec['title'],rec['status'],p,ref=q['source_location']+'; original path: '+q['source_path'],kind='evidence'),
        'Add the current local contract path while retaining the audit row and original location.')
    content=text(p);loc=q['source_location'];result='File exists; narrative meaning needs reviewer inspection'
    if p.endswith('.json') and loc.startswith('/'):
        obj=json.loads(content)
        if loc!='/':
            for key in loc.strip('/').split('/'):
                key=key.replace('~1','/').replace('~0','~')
                obj=obj[int(key)] if isinstance(obj,list) else obj[key]
        result='JSON pointer resolves; no semantic pass inferred'
    elif p.endswith('.csv') and re.match(r'record \d+',loc):
        number=int(re.match(r'record (\d+)',loc).group(1));records=list(csv.reader(content.splitlines()))
        assert 1<=number<=len(records),(p,loc)
        result='CSV record exists; exact contract content checked by family, not all prose semantics'
    source_checks.append(dict(record_id=q['requirement_id'],actual_source=p,source_location=loc,result=result,method='Exhaustive locator check; family source checks and stated review limits'))

# Current provenance evidence is its own audit record. The remaining historical
# comparison issue is not an organizer selection question after user confirmation.
id='REG-ISS-010'
for r in rows:
    if r['record_id']==id:r['title']='S01 historical content comparison evidence'
add(newrow(id,'Registry Issue',main(id)['title'],'Open','Docs/architecture/registry/audit-ARCH-REG-002/request.txt',ref='Section 1; user confirms current official PDF',kind='evidence'),
    'Current source identification is resolved by the user instruction; historical content equivalence remains unverified.')
add(newrow(id,'Registry Issue',main(id)['title'],'Open',PDF,ref='Direct byte SHA-256 '+CURRENT,kind='evidence'), 'Record the exact current PDF member as direct provenance evidence.')

# Add the missing later-model/tooling evidence for the two broad Registry findings.
for id,p,ref in [('REG-ISS-007','Docs/architecture/audit-2026-11-09/structurizr-gap-report.md','SG-04, SG-05, SG-13'),
                 ('REG-ISS-008','Docs/architecture/audit-2026-11-09/structurizr-gap-report.md','SG-01, SG-14')]:
    rec=main(id);add(newrow(id,rec['record_type'],rec['title'],'Open',p,ref=ref,kind='evidence'),'Add the actual supporting gap records, not only a generic source section.')

# Declare source-to-record relationships for direct documentary support. These
# describe provenance, not implementation dependencies or expanded access grants.
for n in range(1,18):
    adr=f'ADR-{n:02d}'
    sids=set(re.findall(r'\bS\d{2}\b',sect(d3,adr.lower())))
    for m in re.finditer(r'\bS(\d{2})-S(\d{2})\b',sect(d3,adr.lower())):
        sids.update(f'S{x:02d}' for x in range(int(m[1]),int(m[2])+1))
    for sid in sorted(sids):
        if not has_edge(sid,adr,'ADR'):
            add(edge(sid,adr,'ADR',D3,adr.lower(),'ADR source explicitly attributes this source ID','supports'), 'Add the source-to-record direction of an explicit source attribution.')

for rec in list(rows):
    if rec['row_kind']=='record' and rec['record_type']=='Decision Statement' and rec['status']=='Accepted':
        add(edge('S19',rec['record_id'],'Decision Statement','Docs/architecture/audit-2026-11-09/request.txt','',
                 'Section 1; explicit five-boundary confirmation','supports'),
            'Add the explicit approval source for this Accepted statement. This is approval provenance, not a product implementation dependency.')

# Keep inverse classifications consistent with the reviewed forward association.
for r in rows:
    if r['row_kind']=='relationship' and r['record_type']=='AT' and r['relationship_type']=='referenced_by':
        forward=next((x for x in rows if x['row_kind']=='relationship' and x['record_id']==r['target_id'] and x['target_id']==r['record_id'] and x['target_type']=='AT'),None)
        if forward and r['relationship_status']!=forward['relationship_status']:
            old=r['relationship_status'];r['relationship_status']=forward['relationship_status']
            correction('Inverse classification',r['record_id'],r['target_id']+' / '+old,r['target_id']+' / '+r['relationship_status'],
                       'An inverse cannot claim stronger evidence than its reviewed forward association.',forward['source_file']+'#'+forward['source_anchor'])

# Save the corrected matrix with the existing schema and stable record IDs.
dump_csv(REG/'traceability-matrix.csv',rows,fields)

# Keep all original source extract blocks unchanged. Correct only index text.
issue_text=original(regpath('open-issues-registry.md'))
old010=sect(issue_text,'reg-iss-010')
new010='''<a id="reg-iss-010"></a>

## REG-ISS-010: S01 historical content comparison evidence

Status: **Open**. Evidence state: **Evidence Pending**.

Required work: Engineering Evidence Required.

Resolved subpart: The user confirms the current official S01 PDF in ARCH-REG-002 section 1. The file exists at the declared repository path. Its current SHA-256 is `CURRENT_HASH`. Source identification needs no further organizer answer.

Remaining question: The prior review recorded SHA-256 `OLD_HASH`. The historical PDF bytes have not been recovered for a content comparison. The old review result cannot establish semantic equality with the current bytes.

Effect: Keep the current source identity separate from unverified historical content agreement. A byte-hash difference does not prove changed requirements.

Existing options: Recover the historically identified PDF and compare content, or record an authorized disposition of the unrecoverable historical comparison. Neither disposition is selected here.

Decision owner: No person is documented. This is an evidence/provenance task, not a new architecture selection.

Closure criterion: Supply the historical comparison or a recorded authorized disposition. The current identity subpart is resolved. The whole record remains Open.

Source Evidence: [Source register](../001-system-blueprint.md#system-2), [prior review](../004-reconciliation-review.md), [current user instruction](audit-ARCH-REG-002/request.txt), and [audit findings](semantic-audit-report.md).

Dependencies: DL-16 is a Proposed / Inferred Relationship for provenance review. It does not create an organizer dependency.
'''.replace('CURRENT_HASH',CURRENT).replace('OLD_HASH',OLD)
issue_text=issue_text.replace(old010,new010)
correction('Issue provenance','REG-ISS-010',old010,new010,'Split the user-resolved source identity from the still-unverified historical comparison; keep the issue Open.','ARCH-REG-002 request section 1; actual byte hash')
# The source says organizer clarification is conditional, not a blanket blocker.
for id,old,new in [
 ('DL-06','Required work: Team Decision Required; Organizer / Source Clarification Required; Engineering Evidence Required.',
  'Required work: Team Decision Required; Engineering Evidence Required. Organizer / Source Clarification Required only if the documented manager-Q08 source-meaning ambiguity cannot be resolved from the supplied brief and access matrix.'),
 ('DL-07','Required work: Team Decision Required; Organizer / Source Clarification Required; Engineering Evidence Required.',
  'Required work: Team Decision Required; Engineering Evidence Required. Source clarification is conditional on choosing an hours measure whose working-hours contract is absent. A headcount design does not itself require an organizer answer.'),
 ('DL-14','Required work: Team Decision Required; Organizer / Source Clarification Required; Engineering Evidence Required.',
  'Required work: Team Decision Required; Engineering Evidence Required. Final organizer hardware/profile confirmation is tracked in DL-16. Model, provider, gateway and internal limits remain team choices.'),
 ('REG-ISS-008','Required work: Team Decision Required; Engineering Evidence Required.',
  'Required work: Engineering Evidence Required. This is a documentation maintenance follow-up. Historical Git context does not establish an unresolved architecture selection.')]:
    body=sect(issue_text,id.lower());assert old in body
    issue_text=issue_text.replace(body,body.replace(old,new));correction('Issue route',id,old,new,'Do not turn engineering/team choices into unconditional organizer blockers.',D3+'#'+('adr-06' if id=='DL-06' else 'decision-log'))

# Correct stale dependency text from the compressed-reference parser.
for id in dlraw:
    body=sect(issue_text,id.lower());old=next((s for s in body.splitlines() if s.startswith('Dependencies: ')),None)
    if not old:continue
    actual_deps=sorted({r['target_id'] for r in rows if r['record_id']==id and r['row_kind']=='relationship' and r['target_type'] in ['ADR','AT']})
    new='Dependencies: '+', '.join(actual_deps)+'.'
    if old!=new:
        issue_text=issue_text.replace(body,body.replace(old,new));correction('Dependency index',id,old,new,'Match the corrected graph. Proposed additional gates remain proposed in the CSV/ledger.',D3+'#decision-log; related ADR/AT section')
put(regpath('open-issues-registry.md'),issue_text)

inv=original(regpath('source-inventory.md'))
inv=inv.replace('Recorded PDF hash differs from the actual local file; see REG-ISS-010. No requirement change is established.',
                f'Current official source confirmed by the user in ARCH-REG-002; SHA-256 `{CURRENT}`. Prior recorded SHA-256 `{OLD}` is historical. Historical content comparison remains REG-ISS-010; no requirement change is established.')
inv=inv.replace('Source-version/content-equivalence evidence for the mismatched S01 PDF hash: REG-ISS-010.',
                'Historical PDF content-comparison evidence: REG-ISS-010. Current S01 identification is resolved by user confirmation.')
put(regpath('source-inventory.md'),inv)
correction('Source inventory','S01','Hash mismatch without current authority disposition',CURRENT+' current; '+OLD+' historical','User establishes the current source identity; historical comparison stays pending.','ARCH-REG-002 request section 1')

# Freeze the old task's scripts. They are retained as historical evidence, but a
# later accidental run must not replace this audited Registry with old mappings.
for name in ['build_registry.py','validate_registry.py']:
    s=original(regpath(name));needle='from pathlib import Path\n'
    guard=('from pathlib import Path\n'
           'if (Path(__file__).resolve().parent / "semantic-audit-report.md").exists():\n'
           '    raise SystemExit("ARCH-REG-001 historical script: use audit-ARCH-REG-002/validate_semantic_audit.py for current validation. Do not regenerate the audited Registry.")\n')
    assert needle in s;put(regpath(name),s.replace(needle,guard,1))
    correction('Historical script guard',name,'Unrestricted ARCH-REG-001 regeneration/check',guard,'Prevent an old generator/checker from silently undoing corrections or overwriting historical results.',regpath(name)+'; ARCH-REG-002 scope')

counts=dict(rows=len(rows),kinds=dict(Counter(r['row_kind'] for r in rows)),records=dict(Counter(r['record_type'] for r in rows if r['row_kind']=='record')))
summary=json.loads(original(regpath('extraction-summary.json')))
summary.update(task='ARCH-REG-002',requirements=334,accepted_boundary_records=5,indexed_source_matrix_ids=339,
               matrix_rows=len(rows),team_required=24,organizer_source_required=8,conditional_organizer_source_required=2,
               engineering_evidence_required=29)
put(regpath('extraction-summary.json'),json.dumps(summary,indent=2))
correction('Counts','Registry summary',json.dumps(before_counts),json.dumps(counts),'Separate 334 Requirement records from five Accepted Decision Boundary records; add missing endpoint/evidence/edge rows.','Actual parsed CSV')
put(regpath('validation-report.md'),original(regpath('validation-report.md'))+'\n\n## ARCH-REG-002 superseding audit note\n\nThe results above describe the ARCH-REG-001 extraction snapshot. They do not establish semantic correctness. Read [semantic-audit-report.md](semantic-audit-report.md) for current counts, S01 identity, corrected mappings and remaining review limits. The current S01 identity is confirmed; historical content comparison remains Open. The old validation-results.json and baseline-comparison.csv are retained unchanged as historical evidence.\n')
readme=original(regpath('README.md'))
readme=readme.replace('Task: `ARCH-REG-001`.','Tasks: `ARCH-REG-001` extraction; `ARCH-REG-002` semantic audit.')
readme=readme.replace('Existing requirement','Existing requirement')
readme=readme.replace('All original sources are read-only for this task. All 141 initial untracked files must remain unchanged. Only new files in this folder are permitted.',
 'For ARCH-REG-002, only the S01 provenance metadata in 001 and 004 can change outside this folder. All other original source bytes remain unchanged. Before bytes, exact corrections and after hashes are retained in audit-ARCH-REG-002/.')
readme+='''\n\n## Current semantic audit

Read [semantic-audit-report.md](semantic-audit-report.md). The audit keeps this schema and all original record IDs. Five `DEC-*` records now use `Decision Boundary`, with Accepted status. They are not Requirement records. The original audit index has 339 IDs: 334 Requirements and five Accepted boundaries.

All relationship endpoints now have main records. Ten existing DSL elements and seven existing acceptance supplements were missing from the main-record index. Adding their index records creates no architecture component or acceptance requirement. Imported audit mappings are Proposed Relationships unless there is direct source proof. Unsupported removed edges remain in the correction ledger and before snapshot. A source attribution is not a proof of every claim in a referenced document.

The [edge review](audit-ARCH-REG-002/relationship-review.csv) separates Explicit Source Relationship, Proposed / Inferred Relationship, and unsupported edges. The [correction ledger](audit-ARCH-REG-002/corrections.csv) retains before/after values. The [source checks](audit-ARCH-REG-002/source-locator-checks.csv) resolve current paths and source locations. Review scope and limits are stated in the semantic report; automated checks do not constitute exhaustive semantic approval.

Organizer routes are unconditional only for eight issues. Two further routes are conditional. Model/provider/internal-limit choices stay with the team. REG-ISS-010 now needs engineering evidence for historical content comparison; user confirmation resolves current S01 identification. All 29 issues remain Open, all 30 ATs remain Planned / Not Executed, and all 20 risks retain Not Assessed severity.

The ARCH-REG-001 build/check scripts are frozen as historical tools. Use [validate_semantic_audit.py](audit-ARCH-REG-002/validate_semantic_audit.py) for current read-only checks. No old generator should replace this reviewed extraction.
'''
put(regpath('README.md'),readme)
correction('Registry documentation','README and prior validation report','ARCH-REG-001 limits and counts only','Current semantic audit note, precise route/count meanings and historical script/output limits','Make current results distinct from the retained extraction evidence.','ARCH-REG-002 actual checks')

# Create a per-edge semantic review ledger. This does not claim that an automated
# record match proves meaning. High-volume mappings are explicitly inference-based.
review=[]
for i,r in enumerate(rows,2):
    if r['row_kind']!='relationship':continue
    is_high=r['record_type'] in ['ADR','DL','Registry Issue','Risk','AT','Decision Statement','Decision Boundary','Source']
    category='Explicit Source Relationship' if r['relationship_status']=='Documented' else 'Proposed / Inferred Relationship'
    method='Targeted source-topic review for every high-impact record; per-edge rule/provenance check' if is_high else 'Exhaustive imported-row/locator check; family semantic review; individual source meaning not exhaustively approved'
    reason=('An exact source attribution, named gate, container/supplement membership or typed inverse supports this link.' if category.startswith('Explicit') else
            'The topic is relevant or was imported by the earlier audit, but the exact assignment is not approved or not explicit. Keep for review; do not treat co-occurrence as proof.')
    if r['record_type']=='Risk':reason='The named test addresses part of the stated control; no risk reduction is proved. All risk links remain Proposed for team review.'
    review.append(dict(matrix_row=i,record_id=r['record_id'],record_type=r['record_type'],target_id=r['target_id'],target_type=r['target_type'],
                       relationship_type=r['relationship_type'],classification=category,method=method,reason=reason,
                       source_file=r['source_file'],source_anchor=r['source_anchor'],source_ref=r['source_ref']))
for r in unsupported:
    review.append(dict(matrix_row='',record_id=r['record_id'],record_type=r['record_type'],target_id=r['target_id'],target_type=r['target_type'],relationship_type=r['relationship_type'],
                       classification='Unsupported Relationship',method='Direct requirement-title versus ADR-scope review',reason=wrong[(r['record_id'],r['target_id'])],source_file=r['source_file'],source_anchor=r['source_anchor'],source_ref=r['source_ref']))
dump_csv(AUD/'relationship-review.csv',review)
dump_csv(AUD/'source-locator-checks.csv',source_checks)
dump_csv(AUD/'corrections.csv',corrections)
(AUD/'audit-counts.json').write_text(json.dumps(dict(before=before_counts,after=counts,unsupported_removed=len(unsupported),
    review_categories=dict(Counter(x['classification'] for x in review)),corrections=len(corrections)),indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(before=before_counts,after=counts,corrections=len(corrections),unsupported_removed=len(unsupported)),indent=2))
