"""Public real-input ingestion tests; no product or original guest execution."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
CLI = ROOT / 'scripts/conformance/v1/ingest_wp29.py'

class IngestionCLI(unittest.TestCase):
    def test_real_dry_check(self):
        p = subprocess.run(['python3', str(CLI), 'check'], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        value = json.loads(p.stdout)
        self.assertFalse(value['parity_accepted'])
        self.assertEqual(value['original_attempts_inclusive'], 19)

    def test_readiness_has_no_parent_closure(self):
        p = subprocess.run(['python3', str(CLI), 'report'], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        value = json.loads(p.stdout)
        self.assertEqual(len(value['requirements']), 38)
        self.assertEqual(len(value['groups']), 91)
        self.assertTrue(all(x['status'] == 'open' for x in value['requirements'] + value['groups']))
        self.assertEqual(value['producer']['go_module_input_count'], 90)


class RejectionCLI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((ROOT / 'docs/conformance/v1/registry.json').read_text())
        cls.original_bytes = (ROOT / 'docs/conformance/v1/registry.json').read_bytes()

    def reject(self, value, expected=None):
        with tempfile.TemporaryDirectory(prefix='wp31-reject-') as temp:
            proposal = Path(temp) / 'proposal.json'
            raw = (json.dumps(value, sort_keys=True) + '\n').encode()
            proposal.write_bytes(raw)
            p = subprocess.run(['python3', str(ROOT / 'scripts/conformance/v1/conformance.py'),
                                'validate', '--registry', str(proposal)], cwd=ROOT,
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 1, p.stdout + p.stderr)
            if expected:
                self.assertIn(expected, p.stdout)
            self.assertEqual(proposal.read_bytes(), raw)
        self.assertEqual((ROOT / 'docs/conformance/v1/registry.json').read_bytes(), self.original_bytes)

    def copied(self):
        return json.loads(json.dumps(self.registry))

    def test_forged_full_flags_and_parent_closure(self):
        for flag in ['parity_accepted', 'all_m1_obligations_closed', 'queue_exhaustion_authorizes_acceptance']:
            value = self.copied(); value['mission'][flag] = True
            with self.subTest(flag=flag): self.reject(value, 'exact boolean false')
        for key in ['requirements', 'groups']:
            value = self.copied(); value[key][0]['status'] = 'pass'
            with self.subTest(key=key): self.reject(value, 'immutable typed')

    def test_omitted_discovered_leaves_and_old_snapshot(self):
        for key in ['historical', 'discovery', 'resources', 'source_snapshots']:
            value = self.copied()
            if key == 'historical': value[key]['cases'] = value[key]['cases'][:236]
            elif key == 'source_snapshots': value[key][0]['commit'] = '0' * 40
            else: value[key] = {}
            with self.subTest(key=key): self.reject(value, 'immutable typed')

    def test_wrong_valid_case_and_revision_and_partial_scope(self):
        for key, val in [('case_id', 'CMD51-069'), ('case_revision', '0' * 64),
                         ('scope', 'All native formats fully verified')]:
            value = self.copied(); value['evidence'][0][key] = val
            with self.subTest(key=key): self.reject(value)

    def test_missing_review_or_raw_and_forged_run_hash(self):
        for key in ['run', 'review']:
            value = self.copied(); del value['evidence'][0][key]
            with self.subTest(key=key): self.reject(value, 'invalid fields')
        value = self.copied(); value['evidence'][0]['run']['sha256'] = '1' * 64
        self.reject(value, 'hash mismatch')

    def test_bad_lineage_and_extra_duplicate_identity(self):
        value = self.copied(); value['extensions'][0]['supersedes'] = {'id': 'EXT51-9999', 'sha256': '0' * 64}
        self.reject(value, 'invalid extension lineage')
        value = self.copied(); value['evidence'].append(value['evidence'][0])
        self.reject(value, 'duplicate')

    def test_original_only_and_helper_only_and_physical_cannot_promote(self):
        for level in ['original_observation', 'documentary', 'physical_qualification', 'component']:
            value = self.copied(); value['evidence'][0]['level'] = level
            with self.subTest(level=level): self.reject(value)

    def test_fail_and_incomplete_cannot_become_pass(self):
        for index in [-1, -2, -3, -4]:
            value = self.copied(); value['evidence'][index]['state'] = 'pass'
            with self.subTest(index=index): self.reject(value, 'invalid fields')

    def test_matching_but_wrong_import_reference_rejected(self):
        value = self.copied()
        # A different real successful run is not a valid replacement for this ID.
        value['evidence'][0]['run'] = value['evidence'][1]['run']
        self.reject(value)

    def test_missing_import_row_cannot_silently_reduce_repetition_or_scope(self):
        value = self.copied(); value['evidence'].pop(1)
        self.reject(value, 'imported evidence set changed')


class SourceJoin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import sys
        sys.path.insert(0, str(ROOT / 'scripts/conformance/v1'))
        import ingest_wp29
        cls.w = ingest_wp29
        cls.product = json.loads((ROOT / 'docs/research/continuation/editing-differential/preparations/app-b/inputs.json').read_text())

    def test_publication_second_replace_failure_rolls_back_all_prior_data(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory(prefix='wp31-rollback-') as directory:
            root = Path(directory)
            outputs = {self.w.c.DIRECTORY + 'registry.json': b'new-registry',
                       self.w.c.DIRECTORY + 'index.md': b'new-index',
                       self.w.OUT + 'readiness.json': b'new-readiness'}
            original = {}
            for name in outputs:
                path = root / name; path.parent.mkdir(parents=True, exist_ok=True)
                original[name] = ('prior-' + name).encode(); path.write_bytes(original[name])
            replace = self.w.os.replace
            calls = []
            def fail_second(source, target):
                calls.append(str(target))
                if len(calls) == 2:
                    raise OSError('declared second publication failure')
                return replace(source, target)
            with patch.object(self.w.os, 'replace', side_effect=fail_second), self.assertRaises(OSError):
                self.w.publish(root, outputs)
            self.assertEqual({name: (root / name).read_bytes() for name in outputs}, original)
            self.assertFalse(list(root.rglob('.wp31-*')))

    def test_actual_complete_source_join(self):
        self.w.product_inputs(ROOT, self.w.Snapshot(ROOT), self.product)

    def test_missing_extra_changed_sources_and_wrong_compiled_set(self):
        for kind in ['missing', 'extra', 'hash', 'files', 'flags', 'tree']:
            value = json.loads(json.dumps(self.product))
            if kind == 'missing': value['product_inputs'].pop('cmd/wordling/main.go')
            if kind == 'extra': value['product_inputs']['internal/fake.go'] = {'size': 1, 'sha256': '0' * 64}
            if kind == 'hash': value['product_inputs']['cmd/wordling/main.go']['sha256'] = '0' * 64
            if kind == 'files': value['compiled_local_packages'][0]['go_files']['invented.go'] = {'size': 1, 'sha256': '0' * 64}
            if kind == 'flags': value['GOFLAGS'] = '-overlay=/tmp/forged'
            if kind == 'tree': value['actual_head'] = self.w.REVIEWED
            with self.subTest(kind=kind), self.assertRaises(self.w.c.Invalid):
                self.w.product_inputs(ROOT, self.w.Snapshot(ROOT), value)

    def test_actual_review_event_rejects_force_actor_result_or_missing_identity(self):
        from unittest.mock import patch
        raw = self.w.c.blob(ROOT, self.w.APPROVAL_EVENTS)
        original = [json.loads(line) for line in raw.splitlines()]
        self.w.approval_event(ROOT)
        for kind in ['force', 'actor', 'result', 'missing']:
            events = json.loads(json.dumps(original))
            event = next(e for e in events if e['event_id'] == self.w.APPROVAL)
            if kind == 'force': event['force'] = True
            if kind == 'actor': event['actor']['profile'] = 'implementer-ivan'
            if kind == 'result': event['review_result']['verdict'] = 'planned'
            if kind == 'missing': events.remove(event)
            changed = b''.join((json.dumps(e) + '\n').encode() for e in events)
            with self.subTest(kind=kind), patch.object(self.w.c, 'blob', return_value=changed), self.assertRaises(self.w.c.Invalid):
                self.w.approval_event(ROOT)

    def test_wrong_actor_source_and_report_cannot_use_new_join(self):
        value = json.loads((ROOT / 'docs/conformance/v1/registry.json').read_text())['evidence'][0]
        run = self.w.c.load_json(self.w.c.blob(ROOT, value['run']))
        self.w.approved_review(ROOT, run, value)
        for kind in ['actor', 'report', 'tree']:
            e, r = json.loads(json.dumps(value)), json.loads(json.dumps(run))
            if kind == 'actor': e['review']['reviewer'] = 'implementer-ivan'
            if kind == 'report': e['review']['artifact']['commit'] = self.w.REVIEWED
            if kind == 'tree': r['implementation_commit'] = self.w.REVIEWED
            with self.subTest(kind=kind), self.assertRaises(self.w.c.Invalid):
                self.w.approved_review(ROOT, r, e)



class RealRunEnvelopeMutants(unittest.TestCase):
    """Actual WP29 envelopes in an isolated object store, not synthetic product proof."""
    @classmethod
    def setUpClass(cls):
        import sys
        sys.path.insert(0, str(ROOT / 'scripts/conformance/v1'))
        import ingest_wp29 as w
        cls.w = w
        cls.registry = json.loads((ROOT / 'docs/conformance/v1/registry.json').read_text())
        cls.row = cls.registry['evidence'][0]
        cls.actual_run = w.c.load_json(w.c.blob(ROOT, cls.row['run']))
        cls.directory = tempfile.TemporaryDirectory(prefix='wp31-real-mutants-')
        cls.root = Path(cls.directory.name)
        subprocess.run(['git', 'init', '-q', str(cls.root)], check=True)
        common = subprocess.check_output(['git', 'rev-parse', '--path-format=absolute', '--git-common-dir'], cwd=ROOT, text=True).strip()
        (cls.root / '.git/objects/info/alternates').write_text(common + '/objects\n')
        cls.parent = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
        subprocess.run(['git', 'read-tree', cls.parent], cwd=cls.root, check=True)

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def test_explicit_write_preflight_failure_preserves_prior_registry(self):
        base = json.loads(json.dumps(self.registry))
        base['extensions'] = []; base['evidence'] = []
        path = self.root / 'docs/conformance/v1/registry.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        before = self.w.c.encoded(base); path.write_bytes(before)
        outside = self.root / 'outside.txt'; outside.write_text('untouched')
        target = self.root / 'docs/conformance/v1/imports/wp29/readiness.json'
        target.parent.mkdir(parents=True, exist_ok=True); target.symlink_to(outside)
        p = subprocess.run(['python3', str(CLI), '--root', str(self.root), 'write'],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(p.returncode, 1, p.stdout + p.stderr)
        self.assertIn('symlink refused', p.stdout)
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(outside.read_text(), 'untouched')
        target.unlink()

    def test_real_envelope_rejects_laundering(self):
        for kind in ['executable', 'original-only', 'helper-only', 'resource', 'baseline', 'partial', 'wrong-source', 'self-comparison']:
            run = json.loads(json.dumps(self.actual_run))
            if kind == 'executable': run['executable_sha256'] = '0' * 64
            if kind == 'original-only': run['kind'] = 'original-observation'
            if kind == 'helper-only': run['argv'][0] = '/tmp/serializer-helper'
            if kind == 'resource': run['profile']['resources'][0]['sha256'] = '0' * 64
            if kind == 'baseline': run['baseline_id'] = 'unreviewed-profile'
            if kind == 'partial': run['scope'] = 'All original native structures verified'
            if kind == 'wrong-source': run['implementation_commit'] = self.w.REVIEWED
            if kind == 'self-comparison': run['checks'][0]['right'] = run['checks'][0]['left']
            raw = self.w.c.encoded(run)
            path = 'docs/conformance/v1/mutant-run.json'
            blob = subprocess.check_output(['git', 'hash-object', '-w', '--stdin'], input=raw, cwd=self.root).decode().strip()
            subprocess.run(['git', 'update-index', '--add', '--cacheinfo', '100644,' + blob + ',' + path], cwd=self.root, check=True)
            tree = subprocess.check_output(['git', 'write-tree'], cwd=self.root).decode().strip()
            commit = subprocess.check_output(['git', '-c', 'user.name=WP31 isolated negative', '-c', 'user.email=negative@example.invalid',
                                              'commit-tree', tree, '-p', self.parent], input=b'actual envelope semantic negative\n', cwd=self.root).decode().strip()
            value = json.loads(json.dumps(self.registry))
            value['evidence'][0]['run'] = {'commit': commit, 'path': path, 'sha256': self.w.c.digest(raw)}
            proposal = self.root / 'proposal.json'; proposal.write_bytes(self.w.c.encoded(value))
            p = subprocess.run(['python3', str(ROOT / 'scripts/conformance/v1/conformance.py'), '--root', str(self.root),
                                'validate', '--registry', str(proposal)], cwd=ROOT, capture_output=True, text=True)
            with self.subTest(kind=kind):
                self.assertEqual(p.returncode, 1, p.stdout + p.stderr)
                self.assertEqual(proposal.read_bytes(), self.w.c.encoded(value))


if __name__ == '__main__':
    unittest.main()
