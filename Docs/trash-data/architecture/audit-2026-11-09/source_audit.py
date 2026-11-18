"""Read-only source inspection and documentation tables. Does not execute SQL."""
from audit_support import ROOT, OUT, read
from pathlib import Path
from collections import Counter, defaultdict
import csv
import hashlib
import json
import re
from datetime import date, timedelta

def rows(path):
    with (ROOT / path).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))

def emit(name, records):
    with (OUT / name).open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)

def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

K = rows('dataset/config/kpi_dictionary.csv')
rules = rows('dataset/config/escalation_rules.csv')
stages = rows('dataset/config/workflow_definitions.csv')
inputs = json.loads(read('dataset/manager_inputs/scripted_inputs.json'))
assert len(K) == 55 and len({k['kpi_id'] for k in K}) == 55
assert [r['rule_id'] for r in rules] == [f'R{i}' for i in range(1, 9)]
assert len(stages) == 12

families = defaultdict(lambda: defaultdict(list))
manifest_checks = []
raw_counts = Counter()
for folder in sorted((ROOT / 'dataset/drops').iterdir()):
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    actual = {}
    for p in sorted(folder.glob('*.csv')):
        with p.open(encoding='utf-8-sig', newline='') as f:
            r = csv.DictReader(f)
            header = tuple(r.fieldnames)
            count = sum(1 for _ in r)
        families[p.name][header].append(manifest['drop_day'])
        actual[p.name] = count
        raw_counts[p.name] += count
    manifest_checks.append(dict(path=(folder / 'manifest.json').relative_to(ROOT).as_posix(),
        drop_day=manifest['drop_day'], date=manifest['date'], declared=manifest['files'],
        actual=actual, matches=actual == manifest['files']))
assert len(manifest_checks) == 91 and all(r['matches'] for r in manifest_checks)

headers = []
for family, versions in sorted(families.items()):
    for header, days in versions.items():
        headers.append(dict(family=family, header=list(header), first_drop=min(days),
                            last_drop=max(days), delivery_count=len(days)))
orders = rows('dataset/drops/day_076/orders.csv')
counts = Counter(tuple(r.items()) for r in orders)
correction_rows = []
for day in [64, 70]:
    path = f'dataset/drops/day_{day:03d}/crm_lead_events.csv'
    for number, r in enumerate(rows(path), 2):
        if r['lead_id'] == 'L02045':
            correction_rows.append(dict(source=path, record=number, **r))
late_support = {}
for name in ['tickets.csv', 'ticket_events.csv', 'csat.csv']:
    r = rows('dataset/drops/day_067/' + name)
    field = {'tickets.csv': 'created_at', 'ticket_events.csv': 'at', 'csat.csv': 'answered_at'}[name]
    late_support[name] = dict(Counter(x[field][:10] for x in r))
calendar = rows('dataset/calendar/calendar_days.csv')
calendar_by_day = {int(r['day_idx']): r for r in calendar}
assert len(calendar_by_day) == len(calendar) == 90
assert sorted(calendar_by_day) == list(range(1, 91))
dates = [date.fromisoformat(calendar_by_day[i]['date']) for i in range(1, 91)]
assert all(b-a == timedelta(days=1) for a, b in zip(dates, dates[1:]))
assert all(m['date'] == calendar_by_day[m['drop_day']]['date'] for m in manifest_checks if m['drop_day'])
events = rows('dataset/calendar/events_calendar.csv')

# Verify every catalog metadata field, not only its ID count.
catalog = read('docs/architecture/002-data-architecture.md').split('<!-- KPI_CATALOG_START -->')[1].split('<!-- KPI_CATALOG_END -->')[0]
catalog_rows = {}
for line in catalog.splitlines():
    if not re.match(r'^\| `K_', line):
        continue
    cells = [c.strip() for c in line.strip('|').split('|')]
    key = re.search(r'`(K_[A-Z0-9_]+)`', cells[0])[1]
    catalog_rows[key] = cells
for record, k in enumerate(K, 2):
    c = catalog_rows[k['kpi_id']]
    assert c[0].endswith(str(record)), k['kpi_id']
    assert c[1] == f"`{k['entity_id']} / {k['owner_manager_id']}`", k['kpi_id']
    assert c[2] == f"{k['unit']}؛ `{k['dim'] or 'none'}`", k['kpi_id']
    assert c[3] == f"`{k['direction']}; {k['rule']}; esc={k['escalate_after_days']}`", k['kpi_id']
    assert c[4] == '`' + ' / '.join(k[x] or '-' for x in ['target', 'warn', 'crit']) + '`', k['kpi_id']
assert set(catalog_rows) == {r['kpi_id'] for r in K}

S = {}
def spec(ids, clock, window, meaning, boundary):
    for key in ids.split():
        assert key not in S, key
        S[key] = dict(output_clock=clock, window=window, formula_population=meaning,
                      row_null_and_population_boundary=boundary)

spec('K_ORG_NET_REV', 'cal.d; paid/refunded event date and won date', 'daily',
     'ROUND((b2c+b2b)/1e6,1); revenue_daily calendar spine.',
     'Raw order joins affect B2C; corrections replace B2B value on won date; canonical COALESCE zeros do not prove completeness.')
spec('K_ORG_REV_MTD_ATTAIN', 'cal.d and jmonth', 'Jalali MTD through c.d',
     'Cumulative b2c+b2b divided by ORG monthly target prorated by day_in_month/mdays; percent ROUND 1.',
     'Inner target join requires matching jmonth/scope; use supplied month length; R8 gates alerting, not calculation.')
spec('K_ORG_ONTIME K_OPS_ONTIME K_SHP_ONTIME', 'date(delivered_at)', 'daily delivered population',
     '100*AVG(delivered_at<=promised_by), ROUND 1; order_fact with non-NULL delivered_at.',
     'Missing promised_by produces SQL NULL in the boolean expression; preserve AVG NULL behavior. No delivered group means no row.')
spec('K_ORG_CSAT K_SUP_CSAT', 'date(answered_at)', 'daily',
     'AVG(score), ROUND 2, directly from csat.',
     'No tickets/event join. No group is not zero. Repeated IDs in another source do not create a visibility grant.')
spec('K_ORG_FRT_MED K_SUP_FRT_MED K_RSP_FRT_MED', 'date(first_response_at)', 'daily first-response population',
     'Median((julianday(first_response_at)-julianday(created_at))*24), ROUND 2; T_RSP and non-NULL first response.',
     'ticket_fact uses MIN first response. Preserve NULL samples and time rounding. Three canonical IDs are not three independent witnesses.')
spec('K_ORG_ORDERS', 'cal.d; date(orders.created_at)', 'daily calendar spine',
     'COUNT(o.order_id) from calendar LEFT JOIN orders.',
     'Counts raw accepted occurrences; a known empty day can be zero. Future calendar rows are not publishable facts.')
spec('K_WF1_SLA', 'date(delivered_at)', 'daily delivered population',
     '100*AVG(paid-created<=1h AND picked-paid<=12h AND handed_over-picked<=6h AND delivered<=promised_by), ROUND 1.',
     'Preserve three-valued AND/AVG semantics. Canonical KPI excludes the follow-up stage; stage targets are separate.')
spec('K_WF2_SLA K_CMP_RES_48H_PCT', 'date(resolved_at)', 'daily resolved T_CMP population',
     '100*AVG((resolved_at-created_at)<=48h), ROUND 1.',
     'Do not sum 8/36/24 stage SLA. ticket_fact uses MAX resolved; current reopen state is separate.')
spec('K_WF3_SLA_7D', 'cal.d with date(COALESCE(won_at,lost_at))', 'inclusive c.d-6 through c.d',
     'Closed-lead AVG of first_contact-created<=24h AND proposal-qualified<=120h AND close-proposal<=720h, percent ROUND 1.',
     'No WF3.2 72h predicate. COALESCE prefers won_at. Preserve NULL boolean handling and inner-window no-row behavior.')
spec('K_SAL_B2C_REV', 'revenue_daily.d from paid/refunded dates', 'daily',
     'ROUND(b2c/1e6,1); net online paid order amount minus refund event amount.',
     'Not gross sales and not organization B2C+B2B. Raw order multiplicity affects joins.')
spec('K_SAL_CONV', 'sessions.date joined to date(orders.created_at)', 'daily',
     '100*raw order COUNT(*) / daily SUM(sessions), ROUND 2.',
     'Inner join of daily groups. No denominator guard is present in source SQL; zero/NULL behavior must match the reference port.')
spec('K_SAL_PAYFAIL', 'date(created_at)', 'daily order_fact population',
     '100*AVG(failed_at IS NOT NULL), ROUND 2.',
     'MAX failure timestamp in order_fact; late events can restate creation-date metrics. Not a count of failure events.')
spec('K_SAL_PAYFAIL_BY_CH', 'date(created_at), channel', 'daily per channel',
     '100*AVG(failed_at IS NOT NULL), ROUND 2, grouped by date/channel.',
     'Use source channel dimension, not team ownership inferred from the table.')
spec('K_ENT_FC_SLA', 'date(first_contact_at)', 'daily first-contact population',
     '100*AVG(first_contact-created<=24h), ROUND 1; non-NULL first_contact.',
     'Initial CRM dates before calendar are valid. There is no extra source/team filter in canonical SQL.')
spec('K_ENT_WINRATE_30D', 'cal.d and closed date COALESCE(won_at,lost_at)', 'inclusive c.d-29 through c.d',
     '100*AVG(won_at IS NOT NULL) among closed leads, ROUND 1.',
     'No closed group means no row. New source breakdown is a separately registered query, not a change to this canonical SQL.')
spec('K_ENT_PIPELINE', 'cal.d', 'state at calendar date',
     'COUNT(leads with proposal date<=d and no close or close date>d), calendar LEFT JOIN.',
     'Uses proposal state, not every open lead. Date equality at close removes the lead that day.')
spec('K_ENT_CONTRACT_MTD', 'cal.d/jmonth and won date', 'Jalali MTD',
     'Cumulative revenue_daily.b2b by jmonth /1e6, ROUND 1.',
     'info only: display, no alert. Corrections revise won-date buckets; calendar spine controls the output set.')
for team in ['ENT','DIG','MKT','WH','SHP','RSP','CMP']:
    spec('K_TASK_OVERDUE_T_' + team, 'cal.d; created/due/done dates', 'daily end-date state',
         f"COUNT(task_fact for T_{team} with due_date<d and created_date<=d and done NULL or done_date>d).",
         'Calendar LEFT JOIN; done on date d removes the task on d. Preserve MAX done. Team name does not imply ticket dependency.')
spec('K_DIG_LEADS', 'mkt_daily.date', 'daily', 'SUM(leads) across advertising sources.',
     'No calendar spine; absent daily group is not a generated zero.')
spec('K_DIG_CPL_7D', 'cal.d with mkt_daily.date', 'inclusive c.d-6 through c.d',
     'SUM(spend)/NULLIF(SUM(leads),0)/1000.0, ROUND 0; thousand toman.',
     'Sum divided by sum, not mean daily CPL. Preserve integer division before /1000.0 and zero-denominator NULL.')
spec('K_DIG_SPEND', 'mkt_daily.date', 'daily', 'SUM(spend_toman)/1e6, ROUND 1.',
     'info only; no alert. No source group means no row.')
spec('K_MKT_ORDERS', 'date(orders.created_at)', 'daily marketplace',
     "COUNT(*) with channel='marketplace'.", 'No calendar zero-fill. Active manager and historical entitlement are separate from calculation.')
spec('K_MKT_REV', 'revenue_daily.d from paid/refunded dates', 'daily marketplace',
     'ROUND(marketplace/1e6,1) only WHERE marketplace<>0.',
     'Zero-total dates are absent rows by definition, not missing-source proof. info only. Receipt and historical entitlement still apply.')
spec('K_OPS_PICK_MED K_WH_PICK_MED', 'date(picked_at)', 'daily picked population',
     'Median((picked_at-paid_at) in reference Julian hours), ROUND 2; non-NULL picked.',
     'No extra team predicate in SQL. Duplicate canonical definitions are not independent cause evidence.')
spec('K_WH_PICK_12H_PCT', 'date(picked_at)', 'daily picked population',
     '100*AVG(picked-paid<=12h), ROUND 1.', 'Preserve NULL start-time behavior and SQL boolean population.')
spec('K_WH_BACKLOG', 'cal.d at 22:00:00', 'point-in-time backlog',
     'COUNT(order_fact paid<=cutoff, cancelled NULL or >cutoff, picked NULL or >cutoff).',
     'Equality at picked/cancelled cutoff excludes the row. Do not use day-end 23:59 or current lifecycle.')
spec('K_WH_DAMAGE_RATE', 'cal.d; ticket created and order delivered dates', 'daily',
     '100*COALESCE(defective-ticket count,0)/delivered-order count, ROUND 2.',
     'Inner denominator group and LEFT numerator. Not a same-order cohort rate. Missing numerator source is not proved zero.')
spec('K_WH_DAMAGE_BY_CAT_7D', 'cal.d and order product category', 'inclusive c.d-6 through c.d',
     'Defective tickets JOIN raw orders by order_id for product category; numerator sum / delivered order_fact count sum, percent ROUND 2.',
     'Raw duplicate orders can multiply numerator joins. Category is order category, not ticket category. No denominator group means no row.')
spec('K_WH_INSPECT_MED', 'date(inspected_at)', 'daily inspected population',
     'Median(inspected-first_response in reference Julian hours), ROUND 2.',
     'No team=T_WH predicate in SQL. Preserve MAX inspection/MIN response and authorized aggregate result boundary.')
spec('K_SHP_HANDOVER_MED', 'date(handed_over_at)', 'daily handover population',
     'Median(handed_over-picked in reference Julian hours), ROUND 2.', 'Uses selected MAX event times, not arbitrary adjacent events.')
spec('K_SHP_ONTIME_BY_CITY', 'date(delivered_at), city', 'daily delivered per city',
     '100*AVG(delivered_at<=promised_by), ROUND 1.', 'Use canonical city dimension and NULL deadline behavior; do not average city percentages for rollup.')
spec('K_SHP_DELIV_DAYS_MED', 'date(delivered_at)', 'daily delivered population',
     'ROUND(median(reference hours delivered-paid)/24,2).', 'Division by 24 occurs before final rounding. Do not round hours first.')
spec('K_SUP_TICKETS', 'cal.d and date(tickets.created_at)', 'daily all support',
     'COUNT(ticket_id), calendar LEFT JOIN tickets.', 'All teams; false zero is possible when source is missing. Quality gate is separate.')
spec('K_SUP_BACKLOG', 'cal.d at 22:00:00', 'point-in-time all support',
     'COUNT(ticket_fact created<=cutoff and resolved NULL or >cutoff).', 'Uses MAX resolved; reopening is not an added canonical predicate.')
spec('K_RSP_FRT_2H_PCT', 'date(first_response_at)', 'daily T_RSP first-response population',
     '100*AVG(first_response-created<=2h), ROUND 1.', 'Non-NULL first response required; preserve MIN first response and NULL elapsed sample behavior.')
spec('K_RSP_TICKETS', 'cal.d and date(tickets.created_at)', 'daily T_RSP',
     "COUNT(ticket_id) with team_id='T_RSP' in calendar LEFT JOIN.", 'Calendar counts differ from the dimensioned query row set; missing source can appear as false zero.')
spec('K_RSP_TICKETS_BY_CAT', 'date(created_at), ticket category', 'daily T_RSP per category',
     "COUNT(*) from tickets WHERE team_id='T_RSP' GROUP BY date/category.", 'No category group means no row. New categories cannot be hard-coded away.')
spec('K_RSP_BACKLOG', 'cal.d at 22:00:00', 'point-in-time T_RSP',
     'COUNT(ticket_fact T_RSP created<=cutoff and first_response NULL or >cutoff).', 'Uses MIN first_response. It is unanswered backlog, not unresolved backlog.')
spec('K_RSP_CSAT', 'date(answered_at)', 'daily answers joined to T_RSP tickets',
     'AVG(score), ROUND 2; csat JOIN tickets USING(ticket_id) with team=T_RSP.', 'Tickets affect membership. No event join. Source scope and survey response occurrence are distinct.')
spec('K_CMP_RES_MED', 'date(resolved_at)', 'daily resolved T_CMP',
     'Median(resolved-created in reference Julian hours), ROUND 2.', 'Uses MAX resolved. Reopen lifecycle is separate; no silent formula repair.')
spec('K_CMP_TICKETS', 'cal.d and date(created_at)', 'daily T_CMP',
     "COUNT(ticket_id) in calendar LEFT JOIN with team_id='T_CMP'.", 'Known empty and missing source are distinct despite canonical zero behavior.')
spec('K_CMP_BACKLOG', 'cal.d at 22:00:00', 'point-in-time T_CMP',
     'COUNT(ticket_fact T_CMP created<=cutoff and resolved NULL or >cutoff).', 'Uses MAX resolved, not current reopen state. Preserve exact cutoff equality.')
assert set(S) == {r['kpi_id'] for r in K}, (set(S) ^ {r['kpi_id'] for r in K})

contracts = []
for number, k in enumerate(K, 2):
    rounds = re.findall(r',\s*(\d+)\)\s+(?:AS\s+)?value', k['sql'], re.I)
    contracts.append(dict(requirement_id='REQ-KPI-' + k['kpi_id'],
        parent_req='REQ-02', source=f'dataset/config/kpi_dictionary.csv:record {number}',
        classification='Requirement', component='kpi', **k,
        sql_sha256=hashlib.sha256(k['sql'].encode()).hexdigest(),
        precision=rounds[-1] if rounds else 'integer count or source SUM; no added ROUND',
        **S[k['kpi_id']], contract='Canonical definition/result; approved PostgreSQL translation; frozen eligible inputs; no silent formula edits.',
        adr='ADR-01;ADR-02;ADR-03;ADR-04;ADR-06;ADR-07',
        acceptance='AT-02;AT-03;AT-05;AT-06;AT-24',
        implementation_evidence='Not executed by this audit; PostgreSQL equivalence remains Open.'))
emit('kpi-contracts.csv', contracts)
emit('workflow-contracts.csv', [dict(requirement_id=f"REQ-WF-{r['workflow_id']}-{r['stage_order']}",
    source=f'dataset/config/workflow_definitions.csv:record {i}', classification='Requirement', component='workflows',
    **r, stage_owner='Open; not inferred from M01 end-to-end owner.',
    contract='Stage duration/deadline and median target remain separate from canonical workflow KPI.',
    adr='ADR-15;ADR-07', acceptance='AT-12;AT-25', implementation_evidence='Planned only')
    for i, r in enumerate(stages, 2)])

result = dict(method='Read source CSV/JSON and SQL text. No SQL execution. Data is synthetic.',
    source_hashes={p:sha(p) for p in ['dataset/config/kpi_dictionary.csv','dataset/config/reference_views.sql',
        'dataset/config/escalation_rules.csv','dataset/config/workflow_definitions.csv','docs/architecture/sources/Adr.md',
        'architecture/structurizr/workspace.dsl']}, manifest_count=91, manifest_checks=manifest_checks,
    header_versions=headers, source_row_counts=dict(raw_counts),
    day076_orders=dict(raw_rows=len(orders), distinct_payloads=len(counts), extra_exact_rows=len(orders)-len(counts)),
    day066_missing_support=['tickets.csv','ticket_events.csv','csat.csv'],
    day067_support_by_business_date=late_support, correction_fixture=correction_rows,
    calendar=dict(rows=90, consecutive=True, day_indices_unique=True,
        fields=list(calendar[0]), date_min=str(dates[0]), date_max=str(dates[-1]),
        manifest_dates_match=True,
        month_metadata={m:sorted({r['mdays'] for r in calendar if r['jmonth']==m}) for m in sorted({r['jmonth'] for r in calendar})}),
    events_calendar=dict(rows=len(events), fields=list(events[0]),
        known_at_field_supplied=any(k in events[0] for k in ['known_at','announced_at','received_at'])),
    catalog_metadata_rows_verified=55, original_sql_executed=False,
    input_count=len(inputs), question_count=sum(r['type']=='question' for r in inputs),
    input_types=dict(Counter(r['type'] for r in inputs)),
    unresolved='Input modes, source closure, correction tie, NULL dimension wire mapping, M11 precedence, attachment readiness, capacity formula remain Open.')
(OUT / 'source-checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(dict(manifests=91, matching_manifest_counts=91, canonical_metadata_rows=55,
    semantic_kpi_contracts=len(contracts), workflow_stages=len(stages), rule_ids=[r['rule_id'] for r in rules])))
