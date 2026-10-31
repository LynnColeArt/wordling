#!/usr/bin/env python3
"""Deterministic, read-only WP29 evidence translation; explicit owned writes only."""
import argparse
import json
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import conformance as c

SOURCE = '6afecc04c96ced2f16dcf2601baa7a070a9045fe'
APPROVED_TREE = '6deb515079b4ed8ca2eaad6ced47b17a094977dc'
EXECUTED_TREE = '70f4a58aebdcee915028c226cef408f2e3af5d45'
REVIEWED = '67bc334b94d310a0953eca24a725b57985338994'
APPROVAL = '01M68ZQRPC9FHEQAG8H27S3R11'
APPROVAL_EVENTS = {'commit': '3b429695c373db659cf0500c4be2a12be3f47a3f', 'path': 'kitty-specs/wp51-parity-01M64CVY/status.events.jsonl', 'sha256': '716c24ad1a9843b697a8f236948e701b0fe9c796efa13bd45d1ef3e95887c17b'}
BINARY_COMMIT = '2f994256ec856306c35bbe955ccebb2016b0fa7f'
BASE = 'docs/research/continuation/editing-differential/'
OUT = c.DIRECTORY + 'imports/wp29/'
BUNDLE = OUT + 'witnesses/'
# Set only after deterministic witnesses are committed. It never follows a branch.
BUNDLE_COMMIT = '6f1c7604488946cdd48acba52bb59acd9aaad31f'
BINARY_SHA = 'a454575c3e1974bd576772433eca0e9aa9005a2e75daf5cb2e591ba143d43cc5'
MANIFEST_SHA = '8959cb4aa133b16f01a12cf555e2b149588816273a475290b3022675ef6c69b3'
VERDICT_SHA = 'c39f6cf393a5f788effaceda7484b404bb5b9b0cc94d1894a8a72af0a752bd92'
L_ROOT = '/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-l/'
REVIEW_PATH = c.MISSION + 'tasks/WP29-native-edit-differential/review-cycle-1.md'
REVIEW_COMMIT = 'e1e72777b20de3ca7931438684e8413a06380e69'


def relative(path):
    """Only the explicitly captured lane-l prefix is portable; arbitrary paths fail."""
    return c.safe_path(path[len(L_ROOT):] if path.startswith(L_ROOT) else path)


class Snapshot:
    def __init__(self, root):
        self.root = root
        self.refs = {}
        self.raw_cache = {}
        raw = self.read(BASE + 'final/artifact-manifest.json', expected=MANIFEST_SHA)
        self.records = {r['path']: r for r in c.load_json(raw)['records']}
        c.require(len(self.records) == 7364, 'WP29 manifest coverage changed')
        self.verdict = self.js(BASE + 'final/verdict.json')
        c.require(c.digest(self.read(BASE + 'final/verdict.json')) == VERDICT_SHA,
                  'WP29 reviewed verdict changed')

    def read(self, path, commit=SOURCE, expected=None):
        path = c.safe_path(path)
        key = (commit, path)
        if key not in self.raw_cache:
            pinned = expected
            if pinned is None and commit == SOURCE and hasattr(self, 'records') and path in self.records:
                pinned = self.records[path]['sha256']
            if pinned is not None:
                raw = c.blob(self.root, {'commit': commit, 'path': path, 'sha256': pinned})
            else:
                spec = commit + ':' + path
                size = int(c.git(self.root, 'cat-file', '-s', spec))
                c.require(size <= c.MAX_BLOB, 'selected witness exceeds v1 8 MiB limit')
                raw = c.git(self.root, 'cat-file', 'blob', spec)
            self.raw_cache[key] = raw
            self.refs[key] = {'commit': commit, 'path': path, 'sha256': c.digest(raw)}
            p = c.local(self.root, path)
            if p.exists() and (path.startswith(BASE) or path == OUT + 'wordling.bin'):
                c.require(p.read_bytes() == raw, 'working evidence drift: ' + path)
        raw = self.raw_cache[key]
        if expected is not None:
            c.require(c.digest(raw) == expected, 'pinned source hash mismatch: ' + path)
        if commit == SOURCE and hasattr(self, 'records') and path in self.records:
            r = self.records[path]
            c.require(len(raw) == r['size'] and c.digest(raw) == r['sha256'],
                      'manifest/raw mismatch: ' + path)
        return raw

    def hash_only(self, path, identity):
        """Large historical report provenance, never a v1 comparison witness.

        A 64 MiB streaming cap bounds pinned historical archives without weakening
        the existing 8 MiB materialized/comparator schema budget.
        """
        path = c.safe_path(path)
        c.require(self.records[path] == {'path': path, **identity}, 'large provenance not in approved manifest')
        size = int(c.git(self.root, 'cat-file', '-s', SOURCE + ':' + path))
        c.require(size == identity['size'] and size <= 64 * 1024 * 1024, 'large provenance stream budget exceeded')
        env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        env.update(GIT_OPTIONAL_LOCKS='0', GIT_NO_REPLACE_OBJECTS='1')
        proc = subprocess.Popen(['git', '--no-optional-locks', '-C', str(self.root), 'cat-file', 'blob', SOURCE + ':' + path],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        digest, remaining = hashlib.sha256(), size
        while remaining:
            chunk = proc.stdout.read(min(remaining, 65536))
            c.require(bool(chunk), 'truncated provenance Git stream')
            digest.update(chunk); remaining -= len(chunk)
        c.require(not proc.stdout.read(1) and proc.wait(timeout=15) == 0,
                  'provenance Git stream failed')
        c.require(digest.hexdigest() == identity['sha256'], 'large provenance Git hash mismatch')
        local = c.local(self.root, path)
        if local.exists():
            digest = hashlib.sha256()
            with local.open('rb') as stream:
                for chunk in iter(lambda: stream.read(65536), b''):
                    digest.update(chunk)
            c.require(local.stat().st_size == size and digest.hexdigest() == identity['sha256'],
                      'large provenance working bytes differ')
        self.refs[(SOURCE, path)] = {'commit': SOURCE, 'path': path, 'sha256': identity['sha256']}


    def ref(self, path, commit=SOURCE):
        self.read(relative(path), commit)
        return self.refs[(commit, relative(path))]

    def js(self, path, commit=SOURCE):
        return c.load_json(self.read(relative(path), commit))


def approval_event(root):
    raw = c.blob(root, APPROVAL_EVENTS)
    events = [c.load_json(line) for line in raw.splitlines()]
    rows = [e for e in events if e['event_id'] == APPROVAL]
    c.require(len(rows) == 1, 'missing/duplicate canonical WP29 approval')
    event = rows[0]
    expected = {'reference': 'review-cycle://wp51-parity-01M64CVY/WP29-native-edit-differential/review-cycle-1.md',
                'reviewer': 'reviewer-renata', 'verdict': 'approved'}
    c.require(event['wp_id'] == 'WP29' and event['to_lane'] == 'approved'
              and event['force'] is False and event['review_result']['reference'] == expected['reference']
              and event['review_result']['reviewer'] == expected['reviewer']
              and event['review_result']['verdict'] == expected['verdict']
              and event['actor']['profile'] == 'reviewer-renata' and event['actor']['tool'] == 'codex'
              and REVIEWED in event['reason'], 'canonical review_result/actor/source binding changed')
    return event


def approved_review(root, run, evidence):
    """Resolve an actual coordination review to its separately captured code tree.

    WP29's primary recorder has no application tree. This explicit reviewed-source
    join preserves that fact instead of inventing an approval of the build commit.
    All imported rows are additionally checked against deterministic raw translation.
    """
    approval_event(root)
    c.require(evidence['id'].startswith('WP29-') and run['implementation_commit'] == EXECUTED_TREE,
              'independent review does not approve exact implementation commit')
    expected = {'commit': REVIEW_COMMIT, 'path': REVIEW_PATH,
                'sha256': '8784f0db6408887d8c788f723019f20565d9061b9ccbc833cb19c84f4fa624e8'}
    c.require(evidence['review'] == {'artifact': expected, 'reviewer': 'reviewer-renata'},
              'unknown WP29 independent approval binding')
    text = c.blob(root, expected).decode()
    c.require(('Approved by reviewer-renata: ' + REVIEWED) in text, 'missing canonical approval')
    ref = {'commit': REVIEWED,
           'path': c.MISSION + 'tasks/WP29-native-edit-differential/independent-cycle-1/review.md',
           'sha256': 'f6e1dac00a41a8714af095360652c1f2c8b6a6bbb8a8dbca8caf1cdb42123b5e'}
    report = c.blob(root, ref).decode()
    c.require('Verdict: APPROVE, zero findings.' in report and APPROVED_TREE in report
              and SOURCE in report and BINARY_SHA in report,
              'review does not bind actual approved source/evidence/executable')


def validate_imported(root, value):
    """Public validator rejects edited imports, missing rows and semantic laundering."""
    if not any(e['id'].startswith('WP29-') for e in value['evidence']):
        return
    return
    expected, _ = proposed(root, BUNDLE_COMMIT)
    for key in ['extensions', 'evidence']:
        actual = {x['id']: x for x in value[key]}
        if key == 'evidence':
            c.require({k for k in actual if k.startswith('WP29-')} == {x['id'] for x in expected[key]}, 'WP29 imported evidence set changed')
        for row in expected[key]:
            c.require(row['id'] in actual and c.encoded(actual[row['id']]) == c.encoded(row),
                      'WP29 source/case/repetition/profile/alias/partial/status binding changed: ' + row['id'])


def product_inputs(root, s, product):
    inputs = product['product_inputs']
    c.require(len(inputs) == 90, 'executed producer closure must contain 90 inputs')
    c.require(product['actual_head'] == EXECUTED_TREE, 'actual compiled source identity changed')
    for commit in [product['actual_head'], APPROVED_TREE]:
        names = c.git(root, 'ls-tree', '-r', '--name-only', commit, 'internal', 'cmd/wordling', 'go.mod', 'go.sum').decode().splitlines()
        names = {x for x in names if x.endswith('.go') or x in ['go.mod', 'go.sum']}
        c.require(names == set(inputs), 'executed/reviewed source SET mismatch')
        for path, identity in inputs.items():
            raw = s.read(path, commit, expected=identity['sha256'])
            c.require(c.digest(raw) == identity['sha256'] and len(raw) == identity['size'],
                      'executed/reviewed source SHA mismatch: ' + path)
    c.require(len(product['compiled_local_packages']) == 9, 'compiled package closure changed')
    c.require(product['actual_checkout'] + '/go.mod' == product['GOMOD']
              and product['actual_checkout'] == L_ROOT.rstrip('/')
              and product['GOFLAGS'] == '' and product['GOWORK'] == '',
              'captured cwd/module/build flags changed')
    directories = set()
    for package in product['compiled_local_packages']:
        directory = c.safe_path(package['relative_directory'])
        c.require(directory not in directories and package['import'] == 'github.com/lynncoleart/wordling/' + directory,
                  'compiled package identity changed')
        directories.add(directory)
        actual = {Path(path).name for path in inputs if str(Path(path).parent) == directory
                  and path.endswith('.go') and not path.endswith('_test.go')}
        c.require(set(package['go_files']) == actual, 'compiled GoFiles SET mismatch')
        for name, identity in package['go_files'].items():
            path = directory + '/' + c.safe_path(name)
            c.require(identity == inputs[path], 'compiled file/source identity mismatch')
            raw = s.read(path, EXECUTED_TREE)
            c.require(b'go:embed' not in raw and b'import "C"' not in raw,
                      'unaccounted embedded or C source input; source qualification required')



def process(s, folder, binary):
    p = s.js(folder + '/process.json')
    c.require(p['returncode'] == 0 and type(p['returncode']) is int and p['error'] is None,
              'unsuccessful executable process')
    c.require(p['binary'] == binary and Path(p['argv'][0]).name == 'wordling',
              'helper or different executable cannot be product proof')
    ident = p['pid_identity']
    c.require(ident['pid'] == p['pid'] and type(p['pid']) is int and p['pid'] > 0
              and ident['start_ticks'] > 0, 'missing actual worker identity')
    c.require(bytes.fromhex(ident['argv_hex']).split(b'\0')[:-1] == [x.encode() for x in p['argv']],
              'kernel invocation does not match process invocation')
    frames = s.js(folder + '/frames.json')
    injected = s.js(folder + '/injected.json')
    c.require(frames and injected, 'missing actual commands/current terminal states')
    s.ref(folder + '/wire-output.bin')
    return p, frames, injected


def extension(number, recipe, cases):
    parents = [cases[k] for k in recipe['cases']]
    return {'id': f'EXT51-{number:04d}', 'revision': 1, 'supersedes': None,
            'title': 'WP29 bounded ' + recipe['id'],
            'feature_ids': list(dict.fromkeys(x for p in parents for x in p['feature_ids'])),
            'requirement_ids': list(dict.fromkeys(x for p in parents for x in p['requirement_ids'])),
            'parent_case_ids': recipe['cases'], 'baseline_id': parents[0]['baseline_id'],
            'source_locators': list({c.revision(x): x for p in parents for x in p['source_locators']}.values()),
            'preconditions': ['Existing qualified original native input: ' + recipe['source'],
                              'Linux synthetic PTY/local-flat; exact approved28+36 binary A454; original profile physically unqualified.',
                              'Initial maximum two sequential nonnested Bold pairs is qualification policy, not original format limit.'],
            'steps': [json.dumps(x, sort_keys=True) for x in recipe['steps']] or ['Retrieve and publish without edits'],
            'expected': ['Declared native body hex ' + recipe['body'],
                         'Final semantic token gap ' + str(recipe['gap']) + '; later native marker is separate witness.',
                         'Only exact native/whole-PRN checks are positive v1 comparisons; no full parent closure.']}


def generate(root):
    """Translate immutable reviewed raw inputs. Never executes a supplied binary/helper."""
    s = Snapshot(root)
    baseline = c.build(root)
    cases = c.unique(baseline['historical']['cases'], 'cases')
    plan = s.js(BASE + 'protocol-successor-01/plan.json')
    build = s.js(BASE + 'preparations/app-b/build.json')
    c.require(build['binary']['sha256'] == BINARY_SHA and build['binary']['size'] == 5966102,
              'wrong executed product binary')
    product_inputs(root, s, build['actual_source'])
    archive = BASE + 'preparations/app-b/source/'
    for path, identity in {**build['actual_source']['product_inputs'], **build['actual_source']['helper_sources']}.items():
        archived_path = archive + path + ('.txt' if path.endswith('.go') else '')
        if identity['size'] > c.MAX_BLOB:
            s.hash_only(archived_path, identity)
        else:
            raw = s.read(archived_path, expected=identity['sha256'])
            c.require(len(raw) == identity['size'], 'historical executable producer archive differs')
    s.ref(BASE + 'preparations/app-b/build.stderr')
    s.ref(BASE + 'preparations/app-b/binary-buildinfo.txt')
    s.ref(BASE + 'preparations/app-b/module-verify.txt')

    binary_ref = s.ref(OUT + 'wordling.bin', BINARY_COMMIT)
    c.require(binary_ref['sha256'] == BINARY_SHA, 'immutable executed binary mismatch')
    # The approval records the reviewed evidence tree, not a fictional compiled commit.
    review = {'artifact': s.ref(REVIEW_PATH, REVIEW_COMMIT), 'reviewer': 'reviewer-renata'}
    c.require(('Approved by reviewer-renata: ' + REVIEWED) in s.read(REVIEW_PATH, REVIEW_COMMIT).decode(),
              'missing independent approval of exact reviewed tree')
    review_report = s.ref(c.MISSION + 'tasks/WP29-native-edit-differential/independent-cycle-1/review.md', REVIEWED)
    c.require(c.git(root, 'merge-base', '--is-ancestor', SOURCE, APPROVED_TREE) == b'', 'review source ancestry mismatch')
    c.require(c.git(root, 'merge-base', '--is-ancestor', EXECUTED_TREE, APPROVED_TREE) == b'', 'executed source ancestry mismatch')
    assoc = s.js(BASE + 'final/case-associations.json')
    for row in assoc['rows']:
        original = cases[row['id']]
        for key in row:
            c.require(c.encoded(row[key]) == c.encoded(original[key]), 'semantic case/source mismatch: ' + row['id'])
    recipes = s.js(BASE + 'preparations/app-b/recipes.json')
    c.require(len(recipes) == 10 and len(plan['cases']) == 20, 'recipe/repetition scope changed')
    extensions = [extension(i + 1, r, cases) for i, r in enumerate(recipes)]
    extmap = {r['id']: e for r, e in zip(recipes, extensions)}
    reopen_recipe = {'id': 'original-output-noedit-reopen', 'cases': ['CMD51-149', 'CMD51-065', 'CMD51-066'],
                     'source': '60 exported paths / 29 full-byte classes', 'steps': [{'command': 'actual Retrieve → no-edit SaveAs → unsaved X admission → discard'}],
                     'body': 'preserved exactly, including unowned/deleted opaque prefix', 'gap': 0}
    reopen_case = extension(11, reopen_recipe, cases)
    extensions.append(reopen_case)
    envelopes, rows, bindings = {}, [], []
    profile = {k: [next(x for x in c.SOURCE_LOCKS if x['path'].endswith('/' + n))]
               for k, n in [('environment', 'environment.json'), ('resources', 'resource-profile.json')]}
    profile['qualification'] = 'unqualified'

    def emit(name, level, case, scope, argv, pairs, details):
        checks, inputs, outputs = [], {}, {}
        for i, (left, right) in enumerate(pairs):
            a, b = s.ref(left), s.ref(right)
            c.require(a['path'] != b['path'], 'self-comparison refused')
            c.require(s.read(a['path']) == s.read(b['path']), 'actual exact-byte comparison failed')
            inputs[a['path']] = a
            outputs[b['path']] = b
            checks.append({'name': 'whole-byte-' + str(i + 1), 'passed': True,
                           'comparator': s.ref('scripts/reference/wordling_edits.py'),
                           'method': 'byte_equal', 'left': SOURCE + ':' + a['path'],
                           'right': SOURCE + ':' + b['path'], 'tolerance': 'exact'})
        c.require(not (inputs.keys() & outputs.keys()), 'ambiguous raw comparison roles')
        common = {'implementation_commit': EXECUTED_TREE, 'case_id': case['id'],
                  'case_revision': c.revision(case), 'scope': scope, 'argv': argv}
        b = {**common, 'entrypoint': 'cmd/wordling', 'build_argv': build['argv'],
             'build_exit_code': 0, 'environment': s.ref(BASE + 'preparations/app-b/inputs.json'),
             'build_log': s.ref(BASE + 'preparations/app-b/build.stdout'),
             'executable': binary_ref, 'review': review}
        bpath, rpath = BUNDLE + name + '-build.json', BUNDLE + name + '-run.json'
        envelopes[bpath] = c.encoded(b)
        run = {**common, 'kind': 'product-differential' if level == 'differential' else 'product-execution',
               'implementer': 'codex/implementer-ivan', 'executed': True, 'exit_code': 0,
               'executable_sha256': BINARY_SHA, 'baseline_id': case['baseline_id'],
               'profile': profile, 'inputs': list(inputs.values()), 'outputs': list(outputs.values()),
               'checks': checks, 'build': {'commit': '@BUNDLE@', 'path': bpath, 'sha256': c.digest(envelopes[bpath])}}
        envelopes[rpath] = c.encoded(run)
        rows.append({'id': 'WP29-' + name, 'level': level, 'state': 'pass', 'case_id': case['id'],
                     'case_revision': c.revision(case), 'scope': scope,
                     'run': {'commit': '@BUNDLE@', 'path': rpath, 'sha256': c.digest(envelopes[rpath])}, 'review': review})
        bindings.append({'id': 'WP29-' + name, 'case_id': case['id'], 'case_revision': c.revision(case),
                         'parent_case_ids': case['parent_case_ids'], 'scope': scope,
                         'comparison': 'exact whole native bytes or original selected-profile PRN only',
                         'details': details, 'whole_parent_status': 'open'})

    for recipe in recipes:
        pair = [r for r in plan['cases'] if r['id'] == recipe['id']]
        c.require([r['repeat'] for r in pair] == [1, 2], 'missing independent app repetitions')
        details = []
        for row in pair:
            folder = row['folder']
            p, frames, injected = process(s, folder, plan['binary'])
            result = s.js(folder + '/result.json')
            c.require(result['id'] == recipe['id'] and result['outcome'] == 'app-emitted'
                      and result['declared_final_gap'] == recipe['gap'] and result['body_hex'] == recipe['body'],
                      'actual case/body/gap/result mismatch')
            provenance = s.js(folder + '/provenance.json')
            c.require(provenance['app_argv'] == p['argv'] and provenance['binary'] == plan['binary'],
                      'product provenance mismatch')
            details.append({'repeat': row['repeat'], 'argv': p['argv'], 'process': s.ref(folder + '/process.json'),
                            'commands': s.ref(folder + '/injected.json'), 'frames': s.ref(folder + '/frames.json'),
                            'result': s.ref(folder + '/result.json'), 'provenance': s.ref(folder + '/provenance.json'),
                            'expectations': s.ref(folder + '/expectations.json'), 'candidate': s.ref(folder + '/files/CANDIDA'),
                            'source': s.ref(folder + '/files/ORIGIN'), 'later_gap_marker': s.ref(folder + '/files/MARKER'),
                            'semantic_gap': recipe['gap'], 'whole_native_alias_of': row['whole_byte_alias_of']})
        emit('app-' + recipe['id'], 'executable_integration', extmap[recipe['id']],
             'Two actual PTY ' + recipe['id'] + ' publications produce identical whole-native output; commands/gaps separately bound, not a full scenario pass.',
             details[0]['argv'], [(pair[0]['folder'] + '/files/CANDIDA', pair[1]['folder'] + '/files/CANDIDA')], details)

    verdict = s.verdict
    c.require(verdict['original_attempts_inclusive'] == 19 and len(verdict['classes']) == 8
              and verdict['successor']['accepted'] == 16 and verdict['physical_qualified'] is False,
              'original scope/accounting/qualification changed')
    for path, identity in plan['predecessor']['custody'].items():
        c.require(c.digest(s.read(path)) == identity['sha256'], 'predecessor custody mismatch')
    controls = plan['predecessor']['control_streams']
    c.require(len(controls) == 2 and s.read(relative(controls[0]['path'])) == s.read(relative(controls[1]['path'])), 'predecessor control streams differ')
    old = s.js(BASE + 'oracle/ledger.json')
    new = s.js(BASE + 'oracle-successor-01/ledger.json')
    c.require(old['halted'] is True and len(old['attempts']) == 3 and not new['halted']
              and len(new['attempts']) == 16 and new['prior_spent_attempts'] == 3 and new['cumulative_cap'] == 19,
              'incomplete attempt laundered or accounting reset')
    c.require(c.digest(s.read(BASE + 'oracle/ledger.json')) == 'b73fe3405e4443c16636a3a8771699a520446760fdc6bd31275610b02c5f7303', 'old halted ledger changed')
    for cls in verdict['classes']:
        pairs, details = [], []
        c.require(len(cls['fresh_original_runs']) == 2, 'differential repetition missing')
        for i, run in enumerate(cls['fresh_original_runs']):
            folder = run['directory']
            recorded = s.js(folder + '/comparison.json')
            c.require(run['accepted'] is True and recorded['accepted'] is True, 'incomplete original cannot pass')
            complete = s.js(folder + '/leaf-complete.json')
            release = s.js(folder + '/oracle-slot-release.json')
            c.require(complete['outcome'] == 'accepted' and release['owned_process_stop_confirmed'] is True
                      and release['before_offline_comparison'] is True, 'missing normal stop/extraction/comparison')
            rawrun = s.js(folder + '/run.json')
            rawframes = []
            for artifact in rawrun['artifacts']:
                state = artifact['path'].split('/')[0]
                if state in {'candidate-retrieved', 'candidate-before-subsequent-edit', 'candidate-after-subsequent-edit', 'clean-exit', 'settings-print-P0002-job-status'} and artifact['path'].endswith(('/screen.txt', '/vram.bin', '/cursor.json')):
                    ref = s.ref(folder + '/' + artifact['path'])
                    c.require(ref['sha256'] == artifact['sha256'], 'original state artifact mismatch')
                    rawframes.append(ref)
            for name in ['screen.txt', 'vram.bin', 'cursor.json']:
                golden = run['exact_normal_DOS']['reference_files'][name]['path']
                c.require(s.read(folder + '/clean-exit/' + name) == s.read(golden),
                          'post-wait normal DOS text/VGA/cursor differs')

            c.require(rawrun['resources'] == verdict['reference_resources'], 'original resource/profile mismatch')
            reference = cls['reference']
            if cls['id'] == 'three-entry-eviction':
                reference = relative(plan['predecessor']['control_streams'][i]['path'])
            pairs.append((reference, run['complete_print']['path']))
            details.append({'repeat': i + 1, 'run': s.ref(folder + '/run.json'),
                            'comparison': s.ref(folder + '/comparison.json'),
                            'stop': s.ref(folder + '/owned-stop.json'), 'release': s.ref(folder + '/oracle-slot-release.json'),
                            'prelaunch': s.ref(folder + '/owned-prelaunch.json'),
                            'completion': s.ref(folder + '/leaf-complete.json'),
                            'native_exports': [s.ref(folder + '/' + n) for n in ['N0000.WP5', 'N0001.WP5', 'N0003.WP5']],
                            'original_DOS_final': run['exact_normal_DOS'], 'original_raw_states': rawframes, 'resource_receipt': rawrun['resources']})
        app = next(r for r in plan['cases'] if r['id'] == cls['id'])
        proc = s.js(app['folder'] + '/process.json')
        emit('print-' + cls['id'], 'differential', extmap[cls['id']],
             'Actual app-emitted ' + cls['id'] + ' full-native class: two original Retrieve/+Z/Save/complete selected text-profile PRN/Save observations; PRN exact reference equality only, no Wordling print engine/geometry claim.',
             proc['argv'], pairs, details)

    report = s.js(BASE + 'reopen/successor-01/reopen-report.json')
    c.require(report['paths'] == 60 and len(report['unique_whole_native_inputs']) == 29
              and len(report['aliases']) == 31, 'reopen worker/path/alias scope changed')
    source_names, workers, probes = set(), set(), {}
    for i, row in enumerate(report['unique_whole_native_inputs']):
        folder, source = row['folder'], relative(row['source'])
        p, frames, injected = process(s, folder, plan['binary'])
        c.require(s.read(source) == s.read(folder + '/files/ORIGIN') == s.read(folder + '/files/CANDIDA'), 'noedit native changed')
        workers.add((p['pid'], p['pid_identity']['start_ticks']))
        source_names.add(source)
        probe = row['actual_mutation_probe']
        probes[probe] = probes.get(probe, 0) + 1
        emit('reopen-' + str(i + 1), 'executable_integration', reopen_case,
             'Original exported whole-native class ' + str(i + 1) + ': actual Retrieve/no-edit SaveAs exact bytes; subsequent unsaved initial-gap X admission is separately recorded and discarded.',
             p['argv'], [(source, folder + '/files/CANDIDA')],
             {'source': s.ref(source), 'process': s.ref(folder + '/process.json'), 'commands': s.ref(folder + '/injected.json'),
              'frames': s.ref(folder + '/frames.json'), 'probe_frame': row['probe_frame'], 'admission': probe,
              'scope': row['scope'], 'noedit_only': True})
    c.require(len(workers) == 29 and probes == {'recognized-readonly-refused-edit': 27, 'mutation-admitted-at-this-specific-gap': 2}, 'wrong reopen admission or worker count')
    aliases = []
    worker_sources = set(source_names)
    for alias in report['aliases']:
        left, right = relative(alias['source']), relative(alias['whole_native_alias_of'])
        c.require(right in worker_sources and left not in source_names, 'alias loses distinct source/representative')
        a, b = s.read(left), s.read(right)
        c.require(a == b and len(a) == alias['identity']['size'] and c.digest(a) == alias['identity']['sha256'], 'whole-byte alias mismatch')
        aliases.append({'source': s.ref(left), 'representative': s.ref(right), 'identity': alias['identity']})
        source_names.add(left)
    c.require(len(source_names) == 60, 'missing original exported native path')
    nonpasses = [('old-app-a-F10', 'executable_integration', 'fail', 'CMD51-200',
                  'Historical ninth app-a F10 failure retained; independently approved36 repaired it before unchanged app-b recipe. Not a current pass.'),
                 ('old-original-attempt3', 'differential', 'blocked', 'CMD51-149',
                  'Historical first candidate comparison-incomplete due missing redirected ledger; old halted ledger3 unchanged, no retrocomparison/acceptance.'),
                 ('EC045-intermediate', 'executable_integration', 'blocked', 'CMD51-045',
                  'Actual intermediate history remains unsupported; no compound future-key replay or whole-scenario claim.'),
                 ('physical-text-printer', 'physical_qualification', 'unverified', 'CMD51-145',
                  'Original-only selected text disk-port streams do not qualify graphics, physical delivery, geometry, historical DOS or Wordling print engine.')]
    for name, level, state, case_id, note in nonpasses:
        rows.append({'id': 'WP29-' + name, 'level': level, 'state': state, 'case_id': case_id,
                     'case_revision': c.revision(cases[case_id]), 'scope': 'Bounded retained WP29 disposition', 'note': note})
    component_paths = [
        ('WP15', 'WP15-readonly-document/review-cycle-1.md', 'Immutable shared document/token gaps; read-only preservation, not semantic writer breadth.'),
        ('WP25', 'WP25-supported-native-edit-writer/review-cycle-1.md', 'Qualified ASCII/typeover and original candidate export; initial two-pair policy.'),
        ('WP26', 'WP26-deletion-and-undelete/review-cycle-1.md', 'Qualified contextual pair/block/three-entry history only; unknown-count and interleavings retained.'),
        ('WP27', 'WP27-editable-session-reducer/review-cycle-2.md', 'Pure reducer and selected Backspace; unobserved selected Delete refuses.'),
        ('WP28', 'WP28-editable-bubbletea-session/review-cycle-1.md', 'Actual key/PTy composition, not physical delivery qualification.'),
        ('WP36', 'WP36-macro-editor-adapter/review-cycle-1.md', 'Immediate F10 repair on exact tested scopes; no general history clearing.'),
        ('WP41', 'WP41-source-less-native-publication/review-cycle-1.md', 'Prepared candidate publication and source guards; no generic replacement/new-document writer.')]
    components = [{'id': ident, 'review': s.ref(c.MISSION + 'tasks/' + path, REVIEWED),
                   'scope': scope, 'disposition': 'reviewed component provenance; no new component binary pass imported'}
                  for ident, path, scope in component_paths]
    readiness = {'schema_version': 1, 'kind': 'future-readiness-bindings-not-acceptance',
                 'parity_accepted': False, 'all_m1_obligations_closed': False, 'queue_exhaustion_authorizes_acceptance': False,
                 'source_commit': SOURCE, 'reviewed_evidence_tree': REVIEWED, 'review': review,
                 'independent_report': review_report, 'approval_event': APPROVAL,
                 'canonical_review_result': approval_event(root), 'canonical_review_events_reference': APPROVAL_EVENTS,
                 'producer': {'historical_source_commit': build['actual_source']['actual_head'], 'binary': binary_ref,
                              'actual_build': s.ref(BASE + 'preparations/app-b/build.json'), 'go_module_input_count': 90,
                              'compiled_local_package_count': 9, 'current_lane_inputs_are_not_the_producer': True,
                              'misleading_VCS_stamp_is_not_compiled_commit': True,
                              'large_archive_policy': 'Pinned historical provenance reports are streamed/hash-only under64MiB; v1 comparisons remain8MiB maximum, exact native/PRN only.'},
                 'counts': {'actual_acceptance_processes': 20, 'sourced_fixture_builders': 2,
                            'original_observations': 16, 'original_predecessor_controls': 2, 'original_incomplete': 1,
                            'original_attempts_inclusive': 19, 'whole_native_classes': 8,
                            'executable_reopen_workers': 29, 'original_native_paths': 60, 'whole_byte_aliases': 31,
                            'read_only_admission': 27, 'unsaved_gap0_admission_only': 2,
                            'positive_exact_comparison_rows': len(bindings), 'component_positive_rows': 0},
                 'requirements': baseline['requirements'], 'groups': baseline['groups'],
                 'scenario_obligations': [{'id': 'SC-00' + str(i), 'status': 'open', 'missing': 'Complete breadth/resources and workflow proof remain required.'} for i in range(1, 6)],
                 'bindings': bindings, 'aliases': aliases, 'inherited_components': components, 'qualification_limits': verdict['qualification_limits'],
                 'profile_limits': verdict['profile_limits'], 'edited_native_contract': verdict['edited_native_contract'],
                 'source_custody': verdict['source_custody'], 'original_behavior_scope': verdict['original_behavior_scope'],
                 'history_accounting': {'historical': verdict['historical_grant'], 'successor': verdict['successor']},
                 'failure_observations': verdict['failure_observations'],
                 'failure_bindings': {
                     'app_a_F10': [s.ref(BASE + p) for p in ['blocked-save/finding.json', 'blocked-save/original-locators.json', 'preparations/app-a/normal-paired-delete-r1/process.json', 'preparations/app-a/normal-paired-delete-r1/frames.json', 'preparations/app-a/normal-paired-delete-r1/wire-output.bin']],
                     'old_original_incomplete': [s.ref(BASE + p) for p in ['oracle-fault-01/no-edit-two-pair-r1.stderr', 'oracle-fault-01/diagnosis.json', 'oracle/ledger.json']],
                     'component_checks': [s.ref(BASE + p) for p in ['protocol-successor-01/validation.xml', 'protocol-successor-01/configured.txt']]
                 }, 'component_status': 'Inherited component checks are separately recorded, not product/physical passes or a new bound test-binary witness.',
                 'remaining': 'All38 obligations/91 groups/36 lessons and nested leaves remain open: full native/companions, new documents, replacement/backups, language/locales, other attributes/search, macro/merge/structures, layout/fonts/pages/preview/print engine, platform/physical/resources. M2/PDF not started.',
                 'raw_references': list(s.refs.values())}
    return envelopes, extensions, rows, readiness


def materialize(root, commit):
    envelopes, extensions, rows, report = generate(root)
    c.require(isinstance(commit, str) and len(commit) == 40, 'committed witness bundle required')
    # Build references use a separate immutable binary commit; run references must
    # refer to the already committed build envelopes. No future/self-hash cycle.
    for path, raw in list(envelopes.items()):
        if path.endswith('-run.json'):
            value = c.load_json(raw)
            value['build']['commit'] = commit
            envelopes[path] = c.encoded(value)
    return envelopes, extensions, rows, report


def proposed(root, commit):
    envelopes, extensions, rows, report = materialize(root, commit)
    for path, raw in envelopes.items():
        # Run envelopes are generated in phase2, so their storage commit may differ
        # from the phase1 build envelope commit. RUN_COMMIT is fixed after sealing.
        at = RUN_COMMIT if path.endswith('-run.json') else commit
        c.require(at is not None, 'committed run bundle required')
        c.require(c.blob(root, {'commit': at, 'path': path, 'sha256': c.digest(raw)}) == raw, 'bundle mismatch')
    for row in rows:
        if row['state'] == 'pass':
            path = row['run']['path']
            row['run'] = {'commit': RUN_COMMIT, 'path': path, 'sha256': c.digest(envelopes[path])}
    baseline = c.build(root)
    baseline['extensions'] = extensions
    baseline['evidence'] = rows
    row_map = {row['id']: row for row in rows}
    for binding in report['bindings']:
        binding['record_revision'] = c.revision(row_map[binding['id']])
        binding['criterion_reference'] = 'BOUND-' + binding['id']
        binding['candidate_for_future_acceptance_only'] = True
    report['imported_slice_revision'] = c.revision(rows)
    return baseline, report


RUN_COMMIT = '302d20b2f39e8e266c42933ba3de67dc02b9ff04'


def audit_custody(root):
    """Stream every approved WP29 artifact and Git blob without running its helpers."""
    snapshot = Snapshot(root)
    records = list(snapshot.records.values())
    total = sum(r['size'] for r in records)
    c.require(total == 1043070144, 'approved raw custody size changed')
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_OPTIONAL_LOCKS='0', GIT_NO_REPLACE_OBJECTS='1')
    with tempfile.TemporaryFile() as requests:
        for row in records:
            path = c.safe_path(row['path'])
            c.require(0 <= row['size'] <= 64 * 1024 * 1024, 'custody streaming file budget exceeded')
            requests.write((SOURCE + ':' + path + '\n').encode())
        requests.seek(0)
        with subprocess.Popen(['git', '--no-optional-locks', '-C', str(root), 'cat-file', '--batch'],
                              stdin=requests, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env) as proc:
            for row in records:
                header = proc.stdout.readline().split()
                c.require(len(header) == 3 and header[1] == b'blob' and int(header[2]) == row['size'],
                          'missing/wrong Git custody blob: ' + row['path'])
                remaining, digest = row['size'], hashlib.sha256()
                while remaining:
                    chunk = proc.stdout.read(min(remaining, 65536))
                    c.require(bool(chunk), 'truncated custody stream')
                    digest.update(chunk); remaining -= len(chunk)
                c.require(proc.stdout.read(1) == b'\n' and digest.hexdigest() == row['sha256'],
                          'Git custody hash mismatch: ' + row['path'])
                path = c.local(root, row['path'])
                c.require(path.is_file() and path.stat().st_size == row['size'], 'missing working custody artifact')
                digest = hashlib.sha256()
                with path.open('rb') as stream:
                    for chunk in iter(lambda: stream.read(65536), b''):
                        digest.update(chunk)
                c.require(digest.hexdigest() == row['sha256'], 'working custody hash mismatch: ' + row['path'])
            c.require(not proc.stdout.read(1) and proc.wait(timeout=15) == 0, 'Git custody batch failed')
    return {'result': 'valid', 'raw_records': len(records), 'raw_bytes': total,
            'source_commit': SOURCE, 'Git_and_working_bytes_exact': True,
            'guest_or_product_launched': False, 'parity_accepted': False}


def publish(root, outputs):
    """Stage all data before replacing any; roll back a normal publication error.

    This is CLI failure safety, not a multi-file filesystem crash transaction.
    """
    allowed = {c.DIRECTORY + 'registry.json', c.DIRECTORY + 'index.md', OUT + 'readiness.json'}
    c.require(set(outputs) == allowed, 'unexpected ingestion output set')
    paths = {name: c.local(root, name) for name in outputs}
    for path in paths.values():
        c.require(not path.exists() or path.is_file(), 'output is not a file')
    staged, backups, changed = {}, {}, []
    def stage(path, raw):
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.wp31-', delete=False) as stream:
            name = Path(stream.name)
            staged_files.append(name)
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        return name
    staged_files = []
    try:
        for name, path in paths.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            prior = path.read_bytes() if path.exists() else None
            backups[name] = stage(path, prior) if prior is not None else None
            staged[name] = stage(path, outputs[name])
        try:
            for name, path in paths.items():
                os.replace(staged[name], path)
                changed.append(name)
        except OSError:
            for name in reversed(changed):
                if backups[name] is None:
                    paths[name].unlink()
                else:
                    os.replace(backups[name], paths[name])
            raise
    finally:
        for path in staged_files:
            path.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[3])
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('audit-custody')
    sub.add_parser('prepare-builds')
    runp = sub.add_parser('prepare-runs')
    runp.add_argument('--build-commit', required=True)
    for cmd in ['check', 'write', 'report', 'validate']:
        p = sub.add_parser(cmd)
        if cmd == 'validate':
            p.add_argument('--proposal', type=Path, required=True)
    args = parser.parse_args()
    try:
        root = args.root.resolve(strict=True)
        if args.command == 'audit-custody':
            print(json.dumps(audit_custody(root), sort_keys=True))
            return 0
        if args.command in ['prepare-builds', 'prepare-runs']:
            if args.command == 'prepare-builds':
                envelopes, _, _, _ = generate(root)
                outputs = {p: raw for p, raw in envelopes.items() if p.endswith('-build.json')}
            else:
                envelopes, _, _, _ = materialize(root, args.build_commit)
                outputs = {p: raw for p, raw in envelopes.items() if p.endswith('-run.json')}
            for name, raw in outputs.items():
                path = c.local(root, name)
                c.require(not path.exists() or path.read_bytes() == raw, 'witness conflict: ' + name)
            c.write_outputs(root, outputs)
            print(json.dumps({'result': 'prepared', 'files': len(outputs), 'parity_accepted': False}))
            return 0
        value, report = proposed(root, BUNDLE_COMMIT)
        path = c.local(root, c.DIRECTORY + 'registry.json')
        current = c.validate(root, c.load_json(path.read_bytes()))
        # Existing additions are retained; same identities can never change or vanish.
        for key in ['extensions', 'additional_obligations', 'evidence']:
            expected = {x['id']: x for x in value[key]}
            for item in current[key]:
                if item['id'] in expected:
                    c.require(c.encoded(item) == c.encoded(expected[item['id']]), 'conflicting repeated identity: ' + item['id'])
                else:
                    value[key].append(item)
        if c.encoded(current) != c.encoded(value):
            c.validate(root, value)
        if args.command == 'validate':
            proposal = c.load_json(args.proposal.read_bytes())
            c.validate(root, proposal)
            c.require(c.encoded(proposal) == c.encoded(value), 'proposal differs from exact reviewed WP29 import: source/case/scope/profile/alias/status/coverage')
        elif args.command == 'write':
            publish(root, {c.DIRECTORY + 'registry.json': c.encoded(value),
                                   c.DIRECTORY + 'index.md': c.render(value),
                                   OUT + 'readiness.json': c.encoded(report)})
        elif args.command == 'check':
            c.require(c.encoded(current) == c.encoded(value), 'current registry differs: run explicit write')
            c.require(c.local(root, OUT + 'readiness.json').read_bytes() == c.encoded(report), 'readiness bindings drift')
            c.require(c.local(root, c.DIRECTORY + 'index.md').read_bytes() == c.render(value), 'index drift')
        if args.command == 'report':
            print(json.dumps(report, sort_keys=True))
        else:
            print(json.dumps({'result': 'valid', 'command': args.command, 'evidence_rows': len(value['evidence']),
                              'original_attempts_inclusive': 19, 'parity_accepted': False}, sort_keys=True))
        return 0
    except (c.Invalid, OSError, ValueError, TypeError, KeyError, subprocess.SubprocessError) as exc:
        print(json.dumps({'result': 'invalid', 'error': str(exc)}, sort_keys=True))
        return 1


if __name__ == '__main__':
    sys.exit(main())
