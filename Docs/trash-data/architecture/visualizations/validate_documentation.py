"""Validate the documentation against unchanged local sources. No application tests."""
import csv, hashlib, json
from pathlib import Path

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
catalog=rows(OUT/'table-column-catalog.csv')
observed=set()
for p in (ROOT/'dataset').rglob('*.csv'):
    name=p.stem if 'drops' in p.parts else p.relative_to(ROOT/'dataset').with_suffix('').as_posix().replace('/','__')
    with p.open(encoding='utf-8-sig',newline='') as f:
        for col in next(csv.reader(f)):observed.add((name,col))
assert observed=={(r['table'],r['column']) for r in catalog}
access=rows(OUT/'access-matrix-detailed.csv')
grants={r['manager_id']:r for r in rows(ROOT/'dataset/org/access_matrix.csv')}
for mid,g in grants.items():
    found=[r for r in access if r['manager_id']==mid]
    assert {(r['source_table'],r['column']) for r in found}==observed
    assert all(r['organizational_scope']==g['visible_entities'] for r in found)
    if not g['individual_level_data_team']:
        assert not any(r['column_visibility']=='VISIBLE_DIRECT_TEAM' for r in found)
    for r in found:
        if r['source_table']=='staff_availability' and r['column'] in {'status','staff_id'}:
            assert r['column_visibility']=='DENIED' and r['internal_use']=='REQUIRED_INTERNAL'
        if mid in {'M01','M02','M03','M04'} and (r['column'] in {'staff_id','owner_id'} or (r['source_table']=='org__staff' and r['column']=='name_fa')):
            assert r['column_visibility']=='DENIED'
mapping=rows(OUT/'kpi-source-manager-mapping.csv')
definitions={r['kpi_id']:r for r in rows(ROOT/'dataset/config/kpi_dictionary.csv')}
assert len(mapping)==len(definitions)==55
for r in mapping:
    k=definitions[r['kpi_id']]
    assert r['sql']==k['sql'] and r['entity_id']==k['entity_id'] and r['owner_manager_id']==k['owner_manager_id']
    expected={mid for mid,g in grants.items() if k['entity_id'] in g['visible_entities'].split('|')}
    assert set(r['authorized_managers'].split('|'))==expected
    assert r['kpi_id'] in (OUT/f'06-lineage-{k["entity_id"]}.mmd').read_text(encoding='utf-8')
    for field in ['value_columns','join_filter_columns']:
        for t,columns in json.loads(r[field]).items():
            real='calendar__calendar_days' if t=='cal' else 'config__monthly_targets' if t=='monthly_targets' else t
            for c in columns:
                if t=='crm_lead_events' and c=='drop_day':continue
                c='date' if t=='cal' and c=='d' else c
                assert (real,c) in observed,(r['kpi_id'],t,c)
for r in rows(OUT/'source-inventory.csv'):assert digest(ROOT/r['path'])==r['sha256']
for r in rows(OUT/'protected-file-hashes.csv'):assert digest(ROOT/r['path'])==r['sha256']
diagrams=list(OUT.glob('*.mmd'))
for p in diagrams:
    text=p.read_text(encoding='utf-8')
    assert '```' not in text
    assert text.count('[')==text.count(']')
    if 'flowchart' in text:
        assert text.count('"')%2==0
assert not list(OUT.glob('*.svg'))
result={'catalog_matches_all_headers':True,'all_11_manager_scopes_match':True,'all_55_original_sql_strings_match':True,'all_kpis_in_domain_diagrams':True,'no_upper_manager_individual_visibility':True,'no_individual_attendance_visibility':True,'all_dependency_columns_exist_or_are_documented_metadata':True,'source_and_existing_file_hashes_unchanged':True,'diagram_structure_checked':len(diagrams),'mermaid_parser_and_svg_render':'UNAVAILABLE; not claimed as validated','application_implemented':False}
(OUT/'independent-validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
