"""Documentation audit support. This file is not product implementation."""
from pathlib import Path
import json
import zipfile

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent

def read(path):
    return (ROOT / path).read_text(encoding='utf-8')

def write(path, text):
    (ROOT / path).write_text(text, encoding='utf-8', newline='\n')

def finding(number, document, needle, category, severity, evidence,
            correction, uncertainty='None.', status='Corrected'):
    with zipfile.ZipFile(OUT / 'pre-edit.zip') as archive:
        original = archive.read(document).decode('utf-8-sig')
    lines = original.splitlines()
    matches = [(i + 1, line) for i, line in enumerate(lines) if needle in line]
    assert matches, (number, document, needle)
    start, claim = matches[0]
    record = dict(id=f'AUD-{number:03d}', document=document,
                  original_line=start, original_claim=claim,
                  category=category, severity=severity, evidence=evidence,
                  correction=correction, status=status,
                  uncertainty=uncertainty)
    path = OUT / 'findings.json'
    records = json.loads(path.read_text(encoding='utf-8')) if path.exists() else []
    assert record['id'] not in {r['id'] for r in records}
    records.append(record)
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')

def replace_span(text, start, end, body):
    a = text.index(start)
    b = text.index(end, a)
    return text[:a] + body.strip() + '\n\n' + text[b:]
