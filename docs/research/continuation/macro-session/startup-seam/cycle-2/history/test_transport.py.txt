"""Public API/OS tests for the new generic transport. Apache-2.0 authored fixtures."""
import importlib.util
import os
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('startup_transport', pathlib.Path(os.environ.get('STARTUP_TRANSPORT_UNDER_TEST', str(ROOT/'scripts/reference/startup_transport.py'))))
st = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = st
spec.loader.exec_module(st)

class TransportTests(unittest.TestCase):
    def test_source_copy_and_prior_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            source = root/'source'
            source.write_bytes(b'authored fixture')
            artifact = st.ArtifactSpec.capture(source)
            with st.Attempt(root) as attempt:
                self.assertEqual(attempt.copy(artifact, 'copy').sha256, artifact.sha256)
                self.assertEqual((root/'copy').read_bytes(), source.read_bytes())
                with self.assertRaises(st.Failure):
                    attempt.copy(artifact, 'copy')
                self.assertEqual((root/'copy').read_bytes(), b'authored fixture')

    def test_public_verify_limit_cannot_exceed_frozen_ceiling(self):
        with tempfile.TemporaryDirectory() as d:
            source=pathlib.Path(d)/'source'
            source.write_bytes(b'x')
            artifact=st.ArtifactSpec.capture(source)
            for limit in (8388609,0,-1,1.5):
                with self.assertRaises(st.Failure):
                    artifact.verify(limit)

    def test_json_depth_and_size(self):
        self.assertEqual(st.decode_json(b'{"a":1}'), {'a':1})
        for value in (b'['*20+b'0'+b']'*20, b' '*65537, b'{', b'NaN'):
            with self.assertRaises(st.Failure):
                st.decode_json(value)

class OSTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='startup-os-')
        self.root = pathlib.Path(self.temp.name)
        self.tool = st.ArtifactSpec.capture(pathlib.Path(sys.executable).resolve())

    def tearDown(self):
        self.temp.cleanup()

    def command(self, body, name='child.py'):
        source = self.root/name
        source.write_text(body)
        artifact = st.ArtifactSpec.capture(source)
        return st.CommandSpec(self.tool, (self.tool.path, '-B', str(source)), str(self.root), sources=(artifact,))

    def run_failure(self, body, code, **limits):
        command = self.command(body)
        with st.Attempt(self.root, st.Limits(seconds=1, **limits)) as attempt:
            with self.assertRaises(st.Failure) as caught:
                attempt.run(command)
            error = caught.exception
            self.assertEqual(error.code, code)
            self.assertIsNotNone(error.result)
            self.assertGreater(error.result.spawned_pid, 0)
            self.assertEqual(error.result.launch_state, 'OBSERVED')
            self.assertEqual(error.result.daemon_state, 'UNKNOWN')
            self.assertEqual(error.result.cleanup, 'SESSION_STOPPED_DAEMON_UNKNOWN')
            self.assertFalse(pathlib.Path('/proc', str(error.result.spawned_pid)).exists())
            before = attempt.journal
            with self.assertRaises(st.Failure):
                attempt.run(command)
            self.assertEqual(attempt.journal, before)
            return error.result

    def test_success_exact_output_and_journal_copy(self):
        command = self.command("import os; os.write(1,b'hello'); os.write(2,b'error')\n")
        with st.Attempt(self.root) as attempt:
            result = attempt.run(command)
            self.assertEqual((result.returncode, result.stdout, result.stderr), (0, b'hello', b'error'))
            copy = attempt.journal
            copy[0]['phase'] = 'forged'
            self.assertEqual(attempt.journal[0]['phase'], 'intended')
            self.assertGreater(result.peak_rss, 0)
            self.assertLess(result.elapsed, 2)

    def test_nonzero_retains_partial_output(self):
        result = self.run_failure("import os; os.write(1,b'partial'); os._exit(7)\n", 'nonzero')
        self.assertEqual((result.returncode, result.stdout), (7, b'partial'))

    def test_stdout_limit(self):
        result = self.run_failure("import os; os.write(1,b'x'*65536)\n", 'output-limit', stream_bytes=1024)
        self.assertEqual(len(result.stdout), 1024)

    def test_stderr_limit(self):
        result = self.run_failure("import os; os.write(2,b'x'*65536)\n", 'output-limit', stream_bytes=1024)
        self.assertEqual(len(result.stderr), 1024)

    def test_aggregate_limit(self):
        self.run_failure("import os; os.write(1,b'x'*1000); os.write(2,b'y'*1000)\n", 'output-limit', stream_bytes=2000, aggregate_bytes=1500)

    def test_deadline_and_term_ignore(self):
        result = self.run_failure("import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); time.sleep(30)\n", 'deadline')
        self.assertEqual(result.returncode, -9)
        self.assertLess(result.elapsed, 2)

    def test_closed_pipe_orphan(self):
        result = self.run_failure("import os,time\nif os.fork()==0:\n os.close(1); os.close(2); time.sleep(30); os._exit(0)\nos._exit(0)\n", 'surviving-session-child')
        self.assertEqual(result.returncode, 0)

    def test_open_pipe_orphan(self):
        self.run_failure("import os,time\nif os.fork()==0: time.sleep(30); os._exit(0)\nos._exit(0)\n", 'surviving-session-child')

    def test_process_count(self):
        self.run_failure("import os,time\nfor i in range(4):\n if os.fork()==0: time.sleep(30); os._exit(0)\ntime.sleep(30)\n", 'process-limit', processes=2)

    def test_rss_aggregate(self):
        self.run_failure("import os,time\na=bytearray(18*1024*1024)\nif os.fork()==0: time.sleep(30); os._exit(0)\ntime.sleep(30)\n", 'rss-limit', rss_bytes=45*1024*1024)

    def test_exec_address_space_limit(self):
        result = self.run_failure("a=bytearray(200*1024*1024)\n", 'nonzero', rss_bytes=40*1024*1024)
        self.assertIn(b'MemoryError', result.stderr)

    def test_before_observer_failure_no_main_launch(self):
        command = self.command("from pathlib import Path; Path('FORBIDDEN').touch()\n")
        observer = self.command("import sys; sys.exit(9)\n", 'observer.py')
        with st.Attempt(self.root) as attempt:
            with self.assertRaises(st.Failure):
                attempt.run(command, before_spawn=observer)
            self.assertFalse((self.root/'FORBIDDEN').exists())
            self.assertEqual(sum(e['phase']=='spawned' for e in attempt.journal), 1)
            self.assertEqual(sum(e['phase']=='intended' for e in attempt.journal), 2)

    def test_post_identity_observer_failure_retains_main_pid(self):
        command = self.command("import time; time.sleep(10)\n")
        observer = self.command("import sys; sys.exit(8)\n", 'observer.py')
        with st.Attempt(self.root, st.Limits(seconds=1)) as attempt:
            with self.assertRaises(st.Failure) as caught:
                attempt.run(command, after_identity=observer)
            result = caught.exception.result
            self.assertEqual(caught.exception.code, 'nonzero')
            self.assertIsNotNone(result.identity)
            self.assertEqual(sum(e['phase']=='spawned' for e in attempt.journal), 2)
            self.assertFalse(pathlib.Path('/proc',str(result.spawned_pid)).exists())

    def test_unbounded_callback_is_capped(self):
        command = self.command("import time; time.sleep(10)\n")
        observer = self.command("import os; os.write(1,b'x'*65536)\n", 'observer.py')
        with st.Attempt(self.root, st.Limits(seconds=1, stream_bytes=1024)) as attempt:
            with self.assertRaises(st.Failure) as caught:
                attempt.run(command, before_spawn=observer)
            self.assertEqual(caught.exception.code, 'output-limit')
            self.assertEqual(sum(e['phase']=='spawned' for e in attempt.journal), 1)

    def test_sources_changed_before_launch(self):
        command = self.command("print('never')\n")
        pathlib.Path(command.sources[0].path).write_text("print('changed')\n")
        with st.Attempt(self.root) as attempt:
            with self.assertRaises(st.Failure):
                attempt.run(command)
            self.assertFalse(any(e['phase']=='spawned' for e in attempt.journal))

    def test_source_changed_during_execution(self):
        command = self.command("from pathlib import Path; Path(__file__).write_text('changed')\n")
        with st.Attempt(self.root) as attempt:
            with self.assertRaises(st.Failure) as caught:
                attempt.run(command)
            self.assertEqual(caught.exception.code, 'source-changed')
            self.assertIsNotNone(caught.exception.result.spawned_pid)

    def test_foreign_endpoint_zero_commands(self):
        import socket
        endpoint = self.root/'foreign'
        server = socket.socket(socket.AF_UNIX)
        server.bind(str(endpoint))
        server.listen(1)
        server.settimeout(2)
        command = self.command("import time; time.sleep(10)\n")
        try:
            with st.Attempt(self.root, st.Limits(seconds=1)) as attempt:
                with self.assertRaises(st.Failure) as caught:
                    attempt.run(command, readiness=st.EndpointSpec(str(endpoint)))
                self.assertEqual(caught.exception.code, 'foreign-peer')
                self.assertTrue(endpoint.exists())
        finally:
            connection,_=server.accept()
            with connection:
                captured=connection.recv(4096)
            server.close()
        self.assertEqual(captured, b'')

    def test_legitimate_endpoint_and_callback(self):
        endpoint = self.root/'owned'
        command = self.command("import socket,time\ns=socket.socket(socket.AF_UNIX); s.bind('owned'); s.listen(1)\nc,_=s.accept(); assert c.recv(64)==b'TEST ping\\n'; c.sendall(b'TEST ready\\n'); c.close(); s.close(); time.sleep(.03)\n")
        observer = self.command("print('observation only')\n", 'observer.py')
        with st.Attempt(self.root) as attempt:
            result = attempt.run(command, readiness=st.EndpointSpec(str(endpoint)), after_identity=observer)
            self.assertTrue(result.ready)
            self.assertIsNotNone(result.identity)
            self.assertEqual(result.identity.pid, result.spawned_pid)
            self.assertTrue(endpoint.exists())

    def test_no_readiness_after_early_exit(self):
        command = self.command("pass\n")
        with st.Attempt(self.root) as attempt:
            with self.assertRaises(st.Failure) as caught:
                attempt.run(command, readiness=st.EndpointSpec(str(self.root/'absent')))
            self.assertEqual(caught.exception.code, 'not-ready')

    def test_stale_identity_and_unknown_pid(self):
        import os
        import dataclasses
        identity = st.Identity.observe(os.getpid())
        with self.assertRaises(st.Failure):
            dataclasses.replace(identity,ticks=identity.ticks+1).verify()
        with self.assertRaises(st.Failure):
            st.Identity.observe(2147483647)

    def test_no_arbitrary_callback(self):
        command = self.command("pass\n")
        with st.Attempt(self.root) as attempt:
            with self.assertRaises(st.Failure):
                attempt.run(command, before_spawn=lambda: True)
            self.assertFalse(any(e['phase']=='spawned' for e in attempt.journal))

    def test_no_replace_publication_and_prior_json(self):
        prior = self.root/'report'
        prior.write_bytes(b'original')
        with st.Attempt(self.root) as attempt:
            with self.assertRaises(st.Failure):
                attempt.publish('report',{'new':True})
            self.assertEqual(prior.read_bytes(),b'original')
            self.assertFalse(any(e['phase']=='publication-durable' for e in attempt.journal))

    def test_hardlink_symlink_retarget(self):
        import os
        source = self.root/'source'
        source.write_bytes(b'original')
        artifact = st.ArtifactSpec.capture(source)
        os.link(source,self.root/'alias')
        with self.assertRaises(st.Failure):
            artifact.verify()
        (self.root/'alias').unlink()
        (self.root/'link').symlink_to(source)
        with self.assertRaises(st.Failure):
            st.ArtifactSpec.capture(self.root/'link')
        source.unlink()
        source.write_bytes(b'original')
        with self.assertRaises(st.Failure):
            artifact.verify()

    def test_changed_wrapper_and_snapshot(self):
        import dataclasses
        source = self.root/'source'
        source.write_bytes(b'original')
        artifact = st.ArtifactSpec.capture(source)
        with st.Attempt(self.root) as attempt:
            self.assertEqual(attempt.snapshot((artifact,)), ((str(source),artifact.sha256),))
            with self.assertRaises(st.Failure):
                attempt.copy(dataclasses.replace(artifact,sha256='0'*64),'target')
            self.assertFalse((self.root/'target').exists())

    def test_publish_json_success_and_closed_lifetime(self):
        attempt = st.Attempt(self.root)
        attempt.publish('report',{'observed':True})
        self.assertEqual(st.decode_json((self.root/'report').read_bytes()),{'observed':True})
        attempt.close()
        with self.assertRaises(st.Failure):
            attempt.publish('again',{})

    def test_directory_retarget_refusal(self):
        actual = self.root/'directory'
        actual.mkdir()
        with st.Attempt(actual) as attempt:
            actual.rename(self.root/'old')
            actual.mkdir()
            with self.assertRaises(st.Failure):
                attempt.publish('report',{})
            self.assertFalse((actual/'report').exists())

    def test_limits_are_closed(self):
        for kwargs in ({'seconds':16},{'stream_bytes':1048577},{'processes':0},{'seconds':float('nan')},{'files':2.5}):
            with self.assertRaises(st.Failure):
                st.Limits(**kwargs)

    def test_cli_roster(self):
        import json
        import subprocess
        for case in ('success','nonzero','stdout','stderr','hang','orphan','observer-fail','readiness'):
            with self.subTest(case=case):
                completed = subprocess.run([sys.executable,'-B',str(ROOT/'scripts/reference/startup_transport.py'),'fixture',case],capture_output=True,timeout=8)
                value = json.loads(completed.stdout)
                self.assertEqual(value['ok'],case in ('success','readiness'))
                self.assertEqual(completed.returncode,0 if value['ok'] else 1)
                self.assertLess(len(completed.stdout),65536)

class AdditionalOSTests(unittest.TestCase):
    setUp = OSTests.setUp
    tearDown = OSTests.tearDown
    command = OSTests.command
    run_failure = OSTests.run_failure
    def test_callback_cannot_hide_parent_output_or_deadline(self):
        command = self.command("import os,time; os.write(1,b'x'*65536); time.sleep(10)\n")
        observer = self.command("import time; time.sleep(10)\n", 'observer.py')
        with st.Attempt(self.root,st.Limits(seconds=.7,stream_bytes=1024)) as attempt:
            with self.assertRaises(st.Failure) as caught:
                attempt.run(command,after_identity=observer)
            self.assertEqual(caught.exception.code,'output-limit')
            self.assertLess(caught.exception.result.elapsed,1.5)
            self.assertEqual(len(caught.exception.result.stdout),1024)

    def test_new_process_group_still_cleaned(self):
        self.run_failure("import os,time\nif os.fork()==0:\n os.setpgrp(); time.sleep(30); os._exit(0)\nos._exit(0)\n",'surviving-session-child')

    def test_real_short_write_prior_integrity(self):
        import json
        import subprocess
        root = str(ROOT/'scripts/reference/startup_transport.py')
        script = self.root/'fault.py'
        script.write_text("import importlib.util,sys,resource,signal,json\nfrom pathlib import Path\ns=importlib.util.spec_from_file_location('st',sys.argv[1]); st=importlib.util.module_from_spec(s); sys.modules['st']=st; s.loader.exec_module(st)\np=Path(sys.argv[2]); (p/'source').write_bytes(b'x'*8192); (p/'prior').write_bytes(b'unchanged'); a=st.ArtifactSpec.capture(p/'source')\nwith st.Attempt(p) as attempt:\n resource.setrlimit(resource.RLIMIT_FSIZE,(1024,1024)); signal.signal(signal.SIGXFSZ,signal.SIG_IGN)\n try: attempt.copy(a,'target'); raise AssertionError('succeeded')\n except st.Failure as e: assert e.code in ('OSError','journal-persistence')\n assert not (p/'target').exists(); assert (p/'prior').read_bytes()==b'unchanged'\n assert not any(x['phase']=='publication-durable' for x in attempt.journal)\n print('short-write-preserved')\n")
        complete = subprocess.run([sys.executable,'-B',str(script),root,str(self.root)],capture_output=True,timeout=4)
        self.assertEqual(complete.returncode,0,complete.stderr)
        self.assertEqual(complete.stdout,b'short-write-preserved\n')

    def test_no_clobber_journal(self):
        (self.root/'attempt.jsonl').write_bytes(b'prior')
        with self.assertRaises(FileExistsError):
            st.Attempt(self.root)
        self.assertEqual((self.root/'attempt.jsonl').read_bytes(),b'prior')

    def test_json_preflight_large_or_custom(self):
        for value in (['x']*3000, {'huge':'x'*65537}, object(), {'x':float('nan')}):
            # Each failure gets a separate private attempt directory.
            with tempfile.TemporaryDirectory() as d:
                with st.Attempt(pathlib.Path(d)) as attempt:
                    with self.assertRaises(st.Failure):
                        attempt.publish('report',value)
                    self.assertFalse((pathlib.Path(d)/'report').exists())

    def test_durable_journal_before_spawn_observed_by_child(self):
        command = self.command("from pathlib import Path\nimport json\nevents=[json.loads(x) for x in Path('attempt.jsonl').read_text().splitlines()]\nassert any(e['phase']=='pre-spawn' for e in events)\nprint('observed')\n")
        with st.Attempt(self.root) as attempt:
            result=attempt.run(command)
            self.assertEqual(result.stdout,b'observed\n')

    def test_failed_journal_after_launch_retains_pid(self):
        import subprocess
        script = self.root/'journal_fault.py'
        script.write_text("import importlib.util,sys,resource,signal\nfrom pathlib import Path\ns=importlib.util.spec_from_file_location('st',sys.argv[1]); st=importlib.util.module_from_spec(s); sys.modules['st']=st; s.loader.exec_module(st)\np=Path(sys.argv[2]); child=p/'child.py'; child.write_text('pass\\n'); tool=st.ArtifactSpec.capture(Path(sys.executable).resolve()); source=st.ArtifactSpec.capture(child); command=st.CommandSpec(tool,(tool.path,'-B',str(child)),str(p),sources=(source,))\nwith st.Attempt(p) as a:\n resource.setrlimit(resource.RLIMIT_FSIZE,(520,520)); signal.signal(signal.SIGXFSZ,signal.SIG_IGN)\n try: a.run(command); raise AssertionError('succeeded')\n except st.Failure as e:\n  assert e.result is not None and e.result.spawned_pid is not None, (e.code,e.result)\n  assert not Path('/proc',str(e.result.spawned_pid)).exists()\n  print('partial-launch-retained',e.code)\n")
        complete = subprocess.run([sys.executable,'-B',str(script),str(ROOT/'scripts/reference/startup_transport.py'),str(self.root)],capture_output=True,timeout=4)
        self.assertEqual(complete.returncode,0,complete.stderr)
        self.assertIn(b'partial-launch-retained journal-persistence',complete.stdout)

    def test_threaded_launch_refuses_before_spawn(self):
        import threading
        command=self.command("print('never')\n")
        failures=[]
        with st.Attempt(self.root) as attempt:
            def invoke():
                try: attempt.run(command)
                except st.Failure as error: failures.append(error.code)
            thread=threading.Thread(target=invoke)
            thread.start(); thread.join(2)
            self.assertEqual(failures,['single-thread-launch-required'])
            self.assertFalse(any(e['phase']=='spawned' for e in attempt.journal))

    def test_journal_retarget_after_launch_refuses(self):
        command=self.command("from pathlib import Path; Path('attempt.jsonl').unlink(); Path('attempt.jsonl').write_text('foreign')\n")
        with st.Attempt(self.root) as attempt:
            with self.assertRaises(st.Failure) as caught:
                attempt.run(command)
            self.assertEqual(caught.exception.code,'journal-persistence')
            self.assertIsNotNone(caught.exception.result.spawned_pid)
            self.assertEqual((self.root/'attempt.jsonl').read_text(),'foreign')

    def test_command_cwd_retarget_before_launch_refuses(self):
        directory=self.root/'cwd'
        directory.mkdir()
        command=self.command("print('never')\n")
        import dataclasses
        command=dataclasses.replace(command,cwd=str(directory))
        directory.rename(self.root/'old')
        directory.mkdir()
        with st.Attempt(self.root) as attempt:
            with self.assertRaises(st.Failure):
                attempt.run(command)
            self.assertFalse(any(e['phase']=='spawned' for e in attempt.journal))

    def test_hook_receives_copied_identity_facts(self):
        command=self.command("import time; time.sleep(.35)\n")
        observer=self.command("import json,sys\nf=json.load(sys.stdin); assert f['phase']=='after-identity'; assert f['identity']['pid']>0; print('diagnostic')\n",'observer.py')
        with st.Attempt(self.root) as attempt:
            result=attempt.run(command,after_identity=observer)
            self.assertEqual(result.returncode,0)
            self.assertIsNotNone(result.identity)

    def test_input_bytes_and_callback_json_are_bounded(self):
        import dataclasses
        command=self.command("import sys; assert sys.stdin.buffer.read()==b'input'\n")
        with st.Attempt(self.root) as attempt:
            self.assertEqual(attempt.run(dataclasses.replace(command,input_bytes=b'input')).returncode,0)
            with self.assertRaises(st.Failure):
                attempt.run(dataclasses.replace(command,input_bytes=b'x'*65537))

    def test_kernel_exec_change_after_binding_refuses(self):
        command=self.command("import os,time\nfrom pathlib import Path\nwhile not Path('hookdone').exists(): time.sleep(.01)\ntime.sleep(.3); os.execv('/usr/bin/sleep',['/usr/bin/sleep','.2'])\n")
        observer=self.command("from pathlib import Path; Path('hookdone').touch()\n",'observer.py')
        with st.Attempt(self.root) as attempt:
            with self.assertRaises(st.Failure) as caught:
                attempt.run(command,after_identity=observer)
            self.assertEqual(caught.exception.code,'identity-changed')
            self.assertIsNotNone(caught.exception.result.identity)

    def test_actual_cancel_after_spawn_retains_cleanup(self):
        import signal
        def cancel(*args): raise KeyboardInterrupt()
        command=self.command("import time; time.sleep(10)\n")
        prior=signal.signal(signal.SIGALRM,cancel)
        try:
            with st.Attempt(self.root) as attempt:
                signal.setitimer(signal.ITIMER_REAL,.3)
                with self.assertRaises(st.Failure) as caught:
                    attempt.run(command)
                signal.setitimer(signal.ITIMER_REAL,0)
                self.assertEqual(caught.exception.code,'KeyboardInterrupt')
                self.assertIsNotNone(caught.exception.result.spawned_pid)
                self.assertFalse(pathlib.Path('/proc',str(caught.exception.result.spawned_pid)).exists())
        finally:
            signal.setitimer(signal.ITIMER_REAL,0)
            signal.signal(signal.SIGALRM,prior)

    def test_callback_json_cannot_mint_readiness(self):
        command=self.command("import time; time.sleep(1)\n")
        observer=self.command("import json; print(json.dumps(dict(ready=True,pid=1)))\n",'observer.py')
        with st.Attempt(self.root) as attempt:
            with self.assertRaises(st.Failure) as caught:
                attempt.run(command,after_identity=observer,readiness=st.EndpointSpec(str(self.root/'absent')))
            self.assertEqual(caught.exception.code,'not-ready')
            self.assertFalse(caught.exception.result.ready)

    def test_escaped_daemon_not_claimed_gone_or_adopted_from_pidfile(self):
        import time
        command=self.command("import os,time\nif os.fork()==0:\n os.setsid(); open('pidfile','w').write(str(os.getpid())); os.close(1); os.close(2); time.sleep(.4); os._exit(0)\ntime.sleep(.03)\n")
        with st.Attempt(self.root) as attempt:
            result=attempt.run(command)
            self.assertEqual(result.daemon_state,'UNKNOWN')
            self.assertNotEqual(result.spawned_pid,int((self.root/'pidfile').read_text()))
            # The test child exits autonomously; no PID-file-derived signal authority.
            time.sleep(.5)

if __name__ == '__main__':
    unittest.main()
