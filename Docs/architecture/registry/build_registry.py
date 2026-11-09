"""Build the draft documentation index from local sources. No product code runs."""
from pathlib import Path
if (Path(__file__).resolve().parent / "semantic-audit-report.md").exists():
    raise SystemExit("ARCH-REG-001 historical script: use audit-ARCH-REG-002/validate_semantic_audit.py for current validation. Do not regenerate the audited Registry.")
import csv, hashlib, json, re
from urllib.parse import unquote, quote
from collections import Counter

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
ARCH = ROOT / 'Docs/architecture'
D1 = 'Docs/architecture/001-system-blueprint.md'
D2 = 'Docs/architecture/002-data-architecture.md'
D3 = 'Docs/architecture/003-decisions-and-roadmap.md'
D4 = 'Docs/architecture/004-reconciliation-review.md'
texts = {p: (ROOT / p).read_text(encoding='utf-8-sig') for p in [D1,D2,D3,D4]}
pre = json.loads((OUT/'preflight.json').read_text(encoding='utf-8'))
untracked = set(pre['existing_untracked_files'])
rows = []

def write(name, text):
    (OUT/name).write_text(text.rstrip()+'\n', encoding='utf-8')

def link(path, anchor='', label='Source'):
    import os
    rel = Path(os.path.relpath(ROOT/path, OUT)).as_posix()
    return f'[{label}]({quote(rel, safe="/._-()")}{"#"+anchor if anchor else ""})'

def section(path, anchor):
    text = texts[path]
    start = text.index(f'<a id="{anchor}"></a>')
    m = re.search(r'\n<a id="[^\"]+"></a>', text[start+1:])
    return text[start:start+1+m.start()] if m else text[start:]

def excerpt(text):
    # Quoted source text is retained in its source language. Links inside it are inert.
    return '\n<details><summary>Source extract (unchanged text)</summary>\n\n```text\n'+text.strip()+'\n```\n\n</details>\n'

def anchor(id):
    return f'<a id="{id.lower()}"></a>\n'

FIELDS = ['record_id','record_type','title','status','source_file','source_anchor','source_ref',
          'related_adr','related_dl','related_at','related_risk','roadmap_phase','evidence_state',
          'row_kind','target_id','target_type','relationship_type','relationship_status',
          'architecture_component','registry_file','registry_anchor','source_tracking']

def row(id, typ, title, status, source='', loc='', ref='', kind='record', **kw):
    r = dict.fromkeys(FIELDS,'')
    r.update(record_id=id,record_type=typ,title=title,status=status,source_file=source,
             source_anchor=loc,source_ref=ref,row_kind=kind,evidence_state='Evidence Pending')
    r.update(kw)
    if source:
        r['source_tracking'] = 'Untracked at preflight' if source in untracked else 'Tracked at baseline'
    rows.append(r)
    return r

def edge(rec, target, typ, path, loc, ref, relationship='references', proposed=False):
    kw = dict(target_id=target,target_type=typ,relationship_type=relationship,
              relationship_status='Proposed Relationship' if proposed else 'Documented')
    field = {'ADR':'related_adr','DL':'related_dl','AT':'related_at','Risk':'related_risk',
             'Roadmap Phase':'roadmap_phase','Architecture Component':'architecture_component'}.get(typ)
    if field: kw[field]=target
    return row(rec['record_id'], rec['record_type'],rec['title'],rec['status'],path,loc,ref,kind='relationship',**kw)

def refs(text, prefix):
    return sorted(set(re.findall(r'\b'+prefix+r'-\d{2}\b',text)))

def add_source(rec, path, loc, ref):
    return row(rec['record_id'],rec['record_type'],rec['title'],rec['status'],path,loc,ref,kind='evidence')

# Each tuple below is one status-bearing statement. A status does not apply to a whole ADR.
# Full extracts preserve all conditions, alternatives and source qualifications.
DECISIONS = [
('PostgreSQL execution and canonical KPI equivalence',
 'SQLite reference functions need controlled translation. A product engine choice does not prove numerical equivalence.',
 [('Accepted','PostgreSQL is the only product database engine, for all 55 KPIs and custom queries.'),
  ('Requirement','Preserve the original source data, SQL, views, definitions and canonical results.'),
  ('Proposed','Store PostgreSQL translations with separate versions and original hashes.'),
  ('Proposed','Use an isolated SQLite reference oracle outside the product path.'),
  ('Open','Select the translation strategy, engine version, median implementation and input type profile.'),
  ('Open','Prove whole-result equivalence, including keys, dimensions, no-row, NULL, integer division, time, rounding, joins and all replay mornings.')],
 'Engineering handles translation. The project owner must confirm missing type or input contracts. No named appointee or original approval date is supplied.',
 'Record the missing contracts and inspect all-55 equivalence receipts. DL-19 separately controls changes to existing KPIs.'),
('Accepted orders input', 'Day 076 has 699 raw rows and 437 distinct payloads. RAW/DEDUP changes eight KPIs. The net B2C difference is 332,060,000 toman; it is not gross revenue.',
 [('Requirement','Preserve source occurrences and canonical definitions.'),('Proposed','Compare versioned RAW and exact-payload DEDUP modes with separate lineage and result namespaces.'),('Open','Obtain the accepted orders input policy or an official expected result.')],
 'The project supporter/organizer supplies the answer. The team then approves the policy implementation.',
 'Obtain the recorded source answer and relevant test receipts. Do not deduplicate events by order_id.'),
('Dependencies and selective recalculation','Table dependencies and equal values do not prove the minimum affected set.',
 [('Requirement','Preserve cutoff and canonical results.'),('Proposed','Start with full snapshot rebuilds; then recalculate affected KPIs and, if needed, exact keys.'),('Proposed','Separate value dependencies from execution dependencies; use wider recomputation when evidence is incomplete.'),('Open','Approve the optimization scope and dependency algorithm.')],
 'Data engineering and the test role are named as decision roles. No person is appointed.',
 'Compare selective and full rebuild results for late data, corrections and repeated events. Invalidate changed contributors even when values are equal.'),
('Source completeness and publication','A valid manifest or observed backfill does not prove source closure.',
 [('Requirement','Continue reports; report missing current values as null with a data issue.'),('Proposed','Keep reference values internally and hold unresolved dependent current values while independent outputs continue.'),('Open','Define source-interval closure and release of values after unresolved incidents.'),('Open','Approve eligibility, maximum age and wire mapping for dated last-valid context.')],
 'The organizer/source owner answers contract questions. Data and product roles handle design.',
 'Record closure evidence and publication policy, then test them. Prior context must retain its actual date, query, snapshot, unit and current access. It must never replace current null.'),
('Restatement and report versions','Later knowledge can change an old business date without changing the actual report sent that morning.',
 [('Proposed','Preserve immutable reports and separate as_reported, restated and counterfactual modes.'),('Proposed','Create a restated version with a new cutoff and explicit link to the first report.'),('Open','Select which changes require notice, who approves republication and which version a stable URL shows first.')],
 'Product and architecture roles.', 'Approve restatement and notification rules and inspect version/cutoff evidence. Historical corrections do not cancel past human decisions.'),
('Access control and query security','Shared tables do not supply complete row, column and purpose grants.',
 [('Requirement','Apply the supplied hierarchy and row controls to every user query.'),('Requirement','Permit individual workload data only to the direct supervisor; leave stays aggregate capacity and cannot support individual ranking.'),('Proposed','Use a resource/column/purpose/predicate policy catalog and scoped PostgreSQL views.'),('Proposed','Use read-only validated SELECT/CTE queries, function/table allowlists and roles without owner or BYPASSRLS privileges.'),('Open','Define shared-source predicates, historical scope, text redaction and derived-evidence projections.'),('Open','Define capacity aggregation and controls against small-group identification.')],
 'Security/architecture roles. The organizer can clarify the meaning of manager Q08 if needed.',
 'Review projections and pass negative access cases for joins, subqueries, UNION, CTE, errors, exports, logs, cache and role changes. The source hierarchy itself stays fixed.'),
('Signal and escalation edge cases','R1-R8 are fixed requirements; some comparisons and state transitions are incomplete.',
 [('Requirement','Apply all R1-R8, including > escalation duration, >=20% deterioration, <10% repeat suppression, >N% baseline deviation, no info alerts and the Jalali day-8 gate.'),('Requirement','Check recurrence at detection, report construction and final validation.'),('Proposed','Use named, versioned edge interpretations; strict threshold crossing is a proposal.'),('Open','Define equality, baseline direction, missing/holiday samples, zero denominators and minimum sample counts.'),('Open','Define unknown warning days, recovery/reset, multilevel escalation clocks, ranking weights and evidence-based grouping.')],
 'Product/analysis roles; organizer confirmation is needed for score-sensitive interpretations.',
 'Record the edge policy and rule-version fixtures. Do not invent a numeric warn for R3 or an epsilon denominator.'),
('Management calendar and input precedence','Static day-75 activation conflicts with next-morning manager-input effect.',
 [('Requirement','Apply the supplied cutoff and next-report input-effect rules.'),('Proposed','Use valid time, known time and an explicit report_population_policy.'),('Open','Select M11 first-report precedence: morning 75 gives 317 briefs; morning 76 gives 316.'),('Open','Define same-day question/upload ordering and attachment receipt/readiness.'),('Open','Define calendar known-at and future-plan visibility.')],
 'The organizer answers evaluation timing. Architecture roles handle event ordering.',
 'Obtain a recorded precedence contract and time fixtures. Keep M01-M10 for all 30 mornings. Neither 316 nor 317 is approved.'),
('Output status, precision and registered numbers','The brief and schema have different status terms; the internal Insight schema is incomplete.',
 [('Requirement','Use KPI-specific canonical rounding with zero tolerance after reference rounding.'),('Requirement','Allow registered scoped ad hoc queries; every published number needs actual SQL/result, definition, snapshot, scope and query reference.'),('Requirement','Use one shared Insight Brief as the report source with authorized role projections.'),('Proposed','Validate query_id for every published number even where the wire schema makes it optional.'),('Proposed','Keep suppression history in an internal ledger and open_items, pending approval.'),('Open','Resolve brief suppressed versus schema ongoing without changing the supplied schema.'),('Open','Define added-query/estimate wire mapping and the internal Insight projection contract.')],
 'The organizer resolves output contracts. Product/data roles handle internal presentation.',
 'Record the approved mapping and inspect numerical, scope and content fixtures. Shared analysis creates no access grant.'),
('Budget, models and execution limits','The daily limits cover all reports, analysis, conversation and retry.',
 [('Requirement','Keep total daily LLM cost at or below USD 5, daily runtime at or below 15 minutes on the stated machine, and simulated publication before 07:30.'),('Proposed','Use a provider-neutral gateway, atomic cost reservations, scoped cache and bounded tools/tokens.'),('Proposed','Test USD 3.5 for analysis/reports, USD 1 for QA and USD 0.5 reserve within the same USD 5 limit.'),('Open','Choose model, provider, gateway, tracing, exact limits and allocation rules.')],
 'Engineering/product roles. The organizer must supply the reference machine, rates and final limit profile.',
 'Approve the policy and measure all work, QA, retry, repair and extra model services. Report infrastructure cost separately.'),
('Correction conflicts and entity lifecycle','Some reference selections have no full ordering. No current correction tie was observed.',
 [('Proposed','Track conflicting corrections and payloads separately; quarantine affected uncertain outputs.'),('Open','Obtain a valid source precedence rule for equal-rank conflicts.')],
 'Data roles handle detection/quarantine. The contract owner handles precedence.',
 'Record precedence or quarantine policy and inspect conflict fixtures. Last-row, latest timestamp and greatest value are not supplied rules.'),
('Retention, backup and audit','Replay evidence and restricted logs need a recoverable preservation policy.',
 [('Proposed','Retain raw/config/query/report evidence for evaluation and use consistent archive/database backups with restore checks.'),('Open','Define post-evaluation retention, volume limits, backup periods, audit viewers and restore policy.')],
 'Architecture and operations roles.', 'Approve periods and access, then prove file hashes, snapshot rebuild and sample reports after restore. Derived cache need not be retained forever.'),
('One bounded AI Agent','Writer and Validator modules do not imply extra autonomous Agents.',
 [('Accepted','Use one bounded AI Agent with deterministic support modules.'),('Accepted','Keep KPI calculation, Signal detection, authorization and final validation deterministic.'),('Open','Approve tool calls, tokens, time, cancellation and evidence-review rounds.')],
 'Engineering handles the execution controller. S16 supplies no original approver name or approval date.',
 'Record limits and inspect AT-20/28 evidence. Do not reopen the one-Agent choice.'),
('Independent valid-report publication','A failed manager job does not invalidate another manager package. A partial day is still incomplete.',
 [('Accepted','Publish each valid manager report independently and record failed reports and partial-day outcomes.'),('Proposed','Commit one manager text/JSON package atomically.'),('Proposed','Use bounded retry and a deterministic validated template fallback.'),('Open','Define timeout, retry bounds, fallback content, failure/status export and replacement-version rules.')],
 'Product and engineering roles. Original approver names and dates are not supplied.',
 'Approve failure policies and inspect before-draft and validation-failure tests. A failure file is not a successful report.'),
('Workflow stage ownership','All three end-to-end owners are M01; this does not determine stage owners.',
 [('Requirement','Reconstruct WF1-WF3 from actual logs and preserve M01 ownership and the separate supplied stage and KPI contracts.'),('Proposed','Use a versioned stage responsibility catalog.'),('Open','Approve stage-to-team ownership and stage-delay routing, or retain explicit unresolved routing.')],
 'Product and data roles must approve the mapping.',
 'Record the mapping and test all stages, missing owners and unit-valued actors. Do not infer team-only foreign keys or change canonical KPI owners.'),
('Runtime files and operational documents','Uploads are required. Current CSV/JSON/MD fixtures do not define the full format requirement.',
 [('Requirement','Support structured nightly sources, authenticated manager input and file upload; the brief names Excel.'),('Proposed','Separate structured intake from untrusted document registration and preserve originals, receipt, audience, validation and lineage.'),('Proposed','Use PostgreSQL text retrieval for operational documents.'),('Open','Define exact Excel formats/validation, extra PDF support, file limits, retrieval and same-day readiness.')],
 'Product and engineering roles handle the format contract.',
 'Approve formats and inspect authorized/failed/injected uploads. Developer documents, audits and hidden labels are not product evidence. RAG/vector storage is not an approved dependency.'),
('Human decisions and actual execution','A decision or draft does not prove that an organizational action occurred.',
 [('Accepted','Humans control organizational decisions; the system cannot execute organizational actions.'),('Requirement','Create only drafts after a valid human decision; do not send messages or move staff.'),('Proposed','Separate decision, draft, human execution confirmation and observed follow-up states.'),('Open','Decide whether MVP stores execution confirmation, its authorized confirmer and its required evidence.')],
 'Product handles these details.',
 'Approve the confirmation contract and inspect AT-14/29 evidence. Fixed replay data must stay unchanged.')
]

adr_sections = {}
decision_recs = {}
decision_out = ['# Decisions Registry','', 'State: **Draft / Pending Review**. Task: `ARCH-REG-001`. Date: 2026-11-09.',
 '', 'Read the [Registry rules](README.md). Status applies to each numbered statement. A record can contain several statuses. The source extract keeps all original conditions and alternatives. English text is an index to that extract.',
 '', 'No named decision owner or original approval date is supplied for the Accepted baseline. Role references below are source roles. They are not new assignments. An Open acceptance gate does not reopen an Accepted boundary.']
counts = Counter()
for n, (title,context, statements,owner,closure) in enumerate(DECISIONS,1):
    id=f'ADR-{n:02d}'; a=id.lower(); src=section(D3,a); adr_sections[id]=src
    rec=row(id,'ADR',title,'Mixed; see statements',D3,a,id,registry_file='decisions-registry.md',registry_anchor=a)
    decision_recs[id]=rec
    decision_out += ['',anchor(id),f'## {id}: {title}', '',f'Problem / Context: {context}',
                     '',f'Decision owner: {owner}', '',f'Closure condition: {closure}',
                     '',f'Source Evidence: {link(D3,a,id)}. {link(D4,"question-map","Q01-Q17 status map")}.',
                     '', '| Statement ID | Decision Status | Statement |','|---|---|---|']
    for j,(status,statement) in enumerate(statements,1):
        sid=f'{id}-S{j:02d}'; counts[status]+=1
        decision_out.append(f'| {sid} | {status} | {statement} |')
        sr=row(sid,'Decision Statement',statement,status,D3,a,id,
               registry_file='decisions-registry.md',registry_anchor=a)
        edge(sr,id,'ADR',D3,a,'Parent ADR','part_of')
        if status=='Accepted':
            add_source(sr,D3,'decisions-1','Explicit five-boundary confirmation; S19')
            add_source(sr,'Docs/architecture/audit-2026-11-09/request.txt','','S19 section 1: accepted decisions')
    deps_dl=[];deps_at=[]
    # Source statements in the ADR supply these edges. Compressed AT lists are handled below.
    for target in refs(src,'ADR'):
        if target!=id: edge(rec,target,'ADR',D3,a,'ADR source text')
    for target in refs(src,'DL'): deps_dl.append(target);edge(rec,target,'DL',D3,a,'ADR source text')
    for target in refs(src,'AT'): deps_at.append(target);edge(rec,target,'AT',D3,a,'ADR source text')
    decision_out += ['', 'Accepted decision: '+('See the Accepted statement rows.' if any(s=='Accepted' for s,_ in statements) else 'No explicit Accepted statement is recorded for this ADR.'),
                     '', 'Proposed options and Open details: See the statement rows and the full extract.',
                     '', 'Consequences: The source constraints, effects and exceptions below remain in force. No proposed mechanism is approved by this extraction.',
                     '', 'DL / AT dependencies in the ADR: '+(', '.join(deps_dl+deps_at) or 'No explicit ID in this ADR text; see inbound DL references in the matrix.')+'.', excerpt(src)]
write('decisions-registry.md','\n'.join(decision_out))

# Read the existing Decision Log once. It remains the source record.
dl_rows={}
for line in texts[D3].splitlines():
    if re.match(r'\| DL-\d{2}',line):
        cells=[x.strip() for x in line.strip('|').split('|')]
        dl_rows[cells[0][:5]]=cells
assert len(dl_rows)==19

# T=team, O=organizer/source, E=engineering evidence. These route unresolved work;
# they do not appoint people. Exact source role wording stays in the source extract.
ISSUE_META = [
('All-55 PostgreSQL equivalence','TE','Record the type/translation contract and compare complete results for all 55 definitions and replay mornings.'),
('RAW versus exact-payload DEDUP','TOE','Obtain the official policy or expected result, then test the approved input mode.'),
('Source closure, publication and dated prior values','TOE','Obtain source-interval closure and release contracts, dated-context age/mapping, and test missing/empty/backfill cases.'),
('Selective rebuild and restatement','TE','Approve rebuild scope and restatement notice/version policy, then compare selective and full outputs.'),
('Conflicting payload precedence','TOE','Obtain valid precedence or approve quarantine, then test equal-rank conflict cases.'),
('Shared-source access projections','TOE','Review row/column/purpose predicates, historic scope and text redaction, then inspect negative access tests. Ask the organizer only about unresolved source meaning.'),
('Capacity formula and privacy','TOE','Approve headcount or an hours measure with a valid hours contract, redaction and small-group controls; test them.'),
('Stage ownership and delay routing','TE','Approve the stage mapping without changing M01 end-to-end ownership or canonical owners; test all 12 stages and unknown actors.'),
('Signal edge rules and state','TOE','Record equality, baseline, zero, missing-day and reset policy, then test every R1-R8 boundary.'),
('M11, same-day uploads and calendar known-at','TOE','Obtain precedence and receipt/readiness contracts. Test 316 and 317 scenarios until one is approved.'),
('Suppressed/ongoing and internal Insight schema','TOE','Obtain the status/wire mapping, internal Insight schema and authorized projection contract; test actual-date context and evidence review records.'),
('Decision follow-up and execution confirmation','TE','Approve the MVP confirmation scope, actor/time/subject links, decision-to-observation mapping and evidence; test human-only actions.'),
('Retry, timeout, fallback and failure export','TE','Approve bounded failure/export/replacement policy and inspect pre-draft and validation-failure receipts.'),
('Agent, model, gateway and budget limits','TOE','Approve model/provider/product/limits/rates and budget allocation; obtain final organizer profile, then benchmark all work.'),
('Retention, backup, audit access and restore','TE','Approve periods and audit viewers, then inspect consistent backup and reproducible restore evidence.'),
('Final evaluation profile and missing contracts','OE','Obtain official hardware/profile, hidden evaluation results and a full raw dictionary or recorded disposition of missing contracts.'),
('NULL dimensions and added query numbers','TOE','Approve no-dimension/NULL/empty/new-dimension and ad hoc serialization without an invented sentinel; test fixtures.'),
('Complete content, signal selection and history','TE','Approve full chart/card/content mapping and Candidate/Open/Published transitions; test >5 candidates, authorized history and separate suppression.'),
('KPI changes, activation authority and rollback','TE','Approve the distinction between fixed reference definitions and allowed management changes, with write authority, effect time and rollback; test add and change independently.')
]

EXTRAS = [
('REG-ISS-001','P2/P3 Workflow milestone scope',D3,'decisions-6','TE',
 'The phase table places Workflow in P3. The full-day P2 note requires summaries of all three Workflows. The note is also Proposed.',
 'P2 completeness and phase dependencies are unclear. Required report content cannot be omitted.',
 'Minimum Workflow output in P2 with historical/edge depth in P3; or approved milestone definitions that retain every requirement.',
 'No owner is specified.', 'Record the team scope and dependency decision, then inspect AT-12/15/25/26 outputs.',
 ['ADR-15'],[],['AT-12','AT-15','AT-25','AT-26'],['P2','P3']),
('REG-ISS-002','QA record context and links',D2,'data-2','TE',
 'The source QA schema has required fields, but the internal model does not define links among the authenticated manager, authorized scope, question, snapshot/interactive revision and actual QueryRun results.',
 'The answer and refusal context cannot be reconstructed from the stated record contract.',
 'A reviewed logical mapping is required. No entity name or physical key is selected in the source.',
 'Not documented.', 'Review the logical mapping and answer/refusal samples. Refusals must not create fictional queries or rows.',
 ['ADR-06','ADR-09'],[],['AT-16','AT-30'],[]),
('REG-ISS-003','Workflow stage calculation evidence',D2,'data-2','TE',
 'WorkflowStageObservation does not define retained populations, included/excluded cases, SLA numerator/denominator, calculation Query or bottleneck summary result.',
 'Stage summaries cannot be traced to cases and actual calculations. Ownership in DL-08 is a separate issue.',
 'Review summary-to-case/query storage mapping. No physical design alternative is supplied.',
 'Not documented.', 'Record the logical mapping and inspect case/query evidence, including open and unknown cases. Do not replace stage measures with canonical Workflow KPI formulas.',
 ['ADR-15'],['DL-08'],['AT-12','AT-25'],[]),
('REG-ISS-004','DQ-to-Signal eligibility record',D2,'data-5','TE',
 'The model has quality and invalidation states, but no explicit versioned evaluation link among DQIncident, affected KpiObservation and Signal eligibility.',
 'A data fault or historical value revision can be mistaken for a business Signal.',
 'Review the state-to-eligibility mapping. The source selects no publication policy or unknown-data rule.',
 'Not documented.', 'Record the mapping and receipts for missing, late, corrected, duplicate and schema-change inputs, plus a positive business-deviation control.',
 ['ADR-04','ADR-07'],['DL-03','DL-09'],['AT-04','AT-05','AT-08','AT-24'],[]),
('REG-ISS-005','Claim of about 70 KPI outputs',D3,'decisions-8','E',
 'The prior team claim of about 70 outputs has no inspectable calculation output. The dictionary has 55 definitions. About 150 in the brief is an estimate.',
 'Definition, series and observation counts can be confused and can create false acceptance claims.',
 'Use a reproducible series inventory. No new KPI, dimension or target count is authorized.',
 'Not documented.', 'Supply Definition/Entity/Dimension/date/snapshot/query inventory and a reproducible count method.',
 [],[],['AT-02','AT-10'],[]),
('REG-ISS-006','P5 delivery evidence gap',D3,'decisions-6','E',
 'P5 table alone omits the full delivery checklist stated in the supplement.',
 'Docker success alone cannot prove complete delivery.',
 'Preserve the full existing checklist: three UIs, complete Git history, install and KPI/Source/management-level guides, model/API and infrastructure cost reports, and a 10-minute Demo Day presentation.',
 'Not documented.', 'Inspect item paths/versions, Docker/replay logs, three-UI evidence and cost reports. This task authorizes no commit or push.',
 [],[],['AT-11','AT-12','AT-18','AT-19'],['P5']),
('REG-ISS-007','Physical contracts and detailed model evidence',D2,'data-2','TE',
 'Logical model contracts remain Proposed. Physical keys, nullable foreign keys, indexes and many-to-many records are not approved. Existing Structurizr views do not show entity, row-lineage or complete dated-grant detail.',
 'A diagram can be mistaken for a validated schema or a complete value/access proof.',
 'Review physical contracts and the existing SG-04/05/13 proposals in a later authorized model task. Do not invent source keys or grants.',
 'Data architecture team is a review role in VQ08; no named appointee is supplied.',
 'Record the reviewed contracts; inspect required detail and, after separate authorization, model syntax/layout. Current text inventories do not prove these checks.',
 [],['DL-15','DL-16'],[],[]),
('REG-ISS-008','Historical workspace and tooling statements',D4,'verification','TE',
 '003 says that this workspace has no Git repository; 004 says Git is unavailable. These are historical audit statements. The current local repository and baseline are present. SG-01 also records stale authority/view-count comments; SG-14 records a retired diagram generator.',
 'A later reader or generator can use stale context or overwrite corrected documentation.',
 'Retain historical audit evidence. Review current context notes and retire/adapt the old generator in a later scoped task.',
 'Not documented.', 'Record the review outcome and verify any later authorized reference/tooling changes. Do not change the protected files in this task.',
 [],[],[],[]),
('REG-ISS-009','Runtime upload formats and retrieval',D3,'adr-16','TE',
 'Excel is named in the brief, but exact Excel formats/validation, optional PDF support, file limits and retrieval are not selected. Current CSV/JSON/MD fixtures do not settle this contract.',
 'Intake, parsing and retrieval scope cannot be accepted from fixture coverage alone. Receipt timing stays in DL-10.',
 'Separate document registration and structured intake; PostgreSQL text retrieval is Proposed. Extra PDF and RAG support are not approved dependencies.',
 'Product and engineering are the documented roles; no person is appointed.',
 'Record the format/size/retrieval contract and inspect valid, unsupported, failed and injected upload cases.',
 ['ADR-16'],['DL-10'],['AT-03','AT-13','AT-22'],[]),
('REG-ISS-010','S01 PDF provenance hash differs',D1,'system-2','OE',
 'Documents 001 and 004 record S01 SHA-256 6d68d3fcc285f6908af0d97c0429dfefb489f00b7f6538ed03573552ed6955f8. The actual local PDF has SHA-256 f6761b4fc37145d152f2b9793b298e35f48db666d5205c4d02be0f5f13e4863b. The initial and final local hashes are equal.',
 'The source provenance statement cannot be confirmed for this exact PDF version. A byte-hash difference alone does not establish a requirement change.',
 'Obtain source-version provenance or inspect content equivalence against the reviewed PDF/Markdown. No requirement change or source precedence is selected.',
 'No owner is documented for this newly observed provenance gap. Source authority clarification is required.',
 'Record the correct source version and content comparison evidence before attributing the old visual-review result to this exact PDF. Preserve both hashes and the existing files.',
 [],['DL-16'],[],[])
]

TYPE_NAMES={'T':'Team Decision Required','O':'Organizer / Source Clarification Required','E':'Engineering Evidence Required'}
issues=[]
issue_out=['# Open Issues Registry','','State: **Draft / Pending Review**. All records are **Open**. Required evidence is **Evidence Pending**.',
 '', 'One main record exists for each issue. Source variants are facets of that record. Role names from the Decision Log are proposed roles, not appointments. Route classes identify the type of work; they do not name an owner. Options remain unselected.']

def issue_entry(id,title,types,path,loc,conflict,impact,options,owner,closure,adrs,dls,ats,phases=(),raw='',extra_sources=()):
    rec=row(id,'DL' if id.startswith('DL-') else 'Registry Issue',title,'Open',path,loc,id,
            registry_file='open-issues-registry.md',registry_anchor=id.lower())
    issues.append(dict(id=id,title=title,types=types,rec=rec,ats=ats))
    issue_out.extend(['',anchor(id),f'## {id}: {title}','','Status: **Open**. Evidence state: **Evidence Pending**.',
                      '', 'Required work: '+ '; '.join(TYPE_NAMES[t] for t in types)+'.',
                      '', f'Exact conflict / missing evidence: {conflict}', '',f'Effect: {impact}',
                      '',f'Existing options: {options}', '',f'Decision owner: {owner}', '',f'Closure criterion: {closure}',
                      '',f'Source Evidence: {link(path,loc)}.',
                      '', 'Dependencies: '+(', '.join(adrs+dls+ats+list(phases)) or 'No explicit ID is supplied.')+'.'])
    for targets,typ in [(adrs,'ADR'),(dls,'DL'),(ats,'AT'),(phases,'Roadmap Phase')]:
        for target in targets:
            # Extra ATs without an explicit ID at the cited source are useful suggestions only.
            proposed = id in ['REG-ISS-002','REG-ISS-003','REG-ISS-004','REG-ISS-007'] and typ=='AT' and target not in section(path,loc)
            edge(rec,target,typ,path,loc,'Source section; proposed when no explicit ID is given',proposed=proposed)
    for ep,ea,er in extra_sources:
        add_source(rec,ep,ea,er);issue_out.extend(['',f'Additional Source Evidence: {link(ep,ea,er)}.'])
    if raw: issue_out.append(excerpt(raw))
    return rec

# Every outside-DL facet below is retained under its existing semantic issue.
FACETS = {
 'DL-01': [('Versioned input types and integer/empty-value behavior',D2,'data-6')],
 'DL-06': [('Historic marketplace access; raw text/customer redaction; shared-resource predicates',D1,'system-10')],
 'DL-07': [('Working hours, effective staff dates, small groups and free-text personal data',D2,'data-9')],
 'DL-08': [('WF1.5 follow-up ticket category/time projection and missing SLA; unit-valued actor_team',D1,'system-7')],
 'DL-09': [('Ranking, cause grouping, multilevel recipient clocks and confidence in unknown states',D1,'system-7')],
 'DL-10': [('Historical scope and calendar future-plan visibility; manager Q09 before upload IN07',D2,'data-9')],
 'DL-11': [('Evidence independence storage: groups, result, reason, review version and authorized Insight recipient',D2,'data-8')],
 'DL-12': [('Decision follow-up evidence and actor/time/subject history, separate from actual action execution',D2,'data-8')],
 'DL-16': [('Absent event occurrence IDs, customer/campaign registries and full raw dictionary',D2,'data-4')],
 'DL-17': [('KPI-specific precision, query-number mapping and actual NULL versus no dimension',D2,'data-2')],
 'DL-18': [('Candidate/Open/Published selection and authorized history outside Top 5',D3,'decision-log'),
           ('Qualitative cause confidence versus optional numeric 0..1; source-family aliases and complete internal content/wire mapping',D1,'system-9'),
           ('Read/close/refer actor, time and subject history; no implied action execution',D2,'data-8')],
 'DL-19': [('Existing KPI formula/owner/target changes versus fixed 55 reference definitions; add and change are separate tests',D3,'adr-01')]
}
for n,(title,types,closure) in enumerate(ISSUE_META,1):
    id=f'DL-{n:02d}'; cells=dl_rows[id]; raw='| '+' | '.join(cells)+' |'
    adrs=refs(raw,'ADR'); ats=refs(raw,'AT')
    # The source abbreviates AT-02,03,05,17. Preserve every member.
    ats=sorted(set(ats+['AT-'+x for m in re.finditer(r'AT-([0-9]{2}(?:[,،]\s*[0-9]{2})+)',raw) for x in re.findall(r'\d{2}',m.group(1))]))
    extras=[(p,a,label) for label,p,a in FACETS.get(id,[])]
    rec=issue_entry(id,title,types,D3,'decision-log',cells[2], 'See the exact source options and effects below.',cells[3],
                     'Proposed source role: '+cells[4],closure+' Source gate: '+cells[5],adrs,[],ats,raw=raw,extra_sources=extras)
    for label,p,a in FACETS.get(id,[]):
        issue_out.extend(['',f'Preserved source facet: {label}. See {link(p,a)}.'])
    # Reverse edges retain the source of each DL association.
    for adr in adrs:
        if adr in decision_recs: edge(decision_recs[adr],id,'DL',D3,'decision-log',id,'has_open_detail')
for item in EXTRAS:
    id,title,p,a,types,conflict,impact,opts,owner,close,adrs,dls,ats,phases=item
    issue_entry(id,title,types,p,a,conflict,impact,opts,owner,close,adrs,dls,ats,phases,
                raw=section(p,a) if id in ['REG-ISS-002','REG-ISS-003','REG-ISS-004','REG-ISS-005'] else '')
write('open-issues-registry.md','\n'.join(issue_out))

# Risk records stay separate from issue and test records. Risk links not explicitly
# named by the source are marked Proposed Relationship in the generated index.
RISK_BASE = [
('Future data exposure','Facts or preloaded files can include knowledge beyond the cutoff.','A historical report can look correct but be invalid.','Filter before projection; use future-data injection fixtures and snapshot hashes.',['ADR-08'],['DL-10'],['AT-03']),
('Unclear input grain','RAW and DEDUP can feed different populations to joins.','Canonical values can differ from evaluator results.','Keep separate modes and obtain the official input answer.',['ADR-02'],['DL-02'],['AT-02','AT-05']),
('Manifest mistaken for completeness','A manifest can omit a missing source.','False zero values or early incident closure can be reported.','Use expected-source contracts, separate closure and missing/empty tests.',['ADR-04'],['DL-03'],['AT-04','AT-23']),
('SQL translation drift','PostgreSQL and the reference oracle can differ in time, types, rounding and selected row sets.','Even a hundredth-hour difference can break acceptance.','Use one PostgreSQL product path, versioned translations, original hashes and an independent reference oracle.',['ADR-01'],['DL-01'],['AT-02','AT-05']),
('Raw query or cache exposure','Results, query context, cache or logs can carry another manager scope.','Restricted data can reach a manager or the LLM.','Apply RLS, scoped cache keys, separate worker identity and adversarial query tests.',['ADR-06'],['DL-06'],['AT-06','AT-13']),
('Historical correction mistaken for a business Signal','A knowledge revision can change an old value.','False alerts and escalation can follow.','Keep knowledge_revision and incident links separate from business eligibility.',['ADR-04','ADR-07'],['DL-03','DL-09'],['AT-04','AT-05','AT-24']),
('Hardcoded development events','Runtime logic can depend on known incident dates or IDs.','The product can fail on hidden data.','Vary dates, identifiers, dimensions and delivery order in separate fixtures.',['ADR-08'],['DL-16'],['AT-19']),
('Recurrence without recipient state','One state shared among recipients can erase or repeat their history.','The owner can miss a warning or a parent can receive a duplicate.','Keep episode and recipient state separate and test the escalation chain.',['ADR-07'],['DL-09'],['AT-08','AT-24']),
('Unsupported causes','Two dependent measurements can look like two independent witnesses.','A fabricated cause can receive high confidence.','Use lineage-aware evidence review and deterministic validation outside the LLM.',['ADR-09'],['DL-11','DL-18'],['AT-10']),
('Causal claim from a simulated decision','A decision record and later change can be mistaken for proof of execution or effect.','The report can attribute an effect without evidence.','Compare observations with calendar context and stated limits; preserve fixed replay data.',['ADR-17'],['DL-12'],['AT-14','AT-29']),
('Growth in managers or questions','More reports, QA and retries consume shared daily resources.','Time or cost limits can fail.','Consider template writing, reservations and authorized cache; measure the worst day.',['ADR-10','ADR-13','ADR-14'],['DL-13','DL-14'],['AT-17','AT-18','AT-28']),
('Current lifecycle replaces reference facts','An operational state can be substituted for canonical MIN/MAX selections.','Backlog or SLA can change without source authority.','Keep operational projections separate and retain the formula hash.',['ADR-11'],['DL-05'],['AT-02','AT-05'])
]
RISK_EXTRA = [
('Prompt injection from operational text',D1,'system-10','A ticket or upload contains instructions.','Policy, numbers, recipients or actions can be changed.','Treat text as untrusted data and check destination, number and tool authority independently.',['ADR-06','ADR-16','ADR-17'],['DL-06'],['AT-13','AT-22']),
('Premature attachment evidence',D1,'system-5','A question can precede receipt or readiness of its attachment.','The answer can use evidence unavailable at question time.','Record attachment dependency, receipt and readiness; use clarification/data-unavailable when needed.',['ADR-08','ADR-16'],['DL-10'],['AT-03','AT-22']),
('Incomplete day mistaken for success',D2,'data-11','A required manager job can fail before a draft exists.','Successful independent packages can hide missing daily coverage.','Track job/export/day outcomes separately and record failure even without a draft.',['ADR-14'],['DL-13'],['AT-15','AT-21','AT-28']),
('Unapproved status serialization',D1,'system-9','The brief uses suppressed and the schema uses ongoing.','Output can violate schema or silently lose suppression meaning.','Preserve history and obtain a valid output mapping without changing the source schema.',['ADR-09'],['DL-11'],['AT-11','AT-30']),
('Ambiguous correction precedence',D2,'data-3','Equal-rank conflicting corrections have no supplied secondary order.','An arbitrary payload can be reported as valid.','Record conflict; obtain source precedence or review quarantine. No current correction tie is claimed.',['ADR-11'],['DL-05'],['AT-05']),
('Unrecoverable history',D2,'data-11','Inconsistent archive/database backup or early retention removal can break replay.','Historical reports and their source evidence cannot be reconstructed.','Approve retention/backup policy and test file hashes, snapshot rebuild and sample reports after restore.',['ADR-12'],['DL-15'],['AT-19']),
('Small-group or free-text identification',D1,'system-10','Aggregate capacity or title/blocker text can identify a person.','A higher manager can receive restricted individual or leave data.','Review redaction, purpose and group-size controls; test derived claims and text paths.',['ADR-06'],['DL-06','DL-07'],['AT-06','AT-10']),
('Reference KPI overwritten by management change',D3,'decision-log','Configurable formula/owner/target changes can be confused with changes to the fixed 55 reference definitions.','Canonical evaluation and previous versions can change without authority.','Obtain the DL-19 lifecycle policy; preserve the reference and separately test add/change, effect time and rollback.',['ADR-01','ADR-06','ADR-08'],['DL-19'],['AT-27','AT-29'])
]
risk_out=['# Risk Register','','State: **Draft / Pending Review**.',
 '', 'Severity: **Not Assessed** for every record. The sources supply no risk scoring method. Audit finding severity is not a risk score.',
 '', 'Control state: **Evidence Pending / Not Executed**. Source requirements remain requirements. Engineering controls remain Proposed unless the source explicitly approves them. No control effectiveness is claimed.',
 '', 'The two section-5 SQL translation/oracle risks form one main record. Their two source rows remain below. Other distinct effects stay separate.']
raw_risks=[]
for line in section(D3,'decisions-5').splitlines():
    if line.startswith('| ') and not line.startswith('| ریسک'):
        raw_risks.append(line)
assert len(raw_risks)==13
risk_recs=[]
for k,item in enumerate(RISK_BASE+RISK_EXTRA,1):
    if k<=12:
        title,cause,effect,control,adrs,dls,ats=item;p=D3;a='decisions-5'
        original_indices = [3,11] if k==4 else [k-1 if k<=11 else 12]
        source_extract='\n'.join(raw_risks[i] for i in original_indices)
    else:
        title,p,a,cause,effect,control,adrs,dls,ats=item;source_extract=''
    id=f'REG-RSK-{k:03d}'
    rec=row(id,'Risk',title,'Open',p,a,'Risk extraction',registry_file='risk-register.md',registry_anchor=id.lower())
    risk_recs.append(rec)
    risk_out.extend(['',anchor(id),f'## {id}: {title}', '',f'Cause: {cause}', '',f'Consequence: {effect}',
                     '',f'Control: {control}', '', 'Control status: **Evidence Pending**. The product control is not executed.',
                     '', 'Severity: **Not Assessed**.', '',f'Source Evidence: {link(p,a)}.',
                     '', 'Related ADR / DL / AT: '+', '.join(adrs+dls+ats)+'.',
                     '', 'Evidence needed: The applicable source/policy answer, approved control contract and actual receipts for the related tests. Inspect both positive and negative cases before any risk reduction claim.'])
    for targets,typ in [(adrs,'ADR'),(dls,'DL'),(ats,'AT')]:
        for t in targets: edge(rec,t,typ,p,a,'Risk-to-record review aid; source does not state this complete mapping',proposed=True)
    if source_extract: risk_out.append(excerpt(source_extract))
write('risk-register.md','\n'.join(risk_out))

AT_TITLES = ['Intake and idempotency','PostgreSQL equivalence','Cutoff and replay','Missing, empty and backfill',
 'Duplicates, schema and correction','Authorization','Organization and configuration changes','Recurrence and escalation',
 'Event detection','Evidence support','Output and user interfaces','Three Workflows','Prompt injection',
 'Decision and action','Daily report coverage','Manager QA','Performance','Cost','Generalization and delivery',
 'One bounded Agent','Failure and publication','Upload boundary','Dated historical context','All R1-R8 rules',
 'Every Workflow stage','Complete role report content','Controlled configuration and KPI extension',
 'Parent execution grant','Manager-input lifecycle','Exact output contracts']
AT_EVIDENCE = [
 'Manifest/actual/expected comparisons, unchanged hashes, retry receipts, independent-source extension diff and regression receipts.',
 'All 55 source/translated SQL hashes, engine/type/input-policy versions and complete result comparisons for every replay morning and edge case; zero tolerance after canonical rounding.',
 'Snapshots and query receipts for mornings 62-91, D-1 cutoffs, future-data negative cases and initial CRM history.',
 'Missing/empty/backfill reports with null and issue links; separate 32 support changes from two payment changes.',
 'Separate RAW/DEDUP outputs, header-alias receipts and L02045 correction eligibility from morning 71; no actual-report counterfactual.',
 'Positive and negative access receipts in all three levels, including result, prompt, cache, export, log, errors and source-row drill-down.',
 'Metadata revisions, approved clock, IN06 report-79 effect, cache/grant revisions and added-team/level tests.',
 'Per-recipient history, rule/owner versions, <10% recurrence cases, escalation reasons, max-five outputs and Candidate/Open/Published mapping.',
 'Official labeled event results: correct owner report, within 24 hours, correct KPI/entity and label-consistent cause; at least 90%. Hidden labels are absent.',
 'Actual QueryRun/Snapshot references for every number and cause; reviewed evidence independence, positive/negative shared-population cases and full number-to-file lineage.',
 'Brief/QA schema receipts; authenticated Persian RTL assistant and role-dashboard sessions at three levels; authorized drill-down, decision/referral history and mentioned_staff_ids checks.',
 'Case/stage evidence for three Workflows, supplied SLA versus canonical KPI checks, repeats/open/unknown cases, M01 ownership, approved routing and executive-only Persian RTL control-room sessions.',
 'Injected tickets/uploads/header/filename cases with unchanged permissions, numbers, recipients and action boundaries.',
 'Valid-decision/draft linkage, before/after evidence, valid effect_direction, versioned deadlines/status/reminders and no organizational send/execute call.',
 'The approved active roster for every morning, one valid package per required manager, no duplicate retry package, incomplete failed days and role-content checks.',
 'All 16 supplied manager questions with clock/scope/definition/refusal receipts, plus official evaluator results of at least 85%; supplied samples alone cannot prove that score.',
 'Every day ingest-to-JSON/validation elapsed time on the declared machine, at most 15 minutes, simulated publication before 07:30; warm/cold recorded separately.',
 'Every day actual model cost at most USD 5; token, retry, cache, dated rates and reservation ledgers, including QA and repairs; controlled exhaustion outcomes.',
 'New-root/config run without code edits, one Docker command, restart/restore receipts, no fixed incident/date IDs and the full P5 delivery inventory.',
 'One-Agent execution trace, deterministic calculation/Signal/access/final validation receipts and approved tool/token/time/cancel limits.',
 'One pre-draft failure and one validation failure; independent once-only valid publication, paired text/JSON, visible failed required jobs, incomplete day and bounded rewrite/revalidation traces.',
 'Approved format list, identity/audience/receipt/readiness, parse failure and injection fixtures; no unavailable attachment evidence.',
 'Current null plus issue and historical value with actual date/query/snapshot/unit/current authorization under an approved mapping; no substitution.',
 'Separate and combined R1-R8 cases at detection, report construction and final validation; fixed comparison/owner/history/holiday/info/Jalali-day gates and five DQ cases with positive business control.',
 'All 12 stages with from/to events, numeric SLA versus deadline versus no-SLA, median targets, WF2 48h and separate canonical WF3 conditions; unresolved owners stay explicit.',
 'Eight Insight sections, required charts/cards/health/pending decisions/open actions/dashboard/status, plus every role-matrix cell with content/empty/missing/denied cases. Monthly board summary remains optional.',
 'Preserved 55 definitions; inactive candidate SQL/type/unit/scope/rollup validation, approval and versioned activation; separate add and change tests, write authorization, effect time, rollback and retained prior results.',
 'Parent/child request chain for model/tool/query/retry/upload/repair with nonresetting limits; timeout/cancel/budget and before/after-draft failure receipts. Exact limits require approval.',
 'All 23 authorized input events, all 16 QA files and seven non-question effects with receipt/effect/idempotency; separate close/referral fixtures, unchanged dataset and upload text not treated as a decision.',
 'Every required/nested schema field/type/enum/maxItems/date/value plus all text numbers (Persian, Arabic, Latin and separators) paired with actual JSON/query results; reject unsupported/mismatched/unexecuted SQL numbers.'
]
basis_path='Docs/architecture/audit-2026-11-09/acceptance-basis.csv'
basis={r['test_id']:r for r in csv.DictReader((ROOT/basis_path).open(encoding='utf-8-sig',newline=''))}
at_raw={}
for line in texts[D3].splitlines():
    m=re.match(r'\| <a id="at-\d{2}"></a>(AT-\d{2}) \|',line)
    if m: at_raw[m.group(1)]=line
assert len(at_raw)==30
at_out=['# Acceptance Register','','State: **Draft / Pending Review**.',
 '', 'All 30 tests have execution status **Planned / Not Executed** and evidence state **Evidence Pending**. No product execution receipt is supplied for these gates. Earlier dataset audits and document checks do not make a product test pass.',
 '', 'The source criteria are retained in full under each test. Common supplements below are part of the linked tests. They are not new tests. Source classifications describe authority; they are separate from execution status.']
at_recs={}
for n,(title,ev) in enumerate(zip(AT_TITLES,AT_EVIDENCE),1):
    id=f'AT-{n:02d}'; a=id.lower(); b=basis[id]
    rec=row(id,'AT',title,'Planned / Not Executed',D3,a,id,registry_file='acceptance-register.md',registry_anchor=a);at_recs[id]=rec
    add_source(rec,basis_path,'',id+': '+b['source'])
    inbound_adr=sorted(set(r['record_id'] for r in rows if r['record_type']=='ADR' and r['related_at']==id))
    inbound_issues=sorted(i['id'] for i in issues if id in i['ats'])
    at_out.extend(['',anchor(id),f'## {id}: {title}', '',f'Goal: {title}.',
                   '', 'Execution status: **Planned / Not Executed**. Evidence state: **Evidence Pending**.',
                   '', f'Reference contract / authority: **{b["basis_status"]}**. {b["source"]}.',
                   '',f'Unapproved mechanism or gap: {b["mechanism_or_gap"]}.',
                   '',f'Required evidence and acceptance checks: {ev}',
                   '', 'Related decisions / issues: '+(', '.join(inbound_adr+inbound_issues) or 'See the requirement and source edges in the matrix.')+'.',
                   '',f'Source Evidence: {link(D3,a,id)}; {link(basis_path,"","authority basis")}.',excerpt(at_raw[id])])
    for t in inbound_adr: edge(rec,t,'ADR',D3,t.lower(),'ADR references this AT','referenced_by')
    for issue in issues:
        if id in issue['ats']:
            ir=issue['rec'];proposed=any(r['record_id']==issue['id'] and r['related_at']==id and r['relationship_status']=='Proposed Relationship' for r in rows)
            edge(rec,issue['id'],'DL' if issue['id'].startswith('DL-') else 'Registry Issue',ir['source_file'],ir['source_anchor'],'Issue test dependency','referenced_by',proposed)

# Keep all supplements and matrices as exact source extracts, without new source anchors.
s=texts[D3]
supplements=[
 ('supplement-tests','AT supplements',s[s.index('#### تکمیل معیارهای آزمون موجود'):s.index('#### ماتریس محتوای اختصاصی')],['AT-01','AT-19','AT-27','AT-10','AT-06','AT-30','AT-11','AT-24','AT-04','AT-05','AT-08','AT-21','AT-28','AT-14','AT-29']),
 ('role-matrix','Three management levels: full content matrix',s[s.index('#### ماتریس محتوای اختصاصی'):s.index('#### موارد اختصاصی قواعد')],['AT-06','AT-11','AT-12','AT-14','AT-15','AT-26','AT-29']),
 ('rule-matrix','R1-R8: complete acceptance cases',s[s.index('#### موارد اختصاصی قواعد'):s.index('### ۷.۱.')],['AT-24']),
 ('oracle-boundaries','Calculation, quality and discovery oracles',s[s.index('### ۷.۱.'):s.index('<a id="manager-question-map">')],['AT-02','AT-04','AT-09']),
 ('input-and-negative-cases','Manager questions, seven other inputs and adversarial cases',section(D3,'manager-question-map'),['AT-03','AT-06','AT-07','AT-13','AT-14','AT-16','AT-22','AT-29']),
 ('measurement','Daily performance and cost measurement',section(D3,'decisions-8'),['AT-17','AT-18']),
 ('delivery-checklist','P5 full delivery checklist',s[s.index('تکمیل شرط تحویل P5'):s.index('در هر مرحله، CSVهای audit')],['AT-11','AT-12','AT-18','AT-19'])
]
at_out.extend(['',anchor('supplements'),'## Shared source criteria', '', 'Apply each supplement to its listed ATs. The quoted source language and all numbers, conditions and negative cases are retained.'])
for aid,title,raw,ats in supplements:
    loc='manager-question-map' if aid=='input-and-negative-cases' else ('decisions-8' if aid=='measurement' else ('decisions-6' if aid=='delivery-checklist' else 'decisions-7'))
    at_out.extend(['',anchor(aid),f'### {title}', '', 'Related tests: '+', '.join(ats)+'.', '',f'Source Evidence: {link(D3,loc)}.',excerpt(raw)])
    for t in ats:
        add_source(at_recs[t],D3,loc,title)
        # A separate local supplement pointer avoids comma-packed relation cells.
        edge(at_recs[t],aid,'Acceptance Supplement',D3,loc,'Full source supplement','has_criteria')
write('acceptance-register.md','\n'.join(at_out))

# Locate every S01-S19 member in the source register. Paths are resolved against 001.
source_paths={}
source_raw={}
for line in texts[D1].splitlines():
    m=re.match(r'\| (S\d{2}) \|',line)
    if not m: continue
    sid=m.group(1);source_raw[sid]=line
    found=[]
    for url in re.findall(r'\]\(([^)]+)\)',line):
        path=(ARCH/unquote(url)).resolve()
        found.append(path.relative_to(ROOT).as_posix())
    source_paths[sid]=found
assert len(source_paths)==19
source_lines=['# Source inventory','','State: **Draft / Pending Review**.',
 '', 'S01-S19 keep the IDs from document 001. Each listed member exists locally. Availability does not prove approval or a product test result. Directory sources retain their scope; they are not single-file contracts.',
 '', '| Source | Actual local members | Authority / limits | Tracking at preflight |','|---|---|---|---|']
for sid,paths in source_paths.items():
    authority = ('Official requirement source; preserve its exact contract.' if sid in ['S01','S02','S03','S04','S05','S06','S07','S11','S12'] else
                 'Supplied historical/source data. Preserve source facts; old report definitions are not current KPI contracts.' if sid in ['S13','S14'] else
                 'Historical audit Observation; no product acceptance claim.' if sid in ['S08','S09','S10','S15'] else
                 'Recorded Q01-Q17 review. The result table and body have statement-level authority.' if sid=='S16' else
                 'Existing target model. A proposal or component declaration alone is not team approval.' if sid=='S17' else
                 'Markdown conversion beside the official brief; retain PDF page references.' if sid=='S18' else
                 'Prior audit request: explicit confirmation of five Accepted boundaries.')
    tracking=[]
    for p in paths:
        assert (ROOT/p).exists(),p
        rec=row(sid,'Source',sid,'Source evidence',D1,'system-2',sid,evidence_state='Available')
        rec['row_kind']='record' if not tracking else 'evidence'
        add_source(rec,p,'','Actual local source member')['evidence_state']='Available'
        tracking.append('Untracked' if p in untracked else 'Tracked' if (ROOT/p).is_file() else 'Directory; inspect preflight inventory')
    if sid=='S01': authority+=' Recorded PDF hash differs from the actual local file; see REG-ISS-010. No requirement change is established.'
    source_lines.append('| '+sid+' | '+'; '.join(link(p,'',Path(p).name) for p in paths)+' | '+authority+' | '+'; '.join(tracking)+' |')
source_lines.extend(['','## Missing evidence','','The four architecture documents explicitly report these gaps:',
 '- Complete official raw-column dictionary and valid missing type/empty-value contracts: DL-01 and DL-16.',
 '- Source-interval closure contract and qualified-publication answer: DL-03.',
 '- Hidden labels, final evaluator profile and reference hardware: DL-16.',
 '- Original decision approver names and approval dates: not supplied. S16/S19 still support the Accepted baseline.',
 '- Actual product execution receipts for AT-01 through AT-30: not supplied.',
 '- Inspectable evidence for the earlier claim of about 70 KPI outputs: REG-ISS-005.',
 '- Source-version/content-equivalence evidence for the mismatched S01 PDF hash: REG-ISS-010.',
 '', 'The original Desktop review path is not needed for a missing-source guess. Its local S16 copy is present. Document 004 records the expected SHA-256. This extraction checks that local hash.',
 '', '## Existing reference records',
 '', 'The ADRs, Decision Log and ATs remain in document 003. The Q review stays in S16. The prior audit traceability CSV, acceptance basis, KPI/rule/workflow/schema contracts and VQ register remain supporting evidence. This Registry is a draft extraction index. It does not establish a second approved decision source.',
 '', 'Several audit rows use former `Project_berif/`, `dataset/` or lowercase `docs/` paths. The matrix cites the existing audit CSV row and retains the original location in source_ref. Actual source members above use current local paths. Existing links are not changed.'])
write('source-inventory.md','\n'.join(source_lines))

# One requirement record per existing requirement ID. Edges retain each CSV row's provenance.
req_path='Docs/architecture/audit-2026-11-09/requirements-traceability.csv'
req_rows=list(csv.DictReader((ROOT/req_path).open(encoding='utf-8-sig',newline='')))
seen_req={}
for q in req_rows:
    id=q['requirement_id']
    if id not in seen_req:
        primary=(D1,id.lower()) if f'<a id="{id.lower()}"></a>' in texts[D1] else (req_path,'')
        rec=row(id,'Requirement',q['requirement'],q['classification'],primary[0],primary[1],id,
                evidence_state='Source documented; product evidence pending')
        seen_req[id]=rec
    rec=seen_req[id]
    ref=f'{id}; {q["source_path"]}; {q["source_location"]}; {q["contract_or_rule"]}'
    add_source(rec,req_path,'',ref)
    for field,typ in [('adr','ADR'),('acceptance_tests','AT'),('architecture_component','Architecture Component')]:
        for target in filter(None,(x.strip() for x in q[field].split(';'))):
            edge(rec,target,typ,req_path,'',ref)
    if q['parent_req']: edge(rec,q['parent_req'],'Requirement',req_path,'',ref,'part_of')

# Record target phases and documented component mappings. Proposed phase plans are not work completed.
for phase in ['P0','P1','P2','P3','P4','P5']:
    row(phase,'Roadmap Phase',phase,'Proposed',D3,'decisions-6','Phase table',evidence_state='Not implemented')
for line in section(D1,'system-4').splitlines():
    if line.startswith('|'):
        for comp in re.findall(r'`([A-Za-z][A-Za-z0-9]*)`',line):
            # Only exact existing DSL identifiers become component records.
            dsl=(ROOT/'architecture/structurizr/workspace.dsl').read_text(encoding='utf-8')
            if re.search(r'\b'+re.escape(comp)+r'\s*=\s*(component|container|softwareSystem)\b',dsl):
                if not any(r['record_id']==comp and r['record_type']=='Architecture Component' and r['row_kind']=='record' for r in rows):
                    row(comp,'Architecture Component',comp,'Target model; not implemented',D1,'system-4',line,evidence_state='Model documented')

# Deduplication ledger: count only explicitly listed duplicate placements removed,
# not every text repetition. Each old placement has one main record or a set of
# distinct main records where the old row bundled different issues.
merges=[]
for q,targets in enumerate([
 ['DL-14'],['REG-ISS-009','DL-10'],['DL-01'],['DL-06','DL-14'],['DL-02'],['DL-03'],['DL-04'],['DL-05'],['DL-06'],['DL-07'],['DL-08'],['DL-09'],['DL-10'],['DL-11'],['DL-12'],['DL-13'],['DL-14']],1):
    merges.append((D4,f'review-q{q:02d}','Q'+f'{q:02d}',targets))
for v,targets in enumerate([['DL-10'],['DL-06'],['DL-06'],['DL-06'],['DL-07'],['DL-02'],['DL-01','DL-06'],['REG-ISS-007'],['DL-03','DL-04','DL-05','DL-10','DL-15'],['DL-16']],1):
    merges.append(('Docs/architecture/visualizations/open-questions.md','',f'VQ{v:02d}',targets))
for id,facets in FACETS.items():
    for label,p,a in facets: merges.append((p,a,label,[id]))
merges.append((D3,'decisions-5','SQL translation risk and reference-oracle maintenance risk',['REG-RSK-004']))
ledger=['# Deduplication ledger','','State: **Draft / Pending Review**.',
 '', 'Counting unit: one named source placement attached to its existing main issue or risk. A bundled placement can reference more than one main record. This count is not the number of all repeated sentences. Source records stay unchanged.',
 '', '| Placement | Source | Main record(s) |','|---|---|---|']
for p,a,label,targets in merges:
    ledger.append('| '+label+' | '+link(p,a)+' | '+', '.join(targets)+' |')
    for target in targets:
        match=next(i['rec'] for i in issues if i['id']==target) if not target.startswith('REG-RSK') else next(r for r in risk_recs if r['record_id']==target)
        add_source(match,p,a,label)
write('deduplication-ledger.md','\n'.join(ledger))

# Mark source evidence references stated as Sxx. Ranges in source text are expanded.
for id,src in adr_sections.items():
    sids=set(re.findall(r'\bS\d{2}\b',src))
    for m in re.finditer(r'\bS(\d{2})[-–]S(\d{2})\b',src):
        sids.update(f'S{x:02d}' for x in range(int(m.group(1)),int(m.group(2))+1))
    for sid in sorted(sids): edge(decision_recs[id],sid,'Source',D3,id.lower(),'Explicit source ID','supported_by')

# Remove exact repeated index rows only. Distinct evidence locations are retained.
dedup_rows={tuple(r[f] for f in FIELDS):r for r in rows}
rows=list(dedup_rows.values())
with (OUT/'traceability-matrix.csv').open('w',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=FIELDS);writer.writeheader();writer.writerows(rows)

type_counts=Counter(t for i in issues for t in i['types'])
summary={'decision_status_statements':dict(counts),'adrs':len(DECISIONS),'dls':len(dl_rows),'ats':len(at_raw),
         'open_issues':len(issues),'team_required':type_counts['T'],'organizer_source_required':type_counts['O'],
         'engineering_evidence_required':type_counts['E'],'risks':len(risk_recs),
         'deduplicated_placements':len(merges),'requirements':len(seen_req),'matrix_rows':len(rows)}
write('extraction-summary.json',json.dumps(summary,indent=2))

readme=f'''# Architecture Registry

State: **Draft / Pending Review**. Task: `ARCH-REG-001`. Date: 2026-11-09. Time zone: `Asia/Tehran`.

This Registry extracts decisions, Open issues, risks and acceptance criteria from the local ARKA architecture baseline. It makes no architecture choice and grants no implementation authority. Document 003 and the existing source records remain in place. Team review must occur before any content transfer or reference migration.

## Files and responsibilities

| File | Responsibility |
|---|---|
| [decisions-registry.md](decisions-registry.md) | All 17 ADRs, with numbered status statements, source extracts, consequences, source roles and closure gates. |
| [open-issues-registry.md](open-issues-registry.md) | All 19 DLs and ten temporary Registry issues. Facets retain semantic differences within each main issue. |
| [risk-register.md](risk-register.md) | {len(risk_recs)} risks; controls, pending evidence and unassessed severity. Risks stay separate from issues. |
| [acceptance-register.md](acceptance-register.md) | All 30 ATs, full source criteria, shared supplements, management-level matrix, rule cases and delivery checks. |
| [traceability-matrix.csv](traceability-matrix.csv) | Generated source/record/relationship index. It is not a second decision authority. |
| [source-inventory.md](source-inventory.md) | S01-S19 members, authority, missing evidence and source limits. |
| [deduplication-ledger.md](deduplication-ledger.md) | Explicit duplicate placements and their main records. |
| [preflight.json](preflight.json) | Initial Git state, 141 prior untracked files and source hashes. Registry files are excluded from this initial inventory. |
| [untracked-source-dependencies.csv](untracked-source-dependencies.csv) | Untracked source dependencies and all 141 preserved untracked files. |
| [extraction-summary.json](extraction-summary.json) | Counts from the generated records. |
| [validation-report.md](validation-report.md) | Extraction checks, limits, remaining conflicts and baseline comparison. |
| [validation-results.json](validation-results.json) | Machine-readable documentation checks and new-file hashes. |
| [baseline-comparison.csv](baseline-comparison.csv) | Initial-source hashes, final hashes and every new Registry file. |
| [capture_preflight.py](capture_preflight.py), [build_registry.py](build_registry.py), [validate_registry.py](validate_registry.py) | Local documentation extraction/check scripts. They execute no product tests and write only in this folder. |

## Status rules

- `Requirement`: an explicit applicable brief or dataset contract rule.
- `Accepted`: a recorded team choice with clear supporting evidence.
- `Proposed`: an unapproved option or engineering mechanism.
- `Open`: an unresolved choice, conflict or evidence gap.

`Observation` describes source/audit evidence. It is not a decision approval status. `Evidence Pending` means the required evidence is absent. It does not turn a Requirement or Accepted boundary into Open. A source question or ADR can contain several independent status statements. Repeated text and a target model alone do not prove approval.

The five Accepted boundaries remain fixed: one bounded Agent; PostgreSQL-only product execution; independent valid-report publication; deterministic calculation/Signal/authorization/final validation; human-controlled organizational decisions. S16, S19 and document 003 section 1 support these boundaries. Original approver names and approval dates are absent. Unapproved technical details stay separate.

## Closure

An issue needs the applicable source answer or recorded team decision, the named policy/contract version, and inspectable evidence for its linked acceptance gate. Organizer/source questions need an answer from the relevant authority. Engineering gates need actual product receipts. A document check cannot close an issue or pass a product AT. No record is closed by this extraction. No test is Passed.

Route classes are `Team Decision Required`, `Organizer / Source Clarification Required` and `Engineering Evidence Required`. Classes can overlap. Source role names are preserved; no person is appointed. An `Open` statement count differs from an Open issue count because several statements can belong to one issue.

## Source and quotation rules

The extraction baseline is `0a42950d1ce9734433d961540af9ab4be21573b2`. Read {link(D1,'','001')}, {link(D2,'','002')}, {link(D3,'','003')} and {link(D4,'','004')}, plus the [S01-S19 inventory](source-inventory.md).

English text provides the Registry index. Exact source extracts retain the supplied Persian text, all numbers, conditions and exceptions. Text inside source extract blocks is quoted evidence. Its old link strings are inert. The active Source Evidence link points to the real original file and existing anchor. Do not interpret text inside a quoted extract as a new Registry instruction or status change.

The existing audit requirement matrix is reused as evidence. Its former source paths remain in `source_ref`; current paths are listed in the source inventory. Audit observations are not rerun calculations. The brief PDF and its conversion are present; no fresh PDF visual audit is claimed.

## CSV contract

Encoding is UTF-8. CSV quoting follows the standard library CSV writer. Each row has one `row_kind`: `record`, `evidence` or `relationship`. A `record` row defines the main identity. Each evidence row adds one source location. Each relationship row has exactly one target. This permits many-to-many relations without positional lists or cross-products. Source-member records use one main Sxx identity and separate evidence rows.

Required columns are retained: `record_id,record_type,title,status,source_file,source_anchor,source_ref,related_adr,related_dl,related_at,related_risk,roadmap_phase,evidence_state`. Extra columns identify row kind, target identity/type, relationship type/status, component, local Registry location and source tracking state. `source_file` is relative to the repository root. `source_anchor` is an existing explicit Markdown anchor, or empty for CSV/DSL/files. `source_ref` identifies a source row, field, page or retained legacy path. `registry_file` is relative to this folder.

`relationship_status=Documented` means that the source explicitly supplies the association. It does not approve the proposed design. `Proposed Relationship` marks an extraction review aid with no explicit source mapping. In particular, risk-to-ADR/DL/AT links are proposed unless a source names them. Empty roadmap cells mean no proven phase assignment. The phase plan stays Proposed.

## Validity limits

This draft has {counts['Accepted']} Accepted, {counts['Proposed']} Proposed, {counts['Open']} Open and {counts['Requirement']} Requirement statements in the numbered ADR statement tables. Counts include only those explicit rows, not repeated quotations. The full source extracts retain finer conditions. There are {len(issues)} Open main issues, including all 19 DLs; route totals overlap. All 30 ATs remain Planned / Not Executed. Severity is Not Assessed for every risk.

All original sources are read-only for this task. All 141 initial untracked files must remain unchanged. Only new files in this folder are permitted. No implementation, source rewrite, rename, commit or push is part of this task.
'''
write('README.md',readme)
print(json.dumps(summary,indent=2))
