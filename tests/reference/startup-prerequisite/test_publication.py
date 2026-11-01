"""Public OS backpressure/final-publication falsifiers; no source/global patches."""
from pathlib import Path
import ctypes
import dataclasses
import fcntl
import hashlib
import importlib.util
import json
import os
import signal
import struct
import sys
import tempfile
import time
import unittest

ROOT=Path(__file__).resolve().parents[3]
FACADE=Path(os.environ.get('STARTUP_FAMILY_UNDER_TEST',str(ROOT/'scripts/reference/startup_transport.py')))
spec=importlib.util.spec_from_file_location('publication_acceptance',FACADE)
st=importlib.util.module_from_spec(spec);spec.loader.exec_module(st)


def request(path):
    digest=hashlib.sha256()
    with path.open('rb') as source:
        while raw:=source.read(65536):digest.update(raw)
    return st.SourceRequest(str(path),path.stat().st_size,digest.hexdigest())


def pipe_observation(fd):
    """Copy an owned pipe's frame header with tee; never consume the source."""
    size=struct.unpack('i',fcntl.ioctl(fd,0x541B,struct.pack('i',0)))[0]  # FIONREAD
    header=None
    if size>=4:
        read,write=os.pipe2(os.O_CLOEXEC|os.O_NONBLOCK)
        try:
            libc=ctypes.CDLL(None,use_errno=True)
            libc.tee.argtypes=(ctypes.c_int,ctypes.c_int,ctypes.c_size_t,ctypes.c_uint)
            libc.tee.restype=ctypes.c_ssize_t
            if libc.tee(fd,write,4,2)==4:
                header=struct.unpack('!I',os.read(read,4))[0]+4
        finally:os.close(read);os.close(write)
    return dict(queued_bytes=size,first_frame_bytes=header,
                partial_frame=header is not None and size<header,
                complete_first_frame=header is not None and size>=header)


def run_case(padding=12000,pressure='process',stage='launch',small=True):
    with tempfile.TemporaryDirectory(prefix='publication-TEST-') as temporary:
        root=Path(temporary);actor=root/'actor.py'
        prelude="""from pathlib import Path
import os,sys,time,json,socket
r=Path(sys.argv[1])
"""
        if stage=='ready':
            prelude+="""s=socket.socket(socket.AF_UNIX);s.bind('endpoint');s.listen(1)
c,_=s.accept();assert c.recv(64)==b'ping'
(r/'request-seen').touch()
while not (r/'reply-go').exists():time.sleep(.001)
c.sendall(b'ready')
"""
        prelude+="""(r/'actor-ready').touch()
while not (r/'pressure-go').exists():time.sleep(.001)
(r/'pressure-started').touch()
"""
        bodies={
            'process':"""children=[]
for _ in range(2):
 p=os.fork()
 if p==0:time.sleep(.22);os._exit(0)
 children.append(p)
(r/'members').write_text(json.dumps(dict(leader=os.getpid(),children=children)))
for p in children:os.waitpid(p,0)
""",
            'stream':"os.write(1,b'x'*1500000)\n",
            'rss':"raw=b'R'*(96*1024*1024);time.sleep(.22);del raw\n",
            'identity':"os.execve(sys.executable,(sys.executable,'-c','import time;time.sleep(.7)'),{})\n",
            'none':"time.sleep(.22)\n",
        }
        actor.write_text(prelude+bodies.get(pressure,bodies['none'])+"(r/'pressure-done').touch();time.sleep(.65)\n")
        coordinator=os.fork()
        if coordinator==0:
            session=None;result=dict(padding=padding,pressure=pressure,stage=stage)
            try:
                stream=st.StreamPolicy.test_v1()
                policy=st.ManagedPolicy(total_seconds=.2 if pressure=='lifetime' else 3,
                    startup_seconds=.1 if pressure=='startup' else 15,
                    readiness_seconds=2,processes=4 if pressure=='process' else 8,
                    rss_bytes=100*1024*1024 if pressure=='rss' else 268435456)
                session=st.open_session(st.NewWorkspace(str(root/'work')),stream,policy)
                script=session.capture(request(actor));python=Path(sys.executable).resolve()
                tool=session.tool(session.capture(request(python)))
                (root/'setup-ready').touch()
                while not (root/'release').exists():time.sleep(.001)
                process=session.launch(st.LaunchSpec(tool,(str(python),'-B',
                    st.ResourceArgument('',script,''),str(root),'x'*padding)))
                result['launch_returned']=True
                if stage=='ready':
                    channel=process.open_endpoint('endpoint')
                    result['ready']=dataclasses.asdict(channel.exchange(b'ping',b'ready',
                        .15 if pressure=='readiness' else 1))
                    channel.close()
                result['finish']=dataclasses.asdict(process.finish(2))
            except st.StartupFailure as error:
                result['error']=error.code;result['partial']=dataclasses.asdict(error.observation)
                try:
                    session.capture(request(actor));result['after_fault_accepted']=True
                except st.StartupFailure as later:result['after_fault_error']=later.code
            except BaseException as error:
                result['unexpected']=repr(error)
            finally:
                if session:
                    try:result['outcome']=dataclasses.asdict(session.close())
                    except BaseException as error:result['close_error']=repr(error)
                (root/'result').write_text(json.dumps(result))
                os._exit(0)
        held=False;pipe_reads=[];started=time.monotonic();watch=[]
        def wait(predicate,seconds=3):
            until=time.monotonic()+seconds
            while time.monotonic()<until:
                if predicate():return
                time.sleep(.001)
            raise AssertionError('fixture wait timeout')
        try:
            wait(lambda:(root/'setup-ready').exists())
            pipes=[]
            for entry in Path('/proc',str(coordinator),'fd').iterdir():
                if int(entry.name)<=2:continue
                try:name=os.readlink(entry)
                except FileNotFoundError:continue
                if not name.startswith('pipe:'):continue
                fd=os.open(entry,os.O_RDONLY|os.O_NONBLOCK);pipe_reads.append(fd)
                size=fcntl.fcntl(fd,fcntl.F_GETPIPE_SZ)
                if small:fcntl.fcntl(fd,fcntl.F_SETPIPE_SZ,4096)
                pipes.append(dict(fd=int(entry.name),before=size,after=fcntl.fcntl(fd,fcntl.F_GETPIPE_SZ)))
            assert len(pipes)==2,pipes
            (root/'release').touch()
            if stage=='ready':
                wait(lambda:(root/'request-seen').exists())
            else:
                wait(lambda:(root/'work/session.jsonl').exists() and
                     'SPAWN_INTENT' in (root/'work/session.jsonl').read_text())
            os.kill(coordinator,signal.SIGSTOP);held=True
            if stage=='ready':(root/'reply-go').touch()
            wait(lambda:(root/'actor-ready').exists(),.7)
            observed=[]
            # Both owned pipes are inspected; only the response pipe contains
            # a provisional frame after the request has been consumed.
            until=time.monotonic()+.15
            while time.monotonic()<until:
                observed=[pipe_observation(fd) for fd in pipe_reads]
                if any(x['queued_bytes'] for x in observed):break
                time.sleep(.001)
            (root/'pressure-go').touch();pressure_start=time.monotonic()
            if pressure=='source':actor.write_text(actor.read_text()+'# actual source drift\n')
            if pressure=='parent':
                os.kill(coordinator,signal.SIGKILL);held=False
                os.waitpid(coordinator,0)
            while time.monotonic()-pressure_start<.5:
                if (root/'members').exists():
                    members=json.loads((root/'members').read_text())
                    live=[]
                    for pid in [members['leader'],*members['children']]:
                        try:
                            fields=Path('/proc',str(pid),'stat').read_text().rsplit(')',1)[1].split()
                            if fields[0]!='Z':live.append(pid)
                        except FileNotFoundError:pass
                    if len(live)==3:watch.append(time.monotonic())
                time.sleep(.01)
            if held:
                os.kill(coordinator,signal.SIGCONT);held=False
                wait(lambda:(root/'result').exists(),4)
                os.waitpid(coordinator,0)
                result=json.loads((root/'result').read_text())
            else:result=dict(parent_killed=True)
            journal=[json.loads(x) for x in (root/'work/session.jsonl').read_text().splitlines()]
            observed_pids=[x['pid'] for x in journal if x['phase']=='SPAWNED_UNBOUND']
            still_live=[]
            for pid in observed_pids:
                try:
                    state=Path('/proc',str(pid),'stat').read_text().rsplit(')',1)[1].split()[0]
                    if state!='Z':still_live.append(pid)
                except FileNotFoundError:pass
            result.update(journal=journal,observed_direct_pids=observed_pids,
                          observed_direct_still_live=still_live,
                          pipe_sizes=pipes,queue=observed,live_excess_samples=len(watch),
                          journal_faults=[x['code'] for x in journal if x['phase']=='FAULTED'],
                          elapsed=time.monotonic()-started,source_frozen_sha256=request(actor).sha256)
            destination=os.environ.get('STARTUP_PUBLICATION_RESULTS')
            if destination:
                output=Path(destination);output.mkdir(parents=True,exist_ok=True)
                label=str(padding)+'-'+pressure+'-'+stage+('-4k' if small else '-default')
                (output/(label+'.json')).write_text(json.dumps(result,indent=2)+'\n')
            return result
        finally:
            for fd in pipe_reads:os.close(fd)
            if held:os.kill(coordinator,signal.SIGCONT)
            try:
                pid,_=os.waitpid(coordinator,os.WNOHANG)
                if not pid:
                    os.kill(coordinator,signal.SIGKILL);os.waitpid(coordinator,0)
            except ChildProcessError:pass


class PublicationTests(unittest.TestCase):
    def refused(self,result,code,authority='launch_returned'):
        self.assertNotIn('unexpected',result,result)
        self.assertIn(code,result['journal_faults'],result)
        self.assertFalse(result.get(authority),result)
        self.assertIn(result.get('error'),('ControlLost','CleanupUnknown',code),result)
        # A truncated/incomplete transaction must not become a decoded result.
        self.assertNotIn('finish',result,result)
        self.assertFalse(result.get('after_fault_accepted'),result)
        self.assertEqual(result['observed_direct_still_live'],[],result)
        return result

    def test_partial_large_response_process_pressure(self):
        result=self.refused(run_case(),'ProcessLimit')
        self.assertTrue(any(x['partial_frame'] for x in result['queue']),result)

    def test_fully_queued_provisional_before_commit_process_pressure(self):
        result=self.refused(run_case(padding=3000),'ProcessLimit')
        self.assertTrue(any(x['complete_first_frame'] for x in result['queue']),result)

    def test_small_pipe_small_response_process_control(self):
        self.refused(run_case(padding=0),'ProcessLimit')

    def test_default_pipe_control_still_detects_process_pressure(self):
        result=run_case(small=False)
        self.assertIn('ProcessLimit',result['journal_faults'],result)
        self.assertNotIn('finish',result,result)

    def test_partial_response_stream_pressure(self):
        self.refused(run_case(pressure='stream'),'OutputLimit')

    def test_partial_response_real_rss_pressure(self):
        self.refused(run_case(pressure='rss'),'RSSLimit')

    def test_partial_response_selected_lifetime(self):
        self.refused(run_case(pressure='lifetime'),'LifetimeDeadline')

    def test_partial_response_selected_startup_clock(self):
        self.refused(run_case(pressure='startup'),'StartupDeadline')

    def test_ready_publication_selected_clock(self):
        result=self.refused(run_case(pressure='readiness',stage='ready'),'ReadinessDeadline','ready')
        self.assertTrue(result.get('launch_returned'),result)

    def test_ready_publication_live_identity(self):
        self.refused(run_case(pressure='identity',stage='ready'),'IdentityChanged','ready')

    def test_response_publication_source_change(self):
        self.refused(run_case(pressure='source'),'SourceChanged')

    def test_parent_loss_while_response_blocked(self):
        result=run_case(pressure='parent')
        self.assertTrue(result['parent_killed'],result)
        self.assertIn('ParentLost',result['journal_faults'],result)

    def test_large_legal_backpressure_without_fault_remains_positive(self):
        result=run_case(pressure='none')
        self.assertNotIn('error',result,result)
        self.assertEqual(result['finish']['exit_code'],0,result)
        self.assertIsNone(result['outcome']['first_fault'],result)


if __name__=='__main__':
    unittest.main()
