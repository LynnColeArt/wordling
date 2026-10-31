"""WP43 public/semantic controls; synthetic mutants are not original proof."""
import copy
import importlib.util
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'scripts/reference'))
import native_genesis as g
import state_audit as a
FIXTURE=ROOT/'docs/research/continuation/native-edits/runs/wp23-b-deletions-r1/N0000.WP5'


class Offline(unittest.TestCase):
    def cli(self,*args):return subprocess.run([sys.executable,str(ROOT/'scripts/reference/native_genesis.py'),*args],capture_output=True,text=True)

    def test_public_check_and_exact_five_by_two_cap(self):
        r=self.cli('check');self.assertEqual(r.returncode,0,r.stdout);x=json.loads(r.stdout)
        self.assertIs(x['vm_launched'],False);self.assertIs(x['constructor_ready'],False)
        self.assertEqual(len(x['cases']),5);self.assertEqual(sum(c['repetitions']for c in x['cases']),10)
        self.assertTrue(all('Escape'in c['cancel_branch']or c['cancel_branch']=='No cancellation selected'or c['id']=='ascii-name-cancel'for c in x['cases']))
        self.assertEqual(x['shared_lock'],'/home/lynn/projects/wordling/research/cache/reference/session1.lock')

    def test_public_plan_does_not_create_run_or_change_owned_files(self):
        before={p.relative_to(g.OUT):g.sha(p)for p in g.OUT.rglob('*')if p.is_file()and'__pycache__'not in p.parts}
        r=self.cli('plan');self.assertEqual(r.returncode,0,r.stdout)
        after={p.relative_to(g.OUT):g.sha(p)for p in g.OUT.rglob('*')if p.is_file()and'__pycache__'not in p.parts}
        self.assertEqual(before,after);self.assertFalse((g.OUT/'runs').exists())

    def test_no_guest_authorization_before_any_output(self):
        for flags in [[],['--allow-vm'],['--authorization-note','not an oracle grant']]:
            r=self.cli('run','wp43-unauthorized','--case','empty-first-save',*flags)
            self.assertEqual(r.returncode,1);self.assertEqual(json.loads(r.stdout)['code'],'AuthorizationRequired')
            self.assertFalse((g.OUT/'runs/wp43-unauthorized').exists())

    def test_missing_result_is_public_refusal(self):self.assertEqual(self.cli('result','/tmp/no-wp43-observation.json').returncode,1)

    def test_actual_approved_native_field_inspection_not_default_admission(self):
        x=g.field_report(FIXTURE.read_bytes());self.assertGreater(len(x['fields']),50);self.assertIs(x['constructor_ready'],False)
        g.enforce_field_claims(x['fields']);self.assertTrue(all(f['constructor_encoding_permission']is False for f in x['fields']))

    def test_equal_bytes_do_not_authorize_unexplained_constant(self):
        rows=g.field_report(FIXTURE.read_bytes())['fields']
        for value in [True,0,None]:
            bad=copy.deepcopy(rows);bad[0]['constructor_encoding_permission']=value
            with self.assertRaises(g.Refusal)as e:g.enforce_field_claims(bad)
            self.assertEqual(e.exception.code,'UnsupportedDefaultInference')
        bad=copy.deepcopy(rows);bad[0]['genesis_default_classification']='constant from two equal outputs'
        with self.assertRaises(g.Refusal):g.enforce_field_claims(bad)

    def test_zero_file_is_not_no_file_or_empty_native(self):
        for raw in [b'',b'\0'*16,b'\xffWPC'+b'\0'*12]:
            with self.assertRaises(ValueError):g.field_report(raw)
        self.assertFalse(g.same({'exists':False,'size':None},{'exists':True,'size':0}))

    def test_native_bounds_truncations_and_wrong_pointer(self):
        raw=FIXTURE.read_bytes()
        for n in [0,1,4,15,16,30,65]:
            with self.assertRaises(ValueError):g.field_report(raw[:n])
        bad=bytearray(raw);bad[4:8]=(len(raw)+1).to_bytes(4,'little')
        with self.assertRaises(ValueError):g.field_report(bytes(bad))
        with self.assertRaises(g.Refusal):g.field_report(raw*(g.LIMIT//len(raw)+1))

    def test_measured_native_mutant_budget_is_bounded(self):
        rng=random.Random(43129);raw=FIXTURE.read_bytes();refused=0
        for _ in range(1000):
            b=bytearray(raw);i=rng.randrange(min(len(b),100));b[i]=rng.randrange(256)
            try:x=g.field_report(bytes(b));self.assertIs(x['constructor_ready'],False)
            except ValueError:refused+=1
        self.assertGreater(refused,100)

    def test_actual_go_reader_reopens_approved_reference_without_new_writer(self):
        rows=g.reader([FIXTURE]);self.assertEqual(len(rows),1);self.assertIs(rows[0]['accepted'],True);self.assertIs(rows[0]['exact_no_edit_export'],True)

    def test_sensitive_exact_trace_and_hidden_command_negatives(self):
        for plan in g.cases():
            expected,end=a.sensitive(plan)
            trace=[{'key':k}for k in expected]+[{'capture':end}];a.trace_interval(trace,plan)
            for extra in [{'key':'f10'},{'key':'shift-f1'},{'key':'right'},{'key':'esc'},{'type':'X'}]:
                bad=copy.deepcopy(trace);bad.insert(2,extra)
                with self.assertRaises(g.Refusal)as e:a.trace_interval(bad,plan)
                self.assertEqual(e.exception.code,'HiddenSensitiveCommand')

    def test_wrong_cancel_or_swapped_dirty_branch_refused(self):
        plan=g.cases()[-1];expected,end=a.sensitive(plan);wrong=[{'key':k}for k in expected];wrong[expected.index('f1')]={'key':'esc'};wrong.append({'capture':end})
        with self.assertRaises(g.Refusal):a.trace_interval(wrong,plan)
        other=g.cases()[3]
        with self.assertRaises(g.Refusal):a.trace_interval([{'key':k}for k in expected]+[{'capture':end}],other)

    def test_exact_filename_and_not_cropped_suffix(self):
        a.validate_name('body\nDocument to be saved: C:\\OUT\\G43RETRY\n','G43RETRY')
        for text in ['Document to be saved: G43RETRY','Document to be saved: C:\\OUT\\G43DRAFT','Document to be saved: C:\\OUT\\G43RETRYX']:
            with self.assertRaises(g.Refusal):a.validate_name(text,'G43RETRY')

    def test_rehashed_screen_text_cannot_override_raw_vga(self):
        # An archived actual original source screen is the positive raw replay.
        base=ROOT/'docs/research/continuation/native-edits/runs/wp23-b-deletions-r1/source-0'
        if not base.exists():base=next((ROOT/'docs/research/continuation/native-edits/runs/wp23-b-deletions-r1').glob('*/cursor.json')).parent
        a.captured(base.parent,base.name)
        with tempfile.TemporaryDirectory()as tmp:
            target=Path(tmp)/'capture';target.mkdir()
            for name in ['vram.bin','cursor.json','screen.txt']:(target/name).write_bytes((base/name).read_bytes())
            (target/'screen.txt').write_text('invented original state')
            with self.assertRaises(g.Refusal)as e:a.captured(Path(tmp),'capture')
            self.assertEqual(e.exception.code,'RehashedScreenChanged')

    def test_rehashed_cursor_report_cannot_override_crtc(self):
        base=next((ROOT/'docs/research/continuation/native-edits/runs/wp23-b-deletions-r1').glob('*/cursor.json')).parent
        with tempfile.TemporaryDirectory()as tmp:
            target=Path(tmp)/'capture';target.mkdir()
            for name in ['vram.bin','cursor.json','screen.txt']:(target/name).write_bytes((base/name).read_bytes())
            f=target/'cursor.json';x=json.loads(f.read_text());x['column']+=1;f.write_text(json.dumps(x))
            with self.assertRaises(g.Refusal)as e:a.captured(Path(tmp),'capture')
            self.assertEqual(e.exception.code,'CursorChanged')

    def test_dos_text_inside_document_is_not_normal_exit(self):
        self.assertEqual(g.state('C:\\WP51>\n'+'\n'*24),'dos')
        s='C:\\WP51>\n'+'\n'*23+'Doc 1 Pg 1 Ln 1" Pos 1"\n';self.assertEqual(g.state(s),'main')
        with self.assertRaises(g.Refusal):g.state('Unknown original error state')

    def test_boolean_identity_is_exact(self):
        self.assertFalse(g.same({'constructor_ready':False},{'constructor_ready':0}))
        self.assertFalse(g.same({'offset':1},{'offset':1.0}))

    def test_rehashed_wrong_initial_profile_or_default_source_refused(self):
        for mutate in ['profile','source']:
            prep=g.check();bad=copy.deepcopy(prep)
            if mutate=='profile':bad['private_sources'][0]['sha256']='0'*64
            else:bad['sources'][0]['sha256']='0'*64
            report={'scope':g.SCOPE,'wordling_tested':False,'constructor_ready':False,'complete':True,
                    'oracle_released_before_offline_audit':True,'preparation':bad,'results':[{},{}]}
            with tempfile.TemporaryDirectory()as tmp:
                base=Path(tmp);(base/'prelaunch.json').write_text(json.dumps(bad));f=base/'run.json';f.write_text(json.dumps(report))
                with self.assertRaises(g.Refusal)as e:g.result(f)
                self.assertEqual(e.exception.code,'SourceChanged')

    def test_rehashed_hidden_wire_command_refused(self):
        trace=[{'key':'f10'},{'type':'C:\\OUT\\G43TEXT'},{'key':'ret'}]
        expected=a.keys(trace)
        with tempfile.TemporaryDirectory()as tmp:
            base=Path(tmp);path=base/'qmp-wire.jsonl'
            def record(keys):
                path.write_text(''.join(json.dumps({'direction':'tx-buffer','raw_hex':json.dumps({'execute':'human-monitor-command','arguments':{'command-line':'sendkey '+k+' 80'}}).encode().hex()})+'\n'for k in keys))
            record(expected);self.assertEqual(a.wire_match(base,trace),len(expected))
            record(expected[:1]+['esc']+expected[1:])
            with self.assertRaises(g.Refusal)as e:a.wire_match(base,trace)
            self.assertEqual(e.exception.code,'WireCommandChanged')

    def test_directory_absence_uses_exact_name_not_size_or_substring(self):
        names=g.bare_names('::/OUT/G43TEXT\n::/OUT/G43DRAFT2\n')
        self.assertIn('G43TEXT',names);self.assertNotIn('G43DRAFT',names)


if __name__=='__main__':unittest.main()
