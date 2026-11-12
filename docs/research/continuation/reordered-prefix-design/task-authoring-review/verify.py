from pathlib import Path
import json,hashlib,subprocess,yaml,re,fnmatch
O=Path('/tmp/wordling-prefix-expansion-tasks');P=Path('/home/lynn/projects/wordling');M=Path('kitty-specs/wp51-parity-01M64CVY');T=Path('/tmp/wordling-prefix-expansion-tasks-review');h=lambda b:hashlib.sha256(b).hexdigest()
assert h((O/'seals.json').read_bytes())=='d5bd708ccf948f97a83edb6006b2bd0383a2043d7dab74832d9dd534b8bbac1a';assert h((O/'promotion-manifest.json').read_bytes())=='99e63be4b18f47b4268c54eed1f5f073a762b95080e51a6c3aaa0db27219f001';seal=json.loads((O/'seals.json').read_text());assert len(seal['files'])==202
for n,v in seal['files'].items():b=(O/n).read_bytes();assert len(b)==v['size'] and h(b)==v['sha256']
prom=json.loads((O/'promotion-manifest.json').read_text());assert len(prom['entries'])==36
allowed={str(M/'tasks.md'),str(M/'continuation.md'),str(M/'tasks/WP44-reordered-prefix-mutation.md'),str(M/'tasks/WP45-resaved-prefix-relationships.md')};dest=[]
for row in prom['entries']:
 b=Path(row['source']).read_bytes();assert h(b)==row['sha256'];d=row['destination'];assert d in allowed or d.startswith('docs/research/continuation/reordered-prefix-design/');dest.append(d)
assert len(set(dest))==36 and not any('/tasks/WP27-' in x for x in dest)
receipt=json.loads((O/'promotion/docs/research/continuation/reordered-prefix-design/promotion-receipt.json').read_text());assert len(receipt['files'])==30 and not receipt['content_replacements'] and not receipt['semantics_changed']
for row in receipt['files']:
 b=Path(row['source']).read_bytes();assert b==(O/'promotion'/row['destination']).read_bytes() and h(b)==row['sha256']
baseline=json.loads((O/'protected-baseline.json').read_text());runtime=[];protected=0
for name,w in baseline['files'].items():
 b=subprocess.check_output(['git','show',baseline['primary_head']+':'+name],cwd=P);assert len(b)==w['size']and h(b)==w['sha256'];live=(P/name).read_bytes()
 if name.startswith(str(M/'tasks')+'/') and name.endswith('.md'):
  assert (O/name).read_bytes()==b;protected+=1
  if live!=b:
   assert name==str(M/'tasks/WP27-editable-session-reducer.md') and live.startswith(b);tail=live[len(b):];assert tail.lstrip().startswith(b'## Activity Log\n');runtime.append({'path':name,'tail_sha256':h(tail),'tail_bytes':len(tail),'live_sha256':h(live)})
 else:assert live==b
assert protected==43
for name in [str(M/'tasks.md'),str(M/'continuation.md')]:
 old=subprocess.check_output(['git','show',baseline['primary_head']+':'+name],cwd=P);assert (O/name).read_bytes().startswith(old);assert (P/name).read_bytes()==old
r=json.loads((O/'runtime-snapshot/receipt.json').read_text());assert r['authorized_fix_event']=='01M68FK09ZPT2VPBEYBXHS7MRX';assert runtime and runtime[0]['tail_sha256']==r['history_tail_sha256'];assert (O/'runtime-snapshot/WP27-current.md').read_bytes()==(P/r['path']).read_bytes()
packages={}
for p in (O/M/'tasks').glob('WP*.md'):
 f=yaml.safe_load(p.read_text().split('---',2)[1]);packages[f['work_package_id']]=f
assert len(packages)==45;ids=[t for f in packages.values()for t in f['subtasks']];assert len(ids)==135 and len(set(ids))==135 and set(ids)=={f'T{i:03}'for i in range(1,136)}
assert packages['WP44']['dependencies']==['WP25','WP26','WP42'] and packages['WP44']['owned_files']==['internal/document/**'];assert packages['WP45']['dependencies']==['WP23','WP14','WP22','WP39','WP42'];assert packages['WP45']['owned_files']==['scripts/reference/resaved_prefix_relationships.py','docs/research/continuation/resaved-prefix-relationships/**'];assert len(packages['WP45']['create_intent'])==2
oldlanes=json.loads((P/M/'lanes.json').read_text());mapping={w:l['lane_id'] for l in oldlanes['lanes'] for w in l['wp_ids']};assert len(mapping)==43 and len(set(mapping.values()))==21;mapping.update(WP44='lane-e',WP45='lane-s');deps={w:f['dependencies']for w,f in packages.items()}
def topo(g):
 done=set();pending=set(g)
 while pending:
  ready={k for k in pending if set(g[k])<=done};assert ready,'cycle';done|=ready;pending-=ready
 return len(done)
assert topo(deps)==45
lanes={l['lane_id']:set(l['depends_on_lanes']) for l in oldlanes['lanes']};old={k:set(v) for k,v in lanes.items()}
for w,ps in deps.items():
 for p in ps:
  if mapping[w]!=mapping[p]:lanes[mapping[w]].add(mapping[p])
assert topo(lanes)==21 and {k:sorted(v-old[k])for k,v in lanes.items()if k in old and v!=old[k]}=={'lane-e':['lane-s']};assert lanes['lane-s']=={'lane-d','lane-j','lane-k','lane-q'}
a=json.loads(Path('/tmp/wordling-prefix-expansion-architecture/manifest.json').read_text())
for p in a['source_pins']:
 b=(Path(p['checkout'])/p['path']).read_bytes();assert len(b)==p['size']and h(b)==p['sha256']
for p in a['original_image_pins']:
 b=(P/'.worktrees/wp51-parity-01M64CVY-lane-s'/p['path']).read_bytes();assert len(b)==p['size']and h(b)==p['sha256']
neg=json.loads((O/'negative-checks.json').read_text());assert len(neg['tests'])==10 and all(x['rejected']for x in neg['tests'])
(T/'verification.json').write_text(json.dumps({'input202seals_exact':True,'promotion36exact_and_only_four_authored_mission_targets':True,'design_history_cycle2_30byte_exact_copies':True,'old43prompt_instruction_prefixes_exact':True,'only_live_runtime_delta':runtime,'all_other_protections_exact':True,'45WPs135subtasks21lanes':True,'all21priorIDs_retained':True,'44lane':'lane-e','45lane':'lane-s','added_old_lane_edge':'lane-s -> lane-e','actual_source_pins':len(a['source_pins']),'actual_original_image_pins':len(a['original_image_pins']),'author10draftnegative_results_not_product_tests':True,'canonical_finalizer_or_analysis_executed':False,'primary_mutations':False,'new_VM':False},indent=2)+'\n');print('PASS202seals36promotion30exactcopies/43oldprefixesWP27onlyhistory/45WP135T21laneDAG/sourcepins/originals')
