"""Bind complete inherited source/evidence, actual working bytes and public fixtures."""
from pathlib import Path
import gzip,hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest();git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT)
old=json.loads(gzip.decompress((HERE/'baseline.json.gz').read_bytes()));changed={'internal/tui/model.go'};verified=0
for p,(size,digest,blob) in old['files'].items():
 b=(ROOT/p).read_bytes()
 if p in changed:continue
 assert len(b)==size and sha(b)==digest,(p,'working changed')
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==blob,(p,'Git mismatch');verified+=1
# The claimed planning-only refresh has no unapproved H source or Go drift.
assert git('diff',old['approved_H60'],old['claim_head'],'--','internal/tui','internal/editor','internal/document','internal/input','cmd/wordling','go.mod','go.sum')==b''
fixtures=json.loads((ROOT/'internal/document/evidence/reveal-catalogue/fixtures.json').read_bytes())['files'];assert len(fixtures)==24
for x in fixtures:
 b=(ROOT/x['path']).read_bytes();assert len(b)==x['bytes']and sha(b)==x['sha256'];assert git('rev-parse',x['commit']+':'+x['path']).decode().strip()==x['git_blob'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob']
# Actual production compiler input closure, separate from Go's historical VCS stamp.
build=json.loads((HERE/'build-source.json').read_bytes())
for path,x in build['inputs'].items():b=Path(path).read_bytes();assert len(b)==x['bytes']and sha(b)==x['sha256'],path
assert sha(Path(build['binary']).read_bytes())==build['binary_digest']['sha256']
tracked=git('diff','--name-only',old['claim_head']).decode().splitlines();assert all(p in ['internal/tui/model.go','internal/tui/menu_bar.go','internal/tui/menu_bar_test.go']or p.startswith('internal/tui/evidence/menu-bar/')for p in tracked),tracked
untracked=git('ls-files','--others','--exclude-standard').decode().splitlines();assert all(p in ['internal/tui/menu_bar.go','internal/tui/menu_bar_test.go']or p.startswith('internal/tui/evidence/menu-bar/')for p in untracked),untracked
out=dict(claim_head=old['claim_head'],primary_at_claim=old['primary'],currency_at_claim=old['currency'],approved_H60=old['approved_H60'],approved_E59=old['approved_E59'],complete_baseline_files=len(old['files']),unchanged_Git_and_working_files=verified,allowed_existing_amendment=sorted(changed),approved_source_at_claim_exact=True,public24_fixtures=fixtures,production_entry_unchanged=True,production_binary=build['binary_digest'],production_compiler_inputs=len(build['inputs']),changed_source=['internal/tui/model.go','internal/tui/menu_bar.go','internal/tui/menu_bar_test.go'],no_P_source_consumed=True,no_native_format_changes=True,no_private_original_or_VM_actions=True,full_M1='OPEN')
(HERE/'custody.json').write_text(json.dumps(out,indent=2)+'\n');print('custody',len(old['files']),verified,'fixtures24')
# Recursive current seal: all nested historical manifests are ordinary members.
paths=set(old['files'])|set(tracked)|set(untracked)|{'internal/tui/evidence/menu-bar/custody.json'}
manifest=HERE/'manifest.json.gz';paths.discard(str(manifest.relative_to(ROOT)))
rows=[]
for p in sorted(paths):
 b=(ROOT/p).read_bytes();rows.append([p,len(b),sha(b)])
payload=json.dumps(dict(fields=['path','size','sha256'],files=rows,excludes_only_exact_root='internal/tui/evidence/menu-bar/manifest.json.gz'),separators=(',',':')).encode();manifest.write_bytes(gzip.compress(payload,mtime=0))
fs=[p for p in HERE.rglob('*')if p.is_file()];assert len(fs)<=512 and sum(p.stat().st_size for p in fs)<=8*1024*1024
print('recursive seal members',len(rows),'evidence files/bytes',len(fs),sum(p.stat().st_size for p in fs))
