"""Build the material findings report and pre-edit document-unit ledger."""
from audit_support import ROOT, OUT, read
import csv
import hashlib
import html
import json
import re
import zipfile
from collections import Counter

findings=json.loads((OUT/'findings.json').read_text(encoding='utf-8'))
material=[r for r in findings if r['status']!='Verified; retained']
assert [r['id'] for r in findings]==[f'AUD-{i:03d}' for i in range(1,60)]
with (OUT/'findings.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(findings[0]));writer.writeheader();writer.writerows(findings)

contexts={
 '001':{
 1:'S16 Q01/Q03/Q16; S17 existing target; S19 accepted boundaries. Physical/framework details remain Proposed.',
 2:'Actual source inventory; S01/S18 brief; S02-S07 contracts. Audit observations are not approval.',
 3:'Brief requirements and README; granular children in the current RTM.',
 4:'Brief pp.3,9,13; S17 component allocation/F01-F08. Internal schemas and mechanisms are Proposed.',
 5:'README cutoff/input timing; S17 NightlyData/NightlyBrief/PartialPublication.',
 6:'All55 dictionary records; five reference views; calendar and targets; source KPI contract.',
 7:'All8 escalation rules; all 12 workflow stages; canonical workflow KPI SQL; brief pp.5-8.',
 8:'Brief pp.9-10,13,16; S17 F01/F02/F03; proposed evidence grouping and model limits.',
 9:'Brief pp.5,10-12,15; both output schemas; README mandatory outputs; S16 Q06/Q14/Q16.',
 10:'Brief pp.5,10,12-13; access matrix; S17 identity/query/evidence boundaries. Physical control design Proposed.',
 11:'Brief pp.13,18; S16 one-Agent decision; infrastructure choices otherwise Proposed.'},
 '002':{
 1:'S17 protected RAW/PostgreSQL boundary and canonical calculation requirements. Logical layers Proposed.',
 2:'Observed headers and source identities; S17 target responsibilities. Physical keys/FKs and new internal records Proposed.',
 3:'README cutoff; calendar fields; reference lead/revenue views; source L02045 fixture; RCA CRM-02/03.',
 4:'README source families; all 91 manifests/headers; RAW repeat fixture; schema aliases. Acceptance policy remains Open.',
 5:'README unavailable values; DQ report sections3/6/8/9. Internal states and release policies Proposed/Open.',
 6:'All55 exact SQL/metadata; five view semantics; types from historical audit not official Data Dictionary.',
 7:'Canonical clocks/windows/MIN/MAX/join semantics; DQ contributor evidence. Selective algorithm Proposed.',
 8:'Brief p.9 every-number traceability; S17 query/evidence/report responsibilities. Physical storage/reissue policy Proposed.',
 9:'Org/access source records, README next-morning rule, S07 IN05/IN06, brief privacy/configuration.',
 10:'Accepted PostgreSQL-only boundary; S16 Q03/S17; translation/security proof absent.',
 11:'Brief time/cost/delivery; independent-publication decision. Indexes/jobs/retention/restore details Proposed.'},
 '003':{
 1:'S16 recorded decisions, S17 target, current user accepted-boundary confirmation.',
 2:'README, reference SQL, known aliases, mandatory output and human-decision rules.',
 3:'ADR-specific Requirement/Accepted/Proposed/Open separation; S01-S19 and current Decision Log.',
 4:'Source-backed unresolved options. Priority/owner roles are recommendations, not team assignments.',
 5:'Source/evidence risks and Proposed mitigations. No run or pass is inferred.',
 6:'Brief p.18 milestone/delivery scope; proposed roadmap and slice, not fixed capacity or completed work.',
 7:'Source requirements and planned product gates; schemas/rules/workflows. No AT executed.',
 8:'Brief pp.14,16,19 and Proposed measurement receipts; no benchmark/cost result.',
 9:'Audit scope/method evidence, not software acceptance.',
 10:'Open policy/source gaps; authority, options, consequences and required closure evidence.'}}

def evidence_for(doc,section,text):
    number=doc.split('/')[-1][:3]
    if number=='004':
        return 'S16 Q01-Q17 plus brief/dataset/S17; mapping is a review result, not acceptance proof.'
    keys=re.findall(r'`(K_[A-Z0-9_]+)`',text)
    if keys:
        return 'kpi_dictionary.csv exact records/SQL for '+','.join(dict.fromkeys(keys))+'; semantic contracts and source scopes.'
    if re.match(r'^\| R[1-8] \|',text):
        key=re.search(r'R[1-8]',text)[0]
        return 'escalation_rules.csv '+key+'; brief pp.7-8; fixed meaning versus Open edge behavior.'
    m=re.match(r'^## (\d+)',section)
    sec=int(m[1]) if m else 0
    return contexts.get(number,{}).get(sec,'Document metadata/status/source context; no independent runtime or approval claim.')

def units(lines):
    i=0
    while i<len(lines):
        if not lines[i].strip():i+=1;continue
        start=i
        s=lines[i]
        if s.startswith('```'):
            i+=1
            while i<len(lines) and not lines[i].startswith('```'):i+=1
            if i<len(lines):i+=1
            yield start+1,i,'code/diagram block','\n'.join(lines[start:i]);continue
        if s.startswith('#'):kind='heading'
        elif s.startswith('|'):kind='table row'
        elif s.startswith('<a '):kind='anchor'
        elif s.startswith('<!--'):kind='metadata marker'
        elif re.match(r'^[-*] |^\d+[.،] ',s):kind='list/numbered paragraph'
        else:kind='paragraph'
        i+=1
        if kind=='paragraph':
            while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||```|<a |<!--|[-*] |\d+\. )',lines[i]):i+=1
        yield start+1,i,kind,'\n'.join(lines[start:i])

ledger=[]
with zipfile.ZipFile(OUT/'pre-edit.zip') as archive:
    for doc in ['docs/architecture/001-system-blueprint.md','docs/architecture/002-data-architecture.md',
                'docs/architecture/003-decisions-and-roadmap.md','docs/architecture/004-reconciliation-review.md']:
        text=archive.read(doc).decode('utf-8-sig');lines=text.splitlines();section='Document front matter';covered=set()
        doc_findings=[r for r in findings if r['document']==doc]
        headings=[(i+1,s) for i,s in enumerate(lines) if s.startswith('## ')]
        for first,last,kind,body in units(lines):
            covered.update(range(first,last+1))
            if body.startswith('## '):section=body
            end=next((n-1 for n,_ in headings if n>first),len(lines))
            section_start=max([n for n,_ in headings if n<=first] or [1])
            direct=[r['id'] for r in doc_findings if first<=r['original_line']<=last]
            related=[r['id'] for r in doc_findings if section_start<=r['original_line']<=end]
            if kind in {'heading','anchor','metadata marker'} or re.fullmatch(r'[|:\-\s]+',body):
                classification='Structural';evidence='Document navigation/format; verify separately from source meaning.'
            else:
                labels=[]
                for label,pattern in [('Requirement','Requirement|الزام'),('Accepted','Accepted'),('Proposed','Proposed|پیشنهاد'),('Open','Open|باز|unknown')]:
                    if re.search(pattern,body,re.I):labels.append(label)
                classification=';'.join(labels) if labels else 'Source/design context; see evidence and section disposition'
                evidence=evidence_for(doc,section,body)
            ledger.append(dict(unit_id=f"{doc.split('/')[-1][:3]}-U{sum(r['document']==doc for r in ledger)+1:03d}",
                document=doc,pre_edit_first_line=first,pre_edit_last_line=last,unit_kind=kind,section=section,
                original_sha256=hashlib.sha256(body.encode()).hexdigest(),original_excerpt=body[:240],
                classification_context=classification,source_or_design_context=evidence,
                direct_findings=';'.join(direct),section_findings=';'.join(related),
                disposition=('Verified source observation retained' if direct and all(
                    r['status']=='Verified; retained' for r in doc_findings if r['id'] in direct)
                    else 'Material correction recorded' if direct else
                    'Reviewed in source/design context; retained or clarified at section level'),
                verification_limit='Context identifies supporting sources; it is not automatic sentence-level proof or product acceptance.'))
        assert all(i+1 in covered for i,line in enumerate(lines) if line.strip()),doc
with (OUT/'document-review-ledger.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(ledger[0]));w.writeheader();w.writerows(ledger)

counts=Counter(r['severity'] for r in material);states=Counter(r['status'] for r in findings)
report=f'''# Detailed architecture audit report

Review date: 2026-11-09, Asia/Tehran. This is a source-driven documentation audit. It preserves the existing target architecture. It does not certify product correctness or authorize implementation.

## Scope and method

The four numbered documents were reviewed sequentially against the Markdown brief, important/ambiguous PDF passages, README, all five config files, all organization/access files, both output schemas and example, all 23 manager inputs, all 91 manifests and delivered header/count evidence, relevant source fixtures, investigation reports, the recorded 17-question discussion, and the existing Structurizr model. The source records and model remain unchanged.

The PDF has 26 annotations. Current checked pages 8,10,15 agree with the Markdown requirements; the same current PDF was checked on pages 13,16 in the previous review. Highlighting/resaving and byte-hash differences do not establish requirement changes. See [brief evidence](brief-content-check.json).

Requirements come from official sources. Accepted choices come from recorded team/user decisions. Physical mechanisms, algorithms and exact limits remain Proposed or Open unless evidence approves them. Observation is an evidence category. The current user confirms all five accepted boundaries; none was reopened.

## Results and limits

There are {len(findings)} audit records: {len(material)} material findings and one verified, retained source observation (AUD-028). Material severity: {dict(counts)}. Record states: {dict(states)}. The two deferred findings concern DSL source/count comments. Model work is reserved for the subsequent visualization phase. Open business/source policies remain in the [Decision Log](../003-decisions-and-roadmap.md#decision-log); a corrected document does not close them.

The [unit ledger](document-review-ledger.csv) inventories {len(ledger)} pre-edit headings, paragraphs/list items, table rows, blocks and anchors. Every nonblank line in the four pre-edit documents belongs to a review unit. Each unit has a hash, exact line span, context and relevant findings. Inherited section evidence is review context, not an independent proof of every sentence. Semantic results rest on the detailed issue analysis and [granular traceability](requirements-traceability.md), not link counts.

The [findings CSV](findings.csv) and [JSON](findings.json) preserve every full original claim. Locations below refer to immutable pre-edit bytes in [pre-edit.zip](pre-edit.zip), not shifted current line numbers. The [baseline manifest](pre-edit-manifest.json) identifies the files. Corrected means the documentation issue was addressed; it does not mean an implementation passed a test.

## Findings and the retained source observation

'''
for r in findings:
    claim=(html.escape(r['original_claim']).replace('`','&#96;').replace('|','&#124;')
           .replace('[','&#91;').replace(']','&#93;'))
    report+=f"""### {r['id']}: {r['category']}

- Location: `{r['document']}`, pre-edit line {r['original_line']}.
- Severity: **{r['severity']}**. Correction status: **{r['status']}**.
- Original claim or affected location: {claim}
- Source evidence: {r['evidence']}
- Correction: {r['correction']}
- Remaining uncertainty: {r['uncertainty']}

"""
report+='''## Unresolved matters and implementation limits

The central log retains numerical equivalence/input types and input mode, source closure/release, correction ties, shared-resource/privacy/capacity policy, stage owners, genuinely unspecified rule boundaries, M11/attachment timing, output status/number/dimension mapping, human execution confirmation, model limits, approval roles, retention and official evaluation profile. Full source coverage cannot invent these answers.

The five accepted architecture boundaries remain intact. All55 canonical definitions, all 8 rules, all 12 stages, all 11 access scopes and all 23 supplied inputs have semantic trace records. Exact schema constraints are recorded separately from required report content. All AT gates remain planned. No KPI SQL, PostgreSQL parity, model call, product security, runtime, restore or official acceptance test was executed.

No Structurizr element, relationship, view, style or layout was changed. The [gap report](structurizr-gap-report.md) distinguishes existing coverage from future visualization work. Active legacy rendered previews are retired; original raw files and generators remain historical and must not replace the baseline.
'''
(OUT/'audit-report.md').write_text(report,encoding='utf-8',newline='\n')
(OUT/'audit-summary.json').write_text(json.dumps(dict(audit_records=len(findings),material_findings=len(material),severity=dict(counts),correction_states=dict(states),review_units=len(ledger),
    units_by_document=dict(Counter(r['document'] for r in ledger))),indent=2),encoding='utf-8')
print(json.dumps(dict(audit_records=len(findings),material_findings=len(material),review_units=len(ledger),states=dict(states))))
