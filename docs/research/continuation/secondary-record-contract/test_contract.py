"""Public checker regressions; all synthetic bytes are OFFLINE, never candidates."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[4]
SPEC = importlib.util.spec_from_file_location('secondary_record_contract', ROOT / 'scripts/reference/secondary_record_contract.py')
C = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(C)


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = C.Session(ROOT)
        cls.pro = cls.session.provenance
        cls.proof = json.loads((cls.pro / 'recon/source-proof.json.txt').read_text())
        cls.case = next(x for x in cls.proof['cases'] if x['case'] == 'CMD51-207')
        cls.raw = cls.source('Secondary')
        cls.info = cls.session.inspect(cls.raw, 'Secondary')
        cls.known = cls.session.authority['known_secondary_D4_00']
        cls.negatives = []

    @classmethod
    def source(cls, role, case=None):
        row = next(x for x in (case or cls.case)['sources'] if x['role'] == role)
        return (cls.pro / 'git' / C.READER / (row['path'] + '.txt')).read_bytes()

    @classmethod
    def tearDownClass(cls):
        if os.environ.get('WP53_TEST_RECEIPT'):
            Path(os.environ['WP53_TEST_RECEIPT']).write_text(json.dumps({
                'synthetic_offline_only': True, 'negatives': cls.negatives,
                'helper_receipt': cls.session.receipt}, indent=2) + '\n')
        cls.session.close()

    def shape(self, raw):
        # Fresh integrity hashes are valid for every generated counterexample.
        manifest = {'size': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
        self.assertEqual(C.digest(raw), manifest['sha256'])
        info = self.session.inspect(raw, 'Secondary', synthetic=True)
        return C.secondary_shape(info, self.known)

    def refused_shape(self, raw):
        # A successful reader inspection ensures the semantic refusal is NOT
        # merely bad hashes, framing corruption or an unavailable helper.
        info = self.session.inspect(raw, 'Secondary', synthetic=True)
        with self.assertRaises(C.Refusal) as caught:
            C.secondary_shape(info, self.known)
        self.negatives.append({'sha256': C.digest(raw), 'bytes': len(raw),
            'raw_hex': raw.hex() if len(raw) < 4096 else None,
            'native_reader_framing_succeeded': True, 'semantic_refusal': str(caught.exception)})
        return info

    def test_original_pairs(self):
        with C.Session(ROOT) as other:
            result = C.audit(other)
        self.assertEqual((result['case_count'], result['original_runs'], result['native_inputs']), (5, 10, 30))
        self.assertFalse(result['production_secondary_admission_changed'])
        self.assertFalse(result['interpreter_executed'])
        self.assertEqual(len({p['run'] for c in result['cases'] for p in c['paired']}), 4)

    def test_nonfixture_value_uses_real_spans(self):
        raw = self.raw[:324] + b'Clara' + self.raw[329:]
        records = self.shape(raw)
        self.assertEqual(records[0]['explicit_values_hex'], [b'Clara'.hex()])
        self.assertEqual(C.explicit_reference(records, 1), [b'Clara'.hex(), b'Bob'.hex()])
        self.assertNotEqual(C.digest(raw), C.digest(self.raw))

    def test_count_decrement_and_contradiction(self):
        for value in (0, 1, 3, 65535):
            with self.subTest(value=value):
                raw = bytearray(self.raw);raw[342:344] = value.to_bytes(2, 'little')
                self.refused_shape(bytes(raw))

    def test_unproved_three_explicit_fields_count4_is_not_count_minus_one(self):
        case = next(x for x in self.proof['cases'] if x['case'] == 'CMD51-209')
        raw = self.source('Secondary', case)
        info = self.session.inspect(raw, 'Secondary', synthetic=True)
        at = info['records'][0]['end_record']['Offset']
        raw = raw[:at] + b'Z' + bytes.fromhex('de310400040031de') + b'\n' + raw[at:]
        raw = bytearray(raw);raw[at + 10 + 4:at + 10 + 6] = b'\x04\x00'
        self.refused_shape(bytes(raw))

    def test_genuine_empty_missing_and_space_distinct(self):
        case = next(x for x in self.proof['cases'] if x['case'] == 'CMD51-209')
        raw = self.source('Secondary', case)
        info = self.session.inspect(raw, 'Secondary', synthetic=True)
        records = C.secondary_shape(info, self.known)
        self.assertEqual(C.explicit_reference(records, 2)[1], '')
        f = info['records'][1]['fields'][1]
        at = f['end_field']['Offset'];end = at + f['end_field']['Length']
        self.refused_shape(raw[:at] + raw[end:])
        self.refused_shape(raw[:at] + b' ' + raw[at:])
        # Missing field2 is not a zero-length explicit value.
        records = C.secondary_shape(self.info, self.known)
        with self.assertRaisesRegex(C.Refusal, 'OutsideExplicitFields'):
            C.explicit_reference(records, 2)

    def test_extra_HR_and_space_and_embedded_controls(self):
        for at, value in [(338, b'\n'), (338, b' '), (326, b'\n'), (326, b'\x0c')]:
            with self.subTest(at=at, value=value):
                self.refused_shape(self.raw[:at] + value + self.raw[at:])

    def test_nonempty_unaddressed_tail(self):
        self.refused_shape(self.raw[:338] + b'TAIL' + self.raw[338:])

    def test_remove_EF_EOR_and_swap_extent(self):
        for start, end in [(329, 337), (338, 348)]:
            with self.subTest(start=start):
                self.refused_shape(self.raw[:start] + self.raw[end:])
        info = copy.deepcopy(self.info)
        info['records'][0]['tail']['Offset'] += 1
        with self.assertRaises(C.Refusal):
            C.secondary_shape(info, self.known)

    def test_D4_absent_misplaced_unknown_function_group_payload(self):
        variants = [self.raw[:348] + self.raw[380:],
                    self.raw[:348] + self.raw[380:381] + self.raw[348:380] + self.raw[381:]]
        unknown = bytearray(self.raw);unknown[349] ^= 1;unknown[378] ^= 1;variants.append(bytes(unknown))
        for offset in [352, 354, 360]:
            raw = bytearray(self.raw);raw[offset] ^= 1;variants.append(bytes(raw))
        for raw in variants:
            with self.subTest(hash=C.digest(raw)):
                self.refused_shape(raw)

    def test_hardpage_is_not_formatter_or_extra_control(self):
        for value in [b'', b'\n', b'\x0c\x0c']:
            self.refused_shape(self.raw[:380] + value + self.raw[381:])

    def test_truncated_and_frame_corruption(self):
        for raw in [b'', b'not native', self.raw[:350], self.raw[:-1] + b'\xde', self.raw[:349] + b'\x01' + self.raw[350:]]:
            with self.subTest(size=len(raw)), self.assertRaises(C.Refusal):
                self.session.inspect(raw, 'Secondary', synthetic=True)

    def test_primary_reference_and_unbalanced_context(self):
        records = C.secondary_shape(self.info, self.known)
        primary = self.source('Primary')
        info = self.session.inspect(primary, 'Primary', synthetic=True)
        self.assertEqual(C.primary_contract(info, records)[0]['number'], 1)
        at = info['commands'][0]['operand']['Offset']
        raw = primary[:at] + b'2' + primary[at + 1:]
        bad = self.session.inspect(raw, 'Primary', synthetic=True)
        with self.assertRaises(C.Refusal):C.primary_contract(bad, records)
        case = next(x for x in self.proof['cases'] if x['case'] == 'CMD51-209')
        primary = self.source('Primary', case)
        info = self.session.inspect(primary, 'Primary', synthetic=True)
        endif = info['commands'][2]['function']
        raw = primary[:endif['Offset']] + primary[endif['Offset'] + endif['Length']:]
        bad = self.session.inspect(raw, 'Primary', synthetic=True)
        with self.assertRaises(C.Refusal):C.primary_contract(bad, records)

    def test_result_projection_retains_metadata_and_controls(self):
        info = self.session.inspect(self.source('Result'), 'Result', synthetic=True)
        p = C.result_projection(info)
        self.assertEqual(bytes.fromhex(p['selected_hex']), b'Hello Alice\n\fHello Bob\n')
        self.assertTrue(p['retained_D4_metadata'])
        raw = bytearray(self.source('Result'));raw[info['body_offset']] = 0x80
        opaque = self.session.inspect(bytes(raw), 'Result', synthetic=True)
        with self.assertRaisesRegex(C.Refusal, 'ResultFinding'):C.result_projection(opaque)
        info = copy.deepcopy(info);info['tokens'][0]['code'] = 0xc3;info['tokens'][0]['kind'] = 3
        with self.assertRaises(C.Refusal):C.result_projection(info)

    def test_rehashed_case_role_result_source_swaps(self):
        triplet = copy.deepcopy(self.case['sources'][:3])
        for change in ['case', 'run', 'result', 'role']:
            bad = copy.deepcopy(triplet)
            if change == 'case':bad[0]['path'] = bad[0]['path'].replace('207', '208')
            if change == 'run':bad[0]['run'] = 'foreign-run'
            if change == 'result':bad[2]['path'] = bad[0]['path']
            if change == 'role':bad[2]['role'] = 'Secondary'
            # Rehashing a supplied local manifest cannot authorize a foreign case.
            json.dumps({'sha256': C.digest(json.dumps(bad).encode()), 'sources': bad})
            with self.subTest(change=change), self.assertRaises(C.Refusal):
                C.paired_sources('CMD51-207', bad)

    def test_original_context_does_not_equate_PAGE_OFF_with_ON(self):
        records = C.secondary_shape(self.info, self.known)
        primary = self.session.inspect(self.source('Primary'), 'Primary', synthetic=True)
        C.original_context('CMD51-207', primary, records)
        bad = copy.deepcopy(primary);bad['commands'][0]['kind'] = 0x4d
        with self.assertRaises(C.Refusal):C.original_context('CMD51-207', bad, records)

    def test_copied_field_unknown_span_and_out_of_range_refuse(self):
        for change in ['zero', 'negative', 'length', 'offset']:
            bad = copy.deepcopy(self.info);p = bad['records'][0]['fields'][0]['content']
            if change == 'zero':p.clear()
            if change == 'negative':p['Offset'] = -1
            if change == 'length':p['Length'] += 1
            if change == 'offset':p['Offset'] += 1
            with self.subTest(change=change), self.assertRaises(C.Refusal):C.secondary_shape(bad, self.known)
        bad = copy.deepcopy(self.info);bad['findings_capped'] = True
        with self.assertRaisesRegex(C.Refusal, 'FindingsCapped'):C.secondary_shape(bad, self.known)

    def test_reader_ownership_and_race_go(self):
        out = self.session.run(['go', 'test', '-race', '-count=1', './internal/secondary-contract'])
        self.assertIn(b'ok', out)

    def test_near_token_limit_resource_shape(self):
        raw = self.raw[:324] + b'R' * 65000 + self.raw[329:]
        records = self.shape(raw)
        self.assertEqual(len(bytes.fromhex(records[0]['explicit_values_hex'][0])), 65000)
        limits = self.session.authority
        self.assertEqual(len(limits['known_secondary_D4_00']), 8)
        with self.assertRaisesRegex(C.Refusal, 'InputLimit'):
            self.session.inspect(b'A' * (C.MAX_INPUT + 1), 'Secondary', synthetic=True)

    def test_input_and_aggregate_limits_before_helper(self):
        count, total = self.session.inputs, self.session.total
        self.session.inputs = C.MAX_INPUTS
        try:
            with self.assertRaisesRegex(C.Refusal, 'AggregateLimit'):self.session.inspect(self.raw, 'Secondary')
        finally:self.session.inputs, self.session.total = count, total
        with self.assertRaisesRegex(C.Refusal, 'InvalidRole'):self.session.inspect(self.raw, 'Document')

    def test_bounded_subprocess_timeout_cap_failure_and_no_orphan(self):
        with tempfile.TemporaryDirectory() as d:
            pid = Path(d) / 'pid'
            code = f'import os,time;open({str(pid)!r},"w").write(str(os.getpid()));time.sleep(10)'
            with self.assertRaisesRegex(C.Refusal, 'HelperTimeout'):
                C.bounded([sys.executable, '-c', code], Path(d), timeout=.2)
            child = int(pid.read_text())
            with self.assertRaises(ProcessLookupError):__import__('os').kill(child, 0)
            with self.assertRaisesRegex(C.Refusal, 'HelperOutputLimit'):
                C.bounded([sys.executable, '-c', 'print("X"*10000)'], Path(d), cap=100)
            with self.assertRaisesRegex(C.Refusal, 'SubprocessFailure'):
                C.command([sys.executable, '-c', 'raise SystemExit(7)'], Path(d))
            with self.assertRaisesRegex(C.Refusal, 'InvalidJSON'):C.load_json(b'{"partial":')

    def test_rehashed_authority_substitution_and_symlinks(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);p = root / C.OWNED;p.mkdir(parents=True)
            raw = (ROOT / C.OWNED / 'authority.json').read_bytes().replace(C.READER.encode(), b'0' * 40)
            (p / 'authority.json').write_bytes(raw)
            with self.assertRaisesRegex(C.Refusal, 'AuthorityBinding'):C.authority(root)
            link = root / 'link';link.symlink_to(ROOT / C.OWNED / 'authority.json')
            with self.assertRaisesRegex(C.Refusal, 'SymlinkInput'):C.limited_read(link, C.MAX_INPUT)
            with self.assertRaisesRegex(C.Refusal, 'UnsafePath'):C.relative(root, '../secret')

    def test_immutable_source_binding_and_partial_helper_fail_atomically(self):
        original = C.limited_read
        native = ROOT / 'internal/merge/native/image.go'
        def read(path, cap):
            raw = original(path, cap)
            return raw + b'// changed' if path == native else raw
        with mock.patch.object(C, 'limited_read', side_effect=read):
            with self.assertRaisesRegex(C.Refusal, 'InheritedGoModuleBytes'):C.authority(ROOT)
        for output in [b'{"partial":', b'{}', json.dumps({'sha256':'foreign'}).encode()]:
            with mock.patch.object(self.session, 'run', return_value=output):
                with self.assertRaises(C.Refusal):self.session.inspect(self.raw, 'Secondary', synthetic=True)

    def test_atomic_reports_and_path_refusals(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'report.json';p.write_bytes(b'prior-report')
            with self.assertRaises(C.Refusal):C.atomic_report(p, b'new-report', check=True)
            self.assertEqual(p.read_bytes(), b'prior-report')
            C.atomic_report(p, b'new-report');C.atomic_report(p, b'new-report', check=True)
            with self.assertRaises(C.Refusal):C.output_path(ROOT / 'docs/research/command-scenarios.json')
            with self.assertRaises(C.Refusal):C.output_path(Path(d) / 'SECOND.WP5')
            with self.assertRaisesRegex(C.Refusal, 'ReportTraversal'):C.output_path(ROOT / C.OWNED / 'evidence/../../other.json')

    def test_public_cli_semantic_refusal_preserves_prior_output(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d);raw = bytearray(self.raw);raw[342:344] = b'\x01\x00'
            (p / 'negative.wp5').write_bytes(raw);out = p / 'report.json';out.write_bytes(b'prior-report')
            run = subprocess.run([sys.executable, str(ROOT / 'scripts/reference/secondary_record_contract.py'),
                    'inspect', '--input', str(p / 'negative.wp5'), '--role', 'Secondary', '--output', str(out)],
                    capture_output=True, timeout=120)
            self.assertEqual(run.returncode, 1);self.assertIn(b'REFUSED', run.stderr)
            self.assertEqual(out.read_bytes(), b'prior-report')
            run = subprocess.run([sys.executable, str(ROOT / 'scripts/reference/secondary_record_contract.py'),
                    'inspect', '--role', 'Unknown'], capture_output=True, timeout=5)
            self.assertEqual(run.returncode, 2)


if __name__ == '__main__':unittest.main(verbosity=2)
