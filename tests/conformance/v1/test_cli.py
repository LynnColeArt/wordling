"""Public CLI acceptance and corruption checks; no private module imports."""
import copy
import hashlib
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
CLI = ROOT / 'scripts/conformance/v1/conformance.py'
REG = ROOT / 'docs/conformance/v1/registry.json'


class ConformanceCLI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = json.loads(REG.read_text())

    def cli(self, *args):
        return subprocess.run([sys.executable, str(CLI), '--root', str(ROOT), *args],
                              text=True, capture_output=True)

    def validate(self, data):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'registry.json'
            p.write_text(json.dumps(data))
            before = p.read_bytes()
            result = self.cli('validate', '--registry', str(p))
            self.assertEqual(p.read_bytes(), before)
            return result

    def reject(self, mutate, message=None):
        data = copy.deepcopy(self.base)
        mutate(data)
        result = self.validate(data)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        error = json.loads(result.stdout)['error']
        if message:
            self.assertIn(message, error)

    def test_default_check_read_only(self):
        paths = [ROOT / p['path'] for p in self.base['source_snapshots']
                 if (ROOT / p['path']).exists()]
        paths += [REG, REG.with_name('index.md'), REG.with_name('schema.json')]
        before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        git_before = subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT)
        result = self.cli('check')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(before, {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
        self.assertEqual(git_before, subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT))

    def test_import_idempotent(self):
        paths = [REG, REG.with_name('index.md'), REG.with_name('schema.json')]
        before = [p.read_bytes() for p in paths]
        for command in ('import', 'regenerate', 'check'):
            result = self.cli(command)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(before, [p.read_bytes() for p in paths])

    def test_valid_default(self):
        result = self.validate(self.base)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(len(self.base['historical']['cases']), 244)
        self.assertEqual(len(self.base['historical']['features']), 91)
        self.assertEqual(len(self.base['requirements']), 38)

    def test_missing_duplicate_and_old_primary_cases(self):
        self.reject(lambda d: d['historical']['cases'].pop(), 'historical')
        self.reject(lambda d: d['historical']['cases'].append(d['historical']['cases'][0]), 'historical')
        self.reject(lambda d: d['historical'].__setitem__('cases', d['historical']['cases'][:236]), 'historical')

    def test_source_hash_and_inherited_semantics(self):
        self.reject(lambda d: d['source_snapshots'][0].__setitem__('sha256', '0' * 64), 'source_snapshots')
        self.reject(lambda d: d['historical']['cases'][0].__setitem__('title', 'changed'), 'historical')
        self.reject(lambda d: d['historical']['features'][0].__setitem__('command_scenario_ids', []), 'historical')
        self.reject(lambda d: d['historical']['cases'][0].__setitem__('source_locators', []), 'historical')

    def test_missing_obligation_leaf_resource(self):
        self.reject(lambda d: d['requirements'].pop(), 'requirements')
        self.reject(lambda d: d['discovery']['reference_leaves'].pop(), 'discovery')
        self.reject(lambda d: d['resources']['formats'].pop(), 'resources')
        self.reject(lambda d: d['resources']['locales'][0].__setitem__('qualified', True), 'resources')

    def test_parent_and_mission_closure_forbidden(self):
        self.reject(lambda d: d['requirements'][0].__setitem__('status', 'passed'), 'requirements')
        self.reject(lambda d: d['groups'][0].__setitem__('status', 'closed'), 'groups')
        self.reject(lambda d: d['mission'].__setitem__('parity_accepted', True), 'mission')
        self.reject(lambda d: d.__setitem__('schema_version', 2), 'schema_version')
        self.reject(lambda d: d.__setitem__('exclusions', ['encryption']), 'fields')

    @staticmethod
    def extension():
        return {'id': 'EXT51-0001', 'revision': 1, 'supersedes': None,
                'title': 'Documentary insertion branch extension',
                'feature_ids': ['WP51-012'], 'requirement_ids': ['FR-005'],
                'parent_case_ids': ['CMD51-046'], 'baseline_id': 'wp51-dos-us-1992-03-09',
                'source_locators': [{'source_id': 'REF51', 'printed_start': 10,
                                     'printed_end': 11, 'pdf_start': 27, 'pdf_end': 28}],
                'preconditions': ['Owned scratch input at declared gap'],
                'steps': ['Use the original branch under study'],
                'expected': ['Capture original result before any implementation claim']}

    def test_versioned_extension_and_duplicate_parent_lineage_guards(self):
        data = copy.deepcopy(self.base)
        data['extensions'].append(self.extension())
        self.assertEqual(self.validate(data).returncode, 0)
        self.reject(lambda d: d['extensions'].extend([self.extension(), self.extension()]), 'duplicate')
        for key, value in [('id', 'CMD51-046'), ('feature_ids', ['WP51-999']),
                           ('parent_case_ids', ['CMD51-999']), ('parent_case_ids', ['CMD51-185']),
                           ('source_locators', []), ('source_locators', [{'source_id': 'REF51', 'printed_start': 10, 'printed_end': 11, 'pdf_start': 29, 'pdf_end': 30}]),
                           ('revision', 2), ('baseline_id', 'invented')]:
            def mutate(d, key=key, value=value):
                e = self.extension()
                e[key] = value
                d['extensions'].append(e)
            self.reject(mutate)

    def test_evidence_without_execution_cannot_pass(self):
        for level in ['component', 'executable_integration', 'differential', 'physical_qualification']:
            e = {'id': 'E-1', 'level': level, 'state': 'pass', 'case_id': 'CMD51-046',
                 'case_revision': '0' * 64, 'scope': 'bounded test', 'note': 'not proof'}
            self.reject(lambda d, e=e: d['evidence'].append(e))

    def test_nonpassing_evidence_is_not_closure(self):
        data = copy.deepcopy(self.base)
        case = data['historical']['cases'][0]
        digest = hashlib.sha256((json.dumps(case, sort_keys=True, separators=(',', ':'), ensure_ascii=False)+'\n').encode()).hexdigest()
        data['evidence'].append({'id': 'E-1', 'level': 'differential', 'state': 'blocked',
                                 'case_id': case['id'], 'case_revision': digest,
                                 'scope': 'not executed', 'note': 'Original execution missing'})
        self.assertEqual(self.validate(data).returncode, 0)
        self.assertTrue(all(r['status'] == 'open' for r in data['requirements']))

    def test_option_and_path_injection_in_evidence_refs(self):
        for commit, path in [('--help', 'README.md'), ('0'*40, '../README.md'),
                              ('HEAD', 'README.md'), ('0'*40, '/etc/passwd')]:
            data = copy.deepcopy(self.base)
            data['evidence'].append({'id': 'E-1', 'level': 'differential', 'state': 'pass',
                                     'case_id': 'CMD51-046', 'case_revision': hashlib.sha256((json.dumps(next(c for c in self.base['historical']['cases'] if c['id'] == 'CMD51-046'), sort_keys=True, separators=(',', ':'), ensure_ascii=False)+'\n').encode()).hexdigest(),
                                     'scope': 'test', 'run': {'commit': commit, 'path': path,
                                                           'sha256': '0'*64}})
            self.assertNotEqual(self.validate(data).returncode, 0)

    def test_committed_positive_envelope_and_real_corruption_guards(self):
        # A synthetic isolated Git repository tests the integrity protocol only;
        # these fixtures never enter the product registry or claim compatibility.
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(['git', 'init', '-q', str(repo)], check=True)
            common = subprocess.check_output(['git', 'rev-parse', '--git-common-dir'], cwd=ROOT, text=True).strip()
            objects = (ROOT / common / 'objects').resolve()
            (repo / '.git/objects/info/alternates').write_text(str(objects) + '\n')
            def commit(files):
                for name, raw in files.items():
                    p = repo / name
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_bytes(raw)
                subprocess.run(['git', 'add', '--', *files], cwd=repo, check=True)
                subprocess.run(['git', '-c', 'user.name=Fixture Implementer', '-c',
                                'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false',
                                'commit', '--allow-empty', '-qm', 'synthetic protocol fixture'], cwd=repo, check=True)
                return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip()
            code = commit({'cmd/wordling/fixture.txt': b'not executable product evidence\n'})
            raw = {'input.bin': b'preserved native fixture', 'output.bin': b'preserved native fixture',
                   'environment.json': b'{"environment":"synthetic test"}',
                   'resources.json': b'{"resources":"synthetic test"}',
                   'comparator.py': b'# synthetic protocol fixture: byte_equal\n',
                   'review.md': ('Approved by fixture-reviewer: ' + code + '\n').encode()}
            evidence_commit = commit(raw)
            def ref(name):
                return {'commit': evidence_commit, 'path': name,
                        'sha256': hashlib.sha256(raw[name]).hexdigest()}
            case = self.base['historical']['cases'][45]
            case_rev = hashlib.sha256((json.dumps(case, sort_keys=True, separators=(',', ':'), ensure_ascii=False)+'\n').encode()).hexdigest()
            run = {'kind': 'product-differential', 'case_id': case['id'], 'case_revision': case_rev,
                   'scope': 'synthetic protocol validation only', 'implementation_commit': code,
                   'implementer': 'fixture-implementer', 'executed': True, 'argv': ['./wordling', 'fixture'],
                   'exit_code': 0, 'executable_sha256': '1'*64, 'baseline_id': case['baseline_id'],
                   'profile': {'environment': [next(x for x in self.base['source_snapshots'] if x['path'].endswith('/environment.json'))], 'resources': [next(x for x in self.base['source_snapshots'] if x['path'].endswith('/resource-profile.json'))],
                               'qualification': 'unqualified'},
                   'inputs': [ref('input.bin')], 'outputs': [ref('output.bin')],
                   'checks': [{'name': 'raw exact preservation', 'passed': True,
                               'comparator': ref('comparator.py'), 'method': 'byte_equal',
                               'left': evidence_commit+':input.bin', 'right': evidence_commit+':output.bin',
                               'tolerance': 'exact'}]}
            def check(run, change_evidence=None):
                run_raw = json.dumps(run).encode()
                run_commit = commit({'run.json': run_raw})
                data = copy.deepcopy(self.base)
                e = {'id': 'E-FIXTURE', 'level': 'differential', 'state': 'pass', 'case_id': case['id'],
                     'case_revision': case_rev, 'scope': run['scope'],
                     'run': {'commit': run_commit, 'path': 'run.json', 'sha256': hashlib.sha256(run_raw).hexdigest()},
                     'review': {'artifact': ref('review.md'), 'reviewer': 'fixture-reviewer'}}
                if change_evidence:
                    change_evidence(e)
                data['evidence'] = [e]
                path = repo/'fixture-registry.json'
                path.write_text(json.dumps(data))
                return subprocess.run([sys.executable, str(CLI), '--root', str(repo),
                                       'validate', '--registry', str(path)], capture_output=True, text=True)
            self.assertEqual(check(run).returncode, 0)
            for mutation, expected in [
                (lambda r: r.__setitem__('executed', False), 'nonexecuted'),
                (lambda r: r.__setitem__('kind', 'original-reference-only'), 'helper/original-only'),
                (lambda r: r.__setitem__('argv', ['./serializer-helper']), 'invoke wordling'),
                (lambda r: r['inputs'][0].__setitem__('sha256', '0'*64), 'hash mismatch'),
                (lambda r: r.__setitem__('case_revision', '0'*64), 'revision/scope'),
                (lambda r: r['profile'].__setitem__('resources', []), 'resources'),
                (lambda r: r['profile'].__setitem__('resources', [ref('resources.json')]), 'unknown environment/resource profile'),
                (lambda r: r['checks'][0].__setitem__('right', r['checks'][0]['left']), 'self-comparison'),
                (lambda r: r['checks'][0].__setitem__('method', 'trust-passed-boolean'), 'unsupported comparator'),
                (lambda r: r.__setitem__('implementation_commit', evidence_commit), 'does not approve'),
            ]:
                altered = copy.deepcopy(run)
                mutation(altered)
                result = check(altered)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn(expected, json.loads(result.stdout)['error'])
            for change in [lambda e: e['run'].__setitem__('commit', '--help'),
                           lambda e: e['run'].__setitem__('path', '../run.json'),
                           lambda e: e['review'].__setitem__('reviewer', 'fixture-implementer'),
                           lambda e: e.pop('review')]:
                self.assertNotEqual(check(run, change).returncode, 0)
            physical = copy.deepcopy(run)
            physical['kind'] = 'physical-qualification'
            result = check(physical, lambda e: e.__setitem__('level', 'physical_qualification'))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('unqualified resource', json.loads(result.stdout)['error'])
            # A fully hash-bound but unequal output must fail despite passed:true.
            raw['output.bin'] = b'different output'
            evidence_commit = commit({'output.bin': raw['output.bin']})
            different = copy.deepcopy(run)
            different['outputs'] = [ref('output.bin')]
            different['checks'][0]['right'] = evidence_commit + ':output.bin'
            result = check(different)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('recomputed comparator failed', json.loads(result.stdout)['error'])
            # JSON comparison tolerates key/whitespace order, but not value-type changes.
            raw['input.bin'] = b'{"a":true,"b":2}'
            raw['output.bin'] = b'{ "b": 2, "a": true }'
            evidence_commit = commit({name: raw[name] for name in ['input.bin', 'output.bin']})
            json_run = copy.deepcopy(run)
            json_run['inputs'] = [ref('input.bin')]
            json_run['outputs'] = [ref('output.bin')]
            json_run['checks'][0].update(method='json_equal', left=evidence_commit+':input.bin',
                                         right=evidence_commit+':output.bin')
            self.assertEqual(check(json_run).returncode, 0)
            raw['output.bin'] = b'{"a":1,"b":2}'
            evidence_commit = commit({'output.bin': raw['output.bin']})
            json_run['outputs'] = [ref('output.bin')]
            json_run['checks'][0]['right'] = evidence_commit+':output.bin'
            result = check(json_run)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('recomputed comparator failed', json.loads(result.stdout)['error'])

    def test_source_drift_and_failed_regeneration_write_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(['git', 'init', '-q', str(repo)], check=True)
            common = subprocess.check_output(['git', 'rev-parse', '--git-common-dir'], cwd=ROOT, text=True).strip()
            (repo / '.git/objects/info/alternates').write_text(str((ROOT/common/'objects').resolve())+'\n')
            def cli(command):
                return subprocess.run([sys.executable, str(CLI), '--root', str(repo), command],
                                      text=True, capture_output=True)
            self.assertEqual(cli('import').returncode, 0)
            docs = repo/'docs/conformance/v1'
            before = {p.name: p.read_bytes() for p in docs.iterdir()}
            source = repo/'docs/research/command-scenarios.json'
            source.parent.mkdir(parents=True)
            source.write_text(json.dumps(self.base['historical']['cases'][:236]))
            for command in ['check', 'regenerate', 'import']:
                result = cli(command)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('working source drift', json.loads(result.stdout)['error'])
                self.assertEqual(before, {p.name: p.read_bytes() for p in docs.iterdir()})
            source.unlink()
            (docs/'index.md').write_text('stale current index')
            self.assertNotEqual(cli('check').returncode, 0)
            self.assertNotEqual(cli('import').returncode, 0)  # never overwrites a divergent output
            self.assertEqual(cli('regenerate').returncode, 0)
            self.assertEqual(before, {p.name: p.read_bytes() for p in docs.iterdir()})
            (docs/'index.md').unlink()
            outside = repo/'outside.txt'
            outside.write_text('untouched')
            (docs/'index.md').symlink_to(outside)
            self.assertNotEqual(cli('regenerate').returncode, 0)
            self.assertEqual(outside.read_text(), 'untouched')

    def test_check_git_calls_are_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            real_git = shutil.which('git')
            wrapper = tmp/'git'
            log = tmp/'git-calls.jsonl'
            wrapper.write_text('#!' + sys.executable + '\n' +
                               'import json, os, sys\n' +
                               'args=sys.argv[1:]\n' +
                               'assert args[0]=="--no-optional-locks" and args[1]=="-C" and args[3]=="cat-file", args\n' +
                               'with open(os.environ["WP30_CALLS"],"a") as f: f.write(json.dumps(args)+"\\n")\n' +
                               'os.execv(' + repr(real_git) + ', [' + repr(real_git) + '] + args)\n')
            wrapper.chmod(0o755)
            env = dict(os.environ, PATH=str(tmp)+os.pathsep+os.environ['PATH'], WP30_CALLS=str(log))
            result = subprocess.run([sys.executable, str(CLI), '--root', str(ROOT), 'check'],
                                    env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            calls = [json.loads(line) for line in log.read_text().splitlines()]
            self.assertTrue(calls)
            self.assertTrue(all(call[3] == 'cat-file' for call in calls))


if __name__ == '__main__':
    unittest.main()
