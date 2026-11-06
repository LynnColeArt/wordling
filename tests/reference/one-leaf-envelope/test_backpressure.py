"""Real owned 4KiB pipe stalls against public usage, no protocol/client patch."""
import ctypes
import dataclasses
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import struct
import sys
import tempfile
import time
import unittest

ROOT=Path(__file__).resolve().parents[3]
FACADE=Path(os.environ.get('STARTUP_FAMILY_UNDER_TEST',ROOT/'scripts/reference/startup_transport.py'))
spec=importlib.util.spec_from_file_location('envelope_backpressure',FACADE)
st=importlib.util.module_from_spec(spec);spec.loader.exec_module(st)

def request(path):
    raw=path.read_bytes();return st.SourceRequest(str(path),len(raw),hashlib.sha256(raw).hexdigest())

def run_case(pressure='process',padding=12000,small=True):
    with tempfile.TemporaryDirectory(prefix='envelope-pipe-TEST-') as temporary:
        root=Path(temporary);actor=root/'actor.py'
        body="""import os,time,sys
from pathlib import Path
r=Path(sys.argv[1]);(r/'actor-ready').touch()
while not (r/'pressure-go').exists():time.sleep(.001)
"""
        if pressure=='process':body+='children=[]\nfor _ in range(2):\n p=os.fork()\n if p==0:time.sleep(.22);os._exit(0)\n children.append(p)\nfor p in children:os.waitpid(p,0)\n'
        else:body+='time.sleep(.2)\n'
        body+='time.sleep(1)\n';actor.write_text(body)
        coordinator=os.fork()
        if coordinator==0:
            session=None;result={}
            try:
                now=time.monotonic()
                envelope=st.SharedEnvelopePolicy(origin=now,end=now+(1.2 if pressure=='deadline' else 8),
                    processes=4 if pressure=='process' else 8)
                (root/'absolute-end').write_text(str(envelope.end))
                session=st.open_session(st.NewWorkspace(str(root/'work')),st.StreamPolicy(),
                                       st.ManagedPolicy(),envelope=envelope)
                source=session.capture(request(actor));python=Path(sys.executable).resolve()
                tool=session.tool(session.capture(request(python)))
                process=session.launch(st.LaunchSpec(tool,(str(python),'-B',
                    st.ResourceArgument('',source,''),str(root),'x'*padding)))
                result['launch_returned']=True;(root/'setup-ready').touch()
                while not (root/'release').exists():time.sleep(.001)
                result['usage']=dataclasses.asdict(session.usage())
                result['finish']=dataclasses.asdict(process.finish(3))
            except st.StartupFailure as error:
                result['error']=error.code;result['partial']=dataclasses.asdict(error.observation)
                try:session.usage();result['later_accepted']=True
                except st.StartupFailure as again:result['later_error']=again.code
            except BaseException as error:result['unexpected']=repr(error)
            finally:
                if session:
                    try:result['outcome']=dataclasses.asdict(session.close())
                    except BaseException as error:result['close_error']=repr(error)
                (root/'result').write_text(json.dumps(result));os._exit(0)
        held=False;reads=[];queue=[];start=time.monotonic()
        def wait(predicate,seconds=4):
            end=time.monotonic()+seconds
            while time.monotonic()<end:
                if predicate():return
                time.sleep(.001)
            raise AssertionError('bounded fixture wait timeout')
        try:
            wait(lambda:(root/'setup-ready').exists())
            sizes=[]
            for entry in Path('/proc',str(coordinator),'fd').iterdir():
                if int(entry.name)<=2:continue
                try:target=os.readlink(entry)
                except FileNotFoundError:continue
                if not target.startswith('pipe:'):continue
                fd=os.open(entry,os.O_RDONLY|os.O_NONBLOCK);reads.append(fd)
                if small:fcntl.fcntl(fd,fcntl.F_SETPIPE_SZ,4096)
                sizes.append(fcntl.fcntl(fd,fcntl.F_GETPIPE_SZ))
            assert len(reads)==2
            (root/'release').touch()
            wait(lambda:'USAGE_INTENT' in (root/'work/session.jsonl').read_text())
            os.kill(coordinator,signal.SIGSTOP);held=True
            # Allow the real provisional response to fill its owned pipe.
            end=time.monotonic()+.65
            while time.monotonic()<end:
                queue=[struct.unpack('i',fcntl.ioctl(fd,0x541B,struct.pack('i',0)))[0] for fd in reads]
                if max(queue)>=4096:break
                time.sleep(.001)
            frames=[]
            for fd,n in zip(reads,queue):
                header=None
                if n>=4:
                    a,b=os.pipe2(os.O_CLOEXEC|os.O_NONBLOCK)
                    try:
                        libc=ctypes.CDLL(None,use_errno=True);libc.tee.argtypes=(ctypes.c_int,ctypes.c_int,ctypes.c_size_t,ctypes.c_uint);libc.tee.restype=ctypes.c_ssize_t
                        if libc.tee(fd,b,4,2)==4:header=struct.unpack('!I',os.read(a,4))[0]+4
                    finally:os.close(a);os.close(b)
                frames.append(dict(queued=n,first_frame=header))
            (root/'pressure-go').touch()
            if pressure=='source':actor.write_text(body+'# genuine changed source\n')
            duration=max(.5,float((root/'absolute-end').read_text())-time.monotonic()+.1) if pressure=='deadline' else .5
            if pressure=='parent':
                os.kill(coordinator,signal.SIGKILL);held=False;os.waitpid(coordinator,0)
            time.sleep(duration)
            if pressure=='parent':result=dict(parent_killed=True)
            else:
                os.kill(coordinator,signal.SIGCONT);held=False
                wait(lambda:(root/'result').exists());os.waitpid(coordinator,0)
                result=json.loads((root/'result').read_text())
            rows=[json.loads(x) for x in (root/'work/session.jsonl').read_text().splitlines()]
            faults=[x for x in rows if x['phase']=='FAULTED']
            live=[]
            for row in rows:
                if row['phase']!='SPAWNED_UNBOUND':continue
                try:state=Path('/proc',str(row['pid']),'stat').read_text().rsplit(')',1)[1].split()[0]
                except FileNotFoundError:continue
                if state!='Z':live.append(row['pid'])
            result.update(journal=rows,faults=faults,still_live=live,pipe_sizes=sizes,
                          queued=queue,frames=frames,padding=padding,pressure=pressure,elapsed=time.monotonic()-start)
            output=os.environ.get('ENVELOPE_BACKPRESSURE_RESULTS')
            if output:
                dest=Path(output);dest.mkdir(parents=True,exist_ok=True)
                (dest/(pressure+'-'+str(padding)+('-4k' if small else '-default')+'.json')).write_text(json.dumps(result,indent=2)+'\n')
            return result
        finally:
            for fd in reads:os.close(fd)
            if held:os.kill(coordinator,signal.SIGCONT)
            try:
                pid,_=os.waitpid(coordinator,os.WNOHANG)
                if not pid:os.kill(coordinator,signal.SIGKILL);os.waitpid(coordinator,0)
            except ChildProcessError:pass

class BackpressureTests(unittest.TestCase):
    def refusal(self,result,cause):
        self.assertNotIn('unexpected',result,result)
        self.assertTrue(result.get('launch_returned'),result)
        self.assertIn(cause,[x['code'] for x in result['faults']],result)
        self.assertNotIn('usage',result,result);self.assertNotIn('finish',result,result)
        self.assertFalse(result.get('later_accepted'),result)
        self.assertEqual(result['still_live'],[],result)
        self.assertGreater(result['faults'][0]['lost_response_bytes'],0,result)
    def test_partial_usage_process_pressure(self):
        result=run_case();self.refusal(result,'ProcessLimit')
        self.assertEqual(max(result['queued']),4096,result)
    def test_fully_queued_provisional_usage_no_commit(self):
        result=run_case(padding=1700);self.refusal(result,'ProcessLimit')
        self.assertTrue(any(x['first_frame'] and x['queued']>=x['first_frame'] for x in result['frames']),result)
    def test_parent_loss_during_usage(self):
        result=run_case('parent');self.assertTrue(result['parent_killed'],result)
        self.assertTrue(set(x['code'] for x in result['faults']) & {'ParentLost','ControlLost'},result)
        self.assertEqual(result['still_live'],[],result)
        self.assertGreater(result['faults'][0]['lost_response_bytes'],0,result)
    def test_usage_absolute_clock_during_backpressure(self):self.refusal(run_case('deadline'),'EnvelopeDeadline')
    def test_usage_source_drift_during_backpressure(self):self.refusal(run_case('source'),'SourceChanged')
    def test_bounded_stall_without_fault_is_positive(self):
        result=run_case('none');self.assertIn('usage',result,result);self.assertIn('finish',result,result)
        self.assertFalse(result['faults'],result)
    def test_default_pipe_process_control(self):
        result=run_case(small=False);self.assertIn('ProcessLimit',[x['code'] for x in result['faults']],result)
        self.assertNotIn('finish',result,result)

if __name__=='__main__':unittest.main()
