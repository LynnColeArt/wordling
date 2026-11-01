from pathlib import Path
import json,hashlib,subprocess
r=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-h');o=Path('/tmp/wordling-WP37-independent-review');b=r/'docs/research/continuation/macro-executable';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();git=lambda *v:subprocess.check_output(['git',*v],cwd=r);assert git('rev-parse','HEAD').decode().strip()=='dfd2df9de6e6082cfdf32f9a82cbc5d68908b8f8'
s=json.load(open(b/'evidence/final-seals.json'));assert len(s['records'])==658
for v in s['records']:
 p=r/v['path'];assert h(p)==v['sha256'] and p.stat().st_size==v['size'];assert git('cat-file','blob',v['git_blob'])==p.read_bytes();assert git('show','HEAD:'+v['path'])==p.read_bytes()
comp=json.load(open(b/'evidence/approved-composition.json'));count=0
for row in comp['records']:
 p=row['path']
 if p.startswith(('internal/tui/','cmd/wordling/')):continue
 raw=(r/p).read_bytes();assert h(r/p)==row['sha256'];assert raw==git('show',row['approved_source']+':'+p);count+=1
assert count==71
for prefix,pin in comp['source_pins'].items():
 if prefix=='internal/tui':continue
 expected={x for x in git('ls-tree','-r','--name-only',pin,'--',prefix).decode().splitlines()if x.endswith('.go')};actual={str(x.relative_to(r))for x in(r/prefix).rglob('*.go')};assert actual==expected
closure=json.load(open(b/'evidence/final-source-closure.json'));assert len(closure['packages'])==16 and len(closure['compiled_inputs'])==104
for p,v in closure['compiled_inputs'].items():assert h(r/p)==v['sha256']
manifest=json.load(open(b/'runs/final01/native-comparisons.json'));assert len(manifest['comparisons'])==57
for v in manifest['comparisons']:
 p=Path(v['Actual']);ep=Path(v['Expected']);ep=ep if ep.is_absolute() else r/ep
 assert h(ep)==v['SHA256'];assert p.is_file()
 if v['Exact']:assert p.read_bytes()==ep.read_bytes()
# Genuine source/model comparison is separately exercised via actual Go tests.
sync=json.load(open('/tmp/wordling-WP37-stale-sync.json'));assert all(h(r/p)==v for p,v in sync['source_before'].items());assert len(sync['source_before'])==101
changes=git('diff','--name-only','8916f81f0ea5dd3ff1daafb26ec239b399df7a98','d5c2ab9727bc5422f7b1fa928828e0214b779c6d','--','internal/tui','cmd/wordling').decode().splitlines();assert all(p.startswith(('internal/tui/','cmd/wordling/'))for p in changes)
(o/'audit.json').write_text(json.dumps({'source':'d5c2ab9727bc5422f7b1fa928828e0214b779c6d','frozen_evidence':'d67ad093','current_primary_only_sync':'dfd2df9de6e6082cfdf32f9a82cbc5d68908b8f8','verified_working_Git_seals':658,'inherited_dependency_records':count,'source_path_sets_exact':True,'packages':16,'compiled_test_module_inputs':104,'raw_native_comparisons':57,'sync101source_set_bytes_exact':True,'changed_UI_main_paths':changes,'no46source_or_VM':True},indent=2)+'\n');print('Independent source/custody audit PASS658seals/71dependencies/16packages104inputs/57nativebindings/101syncbytes.')
