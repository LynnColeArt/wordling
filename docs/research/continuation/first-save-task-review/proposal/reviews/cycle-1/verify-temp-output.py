from pathlib import Path
import json,hashlib,yaml
from specify_cli.ownership.models import OwnershipManifest
from specify_cli.ownership.validation import validate_all,validate_glob_matches
from specify_cli.lanes.compute import compute_lanes
r=Path('/home/lynn/projects/wordling');o=Path('/tmp/wordling-first-save-tasks');m=Path('kitty-specs/wp51-parity-01M64CVY');h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();manifest=json.loads((o/'manifest.json').read_text());paths=list((r/m/'tasks').glob('WP*.md'))+list((o/m/'tasks').glob('WP*.md'));fm={};bodies={}
for p in paths:
 x=p.read_text().split('---',2);d=yaml.safe_load(x[1]);k=d['work_package_id'];assert k not in fm;fm[k]=d;bodies[k]=x[2]
assert len(fm)==48;alltasks=[t for d in fm.values()for t in d['subtasks']];assert len(alltasks)==len(set(alltasks))==144 and set(alltasks)=={f'T{i:03}'for i in range(1,145)}
assert len(manifest['protected_hashes'])==50 and all(h(r/n)==v for n,v in manifest['protected_hashes'].items());assert fm['WP47']['dependencies']==['WP36','WP41','WP43','WP46'];assert fm['WP48']['dependencies']==['WP37','WP41','WP43','WP46','WP47'];assert fm['WP47']['owned_files']==['internal/editor/**'];assert fm['WP48']['owned_files']==['internal/tui/**','cmd/wordling/*.go','docs/research/continuation/new-session/**']
own={w:OwnershipManifest.from_frontmatter(d)for w,d in fm.items()};deps={w:d.get('dependencies',[])for w,d in fm.items()};v=validate_all(own,deps);g=validate_glob_matches(own,r,create_intent={w:d.get('create_intent',[])for w,d in fm.items()});assert not v.errors and not g.errors
lanes=compute_lanes(deps,own,'wp51-parity-01M64CVY','feat/wp51-parity',bodies,mission_id='01M64CVYYRTDKBCYZ56H6XNTEQ').to_dict();old=json.loads((r/m/'lanes.json').read_text());mapping=lambda d:{w:l['lane_id']for l in d['lanes']for w in l['wp_ids']};before=mapping(old);after=mapping(lanes);assert all(after[w]==k for w,k in before.items());assert len(lanes['lanes'])==len(old['lanes'])==21;assert after['WP47']==after['WP36']=='lane-g';assert after['WP48']==after['WP37']=='lane-h';assert lanes['collapse_report']['independent_wps_collapsed']==0

def acyclic(graph):
 done=set();active=set()
 def visit(w):
  assert w not in active,('cycle',w)
  if w in done:return
  active.add(w)
  for d in graph[w]:visit(d)
  active.remove(w);done.add(w)
 for w in graph:visit(w)
acyclic(deps);acyclic({l['lane_id']:l.get('depends_on_lanes',[])for l in lanes['lanes']});negative={w:list(d)for w,d in deps.items()};negative['WP46'].append('WP48')
try:acyclic(negative)
except AssertionError:pass
else:raise AssertionError('cycle mutant accepted')
for name in ['tasks.md','continuation.md']:
 assert h(r/m/name)==manifest['summary_base_hashes'][str(m/name)]
 assert (o/m/name).read_bytes()==(r/m/name).read_bytes()+(o/(name.removesuffix('.md')+'.append.md')).read_bytes()
for row in manifest['architecture_promotion']:assert h(Path(row['source']))==row['sha256']==h(o/'promotion'/row['destination'])
assert 'PublishedUnbound' in bodies['WP47'] and 'PublicationUncertain' in bodies['WP47'];assert 'lifetimeNoLoadedOriginal' in bodies['WP47'];assert 'actual41 final Outcome.Identity' in bodies['WP47'];assert 'same-receipt Read-only retry' in bodies['WP47'];assert 'opaque request identity' in bodies['WP48']
result={'kind':'pure installed validation only; no canonical commands or lifecycle','WP_count':48,'subtask_count':144,'lane_count':len(lanes['lanes']),'all46_old_assignments_unchanged':True,'all50_protected_hashes_exact':True,'mapping':{w:after[w]for w in ['WP46','WP47','WP48']},'ownership_errors':v.errors,'ownership_warnings':v.warnings,'glob_errors':g.errors,'glob_warnings':g.warnings,'glob_info':g.info,'collapse_report':lanes['collapse_report'],'package_and_lane_DAGs_acyclic':True,'cycle_mutant_refused':True,'actual46_code_prerequisite_pending':True,'canonical_mutation':False,'source_changes':False,'VM_attempts':0}
(Path('/tmp/wordling-first-save-tasks-review')/'pure-validation.json').write_text(json.dumps(result,indent=2)+'\n');(Path('/tmp/wordling-first-save-tasks-review')/'lanes-preview.json').write_text(json.dumps(lanes,indent=2)+'\n');print('Pure proof48WPs/144tasks/21lanes; all46assignments/50protections exact; zeroerrors/independentcollapse, twoDAGs acyclic')
