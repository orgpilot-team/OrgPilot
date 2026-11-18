"""Check source files. Keep all source files unchanged."""
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
import csv
import json
import re
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE / 'dataset'
OUT = BASE / 'review' / 'types-and-missing'
OUT.mkdir(exist_ok=True)
ALIASES = {'tickets.csv': {'create_time': 'created_at'},
           'ticket_events.csv': {'event_time': 'at'}}
INTS = set('day_idx day_in_month mdays iwd is_holiday direction escalate_after_days stage_order score spend_toman impressions clicks leads amount_toman items order_value_toman sessions decided_day week_no sales_toman level effective_from_day effective_to_day فروش_تومان'.split())
DECIMALS = set('target warn crit target_million_toman stage_target_median_h contract_value_toman'.split())
DATES = set('date end_date due_date decided_date effective_from_date'.split())
TIMES = set('at created_at answered_at promised_by'.split())
SENTINELS = {'null', 'none', 'nan', 'na', 'n/a', '<na>', 'nat'}
tables = defaultdict(list)
headers = defaultdict(lambda: defaultdict(list))
totals = Counter()
sentinels = Counter()
malformed = []
json_nulls = []
for p in sorted(ROOT.rglob('*.csv')):
    name = p.name if p.parent.parent.name == 'drops' else p.relative_to(ROOT).as_posix()
    with p.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        headers[name][tuple(reader.fieldnames or [])].append(p.relative_to(BASE).as_posix())
        for line, raw in enumerate(reader, 2):
            totals['csv_rows'] += 1
            totals['csv_cells'] += len(reader.fieldnames)
            if None in raw or any(v is None for v in raw.values()):
                malformed.append({'file': str(p.relative_to(BASE)), 'record': line})
            row = {ALIASES.get(name, {}).get(k, k): v for k, v in raw.items()}
            tables[name].append(row)
            for v in raw.values():
                if isinstance(v, str):
                    totals['empty_csv_cells'] += not v.strip()
                    if v.strip().lower() in SENTINELS:
                        sentinels[v] += 1
    totals['csv_files'] += 1

def walk(obj, path, source):
    if obj is None:
        json_nulls.append({'file': source, 'path': path})
    elif isinstance(obj, dict):
        for key, val in obj.items():
            walk(val, path + '.' + key, source)
    elif isinstance(obj, list):
        for i, val in enumerate(obj):
            walk(val, f'{path}[{i}]', source)

for p in sorted(ROOT.rglob('*.json')):
    walk(json.loads(p.read_text(encoding='utf-8-sig')), '$', p.relative_to(BASE).as_posix())
    totals['json_files'] += 1

profiles = []
summaries = []
failures = []
for name, rows in tables.items():
    cols = list(dict.fromkeys(c for row in rows for c in row))
    duplicates = len(rows) - len({tuple(sorted(r.items())) for r in rows})
    summaries.append({'table': name, 'rows': len(rows), 'columns': len(cols),
                      'empty_cells': sum(not v.strip() for r in rows for v in r.values() if isinstance(v, str)),
                      'rows_with_empty': sum(any(isinstance(v, str) and not v.strip() for v in r.values()) for r in rows),
                      'exact_duplicate_rows': duplicates})
    for c in cols:
        values = [r[c] for r in rows if c in r]
        counts = Counter(v for v in values if isinstance(v, str) and v.strip())
        kind = ('Int64' if c in INTS else 'Float64/DECIMAL' if c in DECIMALS else
                'date' if c in DATES else 'datetime' if c in TIMES else
                'number_or_deadline_field' if c == 'sla_hours' else 'string')
        invalid = Counter()
        nums = []
        for v, count in counts.items():
            valid = True
            try:
                if kind == 'Int64':
                    valid = bool(re.fullmatch(r'[+-]?\d+', v))
                    if valid:
                        nums.append(int(v))
                elif kind == 'Float64/DECIMAL':
                    x = Decimal(v)
                    valid = x.is_finite()
                    if valid:
                        nums.append(float(x))
                elif kind == 'date':
                    valid = bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}', v))
                    date.fromisoformat(v)
                elif kind == 'datetime':
                    valid = bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(:\d{2})?', v))
                    datetime.fromisoformat(v)
                elif kind == 'number_or_deadline_field':
                    valid = v == 'promised_by' or Decimal(v).is_finite()
            except (ValueError, InvalidOperation, OverflowError):
                valid = False
            if not valid:
                invalid[v] += count
        item = {'table': name, 'column': c, 'rows': len(rows),
                'empty_cells': sum(v is None or not v.strip() for v in values),
                'absent_column_rows_after_aliases': len(rows) - len(values),
                'null_like_text': sum(n for v, n in counts.items() if v.strip().lower() in SENTINELS),
                'type_to_use': kind, 'invalid_nonempty': sum(invalid.values()),
                'invalid_examples': dict(invalid.most_common(5)), 'distinct_nonempty': len(counts),
                'min': min(nums) if nums else None, 'max': max(nums) if nums else None}
        profiles.append(item)
        if invalid:
            failures.append(item)

coverage = []
expected = {p.name for p in (ROOT/'drops/day_001').glob('*.csv')}
for folder in sorted((ROOT/'drops').glob('day_*')):
    day = int(folder.name[4:])
    missing = expected - {p.name for p in folder.glob('*.csv')}
    if day and missing:
        coverage.append({'day': day, 'missing': sorted(missing)})

numeric_cast = []
for table, col in [('order_events.csv', 'amount_toman'), ('crm_lead_events.csv', 'contract_value_toman'),
                   ('org/staff.csv', 'effective_to_day')]:
    s = pd.Series([r[col] for r in tables[table]], dtype='string')
    n = pd.to_numeric(s.mask(s.str.strip().eq('')), errors='raise')
    numeric_cast.append({'table': table, 'column': col, 'dtype': str(n.dtype), 'missing': int(n.isna().sum())})

event_values = {}
for table, col in [('order_events.csv', 'amount_toman'), ('crm_lead_events.csv', 'contract_value_toman')]:
    grouped = defaultdict(Counter)
    for r in tables[table]:
        grouped[r['event']]['present' if r[col].strip() else 'empty'] += 1
    event_values[table] = {event: dict(counts) for event, counts in grouped.items()}
result = {'scope': 'All CSV and JSON files under dataset. CSV aliases applied in memory.',
          'totals': dict(totals), 'null_like_csv_text': dict(sentinels), 'json_nulls': json_nulls,
          'malformed_csv_records': malformed, 'missing_delivery_files': coverage,
          'tables': summaries, 'columns': profiles, 'type_failures': failures,
          'nullable_cast_checks': numeric_cast, 'event_value_coverage': event_values,
          'schema_changes': {t: [{'columns': list(h), 'files': paths} for h, paths in variants.items()]
                             for t, variants in headers.items() if len(variants) > 1}}
(OUT/'evidence.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
with (OUT/'column-checks.csv').open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(profiles[0]))
    writer.writeheader()
    writer.writerows(profiles)
report = [
    '# Data type and missing value check',
    '',
    'The source files need type conversion and consistent column names before analysis.',
    'The checked nonempty numeric and Gregorian date fields have no format errors.',
    'This result does not prove that each business value is correct.',
    '',
    f'Scope: all {totals["csv_files"]:,} CSV files and {totals["json_files"]} JSON files under dataset. The CSV files contain {totals["csv_rows"]:,} rows in {len(tables)} tables.',
    'Counts include all deliveries, repeated rows, reference tables, and the uploaded CSV.',
    'Source files and analysis.ipynb were not changed.',
    '',
    '## Missing values',
    '',
    'The CSV files contain 190,185 empty cells out of 1,287,636 cells (14.77%).',
    'A total of 188,928 rows have at least one empty cell. These are cell and row counts, respectively.',
    'There are no CSV text values that equal null, none, nan, na, n/a, <na>, or nat after case and space changes.',
    'There is one JSON null. It is decision_card in output_contract/example_brief.json. This is an output example.',
    '',
    '| Table | Column | Empty cells | Percent of table rows |',
    '| --- | --- | ---: | ---: |',
]
for item in profiles:
    if item['empty_cells']:
        report.append(f"| {item['table']} | {item['column']} | {item['empty_cells']:,} | {100*item['empty_cells']/item['rows']:.2f}% |")
report += [
    '',
    'Do not replace all empty cells with zero or delete all rows with empty cells.',
    'All 1,677 refund events have an amount. Other order events have no amount in this field.',
    'All 314 won events and the one value correction have a contract value. Other CRM events have no contract value.',
    'An empty parent_id is expected for ORG. An empty effective_to_day can indicate no end date.',
    'An empty campaign_id can indicate no campaign. An empty blocker_fa can indicate no blocker.',
    'Confirm the business meaning before you fill other empty fields.',
    'The 1,475 empty promised_by values and 1,539 empty staff_id values need explicit rules.',
    'An empty access field must not grant access.',
    '',
    '## Data types',
    '',
    'CSV files have no declared data types. The notebook uses dtype="string" and keep_default_na=False for most source loads.',
    'This retains empty cells as empty strings. A direct isna() count will not detect them.',
    'Use a copy for conversion. First replace empty strings with pd.NA.',
    '',
    '| Fields | Type to use |',
    '| --- | --- |',
    '| IDs, codes, names, category values, jdate, jmonth | string |',
    '| Counts, day numbers, score, direction | nullable Int64 |',
    '| Money | nullable Int64 for whole toman values; DECIMAL for exact decimal values |',
    '| Thresholds and fractional durations | nullable Float64 or DECIMAL |',
    '| created_at, at, answered_at, promised_by | datetime |',
    '| date, due_date, effective_from_date | date |',
    '| is_holiday | boolean after a 0/1 check |',
    '',
    'effective_to_day has 26 empty values and no populated values. Use nullable Int64 because it is a day number.',
    'Its intended type cannot be inferred from its values alone.',
    'sla_hours has ten numeric values, one empty value, and the text promised_by.',
    'Keep this source field. In a derived table, use a numeric duration and a separate deadline field reference.',
    'Do not convert promised_by to an unreported missing number.',
    'The Gregorian date checks do not validate the Jalali calendar. Keep jdate and jmonth as strings.',
    'The source timestamps have no time zone. Confirm the source time zone before conversion to UTC.',
    '',
    '## Normalization',
    '',
    'Data cleaning is necessary. Apply the following changes in a derived data layer:',
    '',
    '1. Map tickets.create_time to created_at and ticket_events.event_time to at. The names change on day 082.',
    '2. Convert empty cells to nullable values and apply an explicit type for each column.',
    '3. Remove 262 exact repeated order rows from the analysis copy. Keep the source records and delivery details.',
    '4. Keep a missing delivery separate from empty cells. Day 066 has no tickets, ticket_events, or csat file.',
    '',
    'Numeric scaling, such as Min-Max or Z-score, is not required for the supplied KPI SQL.',
    'Keep amounts, durations, and counts in their specified units. If an ML model is added, assess scaling for that model.',
    'For a distance-based or gradient-based model, fit a scaler on training data only.',
    'For database normalization, separate multi-value fields when they are needed for joins or access checks.',
    'Examples are access_matrix.visible_entities and workflow_definitions.units.',
    'A full database redesign is not required to run the supplied KPI queries.',
    '',
    '## Evidence',
    '',
    'Run: .venv/Scripts/python.exe review/check_types_and_missing.py',
    'See evidence.json for counts, column name changes, conversion checks, and delivery gaps.',
    f'See column-checks.csv for all {len(profiles)} columns after the two column name mappings.',
]
(OUT/'report.md').write_text('\n'.join(report) + '\n', encoding='utf-8')
print(json.dumps({'totals': dict(totals), 'tables': len(tables), 'columns': len(profiles),
                  'empty_columns': sum(bool(p['empty_cells']) for p in profiles),
                  'type_failures': len(failures), 'report': str(OUT/'report.md')}, indent=2))
