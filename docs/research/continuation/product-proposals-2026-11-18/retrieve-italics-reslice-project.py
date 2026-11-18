"""Pure scheduling hypothesis against the frozen 8e7cfff8 source; no live writes."""
from pathlib import Path
import hashlib
import json
import subprocess
from specify_cli.status.wp_metadata import read_authored_wp_frontmatter
from specify_cli.ownership.frontmatter_source import InMemoryFrontmatterSource, resolve_wp_manifests
from specify_cli.ownership.validation import validate_all, validate_glob_matches
from specify_cli.core.dependency_graph import detect_cycles
from specify_cli.lanes.compute import compute_lanes

ROOT = Path('/home/lynn/projects/wordling')
OUT = Path('/tmp/wordling-mission1-closeout-20261118/retrieve-italics-reslice')
OUT.mkdir(exist_ok=True)
BASE = '8e7cfff8e136a5e0ec260fb49c874c30eed76479'
PREFIX = 'kitty-specs/wp51-parity-01M64CVY/'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

front, bodies, pins = {}, {}, {}
for rel in git('ls-tree', '-r', '--name-only', BASE, PREFIX + 'tasks/').decode().splitlines():
    p = Path(rel)
    if p.parent.as_posix() != PREFIX.rstrip('/') + '/tasks' or p.suffix != '.md' or not p.name.startswith('WP'):
        continue
    data = git('show', BASE + ':' + rel)
    tmp = OUT / p.name
    tmp.write_bytes(data)
    fm, body = read_authored_wp_frontmatter(tmp)
    front[fm.work_package_id], bodies[fm.work_package_id] = fm, body
    pins[rel] = hashlib.sha256(data).hexdigest()
assert len(front) == 103 and 'WP105' not in front and 'WP106' not in front and 'WP107' not in front

held = PREFIX + 'continuation-2026-11-18/tasks/WP105-original-readiness-stopped-export.md'
tmp105 = OUT / 'held105.md'
tmp105.write_bytes(git('show', BASE + ':' + held))
f105, b105 = read_authored_wp_frontmatter(tmp105)
front['WP101'] = front['WP101'].builder().set(dependencies=['WP38', 'WP63', 'WP64', 'WP70', 'WP105']).build()
front['WP105'], bodies['WP105'] = f105, b105
draft = Path('/tmp/wordling-mission1-closeout-20261118/retrieve-italics-proposal/tasks/WP106-retrieve-balanced-italics.md')
f106, b106 = read_authored_wp_frontmatter(draft)

# Scheduling only: IDs are hypothetical, unreserved, and task bodies are not
# claimed to be authored executable packages. All original obligations remain.
core = f106.builder().set(
    dependencies=['WP99'],
    owned_files=['internal/document/everyday.go', 'internal/document/retrieve_italics_test.go', 'internal/document/evidence/retrieve-italics/**'],
    create_intent=['internal/document/retrieve_italics_test.go', 'internal/document/evidence/retrieve-italics/'],
).build()
integration = f106.builder().set(
    work_package_id='WP107',
    subtasks=['T347', 'T348', 'T349'],
    dependencies=['WP106', 'WP94', 'WP84', 'WP85'],
    owned_files=['internal/editor/retrieve_italics_test.go', 'internal/tui/retrieve_italics_test.go', 'internal/editor/evidence/retrieve-italics/**'],
    create_intent=['internal/editor/retrieve_italics_test.go', 'internal/tui/retrieve_italics_test.go', 'internal/editor/evidence/retrieve-italics/'],
    authoritative_surface='internal/editor/retrieve_italics_test.go',
).build()

def project(label, additions):
    fs = {**front, **additions}
    bs = {**bodies, **{wp: b106 for wp in additions}}
    graph = {wp: list(f.dependencies) for wp, f in fs.items()}
    manifests = resolve_wp_manifests(InMemoryFrontmatterSource(fs))
    own = validate_all(manifests, graph)
    literal = validate_glob_matches(manifests, ROOT, {wp: list(f.create_intent) for wp, f in fs.items() if f.create_intent})
    record = {'label': label, 'wp_count': len(fs), 'wp_cycles': detect_cycles(graph), 'ownership_errors': own.errors, 'literal_errors': literal.errors, 'warnings': literal.warnings}
    try:
        lanes = compute_lanes(dependency_graph=graph, ownership_manifests=manifests, mission_slug='wp51-parity-01M64CVY', target_branch='feat/wp51-parity', wp_bodies=bs, mission_id='01M64CVYYRTDKBCYZ56H6XNTEQ')
        record.update(lane_result='PASS', manifest=lanes.to_dict())
    except Exception as exc:
        record.update(lane_result=type(exc).__name__, detail=str(exc))
    return record

result = {'disposition': 'PURE_UNRESERVED_HYPOTHESIS_NOT_REVIEWED_PACKAGES_OR_REGISTRATION', 'wordling_source': BASE, 'tool_source': 'b45b48fd5e39c4e1a4b15af51f9569bcf6f5c2d3', 'frozen_prompt_pins': pins,
          'projections': [project('core_only', {'WP106': core}), project('core_then_public_integration', {'WP106': core, 'WP107': integration})]}
(OUT / 'projection.json').write_text(json.dumps(result, indent=2) + '\n')
for r in result['projections']:
    print({k: v for k, v in r.items() if k != 'manifest'})
