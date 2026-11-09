"""Capture local source state. Write only inside this Registry folder."""
from pathlib import Path
import subprocess, hashlib, json

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
def git(*args):
    p = subprocess.run(['git', '-c', 'core.quotepath=false', *args], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    return {'returncode': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}

if __name__ == '__main__':
    target = OUT / 'preflight.json'
    if target.exists():
        raise SystemExit('Preflight already exists. Do not replace the initial evidence.')
    tracked = git('ls-files', '-z')['stdout'].strip('\0').split('\0')
    untracked = git('ls-files', '--others', '--exclude-standard', '-z')['stdout'].strip('\0').split('\0')
    # Exclude this task folder. It did not exist at the first Git inspection.
    untracked = [p for p in untracked if p and not p.startswith('Docs/architecture/registry/')]
    hashes = {}
    for name in sorted(set(tracked + untracked)):
        path = ROOT / name
        if path.is_file():
            hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    data = {'task': 'ARCH-REG-001', 'date': '2026-11-09', 'timezone': 'Asia/Tehran',
            'baseline': '0a42950d1ce9734433d961540af9ab4be21573b2',
            'head': git('rev-parse', 'HEAD'), 'status': git('status', '--porcelain=v1', '-uall'),
            'baseline_diff': git('diff', '--name-status', '0a42950d1ce9734433d961540af9ab4be21573b2'),
            'tracked_files': tracked, 'existing_untracked_files': untracked, 'sha256': hashes,
            'note': 'Registry files are excluded from the initial inventory. The first Git inspection found 141 untracked files and no tracked changes.'}
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'existing_untracked': len(untracked), 'source_hashes': len(hashes)}))
