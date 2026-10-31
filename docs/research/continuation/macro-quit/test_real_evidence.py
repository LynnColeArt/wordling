"""Read-only originals; semantic mutations use temporary replay copies only."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'docs/research/continuation/macro-quit'
CLI=ROOT/'scripts/reference/macro_quit.py'
AUDIT=OUT/'audit.py'


class RealEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory(prefix='wp39-semantic-replay-')
        cls.replay=Path(cls.temp.name)
        shutil.copytree(OUT/'runs',cls.replay/'runs')

    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()

    def replay_mutant(self,name,run_id,mutate,expected,audit=False,expected_result_pass=False):
        base=self.replay/'runs'/run_id
        shutil.rmtree(base);shutil.copytree(OUT/'runs'/run_id,base)
        report=json.loads((base/'run.json').read_text());mutate(base,report)
        # Adversarial inputs recompute ALL their local artifact/export hashes.
        # Rejection therefore needs source/semantic/state/Git binding, not a stale checksum.
        for row in report['results']:
            for item in row['stopped_exports']:
                p=base/item['path']
                item.update(size=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
        report['artifacts']=[{'path':str(p.relative_to(base)),'size':p.stat().st_size,
                             'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
                            for p in sorted(base.rglob('*'))if p.is_file()and p.name not in ['run.json','results.xml']]
        (base/'run.json').write_text(json.dumps(report,indent=2)+'\n')
        if expected_result_pass:
            p=subprocess.run([sys.executable,str(CLI),'result',str(base/'run.json')],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stdout+p.stderr)
            self.assertTrue(all(r['branch']=='child-return-observed-not-stop-all'for r in json.loads(p.stdout)['observations']))
        argv=[sys.executable,str(AUDIT),'--evidence-root',str(self.replay)]if audit else[sys.executable,str(CLI),'result',str(base/'run.json')]
        p=subprocess.run(argv,capture_output=True,text=True)
        self.assertEqual(p.returncode,1,p.stdout+p.stderr)
        result=json.loads(p.stdout);self.assertEqual(result['code'],expected,p.stdout)
        print(json.dumps({'mutant':name,'all_envelope_hashes_recomputed':True,'expected_rejection':expected,
                          'actual_rejection':result['code'],'exit':p.returncode,'originals_modified':False}),flush=True)

    def test_actual_original_pairs_and_git_custody_pass_public_audit(self):
        p=subprocess.run([sys.executable,str(AUDIT)],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        x=json.loads(p.stdout);self.assertEqual(x['complete_original_observations'],4)
        self.assertEqual(x['incomplete_diagnostic_observations'],2)
        self.assertEqual(x['verified_raw_Git_files'],740)

    def test_rehashed_screen_sentinel_cannot_change_actual_observation(self):
        def change(base,r):
            p=base/'root-1/macro-completed-before-manual/screen.txt'
            p.write_text(p.read_text().replace('R39','R38'))
        self.replay_mutant('screen-sentinel','wp39-root-02',change,'ManualContinuation')

    def test_rehashed_native_output_cannot_change_actual_observation(self):
        def change(base,r):
            p=base/'root-1/QBEFORE.WP5';raw=p.read_bytes();self.assertIn(b'R39',raw)
            p.write_bytes(raw.replace(b'R39',b'R38'))
        self.replay_mutant('native-body','wp39-root-02',change,'NativeSemanticChanged')

    def test_rehashed_source_and_updated_source_envelope_still_rejected(self):
        def change(base,r):
            path='scripts/reference/macro_quit.py';p=base/'runner-source'/path;p.write_bytes(p.read_bytes()+b'\n# changed source identity\n')
            pin=next(x for x in r['preparation']['sources']if x['path']==path)
            raw=p.read_bytes();pin.update(size=len(raw),sha256=hashlib.sha256(raw).hexdigest(),git_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest())
            (base/'prelaunch.json').write_text(json.dumps(r['preparation'],indent=2)+'\n')
        self.replay_mutant('source-rehashed-and-envelope-updated','wp39-root-02',change,'SourceChanged')

    def test_rehashed_case_substitution_rejected(self):
        self.replay_mutant('case-substitution','wp39-root-02',lambda b,r:r.update(case='nested'),'CaseChanged')

    def test_rehashed_native_instruction_change_rejected(self):
        def change(base,r):
            p=base/'input/Q39R.WPM';raw=bytearray(p.read_bytes());self.assertEqual(raw[90:92],b'\x20\xfc');raw[90]=0x22;p.write_bytes(raw)
        self.replay_mutant('native-QUIT-to-RETURN','wp39-root-02',change,'InputChanged')

    def test_rehashed_dos_text_in_document_is_not_completion(self):
        def change(base,r):(base/'root-1/clean-exit/screen.txt').write_text('C:\\WP51>\nDoc 1\n')
        # A trailing blank can make this unknown rather than main; both reject DOS.
        self.replay_mutant('DOS-looking-document','wp39-root-02',change,'CompletionState')

    def test_rehashed_exit_response_cannot_send_no_to_exit_question(self):
        def change(base,r):r['results'][0]['exit_actions'][2]['key']='n'
        self.replay_mutant('No-at-Exit-doc1','wp39-root-02',change,'CompletionState')

    def test_rehashed_host_containment_cannot_become_original_completion(self):
        def change(base,r):r['results'][0]['outcome']='host-contained'
        self.replay_mutant('host-containment','wp39-root-02',change,'IncompleteObservation')

    def test_rehashed_operator_f1_trace_cannot_become_normal_quit(self):
        def change(base,r):
            cmd={'execute':'human-monitor-command','arguments':{'command-line':'sendkey f1 80'}}
            raw=(json.dumps(cmd)+'\n').encode()
            with(base/'root-1/qmp-wire.jsonl').open('a')as f:f.write(json.dumps({'direction':'tx-buffer','raw_hex':raw.hex()})+'\n')
        self.replay_mutant('operator-F1','wp39-root-02',change,'OperatorStop')

    def test_consistently_rehashed_child_return_cannot_rewrite_original_stop_all_ledger(self):
        def change(base,r):
            before='D1SENT DIRTY1P39C39';after=before+'READY'
            new_before=before+'PARENTBACK';new_after=new_before+'READY'
            for row in r['results']:
                case=base/row['id']
                for p in case.glob('*/screen.txt'):
                    text=p.read_text();lines=text.splitlines(keepends=True)
                    if lines and lines[0].rstrip('\n')in [before,after]:
                        old=lines[0].rstrip('\n');lines[0]=(new_before if old==before else new_after)+'\n';p.write_text(''.join(lines))
                for name,old,new in [('QBEFORE',before,new_before),('QAFTER',after,new_after)]:
                    p=case/(name+'.WP5');raw=p.read_bytes();self.assertIn(old.encode(),raw);p.write_bytes(raw.replace(old.encode(),new.encode()))
                row['observed'].update(before_manual=new_before,after_manual=new_after,branch='child-return-observed-not-stop-all')
        self.replay_mutant('consistent-alternative-child-return','wp39-nested-02',change,
                           'LedgerSemanticChanged',audit=True,expected_result_pass=True)


if __name__=='__main__':unittest.main()
