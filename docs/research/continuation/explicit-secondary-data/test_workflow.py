"""Public launcher and inherited bounded-OS acceptance (no private supervisor hooks)."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[4]
SPEC = importlib.util.spec_from_file_location('explicit_secondary_data', ROOT/'scripts/reference/explicit_secondary_data.py')
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

class WorkflowTests(unittest.TestCase):
    def test_diagnostic_refusals(self):
        for value in [b'', b'{', b'{}', b'{"schema":"wordling.explicit-secondary-data.v1"}', b'{} trailing']:
            with self.assertRaises(MOD.Refusal):
                MOD.diagnostic(value, [])

    def test_actual_diagnostic_and_replay_falsifiers(self):
        with tempfile.TemporaryDirectory() as directory:
            session = MOD.Session(ROOT, Path(directory))
            session.build()
            corpus, inputs = MOD.corpus_inputs(session)
            actual = session.qualify(inputs)
            self.assertEqual(MOD.compare_originals(actual, corpus)['explicit_fields'], 36)
            for change in ('missing', 'empty', 'source', 'truncated', 'old-observer'):
                altered = json.loads(json.dumps(actual))
                if change == 'missing': altered['inputs'][1]['records'][0]['missing']['valid'] = True
                if change == 'empty': altered['inputs'][1]['records'][0]['fields'][0]['explicitly_empty'] = True
                if change == 'source': altered['inputs'][0]['sha256'] = '0'*64
                if change == 'truncated': altered['inputs'].pop()
                if change == 'old-observer':
                    altered = json.loads((ROOT/'docs/research/continuation/secondary-record-contract/evidence/original-audit.json').read_text())
                with self.assertRaises(MOD.Refusal): MOD.diagnostic(json.dumps(altered).encode(), inputs)

    def test_source_substitution_preserves_report(self):
        import shutil
        manifest = json.loads((ROOT/MOD.OWNED/'source-manifest.json').read_text())
        pins = json.loads((ROOT/MOD.OWNED/'inherited-pins.json').read_text())
        files = set(manifest['files']) | {p['path'] for p in pins['unchanged_members']} | {
            str(MOD.OWNED/'source-manifest.json'), 'scripts/reference/explicit_secondary_data.py'}
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            for name in files:
                dest=target/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dest)
            report=target/'report.json';report.write_bytes(b'prior-success')
            source=target/'internal/merge/explicit/data.go';source.write_bytes(source.read_bytes()+b'\n// substituted\n')
            result=subprocess.run([sys.executable,str(target/'scripts/reference/explicit_secondary_data.py'),'audit','--report',str(report)],capture_output=True,timeout=30)
            self.assertNotEqual(result.returncode,0)
            self.assertIn(b'SourceSubstitution',result.stderr)
            self.assertEqual(report.read_bytes(),b'prior-success')

    def test_real_helper_exit_deadline_and_caps(self):
        with tempfile.TemporaryDirectory() as directory:
            runner = MOD.inherited_bounded(ROOT, Path(directory))
            code, out, err = runner([sys.executable, '-c', 'import sys;print("hello");sys.exit(7)'], ROOT, timeout=3, cap=64)
            self.assertEqual((code, out), (7, b'hello\n'))
            print(json.dumps({'public_bounded_exit': code, 'stdout': out.decode(), 'stderr': err.decode()}))
            for program, timeout, cap in [('import time;time.sleep(3)', .1, 64), ('print("x"*10000)', 3, 64), ('import sys;sys.stderr.write("x"*(2<<20))',3,64)]:
                began=time.monotonic()
                with self.assertRaises(Exception) as refused:
                    runner([sys.executable, '-c', program], ROOT, timeout=timeout, cap=cap)
                print(json.dumps({'public_bounded_refusal': str(refused.exception), 'elapsed_seconds':time.monotonic()-began, 'timeout':timeout,'stdout_cap':cap}))

    def test_exited_leader_term_ignoring_descendant_pipe_cleanup(self):
        with tempfile.TemporaryDirectory() as directory:
            runner = MOD.inherited_bounded(ROOT, Path(directory))
            marker = Path(directory)/'descendant.json'
            child = 'import os,signal,time,json;signal.signal(signal.SIGTERM,signal.SIG_IGN);open('+repr(str(marker))+',"w").write(json.dumps([os.getpid(),open("/proc/self/stat").read().split()[21]]));time.sleep(10)'
            leader = 'import subprocess,sys;subprocess.Popen([sys.executable,"-c",'+repr(child)+']);sys.exit(0)'
            with self.assertRaises(Exception):
                runner([sys.executable, '-c', leader], ROOT, timeout=.4, cap=4096)
            self.assertTrue(marker.exists())
            pid, birth = json.loads(marker.read_text())
            # A retained descendant zombie is dead, not running or falsely reaped.
            try:
                stat = Path(f'/proc/{pid}/stat').read_text().split()
                self.assertTrue(stat[21] != birth or stat[2] == 'Z')
                print(json.dumps({'owned_descendant':pid,'birth':birth,'observed_birth':stat[21],'state':stat[2],'reaped_claim':False}))
            except FileNotFoundError:
                print(json.dumps({'owned_descendant':pid,'birth':birth,'proc_absent_after_group_cleanup':True,'reaped_claim':False}))

    def test_ownership_loss_refuses_without_numeric_signal(self):
        with tempfile.TemporaryDirectory() as directory:
            runner = MOD.inherited_bounded(ROOT, Path(directory))
            # Another actual wait owner consumes this process's child. The public
            # helper must report its lost unreaped pin rather than signal a PID.
            program = 'import subprocess,sys;subprocess.Popen([sys.executable,"-c","import time;time.sleep(.4)"]);sys.exit(0)'
            import threading
            stop = threading.Event();reaped=[]
            def reap():
                while not stop.is_set():
                    try:
                        pid,status=os.waitpid(-1, os.WNOHANG)
                        if pid: reaped.append([pid,status])
                    except ChildProcessError: pass
                    time.sleep(.001)
            thread = threading.Thread(target=reap)
            thread.start()
            try:
                with self.assertRaises(Exception) as raised:
                    runner([sys.executable, '-c', program], ROOT, timeout=1, cap=64)
                self.assertIn('OwnershipLost', str(raised.exception))
                print(json.dumps({'actual_other_wait_owner_reaps':reaped,'public_refusal':str(raised.exception),'numeric_signal_after_lost_pin':False,'signal_fact_basis':'exact inherited public bounded source branch before signal'}))
            finally:
                stop.set();thread.join()

    def test_cli_failure_preserves_existing_report(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory)/'report.json'; report.write_bytes(b'prior-good-report')
            bad = Path(directory)/'bad.wp5';bad.write_bytes(b'not native')
            for args in [['inspect','--input',str(bad),'--role','Secondary'], ['inspect','--input',str(bad),'--role','Other'], ['inspect','--input',str(bad),'--role','Primary']]:
                result = subprocess.run([sys.executable,str(ROOT/'scripts/reference/explicit_secondary_data.py'),*args,'--report',str(report)],capture_output=True,timeout=30)
                self.assertNotEqual(result.returncode,0)
                self.assertEqual(report.read_bytes(),b'prior-good-report')

if __name__ == '__main__': unittest.main()
