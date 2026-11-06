"""Four finite real pending transactions interrupted by causal loss/source drift."""
import dataclasses
import json
import os
from pathlib import Path
import select
import signal
import sys
import tempfile
import time
import unittest
from test_derivation import st,request
from test_loss import kernel

def run_pending_loss(which):
 with tempfile.TemporaryDirectory(prefix='pending-loss-TEST-') as tmp:
  root=Path(tmp);coordinator=os.fork()
  if coordinator==0:
   session=None;result={}
   try:
    now=time.monotonic();session=st.open_session(st.NewWorkspace(str(root/'work')),st.StreamPolicy(),st.ManagedPolicy(),envelope=st.SharedEnvelopePolicy(now,now+12,measurement_completion='bounded-original-v2'))
    if which=='control':
     opened=next(json.loads(row)['supervisor'] for row in (root/'work/session.jsonl').read_text().splitlines() if json.loads(row).get('phase')=='OPENED')
     assert kernel(opened)['ppid']==os.getpid()
     worker_pipes=set()
     for entry in Path('/proc',str(opened),'fd').iterdir():
      if int(entry.name)<=2:continue
      try:link=os.readlink(entry)
      except FileNotFoundError:continue
      if link.startswith('pipe:'):worker_pipes.add(link)
     control=[]
     for entry in Path('/proc/self/fd').iterdir():
      if int(entry.name)<=2:continue
      try:link=os.readlink(entry)
      except FileNotFoundError:continue
      if link in worker_pipes:control.append(int(entry.name))
     assert len(control)==2
     def lose_control(signum,frame):
      for fd in control:os.close(fd)
     signal.signal(signal.SIGUSR1,lose_control)
     (root/'control-proof.json').write_text(json.dumps(dict(worker=opened,coordinator=os.getpid(),exact_pipe_intersection_count=len(control))))
    source=root/'input';source.write_bytes(b'authored TEST')
    working=session.prepare(session.capture(request(source)),'working')
    python=Path(sys.executable).resolve();tool=session.tool(session.capture(request(python)))
    body='''import ctypes,pathlib,sys,time,json
root=pathlib.Path(sys.argv[1]);journal=root/'work/session.jsonl'
time.sleep(.3)
assert ctypes.CDLL(None).prctl(4,0,0,0,0)==0
end=time.monotonic()+2
while not any(json.loads(row).get('phase')=='MEASUREMENT_PENDING' for row in journal.read_text().splitlines()):
 if time.monotonic()>=end:sys.exit(93)
 time.sleep(.0001)
(root/'pending-ready').touch()
time.sleep(5)
'''
    process=session.launch(st.LaunchSpec(tool,(str(python),'-c',body,str(root))),resources=(working,))
    process.finish(timeout=5);result['finish_accepted']=True
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
  fds=[];reaped=False
  def wait(predicate,seconds=5):
   end=time.monotonic()+seconds
   while time.monotonic()<end:
    if predicate():return
    time.sleep(.0005)
   raise AssertionError('declared pending-loss window not established')
  try:
   wait(lambda:(root/'pending-ready').exists())
   rows=[json.loads(row) for row in (root/'work/session.jsonl').read_text().splitlines()]
   pending=next(row for row in rows if row.get('phase')=='MEASUREMENT_PENDING')
   worker=next(row['supervisor'] for row in rows if row.get('phase')=='OPENED')
   owned=next(row for row in rows if row.get('phase')=='OWNED');child=owned['pid']
   worker_before=kernel(worker);child_before=kernel(child)
   assert worker_before['ppid']==coordinator and child_before['ppid']==worker
   assert child_before['startticks']==owned['startticks']
   wf=os.pidfd_open(worker);cf=os.pidfd_open(child);pf=os.pidfd_open(coordinator);fds=[wf,cf,pf]
   assert kernel(worker)['startticks']==worker_before['startticks'] and kernel(child)['startticks']==child_before['startticks']
   effect_at=time.monotonic()
   if which=='parent':signal.pidfd_send_signal(pf,signal.SIGKILL);os.waitpid(coordinator,0);reaped=True
   elif which=='worker':signal.pidfd_send_signal(wf,signal.SIGKILL)
   elif which=='control':signal.pidfd_send_signal(pf,signal.SIGUSR1)
   else:(root/'input').write_bytes(b'genuine changed declared source')
   if which!='parent':
    wait(lambda:(root/'result.json').exists());os.waitpid(coordinator,0);reaped=True
    result=json.loads((root/'result.json').read_text())
   else:result={'parent_killed':True}
   fixture_signal=False
   if which=='worker' and not select.select([cf],[],[],0)[0]:
    signal.pidfd_send_signal(cf,signal.SIGTERM);fixture_signal=True
   result.update(which=which,pending=pending,effect_monotonic=effect_at,
    worker_before=worker_before,child_before=child_before,
    worker_pidfd_observed_stopped=bool(select.select([wf],[],[],1.5)[0]),
    child_pidfd_observed_stopped=bool(select.select([cf],[],[],1.5)[0]),
    fixture_child_signal=fixture_signal,child_reaped_by_fixture=False,coordinator_reaped=reaped,
    journal=[json.loads(row) for row in (root/'work/session.jsonl').read_text().splitlines()])
   if which=='control':result['control_proof']=json.loads((root/'control-proof.json').read_text())
   if output:=os.environ.get('MEASUREMENT_RESULTS'):
    folder=Path(output);folder.mkdir(parents=True,exist_ok=True);(folder/('pending-'+which+'.json')).write_text(json.dumps(result,indent=2)+'\n')
   return result
  finally:
   for fd in fds:os.close(fd)
   if not reaped:
    try:
     done,_=os.waitpid(coordinator,os.WNOHANG)
     if not done:os.kill(coordinator,signal.SIGKILL);os.waitpid(coordinator,0)
    except ChildProcessError:pass

class PendingLossTests(unittest.TestCase):
 def case(self,which):
  result=run_pending_loss(which);self.assertNotIn('unexpected',result,result)
  self.assertFalse(result.get('finish_accepted'));self.assertFalse(result.get('later_accepted'))
  self.assertTrue(result['worker_pidfd_observed_stopped'],result);self.assertTrue(result['child_pidfd_observed_stopped'],result)
  self.assertFalse(any(row.get('phase')=='MEASUREMENT_COMPLETED' for row in result['journal']))
  self.assertLess(result['pending']['monotonic'],result['effect_monotonic'])
  if which=='worker':self.assertEqual(result['outcome']['cleanup'],'UNKNOWN')
  elif which=='parent':self.assertIn('ParentLost',[row.get('code') for row in result['journal'] if row.get('phase')=='FAULTED'])
  else:self.assertEqual(result['error'],'ControlLost' if which=='control' else 'SourceChanged')
 def test_parent_loss_during_pending(self):self.case('parent')
 def test_worker_loss_during_pending_stays_unknown(self):self.case('worker')
 def test_control_loss_during_pending(self):self.case('control')
 def test_declared_source_change_during_pending(self):self.case('source')
