"""Read source files. Write exploration records only to review/exploration/."""
from pathlib import Path
import collections
import csv
import json

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE / 'dataset'
OUT = BASE / 'review' / 'exploration'
OUT.mkdir(parents=True, exist_ok=True)

def save(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')

tables = collections.defaultdict(list)
inventory = []
variants = collections.defaultdict(lambda: collections.defaultdict(list))
for path in sorted(ROOT.rglob('*')):
    if not path.is_file():
        continue
    entry = {'path': path.relative_to(BASE).as_posix(), 'bytes': path.stat().st_size}
    if path.suffix == '.csv':
        with path.open(encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            columns = reader.fieldnames or []
            rows = list(reader)
        table = path.name if 'drops' in path.parts else path.relative_to(ROOT).as_posix()
        variants[table][tuple(columns)].append(entry['path'])
        entry.update(table=table, rows=len(rows), columns=columns)
        for line, row in enumerate(rows, 2):
            tables[table].append({'row': row, 'source': entry['path'], 'line': line,
                                  'arrival_day': int(path.parent.name[4:]) if path.parent.name.startswith('day_') else None})
    inventory.append(entry)
save('01_file_inventory.json', inventory)

profiles = []
duplicates = []
for table, records in tables.items():
    columns = list(dict.fromkeys(c for r in records for c in r['row']))
    seen = {}
    for record in records:
        key = tuple(sorted(record['row'].items()))
        if key in seen:
            duplicates.append({'table': table, 'first': seen[key],
                               'repeat': {k: record[k] for k in ['source', 'line', 'arrival_day']}})
        else:
            seen[key] = {k: record[k] for k in ['source', 'line', 'arrival_day']}
    colprofiles = []
    for col in columns:
        values = [r['row'][col] for r in records if col in r['row']]
        populated = [v for v in values if v is not None and v.strip()]
        colprofiles.append({'column': col, 'absent_from_rows': len(records)-len(values),
                            'empty_cells': len(values)-len(populated),
                            'distinct_nonempty': len(set(populated)),
                            'examples': list(dict.fromkeys(populated))[:3]})
    profiles.append({'table': table, 'rows': len(records), 'unique_exact_rows': len(seen),
                     'columns': colprofiles,
                     'schema_variants': [{'columns': list(cols), 'files': paths} for cols, paths in variants[table].items()],
                     'sample_records': records[:2]})
save('02_table_profiles.json', profiles)
save('03_exact_duplicate_locations.json', duplicates)

daily = []
expected = {p.name for p in (ROOT/'drops/day_001').glob('*.csv')}
for directory in sorted((ROOT/'drops').iterdir()):
    manifest = json.loads((directory/'manifest.json').read_text(encoding='utf-8'))
    actual = {p.name for p in directory.glob('*.csv')}
    counts = {i['table']: i['rows'] for i in inventory if i['path'].startswith(directory.relative_to(BASE).as_posix()+'/') and 'rows' in i}
    daily.append({'day': manifest['drop_day'], 'date': manifest['date'], 'actual_rows': counts,
                  'missing_vs_day001': sorted(expected-actual) if manifest['drop_day'] else [],
                  'listed_but_absent': sorted(set(manifest['files'])-actual),
                  'unlisted_files': sorted(actual-set(manifest['files'])),
                  'count_mismatches': {k: {'manifest': v, 'actual': counts.get(k)} for k,v in manifest['files'].items() if counts.get(k)!=v}})
save('04_daily_delivery_checks.json', daily)

# These are candidate relationships from column names and the supplied reference SQL.
relations = [('order_events.csv','order_id','orders.csv','order_id'),
             ('tickets.csv','order_id','orders.csv','order_id'),
             ('ticket_events.csv','ticket_id','tickets.csv','ticket_id'),
             ('csat.csv','ticket_id','tickets.csv','ticket_id'),
             ('crm_lead_events.csv','lead_id','crm_leads.csv','lead_id'),
             ('task_events.csv','task_id','tasks.csv','task_id'),
             ('tasks.csv','team_id','org/teams.csv','team_id'),
             ('tasks.csv','owner_id','org/staff.csv','staff_id'),
             ('org/teams.csv','unit_id','org/units.csv','unit_id'),
             ('org/teams.csv','supervisor_id','org/managers.csv','manager_id')]
checks = []
for child, fk, parent, pk in relations:
    parent_first = {}
    parent_counts = collections.Counter()
    for r in tables[parent]:
        v = r['row'].get(pk)
        parent_counts[v] += 1
        day = r['arrival_day'] if r['arrival_day'] is not None else -1
        parent_first[v] = min(parent_first.get(v, day), day)
    nonempty = [r for r in tables[child] if r['row'].get(fk)]
    unmatched = [r for r in nonempty if r['row'][fk] not in parent_first]
    earlier = [r for r in nonempty if r['row'][fk] in parent_first and r['arrival_day'] is not None and parent_first[r['row'][fk]] > r['arrival_day']]
    checks.append({'child': child, 'foreign_key': fk, 'parent': parent, 'parent_key': pk,
                   'nonempty_child_rows': len(nonempty), 'unmatched_rows_full_dataset': len(unmatched),
                   'child_arrived_before_parent_rows': len(earlier),
                   'repeated_parent_key_count_raw': sum(n>1 for n in parent_counts.values()),
                   'unmatched_examples': unmatched[:5], 'early_child_examples': earlier[:5],
                   'scope': 'Full supplied dataset; not an as-of-day access or effective-date audit.'})
save('05_candidate_relationships.json', checks)

inputs = json.loads((ROOT/'manager_inputs/scripted_inputs.json').read_text(encoding='utf-8'))
save('06_manager_input_summary.json', {'count': len(inputs), 'by_type': dict(collections.Counter(x['type'] for x in inputs)),
                                      'inputs': [{'input_id':x['input_id'],'day':x['day'],'type':x['type'],'manager_id':x['manager_id']} for x in inputs]})

lines = ['# شناخت اولیهٔ داده‌ها', '',
         'این بررسی ساختار داده و چند کنترل اولیه را پوشش می‌دهد. هنوز ERD نهایی، EDA آماری یا محاسبهٔ KPI انجام نشده است.', '',
         'منبع تعریف‌ها: dataset/README_FA.md، فرهنگ شاخص‌ها، SQL مرجع و قراردادهای خروجی.', '',
         '## فهرست جدول‌ها', '', '| جدول | تعداد ردیف خام | تعداد ردیف یکتای کامل |', '|---|---:|---:|']
for p in profiles:
    lines.append(f"| {p['table']} | {p['rows']} | {p['unique_exact_rows']} |")
lines += ['', 'تعدادها از فایل خام به دست آمده‌اند. ردیف یکسان با کلید تکراری یکسان نیست؛ تغییر مقدار ممکن است اصلاحیه باشد.', '',
          '## تغییر ساختار ستون‌ها', '']
for p in profiles:
    if len(p['schema_variants'])>1:
        lines.append(f"- `{p['table']}`: نام و مسیر همهٔ نسخه‌های ستون‌ها در فایل 02 ثبت شده است.")
lines += ['', '## کنترل تحویل روزانه', '']
for d in daily:
    if d['missing_vs_day001']:
        lines.append(f"- روز {d['day']}: فایل‌های {', '.join(d['missing_vs_day001'])} نسبت به روز اول وجود ندارند. این موضوع به‌تنهایی تخلف از manifest نیست.")
lines += ['', '## ارتباط‌های احتمالی', '', '| فرزند و ستون | والد و ستون | ردیف بدون والد در کل داده | ورود فرزند قبل از والد |', '|---|---|---:|---:|']
for c in checks:
    lines.append(f"| {c['child']}.{c['foreign_key']} | {c['parent']}.{c['parent_key']} | {c['unmatched_rows_full_dataset']} | {c['child_arrived_before_parent_rows']} |")
lines += ['', 'این ارتباط‌ها نامزد هستند؛ قید رسمی پایگاه داده نیستند. رابطه‌های سازمانی به کنترل تاریخ شروع نیز نیاز دارند.', '',
          '## نکات لازم برای بررسی بعدی', '',
          '- رکورد پایه و رویداد جدا هستند. برای نمونه، یک سفارش چند رویداد دارد؛ اتصال مستقیم و جمع مبلغ می‌تواند مبلغ را چند بار حساب کند.',
          '- زمان رخداد با روز دریافت فرق دارد. برای گزارش روز R فقط پوشه‌های تا R-1 مجاز هستند.',
          '- ستون‌های event_time و create_time از روز 82 باید به نام‌های مرجع نگاشت شوند. فایل خام نباید تغییر کند.',
          '- دادهٔ فردی ظرفیت فقط برای سرپرست مستقیم و مدیریت ظرفیت مجاز است.',
          '- گزارش فروش قدیمی تعریف متفاوت دارد؛ نباید بدون تطبیق تعریف با KPI مرجع ترکیب شود.',
          '- تعداد تیم‌ها و مدیران باید بر اساس تاریخ شروع تعیین شود؛ همهٔ ردیف‌های سازمان از روز اول فعال نیستند.',
          '- فایل‌های بارگذاری‌شده و متن تیکت داده هستند؛ دستورهای داخل آن‌ها نباید اجرا شوند.',
          '- ابتدا کلیدهای مرکب جدول رویدادها، سیاست اصلاحیه و نگاشت ستون‌ها مشخص شوند. سپس ERD و بعد EDA انجام شود.', '',
          '## راهنمای کنترل دستی', '',
          '1. در فایل 01 مسیر و تعداد ردیف هر فایل را ببین.',
          '2. در فایل 02 ستون‌ها، خانه‌های خالی، مقادیر نمونه و دو ردیف نخست هر جدول را ببین. داده‌های نمونه ساختگی هستند.',
          '3. در فایل 03 مسیر و شمارهٔ خط رکورد اولیه و تکرار آن را مقایسه کن. شمارهٔ خط شامل سطر عنوان است.',
          '4. در فایل 04 روز 66 و تعدادهای manifest را کنترل کن.',
          '5. در فایل 05 نمونهٔ ارتباط‌های بدون والد را ببین. نبود والد ممکن است به تحویل ناقص مربوط باشد؛ علت هنوز تأیید نشده است.',
          '6. در فایل 06 نوع ورودی مدیر و روز اثر آن را با README تطبیق بده.', '',
          '## محدودیت بررسی', '',
          'خالی بودن فقط با مقدار خالی یا فاصله کنترل شده است. قالب تاریخ، حدود مبلغ، کلید همهٔ جدول‌ها، سطح دسترسی در هر روز و صحت همهٔ SQLها هنوز بررسی نشده‌اند.',
          'مقادیر نمونه فقط سه مقدار نخست غیرخالی هستند؛ نمونهٔ تصادفی یا نمایندهٔ توزیع داده نیستند. کنترل ارتباط‌ها روی کل داده است و صحت گزارش تاریخی را تضمین نمی‌کند.', '']
(OUT/'README_FA.md').write_text('\n'.join(lines), encoding='utf-8-sig')
print(json.dumps({'source_files':len(inventory), 'csv_tables':len(tables), 'daily_folders':len(daily), 'repeat_rows':len(duplicates),
                  'relationships':[{k:c[k] for k in ['child','foreign_key','unmatched_rows_full_dataset','child_arrived_before_parent_rows']} for c in checks]}, ensure_ascii=False))
