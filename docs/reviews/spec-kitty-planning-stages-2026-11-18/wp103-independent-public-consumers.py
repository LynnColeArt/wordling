"""Review-only public-consumer reproduction; isolated disposable Git repository."""
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import subprocess
import traceback
from specify_cli.lanes.compute import compute_lanes
from specify_cli.lanes.persistence import write_lanes_json
from specify_cli.ownership.models import OwnershipManifest, WorkProductKind
from specify_cli.context.resolver import resolve_context
from specify_cli.core.worktree_topology import materialize_worktree_topology
from specify_cli.workspace.context import clear_workspace_resolution_caches

results = []
with TemporaryDirectory(prefix='wp103-independent-consumers-', dir='/tmp') as directory:
    root = Path(directory)
    (root / '.kittify').mkdir()
    (root / '.kittify/config.yaml').write_text('project:\n  uuid: 12345678-1234-5678-1234-567812345678\n')
    mission = root / 'kitty-specs/stages'
    (mission / 'tasks').mkdir(parents=True)
    (root / 'src').mkdir()
    graph = {'WP01': [], 'WP02': ['WP01'], 'WP03': ['WP02']}
    owners = {}
    for wp, deps in graph.items():
        planning = wp != 'WP02'
        mode = WorkProductKind.PLANNING_ARTIFACT if planning else WorkProductKind.CODE_CHANGE
        owned = f'kitty-specs/stages/{wp}.md' if planning else f'src/{wp}.py'
        (root / owned).write_text('fixture\n')
        owners[wp] = OwnershipManifest(execution_mode=mode, owned_files=(owned,), authoritative_surface=owned)
        (mission / 'tasks' / f'{wp}-fixture.md').write_text(
            '---\n' + f'work_package_id: {wp}\ntitle: {wp}\nexecution_mode: {mode}\n'
            + 'dependencies: ' + json.dumps(deps) + '\n'
            + f'owned_files: [{owned}]\nauthoritative_surface: {owned}\n'
            + 'planning_base_branch: release/test\nmerge_target_branch: release/test\nsubtasks: []\nhistory: []\n---\n# Fixture\n'
        )
    (mission / 'meta.json').write_text(json.dumps({'mission_slug': 'stages', 'mission_id': '01AAAAAAAAAAAAAAAAAAAAAAAB', 'mission_type': 'software-dev', 'target_branch': 'release/test', 'planning_base_branch': 'release/test', 'merge_target_branch': 'release/test', 'topology': 'single_branch'}))
    manifest = compute_lanes(graph, owners, 'stages', 'release/test', mission_id='01AAAAAAAAAAAAAAAAAAAAAAAB')
    write_lanes_json(mission, manifest)
    for args in [('init', '-b', 'release/test'), ('config', 'user.email', 'review@example.test'), ('config', 'user.name', 'Independent reviewer'), ('add', '.'), ('commit', '-m', 'Disposable public-path fixture')]:
        subprocess.run(['git', *args], cwd=root, check=True, capture_output=True)
    for name, call in [('early_resolve_context', lambda: resolve_context('WP01', 'stages', 'codex', root)), ('late_resolve_context', lambda: resolve_context('WP03', 'stages', 'codex', root)), ('materialize_worktree_topology', lambda: materialize_worktree_topology(root, 'stages'))]:
        clear_workspace_resolution_caches()
        try:
            result = call()
            results.append({'name': name, 'result': 'PASS', 'authoritative_ref': getattr(result, 'authoritative_ref', None)})
        except Exception as error:
            results.append({'name': name, 'result': 'FAIL', 'type': type(error).__name__, 'error': str(error), 'traceback': traceback.format_exc()})
clear_workspace_resolution_caches()
print(json.dumps(results, indent=2))
Path('/tmp/wordling-mission1-closeout-20261118/wp103-independent-public-consumers.json').write_text(json.dumps(results, indent=2) + '\n')
