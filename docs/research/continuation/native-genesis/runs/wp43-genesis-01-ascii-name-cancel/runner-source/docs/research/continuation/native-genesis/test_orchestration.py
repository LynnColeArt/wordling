"""Fault actual run/attempt orchestration with a simulated helper boundary, NEVER VM evidence."""
from contextlib import contextmanager, ExitStack
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'scripts/reference'))
import native_genesis as g


class Orchestration(unittest.TestCase):
    def run_fault(self,fault=None,case='empty-first-save'):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);root=Path(tmp.name)
        out=root/'owned';out.mkdir();private=root/'private';private.mkdir();master=private/'master';master.mkdir()
        for n in ['boot.img','harddisk.img']:(master/n).write_bytes(b'IMMUTABLE MASTER '+n.encode())
        q=SimpleNamespace(RUNTIME=private/'runtime',SOCKET=private/'runtime/qmp.sock');q.RUNTIME.mkdir()
        state={'guard':False,'start_count':0,'stop_count':0,'mcopy_count':0,'mdir_count':0,'extract_in_guard':[],'master_in_guard':[]}
        @contextmanager
        def guard(unused):
            self.assertFalse(state['guard']);state['guard']=True
            try:yield
            finally:state['guard']=False
        class QMP:
            def __enter__(self):return self
            def __exit__(self,*unused):return None
            def capture(self,p):p.mkdir(parents=True);(p/'screen.txt').write_text('SYNTHETIC failure control, not original')
        q.QMP=QMP
        guest=SimpleNamespace(MASTER=master,arguments=lambda boot,disk:['synthetic-qemu','-drive',str(boot),'-drive',str(disk)])
        def start(qmp,guest,work,assets):
            self.assertTrue(state['guard']);state['start_count']+=1
            work.mkdir(parents=True);(work/'boot.img').write_bytes(b'copy');(work/'harddisk.img').write_bytes(b'copy')
            (work/'settings-before.SET').write_bytes(b'SYNTHETIC private setup');(work/'OUT-before.txt').write_bytes(b'original preboot listing control')
            if fault=='prelaunch':raise OSError('injected before argv/launch boundary')
            argv=guest.arguments(work/'boot.img',work/'harddisk.img')
            qmp.SOCKET.touch();(qmp.RUNTIME/'qemu.pid').write_text('99999999')
            return argv
        def capture(qmp,work):
            if fault=='missing-pid':raise FileNotFoundError('injected missing PID file')
            if fault=='unowned-pid':raise g.Refusal('UnprovenPID','wrong socket/private disks in process')
            raw=b'\0'.join([b'SYNTHETIC boundary',('unix:'+str(qmp.SOCKET)+',server=on').encode(),('file='+str(work/'boot.img')+',format=raw').encode(),('file='+str(work/'harddisk.img')+',format=raw').encode()])
            return {'pid':99999999,'start_ticks':'123','cmdline_hex':raw.hex(),
                    'socket':str(qmp.SOCKET),'private_work':str(work),'ownership_validated':True}
        def stop(qmp,guest):
            self.assertTrue(state['guard']);state['stop_count']+=1
            if fault=='stop-error':raise OSError('injected stop failure')
            qmp.SOCKET.unlink();return 'SYNTHETIC stop helper control'
        class Probe:
            def __init__(self,unused,directory):self.exports=[];self.trace=[];self.settings=[];self.checks=[]
        def act(plan,p):
            p.exports=list(g.expected_exports(plan).items())
            if fault=='missing-declaration':p.exports=[]
            return {'first':{'host':plan['first_save_name']+'.WP5'}if plan['first_save_name']else None,'expected_absent':['G43DRAFT']}
        def process(argv,**kwargs):
            if argv[0]=='mdir':
                state['mdir_count']+=1
                after=state['mdir_count']%2==0
                data=(b'::/OUT/G43EMPTY\n'if after and case!='empty-f10-cancel'else b'')
                if fault=='unexpected-absence'and after:data+=b'::/OUT/G43DRAFT\n'
                return subprocess.CompletedProcess(argv,0,data,b'')
            self.assertEqual(argv[0],'mcopy');self.assertTrue(state['guard']);self.assertFalse(q.SOCKET.exists())
            state['extract_in_guard'].append(state['guard']);state['mcopy_count']+=1
            if fault=='copy-exception':raise OSError('injected mcopy exception')
            if fault=='copy-nonzero':return subprocess.CompletedProcess(argv,17,b'',b'injected mcopy failure')
            if fault!='missing-output':Path(argv[-1]).write_bytes(b''if fault=='zero-output'else b'SYNTHETIC copied bytes; not a native fixture')
            if fault=='master-mismatch':(master/'boot.img').write_bytes(b'CHANGED MASTER')
            return subprocess.CompletedProcess(argv,0,b'',b'')
        def resources(work):
            if fault=='post-copy-tamper'and state['mcopy_count']:
                f=out/'runs/wp43-orchestration/r1/G43EMPTY.WP5'
                if f.exists():f.write_bytes(b'changed-after-recorded-extraction-hash')
            return [{'name':'SYNTHETIC resources, not original proof'}]
        actual_master_identity=g.master_identity
        def master_identity(guest):
            self.assertTrue(state['guard']);state['master_in_guard'].append(True)
            return actual_master_identity(guest)
        args=SimpleNamespace(allow_vm=True,authorization_note='UNIT SIMULATION ONLY; no VM grant',case=case,run_id='wp43-orchestration')
        with ExitStack()as stack:
            for target,value in [('OUT',out),('check',lambda:{'sources':[],'scope':'SYNTHETIC fault control'}),('resource_metadata',resources),('capture_owned_pid',capture),('act',act),('master_identity',master_identity)]:stack.enter_context(patch.object(g,target,value))
            stack.enter_context(patch.object(g.session,'configure',return_value=(q,guest,private)))
            stack.enter_context(patch.object(g.session,'exclusive',guard));stack.enter_context(patch.object(g.session,'fresh_start',start));stack.enter_context(patch.object(g.session,'stop_owned',stop))
            stack.enter_context(patch.object(g.session,'settings_snapshot',return_value={'publication':'SYNTHETIC metadata'}))
            stack.enter_context(patch.object(g.native,'MutationProbe',Probe));stack.enter_context(patch.object(g.exit_protocol,'finish_original',return_value=[]))
            stack.enter_context(patch.object(g.subprocess,'run',process))
            result=g.run(args)
        report=json.loads((out/'runs/wp43-orchestration/run.json').read_text());self.assertFalse(state['guard'])
        self.assertTrue(report['shared_guard_released']);self.assertIn('master_after',report);self.assertTrue(state['master_in_guard'])
        if fault:
            self.assertIs(result['complete'],False);self.assertIs(report['complete'],False)
            self.assertEqual(state['start_count'],1);self.assertEqual(len(report['results']),1)
            self.assertEqual(report['results'][0]['outcome'],'incomplete');self.assertIn('master_after',report['results'][0])
            # A separate later case must also refuse before another fresh_start.
            with patch.object(g,'OUT',out),patch.object(g,'check',return_value={'sources':[]}):
                later=SimpleNamespace(**{**vars(args),'run_id':'wp43-other-case','case':'ascii-first-retrieve'})
                with self.assertRaises(g.Refusal)as e:g.run(later)
                self.assertEqual(e.exception.code,'PreviousIncomplete')
        return result,report,state,out

    def test_positive_simulated_boundary_reaches_two_complete_attempts(self):
        r,report,s,_=self.run_fault();self.assertIs(r['complete'],True);self.assertEqual(s['start_count'],2)
        self.assertEqual(s['extract_in_guard'],[True,True]);self.assertTrue(all(x['required_extraction_validated']for x in report['results']))

    def test_missing_pid_never_claims_stopped_or_extracts(self):
        r,report,s,_=self.run_fault('missing-pid');row=report['results'][0]
        self.assertNotIn('guest_stopped',row);self.assertNotIn('pid_gone_or_zombie',row);self.assertFalse(r['oracle_released'])
        self.assertEqual(s['mcopy_count'],0);self.assertEqual(s['stop_count'],0)

    def test_unowned_pid_never_claims_stopped_or_extracts(self):
        _,report,s,_=self.run_fault('unowned-pid');self.assertNotIn('guest_stopped',report['results'][0]);self.assertEqual(s['mcopy_count'],0)

    def test_stop_exception_preserves_error_skips_extraction_and_next_guest(self):
        _,report,s,_=self.run_fault('stop-error');self.assertEqual(s['mcopy_count'],0)
        self.assertTrue(any(e['phase']=='stop'for e in report['results'][0]['errors']))

    def test_mcopy_nonzero_is_incomplete_and_raw_failure_retained(self):
        _,report,s,out=self.run_fault('copy-nonzero');row=report['results'][0]
        self.assertEqual(row['exports'][0]['exit'],17);self.assertTrue(s['extract_in_guard'])
        self.assertEqual((out/'runs/wp43-orchestration/r1/extract-G43EMPTY.WP5.stderr').read_bytes(),b'injected mcopy failure')

    def test_missing_required_export_declaration_stops(self):self.run_fault('missing-declaration')
    def test_success_exit_without_output_file_stops(self):self.run_fault('missing-output')
    def test_zero_byte_output_stops(self):self.run_fault('zero-output')
    def test_postcopy_wrong_size_hash_stops(self):self.run_fault('post-copy-tamper')
    def test_cancelled_output_absence_is_required_before_next_guest(self):self.run_fault('unexpected-absence')

    def test_master_mismatch_is_retained_per_attempt_before_next_guest(self):
        _,report,_,_=self.run_fault('master-mismatch');row=report['results'][0]
        self.assertNotEqual(row['master_before'],row['master_after']);self.assertEqual(row['error_code'],'MasterChanged')

    def test_copy_exception_retains_entry_error_and_report(self):
        _,report,_,out=self.run_fault('copy-exception');self.assertIn('error',report['results'][0]['exports'][0])
        self.assertTrue((out/'runs/wp43-orchestration/r1/extract-G43EMPTY.WP5-failure.json').is_file())

    def test_prelaunch_failure_is_no_start_not_invented_termination(self):
        r,report,s,_=self.run_fault('prelaunch');row=report['results'][0]
        self.assertTrue(row['no_start_proven']);self.assertNotIn('guest_stopped',row)
        self.assertEqual(s['mcopy_count'],0);self.assertEqual(s['stop_count'],0);self.assertTrue(r['oracle_released'])

    def test_actual_pid_capture_refuses_missing_and_unrelated_process(self):
        import os
        with tempfile.TemporaryDirectory()as tmp:
            root=Path(tmp);q=SimpleNamespace(RUNTIME=root,SOCKET=root/'qmp.sock')
            with self.assertRaises(FileNotFoundError):g.capture_owned_pid(q,root/'work')
            (root/'qemu.pid').write_text(str(os.getpid()))
            with self.assertRaises(g.Refusal)as e:g.capture_owned_pid(q,root/'work')
            self.assertEqual(e.exception.code,'UnprovenPID')
            with self.assertRaises(g.Refusal):g.verify_owned_stop(q,root/'work',None)

    def test_hard_ten_attempt_cap_precedes_configure_or_next_start(self):
        with tempfile.TemporaryDirectory()as tmp:
            out=Path(tmp);runs=out/'runs';runs.mkdir()
            for i in range(5):
                d=runs/str(i);d.mkdir();(d/'run.json').write_text(json.dumps({'complete':True,'case':'other'+str(i),'results':[{},{}]}))
            args=SimpleNamespace(allow_vm=True,authorization_note='SYNTHETIC test',case='empty-first-save',run_id='wp43-over-budget')
            with patch.object(g,'OUT',out),patch.object(g,'check',return_value={'sources':[]}),patch.object(g.session,'configure')as configure:
                with self.assertRaises(g.Refusal)as e:g.run(args)
                self.assertEqual(e.exception.code,'GuestBudget');configure.assert_not_called()


if __name__=='__main__':unittest.main()
