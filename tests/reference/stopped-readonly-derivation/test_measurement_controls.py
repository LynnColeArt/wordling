"""Finite causal resource and live-I2 controls; no sampler hooks/private state."""
import dataclasses
import errno
import json
import os
from pathlib import Path
import signal
import sys
import tempfile
import time
import unittest
from test_derivation import st,request

def fields(pid):return (Path('/proc')/str(pid)/'stat').read_text().rsplit(')',1)[1].split()
def wait_for(predicate,seconds=2):
 end=time.monotonic()+seconds
 while time.monotonic()<end:
  if predicate():return
  time.sleep(.0005)
 raise AssertionError('finite causal fixture window not established')
def save(test,result,journal):
 if output:=os.environ.get('MEASUREMENT_RESULTS'):
  folder=Path(output);folder.mkdir(parents=True,exist_ok=True)
  (folder/(test+'.json')).write_text(json.dumps(dict(result=result,journal=journal),indent=2)+'\n')

class ResourcePriorityTests(unittest.TestCase):
 def case(self,dimension):
  with tempfile.TemporaryDirectory(prefix='measurement-priority-TEST-') as tmp:
   root=Path(tmp);session=None;worker_fd=None;stopped=False;opened=[];facts={}
   try:
    now=time.monotonic();limits={'rss_bytes':96*1024*1024} if dimension=='rss' else {'processes':4} if dimension=='process' else {'fds':32}
    session=st.open_session(st.NewWorkspace(str(root/'work')),st.StreamPolicy(),st.ManagedPolicy(),envelope=st.SharedEnvelopePolicy(now,now+10,measurement_completion='bounded-original-v2',**limits))
    python=Path(sys.executable).resolve();tool=session.tool(session.capture(request(python)))
    body='import pathlib,sys,time,ctypes,os\nroot=pathlib.Path(sys.argv[1])\nwhile not (root/"release").exists():time.sleep(.0005)\n'
    if dimension=='rss':body+='payload=bytearray(96*1024*1024)\n'
    if dimension=='process':body+='for _ in range(2):\n if os.fork()==0:time.sleep(2);os._exit(0)\n'
    body+='assert ctypes.CDLL(None).prctl(4,0,0,0,0)==0\n(root/"ready").touch()\ntime.sleep(2)\n'
    process=session.launch(st.LaunchSpec(tool,(str(python),'-c',body,str(root))))
    identity=process.verify_current();child=fields(identity.pid);worker=int(child[1]);before=fields(worker)
    self.assertEqual(int(child[19]),identity.startticks);self.assertEqual(int(before[1]),os.getpid())
    worker_fd=os.pidfd_open(worker);after=fields(worker);self.assertEqual(before[19],after[19]);self.assertEqual(int(after[1]),os.getpid())
    facts['ownership']={'child_pid':identity.pid,'child_birth':identity.startticks,'worker_pid':worker,'worker_before':before,'worker_after':after,'coordinator_pid':os.getpid()}
    signal.pidfd_send_signal(worker_fd,signal.SIGSTOP);stopped=True;wait_for(lambda:fields(worker)[0]=='T')
    (root/'release').touch();wait_for(lambda:(root/'ready').exists())
    # Actual FD denial and retained birth, never a fabricated census outcome.
    child_before=fields(identity.pid)
    with self.assertRaises(PermissionError) as denied:os.listdir(Path('/proc')/str(identity.pid)/'fd')
    self.assertEqual(denied.exception.errno,errno.EACCES)
    self.assertEqual(int(child_before[19]),identity.startticks)
    facts.update(actual_fd_errno=denied.exception.errno,unobservable_child_stat=child_before)
    if dimension=='fd':
     opened=[os.open('/dev/null',os.O_RDONLY) for _ in range(20)]
     facts['coordinator_fds_before_resume']=len(os.listdir('/proc/self/fd'))-1
    facts['resumed_monotonic']=time.monotonic();signal.pidfd_send_signal(worker_fd,signal.SIGCONT);stopped=False
    with self.assertRaises(st.StartupFailure) as caught:process.finish()
    expected={'rss':'RSSLimit','process':'ProcessLimit','fd':'FDLimit'}[dimension]
    self.assertEqual(caught.exception.code,expected)
    for fd in opened:os.close(fd)
    opened=[]
    outcome=session.close();session=None;facts['outcome']=dataclasses.asdict(outcome)
    self.assertEqual(outcome.first_fault,expected);self.assertEqual(outcome.cleanup,'STOPPED')
    counters=dict(outcome.counters)
    peak,limit={'rss':('peak_rss',96*1024*1024),'process':('peak_processes',4),'fd':('peak_fds',32)}[dimension]
    self.assertGreater(counters[peak],limit)
    journal=[json.loads(row) for row in (root/'work/session.jsonl').read_text().splitlines()]
    self.assertFalse(any(row.get('phase')=='MEASUREMENT_PENDING' for row in journal))
    save(self._testMethodName,facts,journal)
   finally:
    if stopped:signal.pidfd_send_signal(worker_fd,signal.SIGCONT)
    for fd in opened:os.close(fd)
    if session:
     try:session.close()
     except st.StartupFailure:pass
    if worker_fd is not None:os.close(worker_fd)
 def test_simultaneous_rss_violation_wins_before_pending(self):self.case('rss')
 def test_simultaneous_process_violation_wins_before_pending(self):self.case('process')
 def test_known_fd_lower_bound_violation_wins_before_pending(self):self.case('fd')

class LiveI2Tests(unittest.TestCase):
 def case(self,operation):
  with tempfile.TemporaryDirectory(prefix='measurement-I2-TEST-') as tmp:
   root=Path(tmp);session=st.open_session(st.NewWorkspace(str(root/'work')),st.StreamPolicy(),st.ManagedPolicy())
   try:
    python=Path(sys.executable).resolve();tool=session.tool(session.capture(request(python)))
    body='import ctypes,pathlib,sys,time\ntime.sleep(.3)\nassert ctypes.CDLL(None).prctl(4,0,0,0,0)==0\npathlib.Path(sys.argv[1]).touch()\ntime.sleep(2)'
    process=session.launch(st.LaunchSpec(tool,(str(python),'-c',body,str(root/'ready'))))
    wait_for(lambda:(root/'ready').exists())
    with self.assertRaises(st.StartupFailure) as caught:
     if operation=='current':process.verify_current()
     else:process.open_endpoint('endpoint')
    self.assertIn(caught.exception.code,('IdentityUnknown','unknown-identity'))
    outcome=session.close();session=None
    self.assertEqual(outcome.first_fault,'IdentityUnknown');self.assertEqual(outcome.cleanup,'STOPPED')
    journal=[json.loads(row) for row in (root/'work/session.jsonl').read_text().splitlines()]
    self.assertFalse(any(row.get('phase')=='MEASUREMENT_PENDING' for row in journal))
    save(self._testMethodName,dataclasses.asdict(outcome),journal)
   finally:
    if session:
     try:session.close()
     except st.StartupFailure:pass
 def test_live_current_cannot_borrow_nonpublishing_uncertainty(self):self.case('current')
 def test_live_endpoint_cannot_borrow_nonpublishing_uncertainty(self):self.case('endpoint')

class PendingRefusalTests(unittest.TestCase):
 from test_derivation import DerivationTests as _helpers
 setUp=_helpers.setUp
 tearDown=_helpers.tearDown
 prepare=_helpers.prepare
 def case(self,case):
  limits={'journal_events':8} if case=='journal' else {'output_bytes':64} if case=='output' else {}
  session=self.prepare(measurement_completion='bounded-original-v2',**limits)
  body='''import ctypes,pathlib,sys,time,os,json
journal=pathlib.Path(sys.argv[1])
def records():return [json.loads(row) for row in journal.read_text().splitlines()]
end=time.monotonic()+2
while not any(row.get('phase')=='PASSIVE_FINISH_INTENT' for row in records()):
 if time.monotonic()>=end:sys.exit(93)
 time.sleep(.0001)
assert ctypes.CDLL(None).prctl(4,0,0,0,0)==0
while not any(row.get('phase')=='MEASUREMENT_PENDING' for row in records()):
 if time.monotonic()>=end:sys.exit(94)
 time.sleep(.0001)
'''
  if case=='late':body+='pending=next(row for row in records() if row.get("phase")=="MEASUREMENT_PENDING")\nwhile time.monotonic()<pending["end"]-.002:time.sleep(.0001)\nassert ctypes.CDLL(None).prctl(4,1,0,0,0)==0\ntime.sleep(.1)\n'
  elif case=='output':body+='os.write(1,b"x"*256)\ntime.sleep(2)\n'
  else:body+='time.sleep(2)\n'
  process=session.launch(st.LaunchSpec(self.tool,(self.py,'-c',body,str(self.root/'work/session.jsonl'))),resources=(self.working,))
  with self.assertRaises(st.StartupFailure) as caught:process.finish(timeout=.050 if case=='late' else 5)
  expected={'persistent':'MeasurementUnknown','late':'LifetimeDeadline','output':'OutputLimit','journal':'JournalPersistence'}[case]
  self.assertEqual(caught.exception.code,expected)
  # Later observations/opaque inputs cannot repair the already latched history.
  with self.assertRaises(st.StartupFailure) as later:session.usage()
  self.assertEqual(later.exception.code,expected)
  outcome=session.close();self.s=None
  self.assertEqual(outcome.first_fault,expected);self.assertEqual(outcome.cleanup,'STOPPED')
  events=[json.loads(row) for row in (self.root/'work/session.jsonl').read_text().splitlines()]
  self.assertFalse(any(row.get('phase')=='MEASUREMENT_COMPLETED' for row in events))
  pending=[row for row in events if row.get('phase')=='MEASUREMENT_PENDING']
  incomplete=[row for row in events if row.get('phase')=='MEASUREMENT_INCOMPLETE']
  if case=='journal':
   self.assertFalse(pending);self.assertFalse(caught.exception.observation.journal_durable)
  else:
   self.assertEqual(len(pending),1);self.assertEqual(len(incomplete),1)
   row=incomplete[0];self.assertEqual(row['mode'],'bounded-original-v2');self.assertEqual(row['window'],.100)
   if case=='persistent':self.assertIn(row['attempts'],(2,3));self.assertLessEqual(row['attempts'],3)
   elif case=='output':
    self.assertLess(row['attempts'],3);self.assertGreater(dict(outcome.counters)['output_bytes'],64)
   else:
    self.assertTrue(row['census_complete'],row);self.assertGreater(row['attempts'],1)
    self.assertGreater(row['observed_monotonic'],row['end']);self.assertLess(row['end']-row['origin'],.100)
  self.assertGreaterEqual(dict(outcome.counters)['lost_response_bytes'],65796)
  save(self._testMethodName,dataclasses.asdict(outcome),events)
 def test_persistent_unobservable_exhausts_one_finite_transaction(self):self.case('persistent')
 def test_accessible_census_returning_after_earlier_finish_clock_refuses(self):self.case('late')
 def test_pending_stream_work_limit_wins_before_three_attempts(self):self.case('output')
 def test_pending_journal_capacity_refuses_without_growing_budget(self):self.case('journal')

class DescendantRefusalTests(unittest.TestCase):
 def test_unknown_descendant_cannot_borrow_original_window(self):
  from test_measurement_completion import LiveRefusalTests
  fixture=LiveRefusalTests('test_omitted_and_explicit_strict_remain_fail_first')
  body='import ctypes,time,os\ntime.sleep(.2)\nif os.fork()==0:\n assert ctypes.CDLL(None).prctl(4,0,0,0,0)==0\n time.sleep(2);os._exit(0)\ntime.sleep(2)'
  error,outcome,events=fixture.run_original('bounded-original-v2',body)
  self.assertEqual(error,'MeasurementUnknown');self.assertEqual(outcome['first_fault'],error)
  self.assertFalse(any(row.get('phase')=='MEASUREMENT_PENDING' for row in events))
  detail=next(row['detail'] for row in events if row.get('phase')=='MEASUREMENT_UNAVAILABLE')
  original=next(row['pid'] for row in events if row.get('phase')=='OWNED')
  self.assertNotEqual(detail['pid'],original);self.assertEqual(detail['errno'],13)
  save(self._testMethodName,outcome,events)
