import pathlib,subprocess,json,hashlib
r=pathlib.Path.cwd();o=r/'internal/editor/evidence/wp36/save-history';sha=lambda b:hashlib.sha256(b).hexdigest();git=lambda *x:subprocess.check_output(['git',*x],text=False)
# Historical manifests stay frozen. Source repair changes precisely two current source entries.
inputs=[]
for x in json.loads((r/'internal/editor/evidence/wp36/source-inputs.json').read_text()):
 b=(r/x['path']).read_bytes();assert sha(b)==x['sha256'];assert subprocess.check_output(['git','hash-object',str(r/x['path'])],text=True).strip()==x['git_blob'];inputs.append(x)
diagnosis=r/'docs/research/continuation/save-history-diagnosis';ds=json.loads((diagnosis/'seals.json').read_text())
for p,x in ds.items():assert sha((diagnosis/p).read_bytes())==x['sha256']
assert sha((diagnosis/'report.md').read_bytes())=='2b09ff85a9d0a10d358617d718e06a6c2a7d66f84f9f5fa3ddf8c09e53ba0ffa'
a=[]
for commit,path in [('5c2a849161b78794b9ba1bf00aa47b787493c7a3','internal/editor/evidence/wp36/artifact-manifest.json'),('2431de0955b705a599303261b083fa30a321a3e5','internal/editor/evidence/wp36/planning-target-sync/artifact-manifest.json')]:
 data=json.loads(git('show',commit+':'+path));rows=[]
 for x in data['records']:
  b=git('show',commit+':'+x['path']);assert sha(b)==x['sha256'];assert git('rev-parse',commit+':'+x['path']).decode().strip()==x['git_blob']
  actual=(r/x['path']).read_bytes();rows.append({'path':x['path'],'historical_git_seal':True,'current_equal':sha(actual)==x['sha256']})
 assert all(x['current_equal'] or x['path'] in ['internal/editor/editing.go','internal/editor/session.go'] for x in rows)
 a.append({'commit':commit,'manifest':path,'verified_count':len(rows),'working_differences':[x['path'] for x in rows if not x['current_equal']]})
pins=[]
for scope,pin in [('internal/document','951903221566629f0df8b4a78c98a03483992c4b'),('internal/macro/runtime','00ea296407985fb2459e72a71d841c8f811a41db'),('internal/storage','0df934ce3185d73ec53be6d887fba513b44ab803')]:
 paths=git('ls-tree','-r','--name-only',pin,scope).decode().splitlines();paths=[p for p in paths if p.endswith('.go') and '/evidence/' not in p];working=sorted(str(p.relative_to(r)) for p in (r/scope).glob('*.go'));assert sorted(paths)==working
 for p in paths:assert git('show',pin+':'+p)==(r/p).read_bytes(),p
 pins.append({'scope':scope,'pin':pin,'go_files':len(paths),'exact_set_and_bytes':True})
# Complete actual discovery/compiled source set, including actual historical test packages.
raw=git if False else subprocess.check_output(['go','list','-json','./...'],text=True);dec=json.JSONDecoder();pk=[]
while raw.strip():obj,end=dec.raw_decode(raw.lstrip());pk.append(obj);raw=raw.lstrip()[end:]
files=[]
for p in pk:
 for kind in ['GoFiles','CgoFiles','TestGoFiles','XTestGoFiles']:
  for f in p.get(kind,[]):
   path=pathlib.Path(p['Dir'])/f;files.append({'path':str(path.relative_to(r)),'kind':kind,'package':p['ImportPath'],'sha256':sha(path.read_bytes())})
for p in ['go.mod','go.sum']:files.append({'path':p,'kind':'module','sha256':sha((r/p).read_bytes())})
old=json.loads((r/'internal/editor/evidence/wp36/compiled-source-inventory.json').read_text());before={x['path']:x['sha256'] for x in old['files']};now={x['path']:x['sha256'] for x in files};added=sorted(now.keys()-before.keys());removed=sorted(before.keys()-now.keys());changed=sorted(p for p in before.keys()&now.keys() if before[p]!=now[p]);assert added==['internal/editor/save_history_internal_test.go','internal/editor/save_history_test.go'];assert not removed;assert changed==['internal/editor/editing.go','internal/editor/session.go'];assert len(pk)==10
(pathlib.Path('/tmp/wordling-wp36-independent')/'compiled-source-inventory.json').write_text(json.dumps({'packages':len(pk),'files':files,'added':added,'removed':removed,'changed':changed},indent=2)+'\n')
native=[]
for p in sorted((o/'native').glob('*')):
 if p.is_file():oldp=r/'internal/editor/evidence/wp36/native'/p.name;assert p.read_bytes()==oldp.read_bytes();native.append({'path':str(p.relative_to(r)),'sha256':sha(p.read_bytes()),'exact_prior_native_output':True})
assert len(native)==48
(pathlib.Path('/tmp/wordling-wp36-independent')/'audit.json').write_text(json.dumps({'source_input_seals_verified':len(inputs),'diagnosis_seals_verified':len(ds),'historical_seals':a,'approved_pins':pins,'native_comparisons':native,'current_product_changes':changed,'test_additions':added,'package_count':len(pk),'compiled_plus_module_files':len(files),'recorded_planning_ancestor':subprocess.run(['git','merge-base','--is-ancestor','074eb519a0dedee3de36762bedfd2d972e04d873','HEAD']).returncode==0,'unreviewed_C92_not_ancestor':subprocess.run(['git','merge-base','--is-ancestor','92beb215322c07482fe8295d1b434f9f96a8d203','HEAD']).returncode==1},indent=2)+'\n');print('historical261+7 verified; document/runtime/storage Go pins exact; 48 native bytes exact; packages',len(pk),'files',len(files))
