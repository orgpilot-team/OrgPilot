"""Build source-backed documentation traceability. No product SQL is executed."""
from audit_support import ROOT, OUT, read
from source_audit import rows, emit
import csv
import json
import re

brief = next((ROOT/'Project_berif').glob('*.md')).relative_to(ROOT).as_posix()
pdf = next((ROOT/'Project_berif').glob('*.pdf')).relative_to(ROOT).as_posix()
matrix = []

def add(identifier, source, locator, requirement, component, contract, adr, gates,
        parent='', classification='Requirement', evidence='Source contract', gap='None.', granularity='atomic'):
    assert (ROOT/source).exists(), source
    matrix.append(dict(requirement_id=identifier, parent_req=parent, granularity=granularity,
        classification=classification, evidence_category=evidence, source_path=source,
        source_location=locator, requirement=requirement, architecture_component=component,
        contract_or_rule=contract, adr=adr, acceptance_tests=gates,
        coverage='Documented; product tests not run', remaining_gap=gap))

def B(identifier, pages, requirement, component, contract, adr, gates, parent, gap='None.'):
    add(identifier, brief, 'PDF page(s) '+pages+'; matching Markdown page comments/section',
        requirement, component, contract, adr, gates, parent, gap=gap)

# Keep the original umbrella IDs; granular children below carry individual obligations.
parents = [
 ('01','13-14','Modular intake and report continuation','ingestion;quality;jobs','SourceContract','ADR-16','AT-01;AT-04'),
 ('02','9,13,16','Canonical numbers from registered SQL','kpi;queryGateway;outputValidator','KpiDefinition/QueryRun','ADR-01','AT-02;AT-03'),
 ('03','2,13,17','Configurable organization without code changes','managerConfig;access','OrgEdgeVersion','ADR-08','AT-07'),
 ('04','7-8','Owned, nonrepeated and rule-escalated maximum-five items','signals;reportWriter;outputValidator','R1-R8','ADR-07','AT-08;AT-24'),
 ('05','9-10','Evidence-backed causes and numerical traceability','evidence;insights;outputValidator','EvidenceBundle/InsightBrief','ADR-09','AT-10'),
 ('06','11-12,15','Persian RTL reports and three interfaces','web;publication','ReportContent','ADR-09','AT-11;AT-26'),
 ('07','5-6,16','Three reconstructed workflows with stages/SLA/bottlenecks','workflows','WorkflowStageObservation','ADR-15','AT-12;AT-25'),
 ('08','13','Row controls in every user query','access;queryGateway','AuthContext','ADR-06','AT-06'),
 ('09','5,12-13','Direct-team workload exception and no individual attendance','access;evidence;reportWriter','Purpose/scope projection','ADR-06','AT-06'),
 ('10','13,17','Instructions in source text do not control execution','documents;queryGateway;outputValidator','Input boundary','ADR-16','AT-13'),
 ('11','11-12','Human decision, drafts and follow-up without execution','decisions','DecisionEvent/ActionDraft','ADR-17','AT-14'),
 ('12','14','History and 30-day replay without future leakage','jobs;snapshots','KnowledgeCutoff','ADR-08','AT-03;AT-15'),
 ('13','16-17','Official event/QA accuracy thresholds','audit','EvaluationProfile','ADR-10','AT-09;AT-16'),
 ('14','14','Daily time and simulated deadline','jobs;audit','DayRunOutcome','ADR-10','AT-17'),
 ('15','16','Whole-day LLM cost cap','modelGateway;audit','BudgetLedger','ADR-10','AT-18'),
 ('16','14,18','Hidden-data execution and one-command delivery','jobs;ingestion;api;web','Deployment/configuration contract','ADR-16','AT-19'),
 ('17','14,17','Data errors are reported separately from business signals','quality;signals','DQIncident','ADR-04','AT-04;AT-05')]
for n, pages, req, comp, contract, adr, gates in parents:
    add('REQ-'+n, brief, 'PDF pages '+pages, req, comp, contract, adr, gates, granularity='umbrella')

# General atomic obligations. Source text is authoritative; component allocation is target design.
generic = [
 ('SRC-01','13','Each new source/unit/metric can be added without redesign.','ingestion;managerConfig','SourceAdapter/definition registry','ADR-16','AT-01;AT-27','REQ-01'),
 ('SRC-02','13,17','A missing source does not stop the morning report; identify it.','quality;publication','DQIncident/data_issues','ADR-04','AT-04','REQ-01'),
 ('SRC-03','14,17','Late records are data issues, not new business signals.','quality;signals','DQIncident/knowledge revision','ADR-04','AT-04;AT-05','REQ-17'),
 ('SRC-04','14,17','Historical corrections are data issues, not independent new business events.','quality;snapshots;signals','CorrectionLink','ADR-11','AT-05','REQ-17'),
 ('SRC-05','14,17','Repeated exports are data issues; preserve original sources.','quality;rawFiles','Occurrence versus input policy','ADR-02','AT-05','REQ-17'),
 ('SRC-06','14,17','Source schema changes are reported as data issues.','ingestion;quality','SourceSchema','ADR-16','AT-05','REQ-17'),
 ('NUM-01','9,13','Every numerical report/answer claim has registered executed SQL.','queryGateway;outputValidator','QueryRun/QueryReceipt','ADR-09','AT-02;AT-10','REQ-02'),
 ('NUM-02','16','Reference-rounded values compare with zero tolerance.','kpi;outputValidator','Canonical rounding','ADR-01','AT-02','REQ-02'),
 ('NUM-03','16','Persian/Arabic/Latin digits and thousands formatting do not change values.','reportWriter;outputValidator','Value representation','ADR-09','AT-02;AT-11','REQ-02'),
 ('NUM-04','13','The LLM can propose SQL but cannot supply invented query results.','agent;queryGateway','Read-only registered query result','ADR-06','AT-06;AT-16','REQ-02'),
 ('NUM-05','6,13','KPI calculation and signal detection use deterministic SQL/statistics, not LLM.','kpi;signals','Deterministic engines','ADR-13','AT-02;AT-20','REQ-02'),
 ('EVID-01','9','Each cause has at least two independent witnesses.','evidence;outputValidator','EvidenceBundle','ADR-09','AT-10','REQ-05'),
 ('EVID-02','9','State confidence and alternative causes; correlation is not proven causality.','agent;insights;outputValidator','Cause/alternative/limitation fields','ADR-09','AT-10','REQ-05'),
 ('EVID-03','9','Use one shared Insight Brief as the source for role reports.','insights;reportWriter','InsightVersion','ADR-09','AT-10;AT-26','REQ-05'),
 ('EVID-04','9','Insight includes summary and impact.','insights','Insight.summary/impact','ADR-09','AT-26','REQ-05'),
 ('EVID-05','9','Insight includes metric and deviation.','insights','Insight.metric_refs/deviation','ADR-09','AT-26','REQ-05'),
 ('EVID-06','9','Insight includes breakdown.','insights','Insight.drilldowns','ADR-09','AT-26','REQ-05'),
 ('EVID-07','9','Insight includes possible causes and confidence.','insights','Insight.causes','ADR-09','AT-10;AT-26','REQ-05'),
 ('EVID-08','9','Insight includes decision options.','insights','Insight.options','ADR-09','AT-26','REQ-05'),
 ('EVID-09','9','Insight includes history and prior decisions.','insights;decisions','Insight.history','ADR-09','AT-26','REQ-05'),
 ('EVID-10','9','Insight includes a proposed owner.','insights','Insight.proposed_owner','ADR-09','AT-26','REQ-05'),
 ('EVID-11','9','Insight includes reference/registered query list and click-through provenance.','insights;queryGateway','Insight.query_refs','ADR-09','AT-10;AT-26','REQ-05'),
 ('OUT-01','10','Morning item includes title, number/target, possible cause, owner, suggested question.','reportWriter','ReportContent.item','ADR-09','AT-26','REQ-06'),
 ('OUT-02','10','Chart specification includes type, metric, range, breakdown and target line.','reportWriter','ReportContent.chart','ADR-09','AT-26','REQ-06'),
 ('OUT-03','10-12','Required important/escalated cards include problem, options, effect, cost, risk, confidence, owner, deadline, success criterion and evidence.','reportWriter;decisions','ReportContent.decision_card','ADR-17','AT-10;AT-26','REQ-06'),
 ('OUT-04','10-11','Every package includes scope health, open actions and dashboard link.','publication;reportWriter','DailyBriefPackage','ADR-09','AT-26','REQ-06'),
 ('OUT-05','11','Package includes pending decisions, deadlines and prior-decision effects.','publication;decisions','Decision follow-up','ADR-17','AT-14;AT-26','REQ-06'),
 ('OUT-06','3,11','Support read state, recorded decision, authorized close and referral.','requests;decisions;publication','Manager operations/state','ADR-17','AT-14;AT-29','REQ-11'),
 ('OUT-07','5,11','Executive gets five key health indicators, three workflows, bottlenecks and escalations.','reportWriter;controlUi','Executive package/control room','ADR-15','AT-12;AT-26','REQ-06'),
 ('OUT-08','5,10','Unit and supervisor reports use role depth, goals and preferences within permitted scope.','reportWriter;access','Role projection','ADR-06','AT-06;AT-26','REQ-06'),
 ('UI-01','11-12,18','Provide a conversational assistant with follow-up, charts, queries and decision/referral.','chatUi;requests','InteractiveAssistant','ADR-06','AT-11;AT-16;AT-29','REQ-06'),
 ('UI-02','11-12,18','Provide a role-based BI dashboard with targets, trends and authorized drill-down.','dashboardUi;publication','Dashboard query contract','ADR-06','AT-06;AT-11','REQ-06'),
 ('UI-03','11-12,18','Provide an executive-only three-Workflow control room.','controlUi;access;workflows','Control room','ADR-15','AT-06;AT-12','REQ-06'),
 ('UI-04','15','All required reports and interfaces are Persian RTL.','web;reportWriter','Localization contract','ADR-09','AT-11','REQ-06'),
 ('SEC-01','5,10,13','Each role sees only its allowed subtree; upper roles receive aggregates.','access;queryGateway;evidence','AccessGrantVersion','ADR-06','AT-06','REQ-08'),
 ('SEC-02','13','Apply row restrictions in the data layer for all queries, including conversation.','access;queryGateway','Trusted server identity/RLS','ADR-06','AT-06','REQ-08'),
 ('SEC-03','5,12-13','Individual task details are only for a direct supervisor managing workload.','access;evidence;reportWriter','Direct-team purpose','ADR-06','AT-06','REQ-09'),
 ('SEC-04','6,9,12-13','Leave/availability contributes only to aggregate capacity, not individual attendance monitoring.','access;evidence','Capacity purpose','ADR-06','AT-06;AT-10','REQ-09'),
 ('SEC-05','10,12-13,17','Do not rank or blame employees, or monitor behavior/location.','outputValidator;access','Fairness/privacy controls','ADR-06','AT-06;AT-11','REQ-09'),
 ('SEC-06','13,17','Ticket/upload instructions cannot change tools, numbers, grants or recipients.','documents;agent;outputValidator','Untrusted-data boundary','ADR-16','AT-13','REQ-10'),
 ('CONF-01','3,13','Accept authorized manager goals and targets without code changes.','managerConfig','Versioned settings','ADR-08','AT-07;AT-27','REQ-03'),
 ('CONF-02','3,7,10,13','Priorities affect authorized selection, evidence focus and report emphasis.','managerConfig;signals;evidence;reportWriter','Priority context','ADR-10','AT-07;AT-27','REQ-03'),
 ('CONF-03','8,13','Thresholds and escalation rules are configurable without code changes.','managerConfig;signals','Versioned rule policy','ADR-07','AT-07;AT-24','REQ-03'),
 ('CONF-04','2,13,17','Adding unit, team, or management level does not require code changes.','managerConfig;access','Versioned hierarchy','ADR-08','AT-07','REQ-03'),
 ('ACT-01','11-12','A human decides; ARKA never transfers staff, sends staff messages, or performs organizational actions.','decisions;agent','DecisionEvent/ActionDraft','ADR-17','AT-14','REQ-11'),
 ('ACT-02','11-12','Create task/message drafts only after the human decision; the human approves and sends.','decisions;agent','Authorized draft lifecycle','ADR-17','AT-14;AT-29','REQ-11'),
 ('ACT-03','12,15','Track later observations of scripted decisions without changing fixed replay data.','decisions;evidence','Observed follow-up','ADR-17','AT-14;AT-29','REQ-11'),
 ('TIME-01','14','Use supplied Tehran/Jalali time semantics.','snapshots;kpi;jobs','Clock/context','ADR-08','AT-03','REQ-12'),
 ('TIME-02','14','Admit scheduled data at simulated 00:00 and publish before 07:30.','jobs;publication','Simulated schedule','ADR-10','AT-17','REQ-14'),
 ('TIME-03','14','Whole daily pipeline to reports/JSON takes at most 15 real minutes on the reference machine.','jobs;audit','Daily wall-time receipt','ADR-10','AT-17','REQ-14'),
 ('EVAL-01','16','Detection is >=90%, correct owner, within 24h, correct KPI/entity and plausible hidden-label cause.','signals;publication;audit','EvaluationProfile.discovery','ADR-07','AT-09','REQ-13'),
 ('EVAL-02','17','QA accuracy >=85% on about 60 official questions, including refusals and follow-up.','requests;queryGateway;audit','EvaluationProfile.qa','ADR-06','AT-16','REQ-13'),
 ('EVAL-03','16','Daily LLM total is <=USD 5 for reports, analysis and scripted conversation; measure token costs.','modelGateway;audit','Daily cost record','ADR-10','AT-18','REQ-15'),
 ('EVAL-04','14','Run hidden 90-day data with different event timing without code changes.','ingestion;jobs;managerConfig','Data-root/config interface','ADR-16','AT-19','REQ-16'),
 ('DEL-01','18','Deliver the full system with a single Docker command.','api;worker;web;postgres','Delivery package','ADR-16','AT-19','REQ-16'),
 ('DEL-02','18','Deliver installation/configuration and extension documentation.','audit','Delivery documentation','ADR-16','AT-19','REQ-16'),
 ('DEL-03','18','Deliver full source code with change history.','audit','Source package','ADR-12','AT-19','REQ-16'),
 ('DEL-04','18','Deliver daily API/LLM and infrastructure cost report and 10-minute presentation.','audit','Delivery evidence','ADR-10','AT-18;AT-19','REQ-16'),
 ('EVAL-05','19','Organizer finalizes numeric limits before start; preserve their version.','audit;managerConfig','EvaluationProfile version','ADR-10','AT-09;AT-16;AT-17;AT-18','REQ-13')]
for child, pages, req, comp, contract, adr, gates, parent in generic:
    B('REQ-'+child, pages, req, comp, contract, adr, gates, parent)

# Required source/dataset timing and output obligations, at exact README locations.
readme = [
 ('TIME-04','Replay period table and cutoff paragraph','Initial CRM day000; history days1-60; replay mornings62-91 uses drops000..R-1.','jobs;snapshots','KnowledgeCutoff','ADR-08','AT-03;AT-15','REQ-12'),
 ('TIME-05','Manager input timing paragraph','A day-D question uses operational drops through D-1.','requests;snapshots','Interactive context','ADR-08','AT-03;AT-16','REQ-12'),
 ('TIME-06','Manager input timing paragraph','Day-D manager changes affect the morning D+1 report, subject to recorded M11 precedence conflict.','managerConfig;jobs','Effective-time version','ADR-08','AT-07;AT-29','REQ-12'),
 ('SRC-07','Drop table and manifest paragraphs','Compare manifest with actual file set/count; missing source is not zero.','ingestion;quality','Delivery receipt','ADR-16','AT-01;AT-04','REQ-01'),
 ('NUM-06','KPI prerequisites','Expose calendar date as cal.d and retain calendar fields; use supplied views and monthly_targets.','ingestion;kpi','Reference input contract','ADR-01','AT-02;AT-03','REQ-02'),
 ('CONF-05','KPI extension paragraph','Additional KPIs/breakdowns are allowed; existing definitions must not change.','managerConfig;kpi','Candidate lifecycle','ADR-01','AT-02;AT-27','REQ-02'),
 ('OUT-09','Mandatory output paragraphs','Each active manager has a Persian report and schema JSON each morning.','publication;jobs','ReportVersion/DayRunOutcome','ADR-14','AT-11;AT-15','REQ-06'),
 ('OUT-10','Mandatory output paragraphs','Unavailable current values are null with a data issue.','quality;publication','Publication state/data_issues','ADR-04','AT-04;AT-23','REQ-17'),
 ('OUT-11','Mandatory output paragraphs','Every number in report text is represented in numbers/evidence with KPI/entity/dimension/date.','outputValidator','Number reference','ADR-09','AT-10;AT-30','REQ-02'),
 ('OUT-12','Mandatory output paragraphs','Register IDs for all staff named in text and enforce their allowed purpose/scope.','outputValidator;access','mentioned_staff_ids','ADR-06','AT-06;AT-11','REQ-09'),
 ('INPUT-01','Manager input table','Question outputs use submission/qa/<input_id>.json and qa_answer_schema.json.','publication','QA export','ADR-09','AT-16;AT-29;AT-30','REQ-06'),
 ('OUT-13','Mandatory output paths','Brief outputs use submission/briefs/day_XXX/<manager_id>.json.','publication','Brief export','ADR-14','AT-11;AT-15;AT-30','REQ-06')]
for child, loc, req, comp, contract, adr, gates, parent in readme:
    add('REQ-'+child, 'dataset/README_FA.md', loc, req, comp, contract, adr, gates, parent)

rule_contracts = {
 'R1':('Canonical owner first; preserve owner and do not infer a substitute.', 'Canonical owner; active hierarchy; eligible signal', 'Owned routing; unresolved owner is a routing issue'),
 'R2':('Crit crossing OR warn duration>N OR worsening>=20% from first report.', 'Direction; warn/crit; duration; first-report value; recipients', 'Upward escalation with explicit reason/history'),
 'R3':('Workflow/ORG warn crossing routes to M01.', 'Indicator kind/entity; supplied warn; eligible value', 'Executive escalation; no new evidence access grant'),
 'R4':('Less than10% change is not new; remain open for the same recipient.', 'Series; recipient history; approved comparand', 'Suppress new repeat; retain open history'),
 'R5':('Median same weekday in four previous weeks; deviation>N%; holiday exemption.', 'Calendar; four prior weekday observations; N; cutoff', 'Supported signal or unavailable evaluation'),
 'R6':('At most five report items; supported same-cause signals form one item.', 'Eligible signals; cause evidence; authorized recipient', 'Grouped ranked package; preserve series/owner history'),
 'R7':('Info metrics display only and never alert.', 'Canonical rule=info; value/scope/quality', 'Display only; no alert or escalation occurrence'),
 'R8':('threshold_from_day8 begins only at Jalali day8.', 'cal.day_in_month; thresholds; eligible value', 'No pre-day8 threshold alert; normal threshold evaluation from day8')}
rule_details = []
for number, r in enumerate(rows('dataset/config/escalation_rules.csv'), 2):
    key = r['rule_id']; meaning, inputs, output = rule_contracts[key]
    add('REQ-'+key,'dataset/config/escalation_rules.csv',f'record {number}', meaning,
        'signals;reportWriter;outputValidator', key+'; '+inputs+' -> '+output,'ADR-07','AT-08;AT-24','REQ-04',
        gap='ADR-07 edge policies only. Explicit source comparisons remain fixed.')
    rule_details.append(dict(rule_id=key, source_record=number, source_text=r['rule_fa'],
        classification='Requirement', exact_meaning=meaning, trigger_inputs=inputs, output_routing=output,
        state_transition='See document 001 complete rule table; storage fields are Proposed.',
        ownership='signals evaluates; reportWriter/outputValidator repeat controls; canonical owner/M01 per rule.',
        adr='ADR-07', acceptance='AT-08;AT-24', remaining_ambiguity='See ADR-07; no invented default.'))
emit('rule-contracts.csv', rule_details)

with (OUT/'kpi-contracts.csv').open(encoding='utf-8-sig',newline='') as f:
    for k in csv.DictReader(f):
        add(k['requirement_id'],'dataset/config/kpi_dictionary.csv',k['source'].split(':',1)[1],
            k['formula_population'], 'kpi', k['output_clock']+'; '+k['window']+'; '+k['row_null_and_population_boundary'],
            k['adr'], k['acceptance'], 'REQ-02', gap='PostgreSQL equivalence and accepted input/type policy remain unproved.')
with (OUT/'workflow-contracts.csv').open(encoding='utf-8-sig',newline='') as f:
    for r in csv.DictReader(f):
        add(r['requirement_id'],'dataset/config/workflow_definitions.csv',r['source'].split(':',1)[1],
            f"{r['workflow_id']}.{r['stage_order']}: {r['from_event']} -> {r['to_event']}; SLA={r['sla_hours'] or 'not supplied'}; median target={r['stage_target_median_h'] or 'not supplied'}h; end-to-end owner={r['owner']}.",
            'workflows',r['contract'],r['adr'],r['acceptance'],'REQ-07',gap='Stage owner is Open; no guessed SLA for blank/deadline reference.')

view_meanings = {
 'order_fact':'Order LEFT event join; business-ID grouping; MAX selected paid/failed/cancelled/picked/handover/delivered times; preserve payload multiplicity/conflict boundaries.',
 'ticket_fact':'Ticket LEFT event join; MIN response; MAX inspection/resolution and separate reopened flag; no lifecycle rewrite.',
 'lead_fact':'Lead LEFT events; MAX stage times; latest delivered correction replaces amount, fallback to won; no secondary same-drop precedence.',
 'task_fact':'Task LEFT events and MAX done; preserve overdue state predicates.',
 'revenue_daily':'Calendar spine; paid/refund event-date B2C/marketplace; won-date corrected B2B; canonical COALESCE and raw joins.'}
vtext=read('dataset/config/reference_views.sql')
for key, meaning in view_meanings.items():
    line=next(i for i,s in enumerate(vtext.splitlines(),1) if f'CREATE VIEW {key} AS' in s)
    add('REQ-VIEW-'+key,'dataset/config/reference_views.sql',f'line {line} and its complete CREATE VIEW',meaning,
        'kpi;snapshots',key,'ADR-01;ADR-02;ADR-11','AT-02;AT-03;AT-05','REQ-02',gap='Native translation proof; conflict precedence where source has no tie order.')
for i, r in enumerate(rows('dataset/config/monthly_targets.csv'), 2):
    add('REQ-TARGET-'+r['jmonth'],'dataset/config/monthly_targets.csv',f'record {i}',
        f"Use {r['scope']} target {r['target_million_toman']} million toman for {r['jmonth']}; prorate with supplied calendar fields.",
        'kpi;managerConfig','K_ORG_REV_MTD_ATTAIN target relation','ADR-01;ADR-08','AT-02;AT-07','REQ-02')

for identifier, source, locator, obligation, contract, gap in [
 ('REQ-CAL-01','dataset/calendar/calendar_days.csv','header record1; records2-91',
  'Expose date as cal.d and preserve day_idx,jdate,jmonth,day_in_month,mdays,iwd,is_holiday.',
  'Calendar relation/input contract','Do not replace supplied Jalali metadata with a real-calendar calculation.'),
 ('REQ-CAL-02','dataset/calendar/calendar_days.csv','mdays/jmonth/day_in_month fields',
  'Use supplied month length and day fields for prorated MTD target and R8.',
  'MTD and threshold_from_day8','Partial observed month length is not the mdays denominator.'),
 ('REQ-CAL-03','dataset/calendar/calendar_days.csv','iwd/is_holiday fields',
  'Use supplied weekday/holiday context for R5 instead of a fabricated holiday calendar.',
  'R5 baseline and holiday exception','Historical holiday sample selection remains Open in ADR-07.'),
 ('REQ-CAL-04','dataset/calendar/events_calendar.csv','all7 event records; no known_at field',
  'Use events only as authorized known context; a future event is not an observed cause.',
  'Evidence context/known-at boundary','Announcement-time/planned-event visibility remains Open in ADR-08.')]:
    add(identifier,source,locator,obligation,'snapshots;signals;evidence;kpi',contract,
        'ADR-01;ADR-07;ADR-08','AT-02;AT-03;AT-24','REQ-12',gap=gap)

for file, family, component in [('units.csv','UNIT','managerConfig;access'),('teams.csv','TEAM','managerConfig;access'),('managers.csv','MANAGER','managerConfig;access'),('staff.csv','STAFF','access;evidence')]:
    for number,r in enumerate(rows('dataset/org/'+file),2):
        key = r[{'UNIT':'unit_id','TEAM':'team_id','MANAGER':'manager_id','STAFF':'staff_id'}[family]]
        fields = {k:v for k,v in r.items() if k not in {'name_fa','role_fa'}}
        add('REQ-ORG-'+family+'-'+key,'dataset/org/'+file,f'record {number}',
            'Apply supplied assignment/effective metadata: '+json.dumps(fields,ensure_ascii=False),component,
            'Versioned organization membership; no inferred transfer','ADR-06;ADR-08','AT-06;AT-07','REQ-03',
            gap='Known-at and M11 precedence remain Open. Empty end date is not an access grant.')
for number,r in enumerate(rows('dataset/org/access_matrix.csv'),2):
    add('REQ-ACCESS-'+r['manager_id'],'dataset/org/access_matrix.csv',f'record {number}',
        'Visible entities='+r['visible_entities']+'; direct-team individual workload exception='+(r['individual_level_data_team'] or 'none')+'.',
        'access;queryGateway;evidence;publication','AuthContext/row-column-purpose policy','ADR-06','AT-06;AT-07','REQ-08',
        gap='Exact raw row/column projections and historical scope remain Open; aggregate grants never imply attendance disclosure.')

checks=json.loads((OUT/'source-checks.json').read_text(encoding='utf-8'))
for h in checks['header_versions']:
    suffix = 'post-alias' if ('create_time' in h['header'] or 'event_time' in h['header']) else 'base'
    add('REQ-SOURCE-'+h['family'].replace('.csv','')+'-'+suffix,
        f"dataset/drops/day_{h['first_drop']:03d}/"+h['family'],'header record 1',
        'Process the supplied family without modifying originals; observed fields='+','.join(h['header'])+'.',
        'ingestion;quality','SourceSchema/receipt; actual header observation','ADR-16','AT-01;AT-05','REQ-01',
        evidence='Observed schema used by source contract',gap='Observed headers do not prove hidden-data uniqueness or physical types.')

question_expectations = {
 'Q01':'M09: prior-day T_RSP tickets by category; cause needs enough authorized evidence; operational cutoff065.',
 'Q02':'M04: day066 support gap at day67; no false zero; publication policy determines unavailable versus accepted qualified result.',
 'Q03':'M02: clarify income/target scope; ORG target does not become a Sales grant.',
 'Q04':'M01: seven prior daily picking medians; not median of daily medians.',
 'Q05':'M11: marketplace orders since approved activity start through yesterday; historical scope remains Open.',
 'Q06':'M11: refuse organization revenue outside T_MKT scope.',
 'Q07':'M01: clarify or state a permitted definition of sales; do not replace canonical meaning with legacy report.',
 'Q08':'M03: order count needs a permitted operations projection; do not expose ORG KPI merely because orders are shared.',
 'Q09':'M02: reconcile meaning/period/unit after authorized attachment receipt/readiness; no early filesystem access.',
 'Q10':'M07: direct-team open work per member for workload; no performance ranking.',
 'Q11':'M03: refuse individual warehouse workload; offer a permitted team aggregate.',
 'Q12':'M05: registered lead-source win-rate breakdown with canonical won/lost/30-day population and T_ENT scope.',
 'Q13':'M09: refuse T_CMP cases outside direct-team scope.',
 'Q14':'M08: three prior daily Mashhad on-time values, correct city scope/precision and cutoff089.',
 'Q15':'M01: permitted prior decisions and later observed effects/uncertainty; legacy outcome text is not computed evidence.',
 'Q16':'M06: seven-day spend sum / lead sum per source, canonical NULLIF/unit/arithmetic; not mean daily CPL.'}
event_expectations = {
 'IN01':'Version M01 delivery/customer-experience priority for later selection/evidence/report focus; no formula/grant change.',
 'IN02':'Record M04 DE-01 temporary-transfer decision and drafts/follow-up. Do not execute or invent a staff assignment.',
 'IN03':'Record M04 DE-02 FAQ decision and drafts/follow-up. No outbound publication.',
 'IN04':'Register untrusted meeting minutes; embedded directives cannot change numbers, recipients or access.',
 'IN05':'Version T_MKT/M11/E25/E26 without code changes; day75/76 precedence remains Open.',
 'IN06':'After authority checks, version K_RSP_FRT_MED warn3h to4h for morning79; retain canonical formula and history.',
 'IN07':'Register external sales CSV after receipt and processing; definition/period reconciliation required.'}
manager_contracts=[]
for index,r in enumerate(json.loads(read('dataset/manager_inputs/scripted_inputs.json'))):
    key=r['input_id']; expected=(question_expectations|event_expectations)[key]
    adr='ADR-06;ADR-08;ADR-09' if r['type']=='question' else {'priority':'ADR-10;ADR-08','decision':'ADR-17','upload':'ADR-16;ADR-08','org_change':'ADR-08','threshold_change':'ADR-07;ADR-08'}[r['type']]
    gates='AT-03;AT-06;AT-16;AT-29;AT-30' if r['type']=='question' else 'AT-07;AT-13;AT-14;AT-22;AT-29'
    manager_contracts.append(dict(input_id=key,source_pointer=f'/{index}',day=r['day'],date=r['date'],manager_id=r['manager_id'],
        type=r['type'],source_content=r['content_fa'],attachment=r.get('attachment',''),decision_id=r.get('decision_id',''),
        expected_boundary=expected,operational_drop_max=r['day']-1,next_report_effect=r['day']+1,
        adr=adr,acceptance=gates,execution_evidence='Not executed; source fixture contract only.'))
    add('REQ-INPUT-'+key,'dataset/manager_inputs/scripted_inputs.json',f'/{index}',expected,
        'requests;managerConfig;documents;decisions;publication','Authorized input receipt/context; '+r['type'],adr,gates,'REQ-12',
        gap='Exact authority/readiness/time policies where named in Decision Log; no precomputed numerical answer.')
emit('manager-input-contracts.csv',manager_contracts)

# Every property, required set, enum, numeric bound, and maxItems is traced to its actual JSON pointer.
schema_contracts=[]
def walk(node, pointer, required=False):
    if not isinstance(node,dict):return
    if pointer and any(k in node for k in ['type','enum','$ref','required','maxItems','minimum','maximum','format']):
        yield pointer,node,required
    for k,v in node.get('properties',{}).items():
        yield from walk(v,pointer+'/properties/'+k,k in node.get('required',[]))
    if isinstance(node.get('items'),dict):yield from walk(node['items'],pointer+'/items',False)
    for k,v in node.get('$defs',{}).items():yield from walk(v,pointer+'/$defs/'+k,False)
for name, tag in [('brief_schema.json','BRIEF'),('qa_answer_schema.json','QA')]:
    source='dataset/output_contract/'+name; schema=json.loads(read(source))
    add('REQ-JSON-'+tag+'-ROOT',source,'/', 'Root required fields='+','.join(schema['required'])+'.',
        'publication;outputValidator','Output schema root','ADR-09;ADR-14','AT-11;AT-30','REQ-06')
    for index,(pointer,node,req) in enumerate(walk(schema,''),1):
        constraints={k:node[k] for k in ['type','enum','$ref','required','maxItems','minimum','maximum','format'] if k in node}
        desc=('Required when containing object exists; ' if req else 'Not schema-required at this property; ')+json.dumps(constraints,ensure_ascii=False)
        key=f'REQ-JSON-{tag}-{index:03d}'
        add(key,source,pointer,desc,'publication;outputValidator','Exact source schema constraint','ADR-09','AT-11;AT-30','REQ-06',
            gap='Schema validity does not prove required narrative content, numeric correctness or authorization.')
        schema_contracts.append(dict(requirement_id=key,source=source,pointer=pointer,required_in_parent=req,
            constraints=json.dumps(constraints,ensure_ascii=False),source_description=node.get('description','')))
emit('output-schema-contracts.csv',schema_contracts)

# Team decisions are distinct from official requirements and from proposed mechanisms.
accepted = [
 ('AGENT','One bounded AI Agent with deterministic supporting modules.','agent;requests;kpi;signals','ADR-13','AT-20;AT-28'),
 ('PG','PostgreSQL is the only product database engine.','postgres;kpi;queryGateway','ADR-01','AT-02;AT-06'),
 ('PUBLICATION','Publish valid manager reports independently and record failed required reports.','publication;jobs;audit','ADR-14','AT-15;AT-21'),
 ('DETERMINISTIC','Calculation, signals, authorization and final validation are deterministic.','kpi;signals;access;outputValidator','ADR-13;ADR-06','AT-02;AT-06;AT-20'),
 ('HUMAN','Organizational decisions and execution authority remain human-controlled.','decisions;agent','ADR-17','AT-14;AT-29')]
for key,meaning,component,adr,gates in accepted:
    add('DEC-'+key,'docs/architecture/audit-2026-11-09/request.txt','section 1: Important accepted decisions',meaning,
        component,'Accepted target boundary',adr,gates,classification='Accepted',evidence='User confirmation and S16/S17',
        gap='Implementation proof remains absent; original approval date/named approvers are not invented.')

assert len({r['requirement_id'] for r in matrix})==len(matrix)
emit('requirements-traceability.csv',matrix)

gate_bases={
 1:('Requirement','Brief13-14; README manifest/source rules','Idempotent receipt mechanism Proposed'),
 2:('Requirement','KPI dictionary all rows; reference views; brief16','PostgreSQL translation strategy Proposed; engine Accepted'),
 3:('Requirement','README replay/input cutoff; brief14','Snapshot/commit implementation Proposed'),
 4:('Requirement','README unavailable values; brief13-14,17','Closure/publication policy Open'),
 5:('Requirement','Brief14,17; observed aliases/correction; README','RAW/DEDUP and correction tie Open'),
 6:('Requirement','Access matrix; brief5,10,12-13','Physical roles/projections Proposed; exact fields Open'),
 7:('Requirement','Brief13,17; README; IN05/IN06','M11 precedence/activation authority Open'),
 8:('Requirement','R1-R8; brief7-8','Ranking/grouping/reset mechanism Proposed/Open'),
 9:('Requirement','Brief16 discovery definition','Official hidden labels unavailable'),
 10:('Requirement','Brief9-10,13,16','Independence/scoring algorithm Proposed'),
 11:('Requirement','Brief10-12,15; output schemas','Internal complete content mapping Open'),
 12:('Requirement','Workflow stages; canonical workflow SQL; brief5-6,16','Stage owner mapping Open'),
 13:('Requirement','Brief13,17; injected operational upload','Enforcement mechanism Proposed'),
 14:('Requirement','Brief11-12,15; scripted decisions','Execution confirmation fields Open'),
 15:('Requirement','README active roster; brief16','Independent publication Accepted; M11 precedence Open'),
 16:('Requirement','Brief17; scripted questions','16 fixtures are not about60 official questions'),
 17:('Requirement','Brief14,19','Hardware/final profile missing; no benchmark'),
 18:('Requirement','Brief16,19','Reservation/rates/retry mechanism Proposed'),
 19:('Requirement','Brief14,18','Restore/restart engineering gate Proposed, not a supplied specific backup policy'),
 20:('Accepted','User request1; S16 Q01; S17 agent','Exact tool/time/token/step limits Open'),
 21:('Accepted','User request1; S16 Q16; S17 PartialPublication','Atomic package mechanism and fallback Proposed'),
 22:('Requirement','Brief3,12-14; README uploads; IN04/IN07','Exact format/readiness policy Open'),
 23:('Proposed','S16 Q06 summary; existing S17 dated-value boundary','Historical display mapping/age Open; never replace current null'),
 24:('Requirement','escalation_rules.csv R1-R8; brief8 three checks','Only unspecified comparisons/samples/reset remain Open'),
 25:('Requirement','workflow_definitions.csv12 stages and canonical workflow SQL','Owner/projection details Open'),
 26:('Requirement','Brief5,9-12,15','Internal/wire content mapping Open'),
 27:('Requirement','Brief13; README KPI extension','Inactive-candidate approval mechanism Proposed'),
 28:('Proposed','Existing S17 F02/F05; user bounded-Agent boundary','Exact controller limits and cancellation product behavior Open'),
 29:('Requirement','Scripted inputs23; brief3,11-14','Write authority and same-day receipt precedence Open'),
 30:('Requirement','brief_schema.json; qa_answer_schema.json; README','Stronger semantic validators separate from permissive schema')}
emit('acceptance-basis.csv',[dict(test_id=f'AT-{i:02d}',basis_status=gate_bases[i][0],source=gate_bases[i][1],
    mechanism_or_gap=gate_bases[i][2],execution_status='Planned; not run by this audit') for i in range(1,31)])

groups={}
for r in matrix:
    family=r['requirement_id'].split('-')[1]
    groups[family]=groups.get(family,0)+1
summary=f'''# Requirement traceability guide

The [CSV matrix](requirements-traceability.csv) has {len(matrix)} source-backed rows. The original REQ-01 through REQ-17 remain umbrella IDs. Their children are atomic obligations or exact source records. Accepted decisions use DEC-* IDs; they are not mislabeled official requirements. Observation is an evidence category, not approval.

Each row identifies the source path/location, obligation, existing component, contract/rule, ADR, planned acceptance gate and remaining gap. A documented row is not an executed test or a complete implementation. The [acceptance-basis register](acceptance-basis.csv) separates official requirements, Accepted target boundaries and Proposed mechanisms.

| Detailed coverage | Artifact / semantic checks |
|---|---|
| R1-R8 | [Rule contracts](rule-contracts.csv): exact source text, trigger/input, output/routing, state and gates. Fixed comparisons are separate from genuine ambiguity. |
| 55 canonical KPIs | [KPI contracts](kpi-contracts.csv): every original field and SQL/hash; formula/population, clock/window, row/NULL and precision boundaries. Metadata checked against all 55 source rows. No SQL was run. |
| 12 Workflow stages | [Stage contracts](workflow-contracts.csv): every endpoint, SLA kind, median target, end-to-end owner and Open stage owner. Canonical workflow SQL remains separate. |
| Organization/access | Exact unit/team/manager/staff assignment and all 11 access-matrix records. Known/effective time and read-versus-write authority remain distinct. |
| Sources/schema | Every delivered header signature and five canonical view contracts. [Source checks](source-checks.json) compare all 91 manifests with actual counts and preserve fixture evidence. |
| Manager inputs | [All 23 records](manager-input-contracts.csv), including all 16 questions and seven non-question events. No stored numerical answers. |
| Output schemas | [Every property/constraint](output-schema-contracts.csv), exact required sets and enums. Conditional nested requirements are not promoted to unconditional fields. |
| Report/Agent/privacy/delivery | Atomic brief-derived obligations and five separately classified Accepted boundaries. Unsupported engineering details remain Proposed/Open. |

Open gaps are explicit: PostgreSQL equivalence/types and input mode; closure/publication; shared-source/privacy/capacity policies; stage owners; unspecified rule boundaries; M11/receipt timing; output mapping and candidate write authority; model limits and final organizer profile. See the [Decision Log](../003-decisions-and-roadmap.md#decision-log).

Optional monthly board summary, forecasting, what-if, audio, messenger integration and automatic decision-impact evaluation are not mandatory runtime dependencies. Employee ranking/surveillance, autonomous actions, real-system connectors, payroll and budgeting remain outside the brief's scope. Ten base reports do not remove the active-manager requirement.
'''
(OUT/'requirements-traceability.md').write_text(summary,encoding='utf-8',newline='\n')
(OUT/'traceability-summary.json').write_text(json.dumps(dict(rows=len(matrix),families=groups,
    rule_rows=8,kpi_rows=55,stage_rows=12,input_rows=23,schema_property_rows=len(schema_contracts),
    product_tests_executed=False),indent=2),encoding='utf-8')
print(json.dumps(dict(traceability_rows=len(matrix),schema_contracts=len(schema_contracts),input_contracts=23,product_tests_run=False)))
