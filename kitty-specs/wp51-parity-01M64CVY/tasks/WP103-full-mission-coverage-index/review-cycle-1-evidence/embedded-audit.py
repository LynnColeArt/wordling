from pathlib import Path
import collections,hashlib,json,re,subprocess
root=Path.cwd();base='kitty-specs/wp51-parity-01M64CVY'
p=root/base/'contracts/mission1-closeout-coverage.json';d=json.loads(p.read_text());nodes=d['nodes'];byid={n['id']:n for n in nodes}
assert len(byid)==len(nodes)
commit=d['execution_snapshot']['commit'];pins={x['path']:x for x in d['source_bindings']};cache={}
for path,pin in pins.items():
 b=subprocess.check_output(['git','show',commit+':'+path]);assert len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256'],path
 assert subprocess.check_output(['git','rev-parse',commit+':'+path],text=True).strip()==pin['git_blob'],path
 cache[path]=b
j=lambda path:json.loads(cache[path])
sets=[('canonical-scenario','scenario_id', {x['id'] for x in j('docs/research/command-scenarios.json')},244),('canonical-feature-parent','parent_id',{x['id'] for x in j('docs/research/feature-inventory.json')},91),('canonical-workbook-lesson','lesson_id',{'WB'+str(x['lesson']).zfill(2) for x in j('docs/research/workbook-map.json')},36),('proposed-delivery-family','family_id',{x['id'] for x in j(base+'/continuation-2026-11-18/full-family-backlog.json')['families']},49),('mission-obligation','obligation_id',{x['id'] for x in j(base+'/continuation-2026-11-18/acceptance-closure-contract.json')['criteria']},38),('mission-success-criterion','success_id',set(j(base+'/continuation-2026-11-18/acceptance-closure-contract.json')['success_criteria']),5)]
for kind,key,expected,count in sets:
 rows=[n for n in nodes if n['kind']==kind];assert len(rows)==count and {n[key] for n in rows}==expected,kind
refkeys={'depends_on','scenario_refs','parent_refs','obligation_refs','family_refs','remaining_gap_refs','source_span_refs','known_leaf_refs','known_direct_leaf_refs','thematic_lesson_refs','lesson_refs','lessons','wp_refs'}
pathkeys={'source_refs','original_evidence_refs','current_evidence_refs'}
for n in nodes:
 for obj in [n,n.get('coverage_links',{})]:
  for key in refkeys:
   assert all(ref in byid for ref in obj.get(key,[])),(n['id'],key)
 for key in ['assignment_ref','pending_gap_ref','source_batch_ref','lesson_ref']:
  if n.get(key):assert n[key] in byid,(n['id'],key)
 for key in ['source_ref','task_ref','canonical_matrix_ref']:
  if n.get(key):assert n[key] in pins,(n['id'],key)
 for key in pathkeys:assert all(path in pins for path in n.get(key,[])),(n['id'],key)
 if n.get('variant_profile_ref'):assert n['variant_profile_ref'] in d['variant_profiles']
 # Verify every projected documentary record against its pinned exact source pointer.
 if 'json_pointer' in n:
  raw=cache[n['source_ref']].decode()
  parts=n['json_pointer'].split('/')
  if parts[0]=='embedded-ledger':value=json.loads(re.search(r'```json\n(.*?)\n```',raw,re.S)[1]);parts=parts[1:]
  else:value=json.loads(raw);parts=parts[1:]
  for part in parts:value=value[int(part)] if isinstance(value,list) else value[part]
  if isinstance(value,dict):assert all(value[key]==val for key,val in n['record'].items()),n['id']
  else:assert n['record']['source_value_type']==type(value).__name__,n['id']
seen=set();active=set()
def walk(id):
 assert id not in active,('cycle',id)
 if id in seen:return
 active.add(id)
 for dep in byid[id].get('depends_on',[]):walk(dep)
 active.remove(id);seen.add(id)
for id in byid:walk(id)
assert len([n for n in nodes if n['kind'] in ['documentary-workbook_steps','documentary-numbered_steps']])==1935
assert len([n for n in nodes if n['kind']=='pending-source-span'])==431
assert len([n for n in nodes if n['kind']=='pending-uncovered-start'])==9
assert len([n for n in nodes if n['kind']=='negative-invariant'])==8
assert byid['prerequisite:backup-contract']['status']=='pending'
assert byid['condition:ALL_DELIVERY_AND_LEAF_CLOSURE']['status']=='pending'
assert 'family:Q4' not in byid['condition:ALL_DELIVERY_AND_LEAF_CLOSURE']['depends_on']
assert byid['wp:WP106']['status_at_snapshot']=='approved' and byid['wp:WP107']['status_at_snapshot']=='planned'
assert byid['wp:WP108']['status_at_snapshot']=='planned' and 'wp:WP108' in byid['wp:WP104']['depends_on']
assert len([n for n in nodes if n['kind']=='registered-work-package'])==108
assert d['audit_summary']=={'verified':186,'partial':38,'unimplemented':20}
assert d['canonical_matrix_snapshot']==j(base+'/acceptance-matrix.json')
assert d['canonical_matrix_snapshot']['overall_verdict']=='pending'
assert all(x['pass_fail']=='pending' for x in d['canonical_matrix_snapshot']['criteria'])
for n in nodes:
 if n['kind'] in {'mission-obligation','mission-success-criterion','negative-invariant'}:assert n['status']=='pending'
assert d['execution_snapshot']['new_Mac_testing'] is False and d['execution_snapshot']['reference_actions']==0
print(json.dumps({'result':'PASS','snapshot_commit':commit,'nodes':len(nodes),'source_pins':len(pins),'typed_links':'resolved','dependencies':'acyclic','documentary_pointers':'exact','counts':{key:d['counts'][key] for key in ['scenarios','parents','lessons','families','obligations','success_criteria','negative_invariants','registered_work_packages','committed_numbered_workbook_steps','concordance_source_entries']},'acceptance':'pending; index integrity only'},indent=2))
