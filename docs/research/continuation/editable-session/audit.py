#!/usr/bin/env python3
"""Reproduce source lineage, actual immutable dependencies and artifact Git seals."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
checks=[]
for commit,directory in [('5d5c767','internal/editor'),('9519032','internal/document'),('5ad84e4','internal/storage')]:
    subprocess.run(['git','merge-base','--is-ancestor',commit,'HEAD'],cwd=ROOT,check=True)
    for p in sorted((ROOT/directory).glob('*.go')):
        if p.name.endswith('_test.go'):continue
        path=str(p.relative_to(ROOT));approved=subprocess.check_output(['git','show',commit+':'+path],cwd=ROOT)
        assert p.read_bytes()==approved,path;checks.append({'path':path,'approved_commit':commit,'sha256':hashlib.sha256(approved).hexdigest()})
for name in ['go.mod','go.sum']:
    assert (ROOT/name).read_bytes()==subprocess.check_output(['git','show','72369db:'+name],cwd=ROOT),name
manifest=HERE/'artifact-manifest.json'
if manifest.exists():
    for row in json.loads(manifest.read_text())['records']:
        p=ROOT/row['path'];raw=p.read_bytes();assert len(raw)==row['size'] and hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
        blob=subprocess.check_output(['git','hash-object','--stdin'],input=raw,cwd=ROOT).decode().strip();assert blob==row['git_blob'],row['path']
        assert subprocess.check_output(['git','show','HEAD:'+row['path']],cwd=ROOT)==raw,row['path']
print(json.dumps({'approved_production_dependencies':checks,'module_72369db_exact':True,'artifact_seals_checked':manifest.exists()},indent=2))
associations=json.loads((HERE/'associations.json').read_text());registry=ROOT/'docs/research/command-scenarios.json'
assert hashlib.sha256(registry.read_bytes()).hexdigest()==associations['registry_sha256']
cases={r['id']:r for r in json.loads(registry.read_text())}
def semantic(a):
    b=cases[a['id']]
    for key in ['title','feature_ids','requirement_ids','oracle_status','implementation_status','source_locators']:assert a[key]==b[key],(a['id'],key)
for a in associations['associations']:semantic(a)
wrong=dict(associations['associations'][0]);wrong['feature_ids']=['WP51-020']
try:semantic(wrong)
except AssertionError:pass
else:raise AssertionError('wrong feature accepted')
print('Seven exact semantic case/title/feature/status/locator associations checked; wrong-feature negative rejects')
# Validate actual final capture/helper/input custody, independently of Go's VCS stamp.
run=HERE/'pty-final-02';inputs=json.loads((run/'inputs.json').read_text())
for path,fact in inputs['working_source_inputs'].items():
    raw=(ROOT/path).read_bytes();assert len(raw)==fact['size'] and hashlib.sha256(raw).hexdigest()==fact['sha256'],path
assert (run/'runner.py.txt').read_bytes()==(HERE/'pty_test.py').read_bytes()
for path,fact in json.loads((run/'manifest.json').read_text()).items():
    raw=(run/path).read_bytes();assert len(raw)==fact['size'] and hashlib.sha256(raw).hexdigest()==fact['sha256'],path
for name in ['ascii','block-restore','repair-restore','normal-question','host-signal']:
    result=json.loads((run/name/'result.json').read_text());assert result['binary']==inputs['binary'] and result['termios_restored'] and not result['physical_qualified']
    assert result['returncode']==(1 if name=='host-signal' else 0)
    assert (run/name/'files/ORIGIN').read_bytes()==(ROOT/'docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5').read_bytes()
assert (run/'block-restore/files/COPY').read_bytes()==(ROOT/'docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/RESTORED.WP5').read_bytes()
for repeat in ['r1','r2']:
    assert (run/'repair-restore/files/COPY').read_bytes()==(ROOT/('docs/research/continuation/native-edits/runs/wp23-b-history-follow-repair-restore-'+repeat+'/N0001.WP5')).read_bytes()
print('Final5 PTY custody/source/module/native/expected-original-byte joins pass; stamps are metadata only')
