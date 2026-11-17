"""Real OS R1 regressions. ONLY this test process adopts its own descendants."""
from pathlib import Path
import contextlib
import argparse
import ctypes
import hashlib
import io
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import types
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[5]
SCRIPT = ROOT / 'scripts/reference/secondary_record_contract.py'
SOURCE = Path(os.environ.get('WP53_CHECKER_SOURCE', SCRIPT))
C = types.ModuleType('secondary_checker')
C.__file__ = str(SCRIPT)
exec(compile(SOURCE.read_bytes(), str(SOURCE), 'exec'), C.__dict__)
RESULTS = []


def state(pid):
    try:
        raw = Path(f'/proc/{pid}/stat').read_text()
    except FileNotFoundError:
        return None
    fields = raw.rsplit(')', 1)[1].split()
    return {'pid': pid, 'state': fields[0], 'ppid': int(fields[1]),
            'pgid': int(fields[2]), 'sid': int(fields[3]), 'ticks': int(fields[19]), 'raw': raw}


def reap(pid, seconds=1):
    until = time.monotonic() + seconds
    while time.monotonic() < until:
        try:
            got, status = os.waitpid(pid, os.WNOHANG)
        except ChildProcessError:
            if state(pid) is None:
                return None
            raise
        if got:
            return status
        time.sleep(.005)
    raise AssertionError(f'known adopted child {pid} did not become reapable')


class CleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.prctl(36, 1, 0, 0, 0) != 0:  # Linux PR_SET_CHILD_SUBREAPER, TEST ONLY.
            raise OSError(ctypes.get_errno(), 'test subreaper unavailable')

    def group_case(self, *, alive=False, ignore=False, flood=False, read_fault=False):
        with tempfile.TemporaryDirectory(prefix='wp53-r1-owned-') as d:
            d = Path(d); ready = d / 'child.json'
            child = f'''import json,os,signal,time,sys
from pathlib import Path
if {ignore!r}: signal.signal(signal.SIGTERM,signal.SIG_IGN)
pid=os.getpid();raw=Path(f'/proc/{{pid}}/stat').read_text();fields=raw.rsplit(')',1)[1].split()
Path({str(ready)!r}).write_text(json.dumps({{'pid':pid,'ppid':os.getppid(),'pgid':os.getpgid(0),'sid':os.getsid(0),'ticks':int(fields[19]),'argv':sys.argv,'exe':os.readlink(f'/proc/{{pid}}/exe')}}))
if {flood!r}:
 if not {alive!r}:
  parent=os.getppid()
  until=time.monotonic()+2
  while time.monotonic()<until:
   try:
    if Path(f'/proc/{{parent}}/stat').read_text().rsplit(')',1)[1].split()[0]=='Z':break
   except FileNotFoundError:break
   time.sleep(.002)
 os.write(1,b'X'*8192)
time.sleep(10)
'''
            parent = f'''import subprocess,sys,time
from pathlib import Path
subprocess.Popen([sys.executable,'-c',{child!r}])
until=time.monotonic()+2
while not Path({str(ready)!r}).exists() and time.monotonic()<until:time.sleep(.002)
if {alive!r}:time.sleep(10)
'''
            argv = [sys.executable, '-c', parent]
            launched = []; real_popen = subprocess.Popen; real_selector = C.selectors.DefaultSelector
            real_killpg = os.killpg; signals = []; leader_start = []
            def capture(*a, **kw):
                process = real_popen(*a, **kw);launched.append(process);leader_start.append(state(process.pid));return process
            def signal_group(pgid, sig):
                self.assertEqual(pgid, launched[0].pid)
                pinned = state(pgid)
                self.assertIsNotNone(pinned)
                self.assertEqual(pinned['ticks'], leader_start[0]['ticks'])
                self.assertEqual(pinned['pgid'], pgid);self.assertEqual(pinned['sid'], pgid)
                self.assertIsNone(launched[0].returncode)
                if sig:signals.append({'signal':sig, 'pin':pinned, 'returncode_before_signal':launched[0].returncode})
                return real_killpg(pgid,sig)
            class FaultSelector(real_selector):
                def select(self, timeout=None):
                    until = time.monotonic() + 1
                    while not ready.exists() and time.monotonic() < until:time.sleep(.002)
                    if not alive:
                        while time.monotonic() < until:
                            current = state(launched[0].pid)
                            if current and current['state'] == 'Z':break
                            time.sleep(.002)
                    raise OSError('injected owned selector failure')
            row = {'alive_leader': alive, 'ignore_TERM': ignore, 'flood': flood,
                   'read_fault': read_fault, 'argv': argv, 'child_argv': [sys.executable, '-c', child],
                   'checker_source': str(SOURCE), 'checker_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest()}
            started = time.monotonic(); child_info = None
            try:
                with mock.patch.object(C.subprocess, 'Popen', side_effect=capture), \
                     mock.patch.object(C.selectors, 'DefaultSelector', FaultSelector if read_fault else real_selector), \
                     mock.patch.object(C.os, 'killpg', side_effect=signal_group):
                    with self.assertRaises((C.Refusal, OSError)) as error:
                        C.bounded(argv, d, timeout=.3, cap=1024)
                row['error'] = str(error.exception)
                expected = 'injected owned selector failure' if read_fault else ('HelperOutputLimit' if flood else 'HelperTimeout')
                self.assertIn(expected, row['error'])
                row['actual_private_group_signals'] = signals
                self.assertEqual(len(launched), 1)
                child_info = json.loads(ready.read_text())
                leader = launched[0]
                self.assertEqual(child_info['pgid'], leader.pid)
                self.assertEqual(child_info['sid'], leader.pid)
                self.assertEqual(child_info['ppid'], leader.pid)
                self.assertEqual(child_info['exe'], os.readlink(f'/proc/{os.getpid()}/exe'))
                after = state(child_info['pid']);row.update(child_identity=child_info, leader_pid=leader.pid,
                    leader_returncode=leader.returncode, descendant_after_return=after)
                if after is not None:
                    self.assertEqual(after['ticks'], child_info['ticks'])
                    self.assertEqual(after['pgid'], leader.pid)
                    row['state_before_bounded_adopted_reap'] = after['state']
                status = reap(child_info['pid'])
                row['child_wait_status'] = status
                self.assertIsNone(state(child_info['pid']))
                self.assertIsNotNone(leader.returncode)
                self.assertIsNone(state(leader.pid))
                with self.assertRaises(ProcessLookupError):os.killpg(leader.pid, 0)
                row['positive_group_gone_after_exact_reap'] = True
                if ignore:
                    self.assertTrue(os.WIFSIGNALED(status))
                    self.assertEqual(os.WTERMSIG(status), signal.SIGKILL)
                self.assertLess(time.monotonic()-started, 4.5)
            finally:
                row['elapsed_seconds'] = time.monotonic()-started
                # A failing RED/mutant must not leave its test-owned group alive.
                # Check the exact recorded child identity before emergency signal.
                if child_info is None and ready.exists():child_info=json.loads(ready.read_text())
                if child_info is not None:
                    now=state(child_info['pid'])
                    if now is not None and now['state']!='Z':
                        assert now['ticks']==child_info['ticks'] and now['pgid']==child_info['pgid']
                        assert launched and child_info['pgid']==launched[0].pid
                        os.killpg(child_info['pgid'],signal.SIGKILL)
                        row['RED_emergency_cleanup_only_recorded_owned_group']=True
                    with contextlib.suppress(ChildProcessError):reap(child_info['pid'])
                for leader in launched:
                    if leader.returncode is None:leader.wait(timeout=1)
                RESULTS.append(row)

    def test_alive_leader_timeout(self):self.group_case(alive=True)
    def test_exited_leader_timeout(self):self.group_case()
    def test_exited_leader_ignores_TERM(self):self.group_case(ignore=True)
    def test_exited_leader_output_limit(self):self.group_case(ignore=True,flood=True)
    def test_alive_leader_output_limit(self):self.group_case(alive=True,flood=True)
    def test_exited_leader_selector_fault(self):self.group_case(ignore=True,read_fault=True)

    def test_pipe_EOF_before_leader_wait_timeout(self):
        argv=[sys.executable,'-c','import os,time;os.close(1);os.close(2);time.sleep(10)']
        launched=[];real=subprocess.Popen
        def capture(*a,**kw):
            p=real(*a,**kw);launched.append(p);return p
        start=time.monotonic()
        with mock.patch.object(C.subprocess,'Popen',side_effect=capture):
            with self.assertRaises(subprocess.TimeoutExpired):C.bounded(argv,ROOT,timeout=.15)
        self.assertIsNone(state(launched[0].pid));self.assertIsNotNone(launched[0].returncode)
        self.assertLess(time.monotonic()-start,3.5)
        RESULTS.append({'case':'pipe-EOF-wait-timeout','argv':argv,'leader':launched[0].pid,
                        'returncode':launched[0].returncode,'positive_leader_reaped':True})

    def test_selector_construction_failure_cleans_unreaped_child(self):
        launched=[];real=subprocess.Popen
        def capture(*a,**kw):
            p=real(*a,**kw);launched.append(p);return p
        with mock.patch.object(C.subprocess,'Popen',side_effect=capture), \
             mock.patch.object(C.selectors,'DefaultSelector',side_effect=OSError('injected selector constructor')):
            with self.assertRaisesRegex(OSError,'injected selector constructor'):
                C.bounded([sys.executable,'-c','import time;time.sleep(10)'],ROOT,timeout=.3)
        self.assertIsNone(state(launched[0].pid));self.assertIsNotNone(launched[0].returncode)
        RESULTS.append({'case':'selector-constructor-failure','leader':launched[0].pid,'returncode':launched[0].returncode,'positive_leader_reaped':True})

    def test_selector_close_failure_still_has_unreaped_pin(self):
        launched=[];real=subprocess.Popen;base=C.selectors.DefaultSelector
        def capture(*a,**kw):
            p=real(*a,**kw);launched.append(p);return p
        class CloseFault(base):
            failed=False
            def close(self):
                if not self.failed:self.failed=True;raise OSError('injected selector close')
                return super().close()
        with mock.patch.object(C.subprocess,'Popen',side_effect=capture), \
             mock.patch.object(C.selectors,'DefaultSelector',CloseFault):
            with self.assertRaisesRegex(OSError,'injected selector close'):
                C.bounded([sys.executable,'-c','pass'],ROOT,timeout=.3)
        self.assertEqual(launched[0].returncode,0);self.assertIsNone(state(launched[0].pid))
        RESULTS.append({'case':'selector-close-failure','leader':launched[0].pid,'returncode':0,'positive_leader_reaped':True})

    def test_unproven_group_identity_is_not_signalled(self):
        p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(10)'],start_new_session=True)
        original=state(p.pid);real_signal=os.killpg
        try:
            with mock.patch.object(C.os,'getpgid',return_value=p.pid+1), \
                 mock.patch.object(C.os,'killpg')as signal_mock:
                with self.assertRaisesRegex(C.Refusal,'CleanupOwnershipLost'):
                    C._terminate_owned_group(p)
                signal_mock.assert_not_called()
        finally:
            current=state(p.pid)
            if current:
                self.assertEqual(current['ticks'],original['ticks'])
                self.assertEqual(current['pgid'],p.pid);self.assertEqual(current['sid'],p.pid)
                real_signal(p.pid,signal.SIGKILL)
            p.wait(timeout=1)
        self.assertIsNone(state(p.pid))
        RESULTS.append({'case':'unproven-group-refuses-signalling','known_test_leader':p.pid,'production_signal_calls':0,'test_owned_emergency_reap':True})

    def test_normal_success_nonzero_and_already_gone(self):
        self.assertEqual(C.bounded([sys.executable,'-c','print("ok")'],ROOT),(0,b'ok\n',b''))
        self.assertEqual(C.bounded([sys.executable,'-c','raise SystemExit(7)'],ROOT)[0],7)
        if hasattr(C,'_terminate_owned_group'):
            p=subprocess.Popen([sys.executable,'-c','pass'],start_new_session=True)
            deadline=time.monotonic()+1
            while os.waitid(os.P_PID,p.pid,os.WEXITED|os.WNOHANG|os.WNOWAIT) is None:
                self.assertLess(time.monotonic(),deadline);time.sleep(.005)
            self.assertIsNone(p.returncode)
            C._terminate_owned_group(p)  # dead/nonrunning group, STILL unreaped pin.
            self.assertEqual(p.returncode,0);self.assertIsNone(state(p.pid))
            with self.assertRaisesRegex(C.Refusal,'CleanupOwnershipLost'):
                C._terminate_owned_group(p)  # cannot signal after a lost/reaped pin


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('-k',default=None);args=parser.parse_args()
    if args.k:unittest.defaultTestLoader.testNamePatterns=['*'+args.k+'*']
    runner=unittest.TextTestRunner(verbosity=2)
    result=runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(CleanupTests))
    if os.environ.get('WP53_CLEANUP_RECEIPT'):
        Path(os.environ['WP53_CLEANUP_RECEIPT']).write_text(json.dumps({'tests':result.testsRun,
            'failures':len(result.failures),'errors':len(result.errors),'results':RESULTS},indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
