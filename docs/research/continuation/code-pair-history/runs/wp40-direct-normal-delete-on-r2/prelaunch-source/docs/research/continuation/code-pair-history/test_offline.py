"""Offline WP40 controls/replays; no new guest and no fabricated original result."""
import importlib.util
import json
import random
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[4]
CLI=ROOT/'scripts/reference/code_pair_history.py'
spec=importlib.util.spec_from_file_location('wp40',CLI);p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)


class Offline(unittest.TestCase):
    def call(self,*args):return subprocess.run([sys.executable,str(CLI),*args],capture_output=True,text=True)

    def test_check_is_offline_and_source_bound(self):
        r=self.call('check');self.assertEqual(r.returncode,0,r.stdout)
        x=json.loads(r.stdout);self.assertFalse(x['vm_launched']);self.assertFalse(x['wordling_tested'])
        self.assertEqual(x['guest_cap'],18);self.assertEqual(x['preview_previous_limit'],3)

    def test_fixed_nine_contexts_and_eighteen_guests(self):
        r=self.call('plan');self.assertEqual(r.returncode,0,r.stdout);x=json.loads(r.stdout)
        self.assertEqual(len(x['cases']),9);self.assertEqual(sum(c['repetitions']for c in x['cases']),18)
        self.assertEqual(sum(c['view']=='normal'for c in x['cases']),4)
        self.assertEqual(x['cases'][-1]['range'],[4,5]);self.assertEqual(x['cases'][-1]['outgoing_gap'],5)
        self.assertTrue(all(c['status']=='unexecuted-template'for c in x['cases']))
        self.assertTrue(all('unavailable prelaunch'in c['source_native_hash']for c in x['cases']))

    def test_run_requires_both_release_controls_before_writes(self):
        case=p.cases()[0]['id'];target=p.OUT/'runs/unauthorized-offline'
        for flags in [[],['--allow-vm'],['--authorization-note','not a root grant']]:
            self.assertFalse(target.exists());r=self.call('run','unauthorized-offline','--case',case,*flags)
            self.assertEqual(r.returncode,1);self.assertEqual(json.loads(r.stdout)['code'],'AuthorizationRequired')
            self.assertFalse(target.exists())

    def test_missing_manifest_is_public_failure(self):
        self.assertEqual(self.call('result','/tmp/no-wp40-original.json').returncode,1)

    def test_literal_fixed_frames_and_ascii(self):
        rows=p.literal_tokens(b'A'+p.BOLD_ON+b'BC'+p.BOLD_OFF+b'D')
        self.assertEqual([r['kind']for r in rows],['ASCII','BoldOn','ASCII','ASCII','BoldOff','ASCII'])
        # Literal identification alone does not require/claim semantic balancing.
        self.assertEqual(p.literal_tokens(p.BOLD_OFF)[0]['kind'],'BoldOff')

    def test_literal_malformed_and_boundary_refusals(self):
        for raw in [b'\xc3',b'\xc3\x0c',b'\xc3\x0d\xc3',b'\xc4\x0c\xc3',b'\x00',b'\xff']:
            with self.assertRaises(p.Refusal):p.literal_tokens(raw)
        with self.assertRaises(p.Refusal):p.literal_tokens(b'A'*(p.TOKENS+1))
        with self.assertRaises(p.Refusal):p.literal_tokens(b'A'*(p.LIMIT+1))

    def test_synthetic_fragment_control_does_not_assert_original_history(self):
        case=p.cases()[0]
        x=p.inferred_fragment(b'A'+p.BOLD_ON+p.BOLD_OFF+b'XBCD',case)
        self.assertEqual(x['restored_fragment_hex'],(p.BOLD_ON+p.BOLD_OFF).hex())
        self.assertFalse(x['pre_marker_export_exists']);self.assertEqual(x['post_restore_reopen_cancel_gap'],3)
        closing=p.cases()[-1]
        raw=b'A'+p.BOLD_ON+b'BC'+p.BOLD_OFF+p.BOLD_ON+p.BOLD_OFF+b'XD'
        self.assertEqual(p.inferred_fragment(raw,closing)['restored_fragment_hex'],(p.BOLD_ON+p.BOLD_OFF).hex())
        # This is a comparator control, not a prediction that closing restores this.

    def test_wrong_marker_or_insertion_relationship_refuses(self):
        for raw in [b'ABCD',b'AXXBCD',b'YXBCD']:
            with self.assertRaises(p.Refusal):p.inferred_fragment(raw,p.cases()[0])

    def valid_trace(self):
        trace=[{'capture':'view-before-sentinel'},{'key':'delete'},{'key':'f1'},{'key':'2'},{'key':'f1'},
               {'key':'right'},{'capture':'target-incoming'},{'key':'delete'},{'key':'y'},
               {'capture':'target-confirmed'},{'key':'f1'},{'key':'2'},{'key':'f1'},{'key':'f1'},{'key':'1'},
               {'capture':'after-restore-before-any-save'},{'key':'f1'},{'key':'2'},{'key':'f1'},
               {'capture':'pre-X-no-navigation'},{'type':'X'}]
        case={'id':p.cases()[0]['id'],'plan':p.cases()[0],'target_trace_start':7,'first_history_trace':10,'marker_trace':20}
        return {'trace':trace,'cases':[case]}

    def test_declared_immediate_history_trace(self):self.assertEqual(p.trace_check(self.valid_trace())['first_history_trace'],10)

    def test_hidden_save_pane_or_typed_interleaving_refuses(self):
        for entry in [{'key':'f10'},{'key':'alt-f3'},{'key':'right,f10'},{'type':'Y'}]:
            r=self.valid_trace();r['trace'][9]=entry
            with self.assertRaises(p.Refusal):p.trace_check(r)

    def test_real_approved_plain_and_reveal_gap_replays(self):
        source=ROOT/'docs/research/continuation/native-edits/runs/wp23-b-deletions-r1'
        self.assertEqual(p.literal_gap(p.PLAIN,source/'delete-0-delete-g1-confirmed',False)['gap'],1)
        closing=ROOT/'docs/research/continuation/native-edits/runs/wp23-a-blocks-r1'
        self.assertEqual(p.literal_gap(p.PAIRED,closing/'block-4-1-y-result',True)['gap'],5)

    def test_truncated_vga_and_wrong_body_cannot_infer_gap(self):
        with tempfile.TemporaryDirectory()as d:
            target=Path(d);(target/'vram.bin').write_bytes(b'\0'*3999)
            with self.assertRaises(p.Refusal):p.literal_gap(p.PLAIN,target,True)
        source=ROOT/'docs/research/continuation/native-edits/runs/wp23-b-deletions-r1/delete-0-delete-g1-confirmed'
        with self.assertRaises(p.Refusal):p.literal_gap(b'YBCD',source,False)
        with self.assertRaises(p.Refusal):p.literal_gap(p.PAIRED,source,False)

    def test_seeded_measured_literal_binary_corpus(self):
        rng=random.Random(400120)
        for _ in range(2000):
            raw=bytes(rng.randrange(256)for _ in range(rng.randrange(81)))
            try:tokens=p.literal_tokens(raw)
            except p.Refusal as error:
                self.assertIn(error.code,['OpaqueLiteralShape','TokenLimit']);continue
            self.assertEqual(b''.join(bytes.fromhex(t['hex'])for t in tokens),raw)
            self.assertTrue(all(0<=t['offset']<len(raw)for t in tokens))


if __name__=='__main__':unittest.main()
