from pathlib import Path
import json,hashlib,yaml,re
from specify_cli.ownership.models import OwnershipManifest
from specify_cli.ownership.validation import validate_all,validate_glob_matches
from specify_cli.lanes.compute import compute_lanes
r=Path('/home/lynn/projects/wordling');o=Path('/tmp/wordling-native-constructor-tasks');m=Path('kitty-specs/wp51-parity-01M64CVY');man=json.load(open(o/'draft-manifest.json'));h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();paths=list((r/m/'tasks').glob('WP*.md'))+[Path(v['path']) for v in man['dependency_draft_inputs'].values()]+[o/man['proposed_WP46']['path']];fm={};bodies={}
for p in paths:
 pieces=p.read_text().split('---',2);d=yaml.safe_load(pieces[1]);k=d['work_package_id'];assert k not in fm;fm[k]=d;bodies[k]=pieces[2]
assert len(fm)==46;tasks=[t for d in fm.values() for t in d['subtasks']];assert len(tasks)==len(set(tasks))==138 and set(tasks)=={f'T{i:03}' for i in range(1,139)}
assert fm['WP46']['dependencies']==['WP25','WP26','WP43','WP44'] and fm['WP46']['owned_files']==['internal/document/**'] and fm['WP46']['execution_mode']=='code_change' and fm['WP46']['create_intent']==[]
assert all(h(r/p)==s for p,s in man['protected_hashes'].items());assert all(h(Path(v['path']))==v['sha256'] for v in man['dependency_draft_inputs'].values());assert len([p for p in man['protected_hashes'] if '/tasks/WP' in p])==45
own={k:OwnershipManifest.from_frontmatter(d) for k,d in fm.items()};deps={k:d.get('dependencies',[]) for k,d in fm.items()};v=validate_all(own,deps);g=validate_glob_matches(own,r,create_intent={k:d.get('create_intent',[]) for k,d in fm.items()});assert not v.errors and not g.errors
lanes=compute_lanes(deps,own,'wp51-parity-01M64CVY','feat/wp51-parity',bodies,mission_id='01M64CVYYRTDKBCYZ56H6XNTEQ').to_dict();old=json.load(open(r/m/'lanes.json'));mapping=lambda d:{w:l['lane_id'] for l in d['lanes'] for w in l['wp_ids']};before=mapping(old);after=mapping(lanes);assert len(old['lanes'])==21;assert all(after[w]==k for w,k in before.items());assert after['WP44']==after['WP46']=='lane-e';assert lanes['collapse_report']['independent_wps_collapsed']==0;assert len(lanes['lanes'])==21;assert fm['WP29']['dependencies'][-1]=='WP36';assert 'ordinary' in bodies['WP36'].lower()
seen=set();active=set()
def visit(k):
 assert k not in active,('cycle',k)
 if k in seen:return
 active.add(k)
 for parent in deps[k]:visit(parent)
 active.remove(k);seen.add(k)
for k in deps:visit(k)
# Full reviewed architecture/history copy equality; source review private PDF extracts excluded.
receipt=json.load(open(o/'promotion-plan.json'))
for row in receipt['files']:assert h(Path(row['source']))==row['sha256']==h(o/'promotion'/row['destination'])
assert receipt['byte_replacements']==[] and not receipt['semantic_changes'];prom=o/'promotion';adr=prom/'docs/decisions/closed-native-constructor.md';resolved=[]
for target in re.findall(r'\]\(([^)]+)\)',adr.read_text()):
 rel=(adr.parent/target).resolve().relative_to(prom.resolve());assert (prom/rel).exists() or (r/rel).exists();resolved.append(str(rel))
text=' '.join((o/man['proposed_WP46']['path']).read_text().split())
for phrase in ['all72','120WPU/01/raw0/raw0','NoLoadedOriginal','pre-print admitted e724/counter01','actual whole native byte','two fresh originals','exact finite total cap','actual independently approved C implementation','OriginalExport() ([]byte,error)','session1.lock','No private','independently authored','no original SET/PRS']:assert phrase.lower() in text.lower(),phrase
# Check both real lane DAG and a deliberately cyclic copy using the same detector.
def acyclic(graph):
 done=set();pending=set()
 def walk(k):
  if k in pending:raise ValueError('cycle')
  if k in done:return
  pending.add(k)
  for parent in graph[k]:walk(parent)
  pending.remove(k);done.add(k)
 for k in graph:walk(k)
lanegraph={l['lane_id']:l.get('depends_on_lanes',[]) for l in lanes['lanes']}
acyclic(lanegraph)
negative={k:list(v) for k,v in deps.items()};negative['WP25'].append('WP46')
try:acyclic(negative)
except ValueError:pass
else:raise AssertionError('negative cycle accepted')
assert len(man['protected_hashes'])==49
result={'kind':'pure installed ownership/glob/compute_lanes/DAG and local task/link/copy proof only; canonical validation NOT executed','baseline':man['primary_baseline'],'WP_count':46,'subtask_count':138,'lane_count':len(lanes['lanes']),'expected_lane_count':21,'actual_lane_prediction_matches':len(lanes['lanes'])==21,'protected45_live_old_prompts_spec_plan_both_charters_count':len(man['protected_hashes']),'old21_lane_IDs_exact':True,'new_mapping':{k:after[k] for k in ['WP44','WP45','WP46']},'WP46_depends_actual_approved_C44_not_architecture':True,'old_prompt_or_source_changes':False,'research_consumer_backedge':False,'ownership_errors':v.errors,'ownership_warnings':v.warnings,'glob_errors':g.errors,'glob_warnings':g.warnings,'glob_info':g.info,'collapse_report':lanes['collapse_report'],'DAG_acyclic':True,'lane_DAG_acyclic':True,'injected_dependency_cycle_refused':True,'promoted_exact_history_review_files':len(receipt['files']),'ADR_repo_relative_links':resolved,'current44_45_prompts_protected':True,'all14_C_classes_and_controls_required_before_implementation':True,'Save_history_amendment_protected':True,'canonical_topology_sha256':man['canonical_topology_sha256'],'canonical_finalization_or_lifecycle_run':False,'VM_attempts':0};(Path('/tmp/wordling-native-constructor-tasks-review')/'pure-validation.json').write_text(json.dumps(result,indent=2)+'\n');(Path('/tmp/wordling-native-constructor-tasks-review')/'lanes-preview.json').write_text(json.dumps(lanes,indent=2)+'\n');print('Pure proof:46WPs/138tasks/'+str(len(lanes['lanes']))+'actual installed lanes;45oldprompts+spec/plan/charters exact; old21laneIDs retained;46 lane-e; no independent collapse/errors; canonicalNOTexecuted')

# Exact append prefixes and no existing prompt edits; deliberate graph-fault controls.
for name in ['tasks.md','continuation.md']:
 base=r/m/name;proposed=o/m/name;assert proposed.read_bytes().startswith(base.read_bytes());assert h(base)==man['summary_append_base_hashes'][str(m/name)]
assert fm['WP46']['subtasks']==['T136','T137','T138']
assert h(r/m/'lanes.json')==man['canonical_topology_sha256']
assert h(o/man['proposed_WP46']['path'])==man['proposed_WP46']['sha256']
assert 'All14 actual C whole-native classes' in (o/man['proposed_WP46']['path']).read_text()
assert 'WP46' not in {d for w in deps if w!='WP46' for d in deps[w]}
