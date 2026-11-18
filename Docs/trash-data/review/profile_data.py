from pathlib import Path
import csv,json,collections
root=Path('dataset'); out={}; counts=collections.Counter(); schemas=collections.defaultdict(dict); duplicate=collections.defaultdict(int); seen=collections.defaultdict(set); mismatch=[]; missing=[]
expected={p.name for p in (root/'drops/day_001').glob('*.csv')}
for d in sorted((root/'drops').iterdir()):
 manifest=json.loads((d/'manifest.json').read_text())
 actual={p.name for p in d.glob('*.csv')}
 if d.name!='day_000' and expected-actual: missing.append([d.name,sorted(expected-actual)])
 for p in sorted(d.glob('*.csv')):
  with p.open(encoding='utf-8-sig',newline='') as f:
   r=csv.DictReader(f); cols=r.fieldnames; rows=list(r)
  schemas[p.name].setdefault('|'.join(cols),[]).append(d.name)
  counts[p.name]+=len(rows)
  for row in rows:
   key=tuple(sorted(row.items()))
   if key in seen[p.name]: duplicate[p.name]+=1
   seen[p.name].add(key)
  if manifest['files'].get(p.name)!=len(rows): mismatch.append([d.name,p.name,manifest['files'].get(p.name),len(rows)])
out={'drop_count':len(list((root/'drops').iterdir())),'rows':dict(counts),'exact_repeated_rows':dict(duplicate),'missing_files':missing,'manifest_mismatches':mismatch,'schema_variants':{k:[{'columns':s.split('|'),'days':v if len(v)<8 else [v[0],v[-1]]} for s,v in variants.items()] for k,variants in schemas.items()}}
for folder in ['org','config']:
 out[folder+'_rows']={p.name:sum(1 for _ in csv.DictReader(p.open(encoding='utf-8-sig',newline=''))) for p in (root/folder).glob('*.csv')}
Path('review/profile.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(out,indent=2,ensure_ascii=False))
