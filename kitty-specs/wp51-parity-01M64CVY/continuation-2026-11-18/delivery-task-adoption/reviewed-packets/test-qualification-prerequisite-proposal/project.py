"""Pure typed metadata/ownership/DAG/lane projection; no writers or operational imports."""
from pathlib import Path
import json,hashlib,re,subprocess,ast
from specify_cli.status.wp_metadata import read_authored_wp_frontmatter
from specify_cli.ownership.frontmatter_source import InMemoryFrontmatterSource,resolve_wp_manifests
from specify_cli.ownership.validation import validate_all,validate_glob_matches
from specify_cli.core.dependency_graph import detect_cycles,topological_sort,dependency_readiness_for_wp
from specify_cli.core.dependency_parser import parse_dependencies_from_tasks_md
from specify_cli.lanes.compute import compute_lanes,LaneDependencyCycleError
from specify_cli.cli.commands.agent.finalization_eligibility import project_finalization_eligibility
from specify_cli.status import Lane
from specify_cli.runtime.resolver import resolve_template
root=Path('/home/lynn/projects/wordling');m=root/'kitty-specs/wp51-parity-01M64CVY';out=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p):return dict(size=p.stat().st_size,sha256=sha(p))
front={};body={};canonical=sorted((m/'tasks').glob('WP*.md'))
for p in canonical:
 f,b=read_authored_wp_frontmatter(p);assert f.work_package_id not in front;front[f.work_package_id]=f;body[f.work_package_id]=b
assert len(front)==104 and 'WP105'in front and not {'WP103','WP106','WP107','WP108'}&set(front)
ids={s for f in front.values()for s in f.subtasks};assert not {'T350','T351','T352'}&ids
f108,b108=read_authored_wp_frontmatter(out/'tasks/WP108-current-test-runtime-qualification.md')
assert f108.subtasks==['T350','T351','T352'];assert f108.dependencies==['WP70','WP63','WP64','WP68','WP74']
original104=list(front['WP104'].dependencies);assert original104==['WP63','WP64','WP68','WP70','WP74']
f104=front['WP104'].builder().set(dependencies=[*original104,'WP108']).build()
future={**front,'WP108':f108,'WP104':f104};futurebody={**body,'WP108':b108}
meta=json.loads((m/'meta.json').read_text());status=json.loads((m/'status.json').read_text());assert status['work_packages']['WP104']['lane']=='in_progress'
before={str(p.relative_to(root)):pin(p) for p in canonical}
for p in (m/'tasks.md',m/'status.json',m/'status.events.jsonl',m/'lanes.json',m/'meta.json'):before[str(p.relative_to(root))]=pin(p)
# Pin against the specified immutable metadata baseline even if ROOT appends unrelated research.
for rel,want in before.items():
 raw=subprocess.check_output(['git','show','c0b249693b9f1dd50546ecbcf9f7ce661da043bc:'+rel],cwd=root)
 assert dict(size=len(raw),sha256=hashlib.sha256(raw).hexdigest())==want,('baseline-metadata-drift',rel)
summary={}
for label,fs,bs in [('canonical_before',front,body),('plus108_and_104_blocker',future,futurebody)]:
 graph={k:list(v.dependencies)for k,v in fs.items()};manifests=resolve_wp_manifests(InMemoryFrontmatterSource(fs))
 own=validate_all(manifests,graph);glob=validate_glob_matches(manifests,root,{k:list(f.create_intent)for k,f in fs.items()if f.create_intent})
 result=dict(wp_count=len(fs),wp_cycles=detect_cycles(graph),topological=topological_sort(graph),ownership_errors=own.errors,ownership_warnings=own.warnings,glob_errors=glob.errors,glob_warnings=glob.warnings,glob_info=glob.info)
 try:
  lanes=compute_lanes(dependency_graph=graph,ownership_manifests=manifests,mission_slug=m.name,target_branch=meta['target_branch'],wp_bodies=bs,mission_id=meta['mission_id']);result.update(lane_result='PASS',lane_count=len(lanes.lanes),manifest=lanes.to_dict())
 except LaneDependencyCycleError as e:result.update(lane_result='LANE_DEPENDENCY_CYCLE',cycle_path=list(e.cycle_path),cycle_lanes=[dict(lane_id=c.lane_id,wp_ids=list(c.wp_ids))for c in e.cycle_lanes])
 life={k:Lane(v['lane'])for k,v in status['work_packages'].items()};life['WP108']=Lane.PLANNED
 eligible=project_finalization_eligibility(fs,graph,life)
 result['finalization_eligibility']=dict(known=len(eligible.known_wp_ids),eligible=len(eligible.eligible_wp_ids),canceled=list(eligible.canceled_wp_ids),stale_canceled=[x.to_dict()for x in eligible.stale_dependencies])
 result['readiness']={k:dict(satisfied=(r:=dependency_readiness_for_wp(k,graph[k],life,provenance=status['work_packages'])).satisfied,unsatisfied=list(r.unsatisfied))for k in (('WP104','WP108')if'WP108'in fs else('WP104',))}
 summary[label]=result
index=(m/'tasks.md').read_text();old='**Dependencies**: WP63, WP64, WP68, WP70, WP74';assert index.count(old)==1
index=index.replace(old,old+', WP108',1).rstrip()+'\n\n'+(out/'tasks-append.md').read_text()
parsed=parse_dependencies_from_tasks_md(index)
before_parsed=parse_dependencies_from_tasks_md((m/'tasks.md').read_text())
for k in front:
 if k!='WP104':assert parsed.get(k)==before_parsed.get(k),('unrelated-index-drift',k)
for k in ('WP104','WP108','WP105','WP101','WP102'):assert parsed[k]==future[k].dependencies,(k,parsed.get(k),future[k].dependencies)
(out/'projected-tasks-index.md').write_text(index)
# Record approved target postimages independently of any unknown reference/candidate.
qual=root/'internal/document/evidence/reference_controller/tests/runtime_qualification.py'
tree=ast.parse(qual.read_text());constants={}
for node in tree.body:
 if isinstance(node,ast.Assign):
  for target in node.targets:
   if isinstance(target,ast.Name)and target.id in ('E_FILES','PROVIDERS'):constants[target.id]=ast.literal_eval(node.value)
prefix='internal/document/evidence/reference_controller/'
source_paths=[prefix+n for n in constants['E_FILES']]+[row[0]for row in constants['PROVIDERS'].values()]
assert len(source_paths)==20 and len(set(source_paths))==20
inputs={}
for rel in source_paths+[prefix+'pyproject.toml',prefix+'tests/harmless_fixture.c',prefix+'tests/controller_roster.json']:
 p=root/rel;raw=subprocess.check_output(['git','show','18af7190:'+rel],cwd=root);assert hashlib.sha256(raw).hexdigest()==sha(p),rel;inputs[rel]=dict(pin(p),target_git_commit='18af7190',blob=subprocess.check_output(['git','rev-parse','18af7190:'+rel],cwd=root,text=True).strip())
providers={}
for name,(rel,oldcommit)in constants['PROVIDERS'].items():
 commit='7869159b5d8e3ab1e26ec3e4dae2313264deb6f0'if name=='startup_family/lifetime.py'else oldcommit
 raw=subprocess.check_output(['git','show',commit+':'+rel],cwd=root);match=hashlib.sha256(raw).hexdigest()==sha(root/rel)
 providers[name]=dict(repository_path=rel,approved_commit=commit,approved_sha256=hashlib.sha256(raw).hexdigest(),current_matches=match)
 assert match,(name,commit)
for rel in ('internal/document/evidence/reference_controller/tests/runtime_qualification.py','internal/document/evidence/reference_controller/tests/controller_deployment.py','internal/document/evidence/reference_controller/tests/runtime_qualification_supervisor.py','.kittify/charter/charter.md','docs/compatibility.md','docs/roadmap.md'):inputs[rel]=pin(root/rel)
template=resolve_template('task-prompt-template.md',project_dir=root,mission='software-dev');(out/'resolved-task-template.md').write_bytes(template.path.read_bytes())
result=dict(disposition='SCRATCH_PURE_PROJECTION_NOT_FINALIZER_NOT_REGISTRATION',baseline_commit='c0b249693b9f1dd50546ecbcf9f7ce661da043bc',observed_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),tool_source='b45b48fd5e39c4e1a4b15af51f9569bcf6f5c2d3',profile='planner-priti',live_Op_opened=False,new_ids='WP108/T350–352 provisional; absent from canonical frontmatter/index/status; no reservation',before_hashes=before,inputs=inputs,provider_rows=providers,source_target_commit='18af7190',source_target_freeze='8e7cfff8e136a5e0ec260fb49c874c30eed76479',template=dict(path=str(template.path),tier=str(template.tier),sha256=sha(template.path)),states={k:status['work_packages'][k]['lane']for k in ('WP70','WP63','WP64','WP68','WP74','WP104','WP105','WP101','WP102')},proposed_dependencies={k:list(future[k].dependencies)for k in ('WP108','WP104','WP105','WP101','WP102')},projections=summary)
(out/'projection.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
for rel,want in before.items():assert pin(root/rel)==want,('live-metadata-mutated',rel)
for n,r in summary.items():print(n,{k:r[k]for k in('wp_count','lane_result','ownership_errors','glob_errors','readiness')},r.get('lane_count'))
print('All captured canonical104prompts/status/events/index/lanes/meta unchanged; approved8providerblobrows match actual target20source inputs.')
