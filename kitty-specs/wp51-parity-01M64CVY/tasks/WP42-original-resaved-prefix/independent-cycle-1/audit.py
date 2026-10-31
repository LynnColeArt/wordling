from pathlib import Path
import sys,json,hashlib,subprocess,copy,tempfile
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-s'); O=R/'docs/research/continuation/resaved-prefix'; T=Path('/tmp/wordling-wp42-independent')
sys.path.insert(0,str(R/'scripts/reference'));import resaved_prefix as m
h=lambda b:hashlib.sha256(b).hexdigest()
def save(name,v):(T/name).write_text(json.dumps(v,indent=2)+'\n')
plan=m.plan();assert m.plan_hash(plan)=='9be995e3d696029e672470cbf571baf75464de7ec244fa44a095e1097c104558';assert len(plan['sources'])==29
ledger=json.loads((R/'docs/research/continuation/native-edits/field-ledger.json').read_text());hand=json.loads((O/'field-ledger.json').read_text());families=json.loads((O/'family-admission.json').read_text());summary=json.loads((O/'evidence/matrix-summary.json').read_text())
assert hand['source_field_ledger_sha256']==h((R/'docs/research/continuation/native-edits/field-ledger.json').read_bytes())
allrows=[];custody=[]
for recipe in plan['cases']:
 folder=O/'runs'/recipe['run_id'];run=json.loads((folder/'run.json').read_text());pre=json.loads((folder/'prelaunch.json').read_text())
 assert m.plan_hash(pre['plan'])==m.plan_hash(plan) and pre['plan_sha256']==m.plan_hash(plan)
 assert pre['argv']==recipe['run_argv'][1:],(pre['argv'],recipe['run_argv'])
 assert run['guard_released'] and run['master_unchanged'] and run['master_before']==run['master_after']==plan['master']
 for pin in plan['sources']:
  b=(folder/'runner-source'/pin['path']).read_bytes();assert h(b)==pin['sha256'] and len(b)==pin['size']
 result=m.result(folder/'run.json');save(recipe['id']+'-result.json',result)
 assert len(result['rows'])==2
 for row in run['results']:
  i=row['repetition'];f=folder/f'r{i}';assert row['qemu_argv']==recipe['qemu_argv'][i-1]
  assert row['guest_stopped'] and row['stop_evidence']['confirmed'] and row['owned_pid']==row['stop_evidence']['pid']
  for e in row['exports']:assert h((folder/e['path']).read_bytes())==e['sha256']
  assert (f/'qmp-wire.jsonl').stat().st_size>0
  screen=(f/'clean-exit/screen.txt').read_text();assert 'C:\\WP51>' in screen
  custody.append({'case':recipe['id'],'repetition':i,'owned_pid':row['owned_pid'],'argv':row['qemu_argv'],'stop':row['stop_evidence'],'settings_before':row['settings_before'],'settings_after':row['settings_after'],'wire_sha256':h((f/'qmp-wire.jsonl').read_bytes())})
 for name in recipe['native_exports']+[recipe['print_export']]:assert (folder/'r1'/name).read_bytes()==(folder/'r2'/name).read_bytes()
 for obs in result['rows'][0]['observations']:
  name=obs['name'];a=obs['audit'];raw=(folder/'r1'/name).read_bytes(); item=next(x for x in hand['artifacts'] if x['case']==recipe['id'] and x['artifact']==name)
  assert len(item['fields'])==item['field_count']==72 and not item['mutation_permission']
  covered=set()
  for old,new,f in zip(ledger['field_coverage'],item['fields'],a['inherited_field_observations'],strict=True):
   assert all(new[k]==old[k] for k in ['name','owner','width','representation','units'])
   assert new['relative_owner_offset']==old['offset'] and new['reference_authority']==old['references']
   assert all(new[k]==f[k] for k in f)
   p=0 if old['owner']=='header' else next(p['offset'] for p in a['packets'] if p['type']==int(old['owner'].split('-')[1]))
   assert new['offset']==p+old['offset'];assert raw[new['offset']:new['offset']+new['width']].hex()==new['raw_hex']
   covered.update(range(new['offset'],new['offset']+new['width']))
  wanted=set(range(16))
  for p in a['packets']:
   if p['type'] not in [0,65535]:wanted.update(range(p['offset'],p['offset']+p['length']))
  assert covered==wanted and all(x['bounds_valid'] for x in a['candidate_relationships'])
  assert a['actual_go_reader']['accepted'] and a['actual_go_reader']['exact_export'] and not a['mutation_permission']
  fam=next(x for x in families['families'] if x['case']==recipe['id']);stage=next(x for x in fam['phases'] if x['name']==name)
  assert stage['native_sha256']==h(raw) and stage['prefix_bytes']==a['body_offset'] and stage['prefix_sha256']==h(raw[:a['body_offset']])
  assert not fam['future_write_permission'] and not fam['mutation_permission']
  allrows.append({'case':recipe['id'],'name':name,'sha256':h(raw),'body_offset':a['body_offset'],'fields':72,'reader_exact_repetitions':2,'links':a['candidate_relationships']})
 off=result['rows'][0]['observations'][3]['audit']['body_offset'];g=(folder/'r1/W42G3.WP5').read_bytes();e=(folder/'r1/W42EDIT.WP5').read_bytes();assert g[:off]==e[:off] and e[off:]==b'X'+g[off:]
 assert (folder/'r1/W42G2.WP5').read_bytes()==g
save('fields-reader-custody.json',{'plan_sha256':m.plan_hash(plan),'sources':29,'attempts':12,'native_reopens':72,'stages':allrows,'custody':custody,'mutation_permission':False})
# Read actual committed Git objects independently, once per unique object.
manifest=json.loads((O/'evidence/matrix-artifacts.json').read_text());files=manifest['files'];tree=subprocess.check_output(['git','ls-tree','-r','-z','HEAD'],cwd=R);ids={}
for line in tree.split(b'\0'):
 if line:
  head,path=line.split(b'\t',1);ids[path.decode()]=head.split()[2].decode()
byid={}
for f in files:byid.setdefault(ids[f['path']],[]).append(f)
p=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
for oid,entries in byid.items():
 p.stdin.write((oid+'\n').encode());p.stdin.flush();line=p.stdout.readline().split();size=int(line[2]);b=p.stdout.read(size);assert p.stdout.read(1)==b'\n'
 for f in entries:assert size==f['size'] and h(b)==f['sha256'] and (R/f['path']).read_bytes()==b
p.stdin.close();assert p.wait()==0
save('git-raw.json',{'count':len(files),'bytes':sum(f['size'] for f in files),'unique_objects':len(byid),'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'all_actual_git_and_worktree_exact':True})
# Real post-run semantic refusals, copying only metadata/capture paths to temporary overlay.
base=O/'runs/w42-two-bold-disabled';original=json.loads((base/'run.json').read_text());neg=[]
for kind in ['source','generation','fast-save','dos','body']:
 with tempfile.TemporaryDirectory() as td:
  folder=Path(td)
  for i in [1,2]:
   dest=folder/f'r{i}';dest.mkdir()
   for f in (base/f'r{i}').iterdir():(dest/f.name).symlink_to(f,target_is_directory=f.is_dir())
  d=copy.deepcopy(original)
  if kind=='source':d['preparation']['profile_sha256']='0'*64;d['plan_sha256']=m.plan_hash(d['preparation'])
  elif kind=='generation':d['results'][0]['phases'][3]['name']='invented-generation'
  elif kind=='fast-save':d['results'][0]['fast_save']['before']='no'
  elif kind=='dos':p=folder/'r1/clean-exit';p.unlink();p.mkdir();(p/'screen.txt').write_text('not DOS')
  elif kind=='body':
   p=folder/'r1/W42G3.WP5';b=bytearray(p.read_bytes());b[-1]=ord('Q');p.unlink();p.write_bytes(b);e=next(e for e in d['results'][0]['exports'] if e['path']=='r1/W42G3.WP5');e['sha256']=h(b);e['size']=len(b)
  p=folder/'run.json';p.write_text(json.dumps(d))
  try:m.result(p);raise AssertionError('negative accepted '+kind)
  except m.Refusal as e:neg.append({'mutation':kind,'refusal':e.code,'detail':e.detail})
save('semantic-negatives.json',neg)
print('PASS actual results/72 readers/36x72 fields/12 custody/Git raw/5 semantic negatives',flush=True)
