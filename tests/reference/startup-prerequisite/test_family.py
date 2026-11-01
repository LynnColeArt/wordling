"""Public OS acceptance for the generic TEST startup family. Apache-2.0."""
import dataclasses
import hashlib
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

ROOT=Path(__file__).resolve().parents[3]
FACADE=Path(os.environ.get('STARTUP_FAMILY_UNDER_TEST',str(ROOT/'scripts/reference/startup_transport.py')))
spec=importlib.util.spec_from_file_location('family_acceptance',FACADE)
st=importlib.util.module_from_spec(spec);spec.loader.exec_module(st)


def request(path):
    path=Path(path)
    digest=hashlib.sha256()
    with path.open('rb') as source:
        while raw:=source.read(65536):
            digest.update(raw)
    return st.SourceRequest(str(path),path.stat().st_size,digest.hexdigest())


class ManagedCase(unittest.TestCase):
    def setUp(self):
        self.temporary=tempfile.TemporaryDirectory(prefix='startup-family-test-')
        self.root=Path(self.temporary.name)
        self.session=None

    def tearDown(self):
        if self.session is not None:
            try:self.session.close()
            except st.StartupFailure:pass
        self.temporary.cleanup()

    def open(self,**policy):
        self.session=st.open_session(st.NewWorkspace(str(self.root/'workspace')),
                                     st.StreamPolicy.test_v1(),st.ManagedPolicy(**policy))
        return self.session

class ManagedTests(ManagedCase):
    def test_small_stream_and_no_clobber_is_sticky(self):
        source=self.root/'source';source.write_bytes(b'authored TEST')
        session=self.open()
        lease=session.capture(request(source))
        working=session.prepare(lease,'copy')
        self.assertEqual((self.root/'workspace/copy').read_bytes(),source.read_bytes())
        snapshot=session.snapshot(working)
        self.assertEqual(snapshot.sha256,request(source).sha256)
        with self.assertRaises(st.StartupFailure) as caught:
            session.prepare(lease,'copy')
        self.assertEqual(caught.exception.code,'NoClobber')
        with self.assertRaises(st.StartupFailure):
            session.capture(request(source))
        self.assertEqual(source.read_bytes(),b'authored TEST')

    def test_real_foreground_launch_finish(self):
        source=self.root/'child.py';source.write_text('import time; print("TEST"); time.sleep(.2)\n')
        session=self.open(total_seconds=3)
        script=session.capture(request(source))
        tool=session.tool(session.capture(request(Path(sys.executable).resolve())))
        process=session.launch(st.LaunchSpec(tool,(str(Path(sys.executable).resolve()),'-B',
                                                  st.ResourceArgument('',script,''))))
        observed=process.verify_current()
        self.assertGreater(observed.pid,0)
        result=process.finish()
        self.assertEqual(result.exit_code,0);self.assertTrue(result.reaped)
        self.assertEqual(result.signals_issued,())
        self.assertFalse(Path('/proc',str(result.created_pid)).exists())

    def test_alias_class_authority(self):
        second=importlib.util.spec_from_file_location('another_alias',FACADE)
        module=importlib.util.module_from_spec(second);second.loader.exec_module(module)
        self.assertIs(module.ArtifactSpec,st.ArtifactSpec)
        self.assertIs(module.Failure,st.Failure)
        self.assertIs(module.Session,st.Session)



class ChannelTests(ManagedCase):
    def peer(self,body,**policy):
        source=self.root/'peer.py'
        source.write_text("import os,sys,time,socket,signal\ns=socket.socket(socket.AF_UNIX)\n"
                          "s.bind('endpoint');s.listen(1)\nc,_=s.accept()\n"+body)
        session=self.open(total_seconds=3,**policy)
        script=session.capture(request(source))
        tool=session.tool(session.capture(request(Path(sys.executable).resolve())))
        process=session.launch(st.LaunchSpec(tool,(str(Path(sys.executable).resolve()),'-B',
                                                   st.ResourceArgument('',script,''))))
        return session,process,process.open_endpoint('endpoint')

    def test_exchange_and_public_send_receive(self):
        session,process,channel=self.peer("assert c.recv(64)==b'ping';c.sendall(b'ready')\n"
                                         "assert c.recv(64)==b'next';c.sendall(b'done');time.sleep(.2)\n")
        ready=channel.exchange(b'ping',b'ready',1)
        self.assertTrue(ready.ready)
        channel.send(b'next',1)
        self.assertEqual(channel.receive(4096,1),b'done')
        channel.close()
        self.assertEqual(process.finish().exit_code,0)

    def test_readiness_absolute_deadline(self):
        session,process,channel=self.peer("c.recv(64)\nfor b in b'ready':\n c.send(bytes([b]));time.sleep(.07)\n",
                                         readiness_seconds=.1)
        with self.assertRaises(st.StartupFailure) as caught:
            channel.exchange(b'ping',b'ready',1)
        self.assertEqual(caught.exception.code,'ReadinessDeadline')
        self.assertEqual(caught.exception.observation.cleanup,'STOPPED')
        with self.assertRaises(st.StartupFailure):process.verify_current()

    def test_exec_full_reply_exit_refused(self):
        session,process,channel=self.peer("c.recv(64)\nos.set_inheritable(c.fileno(),True)\n"
            "os.execve(sys.executable,(sys.executable,'-c',"
            "\"import socket,sys;socket.socket(fileno=int(sys.argv[1])).sendall(b'ready')\",str(c.fileno())),{})\n")
        with self.assertRaises(st.StartupFailure) as caught:
            channel.exchange(b'ping',b'ready',1)
        self.assertIn(caught.exception.code,('IdentityChanged','IdentityUnknown'))

    def test_process_limit_during_progress(self):
        session,process,channel=self.peer(
            "c.recv(64)\nchildren=[]\nfor i in range(2):\n"
            " p=os.fork()\n if p==0: time.sleep(.4);os._exit(0)\n children.append(p)\n"
            "for b in b'ready':\n c.send(bytes([b]));time.sleep(.07)\n"
            "for p in children:os.waitpid(p,0)\ntime.sleep(.2)\n",processes=4)
        with self.assertRaises(st.StartupFailure) as caught:
            channel.exchange(b'ping',b'ready',1)
        self.assertEqual(caught.exception.code,'ProcessLimit')

    def test_busy_resource_snapshot_refused(self):
        source=self.root/'source';source.write_bytes(b'data')
        session=self.open(total_seconds=3)
        working=session.prepare(session.capture(request(source)),'working')
        tool=session.tool(session.capture(request(Path(sys.executable).resolve())))
        process=session.launch(st.LaunchSpec(tool,(str(Path(sys.executable).resolve()),'-c',
                                                   'import time;time.sleep(2)')),(working,))
        with self.assertRaises(st.StartupFailure) as caught:session.snapshot(working)
        self.assertEqual(caught.exception.code,'BusyResource')
        self.assertEqual(caught.exception.observation.cleanup,'STOPPED')

class SuccessorTests(ManagedCase):
    def fixtures(self):
        source=self.root/'source';source.write_bytes(b'base')
        writer=self.root/'writer.py'
        writer.write_text("import sys,time\nfrom pathlib import Path\n"
                          "p=Path(sys.argv[1]);p.write_bytes(p.read_bytes()+b'!');time.sleep(.2)\n")
        session=self.open(total_seconds=3)
        original=session.capture(request(source));script=session.capture(request(writer))
        working=session.prepare(original,'working')
        python=Path(sys.executable).resolve()
        tool=session.tool(session.capture(request(python)))
        return session,source,script,working,tool,str(python)

    def mutate(self,session,script,working,tool,python):
        return session.mutate(working,st.MutationSpec(tool,(python,'-B',
            st.ResourceArgument('',script,''),st.ResourceArgument('',working,'')),
            immutable_inputs=(script,)))

    def test_successive_mutation_delivers_opaque_successor(self):
        session,source,script,working,tool,python=self.fixtures()
        first=self.mutate(session,script,working,tool,python)
        self.assertIsInstance(first,st.MutationResult)
        self.assertEqual((first.before_epoch,first.after_epoch),(0,1))
        self.assertIsNot(first.successor,working)
        snap=session.snapshot(first.successor)
        self.assertIs(snap.successor,first.successor)
        self.assertEqual(snap.epoch,1)
        self.assertIs(session.snapshot(first.successor).successor,first.successor)
        second=self.mutate(session,script,first.successor,tool,python)
        self.assertEqual(second.after_epoch,2)
        self.assertEqual((self.root/'workspace/working').read_bytes(),b'base!!')
        self.assertEqual(source.read_bytes(),b'base')
        process=session.launch(st.LaunchSpec(tool,(python,'-c','import time;time.sleep(.1)')),
                               (second.successor,))
        process.finish()
        stopped=session.snapshot(second.successor)
        self.assertEqual(stopped.epoch,3)
        self.assertIsNot(stopped.successor,second.successor)
        self.assertIs(session.snapshot(stopped.successor).successor,stopped.successor)

    def test_old_mutation_handle_stale_before_effect(self):
        session,source,script,working,tool,python=self.fixtures()
        result=self.mutate(session,script,working,tool,python)
        before=(self.root/'workspace/working').read_bytes()
        with self.assertRaises(st.StartupFailure) as caught:
            self.mutate(session,script,working,tool,python)
        self.assertEqual(caught.exception.code,'StaleEpoch')
        self.assertEqual((self.root/'workspace/working').read_bytes(),before)
        with self.assertRaises(st.StartupFailure):session.snapshot(result.successor)

    def test_ready_snapshot_same_object_no_epoch_churn(self):
        source=self.root/'source';source.write_bytes(b'data')
        session=self.open()
        working=session.prepare(session.capture(request(source)),'working')
        a=session.snapshot(working);b=session.snapshot(working)
        self.assertIs(a.successor,working);self.assertIs(b.successor,working)
        self.assertEqual((a.epoch,b.epoch),(0,0))

class StreamingTests(ManagedCase):
    def test_actual_64m_stream_no_payload_result_and_full_copy(self):
        source=self.root/'source64'
        chunk=bytes(range(256))*256
        digest=hashlib.sha256()
        with source.open('wb') as out:
            for _ in range(1024):
                out.write(chunk);digest.update(chunk)
        req=st.SourceRequest(str(source),67108864,digest.hexdigest())
        session=self.open(total_seconds=3)
        lease=session.capture(req)
        working=session.prepare(lease,'working')
        snap=session.snapshot(working)
        self.assertEqual((snap.size,snap.sha256),(67108864,digest.hexdigest()))
        with source.open('rb') as a,(self.root/'workspace/working').open('rb') as b:
            while left:=a.read(65536):
                self.assertEqual(left,b.read(65536))
            self.assertEqual(b.read(1),b'')
        with self.assertRaises(st.Failure):st.ArtifactSpec.capture(source)
        result=session.close();self.session=None
        self.assertTrue(result.supervisor_reaped)
        counters=dict(result.counters)
        self.assertLessEqual(counters['max_chunk'],65536)
        self.assertGreaterEqual(counters['source_io'],67108864*4)

    def test_over_file_size_refuses_before_read(self):
        source=self.root/'oversize'
        with source.open('wb') as out:out.truncate(67108865)
        session=self.open()
        with self.assertRaises(st.StartupFailure) as caught:
            session.capture(st.SourceRequest(str(source),67108865,'0'*64))
        self.assertEqual(caught.exception.code,'SourceTooLarge')
        self.assertEqual(source.stat().st_size,67108865)

    def test_large_executable_direct_control_and_new_lease(self):
        python=Path(sys.executable).resolve();large=self.root/'python-large'
        with python.open('rb') as a,large.open('wb') as b:
            while raw:=a.read(65536):b.write(raw)
            for _ in range(17):b.write(b'\0'*65536)
        large.chmod(0o755)
        self.assertGreater(large.stat().st_size,8388608)
        control=subprocess.run([str(large),'-c','print("public TEST ELF")'],
                               capture_output=True,timeout=3,env={})
        self.assertEqual(control.returncode,0,control.stderr)
        self.assertEqual(control.stdout,b'public TEST ELF\n')
        with self.assertRaises(st.Failure):st.ArtifactSpec.capture(large)
        session=self.open(total_seconds=3)
        tool=session.tool(session.capture(request(large)))
        process=session.launch(st.LaunchSpec(tool,(str(large),'-c',
            'import time;print("new policy TEST");time.sleep(.2)')))
        self.assertEqual(process.verify_current().exe_hash,request(large).sha256)
        self.assertEqual(process.finish().exit_code,0)

    def test_aggregate_source_io_cap(self):
        source=self.root/'source';source.write_bytes(b'x'*8192)
        self.session=st.open_session(st.NewWorkspace(str(self.root/'workspace')),
            st.StreamPolicy(io_bytes=4096),st.ManagedPolicy.test_v1(3))
        with self.assertRaises(st.StartupFailure) as caught:self.session.capture(request(source))
        self.assertEqual(caught.exception.code,'SourceTooLarge')

    def test_source_change_after_capture_refuses(self):
        source=self.root/'source';source.write_bytes(b'before')
        session=self.open();lease=session.capture(request(source));source.write_bytes(b'after!')
        with self.assertRaises(st.StartupFailure) as caught:session.prepare(lease,'working')
        self.assertEqual(caught.exception.code,'SourceChanged')
        self.assertFalse((self.root/'workspace/working').exists())

    def test_source_symlink_and_hardlink_refused(self):
        source=self.root/'source';source.write_bytes(b'data')
        alias=self.root/'alias';os.link(source,alias)
        session=self.open()
        with self.assertRaises(st.StartupFailure) as caught:session.capture(request(alias))
        self.assertEqual(caught.exception.code,'AliasRefused')

class FailureTests(ManagedCase):
    def running(self,code='import time;time.sleep(2)'):
        session=self.open(total_seconds=3)
        python=Path(sys.executable).resolve()
        tool=session.tool(session.capture(request(python)))
        process=session.launch(st.LaunchSpec(tool,(str(python),'-c',code)))
        return session,process

    def test_cancel_is_terminal_and_owned_child_reaped(self):
        session,process=self.running()
        pid=process.identity().pid
        outcome=process.cancel()
        self.assertEqual((outcome.first_fault,outcome.cleanup),('Cancelled','STOPPED'))
        self.assertFalse(Path('/proc',str(pid)).exists())
        with self.assertRaises(st.StartupFailure):process.verify_current()

    def test_handoff_silence_does_not_stop_stream_monitor(self):
        session,process=self.running('import os,time;time.sleep(.2);os.write(1,b"x"*1500000);time.sleep(1)')
        time.sleep(1.2)
        with self.assertRaises(st.StartupFailure) as caught:process.verify_current()
        self.assertEqual(caught.exception.code,'OutputLimit')
        self.assertEqual(caught.exception.observation.cleanup,'STOPPED')

    def test_worker_death_is_unknown_not_success(self):
        session,process=self.running('import time;time.sleep(.8)')
        identity=process.identity()
        # This test coordinator is actual direct parent; retain pidfd before kill.
        children=Path('/proc/self/task',str(os.getpid()),'children').read_text().split()
        workers=[]
        for value in children:
            pid=int(value)
            fields=Path('/proc',value,'stat').read_text().rsplit(')',1)[1].split()
            if int(fields[1])==os.getpid():
                fd=os.pidfd_open(pid);workers.append((pid,fd))
        self.assertEqual(len(workers),1)
        pid,fd=workers[0]
        import signal
        signal.pidfd_send_signal(fd,signal.SIGKILL);os.close(fd)
        with self.assertRaises(st.StartupFailure) as caught:process.verify_current()
        self.assertIn(caught.exception.code,('CleanupUnknown','ControlLost'))
        outcome=session.close();self.session=None
        self.assertEqual(outcome.cleanup,'UNKNOWN')
        deadline=time.monotonic()+1.5
        while time.monotonic()<deadline:
            try:
                fields=Path('/proc',str(identity.pid),'stat').read_text().rsplit(')',1)[1].split()
                if fields[0]=='Z' or int(fields[19])!=identity.startticks:break
            except FileNotFoundError:break
            time.sleep(.01)
        else:self.fail('authored orphan did not self-stop')

    def test_real_coordinator_kill_contains_term_ignoring_child(self):
        coordinator=self.root/'coordinator.py'
        coordinator.write_text("""import importlib.util,sys,json,time,hashlib
from pathlib import Path
s=importlib.util.spec_from_file_location('coordinator',sys.argv[1]);st=importlib.util.module_from_spec(s);s.loader.exec_module(st)
root=Path(sys.argv[2]);p=Path(sys.executable).resolve()
h=hashlib.sha256(p.read_bytes()).hexdigest()
a=st.open_session(st.NewWorkspace(str(root/'work')),st.StreamPolicy.test_v1(),st.ManagedPolicy.test_v1(3))
tool=a.tool(a.capture(st.SourceRequest(str(p),p.stat().st_size,h)))
child=a.launch(st.LaunchSpec(tool,(str(p),'-c','import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(2)')))
(root/'facts.json').write_text(json.dumps(dict(pid=child.identity().pid)))
time.sleep(5)
""")
        child=subprocess.Popen([sys.executable,'-B',str(coordinator),str(FACADE),str(self.root)],
                               stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            deadline=time.monotonic()+3
            while not (self.root/'facts.json').exists() and time.monotonic()<deadline:
                if child.poll() is not None:
                    self.fail(child.stderr.read().decode())
                time.sleep(.01)
            self.assertTrue((self.root/'facts.json').exists())
            start=time.monotonic();child.kill();child.wait(timeout=1)
            journal=self.root/'work/session.jsonl'
            deadline=time.monotonic()+1.6
            while time.monotonic()<deadline:
                text=journal.read_text()
                if '"code":"ParentLost"' in text or '"code":"ControlLost"' in text:
                    break
                time.sleep(.01)
            else:self.fail('worker did not observe parent loss')
            facts=__import__('json').loads((self.root/'facts.json').read_text())
            while time.monotonic()<deadline:
                try:
                    fields=Path('/proc',str(facts['pid']),'stat').read_text().rsplit(')',1)[1].split()
                    if fields[0]=='Z':break
                except FileNotFoundError:break
                time.sleep(.01)
            else:self.fail('owned child still active after parent loss')
            self.assertLess(time.monotonic()-start,1.6)
        finally:
            if child.poll() is None:child.kill()
            child.communicate(timeout=1)

    def test_forged_and_cross_session_handles_refuse(self):
        source=self.root/'source';source.write_bytes(b'data')
        session=self.open()
        lease=session.capture(request(source))
        with self.assertRaises(TypeError):st.SourceLease()
        with self.assertRaises(AttributeError):lease._epoch=99
        with self.assertRaises(st.StartupFailure) as caught:
            session.prepare({'token':'fake','epoch':1},'copy')
        self.assertEqual(caught.exception.code,'InvalidLease')
        self.assertFalse((self.root/'workspace/copy').exists())

class MutationFailureTests(ManagedCase):
    def fail_mutation(self,body):
        source=self.root/'source';source.write_bytes(b'unchanged master')
        prior=self.root/'prior';prior.write_bytes(b'foreign prior')
        toolscript=self.root/'mutation.py'
        toolscript.write_text("import os,sys,time,resource,signal\nfrom pathlib import Path\n"
                              "time.sleep(.1)\n"+body)
        session=self.open(total_seconds=3)
        working=session.prepare(session.capture(request(source)),'working')
        script=session.capture(request(toolscript));py=Path(sys.executable).resolve()
        tool=session.tool(session.capture(request(py)))
        with self.assertRaises(st.StartupFailure) as caught:
            session.mutate(working,st.MutationSpec(tool,(str(py),'-B',
                st.ResourceArgument('',script,''),st.ResourceArgument('',working,'')),
                immutable_inputs=(script,)))
        self.assertEqual(source.read_bytes(),b'unchanged master')
        self.assertEqual(prior.read_bytes(),b'foreign prior')
        self.assertEqual(len(caught.exception.observation.unusable_resources),1)
        self.assertIsInstance(caught.exception.result,st.MutationResult)
        self.assertEqual(caught.exception.result.status,'UNUSABLE')
        self.assertIsNone(caught.exception.result.successor)
        with self.assertRaises(st.StartupFailure):session.snapshot(working)
        return caught.exception

    def test_actual_nonzero_retains_partial_owned_bytes(self):
        error=self.fail_mutation("Path(sys.argv[1]).write_bytes(b'partial');sys.exit(7)\n")
        self.assertEqual((self.root/'workspace/working').read_bytes(),b'partial')
        self.assertEqual(error.observation.cleanup,'STOPPED')

    def test_actual_fsize_short_write_no_rollback(self):
        self.fail_mutation("resource.setrlimit(resource.RLIMIT_FSIZE,(3,3));signal.signal(signal.SIGXFSZ,signal.SIG_IGN)\n"
                           "Path(sys.argv[1]).write_bytes(b'123456789')\n")
        self.assertEqual((self.root/'workspace/working').read_bytes(),b'123')

    def test_actual_inode_replacement_is_unusable(self):
        error=self.fail_mutation("p=Path(sys.argv[1]);q=p.with_name('replacement');q.write_bytes(b'replaced');os.replace(q,p);time.sleep(.1)\n")
        self.assertEqual(error.code,'PathRetarget')
        self.assertEqual((self.root/'workspace/working').read_bytes(),b'replaced')

    def test_actual_journal_retarget_after_spawn_is_unknown_durability(self):
        error=self.fail_mutation("os.rename('session.jsonl','retained-journal');time.sleep(.1)\n")
        self.assertEqual(error.code,'JournalPersistence')
        self.assertFalse(error.observation.journal_durable)

class LoadingTests(ManagedCase):
    def copied(self,name):
        import shutil
        root=self.root/name;root.mkdir()
        shutil.copytree(FACADE.parent/'startup_family',root/'startup_family',
                        ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copyfile(FACADE,root/'startup_transport.py')
        return root/'startup_transport.py'

    def run_source(self,source,*args):
        runner=self.root/'runner.py';runner.write_text(source)
        p=subprocess.run([sys.executable,'-B',str(runner),*map(str,args)],
                         cwd=self.root,env={'PYTHONPATH':'/unrelated/nonexistent'},
                         capture_output=True,timeout=5)
        self.assertEqual(p.returncode,0,p.stderr.decode())
        return p

    def test_standalone_random_cwd_unrelated_pythonpath(self):
        p=subprocess.run([sys.executable,'-B',str(FACADE),'fixture','success'],
                         cwd=self.root,env={'PYTHONPATH':'/unrelated/nonexistent'},
                         capture_output=True,timeout=5)
        self.assertEqual(p.returncode,0,p.stderr.decode())

    def test_same_bytes_different_root_cannot_share_authority(self):
        first=self.copied('first');second=self.copied('second')
        self.run_source("""import importlib.util,sys
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
a=load('first',sys.argv[1])
try:load('second',sys.argv[2]);raise AssertionError('wrong root accepted')
except ImportError:pass
assert a.source_binding()['root'].endswith('/first/startup_family')
""",first,second)

    def test_changed_cached_package_refused(self):
        first=self.copied('first')
        self.run_source("""import importlib.util,sys
from pathlib import Path
def load(name):
 s=importlib.util.spec_from_file_location(name,sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
a=load('first');p=Path(sys.argv[1]).parent/'startup_family/engine.py';p.write_text(p.read_text()+'\\n# changed TEST source\\n')
try:load('second');raise AssertionError('changed source accepted')
except ImportError:pass
""",first)

    def test_failed_initial_load_cleans_only_owned_new_modules(self):
        first=self.copied('first')
        (first.parent/'startup_family/lifetime.py').write_text("raise RuntimeError('authored initialization failure')\n")
        self.run_source("""import importlib.util,sys
before=set(sys.modules)
s=importlib.util.spec_from_file_location('first',sys.argv[1]);m=importlib.util.module_from_spec(s)
try:s.loader.exec_module(m);raise AssertionError('failure missing')
except RuntimeError:pass
assert not any(k.startswith('wordling_reference_startup_v1') for k in sys.modules)
assert before<=set(sys.modules)
""",first)

    def test_parallel_alias_initialization_shares_single_classes(self):
        first=self.copied('first')
        self.run_source("""import importlib.util,sys,threading
classes=[];errors=[]
def load(i):
 try:
  s=importlib.util.spec_from_file_location('alias'+str(i),sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);classes.append(m.ArtifactSpec)
 except BaseException as e:errors.append(e)
threads=[threading.Thread(target=load,args=(i,)) for i in range(2)]
for t in threads:t.start()
for t in threads:t.join()
assert not errors,errors
assert len(classes)==2 and classes[0] is classes[1]
""",first)

    def test_symlink_facade_refused_before_effects(self):
        link=self.root/'linked.py';link.symlink_to(FACADE)
        with self.assertRaises(ImportError):
            s=importlib.util.spec_from_file_location('linked',link)
            m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

class BoundaryTests(ManagedCase):
    def test_wrong_declared_hash_refuses(self):
        source=self.root/'source';source.write_bytes(b'bounded TEST')
        session=self.open()
        with self.assertRaises(st.StartupFailure) as caught:
            session.capture(st.SourceRequest(str(source),source.stat().st_size,'0'*64))
        self.assertEqual(caught.exception.code,'SourceMismatch')

    def test_declared_source_aggregate_refuses(self):
        a=self.root/'a';b=self.root/'b';a.write_bytes(b'a'*8);b.write_bytes(b'b'*8)
        self.session=st.open_session(st.NewWorkspace(str(self.root/'workspace')),
            st.StreamPolicy(source_bytes=12),st.ManagedPolicy.test_v1(3))
        self.session.capture(request(a))
        with self.assertRaises(st.StartupFailure) as caught:self.session.capture(request(b))
        self.assertEqual(caught.exception.code,'SourceTooLarge')

    def test_preparation_aggregate_preserves_existing_working(self):
        source=self.root/'source';source.write_bytes(b'12345678')
        self.session=st.open_session(st.NewWorkspace(str(self.root/'workspace')),
            st.StreamPolicy(copied_bytes=12),st.ManagedPolicy.test_v1(3))
        lease=self.session.capture(request(source));self.session.prepare(lease,'first')
        with self.assertRaises(st.StartupFailure) as caught:self.session.prepare(lease,'second')
        self.assertEqual(caught.exception.code,'SourceTooLarge')
        self.assertEqual((self.root/'workspace/first').read_bytes(),b'12345678')
        self.assertFalse((self.root/'workspace/second').exists())

    def test_resource_descriptor_cap(self):
        a=self.root/'a';b=self.root/'b';a.write_bytes(b'a');b.write_bytes(b'b')
        self.session=st.open_session(st.NewWorkspace(str(self.root/'workspace')),
            st.StreamPolicy(resource_fds=1),st.ManagedPolicy.test_v1(3))
        self.session.capture(request(a))
        with self.assertRaises(st.StartupFailure) as caught:self.session.capture(request(b))
        self.assertEqual(caught.exception.code,'SourceTooLarge')

    def test_selected_preparation_deadline(self):
        source=self.root/'source';source.write_bytes(b'data')
        self.session=st.open_session(st.NewWorkspace(str(self.root/'workspace')),
            st.StreamPolicy(operation_seconds=.000001),st.ManagedPolicy.test_v1(3))
        with self.assertRaises(st.StartupFailure) as caught:self.session.capture(request(source))
        self.assertEqual(caught.exception.code,'StartupDeadline')

    def test_selected_total_lifetime_never_resets_at_handoff(self):
        session=self.open(total_seconds=.5)
        py=Path(sys.executable).resolve();tool=session.tool(session.capture(request(py)))
        process=session.launch(st.LaunchSpec(tool,(str(py),'-c','import time;time.sleep(2)')))
        process.verify_current();time.sleep(.7)
        with self.assertRaises(st.StartupFailure) as caught:process.verify_current()
        self.assertEqual(caught.exception.code,'LifetimeDeadline')
        self.assertEqual(caught.exception.observation.cleanup,'STOPPED')

    def test_existing_foreign_target_bytes_unchanged(self):
        source=self.root/'source';source.write_bytes(b'new TEST source')
        session=self.open();lease=session.capture(request(source))
        prior=self.root/'workspace/foreign';prior.write_bytes(b'prior foreign bytes')
        with self.assertRaises(st.StartupFailure) as caught:session.prepare(lease,'foreign')
        self.assertEqual(prior.read_bytes(),b'prior foreign bytes')
        self.assertEqual(caught.exception.code,'NoClobber')

    def test_forked_handle_refuses_without_issuing_io(self):
        source=self.root/'source';source.write_bytes(b'data')
        session=self.open();lease=session.capture(request(source))
        read,write=os.pipe()
        pid=os.fork()
        if pid==0:
            os.close(read)
            try:
                session.prepare(lease,'forked');os.write(write,b'accepted')
            except st.StartupFailure as error:os.write(write,error.code.encode())
            finally:os._exit(0)
        os.close(write);raw=os.read(read,64);os.close(read);os.waitpid(pid,0)
        self.assertEqual(raw,b'InvalidLease')
        self.assertFalse((self.root/'workspace/forked').exists())
        self.assertEqual(session.prepare(lease,'parent').observation().size,4)

    def test_result_facts_are_immutable_and_not_lease_constructors(self):
        source=self.root/'source';source.write_bytes(b'data')
        session=self.open();lease=session.capture(request(source))
        facts=lease.observation()
        with self.assertRaises(dataclasses.FrozenInstanceError):facts.size=999
        self.assertEqual(facts.size,4)
        with self.assertRaises(st.StartupFailure) as caught:session.prepare(facts,'forged')
        self.assertEqual(caught.exception.code,'InvalidLease')



class LiveSourceTests(ManagedCase):
    def test_idle_resource_change_refuses_current_identity(self):
        script=self.root/'child.py';script.write_text('import time;time.sleep(2)\n')
        session=self.open(total_seconds=3)
        lease=session.capture(request(script));py=Path(sys.executable).resolve()
        tool=session.tool(session.capture(request(py)))
        process=session.launch(st.LaunchSpec(tool,(str(py),'-B',st.ResourceArgument('',lease,''))))
        process.verify_current()
        script.write_text('changed after launch\n')
        time.sleep(.05)
        with self.assertRaises(st.StartupFailure) as caught:process.verify_current()
        self.assertEqual(caught.exception.code,'SourceChanged')

    def test_closed_foreign_endpoint_sends_zero_bytes(self):
        p=subprocess.run([sys.executable,'-B',str(FACADE),'managed-fixture','foreign-endpoint'],
                         capture_output=True,timeout=6)
        import json
        value=json.loads(p.stdout)
        self.assertEqual(value['foreign_bytes'],0)
        self.assertEqual(value['error'],'ForeignPeer')
        self.assertEqual(p.returncode,1)


if __name__=='__main__':
    unittest.main()
