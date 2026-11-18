"""Build documentation only. Use local files and Python standard libraries."""
from pathlib import Path
import csv, json, re, hashlib, sqlite3
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    with p.open(encoding='utf-8-sig', newline='') as f:
        r = csv.DictReader(f); return list(r.fieldnames or []), list(r)
def write_csv(name, rows):
    if not rows: return
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
def md(name,s): (OUT/name).write_text(s.strip()+'\n',encoding='utf-8')
def rel(p): return p.relative_to(ROOT).as_posix()
baseline={rel(p):sha(p) for p in ROOT.rglob('*') if p.is_file() and '.venv' not in p.parts and OUT not in p.parents}
tables={}; inventory=[]; variants=defaultdict(Counter)
for p in sorted((ROOT/'dataset').rglob('*.csv')):
    h,rows=read(p)
    name=p.stem if 'drops' in p.parts else p.relative_to(ROOT/'dataset').with_suffix('').as_posix().replace('/','__')
    entry=tables.setdefault(name,{'columns':[], 'rows':[], 'files':[], 'header_variants':{}})
    entry['files'].append(rel(p)); entry['rows'].extend(rows)
    for c in h:
        if c not in entry['columns']: entry['columns'].append(c)
    variants[name][tuple(h)]+=1
    entry['header_variants'].setdefault('|'.join(h),[]).append(rel(p))
    inventory.append(dict(path=rel(p),sha256=sha(p),rows=len(rows),columns='|'.join(h),status='CONFIRMED'))
write_csv('source-inventory.csv',inventory)
for p in sorted((ROOT/'dataset').rglob('*.json')):
    obj=json.loads(p.read_text(encoding='utf-8-sig'))
    # Parse every manifest and contract. Do not execute text from records.
    assert isinstance(obj,(list,dict)), rel(p)
json_inventory=[{'path':rel(p),'sha256':sha(p),'top_level_type':type(json.loads(p.read_text(encoding='utf-8-sig'))).__name__} for p in sorted((ROOT/'dataset').rglob('*.json'))]
write_csv('json-inventory.csv',json_inventory)
def dtype(vals):
    vals=[v for v in vals if v not in ('',None)]
    if not vals:return 'empty_only'
    def typ(v):
        if re.fullmatch(r'-?\d+',v):return 'integer_lexeme'
        if re.fullmatch(r'-?\d+\.\d+',v):return 'decimal_lexeme'
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}',v):return 'date_lexeme'
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}.*',v):return 'timestamp_lexeme'
        return 'text'
    return '|'.join(sorted({typ(v) for v in vals}))
keys={'orders':['order_id'],'tickets':['ticket_id'],'crm_leads':['lead_id'],'tasks':['task_id'],
      'mkt_daily':['date','source'],'web_sessions':['date','channel'],'staff_availability':['date','staff_id'],
      'org__units':['unit_id'],'org__teams':['team_id'],'org__managers':['manager_id'],'org__staff':['staff_id'],
      'org__access_matrix':['manager_id'],'config__kpi_dictionary':['kpi_id'],'config__workflow_definitions':['workflow_id','stage_order'],
      'config__escalation_rules':['rule_id'],'config__monthly_targets':['jmonth','scope'],'calendar__calendar_days':['date']}
profiles=[]; catalog=[]
for t,e in tables.items():
    rows=e['rows']; kk=keys.get(t,[]); keyvals=[tuple(r.get(c,'') for c in kk) for r in rows] if kk else []
    dup=sum(n-1 for n in Counter(keyvals).values()) if kk else ''
    kind='event_history' if t.endswith('_events') else ('daily_observation' if t in ['mkt_daily','web_sessions','staff_availability'] else 'entity_or_configuration_records')
    keynote=('Candidate only; unique in supplied records' if kk and not dup else 'Not a reliable raw primary key; preserve file occurrence and CSV record ordinal')
    profiles.append(dict(table=t,files=len(e['files']),rows=len(rows),columns=len(e['columns']),header_variants=len(variants[t]),record_kind=kind,candidate_key='|'.join(kk) or 'UNRESOLVED',candidate_key_duplicate_rows=dup,exact_repeat_rows=len(rows)-len({json.dumps(r,sort_keys=True) for r in rows}),key_status=keynote,physical_constraints='NONE: CSV files',evidence='|'.join(e['files'][:1]),status='CONFIRMED'))
    for c in e['columns']:
        present=[r[c] for r in rows if c in r]; empty=sum(v=='' for v in present)
        catalog.append(dict(table=t,column=c,observed_type=dtype(present),physical_type='CSV text; no declared database type',present_rows=len(present),empty_cells=empty,absent_column_rows=len(rows)-len(present),candidate_key_component=str(c in kk),candidate_key_status=keynote,header_variant_files=';'.join(f'{k}: {len(v)} files' for k,v in e['header_variants'].items()),evidence=e['files'][0],status='CONFIRMED'))
write_csv('table-column-catalog.csv',catalog);write_csv('table-profiles.csv',profiles)

# List observed key relationships. SQL joins are DERIVED, explicit org assignments are CONFIRMED.
spec=[('order_events','order_id','orders','order_id','DERIVED','reference_views.sql: order_fact and revenue_daily'),
('tickets','order_id','orders','order_id','DERIVED','kpi_dictionary.csv: K_WH_DAMAGE_BY_CAT_7D'),
('ticket_events','ticket_id','tickets','ticket_id','DERIVED','reference_views.sql: ticket_fact'),
('csat','ticket_id','tickets','ticket_id','DERIVED','kpi_dictionary.csv: K_RSP_CSAT'),
('crm_lead_events','lead_id','crm_leads','lead_id','DERIVED','reference_views.sql: lead_fact'),
('task_events','task_id','tasks','task_id','DERIVED','reference_views.sql: task_fact'),
('tasks','team_id','org__teams','team_id','CONFIRMED','README_FA.md; org/teams.csv'),
('tasks','owner_id','org__staff','staff_id','DERIVED','README_FA.md; matching observed identifiers'),
('tickets','team_id','org__teams','team_id','CONFIRMED','README_FA.md; org/teams.csv'),
('order_events','actor_team','org__teams|org__units','team_id|unit_id','DERIVED','Observed polymorphic actor: T_SHP, T_WH, T_CMP, U_SAL; not an order ownership grant'),
('ticket_events','staff_id','org__staff','staff_id','DERIVED','Matching staff identifiers; not direct-team authorization'),
('staff_availability','staff_id','org__staff','staff_id','CONFIRMED','README_FA.md; org/staff.csv'),
('staff_availability','team_id','org__teams','team_id','CONFIRMED','README_FA.md; org/teams.csv'),
('org__staff','team_id','org__teams','team_id','CONFIRMED','org/staff.csv; org/teams.csv'),
('org__teams','unit_id','org__units','unit_id','CONFIRMED','org/teams.csv; org/units.csv'),
('org__teams','supervisor_id','org__managers','manager_id','CONFIRMED','org/teams.csv'),
('org__units','manager_id','org__managers','manager_id','CONFIRMED','org/units.csv'),
('org__units','parent_id','org__units','unit_id','CONFIRMED','org/units.csv'),
('org__access_matrix','manager_id','org__managers','manager_id','CONFIRMED','org/access_matrix.csv'),
('config__kpi_dictionary','owner_manager_id','org__managers','manager_id','CONFIRMED','config/kpi_dictionary.csv'),
('mkt_daily','date','calendar__calendar_days','date','DERIVED','K_DIG_CPL_7D; cal.date renamed d'),
('web_sessions','date','calendar__calendar_days','date','DERIVED','Observed matching date domain; inferred business date relation, not a K_SAL_CONV calendar join'),
('staff_availability','date','calendar__calendar_days','date','DERIVED','Matching date values; capacity context only')]
relations=[]
for ch,ck,pa,pk,st,ev in spec:
    cr=tables[ch]['rows']
    if '|' in pa:
        pv=Counter(r[key] for parent,key in zip(pa.split('|'),pk.split('|')) for r in tables[parent]['rows'] if r.get(key))
    else:
        pr=tables[pa]['rows']; pv=Counter(r[pk] for r in pr if r.get(pk))
    cv=Counter(r[ck] for r in cr if r.get(ck))
    missing=sum(not r.get(ck) for r in cr);unmatched=sum(n for v,n in cv.items() if v not in pv)
    # Cardinality is measured on distinct parent IDs, not a constraint on raw occurrences.
    relations.append(dict(relationship_id=f'R{len(relations)+1:02}',child_table=ch,child_column=ck,parent_table=pa,parent_column=pk,status=st,evidence=ev,empty_or_absent_child_keys=missing,unmatched_child_rows=unmatched,duplicate_parent_key_rows=sum(n-1 for n in pv.values()),maximum_child_rows_per_parent_key=max(cv.values(),default=0),observed_cardinality='parent distinct key 1 to 0..'+str(max(cv.values(),default=0))+' child rows',enforced='NO',limitation='Full supplied data only; raw repeats can multiply joins; historical eligibility needs separate checks'))
write_csv('relationship-evidence.csv',relations)
for row in catalog:
    rr=[r for r in relations if r['child_table']==row['table'] and r['child_column']==row['column']]
    row['candidate_foreign_keys']=';'.join(r['parent_table']+'.'+r['parent_column'] for r in rr)
    row['relationship_evidence_ids']='|'.join(r['relationship_id'] for r in rr)
    row['foreign_key_enforcement']='NONE: source CSV files'
write_csv('table-column-catalog.csv',catalog)

managers=tables['org__managers']['rows']; grants={r['manager_id']:r for r in tables['org__access_matrix']['rows']}; kpis=tables['config__kpi_dictionary']['rows']
roles=dict(zip([f'M{i:02}' for i in range(1,12)],['Executive Manager','Sales Unit Manager','Operations Unit Manager','Support Unit Manager','Enterprise Sales Supervisor','Digital Marketing Supervisor','Warehouse Supervisor','Shipping Supervisor','Response Supervisor','Complaints Supervisor','Marketplace Supervisor']))
scope_records=[]
entities={r['unit_id'] for r in tables['org__units']['rows']}|{r['team_id'] for r in tables['org__teams']['rows']}
for mid,g in grants.items():
    for entity in g['visible_entities'].split('|'):
        assert entity in entities
        scope_records.append(dict(manager_id=mid,entity_id=entity,relationship='aggregate display scope',direct_team_exception=str(entity==g['individual_level_data_team']),evidence='dataset/org/access_matrix.csv',status='CONFIRMED'))
write_csv('organization-scope-evidence.csv',scope_records)
assert len(kpis)==55 and len(managers)==11
view_sql=(ROOT/'dataset/config/reference_views.sql').read_text(encoding='utf-8-sig')
conn=sqlite3.connect(':memory:');conn.create_aggregate('median',1,type('Median',(object,),{'step':lambda self,x:None,'finalize':lambda self:None}))
source_names=[t for t in tables if '__' not in t]+['cal','monthly_targets']
for t in source_names:
    cols=tables['calendar__calendar_days']['columns'] if t=='cal' else tables['config__monthly_targets']['columns'] if t=='monthly_targets' else tables[t]['columns']
    cols=[('d' if t=='cal' and c=='date' else c) for c in cols]
    if t=='crm_lead_events':cols=cols+['drop_day']
    conn.execute('CREATE TABLE "'+t+'" ('+','.join('"'+c+'" TEXT' for c in cols)+')')
conn.executescript(view_sql)
views=['order_fact','ticket_fact','lead_fact','task_fact','revenue_daily']
sql_reads={};exec_sources={};direct_views={};direct_relations={}
for k in kpis:
    reads=set()
    def auth(action,a,b,db,context):
        if action==sqlite3.SQLITE_READ:reads.add((a,b or '',context or ''))
        return sqlite3.SQLITE_OK
    conn.set_authorizer(auth);conn.execute('EXPLAIN '+k['sql']).fetchall();conn.set_authorizer(None)
    sql_reads[k['kpi_id']]=reads
    exec_sources[k['kpi_id']]={a for a,b,c in reads if a in source_names}
    direct_views[k['kpi_id']]={v for v in views if re.search(r'\b'+v+r'\b',k['sql'])}
    direct_relations[k['kpi_id']]={v for v in source_names+views if re.search(r'\b'+v+r'\b',k['sql'])}

# Expand selected view columns to source inputs. Keep execution reads separate.
fact_base={'order_fact':('orders','order_events','order_id'), 'ticket_fact':('tickets','ticket_events','ticket_id'), 'lead_fact':('crm_leads','crm_lead_events','lead_id'), 'task_fact':('tasks','task_events','task_id')}
time_fields={'paid_at','failed_at','cancelled_at','picked_at','handed_over_at','delivered_at','first_response_at','inspected_at','resolved_at','reopened','first_contact_at','qualified_at','proposal_at','won_at','lost_at','done_at','contract_value'}
value_columns={}; join_columns={}
def add_target(d,t,cs):d[t].update(cs)
for k in kpis:
    q=k['sql']; vc=defaultdict(set);jc=defaultdict(set)
    for t in direct_relations[k['kpi_id']]:
        if t in fact_base:
            base,events,key=fact_base[t];add_target(jc,base,[key]);add_target(jc,events,[key])
            for c in tables[base]['columns']:
                if re.search(r'\b'+c+r'\b',q):vc[base].add(c)
            if any(re.search(r'\b'+f+r'\b',q) for f in time_fields):add_target(vc,events,['event','at'])
            if t=='lead_fact' and ('contract_value' in q):add_target(vc,events,['contract_value_toman']);jc[events].add('drop_day')
        elif t=='revenue_daily':
            add_target(jc,'cal',['d'])
            if re.search(r'\b(b2c|marketplace)\b',q):
                add_target(vc,'orders',['order_value_toman']);add_target(vc,'order_events',['event','at','amount_toman']);add_target(jc,'orders',['order_id']);add_target(jc,'order_events',['order_id'])
                if 'marketplace' in q:vc['orders'].add('channel')
            if re.search(r'\bb2b\b',q):
                add_target(jc,'crm_leads',['lead_id']);add_target(jc,'crm_lead_events',['lead_id','drop_day']);add_target(vc,'crm_lead_events',['event','at','contract_value_toman'])
        elif t in source_names:
            real='calendar__calendar_days' if t=='cal' else 'config__monthly_targets' if t=='monthly_targets' else t
            for c in tables[real]['columns']:
                querycol='d' if t=='cal' and c=='date' else c
                if re.search(r'\b'+querycol+r'\b',q):vc[t].add(querycol)
    if 'USING(ticket_id)' in q:
        for t in ['csat','tickets']:jc[t].add('ticket_id')
    if 'USING(order_id)' in q:
        for t in ['tickets','orders']:jc[t].add('order_id')
    # Qualified fields can share names. Extra matches are conservative and are labelled.
    value_columns[k['kpi_id']]=vc;join_columns[k['kpi_id']]=jc

lineage=[]
for index,k in enumerate(kpis,2):
    kid=k['kpi_id'];vs=set(value_columns[kid])|set(join_columns[kid]);allowed=[m['manager_id'] for m in managers if k['entity_id'] in grants[m['manager_id']]['visible_entities'].split('|')]
    lineage.append(dict(kpi_id=kid,entity_id=k['entity_id'],owner_manager_id=k['owner_manager_id'],reference_views='|'.join(sorted(direct_views[kid])),execution_sources='|'.join(sorted(exec_sources[kid])),selected_value_and_population_sources='|'.join(sorted(vs)),value_columns=json.dumps({t:sorted(v) for t,v in value_columns[kid].items()},sort_keys=True),join_filter_columns=json.dumps({t:sorted(v) for t,v in join_columns[kid].items()},sort_keys=True),authorized_managers='|'.join(allowed),authorization_basis='CONFIRMED: entity in access_matrix.visible_entities; aggregate display only',effective_limit='M11/T_MKT day 75; first report morning 75 or 76 UNRESOLVED; no automatic historic grant',sql=k['sql'],sql_evidence=f'dataset/config/kpi_dictionary.csv: record {index}',dependency_status='DERIVED',column_dependency_limit='Conservative selected-column expansion; same-name fields may be overincluded. Execution sources are independently compiled by SQLite EXPLAIN. No permission follows from a dependency.'))
write_csv('kpi-source-manager-mapping.csv',lineage)
reads_rows=[dict(kpi_id=k,relation=a,column=b,view_context=c,status='DERIVED',meaning='SQLite prepare-time execution read; star expansion can include unused fields; not manager visibility') for k,reads in sql_reads.items() for a,b,c in sorted(reads)]
write_csv('sql-execution-column-reads.csv',reads_rows)

# Access entries have independent computation and display classifications.
access=[];manager_summary=[]
idcols={'staff_id','owner_id','name_fa','customer_id'}
for m in managers:
    mid=m['manager_id'];scope=grants[mid]['visible_entities'].split('|');team=grants[mid]['individual_level_data_team'];level=int(m['level'])
    permitted=[k for k in kpis if k['entity_id'] in scope]
    needed=defaultdict(set)
    for k in permitted:
        for d in (value_columns[k['kpi_id']],join_columns[k['kpi_id']]):
            for t,cols in d.items():
                real='calendar__calendar_days' if t=='cal' else 'config__monthly_targets' if t=='monthly_targets' else t
                needed[real].update('date' if t=='cal' and c=='d' else c for c in cols)
    rowbase='entity_id IN ('+','.join(scope)+'); apply before query/LLM; delivered_drop <= R-1; active scope required'
    manager_summary.append(dict(manager_id=mid,role=m['role_fa'],level=level,scope='|'.join(scope),direct_team=team,effective_from_day=m['effective_from_day'],permitted_kpis='|'.join(k['kpi_id'] for k in permitted),raw_source_access='UNRESOLVED: no raw table grant supplied',internal_calculation_access='Service only; not the manager identity',query_access='Scoped aggregate projections; direct-team workload exception only',report_access='Same limits as query; remove identifiers and sensitive evidence',purpose='Workload management only for individual data; capacity aggregate only',row_filter=rowbase,status='CONFIRMED scope; DERIVED KPI list; physical projections PROPOSED'))
    for cat in catalog:
        t=cat['table'];c=cat['column'];dependency=[]
        for k in permitted:
            kid=k['kpi_id'];tt='cal' if t=='calendar__calendar_days' else 'monthly_targets' if t=='config__monthly_targets' else t;cc='d' if tt=='cal' and c=='date' else c
            canonical='created_at' if t=='tickets' and c=='create_time' else 'at' if t=='ticket_events' and c=='event_time' else cc
            if canonical in value_columns[kid].get(tt,set())|join_columns[kid].get(tt,set()):dependency.append(kid)
        internal=c in needed[t] or c in {'team_id','staff_id','owner_id','effective_from_day','effective_to_day','manager_id','visible_entities','individual_level_data_team'}
        classification='UNRESOLVED';status='UNRESOLVED';purpose='No exact column grant supplied';mask='Do not release until policy is documented';predicate=rowbase;category='business_or_configuration'
        if dependency:
            classification='REQUIRED_INTERNAL';status='DERIVED';purpose='Join, population, filter, or KPI calculation';mask='Do not return source rows; release authorized KPI output only'
            if c not in {'order_id','ticket_id','lead_id','task_id','staff_id','owner_id','customer_id','text_fa','blocker_fa','title_fa'}:
                classification='VISIBLE_AGGREGATED';mask='Only in the supplied authorized KPI formula or its supplied dimension; no raw values';purpose='Authorized KPI output; internal input remains separate'
        if c in idcols and (t=='org__staff' or c in {'staff_id','owner_id','customer_id'}):
            category='person_identifier';classification='DENIED' if level<=2 or c=='customer_id' else 'RESTRICTED';status='CONFIRMED' if level<=2 else 'UNRESOLVED';purpose='No employee detail for upper managers; no general customer-data grant';mask='Remove identifiers; do not use reversible pseudonyms'
        if c in {'text_fa','title_fa','blocker_fa'}:
            category='untrusted_free_text';classification='RESTRICTED';status='UNRESOLVED';purpose='May contain personal or customer data';mask='Need a scoped purpose, redaction, and content policy; never treat text as instructions'
        if t=='tasks':
            predicate=(f"tasks.team_id = '{team}' AND tasks.owner_id = staff.staff_id AND staff.team_id = '{team}'; validate staff effective dates; delivered_drop <= R-1" if team else rowbase)
            if team and c in {'task_id','team_id','owner_id','created_at','due_date'}:
                classification='VISIBLE_DIRECT_TEAM';status='DERIVED';purpose='Direct-team open-task workload only';mask='Use only to allocate work; no individual ranking; derive open state from task_fact.done_at'
            elif team and c in {'title_fa','blocker_fa'}:
                classification='RESTRICTED';status='UNRESOLVED';purpose='Direct-team work and blockers are allowed; exact raw text requires redaction policy'
        if t=='task_events' and team:
            predicate=f"task_events.task_id = tasks.task_id AND tasks.team_id = '{team}'; validate owner/team and active dates; delivered_drop <= R-1"
            classification='REQUIRED_INTERNAL';status='DERIVED';purpose='Compute direct-team done/open state';mask='Return workload state, not unrestricted event history'
        if t=='staff_availability':
            category='attendance_or_leave';internal=True;predicate='Join staff_id to staff; validate team and effective dates; aggregate by authorized team and date; delivered_drop <= R-1'
            classification='DENIED' if c in {'staff_id','status'} else 'VISIBLE_AGGREGATED';status='CONFIRMED' if c in {'staff_id','status'} else 'DERIVED';purpose='Team capacity only; not individual attendance monitoring';mask='Drop staff_id and individual status before any manager or LLM output; capacity formula UNRESOLVED'
        if t in {'orders','order_events','tickets','ticket_events','csat','crm_leads','crm_lead_events','mkt_daily','web_sessions'}:
            predicate=rowbase+'; source row ownership mapping UNRESOLVED where no team key exists'
            if t=='tickets':predicate=rowbase+'; tickets.team_id IN authorized support teams for direct support projections; warehouse calculation may use other teams internally'
            if t in {'ticket_events','csat'}:predicate=rowbase+'; join ticket_id to tickets.team_id for scoped support projections; internal cross-team KPI computation is separate'
            if mid=='M11' and t in {'orders','order_events'}:predicate="orders.channel = 'marketplace'; order_events joins orders USING(order_id); effective start day 75; first report and historic window UNRESOLVED; delivered_drop <= R-1"
        access.append(dict(manager_id=mid,role=m['role_fa'],management_level=level,organizational_scope='|'.join(scope),source_table=t,column=c,data_category=category,purpose=purpose,required_kpi_dependencies='|'.join(dependency),internal_use='REQUIRED_INTERNAL' if internal or dependency else 'UNRESOLVED',raw_source_access='UNRESOLVED: no raw grant supplied',row_level_predicate=predicate,column_visibility=classification,query_visibility=classification,report_visibility=classification,aggregation_or_masking=mask,evidence='dataset/org/access_matrix.csv:'+mid+'; DIDRAH brief pp.6,10,12,13; '+('dataset/config/kpi_dictionary.csv:'+'|'.join(dependency) if dependency else 'dataset/README_FA.md; observed header'),confidence_status=status,projection_implementation='PROPOSED; no database policy is implemented'))
for row in manager_summary:row['role_english']=roles[row['manager_id']]
write_csv('access-matrix-detailed.csv',access);write_csv('manager-access-summary.csv',manager_summary)

def diagram(name,lines):md(name+'.mmd','\n'.join(lines))
legend=['  LEGEND["CONFIRMED: direct evidence | DERIVED: SQL or measured relation<br/>PROPOSED: review required | UNRESOLVED: evidence gap"]']
overview=['flowchart LR']+legend
for group,ts in [('Orders',['orders','order_events']),('Support',['tickets','ticket_events','csat']),('CRM',['crm_leads','crm_lead_events']),('Workload',['tasks','task_events','staff_availability']),('Marketing',['mkt_daily','web_sessions']),('Organization',['org__units','org__teams','org__managers','org__staff','org__access_matrix']),('Configuration',['config__kpi_dictionary','config__workflow_definitions','config__monthly_targets','config__escalation_rules']),('Calendar',['calendar__calendar_days','calendar__events_calendar'])]:
    overview.append(f'  subgraph {group}')
    for t in ts:overview.append(f'    {t}["{t}<br/>{len(tables[t]["columns"])} observed columns"]')
    overview.append('  end')
for r in relations:
    if r['child_table'] in {'order_events','tickets','ticket_events','csat','crm_lead_events','task_events','tasks','org__teams','org__staff'} and r['child_column'] not in {'supervisor_id','owner_id'}:
        overview.append(f'  {r["parent_table"]} -->|"{r["status"]} {r["child_column"]}; no FK"| {r["child_table"]}')
diagram('01-source-data-erd',overview)
# Detailed ERDs show every observed field. No PK/FK constraint markers are invented.
domains={'orders':['orders','order_events'], 'support':['tickets','ticket_events','csat'], 'crm':['crm_leads','crm_lead_events'], 'workload':['tasks','task_events','staff_availability'], 'marketing':['mkt_daily','web_sessions'], 'organization':['org__units','org__teams','org__managers','org__staff','org__access_matrix'], 'configuration':['config__kpi_dictionary','config__workflow_definitions','config__monthly_targets','config__escalation_rules'], 'calendar-history':['calendar__calendar_days','calendar__events_calendar']+[t for t in tables if t.startswith(('history__','uploads__'))]}
for dom,ts in domains.items():
    lines=['erDiagram']
    for t in ts:
        lines.append('  '+t+' {')
        for c in tables[t]['columns']:
            dt=next(r['observed_type'] for r in catalog if r['table']==t and r['column']==c)
            lines.append(f'    string {c} "{dt}; observed CSV"')
        lines.append('  }')
    for r in relations:
        if r['child_table'] in ts and r['parent_table'] in ts:
            # Non-identifying links describe logical distinct keys, not enforced raw cardinalities.
            lines.append(f'  {r["parent_table"]} |o..o{{ {r["child_table"]} : "{r["status"]} {r["child_column"]}; not enforced"')
    diagram('01-source-'+dom+'-detail',lines)

# Copy the conceptual proposal rather than turn it into physical DDL.
arch=(ROOT/'docs/architecture/002-data-architecture.md').read_text(encoding='utf-8-sig')
proposed=re.search(r'```mermaid\s*(erDiagram[\s\S]*?)```',arch).group(1).strip()
diagram('02-proposed-database-erd',['---','title: PROPOSED - NOT IMPLEMENTED','---','%% All entities and edges are conceptual.',proposed])
diagram('02-proposed-layers',[
'flowchart TB','  TITLE["PROPOSED - NOT IMPLEMENTED<br/>Logical layers; no approved physical DDL"]',
'  A["Source archive<br/>SourceContract / IngestBatch / SourceFile / SourceRow"]',
'  B["Canonical history<br/>EntityObservation / EventRecord / CorrectionLink"]',
'  C["Snapshot / SnapshotInput / FactVersion<br/>snapshot_id + projection_id + business_id"]',
'  D["KpiDefinition / KpiDependency / QueryRun / KpiObservation<br/>snapshot + definition version + entity + dim + date"]',
'  E["SignalEpisode / SignalOccurrence / EvidenceRef / InsightVersion"]',
'  F["ReportVersion / DecisionEvent / ActionDraft<br/>report day + manager + run + version"]',
'  G["OrgNode / OrgEdgeVersion / AccessGrantVersion / AuthContext"]',
'  H["Security audit / Query and access log / Budget ledger / DQIncident"]',
'  A -->|PROPOSED| B','  B -->|PROPOSED| C','  C -->|PROPOSED| D','  D -->|PROPOSED| E','  E -->|PROPOSED| F','  G -.->|PROPOSED policy context| C','  G -.->|PROPOSED authorization| F','  A -.->|PROPOSED receipts| H','  D -.->|PROPOSED query audit| H','  F -.->|PROPOSED access audit| H'])

org=['flowchart TB']+legend
for m in managers:org.append(f'  {m["manager_id"]}["{m["manager_id"]}: {roles[m["manager_id"]]} / {m["scope_entity"]}<br/>level {m["level"]}; effective day {m["effective_from_day"]}"]')
for u in tables['org__units']['rows']:
    org.append(f'  {u["unit_id"]}["{u["unit_id"]}"]');org.append(f'  {u["manager_id"]} -->|CONFIRMED manages| {u["unit_id"]}')
    if u['parent_id']:org.append(f'  {u["parent_id"]} -->|CONFIRMED parent_id| {u["unit_id"]}');org.append(f'  M01 -.->|DERIVED reporting chain| {u["manager_id"]}')
for t in tables['org__teams']['rows']:
    org.append(f'  {t["team_id"]}["{t["team_id"]}<br/>day {t["effective_from_day"]}; {t["effective_from_date"]}"]');org.append(f'  {t["unit_id"]} -->|CONFIRMED contains| {t["team_id"]}');org.append(f'  {t["supervisor_id"]} -->|CONFIRMED direct supervisor| {t["team_id"]}')
    parent=next(u['manager_id'] for u in tables['org__units']['rows'] if u['unit_id']==t['unit_id']);org.append(f'  {parent} -.->|DERIVED reporting chain| {t["supervisor_id"]}')
org+=['  DATES["UNRESOLVED: first M11 report morning 75 or 76<br/>Staff E25/E26 effective day 75<br/>Validate staff effective_to_day; hierarchy is not a data grant"]','  DATES -.-> M11']
diagram('03-organization-hierarchy',org)
security=['flowchart LR']+legend+[
'  RAW["Raw CSV archive<br/>No manager raw grant supplied"]','  CALC["Internal calculator<br/>Cross-unit rows only for supplied formulas"]','  POLICY["Required boundary before any LLM<br/>Row scope + columns + purpose + active dates"]','  QUERY["Authorized query projections<br/>Text-to-SQL has the same boundary"]','  REPORT["Authorized report evidence<br/>No source row grant follows from a KPI"]','  LLM["LLM sees authorized data only"]',
'  RAW -->|DERIVED computation| CALC','  CALC -->|CONFIRMED security requirement| POLICY','  POLICY -->|CONFIRMED scoped results| QUERY','  POLICY -->|CONFIRMED scoped evidence| REPORT','  QUERY --> LLM','  REPORT --> LLM']
for m in managers:
    mid=m['manager_id'];g=grants[mid];security.append(f'  {mid}["{mid}: {g["visible_entities"]}<br/>'+('Aggregate only' if not g['individual_level_data_team'] else 'Direct-team workload: '+g['individual_level_data_team'])+'"]');security.append(f'  QUERY -->|CONFIRMED scope; aggregate by default| {mid}')
security+=['  ATT["CONFIRMED: leave/attendance only as team capacity<br/>No individual attendance display at any level"]','  ATT -.-> POLICY','  START["UNRESOLVED: M11 first report and historic marketplace window"]','  START -.-> M11']
diagram('04-management-access-graph',security)
diagram('05-column-access-overview',[
'flowchart TB',*legend,'  C["Observed source column"]','  I["REQUIRED_INTERNAL<br/>Ingestion, join, filter, or computation<br/>This is a use classification, not a display grant"]',
'  A["VISIBLE_AGGREGATED<br/>Only authorized KPI output or team capacity"]','  W["VISIBLE_DIRECT_TEAM<br/>Direct supervisor; minimum workload fields"]','  R["RESTRICTED<br/>Document purpose, scope, and redaction first"]','  D["DENIED<br/>Upper-manager employee details<br/>Individual attendance at all levels"]','  U["UNRESOLVED<br/>No precise source-column grant"]',
'  C --> I','  C -->|DERIVED authorized output mapping| A','  C -->|DERIVED direct workload mapping| W','  C --> R','  C -->|CONFIRMED privacy rule| D','  C --> U','  S["M01-M04: aggregates only<br/>M05-M11: direct-team workload exception<br/>All: no raw grant inferred; no attendance monitoring"]','  S -.-> A','  S -.-> W'])
line=['flowchart LR']+legend
for t in ['orders','order_events','tickets','ticket_events','csat','crm_leads','crm_lead_events','tasks','task_events','mkt_daily','web_sessions','cal','monthly_targets']:line.append(f'  {t}["{t}: source relation"]')
view_parents={'order_fact':['orders','order_events'],'ticket_fact':['tickets','ticket_events'],'lead_fact':['crm_leads','crm_lead_events'],'task_fact':['tasks','task_events'],'revenue_daily':['orders','order_events','lead_fact','cal']}
view_keys={'order_fact':'order_id','ticket_fact':'ticket_id','lead_fact':'lead_id; drop_day correction selection','task_fact':'task_id','revenue_daily':'order_id; date; channel and event filters'}
for v,ps in view_parents.items():
    line.append(f'  {v}["{v}: reference SQL view"]')
    for p in ps:line.append(f'  {p} -->|DERIVED computation| {v}')
    line.append(f'  {ps[0]} -->|"DERIVED join/filter: {view_keys[v]}"| {v}')
for entity in sorted({k['entity_id'] for k in kpis}):
    ks=[k for k in kpis if k['entity_id']==entity];node='K_'+entity;line.append(f'  {node}["{len(ks)} KPI definitions: {entity}"]');line.append(f'  {entity}["{entity}: KPI entity"]');line.append(f'  {node} -->|CONFIRMED entity_id| {entity}')
    for v in sorted(set.union(*(direct_relations[k['kpi_id']] for k in ks))):line.append(f'  {v} -->|DERIVED computation| {node}')
    for m in managers:
        if entity in grants[m['manager_id']]['visible_entities'].split('|'):line.append(f'  {entity} -.->|CONFIRMED aggregate display scope| {m["manager_id"]}')
diagram('06-kpi-data-lineage',line)
for entity in sorted({k['entity_id'] for k in kpis}):
    lines=['flowchart LR']+legend;ks=[k for k in kpis if k['entity_id']==entity]
    sources=set.union(*(exec_sources[k['kpi_id']] for k in ks));usedviews=set.union(*(direct_views[k['kpi_id']] for k in ks))
    if 'revenue_daily' in usedviews:usedviews.add('lead_fact')
    for t in sorted(sources):lines.append(f'  {t}["{t}: calculation input"]')
    for v in sorted(usedviews):
        lines.append(f'  {v}["{v}: SQL view"]')
        for p in view_parents[v]:lines.append(f'  {p} -->|DERIVED execution input| {v}')
        lines.append(f'  {view_parents[v][0]} -->|"DERIVED join/filter: {view_keys[v]}"| {v}')
    for k in ks:
        kid=k['kpi_id'];lines.append(f'  {kid}["{kid}"]')
        for t in sorted(direct_relations[kid]):lines.append(f'  {t} -->|DERIVED computation| {kid}')
        for t,cols in sorted(join_columns[kid].items()):
            if cols:lines.append(f'  {t} -->|"DERIVED join/population: {", ".join(sorted(cols))}"| {kid}')
        lines.append(f'  {kid} -->|CONFIRMED entity_id| {entity}')
    for m in managers:
        if entity in grants[m['manager_id']]['visible_entities'].split('|'):lines.append(f'  {entity} -.->|CONFIRMED aggregate display; active dates apply| {m["manager_id"]}')
    diagram('06-lineage-'+entity,lines)

md('proposed-entity-contracts.md','''# Proposed entity contracts

All entities in Diagram B are PROPOSED - NOT IMPLEMENTED. The source is `../002-data-architecture.md`, sections 1 and 2. This file does not approve physical tables or constraints.

| Entity | Defined identity or grain | Defined links and limits |
|---|---|---|
| Dataset | dataset_id | Namespace for source business identifiers. |
| SourceContract | source_id + contract_version | Source schema, schedule, and accepted mappings. |
| IngestBatch | One delivery acceptance attempt | previous_batch_id connects retries or revisions. No primary key name is specified. |
| SourceFile | One file occurrence | Batch receives files. Hash alone is not occurrence identity. |
| SourceRow | file_occurrence_id + csv_record_ordinal | Preserves original payload. |
| EntityObservation | One entity payload observation | source_row_id; business_id is not a raw occurrence key. |
| EventRecord | event_record_id | source_row_id and business_id; repeated events remain possible. |
| CorrectionLink | One correction relationship | source_row_id; conflicting correction precedence is open. |
| Snapshot | One frozen input and policy set | snapshot_id is used by downstream facts and observations. |
| SnapshotInput | A selected input in a snapshot | SourceFile and Snapshot links; final join key is unspecified. |
| FactVersion | snapshot_id + projection_id + business_id | Rebuildable fields and contributor references. |
| KpiDefinition | kpi_id + definition_version | Supplied definition and original SQL hash. |
| KpiDependency | One declared dependency | Definition link; physical key is unspecified. |
| QueryRun | One recorded calculation or query | Snapshot link; final primary key contract is unspecified. |
| KpiObservation | snapshot_id + definition_version + entity_id + dim_key + business_date | QueryRun and definition links. |
| EvidenceRef | One evidence reference | KPI observation support; no final physical key. |
| SignalEpisode / SignalOccurrence | Episode and occurrence | Proposal specifies a one-to-many conceptual link. |
| InsightVersion / ReportVersion | Versioned insight and report | Many-to-many concept; join-table schema is not defined. |
| ReportVersion | report_day + manager_id + run_id + version | Snapshot, policy, validation, and supersedes references. |
| DecisionEvent / ActionDraft | Decision event and draft | Report informs decisions; decision proposes drafts. |
| OrgNode / OrgEdgeVersion | Organization node and dated edge | AccessGrantVersion scopes nodes. Final keys remain unspecified. |
| AuthContext / access log / budget ledger | Security context and records | Logical security layer only; no final DDL. |
| DQIncident / ExpectedDelivery | Data issue and expected delivery | A missing delivery can have an issue without a SourceFile. |

The conceptual crow's-foot links come from the existing proposal. They are not observed source constraints. PostgreSQL storage, SQLite calculation, final DDL, indexes, security roles, retention, and many-to-many join tables require team review.
''')

md('security-examples.md','''# Security examples

These examples describe requirements and candidate projections. They do not create grants. Evidence: `dataset/org/access_matrix.csv`, the original brief pages 6, 10, 12, and 13, and each cited KPI SQL. Source paths are relative to the project root.

## M07: Warehouse supervisor

CONFIRMED: M07 can see T_WH KPIs and direct-team workload. DERIVED: the minimum workload projection can use `tasks.task_id`, `tasks.team_id`, `tasks.owner_id`, `tasks.created_at`, and `tasks.due_date`. Compute completion from `task_events.task_id`, `task_events.event`, and `task_events.at`, using `task_fact.done_at`. The row condition is `tasks.team_id = 'T_WH'`. Join `tasks.owner_id = staff.staff_id` and verify that `staff.team_id = 'T_WH'` at the applicable date. These are candidate query conditions derived from observed keys. The physical enforcement design is PROPOSED. For an as-of date, use the supplied overdue SQL time conditions, or define a separate approved open-work query. Do not count all historical tasks as open.

RESTRICTED: `tasks.title_fa` and `tasks.blocker_fa` can support work allocation, but exact text can contain personal data. A redaction policy is UNRESOLVED. Q10 requests open work per warehouse member. It does not grant access to other teams.

DERIVED internal calculation: warehouse KPIs use `orders.order_id`, `orders.category`, and selected event timestamps from `order_events.order_id`, `event`, and `at`. `K_WH_DAMAGE_BY_CAT_7D` joins `tickets.order_id = orders.order_id`, filters `tickets.category = 'کالای معیوب'`, and groups by the order product category. This is a cross-team calculation. `K_WH_INSPECT_MED` uses first-response and inspection times from `ticket_fact`. Its supplied SQL has no `team_id = 'T_WH'` filter. Do not add that filter to the formula or grant source tickets to M07. Return the authorized warehouse KPI result.

`tickets.text_fa`, `ticket_events.staff_id`, `orders.customer_id`, unrelated support cases, and other-team workload have no warehouse display grant. Keep them out of the M07 projection. Availability `staff_id` and `status` stay internal; release team capacity only. No supplied KPI uses staff_availability. A capacity formula remains UNRESOLVED.

## M03: Operations manager

CONFIRMED: allowed KPI entities are U_OPS, T_WH, and T_SHP. M03 can receive on-time delivery, picking time, warehouse damage rate, shipping metrics, and aggregate overdue counts. DERIVED: internal calculation may read task ownership to validate scope, but the result must remove `tasks.owner_id`, `staff.staff_id`, `staff.name_fa`, and `ticket_events.staff_id`. Do not group results by an employee or return a row per employee. Q11 asks for warehouse workload per person. Refuse that individual view and offer a team total. A query request cannot expand the access matrix.

PROPOSED: a reviewed aggregate projection can group work by `tasks.team_id` and business date. Exact small-group suppression limits are UNRESOLVED. A team label does not make a one-person aggregate safe.

## M01: Executive manager

CONFIRMED: the matrix includes ORG, all three units, and all seven teams. This permits organization-wide aggregate reporting, including the 55 KPI definitions, subject to team activation. It does not permit employee-level data. Remove employee identifiers from query results, evidence snippets, reports, and LLM input. Do not use employee-level pseudonyms as a substitute. Team capacity is permitted as an aggregate purpose; individual leave is prohibited. Exact capacity calculation, minimum group size, and extra drill-down columns remain UNRESOLVED.

## M11: Marketplace supervisor

CONFIRMED: the scope is T_MKT only. `K_MKT_ORDERS` filters `orders.channel = 'marketplace'`. `revenue_daily.marketplace` uses the same channel condition within the revenue calculation. The order-event calculation joins `order_events.order_id = orders.order_id`. `K_TASK_OVERDUE_T_MKT` uses `tasks.team_id = 'T_MKT'`. DERIVED: these conditions support separate marketplace aggregate and workload projections. They do not grant all Sales data. Q06 requests company revenue; ORG is outside M11 scope.

CONFIRMED: managers, teams, and E25/E26 start on day 75. UNRESOLVED: the first report is morning 75 under static dates or morning 76 under next-morning input effect. The date `2026-10-05` is supplied. The historic marketplace window also needs an explicit policy. Q05 says since team activity began. Do not grant all prior marketplace history by default. A `created_at >= '2026-10-05'` condition is a PROPOSED interpretation for that question, not a general revenue rule: refunds and paid events can refer to older orders.

## Shared orders

DERIVED: Sales uses `orders.order_value_toman`, `order_events.amount_toman`, paid/refunded events, and channel for revenue and conversion KPIs. Operations uses `orders.promised_by`, `orders.city`, `orders.category`, and selected event times for operational KPIs. Marketplace uses channel-filtered order counts and net revenue. Different KPI outputs can use the same source rows.

CONFIRMED: each output must belong to an allowed KPI entity. No `orders.team_id` exists. `order_events.actor_team` identifies an event actor; it is not an order-ownership grant. No source customer table exists for `orders.customer_id`. The exact physical source-row projection for unrestricted questions is UNRESOLVED. Use the supplied KPI formulas internally and show only allowed results. Do not expose order financial rows to Operations merely because Operations needs delivery metrics.

## Query and report boundary

CONFIRMED requirement: enforce scope and purpose in the data layer for every query, including Text-to-SQL. Apply the boundary before data enters an LLM. The same limits apply to reports, evidence, exports, and saved query results. A scoped KPI result and its raw contributors have different access rules. PROPOSED mechanism: separate calculator service identity from manager query roles and use reviewed projections. No such mechanism is implemented by this documentation.
''')

md('open-questions.md','''# Open questions and review points

No item below changes the supplied access matrix or an existing architecture decision.

| ID | Status | Question or review point | Evidence | Review owner |
|---|---|---|---|---|
| Q01 | UNRESOLVED | Is M11 first active for a report on morning 75 or 76? Static start is day 75. The next-morning input rule conflicts with it. | managers.csv; teams.csv; scripted_inputs IN05; README; ADR-08 | Project owner |
| Q02 | UNRESOLVED | Which historic marketplace rows can M11 query? How does “since activity began” apply to paid/refund dates and old orders? | Q05; K_MKT_ORDERS; K_MKT_REV | Data and security owners |
| Q03 | UNRESOLVED | Define exact allowed raw text fragments for direct-team title/blocker evidence. Define customer-data redaction. No general raw-column grant exists. | Brief pp.10,12,13; tasks and tickets headers | Security owner |
| Q04 | UNRESOLVED | Define source-row projections for shared orders and cross-team tickets for queries beyond supplied KPI results. No order team key exists. | reference SQL; access matrix | Data and security owners |
| Q05 | UNRESOLVED | Define team capacity from availability status, working days, and staff effective dates. Specify minimum group size and prevention of individual inference. | Brief pp.6,12,13; staff_availability; calendar | Product and security owners |
| Q06 | UNRESOLVED | Confirm accepted RAW or exact-payload dedup input for orders. Current duplicate keys can multiply joins. | day_076; KPI-VAL-001; ADR-02 | Project owner |
| Q07 | PROPOSED | Review PostgreSQL storage plus SQLite reference calculation, types, RLS, query roles, and safe projection design. | Architecture 001-003; ADR-01,06 | Engineering and security team |
| Q08 | PROPOSED | Complete physical keys, nullable FKs, indexes, many-to-many tables, and audit access for the conceptual model. | Architecture 002 section 2 | Data architecture team |
| Q09 | UNRESOLVED | Define missing-delivery publication, source closure, correction ties, restatement, retention, and source-calendar known-at rules. | ADR-04,05,08,11,12 | Project and architecture owners |
| Q10 | UNRESOLVED | A complete official raw data dictionary is absent. Customer/campaign registries and event occurrence IDs are absent. Do not invent their FKs. | Observed CSV headers; brief p.14 | Source owner |

CONFIRMED restrictions are not open questions: upper managers receive aggregates only; direct supervisors have a workload-purpose exception for their team; attendance is not for individual monitoring; every query is scoped before LLM access. A dependency never creates a permission.
''')

# The check covers generated syntax structure. A Mermaid renderer is not available locally.
checks=[]
for p in OUT.glob('*.mmd'):
    s=p.read_text(encoding='utf-8');assert s.count('[')==s.count(']'),p.name;assert s.count('{')==s.count('}') or 'erDiagram' in s,p.name
    assert 'flowchart' in s or 'erDiagram' in s
    checks.append({'file':p.name,'structural_check':'PASS','mermaid_parser':'NOT RUN: no local Mermaid package or CLI found','svg':'NOT CREATED'})
write_csv('diagram-validation.csv',checks)
assert {r['manager_id'] for r in access}=={m['manager_id'] for m in managers}
assert len(access)==len(catalog)*11
assert {r['kpi_id'] for r in lineage}=={k['kpi_id'] for k in kpis}
assert not any(r['column_visibility']=='VISIBLE_DIRECT_TEAM' and int(r['management_level'])<=2 for r in access)
assert not any(r['source_table']=='staff_availability' and r['column']=='status' and r['column_visibility'] in {'VISIBLE_DIRECT_TEAM','VISIBLE_AGGREGATED'} for r in access)
for path,h in baseline.items():assert sha(ROOT/path)==h,'Source changed: '+path
stats=dict(tables=len(tables),table_column_pairs=len(catalog),csv_files=len(inventory),drop_csv_files=sum('/drops/' in x['path'] for x in inventory),json_files=len(json_inventory),diagrams=len(checks),svg_files=0,kpis=len(kpis),managers=len(managers),access_entries=len(access),relationships=len(relations),confirmed_relationships=sum(r['status']=='CONFIRMED' for r in relations),derived_relationships=sum(r['status']=='DERIVED' for r in relations),enforced_foreign_keys=0,protected_existing_files=len(baseline),protected_hashes_unchanged=True,mermaid_status='Structural checks only; parser/render unavailable; no packages installed and no network service used',sql_status='All 55 original statements compiled with SQLite EXPLAIN against five original views; no KPI results calculated')
(OUT/'validation-summary.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
write_csv('protected-file-hashes.csv',[dict(path=p,sha256=h) for p,h in baseline.items()])
md('README.md',f'''# ARKA / DIDRAH diagrams and access evidence

This collection describes source files, a proposed model, and required access limits. It does not implement a database or approve an open decision. Review date: 2026-11-03, Asia/Tehran.

## Read the diagrams

| Main diagram | Meaning | Companion detail |
|---|---|---|
| [01-source-data-erd.mmd](01-source-data-erd.mmd) | Observed CSV families and selected relations | Eight `01-source-*-detail.mmd` ERDs; catalog, profiles, and relationship evidence |
| [02-proposed-database-erd.mmd](02-proposed-database-erd.mmd) | Existing conceptual proposal, copied with proposal warning | [Layers](02-proposed-layers.mmd); [entity contracts](proposed-entity-contracts.md) |
| [03-organization-hierarchy.mmd](03-organization-hierarchy.mmd) | Unit/team assignments and derived manager reporting chain | manager-access-summary.csv; effective dates |
| [04-management-access-graph.mmd](04-management-access-graph.mmd) | Internal calculation and authorized query/report paths | [Worked examples](security-examples.md) |
| [05-column-access-overview.mmd](05-column-access-overview.mmd) | Column use and visibility classes | access-matrix-detailed.csv |
| [06-kpi-data-lineage.mmd](06-kpi-data-lineage.mmd) | Sources, five views, KPI entity groups, manager display scope | Eleven `06-lineage-*.mmd` domain diagrams; all 55 KPI records |

There are {len(checks)} Mermaid files. No SVG file was created. No suitable local Mermaid renderer was found. No dependency was installed and no network service was used. Structural checks passed. A Mermaid parser and visual layout check remain pending. The large lineage overview is an index; use the entity diagrams for detailed reading.

## Evidence labels and arrows

- CONFIRMED means a source file or an official requirement states the fact.
- DERIVED means SQL, identifier matches, or measured records support the link. It is not an enforced FK or a new grant.
- PROPOSED means a design needs review. Every entity and edge in Diagram B has this status.
- UNRESOLVED means evidence does not establish an exact answer.

In Diagram A, an arrow connects a parent key to a child reference. A domain ERD uses a dotted, non-identifying link. Its `0..1` parent and `0..many` child notation describes a candidate distinct-entity model. Read measured multiplicities and missing keys in relationship-evidence.csv. These symbols do not assert raw uniqueness or mandatory parents. Raw orders contain duplicates. No CSV relationship is enforced by a database.

In Diagram B, crow's-foot arrows reproduce the existing conceptual proposal. They do not describe installed tables or approved physical constraints. SourceFile to DQIncident has the proposal's limitation: a missing delivery can have an incident without a file.

In Diagram C, solid arrows show supplied assignments. Dotted arrows show a manager reporting chain derived through unit/team structure. Neither arrow is an access grant. In Diagram D, arrows show required information boundaries. They do not claim that security controls already exist. In Diagram E, computation use and display classification are independent axes. In Diagram F, solid arrows show computation, joins, or filters. Dotted entity-to-manager arrows show aggregate display scope from the access matrix. They never permit underlying source rows.

## Actual tables and columns

Inspected {len(inventory)} CSV files, including {stats['drop_csv_files']} drops, with {len(tables)} file families and {len(catalog)} distinct table/column pairs. Read all records for type shapes, nulls, key repeats, and joins. CSV has no declared SQL type. Observed lexical types do not choose a database storage type.

table-column-catalog.csv retains exact column names. It includes both `tickets.created_at` and `tickets.create_time`, and both `ticket_events.at` and `ticket_events.event_time`. An absent field after a header change is separate from an empty cell. The documented reference aliases are `create_time -> created_at`, `event_time -> at`, and `calendar_days.date -> cal.d`. `crm_lead_events.drop_day` is ingestion metadata required by reference SQL. It is not an observed CSV column.

table-profiles.csv reports candidate key repeats, exact repeats, file counts, and grains. Event tables have no supplied event occurrence ID. Do not use a business entity ID as an event PK. Daily observations are not a supplied persistent snapshot table. `orders.order_id` is not a reliable raw PK. Unique keys observed in this package remain candidates, not guarantees for hidden data. Customer and campaign IDs have no supplied parent registry. Marketing source strings do not prove a lead-to-advertising attribution FK.

relationship-evidence.csv contains {len(relations)} checked links: {stats['confirmed_relationships']} CONFIRMED assignments and {stats['derived_relationships']} DERIVED joins or identifier/date matches. All are unenforced. Full-data matching does not prove as-of-day completeness or effective-date validity. No relationship is asserted merely because two columns have the same name. The field `order_events.actor_team` refers to both team IDs and the unit ID `U_SAL`. Its checked parent domain is the union of units and teams. It is not a team-only FK. There are 5,017 empty `tickets.order_id` cells and 1,539 empty `ticket_events.staff_id` cells. Keep these optional references; do not make up parent records.

## Access matrix

access-matrix-detailed.csv contains {len(access)} records: every observed column for every manager. The records include scope, use, KPI dependencies, row conditions, query/report visibility, masking, evidence, and status. manager-access-summary.csv gives all 11 manager scopes and permitted KPI IDs.

`internal_use=REQUIRED_INTERNAL` is separate from `column_visibility`. A required input can be DENIED for display. VISIBLE_AGGREGATED means only the supplied authorized KPI result or the stated capacity purpose. It does not allow a manager to select the source column. VISIBLE_DIRECT_TEAM applies only to minimum workload fields for the direct supervisor. RESTRICTED requires an added documented condition. DENIED expresses a prohibited exposure. UNRESOLVED is not permission. Individual attendance status is never an authorized manager result; internal status can support team capacity only.

No raw-table grant was supplied. The matrix does not assert that all raw data is explicitly prohibited by name. It records the missing grant and prevents permission from being inferred. Candidate physical projections and predicate enforcement remain PROPOSED. The exact field mapping has DERIVED or UNRESOLVED status unless an official rule specifies it. No precise raw-column allowlist is present in the brief or CSV matrix.

M01-M04 have no employee-level exception. M05-M11 can use individual data only for direct-team workload. A supervisor cannot see individual leave under that exception. Do not expose unredacted task or ticket text without a purpose and redaction policy. Cross-team KPI computation runs under an internal service boundary; its result is authorized by KPI entity. [Security examples](security-examples.md) explain M07, M03, M01, M11, and shared orders.

## KPI lineage method

All 55 original KPI SQL statements compile with SQLite EXPLAIN against the five original views in an isolated memory schema. No source row was changed and no KPI result was generated in this task. sql-execution-column-reads.csv records prepare-time reads, including `o.*` and `t.*` expansion. Such reads can include unused fields. They are execution dependencies, not selected value lineage or display rights.

kpi-source-manager-mapping.csv separates execution sources from selected value and population sources. Selected view fields are expanded to their source fields. This expansion is conservative where identical field names occur in multiple relations. It is not a proof of a minimum invalidation set. The supplied SQL remains in each record for review. For revenue, selecting b2b does not make order amounts value inputs; selecting b2c or marketplace does not make CRM amounts value inputs. The full revenue view still needs all its relations to compile. The calendar spine can control row presence even when it does not supply an amount.

Each KPI owns the entity stated in the dictionary. A manager can display its aggregate result only if that entity occurs in visible_entities. owner_manager_id identifies signal ownership; it is not the only permitted aggregate viewer. The escalation rules do not grant new source access. None of the 55 definitions uses staff_availability. Capacity is a separate permitted purpose with an unresolved formula.

## Time and known limits

Use only deliveries through R-1 for morning R. Build facts after the cutoff. A filter on a full-history final fact does not prevent future information. Validate active manager, team, and staff records. M11, T_MKT, E25, and E26 have supplied day-75 starts. The first report morning and historic marketplace scope remain open. No diagram treats all 11 managers as active for the entire replay.

Staff assignments have effective dates, but not all temporary changes have a row-level dated transfer record. A decision text is not a replacement staff assignment. Calendar event timing and historic access need a known-at policy. The inherited architecture keeps these review points open.

## Validation and source protection

See validation-summary.json and diagram-validation.csv. All observed headers are catalogued. All 55 SQL statements and all 11 manager scopes are covered. Checks reject direct-team visibility for levels 1 and 2 and reject individual availability status display. All {len(baseline)} protected existing files outside .venv retained their SHA-256 hashes. protected-file-hashes.csv provides the baseline. All new output is in this directory. Existing architecture, source CSVs, SQL, JSON, PDF, audits, and notebooks remain unchanged. No commit or push was made.

The original 19-page PDF was read with the existing bundled pypdf package. Key access requirements were rechecked on pages 6, 10, 12, and 13. Supporting files include all three architecture documents, DATA_MAP_FA.md, exploration relationship evidence, DQ-001, KPI-VAL-001, and the technical review. The supplied matrix and brief take priority over proposals. PDF text extraction preserves imperfect Persian order; this collection uses the explicit requirements cross-checked with the source matrix and README. No new architectural decision was finalized.

For unresolved policy and design work, read [open-questions.md](open-questions.md). This is the stop point for this task.
''')
print(json.dumps(stats,indent=2))
