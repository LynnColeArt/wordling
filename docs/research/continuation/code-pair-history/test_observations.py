"""Post-run semantic controls on copies; these mutants are never original observations."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

import audit as a
import print_literal as p

BASE=a.OUT/'runs/wp40-direct-normal-delete-on-r1'


class Observations(unittest.TestCase):
    def test_actual_full_git_native_menu_cursor_print_audit(self):
        x=a.audit();self.assertEqual(x['complete_original_guests'],18)
        self.assertEqual(x['raw_Git_files_verified'],9252);self.assertEqual(x['actual_reader_artifact_paths'],90)
        self.assertIs(x['entry_counts_or_global_history_rules_qualified'],False)

    def test_exact_closing_stream_and_empty_second_span(self):
        base=a.OUT/'runs/wp40-closing-block-repair-yes-r1';r=json.loads((base/'run.json').read_text());c=r['cases'][0]
        body=bytes.fromhex(a.native.inspect(a.native.bounded_native(base/c['interop']['after_print']),False)['body_hex'])
        stream=(base/c['interop']['print_stream']).read_bytes();x=p.audit(c['id'],body,stream)
        self.assertEqual(len(stream),164);self.assertEqual(x['known_literal_spans'],[{'start':1,'literal_hex':'4243'},{'start':3,'literal_hex':'','empty_second_pair':True}])
        self.assertEqual(x['sha256'],'3f6fad473328caaccfca623e270af5d0fc8c94be521403ee8f122879c6a69349')
        old=a.driver.result(base/'run.json')['print'];self.assertIs(old['qualified'],False)
        self.assertEqual(old['opaque_print_interpretation'],'Original bold overstrike differs from exact native selected span')

    def test_print_control_ink_overstrike_mutations_refused(self):
        stream=p.PREFIX+b' '*10+b'ABCXDZ'+b'\r'+b' '*11+b'BC'+p.SUFFIX
        for bad in [stream[1:],stream+b'\n',stream.replace(b'BC',b'BD'),stream.replace(b' '*11+b'BC'+p.SUFFIX,b' '*13+b'BC'+p.SUFFIX),stream.replace(b'\r\n',b'\n',1),stream.replace(b'\r'+b' '*11+b'BC',b'\r'+b' '*11+b'CB')]:
            with self.subTest(sha=hashlib.sha256(bad).hexdigest()),self.assertRaises(p.PrintRefusal):p.audit('closing-block-repair-yes',p.CLOSING,bad)

    def test_print_does_not_admit_generic_native_or_balancing(self):
        stream=p.PREFIX+b' '*10+b'ABCXDZ'+b'\r'+b' '*11+b'BC'+p.SUFFIX
        for bad in [p.CLOSING[:-1],p.CLOSING.replace(p.ON+p.OFF,p.OFF+p.ON),b'A'+p.ON+b'BCXDZ'+p.OFF,b'ABCXDZ']:
            with self.assertRaises(p.PrintRefusal):p.audit('closing-block-repair-yes',bad,stream)
        with self.assertRaises(p.PrintRefusal):p.audit('other',p.CLOSING,stream)

    def test_bool_and_numeric_facts_are_not_coerced(self):
        self.assertFalse(a.same_facts({'accepted':False},{'accepted':0}))
        self.assertFalse(a.same_facts({'gap':1},{'gap':1.0}))

    def test_rehashed_report_menu_row_does_not_override_screen(self):
        r=json.loads((BASE/'run.json').read_text());c=copy.deepcopy(r['cases'][0]);c['history'][0]['overlaid_first_lines'][0]='T'
        with self.assertRaises(a.driver.Refusal)as e:a.menu_records(BASE,c,r['trace'])
        self.assertEqual(e.exception.code,'MenuSemanticChanged')

    def test_previous_cannot_be_relabelled_restore(self):
        r=json.loads((BASE/'run.json').read_text());trace=copy.deepcopy(r['trace']);start,end=r['cases'][0]['history'][0]['trace_range']
        next(e for e in trace[start:end]if e.get('key')=='2')['key']='1'
        with self.assertRaises(a.driver.Refusal)as e:a.menu_records(BASE,r['cases'][0],trace)
        self.assertEqual(e.exception.code,'HistoryInterleaving')

    def replay(self,change,expected):
        with tempfile.TemporaryDirectory(prefix='wp40-semantic-')as tmp:
            base=Path(tmp)/BASE.name;shutil.copytree(BASE,base)
            r=json.loads((base/'run.json').read_text());change(base,r)
            # Rehash the whole local envelope: a refusal must be semantic, not a stale local hash.
            for item in r['artifacts']:
                f=base/item['path'];item['size']=f.stat().st_size;item['sha256']=a.sha(f)
            for item in r['stopped_exports']:
                f=base/item['host'];item['size']=f.stat().st_size;item['sha256']=a.sha(f)
            (base/'run.json').write_text(json.dumps(r))
            with self.assertRaises(a.driver.Refusal)as e:a.driver.result(base/'run.json')
            self.assertEqual(e.exception.code,expected)

    def test_rehashed_source_native_substitution_refused(self):
        def change(base,r):
            f=base/r['cases'][0]['source'];raw=f.read_bytes();source=a.driver.SOURCE;self.assertEqual(raw.count(source),1);f.write_bytes(raw.replace(source,b'T'+source[1:]))
        self.replay(change,'SourceNativeChanged')

    def test_rehashed_wrong_view_refused(self):
        self.replay(lambda b,r:r['cases'][0]['plan'].__setitem__('view','reveal'),'CaseChanged')

    def test_rehashed_wrong_boundary_confirmation_refused(self):
        self.replay(lambda b,r:r['cases'][0].__setitem__('question',r['cases'][0]['question'].replace('[BOLD]','[bold]')),'ConfirmationChanged')

    def test_rehashed_fake_dos_refused(self):
        self.replay(lambda b,r:(b/'clean-exit/screen.txt').write_text('WordPerfect document still open'),'FakeExit')

    def test_rehashed_source_envelope_cannot_change_executing_identity(self):
        def change(base,r):
            f=base/'prelaunch.json';x=json.loads(f.read_text());x['preparation']['sources'][0]['sha256']='0'*64;f.write_text(json.dumps(x))
        self.replay(change,'SourceChanged')

    def test_consistent_native_marker_substitution_still_disagrees_with_restore_cursor(self):
        # Even a self-consistent hypothetical final-native chain cannot replace the captured ASBCD state.
        with self.assertRaises(a.driver.Refusal)as e:a.driver.literal_gap(b'ATBCD',BASE/'after-restore-before-any-save',False)
        self.assertEqual(e.exception.code,'CursorMismatch')

    def test_git_inventory_cannot_omit_duplicate_or_add_raw_witness(self):
        rows=json.loads((a.OUT/'observations.json').read_text())['raw_files']
        for bad in [rows[:-1],rows+[rows[0]],rows+[{'path':'runs/invented'}]]:
            with self.assertRaises(a.driver.Refusal)as e:a.inventory(bad)
            self.assertEqual(e.exception.code,'GitInventoryChanged')

    def test_git_seal_rejects_changed_raw_bytes(self):
        ledger=json.loads((a.OUT/'observations.json').read_text());item=next(x for x in ledger['raw_files']if x['path'].endswith('clean-exit/screen.txt'))
        with tempfile.TemporaryDirectory()as tmp:
            root=Path(tmp);f=root/item['path'];f.parent.mkdir(parents=True);f.write_bytes(b'changed raw witness')
            with self.assertRaises(a.driver.Refusal)as e:a.git_files(root,[item])
            self.assertEqual(e.exception.code,'GitCustodyChanged')


if __name__=='__main__':unittest.main()
