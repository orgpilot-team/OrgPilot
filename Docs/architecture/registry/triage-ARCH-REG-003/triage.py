"""Classify the existing inferred links. Write new triage documents only."""
from pathlib import Path
from collections import Counter, defaultdict
import csv, hashlib, io, json, re, subprocess, sys
from urllib.parse import unquote

sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).resolve().parent;REG=OUT.parent;ROOT=REG.parents[2]
PREFIX='Docs/architecture/registry/'
pre=json.loads((OUT/'before-manifest.json').read_text(encoding='utf-8'))
def read(p):return (ROOT/p).read_text(encoding='utf-8-sig')
def csvread(p):return list(csv.DictReader(io.StringIO(read(p))))
def digest(s):return hashlib.sha256(s.encode('utf-8')).hexdigest()
def write_csv(path,rs,fields=None):
    assert path.relative_to(ROOT).as_posix() not in pre['sha256'],'Cannot replace an existing task-start file'
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rs[0]));w.writeheader();w.writerows(rs)
def write(path,s):
    assert path.relative_to(ROOT).as_posix() not in pre['sha256'],'Cannot replace an existing task-start file'
    path.write_text(s.rstrip()+'\n',encoding='utf-8')
D1='Docs/architecture/001-system-blueprint.md';D2='Docs/architecture/002-data-architecture.md';D3='Docs/architecture/003-decisions-and-roadmap.md'
MATRIX=PREFIX+'traceability-matrix.csv'
raw=list(csv.DictReader(io.StringIO(read(MATRIX))));records={r['record_id']:r for r in raw if r['row_kind']=='record'}
inferred=[(n,r) for n,r in enumerate(raw,2) if r['row_kind']=='relationship' and r['relationship_status']=='Proposed Relationship']
assert len(inferred)==2470
req={r['requirement_id']:r for r in csvread('Docs/architecture/audit-2026-11-09/requirements-traceability.csv')}
kpis={r['kpi_id']:r for r in csvread('DataSet/arka_dataset/config/kpi_dictionary.csv')}
contracts=read(D2);value_sources={}
for line in contracts.splitlines():
    m=re.match(r'\| `(K_[^`]+)`',line)
    if m:value_sources[m[1]]=set(line.strip('|').split('|')[-1].strip().strip('`').split(', '))
assert set(value_sources)==set(kpis) and len(kpis)==55
sql=read('DataSet/arka_dataset/config/reference_views.sql')
views={m[1]:m[2] for m in re.finditer(r'CREATE VIEW\s+(\w+)\s+AS(.*?);',sql,re.I|re.S)}
known={'orders','order_events','tickets','ticket_events','csat','crm_leads','crm_lead_events','tasks','task_events','mkt_daily','web_sessions','staff_availability','cal','monthly_targets'}|set(views)
def sql_relations(s,seen=()):
    direct={x.lower() for x in re.findall(r'\b(?:FROM|JOIN)\s+(\w+)',s,re.I)}&known
    expanded=set(direct)
    for name in direct:
        if name in views and name not in seen:expanded|=sql_relations(views[name],seen+(name,))
    return expanded
historical={}
for line in read('Docs/review/kpi-val-001-report.md').splitlines():
    cells=[s.strip() for s in line.strip('|').split('|')]
    if len(cells)==6 and cells[0] in kpis and cells[-1].isdigit():historical[cells[0]]=int(cells[-1])
assert len(historical)==55 and sum(x>0 for x in historical.values())==8
kpi_evidence=[];kpi_case={}
for id,k in kpis.items():
    rel=sql_relations(k['sql'])
    case='value-orders' if value_sources[id]&{'O','OE'} else 'declared-execution-only' if rel&{'orders','order_events'} else 'no-orders-relation'
    kpi_case[id]=case
    kpi_evidence.append(dict(kpi_id=id,owner_manager_id=k['owner_manager_id'],entity_id=k['entity_id'],rule=k['rule'],
        selected_value_sources=json.dumps(sorted(value_sources[id])),declared_query_view_relations=json.dumps(sorted(rel)),
        orders_policy_case=case,historical_full_different_keys=historical[id],canonical_sql_sha256=digest(k['sql']),
        source_file='DataSet/arka_dataset/config/kpi_dictionary.csv',source_ref=id,
        value_source_evidence=D2+'#data-6',historical_evidence='Docs/review/kpi-val-001-report.md / table of all 55 definitions',
        limit='Textual relation expansion and documented value sources; no SQL execution, query plan, minimal invalidation proof or new equivalence result.'))
write_csv(OUT/'kpi-policy-evidence.csv',kpi_evidence)

inputs=json.loads(read('DataSet/arka_dataset/manager_inputs/scripted_inputs.json'))
input_by_id={r['input_id']:r for r in inputs};assert len(input_by_id)==23
expected_nonquestion={'IN01':{'AT-07','AT-29'},'IN02':{'AT-14','AT-29'},'IN03':{'AT-14','AT-29'},
 'IN04':{'AT-13','AT-22','AT-29'},'IN05':{'AT-07','AT-15','AT-29'},'IN06':{'AT-07','AT-29'},'IN07':{'AT-03','AT-22','AT-29'}}
source_nonquestion={}
for line in read(D3).splitlines():
    m=re.match(r'\| (IN\d{2})[،,]',line)
    if m:source_nonquestion[m[1]]=set(re.findall(r'AT-\d{2}',line))
assert source_nonquestion==expected_nonquestion
at_content={}
for line in read(D3).splitlines():
    m=re.match(r'\| <a id="at-\d{2}"></a>(AT-\d{2}) \|',line)
    if m:at_content[m[1]]=line
assert len(at_content)==30
stages=csvread('DataSet/arka_dataset/config/workflow_definitions.csv');assert len(stages)==12
access=csvread('DataSet/arka_dataset/org/access_matrix.csv');assert len(access)==11

T='Team';E='Engineering';S='Organizer / Source'
def evidence(file,anchor='',ref=''):return dict(file=file,anchor=anchor,ref=ref)
COMMON=[evidence(PREFIX+'semantic-audit-report.md'),evidence(PREFIX+'audit-ARCH-REG-002/relationship-review.csv')]

def classify(r):
    """Return a single primary group. Cross-cutting exposure stays in member flags."""
    sid=r['record_id'];target=r['target_id'];typ=r['target_type'];rt=r['record_type']
    # key, family, semantics, disposition, priority, reason, impact, action, route, evidence
    def c(key,family,sem,disp,priority,reason,impact,action,route,ev):
        return dict(key=key,family=family,semantic_class=sem,disposition=disp,priority=priority,
                    reason=reason,impact=impact,action=action,route=route,evidence=ev)
    if rt=='AT' and r['relationship_type']=='referenced_by':
        return c('NAV-AT-ISSUE','Test/issue inverse','Navigation reference','Navigation / Pending Confirmation','P2',
                 'This is an inverse lookup. It does not add a test condition or make the issue a prerequisite.',
                 'A reader could mistake navigation for an execution dependency.','Retain as a navigation candidate; verify the forward link and keep its evidence class.',T+'; '+E,
                 [evidence(r['source_file'],r['source_anchor'],r['source_ref'])])
    if rt=='Decision Boundary':
        sem='Accepted-boundary trace candidate' if typ in ['ADR','AT'] else 'Proposed logical responsibility'
        return c('BOUNDARY-'+sid+'-'+typ,'Five Accepted boundaries',sem,'Defensible / Pending Confirmation','P0',
                 'The boundary is Accepted. Its imported ADR/test/component assignment is still inferred; source approval does not prove the implementation or the exact test coverage.',
                 'Do not reopen a boundary, add autonomous Agents, add a product engine, weaken deterministic checks or imply automatic human action.',
                 'Check the named boundary against its exact ADR/test or DSL role. Approve the trace link separately from the boundary; require a criterion or role paragraph.',T+'; '+E,
                 [evidence('Docs/architecture/audit-2026-11-09/request.txt',ref='section 1; five Accepted boundaries'),evidence(D3,'decisions-1')])
    if rt=='Risk':
        risknum=int(sid.rsplit('-',1)[1])
        if typ=='AT':
            weak=(risknum,target) in {(3,'AT-23'),(5,'AT-13'),(19,'AT-10')}
            # These maps can weaken a fixed value/security/publication/rule or
            # whole-day acceptance boundary. Generalization/restore-only maps
            # remain scope/coverage review rather than a new boundary choice.
            priority='P1' if risknum in {7,18} else 'P0'
            reasons={(3,'AT-23'):'Dated prior-value display does not prove source closure or missing-source detection.',
                     (5,'AT-13'):'Prompt-injection rejection does not by itself prove row/column/cache/log isolation.',
                     (19,'AT-10'):'Numerical lineage and independent-cause checks do not specify a small-group privacy or text-redaction oracle.'}
            return c('RISK-TEST-'+('PARTIAL' if weak else 'CONTROL')+'-'+priority,'Risk control evidence','Risk-control test candidate',
                     'Questionable' if weak else 'Defensible / Pending Confirmation',priority,
                     reasons.get((risknum,target),'The test topic is relevant, but the risk-control claim needs a named failure case, oracle and evidence receipt. A related test is not a proved control.'),
                     'A passing test could be reported as full mitigation while some control paths remain untested.',
                     'Create a risk-control-to-criterion checklist for the existing AT. Record uncovered paths; keep control unexecuted and severity Not Assessed.',T+'; '+E,
                     [evidence(PREFIX+'risk-register.md',sid.lower()),evidence(D3,target.lower())])
        return c('RISK-TOPIC-'+typ,'Risk/issue context','Topic similarity / control policy reference','Defensible / Pending Confirmation','P1',
                 'The ADR or issue addresses a related cause/control. It is not a software execution predecessor or a scored reduction.',
                 'Policy discussion could be mistaken for control implementation.','Review the exact control facet; retain only as context unless a substantive relation is recorded.',T+'; '+E,
                 [evidence(PREFIX+'risk-register.md',sid.lower())])
    if rt in ['Registry Issue','DL']:
        documentary=sid in ['REG-ISS-005','REG-ISS-007','REG-ISS-010']
        priority='P2' if documentary and typ=='DL' else 'P1' if documentary else 'P0'
        return c('ISSUE-'+sid+'-'+typ,'Open issue contract','Issue/test or ADR topic candidate','Defensible / Pending Confirmation' if typ=='AT' else 'Questionable',priority,
                 'This temporary or additional issue link was added by extraction. The source documents describe the gap, but do not necessarily assign this exact Registry ID to the target.',
                 'A record gap or absent evidence could become an invented architecture prerequisite or a new test requirement.',
                 'Confirm the same unresolved facet in source and target. Keep evidence-only work distinct from design selection. Do not close the issue.',T+'; '+E,
                 [evidence(r['source_file'],r['source_anchor'],r['source_ref']),evidence(PREFIX+'open-issues-registry.md',sid.lower())])
    q=req[sid];p=q['source_path']
    if sid.startswith('REQ-KPI-'):
        kid=sid[len('REQ-KPI-'):];case=kpi_case[kid];k=kpis[kid]
        ev=[evidence('DataSet/arka_dataset/config/kpi_dictionary.csv',ref=kid),evidence(D2,'data-6'),
            evidence('DataSet/arka_dataset/config/reference_views.sql'),evidence(PREFIX+'triage-ARCH-REG-003/kpi-policy-evidence.csv',ref=kid)]
        if target=='ADR-02':
            tag='historically-sensitive' if historical[kid]>0 else 'value-path-not-proven-sensitive' if case=='value-orders' else case
            questionable=historical[kid]==0
            reason={'historically-sensitive':'The earlier audit reports changed RAW/DEDUP results for this definition. The accepted input policy and a current product result are still absent.',
                    'value-path-not-proven-sensitive':'The documented selected value uses orders, but value-source membership does not prove RAW/DEDUP sensitivity. The historical full-data output did not differ.',
                    'declared-execution-only':'K_ENT_CONTRACT_MTD selects B2B from revenue_daily. The view also declares an orders branch. This is not evidence that orders change the selected B2B value or that the physical plan reads the branch.',
                    'no-orders-relation':'The selected-value catalog and inspected canonical query/view paths contain no orders relation. The all-KPI-to-orders template has no definition-specific policy evidence.'}[tag]
            return c('KPI-ORDERS-'+tag,'Canonical KPI orders policy','Value-policy applicability' if case=='value-orders' else 'Declared query/view relation only' if case=='declared-execution-only' else 'Mere topic similarity',
                     'Questionable' if questionable else 'Defensible / Pending Confirmation','P0',reason,
                     'A generic link could authorize needless DEDUP, alter a canonical result, or falsely block an independent KPI.',
                     'Review this exact SQL/value path and the historical evidence. Record value impact separately from declared/physical execution relations. Do not choose RAW or DEDUP.',
                     T+'; '+E+('; '+S+' via DL-02' if case=='value-orders' else ''),ev+[evidence('Docs/review/kpi-val-001-report.md')])
        if typ=='ADR':
            desc={'ADR-01':('Canonical-result contract','P0','All 55 need preserved definitions and equivalence evidence; the engine choice is fixed.'),
                  'ADR-03':('Recalculation policy','P1','A KPI can need invalidation; the link does not prove its minimum affected key set or endorse selective rebuild.'),
                  'ADR-04':('Publication eligibility policy','P0','Missing-source eligibility must use affected inputs; the link does not justify withholding all KPIs or claiming closure.'),
                  'ADR-06':('Output authorization policy','P0','KPI ownership and input access are distinct. Calculation permission is not a manager grant.'),
                  'ADR-07':('Rule eligibility policy','P0','The rule metadata governs this definition. info requires no-alert gating; other rules need their actual parameters.')}[target]
            rule_tag='-info' if target=='ADR-07' and k['rule']=='info' else ''
            return c('KPI-'+target+rule_tag,'Canonical KPI contract',desc[0],'Defensible / Pending Confirmation',desc[1],desc[2],
                     'Do not change canonical SQL, grant raw access or infer execution order from an ADR reference.',
                     'Review the policy facet and exact field/criterion for this definition; retain the inferred class pending team confirmation.',T+'; '+E,ev+[evidence(D3,target.lower())])
        if typ=='AT':
            nofixture=target=='AT-05' and not value_sources[kid]&{'O','OE','T','TE','L','LE'}
            return c('KPI-'+target+('-no-named-fixture' if nofixture else '-candidate'), 'Canonical KPI test coverage',
                     'Test criterion candidate','Questionable' if nofixture else 'Defensible / Pending Confirmation','P0',
                     'AT-05 names orders duplicates, support aliases and the CRM correction. This value-source set has no matching named fixture; a whole-test label is not criterion-specific coverage.' if nofixture else
                     'The test topic matches the KPI contract, but coverage needs the exact SQL output, scope, rule gate or fixture. Do not treat one test label as proof for every output series.',
                     'Coverage could be overstated or new fixtures could silently become acceptance requirements.',
                     'Attach the exact existing criterion and expected result. Record a coverage gap where no criterion applies; add no acceptance requirement during triage.',T+'; '+E,ev+[evidence(D3,target.lower())])
        return c('KPI-COMPONENT','Canonical KPI responsibility','Proposed logical responsibility','Defensible / Pending Confirmation','P1',
                 'The kpi module matches calculation responsibility, not a deployment, execution dependency or implementation proof.',
                 'The Registry could be used as an implementation dependency graph.','Confirm the existing DSL responsibility and keep the assignment separate from SQL dependencies.',T+'; '+E,ev+[evidence(D1,'system-4')])
    if p=='dataset/config/workflow_definitions.csv':
        weak=target=='ADR-07'
        return c('WORKFLOW-'+target,'Workflow stage scope','Stage-to-rule topic similarity' if weak else 'Stage contract / logical responsibility',
                 'Questionable' if weak else 'Defensible / Pending Confirmation','P0' if typ!='Architecture Component' else 'P1',
                 'A stage SLA/median is not automatically a canonical KPI threshold or a new escalation Signal. Stage owner routing remains Open.' if weak else
                 'All 12 supplied stages need their own from/to, SLA type, median target and unknown/open case checks. A workflows component reference assigns no stage owner.',
                 'WF1.4 deadline, WF1.5 missing SLA or canonical WF2/WF3 formulas could be replaced by a uniform stage template.',
                 'Review each stage type against AT-12/25. Preserve M01 end-to-end ownership; do not infer stage teams or a new Signal from the component mapping.',T+'; '+E,
                 [evidence('DataSet/arka_dataset/config/workflow_definitions.csv',ref=q['source_location']),evidence(D1,'system-7'),evidence(D3,'adr-15')])
    if p=='dataset/manager_inputs/scripted_inputs.json':
        iid=sid[len('REQ-INPUT-'):];item=input_by_id[iid];itype=item['type']
        ev=[evidence('DataSet/arka_dataset/manager_inputs/scripted_inputs.json',ref=iid+' / '+q['source_location']),evidence(D3,'manager-question-map'),evidence(D1,'system-4')]
        if typ=='AT':
            mismatch=iid in expected_nonquestion and target not in expected_nonquestion[iid]
            priority='P0' if mismatch or target in ['AT-03','AT-06','AT-13','AT-14','AT-30'] else 'P1'
            return c('INPUT-TEST-'+itype+'-'+('unnamed' if mismatch else 'candidate')+'-'+priority,'Manager-input test scope','Fixture-specific test candidate',
                     'Questionable' if mismatch else 'Defensible / Pending Confirmation',priority,
                     'This AT is absent from the source table for this non-question event. The generic five-test template is not fixture-specific evidence.' if mismatch else
                     'The source input type and test topic align, but question/refusal, receipt clock and write authority require separate oracles. A question is not a permission grant.',
                     'A priority or organization input could be treated as an action, upload or QA event; security and acceptance scope could change.',
                     'Compare the exact input record with the named source criteria. Recommend retaining, narrowing or later correcting this link; make no matrix change now.',T+'; '+E,ev+[evidence(D3,target.lower())])
        if typ=='Architecture Component':
            direct=(target=='requests' or target=='publication' and itype=='question' or target=='managerConfig' and itype in ['priority','org_change','threshold_change'] or
                    target=='documents' and (itype=='upload' or iid=='Q09') or target=='decisions' and (itype=='decision' or iid=='Q15'))
            p0=target in ['managerConfig','decisions']
            return c('INPUT-COMP-'+target+'-'+('role' if direct else 'template'),'Manager-input component roles','Proposed logical responsibility' if direct else 'Context/topic similarity',
                     'Defensible / Pending Confirmation' if direct else 'Questionable','P0' if p0 else 'P1',
                     'The module has a relevant receipt/read/write role for this event. Read context, write authority and eventual publication are separate.' if direct else
                     'The same five modules were assigned to every input. This event has no demonstrated direct role for this target. Context read does not authorize mutation or human action.',
                     'An inferred component association could grant configuration writes, create a draft without a decision, or require unsupported processing.',
                     'Identify read, authorized write, receipt and eventual-display roles separately in the existing model. Do not infer execution dependencies or add services.',T+'; '+E,ev)
        return c('INPUT-ADR-'+itype,'Manager-input policy','Policy-context candidate','Defensible / Pending Confirmation','P0',
                 'Clock, scope and output contracts can apply, but the shared template does not establish every input-specific obligation.',
                 'Input timing, confidentiality or human-action boundaries could be weakened by an overly broad interpretation.',
                 'Check this input type and actual ADR topic; keep clock, read permission and write/action authority separate.',T+'; '+E,ev+[evidence(D3,target.lower())])
    if p.startswith('dataset/org/'):
        family='Access grants' if p.endswith('access_matrix.csv') else 'Dated organization scope'
        return c('ORG-'+family+'-'+typ,family,'Authorization/scope contract candidate','Defensible / Pending Confirmation','P0',
                 'A supplied entity hierarchy or grant row is not a raw-column permission, staff movement history or appointment of a stage owner. Static and runtime activation dates still conflict.',
                 'A structural association could extend individual data to senior managers, invent historical scope or select M11 morning 75/76.',
                 'Check actual manager/team/effective-day fields; verify direct-supervisor workload purpose and aggregate leave. Keep row/column predicates and M11 precedence Open.',T+'; '+E+'; '+S+' only for the DL-10 timing conflict or conditional DL-06 source meaning',
                 [evidence('DataSet/arka_dataset/'+p[len('dataset/'):],ref=q['source_location']),evidence('DataSet/arka_dataset/org/access_matrix.csv'),evidence(D3,'adr-06'),evidence(D3,'adr-08')])
    if p=='dataset/config/reference_views.sql':
        view=sid[len('REQ-VIEW-'):];no_orders=not sql_relations(views[view])&{'orders','order_events'}
        weak=target=='ADR-02' and no_orders
        return c('VIEW-'+typ+('-orders-unrelated' if weak else '-contract'),'Reference view contract','Topic similarity' if weak else 'Canonical view contract candidate',
                 'Questionable' if weak else 'Defensible / Pending Confirmation','P0',
                 'This canonical view has no orders relation in the inspected definition, yet the generic template assigns the orders input policy.' if weak else
                 'The reference view defines selected times, joins and correction behavior. A policy/test reference does not license a lifecycle rewrite or an arbitrary tie rule.',
                 'A view-level template could alter row sets, MIN/MAX, integer/time behavior or correction precedence.',
                 'Check the complete original view and the exact test/control facet. Keep declared relation names separate from physical reads and minimal recomputation.',T+'; '+E,
                 [evidence('DataSet/arka_dataset/config/reference_views.sql',ref=view),evidence(D2,'data-6')])
    if p.startswith('dataset/output_contract/'):
        sensitive=any(x in q['source_location'] for x in ['/status','/dim','/query_id','/confidence','/answer_status'])
        return c('WIRE-'+typ+('-sensitive' if sensitive else '-general'),'Output schema contracts','Schema criterion / projection candidate','Defensible / Pending Confirmation','P0',
                 'A property type/enum applies when its containing object exists. Optional presence is not made mandatory by this link; stronger brief traceability remains a separate semantic check.',
                 'The link could silently require an optional field, change suppressed/ongoing, collapse NULL/no-dimension or treat schema success as numerical/access success.',
                 'Review the exact JSON pointer and the applicable AT criterion. Record internal validation separately from source schema requirements; preserve DL-11/17/18.',T+'; '+E+'; '+S+' only for actual unresolved wire contracts',
                 [evidence('DataSet/arka_dataset/'+p[len('dataset/'):],ref=q['source_location']),evidence(D1,'system-9'),evidence(D3,'at-30')])
    if p=='dataset/config/escalation_rules.csv':
        return c('RULE-'+typ,'R1-R8 contracts','Rule / test / responsibility candidate','Defensible / Pending Confirmation','P0',
                 'The source rule is fixed; the implementation or whole test label is still inferred. R2 >N and >=20%, R4 <10%, R5 >N, R7 no alert and R8 day 8 must stay distinct.',
                 'A generic reference could select an unresolved equality, reset, baseline or owner rule.',
                 'Bind the exact existing R1-R8 case and all three check points. No invented warn, epsilon, owner or reset policy.',T+'; '+E+'; '+S+' via DL-09 for score-sensitive ambiguity',
                 [evidence('DataSet/arka_dataset/config/escalation_rules.csv',ref=q['source_location']),evidence(D1,'system-7'),evidence(D3,'at-24')])
    if p.startswith('dataset/calendar/'):
        event=p.endswith('events_calendar.csv')
        weak=event and target in ['ADR-01','ADR-07','AT-02','AT-24','kpi','signals']
        return c('CALENDAR-'+('event' if event else 'business-clock')+'-'+typ+('-weak' if weak else '-context' if event else ''),'Calendar visibility / clock','Context visibility' if event else 'Canonical clock contract',
                 'Questionable' if weak else 'Defensible / Pending Confirmation','P0' if not event or weak else 'P1',
                 'Planned contextual events are not canonical KPI SQL inputs and have no supplied known-at. A context event cannot become an observed cause or a calculation dependency.' if event else
                 'Supplied dates, Jalali month/day, weekdays and mdays govern reference calculations and gates; Gregorian substitutions are not allowed.',
                 'Future events, a calendar rewrite or a topic-only link could change historical results or Signal eligibility.',
                 'Confirm whether the link denotes calculation clock or authorized context. Prove any claimed formula dependency from SQL; otherwise retain only context.',T+'; '+E,
                 [evidence('DataSet/arka_dataset/'+p[len('dataset/'):],ref=q['source_location']),evidence(D2,'data-3'),evidence(D2,'data-9')])
    if p=='dataset/config/monthly_targets.csv':
        return c('TARGETS-'+typ,'Canonical monthly targets','Value/configuration candidate','Defensible / Pending Confirmation','P0',
                 'The ORG target and supplied calendar prorating are canonical; a config association grants no write authority or target rewrite.',
                 'A template could expose ORG targets outside scope or change attain values/activation time.',
                 'Check the supplied target row and canonical expression. Separate view access from target changes and keep activation authority Open.',T+'; '+E,
                 [evidence('DataSet/arka_dataset/config/monthly_targets.csv',ref=q['source_location']),evidence(D3,'adr-01'),evidence(D3,'decision-log',ref='DL-19')])
    if p.startswith('dataset/drops/'):
        return c('RAW-SCHEMA-'+typ,'Observed source headers','Intake schema / logical responsibility candidate','Defensible / Pending Confirmation','P1',
                 'An observed header supports an adapter fixture, not an official type dictionary, unique key, foreign key or source-closure contract.',
                 'Observed structure could be enforced as a stronger source contract or hidden-data constraint.',
                 'Check the actual header and known alias. Keep raw occurrences; do not invent a key, type guarantee or fixed incident day.',T+'; '+E+'; '+S+' only for a missing official contract in DL-16',
                 [evidence('DataSet/arka_dataset/'+p[len('dataset/'):],ref=q['source_location']),evidence(D2,'data-4')])
    # Narrative requirements use individually named topics, not one universal mapping.
    family='Dataset timing/output contract' if p=='dataset/README_FA.md' else 'Narrative '+('-'.join(sid.split('-')[:2]) if not re.fullmatch(r'REQ-\d{2}',sid) else 'umbrella')
    security=sid.startswith(('REQ-SEC','REQ-ACT','REQ-NUM','REQ-CONF')) or target in ['ADR-01','ADR-02','ADR-06','ADR-07','ADR-13','ADR-17','AT-02','AT-03','AT-06','AT-13','AT-14','AT-20','AT-24','AT-27','AT-30','access','queryGateway']
    docs=sid.startswith(('REQ-DEL',)) and typ=='Architecture Component'
    priority='P2' if docs else 'P0' if security else 'P1'
    weak=typ=='ADR' or docs
    return c('TEXT-'+family+'-'+typ+'-'+priority,family,'Topic similarity' if weak else 'Criterion or logical responsibility candidate',
             'Questionable' if weak else 'Defensible / Pending Confirmation',priority,
             'A prior audit topic template supplies this assignment. Exact requirement wording does not by itself prove that this ADR/component addresses it.' if weak else
             'The requirement and target have a relevant topic, but the exact criterion, role and exceptions must be attached. No execution edge follows from the reference.',
             'A broad template could expand scope, invent a prerequisite or overstate acceptance coverage.',
             'Review requirement text against the target paragraph or AT criterion. Label responsibility, navigation and coverage separately; recommend later changes without modifying the matrix.',T+'; '+E,
             [evidence('Docs/'+p[len('Project_berif/'):] if p.startswith('Project_berif/') else 'DataSet/arka_dataset/'+p[len('dataset/'):] if p.startswith('dataset/') else p,ref=q['source_location']),
              evidence(r['source_file'],r['source_anchor'],r['source_ref']),evidence(D3,target.lower() if typ in ['ADR','AT'] else 'decisions-7')])

members=[];groups=defaultdict(list);groupdata={}
for number,r in inferred:
    c=classify(r)
    batch_family='Narrative source contracts' if c['family'].startswith('Narrative ') else c['family']
    review_key=c['key'] if c['disposition']=='Questionable' else '|'.join(['BATCH',batch_family,c['semantic_class'],c['priority'],r['target_type'],c['route']])
    gid='TRQ-'+digest(review_key)[:10].upper()
    eid='TRE-'+digest(json.dumps(r,sort_keys=True,ensure_ascii=False))[:14].upper()
    assert r['record_id'] in records and r['target_id'] in records
    m=dict(relationship_id=eid,group_id=gid,classification_key=c['key'],source_pattern_family=c['family'],matrix_row=number,source_id=r['record_id'],source_type=r['record_type'],target_id=r['target_id'],target_type=r['target_type'],
           relationship_type=r['relationship_type'],current_evidence_class=r['relationship_status'],semantic_class=c['semantic_class'],disposition=c['disposition'],priority=c['priority'],
           reason_for_uncertainty=c['reason'],potential_impact=c['impact'],recommended_review_action=c['action'],route=c['route'],status='Pending Review',
           source_file=r['source_file'],source_anchor=r['source_anchor'],source_ref=r['source_ref'],
           relevant_source_evidence=json.dumps(c['evidence'],ensure_ascii=False),
           execution_dependency='Not established by this reference',classification_method='Deterministic full-set source-family/target-role rules; targeted direct source checks; no exhaustive human verification')
    members.append(m);groups[gid].append(m);groupdata[gid]=dict(c,review_key=review_key)
assert len({m['relationship_id'] for m in members})==2470
write_csv(OUT/'relationship-classification.csv',members)

queue=[]
for gid,ms in groups.items():
    c=groupdata[gid]
    assert len({(m['priority'],m['disposition'],m['semantic_class']) for m in ms})==1, c['key']
    # One group can hold several exact pairs. The membership file is authoritative
    # for group membership; source/target sets below are not a Cartesian product.
    ev={json.dumps(e,sort_keys=True,ensure_ascii=False):e for m in ms for e in json.loads(m['relevant_source_evidence'])}
    fine_keys=sorted({m['classification_key'] for m in ms})
    batched=len(fine_keys)>1
    queue.append(dict(review_id=gid,group_key=c['review_key'],classification_keys=json.dumps(fine_keys),source_pattern_families=json.dumps(sorted({m['source_pattern_family'] for m in ms})),scope='Existing inferred relationships',relationship_count=len(ms),candidate_pair_count=0,
        source_ids=json.dumps(sorted({m['source_id'] for m in ms})),target_ids=json.dumps(sorted({m['target_id'] for m in ms})),
        relationship_type=json.dumps(sorted({m['relationship_type'] for m in ms})),current_evidence_class='Proposed / Inferred Relationship',
        semantic_class=c['semantic_class'],disposition=c['disposition'],reason_for_uncertainty=(
            'This review batch combines source-specific groups with the same semantic role and priority. Read each member reason and exact target criterion/role. Topic fit does not approve the link.' if batched else
            'These test links cover only part of their stated risk control. Read each member reason; no whole-risk coverage or mitigation result follows.' if c['key'].startswith('RISK-TEST-PARTIAL') else c['reason']),
        relevant_source_evidence=json.dumps(list(ev.values()),ensure_ascii=False),potential_architectural_impact=c['impact'],priority=c['priority'],
        priority_rationale={'P0':'A wrong interpretation could alter an Accepted boundary, source rule, canonical result, security grant or acceptance condition.',
                            'P1':'A wrong interpretation could materially alter implementation responsibility, scope or test coverage.',
                            'P2':'Navigation or maintenance only; do not turn it into an execution prerequisite.'}[c['priority']],
        recommended_review_action='Review each member action and source-specific criterion or role. Confirm links individually or record a bounded group rationale; do not promote this batch automatically.' if batched else c['action'],route=c['route'],current_status='Pending Review',membership_file=PREFIX+'triage-ARCH-REG-003/relationship-classification.csv',
        member_selection='Exact group_id match; source_ids and target_ids are descriptive sets, not a cross-product'))

# Missing links are review candidates only. They are not added to the matrix and
# are excluded from the 2,470 existing-edge count.
missing=[]
for iid,expected in expected_nonquestion.items():
    sid='REQ-INPUT-'+iid;present={r['target_id'] for _,r in inferred if r['record_id']==sid and r['target_type']=='AT'}
    for target in sorted(expected-present):missing.append(dict(source_id=sid,target_id=target,source_file=D3,source_anchor='manager-question-map',reason='The per-input source table names this AT, but this requirement has no such active inferred AT link.'))
assert {(r['source_id'],r['target_id']) for r in missing}=={('REQ-INPUT-IN05','AT-15'),('REQ-INPUT-IN07','AT-03')}
write_csv(OUT/'missing-link-candidates.csv',missing)
queue.append(dict(review_id='TRQ-MISSING-INPUT',group_key='MISSING-NONQUESTION-TESTS',scope='Missing relationship candidates; no matrix edit',relationship_count=0,candidate_pair_count=len(missing),
    classification_keys='["MISSING-NONQUESTION-TESTS"]',source_pattern_families='["Manager-input test scope"]',
    source_ids=json.dumps(sorted({r['source_id'] for r in missing})),target_ids=json.dumps(sorted({r['target_id'] for r in missing})),relationship_type='Proposed references candidate',
    current_evidence_class='Missing Relationship Candidate',semantic_class='Fixture-specific test coverage gap',disposition='Questionable',
    reason_for_uncertainty='IN05 names AT-15 and IN07 names AT-03 in the source table. The generic requirement-to-test template omits them. Existing DL/AT references elsewhere do not supply these exact pairs.',
    relevant_source_evidence=json.dumps([evidence(D3,'manager-question-map')]),potential_architectural_impact='M11 daily coverage or attachment cutoff could be omitted from the fixture coverage claim.',
    priority='P0',priority_rationale='Daily active-manager acceptance and future-data exclusion are at risk.',recommended_review_action='Review the two exact missing pairs and record a later correction decision. Do not add or promote an edge in triage.',
    route=T+'; '+E,current_status='Pending Review',membership_file=PREFIX+'triage-ARCH-REG-003/missing-link-candidates.csv',member_selection='Two exact rows; not part of the existing-edge membership count'))
queue.sort(key=lambda r:(r['priority'],r['disposition']!='Questionable',r['group_key']))
write_csv(REG/'traceability-review-queue.csv',queue)

# A bounded, criterion-specific review of every proposed risk-to-test pair.
# These descriptions explain relevance and limits. They are not control results.
RISK_TEST_FACETS={
 (1,'AT-03'):('Cutoff and future-storage negative cases','Snapshot immutability/hash and every source path still need actual receipts.'),
 (2,'AT-02'):('Compare all canonical outputs under the same accepted input mode','Numerical comparison does not select the organizer input policy.'),
 (2,'AT-05'):('Keep RAW and DEDUP outputs and their fixtures distinct','A two-mode test does not approve either mode.'),
 (3,'AT-04'):('Distinguish missing, empty and observed backfill with issues','No official source closure contract is proved by a successful test.'),
 (3,'AT-23'):('Prevent a dated prior value from replacing current null','Does not prove expected-source detection, source closure or release policy.'),
 (4,'AT-02'):('All-55 whole-result, type, time, NULL and rounding comparison','The translation strategy and actual equivalence receipts remain pending.'),
 (4,'AT-05'):('Exercise input modes, aliases and historical correction eligibility','These cases do not replace all arithmetic/type edge cases in AT-02.'),
 (5,'AT-06'):('Negative access checks in result, prompt, cache, export, log and errors','Actual grants/projections and every bypass path still need reviewed fixtures.'),
 (5,'AT-13'):('Reject data-text instructions that attempt to change policy or permission','Prompt-injection rejection alone does not prove RLS, pool or cache isolation.'),
 (6,'AT-04'):('Keep missing/late/backfill observations in data issues','The publication/closure policy remains Open.'),
 (6,'AT-05'):('Preserve correction cutoff, input modes and actual versus counterfactual output','A correction fixture alone does not prove business-Signal eligibility.'),
 (6,'AT-24'):('Five DQ classes, eligibility links and positive business control','Unknown-state and edge-policy oracles need approval; SQL success is insufficient.'),
 (7,'AT-19'):('New root, changed incident identifiers and dates without code edits','No official hidden-data detection/QA score is available.'),
 (8,'AT-08'):('Per-recipient recurrence, escalation reason and history','Exact comparison/reset and multilevel clocks remain Open.'),
 (8,'AT-24'):('All R1-R8 cases and three recurrence control points','A rule-version label alone does not prove recipient state isolation.'),
 (9,'AT-10'):('Positive and negative witness-independence and lineage cases','The exact independence method is Proposed and does not prove causality.'),
 (10,'AT-14'):('Valid human decision/draft links and observed before/after evidence','A decision record is not action execution or a causal effect proof.'),
 (10,'AT-29'):('Authorized scripted inputs, fixed replay data and text not treated as decision','All input processing does not prove a real organizational action occurred.'),
 (11,'AT-17'):('Every daily pipeline time and warm/cold state on the stated machine','Final reference hardware/profile and actual measurements are absent.'),
 (11,'AT-18'):('Actual whole-day cost, QA, retries, rates and reservations','Proposed budget shares and model rates need an approved version.'),
 (11,'AT-28'):('Parent budget, timeout and cancellation across child calls','Exact bounds remain Open and no exhaustion/cancellation test was run.'),
 (12,'AT-02'):('Canonical row sets and formula results preserve reference MIN/MAX behavior','Operational current-lifecycle projections need separate negative cases.'),
 (12,'AT-05'):('History/correction fixtures plus shared adversarial reopen cases','Do not infer a new backlog/SLA formula or approved lifecycle precedence.'),
 (13,'AT-13'):('Injected ticket/upload/header instructions cannot change protected outputs','Authorized organizational action boundaries also need their human-decision gates.'),
 (13,'AT-22'):('Upload identity, audience, parse failure, readiness and injection cases','Format/readiness policy is Open; not all raw query paths are upload paths.'),
 (14,'AT-03'):('Question D-1 cutoff and future-data exclusion','Same-day attachment receipt/readiness needs AT-22 and the Open time contract.'),
 (14,'AT-22'):('Unavailable or failed attachment never enters Evidence','It does not select M11 or calendar precedence.'),
 (15,'AT-15'):('Every approved active manager has a valid package; incomplete required coverage stays visible','The M11 roster policy and actual package receipts remain pending.'),
 (15,'AT-21'):('Pre-draft/validation failures and independent once-only valid publication','No guaranteed fallback success or approved failure-export wire contract follows.'),
 (15,'AT-28'):('Parent limits and failure propagation before/after draft','Internal limits and technical status serialization are not selected.'),
 (16,'AT-11'):('Required output/UI schema and role-content checks','Schema success does not resolve suppressed/ongoing semantics.'),
 (16,'AT-30'):('Exact fields, enums and stronger numerical trace checks','The official status/dimension wire questions still need a source answer.'),
 (17,'AT-05'):('Correction cases and shared history boundary cases including correction ties','The equal-rank expected result requires approved source precedence or quarantine.'),
 (18,'AT-19'):('Consistent restart/restore and reproducible new-root delivery','Retention periods, audit viewers and historical archive policy are separate Open choices.'),
 (19,'AT-06'):('Individual-data, purpose and derived/free-text access negative cases','The capacity formula and small-group method remain Open in DL-07.'),
 (19,'AT-10'):('Authorized lineage and evidence references','This criterion does not specify a small-group privacy or text-redaction oracle.'),
 (20,'AT-27'):('Separate add/change KPI tests, fixed references, approval, effect time and rollback','The allowed-change lifecycle is Open; no canonical formula overwrite is approved.'),
 (20,'AT-29'):('Authorized manager changes, receipt/effect time and idempotency','Input processing alone does not prove all-55 preservation or candidate SQL validation.')}
risk_register=read(PREFIX+'risk-register.md');control_rows=[]
for m in members:
    if m['source_type']!='Risk' or m['target_type']!='AT':continue
    n=int(m['source_id'].rsplit('-',1)[1]);facet,limit=RISK_TEST_FACETS[(n,m['target_id'])]
    start=risk_register.index('<a id="'+m['source_id'].lower()+'"></a>')
    tail=risk_register[start:];end=tail.find('\n<a id=',1);block=tail[:end] if end!=-1 else tail
    control=next(x for x in block.splitlines() if x.startswith('Control: '))
    control_rows.append(dict(relationship_id=m['relationship_id'],group_id=m['group_id'],risk_id=m['source_id'],at_id=m['target_id'],
                            control_excerpt=control,existing_criterion_excerpt=at_content[m['target_id']],covered_facet=facet,unproved_or_uncovered_facet=limit,
                            triage_disposition=m['disposition'],status='Pending Review',control_state='Evidence Pending / Not Executed',risk_severity='Not Assessed',
                            source_file=D3,source_anchor=m['target_id'].lower(),risk_source=PREFIX+'risk-register.md#'+m['source_id'].lower(),
                            method='Bounded source-control versus existing-criterion review; no test or full mitigation proof.'))
assert len(control_rows)==38
write_csv(OUT/'risk-control-coverage.csv',control_rows)

# Coverage includes high-impact records even when they have no inferred links.
coverage=[]
for id,r in records.items():
    if r['record_type'] not in ['ADR','DL','Registry Issue','AT','Risk','Decision Boundary']:continue
    matching=[m for m in members if id in [m['source_id'],m['target_id']]]
    coverage.append(dict(record_id=id,record_type=r['record_type'],title=r['title'],inferred_pair_count=len(matching),review_groups=json.dumps(sorted({m['group_id'] for m in matching})),
                         status='Pending Review',note='Inferred links classified; original record status is unchanged.' if matching else 'No inferred link touches this record. Preserve explicit source evidence and review the issue/AT in the readiness list; no edge is invented.'))
for id in kpis:
    matching=[m for m in members if m['source_id']=='REQ-KPI-'+id]
    coverage.append(dict(record_id=id,record_type='Canonical KPI',title=kpis[id]['name_fa'],inferred_pair_count=len(matching),review_groups=json.dumps(sorted({m['group_id'] for m in matching})),status='Pending Review',note=kpi_case[id]))
for stage in stages:
    id='REQ-WF-'+stage['workflow_id']+'-'+stage['stage_order'];matching=[m for m in members if m['source_id']==id]
    coverage.append(dict(record_id=id,record_type='Workflow Stage',title=stage['stage'],inferred_pair_count=len(matching),review_groups=json.dumps(sorted({m['group_id'] for m in matching})),status='Pending Review',note='Numeric SLA / deadline / missing SLA remains as supplied; M01 end-to-end owner does not appoint a stage team.'))
for iid,item in input_by_id.items():
    matching=[m for m in members if m['source_id']=='REQ-INPUT-'+iid]
    coverage.append(dict(record_id=iid,record_type='Manager Input',title=item['type'],inferred_pair_count=len(matching),review_groups=json.dumps(sorted({m['group_id'] for m in matching})),status='Pending Review',note='Actual source event; matching roles/tests do not grant write or action authority.'))
for grant in access:
    matching=[m for m in members if m['source_id']=='REQ-ACCESS-'+grant['manager_id']]
    coverage.append(dict(record_id=grant['manager_id'],record_type='Manager Access Scope',title=grant['visible_entities'],inferred_pair_count=len(matching),review_groups=json.dumps(sorted({m['group_id'] for m in matching})),status='Pending Review',note='Individual workload team: '+(grant['individual_level_data_team'] or 'none')+'; aggregate leave only; effective roster remains policy-gated.'))
write_csv(OUT/'high-impact-coverage.csv',coverage)

summary=dict(state='Draft / Pending Review',inferred_classified=len(members),source_specific_classification_groups=len({m['classification_key'] for m in members}),existing_edge_groups=len(groups),queue_groups=len(queue),
             questionable_relationships=sum(m['disposition']=='Questionable' for m in members),questionable_existing_groups=sum(r['disposition']=='Questionable' and r['relationship_count']>0 for r in queue),
             missing_candidate_pairs=len(missing),missing_candidate_groups=1,priorities_relationships=dict(Counter(m['priority'] for m in members)),
             priorities_queue_groups=dict(Counter(r['priority'] for r in queue)),dispositions_relationships=dict(Counter(m['disposition'] for m in members)),
             kpi_orders_cases=dict(Counter(kpi_case.values())),kpis_historical_sensitive=8,all_kpi_to_orders_edges=55,
             input_test_template_mismatches=sum(m['disposition']=='Questionable' and m['source_id'].startswith('REQ-INPUT-IN') and m['target_type']=='AT' for m in members),
             matrix_modified=False,source_documents_modified=False,product_tests_executed=False)
write(OUT/'summary.json',json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps(summary,ensure_ascii=False,indent=2))
