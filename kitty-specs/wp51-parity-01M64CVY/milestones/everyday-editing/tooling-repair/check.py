import importlib,importlib.util,sys,json
from pathlib import Path
BASE=Path('/tmp/wordling-kitty-lane-repair/after')
def load(name,rel):
 if '--installed' in sys.argv:return importlib.import_module(name)
 spec=importlib.util.spec_from_file_location(name,BASE/rel)
 mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod
# Replace modules only within this isolated verification interpreter.
b=load('specify_cli.lanes.branch_naming','specify_cli/lanes/branch_naming.py')
c=load('specify_cli.lanes.compute','specify_cli/lanes/compute.py')
g=load('specify_cli.policy.commit_guard','specify_cli/policy/commit_guard.py')
r=load('specify_cli.merge.resolve','specify_cli/merge/resolve.py')
from specify_cli.ownership.models import OwnershipManifest,WorkProductKind
assert [c._lane_suffix(i) for i in (0,25,26,27,51,52,701,702)]==['a','z','aa','ab','az','ba','zz','aaa']
assert len({c._lane_suffix(i) for i in range(10000)})==10000
try:c._lane_suffix(-1)
except ValueError:pass
else:raise AssertionError('negative index accepted')
for slug,mid in [('083-example',None),('example-01M64CVY','01M64CVYYRTDKBCYZ56H6XNTEQ')]:
 for suffix in ['a','z','aa','ab','zz','aaa']:
  lane='lane-'+suffix
  branch=b.lane_branch_name(slug,lane,mission_id=mid)
  assert b.parse_lane_id_from_branch(branch)==lane,branch
  assert b.parse_mission_slug_from_branch(branch).lane_id==lane
  assert b.is_lane_branch(branch) and not b.is_mission_branch(branch)
  assert g.is_implementation_branch(branch)
  assert r._extract_mission_slug(branch)==('083-example' if mid is None else 'example')
for suffix in ['','{','|','}','a1','A','planning']:
 branch='kitty/mission-example-01M64CVY-lane-'+suffix
 assert b.parse_lane_id_from_branch(branch) is None
 assert not g.is_implementation_branch(branch)
for n in [1,26,27,29,52]:
 graph={f'WP{i:03}':[] for i in range(n)}
 owners={wp:OwnershipManifest(WorkProductKind.CODE_CHANGE,(f'component{i:03}/**',),f'component{i:03}') for i,wp in enumerate(graph)}
 lanes=c.compute_lanes(graph,owners,'example-01M64CVY',mission_id='01M64CVYYRTDKBCYZ56H6XNTEQ').lanes
 assert len(lanes)==n, (n, lanes)
 assert {x.wp_ids[0]:x.lane_id for x in lanes}=={f'WP{i:03}':'lane-'+c._lane_suffix(i) for i in range(n)}
 for lane in lanes:assert b.parse_lane_id_from_branch(b.lane_branch_name('example-01M64CVY',lane.lane_id,mission_id='01M64CVYYRTDKBCYZ56H6XNTEQ'))==lane.lane_id
print(json.dumps({'result':'PASS','unique_suffixes':10000,'allocation_sizes':[1,26,27,29,52],'roundtrip':'legacy and modern','guard':'multiletter guarded, malformed/reserved excluded','installed_modules':('--installed' in sys.argv)}))
