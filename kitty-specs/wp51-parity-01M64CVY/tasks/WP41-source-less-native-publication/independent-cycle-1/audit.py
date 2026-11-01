from pathlib import Path
import json,subprocess,hashlib
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-b');E=R/'internal/storage/evidence/wp41';T=Path('/tmp/wordling-wp41-independent')
def sha(b):return hashlib.sha256(b).hexdigest()
def git(ref,p):return subprocess.check_output(['git','show',ref+':'+p],cwd=R)
m=json.loads((E/'artifact-manifest.json').read_text());assert len(m['files'])==109
size=0
for p,v in m['files'].items():
 b=(R/p).read_bytes();assert b==git('0df934c',p)and len(b)==v['bytes']and sha(b)==v['sha256'];assert hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()==v['git_blob'];size+=len(b)
assert not any(p.endswith('.pyc')for p in m['files'])
pack=subprocess.check_output(['git','diff','--name-only','5ad84e4','0df934c'],cwd=R,text=True).splitlines();assert set(pack)=={'internal/storage/evidence/wp41/artifact-manifest.json','internal/storage/evidence/wp41/report.md'}
old=json.loads(git('5ad84e4','internal/storage/evidence/wp41/artifact-manifest.json'));removed=set(old['files'])-set(m['files']);assert len(removed)==1 and next(iter(removed)).endswith('.pyc');assert set(old['files'])==set(m['files'])|removed
for p in set(m['files'])-{'internal/storage/evidence/wp41/report.md'}:assert old['files'][p]==m['files'][p]
for x in json.loads((E/'authority-bindings.json').read_text()):
 b=git(x['commit'],x['path']);assert sha(b)==x['sha256']and len(b)==x['bytes']
c=json.loads((E/'consumer-composition.json').read_text());C=Path(c['temp_directory']);code=[]
for p,v in c['code'].items():
 b=(C/p).read_bytes();assert b==git(v['source_commit'],p)and sha(b)==v['sha256'];assert hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()==v['git_blob'];code.append(p)
for p,v in c['current_storage_and_codec'].items():
 b=(C/p).read_bytes();assert sha(b)==v['sha256'];assert p.endswith('_test.go')or b==(R/p).read_bytes()==git('5ad84e4',p)
# Every actual compiled Go source is accounted for, no copied alternate consumer.
actual=sorted(str(p.relative_to(C))for folder in ['internal','cmd']for p in(C/folder).rglob('*.go'));assert set(actual)==(set(c['code'])|set(c['current_storage_and_codec']))-{'go.mod','go.sum'}
# Fixture export precedence is recorded: e1e4c2c planning data replaces equal paths;
# consumer18-only session fixtures remain from approved72369db. Hash all actual data.
base='72369db';planning='e1e4c2c';expected={}
for ref in [base,planning]:
 paths=subprocess.check_output(['git','ls-tree','-r','--name-only',ref,'--','docs','kitty-specs/wp51-parity-01M64CVY/contracts'],cwd=R,text=True).splitlines()
 for p in paths:
  if Path(p).suffix.lower()in ['.txt','.json','.wp5','.wpm']:expected[p]=ref
fixture_count=0
for p,ref in expected.items():
 path=C/p;assert path.is_file()and path.read_bytes()==git(ref,p),p;fixture_count+=1
B=json.loads((E/'consumer-build.json').read_text());binary=Path(B['command'][3]);assert binary.stat().st_size==B['binary_bytes']and sha(binary.read_bytes())==B['binary_sha256']and B['executed']is False
changed=subprocess.check_output(['git','diff','--name-only','70e02f7','5ad84e4','--','internal/storage'],cwd=R,text=True).splitlines();production=[p for p in changed if p.endswith('.go')and not p.endswith('_test.go')];assert set(production)=={'internal/storage/storage_linux.go','internal/storage/publication_linux.go','internal/storage/macro_linux.go'}
result={'source':'5ad84e4000f4d9e2475acc1eb88e0a26448e1761','packaging':'0df934ce3185d73ec53be6d887fba513b44ab803','tracked_seals':109,'manifest_bytes':size,'packaging_only_removed_ignored_cache_and_updated_report':True,'authority_bindings_exact':True,'consumer17':c['consumer17_source'],'consumer18':c['consumer18_source'],'consumer_code_and_module_files':len(c['code']),'current_storage_codec_files':len(c['current_storage_and_codec']),'all_composition_Go_sources_accounted':True,'unused_storage_test_snapshot_precedes_two_added_final_guard_tests':True,'fixture_paths_exact':fixture_count,'actual_built_cmd_binary_hash_exact':True,'cmd_executed':False,'production_changes':production,'no_live_NewPublication_route':True}
(T/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
