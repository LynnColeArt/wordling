"""Pure typed task projection. No finalizer, registry or live mutation."""
from pathlib import Path
import hashlib
import json
import subprocess
import tempfile
from specify_cli.status.wp_metadata import read_authored_wp_frontmatter
from specify_cli.ownership.frontmatter_source import InMemoryFrontmatterSource, resolve_wp_manifests
from specify_cli.ownership.validation import validate_all, validate_glob_matches
from specify_cli.core.dependency_graph import detect_cycles
from specify_cli.lanes.compute import compute_lanes

ROOT = Path('/home/lynn/projects/wordling')
OUT = Path(__file__).resolve().parent
BASE = 'a1b76dd130c8382a496248e0456862812826f019'
TOOL = 'b45b48fd5e39c4e1a4b15af51f9569bcf6f5c2d3'
TOOL_ROOT = Path('/tmp/wordling-spec-kitty-repair-20261118')
PREFIX = 'kitty-specs/wp51-parity-01M64CVY/'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=TOOL_ROOT).decode().strip() == TOOL
front, bodies, pins = {}, {}, {}
with tempfile.TemporaryDirectory(prefix='wordling-italics-projection-', dir='/tmp') as staging:
    stage = Path(staging)
    for rel in git('ls-tree', '-r', '--name-only', BASE, PREFIX+'tasks/').decode().splitlines():
        path = Path(rel)
        if path.parent.as_posix() != PREFIX.rstrip('/')+'/tasks' or path.suffix != '.md' or not path.name.startswith('WP'):
            continue
        data = git('show', BASE+':'+rel)
        temp = stage/path.name
        temp.write_bytes(data)
        fm, body = read_authored_wp_frontmatter(temp)
        assert fm.work_package_id not in front
        front[fm.work_package_id], bodies[fm.work_package_id] = fm, body
        pins[rel] = dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    assert 'WP105' in front and 'WP105' in front['WP101'].dependencies
    assert not {'WP106', 'WP107'} & set(front)
    existing_subtasks = {t for fm in front.values() for t in fm.subtasks}
    assert not set('T344 T345 T346 T347 T348 T349'.split()) & existing_subtasks
    core, core_body = read_authored_wp_frontmatter(OUT/'tasks/WP106-retrieve-balanced-italics-native.md')
    integration, integration_body = read_authored_wp_frontmatter(OUT/'tasks/WP107-retrieve-italics-public-integration.md')
    assert core.execution_mode == integration.execution_mode == 'code_change'

    def project(label, additions, new_bodies):
        fs = {**front, **additions}
        bs = {**bodies, **new_bodies}
        graph = {wp:list(f.dependencies) for wp,f in fs.items()}
        manifests = resolve_wp_manifests(InMemoryFrontmatterSource(fs))
        own = validate_all(manifests, graph)
        literal = validate_glob_matches(manifests, ROOT, {wp:list(f.create_intent) for wp,f in fs.items() if f.create_intent})
        record = dict(label=label, wp_count=len(fs), wp_cycles=detect_cycles(graph), ownership_errors=own.errors,
                      literal_errors=literal.errors, warnings=literal.warnings)
        try:
            lanes = compute_lanes(dependency_graph=graph, ownership_manifests=manifests,
                mission_slug='wp51-parity-01M64CVY', target_branch='feat/wp51-parity', wp_bodies=bs,
                mission_id='01M64CVYYRTDKBCYZ56H6XNTEQ')
            record.update(lane_result='PASS', manifest=lanes.to_dict())
        except Exception as exc:
            record.update(lane_result=type(exc).__name__, detail=str(exc))
        return record

    result = dict(schema='wordling.retrieve-italics-authoring-projection/v1',
        disposition='PROPOSAL_ONLY_NO_REGISTRATION_OR_LIVE_MUTATION', source=BASE, tool=TOOL,
        canonical_wp_count=len(front), current_proposed_ids_unreserved=True,
        actual_105_and_101_dependency_present=True, frozen_prompt_pins=pins,
        proposed_frontmatter={core.work_package_id:core.model_dump(mode='json'),integration.work_package_id:integration.model_dump(mode='json')},
        projections=[project('native_only', {'WP106':core}, {'WP106':core_body}),
                     project('native_then_public_integration', {'WP106':core,'WP107':integration}, {'WP106':core_body,'WP107':integration_body})])
    (OUT/'projection.json').write_text(json.dumps(result, indent=2)+'\n')
    for r in result['projections']:
        print({k:v for k,v in r.items() if k!='manifest'})
