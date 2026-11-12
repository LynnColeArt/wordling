"""Deterministic owned-stop and versioned-budget controls; no VM/real proc/sleeps."""
from pathlib import Path
import copy
import json
import shutil
import types
import unittest
from unittest.mock import patch
import test_oracle as base
o=base.o

ACTUAL_STOP=o.stopped
REAL_PATH=Path
class FakeClock:
 def __init__(self):self.now=0.;self.waits=[]
 def monotonic(self):return self.now
 def pause(self,seconds):self.waits.append(seconds);self.now+=seconds

class StopPoll(unittest.TestCase):
 def setUp(self):
  self.fx=base.Orchestration('test_positive_complete_exports_two_fresh');self.fx.setUp();self.addCleanup(self.fx.doCleanups);self.clock=FakeClock();self.log=[];self.identity=self.fx.identity
 def state(self,kind,socket=False,**kw):
  value={'classification':kind,'pid':123,'pid_present':kind!='gone','socket_present':socket,'state':'Z'if kind=='zombie'else'S','startticks':'456','reason':'isolated deterministic observation'};value.update(kw);return value
 def poll(self,states,timeout=.1):
  queue=iter(states);last=states[-1]
  def observe(*args):return next(queue,last).copy()
  return ACTUAL_STOP(self.fx.qmp,self.identity,observations=self.log,observe=observe,clock=self.clock.monotonic,pause=self.clock.pause,timeout=timeout,interval=.05)
 def test_live_then_same_zombie_waits_and_logs(self):
  proof=self.poll([self.state('live'),self.state('zombie')]);self.assertEqual(len(self.log),2);self.assertEqual(self.clock.waits,[.05]);self.assertTrue(proof['gone_or_same_zombie']);self.assertEqual([x['elapsed_seconds']for x in self.log],[0,.05])
 def test_live_then_gone_waits(self):
  self.poll([self.state('live'),self.state('gone')]);self.assertEqual(len(self.log),2)
 def test_live_forever_deadline_is_exact_not_exit(self):
  with self.assertRaises(o.Refusal)as c:self.poll([self.state('live')])
  self.assertEqual(c.exception.code,'OwnedStopDeadline');self.assertEqual(self.clock.now,.1);self.assertEqual(len(self.log),3)
 def test_reused_zombie_refuses_immediately_without_wait(self):
  with self.assertRaises(o.Refusal)as c:self.poll([self.state('pid-reused',state='Z',startticks='457')])
  self.assertEqual(c.exception.code,'OwnedPIDReused');self.assertEqual(self.clock.waits,[])
 def test_foreign_live_identity_refuses_immediately(self):
  with self.assertRaises(o.Refusal)as c:self.poll([self.state('foreign-identity')])
  self.assertEqual(c.exception.code,'ForeignOwnedIdentity');self.assertEqual(self.clock.waits,[])
 def test_zombie_and_gone_wait_for_socket_absence(self):
  for kind in ['zombie','gone']:
   self.clock=FakeClock();self.log=[];self.poll([self.state(kind,True),self.state(kind,False)]);self.assertEqual(len(self.log),2)
 def test_terminal_PID_with_socket_forever_refuses(self):
  with self.assertRaises(o.Refusal)as c:self.poll([self.state('gone',True)])
  self.assertEqual(c.exception.code,'OwnedStopDeadline')
 def test_missing_identity_before_any_observation(self):
  for identity,code in [({'pid':0},'MissingOwnedPID'),({'pid':123},'MissingOwnedIdentity')]:
   with self.assertRaises(o.Refusal)as c:ACTUAL_STOP(self.fx.qmp,identity,observe=lambda *a:self.fail('must not observe'),clock=lambda:self.fail('must validate first'))
   self.assertEqual(c.exception.code,code)
 def filesystem(self,state='S',start='456'):
  proc=self.fx.base/'fake-proc'/'123';proc.mkdir(parents=True);(proc/'stat').write_text('123 (qemu) '+state+' '+'0 '*18+start+'\n');(proc/'cmdline').write_bytes(b'\0'.join(x.encode()for x in self.identity['argv'])+b'\0');exe=self.fx.base/'qemu';exe.write_bytes(b'isolated-test-executable');(proc/'exe').symlink_to(exe);self.identity['executable']=str(exe);return proc
 def path_adapter(self,value,*args):return self.fx.base/'fake-proc'if value=='/proc'else REAL_PATH(value,*args)
 def test_actual_filesystem_observer_same_live_and_zombie(self):
  proc=self.filesystem()
  with patch.object(o,'Path',side_effect=self.path_adapter):
   self.assertEqual(o.observe_owned_stop(self.fx.qmp,self.identity)['classification'],'live');(proc/'stat').write_text('123 (qemu) Z '+'0 '*18+'456\n');(proc/'cmdline').unlink();self.assertEqual(o.observe_owned_stop(self.fx.qmp,self.identity)['classification'],'zombie')
 def test_actual_filesystem_PID_reuse_and_foreign_argv(self):
  proc=self.filesystem(state='Z',start='457')
  with patch.object(o,'Path',side_effect=self.path_adapter):self.assertEqual(o.observe_owned_stop(self.fx.qmp,self.identity)['classification'],'pid-reused')
  (proc/'stat').write_text('123 (qemu) S '+'0 '*18+'456\n');(proc/'cmdline').write_bytes(b'foreign\0')
  with patch.object(o,'Path',side_effect=self.path_adapter):self.assertEqual(o.observe_owned_stop(self.fx.qmp,self.identity)['classification'],'foreign-identity')
 def test_stat_disappearance_resampled_then_gone(self):
  proc=self.filesystem();original=REAL_PATH.read_text;first=[True]
  def read(path,*args,**kw):
   if path==proc/'stat'and first[0]:first[0]=False;shutil.rmtree(proc);raise FileNotFoundError('isolated disappearance race')
   return original(path,*args,**kw)
  with patch.object(o,'Path',side_effect=self.path_adapter),patch.object(REAL_PATH,'read_text',read):
   ACTUAL_STOP(self.fx.qmp,self.identity,observations=self.log,clock=self.clock.monotonic,pause=self.clock.pause,timeout=.1,interval=.05)
  self.assertEqual([x['classification']for x in self.log],['resample','gone']);self.assertEqual(self.clock.waits,[.05])
 def test_malformed_and_read_denied_stat_fail_closed(self):
  proc=self.filesystem();(proc/'stat').write_text('truncated');
  with patch.object(o,'Path',side_effect=self.path_adapter):
   with self.assertRaises(o.Refusal)as c:ACTUAL_STOP(self.fx.qmp,self.identity,observations=self.log,clock=self.clock.monotonic,pause=self.clock.pause)
  self.assertEqual(c.exception.code,'StopStatMalformed');self.assertEqual(self.log[-1]['raw_stat'],'truncated')
  original=REAL_PATH.read_text
  def read(path,*a,**kw):
   if path==proc/'stat':raise PermissionError('isolated denied read')
   return original(path,*a,**kw)
  with patch.object(o,'Path',side_effect=self.path_adapter),patch.object(REAL_PATH,'read_text',read):
   with self.assertRaises(o.Refusal)as c:ACTUAL_STOP(self.fx.qmp,self.identity,observations=[],clock=self.clock.monotonic,pause=self.clock.pause)
  self.assertEqual(c.exception.code,'PermissionError')
 def actual_attempt_poll(self,states):
  def poll(qmp,identity,**kwargs):
   clock=FakeClock();queue=iter(states)
   return ACTUAL_STOP(qmp,identity,**kwargs,observe=lambda *a:next(queue,states[-1]).copy(),clock=clock.monotonic,pause=clock.pause,timeout=.1,interval=.05)
  return poll
 def test_actual_attempt_live_to_terminal_before_exports_and_second_fresh(self):
  code,r=self.fx.invoke(stopped=self.actual_attempt_poll([self.state('live'),self.state('zombie')]))
  self.assertEqual(code,0);self.assertEqual(self.fx.count,2);self.assertEqual(self.fx.export_calls,8)
  for row in r['results']:self.assertEqual(len(row['stop_observations']),2);self.assertTrue(row['guest_stopped']);self.assertTrue(row['exports_complete'])
 def test_actual_attempt_deadline_no_extract_no_next_sticky(self):
  code,r=self.fx.invoke(stopped=self.actual_attempt_poll([self.state('live')]))
  self.fx.assert_halted_once(r);self.assertEqual(self.fx.export_calls,0);self.assertEqual(r['results'][0]['stop_error_code'],'OwnedStopDeadline');self.assertFalse(r['results'][0]['guest_stopped']);self.assertEqual(len(r['results'][0]['stop_observations']),3)
  ledger=json.loads((self.fx.private/'wp44-attempts-v2.json').read_text());self.assertEqual(ledger['historical_spent']+len(ledger['attempts']),2);self.assertEqual(ledger['attempts'][0]['outcome'],'incomplete')
 def test_actual_attempt_reused_PID_no_extract_or_next(self):
  code,r=self.fx.invoke(stopped=self.actual_attempt_poll([self.state('pid-reused',state='Z',startticks='457')]))
  self.fx.assert_halted_once(r);self.assertEqual(self.fx.export_calls,0);self.assertEqual(r['results'][0]['stop_error_code'],'OwnedPIDReused')
 def test_containment_and_stop_exception_never_poll_or_extract(self):
  for method in ['containment','raises']:
   if method=='raises':
    def stop(*a):raise RuntimeError('isolated stop failure')
    self.fx.session.stop_owned=stop
   else:self.fx.session.stop_owned=lambda *a:'Host containment: not normal QMP completion'
   code,r=self.fx.invoke(stopped=lambda *a,**k:self.fail('must refuse stop method BEFORE polling'))
   self.fx.assert_halted_once(r);self.assertFalse(r['results'][0]['guest_stopped']);self.assertEqual(self.fx.export_calls,0)
   if method=='containment':self.assertEqual(r['results'][0]['stop_error_code'],'HostContained')
   self.fx.doCleanups();self.fx=base.Orchestration('test_positive_complete_exports_two_fresh');self.fx.setUp();self.addCleanup(self.fx.doCleanups)

 def test_actual_attempt_live_to_gone_waits_for_socket(self):
  code,r=self.fx.invoke(stopped=self.actual_attempt_poll([self.state('live',True),self.state('gone',True),self.state('gone',False)]))
  self.assertEqual(code,0);self.assertEqual(self.fx.count,2);self.assertEqual(self.fx.export_calls,8)
  for row in r['results']:self.assertEqual(len(row['stop_observations']),3);self.assertTrue(row['guest_stopped'])
 def test_actual_attempt_missing_identity_never_stops_or_extracts(self):
  code,r=self.fx.invoke(owned_identity=lambda *a:{'pid':123},stopped=lambda *a,**k:self.fail('missing identity must not reach poll'))
  self.fx.assert_halted_once(r);self.assertEqual(self.fx.stops,0);self.assertEqual(self.fx.export_calls,0);self.assertEqual(r['results'][0]['stop_error_code'],'MissingOwnedIdentity')
 def test_terminal_observation_after_deadline_is_not_success(self):
  def late(*a):self.clock.now=.2;return self.state('zombie')
  with self.assertRaises(o.Refusal)as c:ACTUAL_STOP(self.fx.qmp,self.identity,observe=late,clock=self.clock.monotonic,pause=self.clock.pause,timeout=.1,interval=.05,observations=self.log)
  self.assertEqual(c.exception.code,'OwnedStopDeadline');self.assertEqual(self.log[-1]['observation_complete_monotonic'],.2)
 def test_live_executable_mismatch_is_foreign(self):
  proc=self.filesystem();other=self.fx.base/'other-executable';other.write_bytes(b'isolated other');(proc/'exe').unlink();(proc/'exe').symlink_to(other)
  with patch.object(o,'Path',side_effect=self.path_adapter):self.assertEqual(o.observe_owned_stop(self.fx.qmp,self.identity)['classification'],'foreign-identity')

class SuccessorProtocol(unittest.TestCase):
 def setUp(self):
  self.fx=base.Orchestration('test_positive_complete_exports_two_fresh');self.fx.setUp();self.addCleanup(self.fx.doCleanups)
 def test_predecessor_bytes_changed_refuses_before_guest(self):
  old=self.fx.plan['transition']['predecessor']['private_ledger']['path'];Path(old).write_bytes(b'changed')
  with self.assertRaises(o.Refusal)as c:self.fx.invoke()
  self.assertEqual(self.fx.count,0);self.assertEqual(c.exception.code,'PredecessorIdentity');self.assertFalse((self.fx.private/'wp44-attempts-v2.json').exists())
 def test_historical_accounting_cap_transition_hash_and_oldID_refuse(self):
  for field,value in [('historical_spent',0),('historical_spent',True),('cumulative_maximum',49),('transition_receipt_sha256','0'*64)]:
   ledger=self.fx.ledger();ledger[field]=value
   with self.assertRaises(o.Refusal):o.validate_successor_ledger(self.fx.plan,ledger)
  ledger=self.fx.ledger([{'id':self.fx.plan['transition']['failed_attempt_id'],'outcome':'complete-observation'}])
  with self.assertRaises(o.Refusal)as c:o.validate_successor_ledger(self.fx.plan,ledger)
  self.assertEqual(c.exception.code,'PriorAttempt')
 def test_missing_or_wrong_root_transition_authorization_before_output(self):
  args=types.SimpleNamespace(grant_id='wp44-v2-unit',attempt=['attempt1']);p=self.fx.plan
  good={'authorized':True,'plan_sha256':o.canonical(p),'grant_id':args.grant_id,'attempt_ids':args.attempt,'maximum_aggregate_attempts':p['cumulative_maximum_attempts_including_failures'],'transition_authorization':{'authorized_by_root':True,**p['required_grant_transition_fields']}}
  for field,value in [('authorized_by_root',False),('historical_spent',0),('historical_spent',True),('predecessor_ledger_sha256','0'*64),('cumulative_maximum_attempts_including_failures',99)]:
   bad=copy.deepcopy(good);bad['transition_authorization'][field]=value
   with self.assertRaises(o.Refusal)as c:o.selected_attempts(args,p,bad)
   self.assertEqual(c.exception.code,'TransitionAuthorization')
  bad=dict(good);bad.pop('transition_authorization')
  with self.assertRaises(o.Refusal)as c:o.selected_attempts(args,p,bad)
  self.assertEqual(c.exception.code,'TransitionAuthorization')
 def test_current_completion_excludes_retained_historical_failure(self):
  oldpath=Path(self.fx.plan['transition']['predecessor']['private_ledger']['path']);before=oldpath.read_bytes();code,r=self.fx.invoke()
  self.assertEqual(code,0);self.assertTrue(r['current48_complete']);self.assertEqual(r['historical_spent'],1);self.assertEqual(r['cumulative_spent'],3);self.assertEqual(oldpath.read_bytes(),before)
  current=json.loads((self.fx.private/'wp44-attempts-v2.json').read_text());self.assertFalse(current['historical_failed_attempt']['qualified']);self.assertEqual(current['historical_failed_attempt']['outcome'],'incomplete')
 def test_overbudget_exact_subsets_refuse_before_fresh(self):
  # Two current leaves + one historical spent are the isolated fixture ceiling.
  self.fx.plan['new_required_positive_leaves']=1;self.fx.plan['cumulative_maximum_attempts_including_failures']=2;self.fx.plan['required_grant_transition_fields']['cumulative_maximum_attempts_including_failures']=2;code,r=self.fx.invoke();self.assertEqual(self.fx.count,0);self.assertEqual(r['batch_error_code'],'AttemptLimit')

 def test_actual_run_missing_transition_authorization_refuses_before_outputs(self):
  p=self.fx.plan;grant={'authorized':True,'plan_sha256':o.canonical(p),'grant_id':'wp44-v2-noauth','attempt_ids':['attempt1'],'maximum_aggregate_attempts':p['cumulative_maximum_attempts_including_failures']};path=self.fx.base/'bad-grant.json';o.dump(path,grant);args=types.SimpleNamespace(allow_vm=True,grant=str(path),grant_id=grant['grant_id'],attempt=grant['attempt_ids'])
  with patch.object(o,'check',return_value=p),patch.object(o,'HERE',self.fx.here):
   with self.assertRaises(o.Refusal)as c:o.run(args)
  self.assertEqual(c.exception.code,'TransitionAuthorization');self.assertEqual(self.fx.count,0);self.assertFalse((self.fx.here/'runs').exists())

if __name__=='__main__':unittest.main()
