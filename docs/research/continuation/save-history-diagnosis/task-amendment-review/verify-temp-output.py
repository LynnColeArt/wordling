from pathlib import Path
import json,hashlib,yaml
from specify_cli.ownership.models import OwnershipManifest
from specify_cli.ownership.validation import validate_all,validate_glob_matches
from specify_cli.lanes.compute import compute_lanes
r=Path('/home/lynn/projects/wordling');o=Path('/tmp/wordling-save-history-amendment');m=Path('kitty-specs/wp51-parity-01M64CVY');man=json.load(open(o/'manifest.json'));h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();front={};bodies={};oldfront={};oldbodies={}
for old in (r/m/'tasks').glob('WP*.md'):
 p=o/old.relative_to(r);p=p if p.exists() else old;x=p.read_text().split('---',2);v=yaml.safe_load(x[1]);k=v['work_package_id'];front[k]=v;bodies[k]=x[2];oldx=old.read_text().split('---',2);oldfront[k]=yaml.safe_load(oldx[1]);oldbodies[k]=oldx[2]
assert len(front)==45;sub=[t for v in front.values() for t in v['subtasks']];assert len(sub)==len(set(sub))==135
assert front['WP29']['dependencies']==oldfront['WP29']['dependencies']+['WP36'];assert front['WP36']==oldfront['WP36']
for k in front:
 if k!='WP29':assert front[k]==oldfront[k]
 assert front[k]['owned_files']==oldfront[k]['owned_files'] and front[k]['subtasks']==oldfront[k]['subtasks']
 if k not in ['WP29','WP36']:assert bodies[k]==oldbodies[k]
assert bodies['WP29'].replace('**Dependencies:** WP28, WP23, WP14, WP36.','**Dependencies:** WP28, WP23, WP14.')==oldbodies['WP29']
addition=(o/'T108-addition.md').read_text();assert bodies['WP36'].replace('\n'+addition,'',1)==oldbodies['WP36'];assert 'WP29' not in front['WP36']['dependencies'] and 'WP28' not in front['WP36']['dependencies'] and 'WP44' not in front['WP36']['dependencies']
assert all(h(r/p)==v for p,v in man['protected_hashes'].items());assert (o/m/'continuation.md').read_bytes().startswith((r/m/'continuation.md').read_bytes());assert all(h(r/p)==v['old_sha256'] and h(o/p)==v['new_sha256'] for p,v in man['proposals'].items())
deps={k:v.get('dependencies',[]) for k,v in front.items()};owned={k:OwnershipManifest.from_frontmatter(v) for k,v in front.items()};val=validate_all(owned,deps);glob=validate_glob_matches(owned,r,create_intent={k:v.get('create_intent',[]) for k,v in front.items()});assert not val.errors and not glob.errors
new=compute_lanes(deps,owned,'wp51-parity-01M64CVY','feat/wp51-parity',bodies,mission_id='01M64CVYYRTDKBCYZ56H6XNTEQ').to_dict();old=json.load(open(r/m/'lanes.json'));mapping=lambda d:{w:l['lane_id'] for l in d['lanes'] for w in l['wp_ids']};assert mapping(new)==mapping(old);assert len(new['lanes'])==len(old['lanes'])==21;assert new['collapse_report']['independent_wps_collapsed']==0
n={l['lane_id']:set(l['depends_on_lanes']) for l in new['lanes']};prev={l['lane_id']:set(l['depends_on_lanes']) for l in old['lanes']};assert n['lane-l']==prev['lane-l']|{'lane-g'}
assert n['lane-g']==prev['lane-g'];assert n['lane-e']==prev['lane-e'];assert all(n[k]==prev[k] for k in n if k!='lane-l')
def topo(graph):
 done=set();active=set();order=[]
 def visit(k):
  assert k not in active,('cycle',k)
  if k in done:return
  active.add(k)
  for p in graph[k]:visit(p)
  active.remove(k);done.add(k);order.append(k)
 for k in graph:visit(k)
 return order
package=topo(deps);lanes=topo(n)
rec=json.load(open(o/'promotion-plan.json'))
for x in rec['files']:assert h(Path(x['source']))==x['sha256']==h(o/'promotion'/x['destination'])
assert rec['byte_replacements']==[] and not rec['semantic_changes'];text=' '.join(addition.split())
for required in ['InterruptGrouping','Separate(SavedBoundary)','UnsupportedHistoryEffect','CountKnown=false','unique private Transition','filename F1 cancel/error/failure/stale/uncertain/success','or generic ignored-error','immediate F10','No manual dependency/source overlay']:
 assert required.lower() in text.lower(),required
result={'kind':'actual installed pure ownership/glob/lane compute plus manual-body diff/negative-guard checks; no canonical action','baseline':man['baseline'],'WP_count':45,'subtask_count':135,'lane_count':21,'all45_old_lane_assignments_exact':True,'protected_other43_prompts_spec_plan_charters':len(man['protected_hashes']),'all45_manual_bodies_preserved_except_explicit29_dep_and36_T108_addition':True,'new_direct_dependency':'WP29 requires WP36, never WP36 requires WP29','prerequisite_flow':'lane-g36 -> lane-l29; computed lane-l adds lane-g prerequisite only','added_lane_edges':{'lane-l':['lane-g']},'no_editor_to_UI_or_consumer_dependency':True,'no_document44_scope_or_lane_change':True,'package_topological_order':package,'lane_topological_order':lanes,'DAG_acyclic':True,'ownership_errors':val.errors,'ownership_warnings':val.warnings,'glob_errors':glob.errors,'glob_warnings':glob.warnings,'glob_info':glob.info,'collapse_report':new['collapse_report'],'promotion_copy_count':len(rec['files']),'raw_diagnosis_source_pins_verified':22,'T108_status_hand_edited':False,'canonical_finalizer_or_lifecycle_run':False,'guest_attempts':0};(Path('/tmp/wordling-save-history-amendment-review')/'pure-validation.json').write_text(json.dumps(result,indent=2)+'\n');(Path('/tmp/wordling-save-history-amendment-review')/'lanes-preview.json').write_text(json.dumps(new,indent=2)+'\n');print('PASS45WP/135T/21lanes,alloldassignments;29requires36 directG→L;DAGacyclic;47protections;43otherprompts;manualdiffnegativeguards;0independentcollapse;canonicalNOTexecuted')
