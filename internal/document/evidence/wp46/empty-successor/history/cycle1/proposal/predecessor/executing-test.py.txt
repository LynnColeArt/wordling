"""Offline actual owned routing fault controls; all guest/proc boundaries isolated."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import types
import unittest
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'wp44'))
spec=importlib.util.spec_from_file_location('approved_custody_test_fixture',HERE.parent/'wp44/test_oracle.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
spec=importlib.util.spec_from_file_location('owned_wp46_oracle',HERE/'oracle.py');o=importlib.util.module_from_spec(spec);spec.loader.exec_module(o)

class Routing(unittest.TestCase):
 def setUp(self):
  self.f=base.Orchestration('test_positive_complete_exports_two_fresh');self.f.setUp();self.addCleanup(self.f.doCleanups);f=self.f
  class Probe:
   def __init__(self,q,out):self.out=out;self.exports=[('C46PRE','C46PRE.WP5'),('C46FIN','C46FIN.WP5'),('C46PRN.PRN','C46PRN.PRN')];self.trace=[];self.checks=[];self.settings=[]
  f.n.MutationProbe=Probe
  self.plan={'maximum_attempts_including_failures':12,'sources':[],'cases':[{'id':'ascii-edit','native_class':'ascii','candidate':'candidate','candidate_sha256':o.sha(f.base/'candidate'),'candidate_size':len(b'candidate')}],'master':{n:o.sha(f.master/n)for n in ['boot.img','harddisk.img']},'ledger':str(f.private/'wp46-attempts.json'),'attempts':[{'id':'wp46-ascii-edit-candidate-r'+str(i),'case':'ascii-edit','mode':'candidate','qemu_argv':['qemu'],'repetition':i,'private_work':str(f.private/('work'+str(i)))}for i in [1,2]]}
  self.qualify=lambda *a:{'isolated_fake_boundary_only':True}
 def copy(self,argv,**kw):
  self.f.export_calls+=1;Path(argv[-1]).write_bytes(b'candidate'if argv[-2]=='::OUT/C46INPUT'else b'original-output');return subprocess.CompletedProcess(argv,0,b'',b'')
 def invoke(self,**changes):
  f=self.f;grant=f.base/'grant46.json';ids=[x['id']for x in self.plan['attempts']if x['mode']=='candidate'];grant.write_text(json.dumps({'authorized':True,'plan_sha256':o.canonical(self.plan),'grant_id':'wp46-test','attempt_ids':ids,'maximum_aggregate_attempts':12,'authorization_note':'isolated fake-run integrity test, never product proof'}));args=types.SimpleNamespace(allow_vm=True,grant=str(grant),grant_id='wp46-test',attempt=ids)
  values={'HERE':f.here,'ROOT':f.base,'check':lambda:self.plan,'helpers':lambda:(f.session,f.n,None,None,None,None),'perform':f.perform,'qualify':self.qualify,'bind_control':lambda *a:None};values.update(changes)
  guard={'owned_identity':lambda *a:f.identity,'same_identity':lambda *a:None,'stopped':lambda *a,**kw:{'gone_or_same_zombie':True,'socket_absent':True}}
  for name in ['owned_identity','same_identity','stopped']:
   if name in values:guard[name]=values.pop(name)
  with patch.multiple(o,**values),patch.multiple(o.guard,**guard),patch.object(o.subprocess,'run',side_effect=self.copy):code=o.run(args)
  return code,json.loads((f.here/'runs/wp46-test/run.json').read_text())
 def halted_once(self,row):self.assertEqual(self.f.count,1);self.assertFalse(row['complete']);self.assertTrue(row['halted_before_next_guest']);self.assertEqual(len(row['results']),1)
 def test_two_fresh_positive_boundaries(self):
  code,row=self.invoke();self.assertEqual(code,0);self.assertEqual(self.f.count,2);self.assertTrue(row['oracle_released']);self.assertTrue(all(x['plan_sha256']==o.canonical(self.plan)for x in row['results']))
 def test_missing_positive_PID_never_extracts_or_next(self):
  def no(*a):raise o.Refusal('MissingOwnedPID','isolated missing PID')
  code,row=self.invoke(owned_identity=no);self.halted_once(row);self.assertEqual(self.f.export_calls,0);self.assertFalse(row['results'][0]['guest_stopped'])
 def test_stop_exception_never_extracts_or_next(self):
  def fail(*a):raise RuntimeError('isolated stop error')
  self.f.session.stop_owned=fail;code,row=self.invoke();self.halted_once(row);self.assertEqual(self.f.export_calls,0)
 def test_containment_never_marks_guest_stopped(self):
  self.f.session.stop_owned=lambda *a:'host containment';code,row=self.invoke();self.halted_once(row);self.assertEqual(row['results'][0]['stop_error_code'],'HostContained');self.assertFalse(row['results'][0]['guest_stopped']);self.assertEqual(self.f.export_calls,0)
 def test_deadline_never_extracts_or_next(self):
  def fail(*a,**kw):raise o.Refusal('OwnedStopDeadline','isolated still live')
  code,row=self.invoke(stopped=fail);self.halted_once(row);self.assertEqual(row['results'][0]['stop_error_code'],'OwnedStopDeadline');self.assertEqual(self.f.export_calls,0)
 def test_mcopy_failure_even_if_file_exists_never_completes(self):
  original=self.copy
  def fail(*a,**kw):r=original(*a,**kw);return subprocess.CompletedProcess(r.args,1,b'',b'isolated copy error')
  self.copy=fail;code,row=self.invoke();self.halted_once(row);self.assertEqual(row['results'][0]['extraction_error_code'],'RequiredExportFailed')
 def test_missing_required_export_precise_refusal(self):
  self.copy=lambda argv,**kw:subprocess.CompletedProcess(argv,0,b'',b'');code,row=self.invoke();self.halted_once(row);self.assertEqual(row['results'][0]['extraction_error_code'],'RequiredExportMissing')
 def test_unknown_normal_state_stops_grant_without_false_DOS(self):
  def fail(*a):raise o.Refusal('UnknownExitState','isolated modal')
  code,row=self.invoke(perform=fail);self.halted_once(row);self.assertNotIn('normal_DOS',row['results'][0]);self.assertEqual(row['results'][0]['error_code'],'UnknownExitState')
 def test_required_field_or_body_comparison_halts_before_next(self):
  def fail(*a):raise o.Refusal('OriginalBodyMismatch','isolated mismatch')
  code,row=self.invoke(qualify=fail);self.halted_once(row);self.assertEqual(row['results'][0]['qualification_error_code'],'OriginalBodyMismatch')
 def test_master_divergence_retained_and_no_next(self):
  original=self.copy
  def alter(*a,**kw):r=original(*a,**kw);(self.f.master/'harddisk.img').write_bytes(b'wrong');return r
  self.copy=alter;code,row=self.invoke();self.halted_once(row);self.assertFalse(row['master_unchanged'])
 def test_preexisting_ledger_failure_no_fresh_start(self):
  o.dump(Path(self.plan['ledger']),{'plan_sha256':o.canonical(self.plan),'maximum':12,'attempts':[{'id':self.plan['attempts'][0]['id'],'outcome':'incomplete'}]});code,row=self.invoke();self.assertEqual(self.f.count,0);self.assertEqual(row['batch_error_code'],'PriorFailure')
 def test_duplicate_prior_ledger_no_fresh_start(self):
  entry={'id':self.plan['attempts'][0]['id'],'outcome':'complete-observation'};o.dump(Path(self.plan['ledger']),{'plan_sha256':o.canonical(self.plan),'maximum':12,'attempts':[entry,entry]});code,row=self.invoke();self.assertEqual(self.f.count,0);self.assertEqual(row['batch_error_code'],'LedgerIdentity')
 def test_preexisting_private_path_no_launch(self):
  Path(self.plan['attempts'][0]['private_work']).mkdir();code,row=self.invoke();self.assertEqual(self.f.count,0);self.assertEqual(row['batch_error_code'],'ForeignRuntime')
 def test_no_root_authorization_before_check_or_output(self):
  with patch.object(o,'check',side_effect=AssertionError('must not check')):
   with self.assertRaises(o.Refusal)as e:o.run(types.SimpleNamespace(allow_vm=False))
  self.assertEqual(e.exception.code,'AuthorizationRequired')

 def test_changed_completed_control_actual_run_refuses_before_fresh_start(self):
  self.plan['attempts']+=[{'id':f'wp46-ascii-edit-control-r{i}','case':'ascii-edit','mode':'control','repetition':i,'qemu_argv':['qemu'],'private_work':str(self.f.private/f'ctl{i}')}for i in [1,2]]
  ident='wp46-ascii-edit-control-r1';directory=self.f.here/'runs/old'/ident;directory.mkdir(parents=True);stream=directory/'C46PRN.PRN';stream.write_bytes(b'full-stream')
  row={'id':ident,'case':'ascii-edit','mode':'control','repetition':1,'plan_sha256':o.canonical(self.plan),'exports':[{'name':'C46PRN.PRN','path':str(stream),'present':True,'size':11,'sha256':o.sha(stream)}]};report=directory/'result.json';o.dump(report,row)
  o.dump(Path(self.plan['ledger']),{'plan_sha256':o.canonical(self.plan),'maximum':12,'attempts':[{'id':ident,'outcome':'complete-observation','grant_id':'old','result_sha256':o.canonical(row),'result_file_sha256':o.sha(report)}]});stream.write_bytes(b'wrong-bytes')
  code,result=self.invoke(bind_control=o.bind_control);self.assertEqual(self.f.count,0);self.assertEqual(result['batch_error_code'],'ControlExportIdentity');self.assertFalse(result['complete'])
 def test_reused_PID_before_stop_no_export_or_next(self):
  def fail(*a):raise o.Refusal('PIDReused','changed identity')
  code,row=self.invoke(same_identity=fail);self.halted_once(row);self.assertEqual(self.f.export_calls,0);self.assertEqual(self.f.stops,0);self.assertEqual(row['results'][0]['stop_error_code'],'PIDReused')

class ControlPins(unittest.TestCase):
 def setUp(self):
  self.f=base.Orchestration('test_positive_complete_exports_two_fresh');self.f.setUp();self.addCleanup(self.f.doCleanups);self.plan={'frozen':'plan'};self.case={'id':'empty-print'};self.leaf={'mode':'candidate','repetition':1};self.ident='wp46-empty-print-control-r1';self.directory=self.f.here/'runs/grant'/self.ident;self.directory.mkdir(parents=True);self.raw=self.directory/'C46PRN.PRN';self.raw.write_bytes(b'full-stream')
  self.row={'id':self.ident,'case':'empty-print','mode':'control','repetition':1,'plan_sha256':o.canonical(self.plan),'exports':[{'name':'C46PRN.PRN','present':True,'path':str(self.raw),'size':11,'sha256':o.sha(self.raw)}]};self.report=self.directory/'result.json';o.dump(self.report,self.row);self.prior=[{'id':self.ident,'outcome':'complete-observation','grant_id':'grant','result_sha256':o.canonical(self.row),'result_file_sha256':o.sha(self.report)}]
 def test_positive_control_record_bound(self):
  with patch.object(o,'HERE',self.f.here):p=o.bind_control(self.plan,self.case,self.leaf,self.prior)
  self.assertEqual(p['result_sha256'],o.canonical(self.row))
 def test_mutated_PRN_before_candidate_refuses(self):
  self.raw.write_bytes(b'wrong-bytes')
  with patch.object(o,'HERE',self.f.here):
   with self.assertRaises(o.Refusal)as e:o.bind_control(self.plan,self.case,self.leaf,self.prior)
  self.assertEqual(e.exception.code,'ControlExportIdentity')
 def test_rehashed_wrong_repetition_refuses(self):
  self.row['repetition']=2;o.dump(self.report,self.row);self.prior[0].update(result_sha256=o.canonical(self.row),result_file_sha256=o.sha(self.report))
  with patch.object(o,'HERE',self.f.here):
   with self.assertRaises(o.Refusal)as e:o.bind_control(self.plan,self.case,self.leaf,self.prior)
  self.assertEqual(e.exception.code,'ControlIdentity')
 def test_rehashed_wrong_plan_refuses(self):
  self.row['plan_sha256']='0'*64;o.dump(self.report,self.row);self.prior[0].update(result_sha256=o.canonical(self.row),result_file_sha256=o.sha(self.report))
  with patch.object(o,'HERE',self.f.here):
   with self.assertRaises(o.Refusal)as e:o.bind_control(self.plan,self.case,self.leaf,self.prior)
  self.assertEqual(e.exception.code,'ControlIdentity')


class PublicConsumer(unittest.TestCase):
 def setUp(self):
  import tempfile
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.directory=Path(self.tmp.name);self.binary=HERE/'bin/producer';self.empty=(HERE/'candidates/empty.WP5').read_bytes()
 def call(self,raw):
  path=self.directory/'input.WP5';path.write_bytes(raw);return subprocess.run([str(self.binary),'-verify',str(path),'-require-preprint'],capture_output=True)
 def test_selected_scalar_and_owner_mutations_are_actual_consumer_refusals(self):
  # Full schema/header index and resource controls, not self-asserted passed data.
  for offset in [0,4,16,20,26,28,32,64,80+18,80+21,80+50,166+82,256+8,322]:
   raw=bytearray(self.empty);raw[offset]^=1
   with self.subTest(offset=offset):self.assertNotEqual(self.call(raw).returncode,0)
 def test_rehashed_cache_1172_still_fails_required_preprint(self):
  raw=bytearray(self.empty);raw[101:103]=bytes.fromhex('1172');self.assertNotEqual(self.call(raw).returncode,0)
 def test_rehashed_wrong_body_cannot_be_empty_candidate(self):
  directory=self.directory/'candidates';directory.mkdir();(directory/'empty.WP5').write_bytes(self.empty+b'X');(directory/'ascii.WP5').write_bytes((HERE/'candidates/ascii.WP5').read_bytes());v=json.loads((HERE/'candidates/provenance.json').read_text());v['classes'][0].update(bytes=len(self.empty)+1,sha256=o.sha(directory/'empty.WP5'));(directory/'provenance.json').write_text(json.dumps(v))
  def actual_product(*args):
   p=subprocess.run([str(self.binary),*map(str,args)],cwd=o.ROOT,capture_output=True);o.require(p.returncode==0,'PublicProducerRefusal',p.stderr.decode());return json.loads(p.stdout)
  with patch.object(o,'HERE',self.directory),patch.object(o,'product',side_effect=actual_product):
   with self.assertRaises(o.Refusal)as e:o.cases()
  self.assertEqual(e.exception.code,'CandidateBody')
 def test_no_fixture_or_resource_runtime_dependency(self):
  import shutil
  binary=self.directory/'generator';shutil.copyfile(self.binary,binary);binary.chmod(0o755);out=self.directory/'standalone';p=subprocess.run([str(binary),'-out',str(out)],cwd=self.directory,capture_output=True);self.assertEqual(p.returncode,0,p.stderr);self.assertEqual((out/'empty.WP5').read_bytes(),self.empty);self.assertEqual((out/'ascii.WP5').read_bytes(),(HERE/'candidates/ascii.WP5').read_bytes())
 def test_rehashed_changed_stored_version_fails_actual_reader(self):
  raw=bytearray(self.empty);raw[11]=2;path=self.directory/'changed-version.WP5';path.write_bytes(raw);p=subprocess.run([str(self.binary),'-verify',str(path)],capture_output=True)
  self.assertNotEqual(p.returncode,0);self.assertIn(b'wp51: UnsupportedVersion at 10 (stored version): expected 0/1',p.stderr)
 def test_rehashed_changed_profile_field_refuses_field_checker(self):
  raw=bytearray(self.empty);raw[256+10]=1;path=self.directory/'changed-pitch.WP5';path.write_bytes(raw);p=subprocess.run([str(self.binary),'-verify',str(path)],capture_output=True)
  self.assertEqual(p.returncode,0,p.stderr);native=json.loads(p.stdout)
  with self.assertRaises(o.Refusal)as e:o.profile_fields(path,native['inspection'])
  self.assertEqual(e.exception.code,'ProfileFieldMismatch');self.assertIn('display pitch',str(e.exception))
 def test_positive_native_consumer_and_real_reedit(self):
  self.assertEqual(self.call(self.empty).returncode,0);path=self.directory/'input.WP5';output=self.directory/'second.WP5';p=subprocess.run([str(self.binary),'-verify',str(path),'-require-preprint','-reedit-out',str(output)],capture_output=True);self.assertEqual(p.returncode,0,p.stderr);v=json.loads(p.stdout);self.assertTrue(v['second_real_edit']['same_loaded_birth']);self.assertTrue(output.is_file())


class EmptyPrint(unittest.TestCase):
 def probe(self,screen):
  p=types.SimpleNamespace(trace=[],exports=[]);p.q=types.SimpleNamespace(wait_for=lambda *a:None);p.key=lambda k:p.trace.append(k);p.type=lambda v:p.trace.append('type:'+v);p.capture=lambda label:screen;p.screen_step=lambda *a:None;p.setting=lambda *a:'Job Number: None Additional Jobs Not Shown: 0'
  return p
 def test_unknown_NoText_modal_halts_before_another_key(self):
  p=self.probe('No text to print\nDoc 1');quit=types.SimpleNamespace(exit_state=lambda s:'unknown')
  with self.assertRaises(o.Refusal)as e:o.print_empty(p,None,quit)
  self.assertEqual(e.exception.code,'EmptyPrintUnknownState');self.assertEqual(p.trace[-1],'1');self.assertEqual(p.exports,[])
 def test_main_empty_and_actual_completed_queue_declares_stream(self):
  p=self.probe('\nDoc 1');quit=types.SimpleNamespace(exit_state=lambda s:'main');o.print_empty(p,None,quit);self.assertEqual(p.exports,[('C46PRN.PRN','C46PRN.PRN')]);self.assertIn('shift-f7,4',p.trace)
 def test_absence_requires_failed_copy_and_actual_clean_directory(self):
  import tempfile
  with tempfile.TemporaryDirectory()as tmp:
   directory=Path(tmp)
   def call(argv,**kw):return subprocess.CompletedProcess(argv,1 if argv[0]=='mcopy'else 0,b'C:/OUT/OTHER.WP5\n',b'absent')
   with patch.object(o.subprocess,'run',side_effect=call):row=o.export_one(directory,directory,'C46PRN.PRN','print.PRN',True)
   self.assertFalse(row['present'])
   with patch.object(o.subprocess,'run',side_effect=call):
    with self.assertRaises(o.Refusal)as e:o.export_one(directory,directory,'C46PRE','native.WP5',False)
   self.assertEqual(e.exception.code,'RequiredExportFailed')
 def test_failed_directory_or_success_without_file_not_absence_proof(self):
  import tempfile
  with tempfile.TemporaryDirectory()as tmp:
   directory=Path(tmp)
   for code in [0,1]:
    with patch.object(o.subprocess,'run',side_effect=lambda argv,**kw:subprocess.CompletedProcess(argv,code,b'',b'failure')):
     with self.assertRaises(o.Refusal)as e:o.export_one(directory,directory,'C46PRN.PRN','print.PRN',True)
    self.assertEqual(e.exception.code,'RequiredExportMissing'if code==0 else'RequiredAbsenceUnproven')

class RawNormalClaim(unittest.TestCase):
 def test_DOS_looking_first_line_with_modal_is_not_exit(self):
  import tempfile
  with tempfile.TemporaryDirectory()as tmp:
   directory=Path(tmp);(directory/'clean-exit').mkdir();(directory/'clean-exit/screen.txt').write_text('C:\\WP51>\nSave document?')
   with self.assertRaises(o.Refusal)as e:o.normal_dos(directory)
   self.assertEqual(e.exception.code,'NormalDOSMissing')

if __name__=='__main__':unittest.main()
