"""Read-only immutable Wordling metadata projection; no finalizer or runtime action."""
from pathlib import Path
import collections
import hashlib
import json
import subprocess
from specify_cli.status.wp_metadata import read_authored_wp_frontmatter
from specify_cli.ownership.frontmatter_source import InMemoryFrontmatterSource, resolve_wp_manifests
from specify_cli.ownership.validation import validate_all
from specify_cli.core.dependency_graph import detect_cycles, topological_sort
from specify_cli.lanes.compute import compute_lanes, is_planning_lane
from specify_cli.lanes.models import LanesManifest
from specify_cli.lanes.branch_naming import lane_branch_name
from specify_cli.ownership.workspace_strategy import create_planning_workspace

ROOT = Path('/home/lynn/projects/wordling')
BASE = '9f255248b91f0a695d2affd214f37f50d661a03a'
TOOL = 'ec868755fa640238b4bdb98f957e948f28abdc0e'
PREFIX = 'kitty-specs/wp51-parity-01M64CVY/'
CONT = PREFIX + 'continuation-2026-11-18/'
OUT = Path('/tmp/wordling-mission1-closeout-20261118/wp103-current-task-projection')
OUT.mkdir(exist_ok=True)
PINS = {}

def blob(path):
    data = subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=ROOT)
    PINS[path] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    return data

def obj(path):
    return json.loads(blob(path))

paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE], cwd=ROOT, text=True).splitlines()
front, bodies = {}, {}
for rel in paths:
    path = Path(rel)
    if path.parent.as_posix() != PREFIX.rstrip('/') + '/tasks' or not path.name.startswith('WP') or path.suffix != '.md':
        continue
    exported = OUT / path.name
    exported.write_bytes(blob(rel))
    fm, body = read_authored_wp_frontmatter(exported)
    assert fm.work_package_id not in front
    front[fm.work_package_id], bodies[fm.work_package_id] = fm, body
assert len(front) == 107 and 'WP103' not in front
held = OUT / 'held-WP103-full-mission-coverage-index.md'
held.write_bytes(blob(CONT + 'tasks/WP103-full-mission-coverage-index.md'))
f103, b103 = read_authored_wp_frontmatter(held)
assert f103.work_package_id == 'WP103' and f103.dependencies == ['WP05', 'WP21', 'WP86']
assert f103.execution_mode == 'planning_artifact' and f103.subtasks == ['T335', 'T336', 'T337']
assert not ({*f103.subtasks} & {s for f in front.values() for s in f.subtasks})
assert set(f103.create_intent) == set(f103.owned_files) and len(f103.owned_files) == 2
assert not (set(f103.owned_files) & set(paths))
meta = obj(PREFIX + 'meta.json')
status = obj(PREFIX + 'status.json')
blob(PREFIX + 'status.events.jsonl')
blob(PREFIX + 'tasks.md')
blob(PREFIX + 'lanes.json')
assert len(status['work_packages']) == 107 and 'WP103' not in status['work_packages']

def project(fs, bs):
    graph = {wp: list(f.dependencies) for wp, f in fs.items()}
    ownership = resolve_wp_manifests(InMemoryFrontmatterSource(fs))
    checks = validate_all(ownership, graph)
    assert not checks.errors
    assert not detect_cycles(graph)
    order = topological_sort(graph)
    result = compute_lanes(graph, ownership, 'wp51-parity-01M64CVY', meta['target_branch'], wp_bodies=bs, mission_id=meta['mission_id'])
    encoded = result.to_dict()
    assert LanesManifest.from_dict(encoded).to_dict() == encoded
    assert sorted(wp for lane in result.lanes for wp in lane.wp_ids) == sorted(fs)
    for lane in result.lanes:
        for wp in lane.wp_ids:
            assert lane.execution_mode == ownership[wp].execution_mode
            for dep in graph[wp]:
                other = result.lane_for_wp(dep)
                assert other is not None
                if lane.lane_id != other.lane_id:
                    assert other.lane_id in lane.depends_on_lanes
    return result, {'wp_count': len(fs), 'authored_edge_count': sum(map(len, graph.values())), 'wp_cycles': [], 'topological_order': order, 'ownership_errors': checks.errors, 'ownership_warnings': checks.warnings, 'lane_count': len(result.lanes), 'codec_round_trip': True, 'all_wp_memberships_and_kinds_and_edges_preserved': True, 'manifest': encoded}

before, rb = project(front, bodies)
after, ra = project({**front, 'WP103': f103}, {**bodies, 'WP103': b103})
code_before = {lane.lane_id: list(lane.wp_ids) for lane in before.lanes if not is_planning_lane(lane)}
code_after = {lane.lane_id: list(lane.wp_ids) for lane in after.lanes if not is_planning_lane(lane)}
assert code_before == code_after
assert ra['manifest']['version'] == 2 and 'lanes' not in ra['manifest']
(OUT / 'lanes.json').write_text(json.dumps(ra['manifest'], indent=2) + '\n')

scenarios = obj('docs/research/command-scenarios.json')
parents = obj('docs/research/feature-inventory.json')
mapping = obj(CONT + 'all-parents-and-lessons.json')
families = obj(CONT + 'full-family-backlog.json')['families']
closure = obj(CONT + 'acceptance-closure-contract.json')
gaps = obj(CONT + 'all-58-open-scenarios.json')
for values, expected in [(scenarios, 244), (parents, 91), (families, 49), (closure['criteria'], 38), (closure['success_criteria'], 5)]:
    assert len(values) == expected
    assert len({v if isinstance(v, str) else v['id'] for v in values}) == expected
assert len(mapping['parents']) == 91 and len(mapping['workbook_lessons']) == 36 and len(gaps) == 58
assert all(c['status'] == 'pending' for c in closure['criteria'])
scenario_ids = {v['id'] for v in scenarios}
parent_ids = {v['id'] for v in parents}
family_ids = {v['id'] for v in families}
shared_prerequisites = {'coverage-index', 'reference-route', 'resource-census', 'native-relationships', 'layout-profile', 'graphics-font-profile', 'language-profile', 'backup-contract', 'ALL_DELIVERY_AND_LEAF_CLOSURE'}
assert {v['id'] for v in mapping['parents']} == parent_ids
assert {v['id'] for v in mapping['workbook_lessons']} == {f'WB{i:02d}' for i in range(1, 37)}
assert all(set(v['feature_ids']) <= parent_ids for v in scenarios)
assert all(set(v['family_dependencies']) <= family_ids | shared_prerequisites for v in mapping['parents'] + mapping['workbook_lessons'])
assert all(set(v['feature_ids']) <= parent_ids for v in mapping['workbook_lessons'])
assert all(v['scenario'] in scenario_ids and set(v['family_dependencies']) <= family_ids for v in gaps)
assert all(set(v['feature_groups']) <= parent_ids for v in families)
assert all(set(v['depends_on']) <= family_ids | shared_prerequisites for v in families)
for v in families:
    assert all(s in scenario_ids or s == 'full-source/integration obligation beyond the58 rows' for s in v['scenarios'])
workbook_counts = []
for i in range(1, 8):
    census = obj(f'docs/research/continuation/workbook-source-census-2026-11-18/workbook-b{i:02d}-source-census.json')
    workbook_counts.append(census['core_baseline_preserved']['numbered_steps'] if i == 1 else len(census['numbered_steps']))
assert sum(workbook_counts) == 1074
counts = {'scenarios': 244, 'parents': 91, 'workbook_lessons': 36, 'families': 49, 'obligations': 38, 'success_criteria': 5, 'open_gap_floor': 58, 'negative_invariants': len(closure['negative_invariants'])}
planning = [{'lane_id': lane.lane_id, 'wp_ids': list(lane.wp_ids), 'depends_on_lanes': list(lane.depends_on_lanes), 'parallel_group': lane.parallel_group, 'planning_stage': lane.planning_stage} for lane in after.lanes if is_planning_lane(lane)]
for stage in planning:
    lane = next(l for l in after.lanes if l.lane_id == stage['lane_id'])
    stage['target_branch'] = lane_branch_name('wp51-parity-01M64CVY', lane.lane_id, planning_base_branch=meta['target_branch'], lane=lane)
    stage['canonical_root'] = str(create_planning_workspace(mission_slug='wp51-parity-01M64CVY', wp_code=lane.wp_ids[0], owned_files=list(lane.write_scope), repo_root=ROOT))
    assert stage['target_branch'] == 'feat/wp51-parity' and stage['canonical_root'] == str(ROOT)
result = {'disposition': 'PURE_FROZEN_METADATA_PROJECTION_NOT_FINALIZER_OR_REGISTRATION', 'wordling_source': BASE, 'tool_source': TOOL, 'input_pins': PINS, 'current_status_summary': status['summary'], 'held103_has_no_registry_record': True, 'held103_has_no_existing_subtask_collision': True, 'held103_two_outputs_are_new_and_exact_create_intents': True, 'current': rb, 'plus103': ra, 'unchanged_code_groups': code_before, 'code_groups_preserved': True, 'planning_stages': planning, 'counts': counts, 'all_canonical_prior_records_untouched': True}
result['existing_concrete_mapping_ids_have_no_dangling_ids'] = True
result['shared_prerequisite_symbols'] = sorted(shared_prerequisites)
result['shared_symbols_needing_explicit_pending_nodes_in_new_index'] = ['backup-contract', 'ALL_DELIVERY_AND_LEAF_CLOSURE']
result['workbook_documentary_steps_first21'] = {'counts_by_batch': workbook_counts, 'total': sum(workbook_counts), 'execution_claim': False}
(OUT / 'projection.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'current_wps': rb['wp_count'], 'projected_wps': ra['wp_count'], 'current_lanes': rb['lane_count'], 'projected_lanes': ra['lane_count'], 'planning_stages': planning, 'counts': counts, 'code_groups_preserved': True}, indent=2))
