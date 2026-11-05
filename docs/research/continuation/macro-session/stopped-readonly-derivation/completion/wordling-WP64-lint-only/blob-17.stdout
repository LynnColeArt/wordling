"""Real owned 4KiB backpressure on helper capabilities and artifact bytes."""
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
spec=importlib.util.spec_from_file_location('derive_publication',FACADE);st=importlib.util.module_from_spec(spec);spec.loader.exec_module(st)
def request(path):
 raw=path.read_bytes();return st.SourceRequest(str(path),len(raw),hashlib.sha256(raw).hexdigest())
def queue(fd):
 n=struct.unpack('i',fcntl.ioctl(fd,0x541B,struct.pack('i',0)))[0];header=None
 if n>=4:
  a,b=os.pipe2(os.O_CLOEXEC|os.O_NONBLOCK)
  try:
   lib=ctypes.CDLL(None,use_errno=True);lib.tee.argtypes=(ctypes.c_int,ctypes.c_int,ctypes.c_size_t,ctypes.c_uint);lib.tee.restype=ctypes.c_ssize_t
   if lib.tee(fd,b,4,2)==4:header=struct.unpack('!I',os.read(a,4))[0]+4
  finally:os.close(a);os.close(b)
 return dict(queued=n,first_frame=header)
def run_case(stage='derive',fault='output',padding=12000,maximum=16384):
 with tempfile.TemporaryDirectory(prefix='derive-publish-TEST-') as temporary:
  root=Path(temporary);coordinator=os.fork()
  if coordinator==0:
   session=None;result={}
   try:
    now=time.monotonic();end=now+(6 if fault=='deadline' else 12)
    (root/'absolute-end').write_text(str(end))
    session=st.open_session(st.NewWorkspace(str(root/'work')),st.StreamPolicy(),st.ManagedPolicy(),envelope=st.SharedEnvelopePolicy(origin=now,end=end))
    source=root/'input';source.write_bytes(b'own TEST');working=session.prepare(session.capture(request(source)),'working')
    python=Path(sys.executable).resolve();tool=session.tool(session.capture(request(python)))
    original=session.launch(st.LaunchSpec(tool,(str(python),'-c','import time;time.sleep(.2)')),resources=(working,));original.finish()
    working=session.snapshot(working).successor;sealed=session.seal_stopped(working)
    body='import pathlib,sys,time;time.sleep(.15);pathlib.Path(sys.argv[2]).write_bytes(b"Q"*65536);time.sleep(.1)'
    if fault=='deadline':body='import pathlib,sys,time\nwhile time.monotonic()<'+repr(end-.9)+':time.sleep(.01)\npathlib.Path(sys.argv[2]).write_bytes(b"Q"*65536);time.sleep(.05)'
    job=st.DerivationSpec(tool,(str(python),'-c',body,st.ResourceArgument('',sealed,''),st.OutputArgument(0),'x'*padding),(st.OutputSpec('result',65536),),budget=st.JobBudget(seconds=15 if fault=='deadline' else 3))
    if stage=='chunk':batch=session.derive_readonly((sealed,),job)
    (root/'setup-ready').touch()
    while not (root/'release').exists():time.sleep(.001)
    if stage=='derive':
     batch=session.derive_readonly((sealed,),job);result['authority_accepted']=True
    else:
     chunk=session.read_chunk(batch.artifacts[0],0,maximum);result['authority_accepted']=True
     result['chunk_length']=len(chunk.data)
   except st.StartupFailure as error:
    result['error']=error.code;result['partial']=dataclasses.asdict(error.observation)
    try:session.usage();result['later_accepted']=True
    except st.StartupFailure as again:result['later_error']=again.code
   except BaseException as error:result['unexpected']=repr(error)
   finally:
    if session:
     try:result['outcome']=dataclasses.asdict(session.close())
     except BaseException as error:result['close_error']=repr(error)
    (root/'result.json').write_text(json.dumps(result));os._exit(0)
  held=False;readers=[];started=time.monotonic()
  def wait(predicate,seconds=7):
   end=time.monotonic()+seconds
   while time.monotonic()<end:
    if predicate():return
    time.sleep(.001)
   raise AssertionError('bounded publication fixture timeout')
  try:
   wait(lambda:(root/'setup-ready').exists())
   sizes=[]
   for entry in Path('/proc',str(coordinator),'fd').iterdir():
    if int(entry.name)<=2:continue
    try:name=os.readlink(entry)
    except FileNotFoundError:continue
    if not name.startswith('pipe:'):continue
    fd=os.open(entry,os.O_RDONLY|os.O_NONBLOCK);readers.append(fd);fcntl.fcntl(fd,fcntl.F_SETPIPE_SZ,4096);sizes.append(fcntl.fcntl(fd,fcntl.F_GETPIPE_SZ))
   assert len(readers)==2
   (root/'release').touch();phase='DERIVE_COMMITTED' if stage=='derive' else 'CHUNK_INTENT'
   wait(lambda:phase in (root/'work/session.jsonl').read_text())
   os.kill(coordinator,signal.SIGSTOP);held=True;stopped_at=time.monotonic()
   until=time.monotonic()+.2;frames=[]
   while time.monotonic()<until:
    frames=[queue(fd) for fd in readers]
    if max(x['queued'] for x in frames)>0:break
    time.sleep(.001)
   if fault=='output':
    path=root/'work/result';path.chmod(0o600);path.write_bytes(b'genuine changed output')
   if fault=='input':
    path=root/'work/working';path.chmod(0o600);path.write_bytes(b'genuine changed input')
   if fault=='parent':os.kill(coordinator,signal.SIGKILL);held=False;os.waitpid(coordinator,0)
   hold_started=time.monotonic()
   if fault=='deadline':
    absolute_end=float((root/'absolute-end').read_text())
    while time.monotonic()<absolute_end+.1:time.sleep(.001)
   else:time.sleep(.6 if fault!='none' else .25)
   resumed_at=time.monotonic()
   if fault=='parent':result=dict(parent_killed=True)
   else:
    os.kill(coordinator,signal.SIGCONT);held=False;wait(lambda:(root/'result.json').exists());os.waitpid(coordinator,0)
    result=json.loads((root/'result.json').read_text())
   journal=[json.loads(line) for line in (root/'work/session.jsonl').read_text().splitlines()]
   result.update(stage=stage,fault=fault,padding=padding,maximum=maximum,frames=frames,pipe_sizes=sizes,journal=journal,
                 absolute_end=float((root/'absolute-end').read_text()),stopped_monotonic=stopped_at,hold_started=hold_started,resumed_monotonic=resumed_at,
                 faults=[x for x in journal if x['phase']=='FAULTED'],elapsed=time.monotonic()-started)
   output=os.environ.get('DERIVATION_PUBLICATION_RESULTS')
   if output:
    dest=Path(output);dest.mkdir(parents=True,exist_ok=True)
    (dest/(stage+'-'+fault+'-'+str(padding)+'-'+str(maximum)+'.json')).write_text(json.dumps(result,indent=2)+'\n')
   return result
  finally:
   for fd in readers:os.close(fd)
   if held:os.kill(coordinator,signal.SIGCONT)
   try:
    pid,_=os.waitpid(coordinator,os.WNOHANG)
    if not pid:os.kill(coordinator,signal.SIGKILL);os.waitpid(coordinator,0)
   except ChildProcessError:pass
class PublicationTests(unittest.TestCase):
 def refusal(self,r,cause):
  self.assertNotIn('unexpected',r,r);self.assertFalse(r.get('authority_accepted'),r);self.assertFalse(r.get('later_accepted'),r)
  self.assertIn(cause,[x['code'] for x in r['faults']],r)
  self.assertTrue(any(x['queued'] and x['first_frame'] for x in r['frames']),r)
 def test_derive_partial_output_drift(self):self.refusal(run_case(),'SourceChanged')
 def test_derive_partial_input_drift(self):self.refusal(run_case(fault='input'),'SourceChanged')
 def test_derive_clock_during_publication(self):
  r=run_case(fault='deadline');self.refusal(r,'EnvelopeDeadline')
  self.assertLess(r['stopped_monotonic'],r['absolute_end']);self.assertGreater(r['resumed_monotonic'],r['absolute_end'])
 def test_chunk_partial_output_drift(self):self.refusal(run_case(stage='chunk'),'SourceChanged')
 def test_chunk_full_provisional_without_commit(self):
  r=run_case(stage='chunk',maximum=512);self.refusal(r,'SourceChanged')
  self.assertTrue(any(x['first_frame'] and x['queued']>=x['first_frame'] for x in r['frames']),r)
 def test_parent_loss_after_helper_before_capability(self):
  r=run_case(fault='parent');self.assertTrue(r['parent_killed']);self.assertTrue(set(x['code'] for x in r['faults'])&{'ParentLost','ControlLost'})
 def test_derive_bounded_stall_positive(self):
  r=run_case(fault='none');self.assertTrue(r.get('authority_accepted'),r);self.assertFalse(r['faults'],r)
 def test_chunk_bounded_stall_positive(self):
  r=run_case(stage='chunk',fault='none');self.assertEqual(r.get('chunk_length'),16384,r);self.assertFalse(r['faults'],r)
if __name__=='__main__':unittest.main()
