"""Read-only canonical-input projection for reviewed delivery task adoption."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
from specify_cli.status.wp_metadata import read_authored_wp_frontmatter
from specify_cli.ownership.frontmatter_source import InMemoryFrontmatterSource, resolve_wp_manifests
from specify_cli.ownership.validation import validate_all, validate_glob_matches
from specify_cli.core.dependency_graph import detect_cycles
from specify_cli.core.dependency_parser import parse_dependencies_from_tasks_md
from specify_cli.lanes.compute import compute_lanes

root = Path('/home/lynn/projects/wordling')
mission = root / 'kitty-specs/wp51-parity-01M64CVY'
scratch = Path('/tmp/wordling-mission1-closeout-20261118')
out = scratch / 'joint-delivery-adoption'
out.mkdir(exist_ok=True)
front, bodies, before = {}, {}, {}
for path in sorted((mission / 'tasks').glob('WP*.md')):
    fm, body = read_authored_wp_frontmatter(path)
    front[fm.work_package_id], bodies[fm.work_package_id] = fm, body
    before[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
assert len(front) == 104 and all(w not in front for w in ('WP103', 'WP106', 'WP107', 'WP108'))
old104 = list(front['WP104'].dependencies)
assert old104 == ['WP63', 'WP64', 'WP68', 'WP70', 'WP74']
front['WP104'] = front['WP104'].builder().set(dependencies=old104 + ['WP108']).build()
sources = {
    'WP106': scratch / 'retrieve-italics-resliced-proposal/tasks/WP106-retrieve-balanced-italics-native.md',
    'WP107': scratch / 'retrieve-italics-resliced-proposal/tasks/WP107-retrieve-italics-public-integration.md',
    'WP108': scratch / 'test-qualification-prerequisite-proposal/tasks/WP108-current-test-runtime-qualification.md',
}
for wp, path in sources.items():
    fm, body = read_authored_wp_frontmatter(path)
    assert fm.work_package_id == wp
    front[wp], bodies[wp] = fm, body
graph = {wp: list(f.dependencies) for wp, f in front.items()}
assert detect_cycles(graph) is None
all_tasks = [t for f in front.values() for t in f.subtasks]
assert len(all_tasks) == len(set(all_tasks))
manifests = resolve_wp_manifests(InMemoryFrontmatterSource(front))
own = validate_all(manifests, graph)
literal = validate_glob_matches(manifests, root, {wp: list(f.create_intent) for wp, f in front.items() if f.create_intent})
assert not own.errors and not literal.errors, (own.errors, literal.errors)
lanes = compute_lanes(dependency_graph=graph, ownership_manifests=manifests,
    mission_slug=mission.name, target_branch='feat/wp51-parity', wp_bodies=bodies,
    mission_id='01M64CVYYRTDKBCYZ56H6XNTEQ')
index = (mission / 'tasks.md').read_text()
old_index_graph = parse_dependencies_from_tasks_md(index)
pattern = r'(?m)^\*\*Dependencies\*\*: WP63, WP64, WP68, WP70, WP74$'
assert len(re.findall(pattern, index)) == 1
index = re.sub(pattern, '**Dependencies**: WP63, WP64, WP68, WP70, WP74, WP108', index)
append = (scratch / 'retrieve-italics-resliced-proposal/tasks-append.md').read_text()
for wp in ('WP106', 'WP107'):
    append = append.replace(f'## Proposed {wp}:', f'## Work Package {wp}:')
    marker = re.search(rf'(?m)^## Work Package {wp}:.*$', append)
    assert marker
    fm = front[wp]
    section_end = append.find('\n## ', marker.end())
    section = append[marker.end():section_end if section_end >= 0 else len(append)]
    if '**Dependencies**:' not in section:
        canonical_declaration = '\n\n**Dependencies**: ' + ', '.join(fm.dependencies)
        canonical_declaration += '\n\n**Prompt**: `tasks/' + sources[wp].name + '`'
        append = append[:marker.end()] + canonical_declaration + append[marker.end():]
index = index.rstrip() + '\n\n' + append.rstrip() + '\n\n' + (scratch / 'test-qualification-prerequisite-proposal/tasks-append.md').read_text().rstrip() + '\n'
new_index_graph = parse_dependencies_from_tasks_md(index)
for wp, deps in old_index_graph.items():
    assert new_index_graph[wp] == (deps + ['WP108'] if wp == 'WP104' else deps), wp
for wp in ('WP106', 'WP107', 'WP108'):
    assert new_index_graph[wp] == front[wp].dependencies, (wp, new_index_graph[wp])
assert 'WP103' not in new_index_graph
(out / 'projected-tasks-index.md').write_text(index)
result = dict(disposition='PURE_PROJECTION_NOT_REGISTRATION',
    observed_head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
    tool_source='b45b48fd5e39c4e1a4b15af51f9569bcf6f5c2d3', wp_count=len(front),
    lane_count=len(lanes.lanes), ownership_errors=own.errors, literal_errors=literal.errors,
    warnings=literal.warnings, old_prompt_hashes=before,
    proposed_dependencies={wp: graph[wp] for wp in ('WP104', 'WP106', 'WP107', 'WP108')},
    proposal_hashes={wp: hashlib.sha256(p.read_bytes()).hexdigest() for wp, p in sources.items()},
    task_index_sha256=hashlib.sha256(index.encode()).hexdigest(), manifest=lanes.to_dict())
(out / 'projection.json').write_text(json.dumps(result, indent=2) + '\n')
for rel, expected in before.items():
    assert hashlib.sha256((root / rel).read_bytes()).hexdigest() == expected
print(json.dumps({k: result[k] for k in ('disposition', 'observed_head', 'wp_count', 'lane_count', 'ownership_errors', 'literal_errors', 'proposed_dependencies')}, indent=2))
