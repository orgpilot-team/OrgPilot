"""Validate local Registry documentation. Never execute product acceptance tests."""
from pathlib import Path
if (Path(__file__).resolve().parent / "semantic-audit-report.md").exists():
    raise SystemExit("ARCH-REG-001 historical script: use audit-ARCH-REG-002/validate_semantic_audit.py for current validation. Do not regenerate the audited Registry.")
import csv, hashlib, json, re, subprocess
from collections import Counter
from urllib.parse import unquote

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
BASE='0a42950d1ce9734433d961540af9ab4be21573b2'
PREFIX='Docs/architecture/registry/'
pre=json.loads((OUT/'preflight.json').read_text(encoding='utf-8'))
summary=json.loads((OUT/'extraction-summary.json').read_text(encoding='utf-8'))
rows=list(csv.DictReader((OUT/'traceability-matrix.csv').open(encoding='utf-8',newline='')))
errors=[];checks={};warnings=[]

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def git(*args):
    p=subprocess.run(['git','-c','core.quotepath=false',*args],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
    return dict(returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
def check(name,condition,detail=''):
    checks[name]=dict(ok=bool(condition),detail=detail)
    if not condition: errors.append(name+': '+str(detail))
def read(path): return path.read_text(encoding='utf-8-sig')
def without_quotes(text): return re.sub(r'^```[^\n]*\n.*?^```\s*$', '',text,flags=re.M|re.S)
def anchors(path):
    if path.suffix.lower()!='.md': return set()
    return set(re.findall(r'<a\s+id="([^"]+)"',without_quotes(read(path))))
def section(text,id):
    start=text.index(f'<a id="{id}"></a>')
    m=re.search(r'\n<a id="[^"]+"></a>',text[start+1:])
    return text[start:start+1+m.start()] if m else text[start:]

# Reserve names for this run's reports before checking local links. They are new
# files in the allowed task folder, never protected source files.
for name in ['validation-report.md','validation-results.json','baseline-comparison.csv','untracked-source-dependencies.csv']:
    if not (OUT/name).exists(): (OUT/name).write_text('Pending validation.\n',encoding='utf-8')

main=[r for r in rows if r['row_kind']=='record']
ids=[(r['record_type'],r['record_id']) for r in main]
check('Unique main record identities',len(ids)==len(set(ids)),[x for x,c in Counter(ids).items() if c>1])
check('17 ADRs',{r['record_id'] for r in main if r['record_type']=='ADR'}=={f'ADR-{x:02d}' for x in range(1,18)})
check('19 DLs',{r['record_id'] for r in main if r['record_type']=='DL'}=={f'DL-{x:02d}' for x in range(1,20)})
check('30 ATs',{r['record_id'] for r in main if r['record_type']=='AT'}=={f'AT-{x:02d}' for x in range(1,31)})
check('19 source identities',{r['record_id'] for r in main if r['record_type']=='Source'}=={f'S{x:02d}' for x in range(1,20)})
check('All ATs planned',all(r['status']=='Planned / Not Executed' for r in main if r['record_type']=='AT'))
check('All issues Open',all(r['status']=='Open' for r in main if r['record_type'] in ['DL','Registry Issue']))
statements=[r for r in main if r['record_type']=='Decision Statement']
check('Statement status count',dict(Counter(r['status'] for r in statements))==summary['decision_status_statements'])
check('Five Accepted boundaries',len([r for r in statements if r['status']=='Accepted'])==5)
check('No exact duplicate CSV rows',len(rows)==len({tuple(r.items()) for r in rows}))
check('One target per relationship',all(bool(r['target_id']) and bool(r['target_type']) and r['relationship_status'] in ['Documented','Proposed Relationship'] for r in rows if r['row_kind']=='relationship'))
check('No multi-ID relation cells',all(not re.search(r'[,;]',r[f]) for r in rows for f in ['related_adr','related_dl','related_at','related_risk','roadmap_phase']))

# Source anchors in CSV must be explicit existing source anchors. Legacy source
# paths inside source_ref remain quoted provenance, not falsely resolved links.
loc_errors=[]
for r in rows:
    if r['source_file']:
        p=ROOT/r['source_file']
        if not p.exists(): loc_errors.append(r['record_id']+': missing '+r['source_file'])
        elif r['source_anchor'] and r['source_anchor'] not in anchors(p):
            loc_errors.append(r['record_id']+': bad source anchor '+r['source_anchor'])
    if r['registry_file']:
        p=OUT/r['registry_file']
        if not p.exists() or r['registry_anchor'] not in anchors(p):
            loc_errors.append(r['record_id']+': invalid Registry location')
check('All CSV source and Registry locations resolve',not loc_errors,loc_errors[:20])

link_count=0;link_errors=[]
for p in OUT.glob('*.md'):
    txt=without_quotes(read(p))
    local_anchors=re.findall(r'<a\s+id="([^"]+)"',txt)
    if len(local_anchors)!=len(set(local_anchors)): link_errors.append(p.name+': duplicate explicit anchors')
    for url in re.findall(r'\[[^\]\n]*\]\(([^\s)]+(?:\)[^\s)]*)?)\)',txt):
        if re.match(r'\w+://',url): continue
        target,sep,a=url.partition('#');dest=(p.parent/unquote(target)).resolve() if target else p
        link_count+=1
        if not dest.exists(): link_errors.append(p.name+': '+url)
        elif a and unquote(a) not in anchors(dest): link_errors.append(p.name+': '+url)
check('All active Markdown links resolve',not link_errors,dict(links=link_count,errors=link_errors[:20]))

# Loss checks compare full source extracts, not only IDs or word counts.
d3=read(ROOT/'Docs/architecture/003-decisions-and-roadmap.md')
decisions=read(OUT/'decisions-registry.md');accept=read(OUT/'acceptance-register.md');issues=read(OUT/'open-issues-registry.md')
missing=[]
for n in range(1,18):
    if section(d3,f'adr-{n:02d}').strip() not in decisions: missing.append(f'ADR-{n:02d}')
for line in d3.splitlines():
    if re.match(r'\| <a id="at-\d{2}"></a>AT-\d{2} \|',line) and line not in accept: missing.append(line[:45])
    if re.match(r'\| DL-\d{2}',line) and line not in issues: missing.append(line[:20])
check('Complete ADR, DL and AT source extracts',not missing,missing)
supplements=[('#### تکمیل معیارهای آزمون موجود','#### ماتریس محتوای اختصاصی'),
             ('#### ماتریس محتوای اختصاصی','#### موارد اختصاصی قواعد'),
             ('#### موارد اختصاصی قواعد','### ۷.۱.')]
check('Complete supplementary AT and role/rule matrices',all(d3[d3.index(a):d3.index(b)].strip() in accept for a,b in supplements))
check('P5 delivery supplement retained',d3[d3.index('تکمیل شرط تحویل P5'):d3.index('در هر مرحله، CSVهای audit')].strip() in accept)
risk=read(OUT/'risk-register.md')
risk_lines=[x for x in section(d3,'decisions-5').splitlines() if x.startswith('| ') and not x.startswith('| ریسک')]
check('All 13 original risk rows retained',len(risk_lines)==13 and all(x in risk for x in risk_lines))
check('Every risk has unassessed severity',risk.count('Severity: **Not Assessed**.')==summary['risks'])

# Existing audit component IDs must name actual DSL declarations. Keep invalid
# source references visible as warnings; never create fictitious declarations.
dsl=read(ROOT/'architecture/structurizr/workspace.dsl')
components={r['target_id'] for r in rows if r['target_type']=='Architecture Component'}
component_gaps=sorted(x for x in components if not re.search(r'\b'+re.escape(x)+r'\s*=\s*(component|container|softwareSystem)\b',dsl))
check('All component targets exist in DSL',not component_gaps,component_gaps)
known={r['record_id'] for r in main}
supp={'supplement-tests','role-matrix','rule-matrix','oracle-boundaries','input-and-negative-cases','measurement','delivery-checklist'}
unknown=sorted({r['target_id'] for r in rows if r['row_kind']=='relationship' and r['target_id'] not in known|supp|components})
check('All relationship targets resolve',not unknown,unknown)

prior_changed=[]
for name,expected in pre['sha256'].items():
    p=ROOT/name
    if not p.is_file() or sha(p)!=expected: prior_changed.append(name)
check('All 1344 initial files unchanged',not prior_changed,dict(initial_count=len(pre['sha256']),changed=prior_changed))
check('All 141 prior untracked files unchanged',len(pre['existing_untracked_files'])==141 and not any(p in prior_changed for p in pre['existing_untracked_files']))
diff=git('diff','--name-status',BASE)
check('No tracked diff against baseline',diff['returncode']==0 and not diff['stdout'].strip(),diff)
check('HEAD remains baseline',git('rev-parse','HEAD')['stdout'].strip()==BASE)
now_untracked=git('ls-files','--others','--exclude-standard','-z')['stdout'].strip('\0').split('\0')
new=sorted(set(now_untracked)-set(pre['existing_untracked_files']))
check('Every new file is inside Registry',all(x.startswith(PREFIX) for x in new),new)
check('No prior untracked file removed',set(pre['existing_untracked_files'])<=set(now_untracked))
source_hash=sha(ROOT/'Docs/architecture/sources/Adr.md')
check('S16 copy matches recorded hash',source_hash=='0c7cea554016930366100cb1138ada6ace7f05e918e274ee24f0a89e465639df')
pdf_hash=sha(ROOT/'Docs/بریف پروژه بوتکمپ _ دستیار ایجنتیک مدیران سازمانی _ دیدراه.pdf')
recorded_pdf_hash='6d68d3fcc285f6908af0d97c0429dfefb489f00b7f6538ed03573552ed6955f8'
pdf_hash_matches=pdf_hash==recorded_pdf_hash
check('S01 provenance discrepancy recorded',pdf_hash_matches or ('REG-ISS-010' in known and pdf_hash in issues and recorded_pdf_hash in issues),
      dict(actual_sha256=pdf_hash,recorded_sha256=recorded_pdf_hash,matches=pdf_hash_matches,issue='REG-ISS-010'))

# List every original untracked file. Identify direct and directory-scoped uses.
referenced={r['source_file'] for r in rows if r['source_file']}
dep_rows=[]
for name in pre['existing_untracked_files']:
    direct=name in referenced
    scoped=any((ROOT/p).is_dir() and name.startswith(p.rstrip('/')+'/') for p in referenced)
    dep_rows.append(dict(source_file=name,dependency='Direct Registry source' if direct else 'Directory source member' if scoped else 'Preserved prior untracked file',
                         tracking_state='Untracked at preflight',sha256=pre['sha256'].get(name,''),
                         commit_follow_up='Review source inclusion in a future separately authorized commit. No staging in this task.'))
with (OUT/'untracked-source-dependencies.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(dep_rows[0]));w.writeheader();w.writerows(dep_rows)
direct_count=sum(r['dependency']=='Direct Registry source' for r in dep_rows)
scoped_count=sum(r['dependency']=='Directory source member' for r in dep_rows)

status=git('status','--porcelain=v1','-uall')
warnings.append('Git reports that the global ignore file is not readable. Local status and tracked diff commands return success. The known 141 prior untracked files remain in the explicit inventory.')
warnings.append('No fresh PDF visual audit or product test was run. Existing audit source references remain historical evidence.')
if not pdf_hash_matches:
    warnings.append('S01 PDF differs from the recorded 001/004 hash. REG-ISS-010 remains Open / Evidence Pending. The PDF is unchanged during this task; no requirement change is inferred.')
report=f'''# Extraction and validation report

State: **Draft / Pending Review**. Task: `ARCH-REG-001`. Date: 2026-11-09. Time zone: `Asia/Tehran`.

## Result

- ADR coverage: {summary['adrs']}/17. Numbered statements: {summary['decision_status_statements']['Accepted']} Accepted, {summary['decision_status_statements']['Proposed']} Proposed, {summary['decision_status_statements']['Open']} Open and {summary['decision_status_statements']['Requirement']} Requirement.
- Open issue records: {summary['open_issues']}; 19 original DLs and ten temporary Registry IDs.
- Required work: {summary['team_required']} team decisions, {summary['organizer_source_required']} organizer/source clarifications and {summary['engineering_evidence_required']} engineering evidence items. These sets overlap.
- Risks: {summary['risks']}. All severities are Not Assessed. Controls have Evidence Pending.
- AT coverage: {summary['ats']}/30. All Planned / Not Executed. Full supplements, three-level matrix, rule matrix and delivery criteria are retained.
- Duplicate placements attached to main records: {summary['deduplicated_placements']}. The [ledger](deduplication-ledger.md) defines this count and preserves bundled differences.
- Existing requirement IDs indexed: {summary['requirements']}. The [CSV](traceability-matrix.csv) has {summary['matrix_rows']} record/evidence/relationship rows with one target per relationship.

## Missing evidence and remaining conflicts

No main ADR, issue, risk or AT lacks a source location. Product evidence remains pending. Missing contracts include the full raw dictionary and input types, source closure, hidden labels, final organizer profile/hardware, and original decision approver names/dates. The claim of about 70 KPI outputs has no inspectable result. See [source inventory](source-inventory.md).

**S01 provenance discrepancy:** actual PDF SHA-256 is `{pdf_hash}`; 001/004 record `{recorded_pdf_hash}`. The PDF is unchanged from this task's initial inventory. REG-ISS-010 is Open / Evidence Pending. This byte difference does not establish a requirement change. A source-version/content comparison is still required before applying the old visual-review claim to this exact file.

Conflicts remain Open: RAW/DEDUP; closure/release and dated prior values; equal-rank correction precedence; shared-source row/column/purpose grants; capacity/privacy; stage ownership and stage calculation records; Signal equality/baseline/reset; M11 mornings 75/76 and same-day attachment timing; suppressed/ongoing; NULL/no-dimension and extra-number wire mapping; complete Insight/content/history contracts; existing-KPI editing versus fixed reference definitions; P2/P3 scope; failure/retry/fallback/status export; bounded model execution; retention/restore. Registry issues also retain the QA context record, DQ eligibility record, delivery evidence, model detail and stale workspace/tooling context.

No Accepted boundary is reopened. No Proposed mechanism is promoted. Risk-to-record links and extra test links without explicit source IDs are marked Proposed Relationship. Blank phase cells do not imply a phase assignment.

## Documentation checks

Result: **{'PASS' if not errors else 'FAIL'}** for this documentation check run. {sum(x['ok'] for x in checks.values())}/{len(checks)} checks succeeded. These are document/source checks. They do not pass any AT.

The check compares complete ADR/DL/AT extracts and all original risk rows. It checks active links and source anchors, ID coverage, duplicate identities, one-target relationship rows, actual DSL component IDs, source hashes and Git scope. Exact source text retains the original numbers and exceptions. English index statements and route classes remain draft extraction work that needs team review.

## Git and preservation

HEAD: `{git('rev-parse','HEAD')['stdout'].strip()}`. Baseline: `{BASE}`.

Initial state: no tracked changes and 141 untracked files. All {len(pre['sha256'])} initial file hashes remain unchanged. All 141 prior untracked files remain unchanged and untracked. Tracked diff against baseline is empty. New untracked files are confined to `Docs/architecture/registry/`.

Untracked dependencies: {direct_count} direct source files and {scoped_count} directory-source members. The [dependency list](untracked-source-dependencies.csv) also lists every other preserved prior untracked file. A later commit must review these sources separately, including S08-S10, S15-S19, the Q review, audit tables and DSL. Nothing is staged here.

The [baseline comparison](baseline-comparison.csv) covers every initial file and every new Registry file, including untracked additions. Self-referential check output files are listed as Added without an embedded self hash; all other new file hashes are recorded. This avoids an impossible self-hash cycle. The final Git check also counts every new file as a whole-file addition against the baseline.

Git warning: the global ignore file is not readable. Local Git status/diff commands succeed. This warning did not remove or alter any source file.

## Next authorized review stage

Review the draft statuses, routes and Proposed Relationships. Then record team/source answers and product evidence. In a later separately authorized content task, decide how to transfer material from 003, update links, correct stale Git/path/DSL count notes and retire/adapt the old generator. Keep stable ADR/DL/AT IDs. Do not move or rename sources before that review. No implementation, commit or push was done.
'''
if errors: report+='\n## Failed checks\n\n'+'\n'.join('- '+e for e in errors)+'\n'
(OUT/'validation-report.md').write_text(report,encoding='utf-8')

artifact_names={'validation-results.json','validation-report.md','baseline-comparison.csv'}
comparison=[]
for name,expected in pre['sha256'].items():
    p=ROOT/name;actual=sha(p) if p.is_file() else ''
    comparison.append(dict(path=name,baseline_state='Prior untracked' if name in pre['existing_untracked_files'] else 'Tracked baseline',
                           change='Unchanged' if actual==expected else 'Changed or missing',before_sha256=expected,after_sha256=actual))
for p in sorted(OUT.iterdir()):
    if p.is_file():
        comparison.append(dict(path=p.relative_to(ROOT).as_posix(),baseline_state='Absent from baseline and initial inventory',
                               change='Added',before_sha256='',after_sha256='' if p.name in artifact_names else sha(p)))
with (OUT/'baseline-comparison.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(comparison[0]));w.writeheader();w.writerows(comparison)
result=dict(state='Draft / Pending Review',documentation_checks_only=True,checks=checks,errors=errors,warnings=warnings,
            summary=summary,active_markdown_links_checked=link_count,initial_files=len(pre['sha256']),
            initial_untracked=141,changed_initial_files=prior_changed,new_files=new,
            direct_untracked_dependencies=direct_count,directory_untracked_dependencies=scoped_count,
            git_status=status,tracked_diff=diff,
            new_file_hashes={r['path']:r['after_sha256'] for r in comparison if r['change']=='Added'},
            hash_exclusions='Self-referential validation report/results/comparison are listed as Added with no embedded self hash.')
(OUT/'validation-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(ok=not errors,checks=len(checks),errors=errors,links=link_count,new_files=len(new),direct_untracked_dependencies=direct_count),ensure_ascii=False,indent=2))
raise SystemExit(1 if errors else 0)
