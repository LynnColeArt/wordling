"""Offline actual orchestration controls. No original/VM or product positive claim."""
from contextlib import contextmanager
from pathlib import Path
import importlib.util
import json
import subprocess
import tempfile
import types
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('wp44_oracle',Path(__file__).with_name('oracle.py'));o=importlib.util.module_from_spec(spec);spec.loader.exec_module(o)
class Orchestration(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.base=Path(self.tmp.name);self.here=self.base/'owned';self.here.mkdir();self.private=self.base/'private';self.private.mkdir();self.master=self.base/'master';self.master.mkdir()
  for name in ['boot.img','harddisk.img']:(self.master/name).write_bytes(name.encode())
  self.runtime=self.base/'runtime';self.runtime.mkdir();self.qmp=types.SimpleNamespace(RUNTIME=self.runtime,SOCKET=self.runtime/'qmp.sock');self.count=0;self.stops=0;self.export_calls=0
  self.guest=types.SimpleNamespace(MASTER=self.master,arguments=lambda *a:['qemu'])
  class Q:
   def __enter__(self):return self
   def __exit__(self,*a):pass
  self.qmp.QMP=Q
  @contextmanager
  def exclusive(*a):yield
  def fresh(*a):self.count+=1;return ['qemu']
  def stop(*a):self.stops+=1;return 'QMP quit; own socket terminated'
  self.session=types.SimpleNamespace(configure=lambda *a:(self.qmp,self.guest,self.private),exclusive=exclusive,fresh_start=fresh,stop_owned=stop,timeout_signal=lambda *a:None,settings_snapshot=lambda *a:{'sha256':'recorded-private-settings'})
  class Probe:
   def __init__(self,q,out):self.out=out;self.exports=[('C44PRE','C44PRE.WP5'),('C44FIN','C44FIN.WP5'),('C44PRN.PRN','C44PRN.PRN')];self.trace=[];self.checks=[];self.settings=[]
  self.n=types.SimpleNamespace(MutationProbe=Probe)
  self.identity={'pid':123,'startticks':'456','argv':['qemu']}
  def perform(p,*a):
   d=p.out/'clean-exit';d.mkdir();(d/'screen.txt').write_text('C:\\WP51>\n');return {'exit_actions':[]}
  self.perform=perform
  for name in ['candidate','source','provenance']:(self.base/name).write_bytes(name.encode())
  c={'id':'c01','candidate':'candidate','source':'source','provenance':'provenance',**{n+'_sha256':o.sha(self.base/n)for n in ['candidate','source','provenance']},'print_control':{'kind':'approved-existing','path':'existing.PRN'},'exports':['C44PRE.WP5','C44FIN.WP5','C44PRN.PRN']}
  self.plan={'run_id':'wp44-c-01','maximum_attempts_including_failures':2,'sources':[],'cases':[c],'master':{n:o.sha(self.master/n)for n in ['boot.img','harddisk.img']},'attempts':[{'id':'attempt'+str(i),'case':'c01','mode':'candidate','qemu_argv':['qemu'],'repetition':i,'private_work':str(self.private/('work'+str(i)))}for i in [1,2]]}
 def copy(self,argv,**kw):
  self.export_calls+=1;Path(argv[-1]).write_bytes((self.base/'candidate').read_bytes()if argv[-2]=='::OUT/C44INPUT'else b'original-output');return subprocess.CompletedProcess(argv,0,b'',b'')
 def invoke(self,**overrides):
  grant=self.base/'grant.json';grant.write_text(json.dumps({'authorized':True,'plan_sha256':o.canonical(self.plan),'grant_id':'wp44-test','attempt_ids':['attempt1','attempt2'],'maximum_aggregate_attempts':2}));args=types.SimpleNamespace(allow_vm=True,grant=str(grant),grant_id='wp44-test',attempt=['attempt1','attempt2'])
  values={'HERE':self.here,'ROOT':self.base,'check':lambda:self.plan,'helpers':lambda:(self.session,self.n,None,None,None),'owned_identity':lambda *a:self.identity,'same_identity':lambda *a:None,'stopped':lambda *a:{'gone_or_same_zombie':True,'socket_absent':True},'perform':self.perform,'qualify_exports':lambda *a:{'isolated_fake_custody_control':True}};values.update(overrides)
  with patch.multiple(o,**values),patch.object(o.subprocess,'run',side_effect=self.copy):exitcode=o.run(args)
  report=json.loads((self.here/'runs/wp44-test/run.json').read_text());return exitcode,report
 def assert_halted_once(self,report):
  self.assertEqual(self.count,1);self.assertEqual(len(report['results']),1);self.assertFalse(report['complete']);self.assertTrue(report['halted_before_next_guest']);self.assertTrue(report['guard_released'])
 def test_positive_complete_exports_two_fresh(self):
  code,r=self.invoke();self.assertEqual(code,0);self.assertEqual(self.count,2);self.assertEqual(self.export_calls,8);self.assertTrue(r['complete']);self.assertTrue(r['oracle_released'])
 def test_missing_owned_PID_no_stop_no_extraction_no_next(self):
  def absent(*a):raise o.Refusal('MissingOwnedPID','actual PID missing')
  code,r=self.invoke(owned_identity=absent);self.assert_halted_once(r);self.assertEqual(self.stops,0);self.assertEqual(self.export_calls,0);self.assertFalse(r['results'][0]['guest_stopped']);self.assertFalse(r['oracle_released'])
 def test_stop_error_no_extraction_no_next(self):
  def bad(*a):raise RuntimeError('stop failed')
  self.session.stop_owned=bad;code,r=self.invoke();self.assert_halted_once(r);self.assertEqual(self.export_calls,0);self.assertIn('stop_error',r['results'][0])
 def test_owned_start_identity_mismatch_no_stop(self):
  def bad(*a):raise o.Refusal('PIDReused','changed startticks')
  code,r=self.invoke(same_identity=bad);self.assert_halted_once(r);self.assertEqual(self.stops,0);self.assertEqual(self.export_calls,0)
 def test_socket_stop_unproven_no_extraction(self):
  def bad(*a):raise o.Refusal('OwnedSocketPresent','still present')
  code,r=self.invoke(stopped=bad);self.assert_halted_once(r);self.assertEqual(self.export_calls,0);self.assertFalse(r['results'][0]['guest_stopped'])
 def test_mcopy_nonzero_even_existing_output_no_complete(self):
  original=self.copy
  def failed(*a,**kw):original(*a,**kw);return subprocess.CompletedProcess(a[0],1,b'',b'mcopy failure')
  self.copy=failed;code,r=self.invoke();self.assert_halted_once(r);self.assertEqual(r['results'][0]['extraction_error_code'],'RequiredExportFailed')
 def test_missing_required_native_precise_refusal(self):
  self.copy=lambda argv,**kw:subprocess.CompletedProcess(argv,0,b'',b'');code,r=self.invoke();self.assert_halted_once(r);self.assertEqual(r['results'][0]['extraction_error_code'],'RequiredExportMissing')
 def test_empty_required_stream_precise_refusal(self):
  def empty(argv,**kw):Path(argv[-1]).write_bytes(b'');return subprocess.CompletedProcess(argv,0,b'',b'')
  self.copy=empty;code,r=self.invoke();self.assert_halted_once(r);self.assertEqual(r['results'][0]['extraction_error_code'],'RequiredExportMissing')
 def test_master_changes_after_stopped_exports_halts(self):
  original=self.copy
  def changed(*a,**kw):v=original(*a,**kw);(self.master/'harddisk.img').write_bytes(b'changed');return v
  self.copy=changed;code,r=self.invoke();self.assert_halted_once(r);self.assertFalse(r['master_unchanged']);self.assertEqual(r['results'][0]['outcome'],'required-output-or-master-unproven')
 def test_unknown_original_protocol_still_retains_failure_after_guarded_stop(self):
  def bad(*a):raise o.Refusal('UnknownExitState','not DOS')
  code,r=self.invoke(perform=bad);self.assert_halted_once(r);self.assertEqual(r['results'][0]['error_code'],'UnknownExitState');self.assertTrue(r['results'][0]['guest_stopped']);self.assertGreater(self.export_calls,0)
 def test_host_containment_never_complete(self):
  self.session.stop_owned=lambda *a:'Host containment: verified own pid termination; not original Cancel';code,r=self.invoke();self.assert_halted_once(r);self.assertEqual(r['results'][0]['stop_error_code'],'HostContained')
 def test_required_native_refusal_halts_before_next_fresh(self):
  def refused(*a):raise o.Refusal('RequiredPreprintRefused','counter/cache not admitted')
  code,r=self.invoke(qualify_exports=refused);self.assert_halted_once(r);self.assertEqual(r['results'][0]['required_output_or_master_error_code'],'RequiredPreprintRefused')
 def test_chunk_exact_subset_and_no_duplicate_or_unknown_leaf(self):
  args=types.SimpleNamespace(grant_id='wp44-phase01',attempt=['attempt1'])
  grant={'authorized':True,'plan_sha256':o.canonical(self.plan),'grant_id':args.grant_id,'attempt_ids':args.attempt,'maximum_aggregate_attempts':2}
  self.assertEqual(len(o.selected_attempts(args,self.plan,grant)),1)
  for ids in [['attempt1','attempt1'],['unknown']]:
   args.attempt=ids;grant['attempt_ids']=ids
   with self.assertRaises(o.Refusal)as c:o.selected_attempts(args,self.plan,grant)
   self.assertEqual(c.exception.code,'AttemptSelection')
 def test_grant_wrong_source_count_subset_and_identity_rejected(self):
  args=types.SimpleNamespace(grant_id='wp44-phase01',attempt=['attempt1'])
  valid={'authorized':True,'plan_sha256':o.canonical(self.plan),'grant_id':args.grant_id,'attempt_ids':args.attempt,'maximum_aggregate_attempts':2}
  for key,value in [('authorized',False),('plan_sha256','0'*64),('grant_id','wp44-other'),('attempt_ids',['attempt2']),('maximum_aggregate_attempts',3)]:
   bad=dict(valid);bad[key]=value
   with self.assertRaises(o.Refusal)as c:o.selected_attempts(args,self.plan,bad)
   self.assertEqual(c.exception.code,'GrantMismatch')
 def test_missing_new_control_refuses_before_candidate(self):
  case={'id':'c01','print_control':{'kind':'new-original-control'}};leaf={'mode':'candidate','repetition':1}
  with self.assertRaises(o.Refusal)as c:o.control_from_ledger(case,leaf,[])
  self.assertEqual(c.exception.code,'MissingControl')
 def test_durable_incomplete_ledger_blocks_new_chunk_before_fresh(self):
  ledger={'plan_sha256':o.canonical(self.plan),'maximum':2,'attempts':[{'id':'earlier-failed','outcome':'error'}]};(self.private/'wp44-attempts.json').write_text(json.dumps(ledger))
  code,r=self.invoke();self.assertEqual(self.count,0);self.assertFalse(r['complete']);self.assertEqual(r['batch_error_code'],'PriorIncomplete')
 def test_durable_plan_mismatch_refuses_before_any_fresh(self):
  (self.private/'wp44-attempts.json').write_text(json.dumps({'plan_sha256':'wrong','maximum':2,'attempts':[]}));code,r=self.invoke();self.assertEqual(self.count,0);self.assertEqual(r['batch_error_code'],'AggregatePlanMismatch')
 def test_duplicate_prior_complete_leaf_never_replayed(self):
  (self.private/'wp44-attempts.json').write_text(json.dumps({'plan_sha256':o.canonical(self.plan),'maximum':2,'attempts':[{'id':'attempt1','outcome':'complete-observation'}]}));code,r=self.invoke();self.assertEqual(self.count,0);self.assertEqual(r['batch_error_code'],'PriorAttempt')
 def test_changed_candidate_before_leaf_refuses_no_fresh(self):
  (self.base/'candidate').write_bytes(b'tampered');code,r=self.invoke();self.assertEqual(self.count,0);self.assertEqual(r['batch_error_code'],'InputSourceDrift')
 def test_preexisting_private_work_never_started_or_replaced(self):
  work=Path(self.plan['attempts'][0]['private_work']);work.mkdir();(work/'untouched').write_bytes(b'prior');code,r=self.invoke();self.assertEqual(self.count,0);self.assertEqual((work/'untouched').read_bytes(),b'prior');self.assertEqual(r['batch_error_code'],'ForeignRuntime')
 def test_no_grant_refuses_before_check_or_output(self):
  with patch.object(o,'check',side_effect=AssertionError('must not reach')):
   with self.assertRaises(o.Refusal)as c:o.run(types.SimpleNamespace(allow_vm=False))
  self.assertEqual(c.exception.code,'AuthorizationRequired');self.assertEqual(self.count,0)

if __name__=='__main__':unittest.main()
