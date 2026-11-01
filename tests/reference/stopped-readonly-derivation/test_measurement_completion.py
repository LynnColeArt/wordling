"""Prospective measurement-policy compatibility and live completion controls."""
import dataclasses
import hashlib
import json
import os
import subprocess
import sys
import time
import tempfile
from pathlib import Path
import unittest
from test_derivation import st,FACADE

class PolicyTests(unittest.TestCase):
 def test_selector_is_keyword_only_strict_default(self):
  p=st.SharedEnvelopePolicy(1,2)
  self.assertEqual(p.measurement_completion,'strict')
  self.assertTrue(next(f for f in dataclasses.fields(p) if f.name=='measurement_completion').kw_only)
  for mode in ('bounded-original-v1','bounded-original-v2'):
   self.assertEqual(st.SharedEnvelopePolicy(1,2,measurement_completion=mode).measurement_completion,mode)
 def test_all_numeric_fields_still_validated(self):
  for f in dataclasses.fields(st.SharedEnvelopePolicy):
   if f.name in ('origin','end','measurement_completion'):continue
   for v in (0,True,1.5,None):
    with self.subTest(field=f.name,value=v),self.assertRaises(st.Failure):st.SharedEnvelopePolicy(1,2,**{f.name:v})
 def test_selector_exact_type_and_closed_values(self):
  class S(str):pass
  for value in (None,True,1,'bounded','STRICT',S('strict')):
   with self.subTest(value=value),self.assertRaises(st.Failure):st.SharedEnvelopePolicy(1,2,measurement_completion=value)

 def test_real_new_session_committed_hello_and_usage(self):
  with tempfile.TemporaryDirectory(prefix='measurement-TEST-') as tmp:
   now=time.monotonic()
   session=st.open_session(st.NewWorkspace(str(Path(tmp)/'work')),st.StreamPolicy(),st.ManagedPolicy(),envelope=st.SharedEnvelopePolicy(now,now+10,measurement_completion='bounded-original-v1'))
   try:
    usage=session.usage()
    self.assertGreater(usage.control_wire_bytes,0)
    self.assertGreater(usage.current_fds,0)
   finally:session.close()

 def test_tampered_policy_refused_before_workspace(self):
  with tempfile.TemporaryDirectory(prefix='measurement-local-TEST-') as tmp:
   now=time.monotonic();policy=st.SharedEnvelopePolicy(now,now+10)
   object.__setattr__(policy,'measurement_completion','invalid')
   path=Path(tmp)/'work'
   with self.assertRaises(st.Failure):st.open_session(st.NewWorkspace(str(path)),st.StreamPolicy(),st.ManagedPolicy(),envelope=policy)
   self.assertFalse(path.exists())

class CreationTests(unittest.TestCase):
 def test_real_committed_ack_refusal_keeps_setup_and_charge_facts(self):
  root=Path(__file__).resolve().parents[3]
  files=['startup_transport.py']+['startup_family/'+name for name in ('__init__.py','artifacts.py','engine.py','lifetime.py')]
  base=FACADE.parent
  life=(base/'startup_family/lifetime.py').read_text()
  needle="if self.envelope is not None and self.envelope.measurement_completion!='strict' else {}"
  variants={'missing':(needle,'if False else {}'),
   'mismatch':('dict(measurement_completion=self.envelope.measurement_completion)',"dict(measurement_completion='strict')"),
   'unknown':('dict(measurement_completion=self.envelope.measurement_completion)',"dict(measurement_completion='unsupported')"),
   'wrong-type':('dict(measurement_completion=self.envelope.measurement_completion)',"dict(measurement_completion=True)"),
   'unknown-field':('dict(measurement_completion=self.envelope.measurement_completion)',"dict(measurement_completion=self.envelope.measurement_completion,unexpected=True)"),
   'worker-unsupported':('        self.envelope=envelope\n',"        if envelope is not None and envelope.measurement_completion!='strict':raise engine.Failure('UnsupportedMeasurementMode')\n        self.envelope=envelope\n")}
  for mode in ("bounded-original-v1","bounded-original-v2"):
   for name,(old,new) in variants.items():
    with self.subTest(case=name),tempfile.TemporaryDirectory(prefix='measurement-ack-TEST-') as tmp:
     tmp=Path(tmp);self.assertEqual(life.count(old),1);changed=life.replace(old,new);compile(changed,'lifetime.py','exec')
     for path in files:
      dest=tmp/path;dest.parent.mkdir(parents=True,exist_ok=True)
      dest.write_text(changed if path=='startup_family/lifetime.py' else (base/path).read_text())
     cmd=[sys.executable,'-B',str(Path(__file__).with_name('creation_probe.py')),str(tmp/'startup_transport.py'),str(tmp/'work'),mode]
     result=subprocess.run(cmd,cwd=root,capture_output=True,timeout=8)
     output=os.environ.get('MEASUREMENT_RESULTS')
     if output:
      folder=Path(output)/('ack-'+mode+'-'+name);folder.mkdir(parents=True,exist_ok=True)
      (folder/'stdout').write_bytes(result.stdout);(folder/'stderr').write_bytes(result.stderr)
      (folder/'source.txt').write_text(changed)
      (folder/'command.json').write_text(json.dumps(dict(argv=cmd,exit=result.returncode,source_sha256=hashlib.sha256(changed.encode()).hexdigest())))
     self.assertEqual(result.returncode,0,result.stderr.decode());data=json.loads(result.stdout)
     self.assertFalse(data['accepted'])
     self.assertIn(data['error'],('ControlLost','CleanupUnknown') if name=='worker-unsupported' else ('LaunchUnknown',))
     creation=data['creation'];self.assertTrue(creation['workspace_created']);self.assertTrue(creation['journal_created'])
     self.assertEqual(creation['committed_hello_received'],name!='worker-unsupported')
     if name!='worker-unsupported':
      self.assertGreater(creation['received_wire_bytes'],0);self.assertEqual(creation['received_messages'],2)
     else:
      self.assertIsNone(creation['outstanding_response_bytes']);self.assertEqual(creation['outstanding_response_upper_bound_bytes'],65796)
     self.assertTrue(creation['supervisor_fork_returned'])
     self.assertIsNotNone(creation['supervisor_reap_proof']);self.assertEqual(creation['cleanup'],'STOPPED')
     self.assertEqual(data['partial']['launch_state'],'NOT_ATTEMPTED')
     self.assertIn('OPEN_INTENT',data['journal']);self.assertNotIn('SPAWN_INTENT',data['journal'])

class LiveRefusalTests(unittest.TestCase):
 def run_original(self,selector,body,**limits):
  from test_derivation import request
  with tempfile.TemporaryDirectory(prefix='measurement-live-TEST-') as tmp:
   root=Path(tmp);now=time.monotonic();extra={} if selector=='omitted' else {'measurement_completion':selector}
   session=st.open_session(st.NewWorkspace(str(root/'work')),st.StreamPolicy(),st.ManagedPolicy(),envelope=st.SharedEnvelopePolicy(now,now+8,**extra,**limits))
   error=None;outcome=None
   try:
    python=Path(sys.executable).resolve();tool=session.tool(session.capture(request(python)))
    try:
     process=session.launch(st.LaunchSpec(tool,(str(python),'-c',body)))
     process.finish()
    except st.StartupFailure as failure:error=failure.code
   finally:
    outcome=dataclasses.asdict(session.close())
   journal=(root/'work/session.jsonl').read_text()
   output=os.environ.get('MEASUREMENT_RESULTS')
   if output:
    folder=Path(output)/self._testMethodName;folder.mkdir(parents=True,exist_ok=True)
    (folder/(selector+'.json')).write_text(json.dumps(dict(error=error,outcome=outcome,journal=journal)))
   return error,outcome,[json.loads(line) for line in journal.splitlines()]
 def test_omitted_and_explicit_strict_remain_fail_first(self):
  body='import ctypes,time;time.sleep(.2);assert ctypes.CDLL(None).prctl(4,0,0,0,0)==0;time.sleep(1)'
  for selector in ('omitted','strict'):
   with self.subTest(selector=selector):
    error,outcome,events=self.run_original(selector,body)
    self.assertEqual(error,'MeasurementUnknown');self.assertEqual(outcome['first_fault'],error)
    self.assertFalse(any(row['phase']=='MEASUREMENT_PENDING' for row in events))
    self.assertEqual(outcome['cleanup'],'STOPPED')
 def test_known_rss_violation_precedes_unobservable_fd(self):
  body='import ctypes,time;time.sleep(.2);payload=bytearray(96*1024*1024);assert ctypes.CDLL(None).prctl(4,0,0,0,0)==0;time.sleep(1)'
  error,outcome,events=self.run_original('bounded-original-v2',body,rss_bytes=96*1024*1024)
  self.assertEqual(error,'RSSLimit');self.assertEqual(outcome['first_fault'],'RSSLimit')
  self.assertFalse(any(row['phase']=='MEASUREMENT_PENDING' for row in events))
  self.assertEqual(outcome['cleanup'],'STOPPED')


class OtherRoleRefusalTests(unittest.TestCase):
 from test_derivation import DerivationTests as _helpers
 setUp=_helpers.setUp
 tearDown=_helpers.tearDown
 prepare=_helpers.prepare
 stopped=_helpers.stopped
 spec=_helpers.spec
 def test_helper_cannot_borrow_original_window(self):
  session=self.stopped(measurement_completion='bounded-original-v2')
  body='import ctypes,time;time.sleep(.2);assert ctypes.CDLL(None).prctl(4,0,0,0,0)==0;time.sleep(1)'
  with self.assertRaises(st.StartupFailure) as caught:session.derive_readonly((self.input,),self.spec(body))
  self.assertEqual(caught.exception.code,'MeasurementUnknown')
  events=[json.loads(line) for line in (self.root/'work/session.jsonl').read_text().splitlines()]
  begin=next(i for i,row in enumerate(events) if row['phase']=='DERIVE_INTENT')
  self.assertFalse(any(row['phase']=='MEASUREMENT_PENDING' for row in events[begin:]))
 def test_preparation_mutator_cannot_borrow_original_container(self):
  session=self.prepare(measurement_completion='bounded-original-v2')
  body='import ctypes,time;time.sleep(.2);assert ctypes.CDLL(None).prctl(4,0,0,0,0)==0;time.sleep(1)'
  with self.assertRaises(st.StartupFailure) as caught:
   session.mutate(self.working,st.MutationSpec(self.tool,(self.py,'-c',body,st.ResourceArgument('',self.working,''))))
  self.assertEqual(caught.exception.code,'MeasurementUnknown')
  events=[json.loads(line) for line in (self.root/'work/session.jsonl').read_text().splitlines()]
  self.assertFalse(any(row['phase']=='MEASUREMENT_PENDING' for row in events))

class ActualCompletionTests(unittest.TestCase):
 from test_derivation import DerivationTests as _helpers
 setUp=_helpers.setUp
 tearDown=_helpers.tearDown
 prepare=_helpers.prepare
 spec=_helpers.spec
 read=_helpers.read
 def run_completion(self,kind):
  session=self.prepare(measurement_completion='bounded-original-v2')
  journal=self.root/'work/session.jsonl'
  # The authored child observes only its owned TEST journal, not private state.
  # Actual production FD failure/journal causes the next independent child action.
  body='''import ctypes,pathlib,sys,time,os,json
lib=ctypes.CDLL(None,use_errno=True)
root=pathlib.Path(sys.argv[1]).parent.parent
fds=[os.open('/dev/null',os.O_RDONLY) for _ in range(8)]
(root/'fds-ready').touch()
end=time.monotonic()+2
while not (root/'gap-release').exists() or not any(json.loads(row).get('phase')=='PASSIVE_FINISH_INTENT' for row in pathlib.Path(sys.argv[1]).read_text().splitlines()):
 if time.monotonic()>=end:sys.exit(92)
 time.sleep(.0001)
assert lib.prctl(4,0,0,0,0)==0
end=time.monotonic()+2
while not any(json.loads(row).get('phase')=='MEASUREMENT_PENDING' for row in pathlib.Path(sys.argv[1]).read_text().splitlines()):
 if time.monotonic()>=end:sys.exit(93)
 time.sleep(.0001)
'''
  if kind=='accessible':body+='assert lib.prctl(4,1,0,0,0)==0\nfor fd in fds:os.close(fd)\ntime.sleep(.05)\n'
  else:body+='os._exit(0)\n'
  process=session.launch(st.LaunchSpec(self.tool,(self.py,'-c',body,str(journal))),resources=(self.working,))
  deadline=time.monotonic()+2
  while not (self.root/'fds-ready').exists():
   if time.monotonic()>=deadline:raise AssertionError('actual pre-gap FD phase missing')
   time.sleep(.0005)
  pre=session.usage();child_pre=next(row for row in pre.actor_fds if row[0]==process.identity().pid)
  self.assertGreaterEqual(child_pre[2],11)
  (self.root/'gap-release').touch()
  self.exit=process.finish()
  events=[json.loads(line) for line in journal.read_text().splitlines()]
  pending=[row for row in events if row['phase']=='MEASUREMENT_PENDING']
  completed=[row for row in events if row['phase']=='MEASUREMENT_COMPLETED']
  self.assertEqual(len(pending),1,events);self.assertEqual(len(completed),1,events)
  first,last=pending[0],completed[0]
  self.assertEqual(first['detail']['pid'],self.exit.created_pid)
  self.assertEqual(first['detail']['stage'],'fd-enumeration');self.assertEqual(first['detail']['errno'],13)
  self.assertEqual(first['detail']['before'][19],str(self.exit.startticks));self.assertEqual(first['detail']['after'][19],str(self.exit.startticks))
  self.assertIn(last['attempts'],(2,3));self.assertLessEqual(last['interval'],.100)
  self.assertEqual(last['mode'],'bounded-original-v2');self.assertEqual(last['window'],.100)
  self.assertLessEqual(last['observed_monotonic'],last['end'])
  self.assertEqual(last['gap'],'UNOBSERVED');self.assertTrue(last['observed_peaks_not_continuous_bounds'])
  self.assertEqual(last['resolution'],kind if kind=='accessible' else 'kernel-exit')
  self.assertTrue(all('sequence' in row or row['phase']=='OPEN_INTENT' for row in events))
  between=[row['phase'] for row in events if 'sequence' in row and first['sequence']<row['sequence']<last['sequence']]
  self.assertEqual(between,[])
  self.assertLess(last['sequence'],next(row['sequence'] for row in events if row['phase']=='STOPPED'))
  self.assertTrue(self.exit.identity_at_exit_unproved);self.assertEqual(self.exit.daemon_state,'UNKNOWN')
  self.working=session.snapshot(self.working).successor;self.input=session.seal_stopped(self.working)
  before=session.usage()
  self.assertGreaterEqual(before.peak_fds,pre.peak_fds)
  self.assertGreaterEqual(before.peak_processes,pre.peak_processes)
  self.assertGreaterEqual(next(row[2] for row in before.peak_actor_fds if row[0]==self.exit.created_pid),child_pre[2])
  batch=session.derive_readonly((self.input,),self.spec());after=session.usage()
  self.assertEqual(self.read(batch.artifacts[0]),(b'authored readonly TEST\n'*100).upper()+b'derived')
  self.assertEqual(after.charged_operations,before.charged_operations+1)
  output=os.environ.get('MEASUREMENT_RESULTS')
  if output:
   folder=Path(output);folder.mkdir(parents=True,exist_ok=True)
   (folder/(kind+'.json')).write_text(json.dumps(dict(pending=first,completed=last,before=dataclasses.asdict(before),after=dataclasses.asdict(after),exit=dataclasses.asdict(self.exit))))
 def test_actual_accessible_census_and_full_readonly_chain(self):self.run_completion('accessible')
 def test_actual_kernel_exit_and_full_readonly_chain(self):self.run_completion('kernel')


class V1ClockTests(LiveRefusalTests):
 # Override inherited test methods so discovery does not rerun unrelated controls.
 test_omitted_and_explicit_strict_remain_fail_first=None
 test_known_rss_violation_precedes_unobservable_fd=None
 def test_v1_first_successful_full_census_overshoot_refuses_without_pending(self):
  error,outcome,events=self.run_original('bounded-original-v1','import time;time.sleep(.3)')
  self.assertEqual(error,'MeasurementUnknown');self.assertEqual(outcome['first_fault'],error)
  self.assertFalse(any(row['phase']=='MEASUREMENT_PENDING' for row in events))
  failed=[row for row in events if row['phase']=='MEASUREMENT_INCOMPLETE']
  self.assertTrue(failed,events);row=failed[0]
  self.assertTrue(row['census_complete']);self.assertEqual(row['attempts'],1)
  self.assertEqual(row['mode'],'bounded-original-v1');self.assertEqual(row['window'],.010)
  self.assertGreater(row['interval'],.010);self.assertEqual(row['gap'],'NO_UNAVAILABLE_SAMPLE')
  self.assertEqual(outcome['cleanup'],'STOPPED')
