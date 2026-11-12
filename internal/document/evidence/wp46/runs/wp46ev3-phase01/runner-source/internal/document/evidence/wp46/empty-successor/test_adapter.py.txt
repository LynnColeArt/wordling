"""Real-helper frame composition and isolated successor accounting/orchestration."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('wp46_successor_test_target',HERE/'adapter.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
sys.path.insert(0,str(HERE.parent.parent/'wp44'))
spec=importlib.util.spec_from_file_location('approved_wp44_integrity_fixture',HERE.parent.parent/'wp44/test_oracle.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)

class Frames(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.expected=a.expected_empty_status();cls.frame='\n'.join(['']*24+[cls.expected])+'\n';cls.session,_,_,cls.quit,_,_=a.old.helpers()
 def probe(self,submit=None,baseline=None,returned=None):
  p=types.SimpleNamespace(trace=[],exports=[],checks=[]);p.q=types.SimpleNamespace(wait_for=lambda *x:None);p.key=lambda k:p.trace.append(k);p.type=lambda text:p.trace.append('type:'+text);p.screen_step=lambda *x:None;p.setting=lambda *x:'Job Number: None Additional Jobs Not Shown: 0';p.check=lambda n,v:p.checks.append((n,v))
  p.capture=lambda label:baseline if label=='strict-empty-before-print'and baseline is not None else returned if label=='strict-empty-print-return'and returned is not None else submit if label=='strict-empty-submit-classifier'and submit is not None else self.frame
  return p
 def modal(self,text='No text to print',line=12):
  lines=self.frame.splitlines();lines[line]=' '*25+text;return '\n'.join(lines)+'\n'
 def test_actual_helpers_misclassify_modal_but_owned_guard_stops_before_next_key(self):
  modal=self.modal();self.assertTrue(self.session.main_document(modal));self.assertEqual(self.quit.exit_state(modal),'main');p=self.probe(modal)
  with self.assertRaises(a.Refusal)as e:a.print_empty(p,self.session,self.quit)
  self.assertEqual(e.exception.code,'EmptyPrintUnknownState');self.assertEqual(p.trace[-1],'1');self.assertNotIn('shift-f7,4',p.trace);self.assertEqual(p.exports,[])
 def test_exact_root_counterexample_refuses_with_actual_helper(self):
  screen=(HERE/'diagnosis/counterexample-screen.txt').read_text();self.assertTrue(self.session.main_document(screen));self.assertEqual(self.quit.exit_state(screen),'main')
  with self.assertRaises(a.Refusal)as e:a.strict_empty_frame(screen,self.expected)
  self.assertEqual(e.exception.code,'EmptyPrintUnknownState')
 def test_every_body_row_and_ruler_refuses_before_next_key(self):
  for row in range(24):
   with self.subTest(row=row):
    p=self.probe(self.modal('unqualified ruler/body/modal',row))
    with self.assertRaises(a.Refusal)as e:a.print_empty(p,self.session,self.quit)
    self.assertEqual(e.exception.code,'EmptyPrintUnknownState');self.assertEqual(p.trace[-1],'1');self.assertEqual(p.exports,[])
 def test_changed_name_Doc2_page_line_position_or_extra_status_refuses(self):
  for status in [self.expected.replace('C46PRE','C46FIN'),self.expected.replace('Doc 1','Doc 2'),self.expected.replace('Pg 1','Pg 2'),self.expected.replace('Ln 1"','Ln 2"'),self.expected.replace('Pos 1"','Pos 1.1"'),self.expected+' unknown']:
   frame='\n'.join(['']*24+[status])+'\n';self.assertTrue(self.session.main_document(frame));p=self.probe(frame)
   with self.assertRaises(a.Refusal)as e:a.print_empty(p,self.session,self.quit)
   self.assertEqual(e.exception.code,'EmptyPrintUnknownState');self.assertEqual(p.trace[-1],'1')
 def test_line_count_width_tabs_and_control_char_refuse(self):
  for frame in [self.frame+'\n',self.frame.replace('\n','',1),self.modal(' '*81),self.modal('\t'),self.modal('\x0c')]:
   with self.assertRaises(a.Refusal)as e:a.strict_empty_frame(frame,self.expected)
   self.assertEqual(e.exception.code,'EmptyPrintUnknownState')
 def test_unknown_before_menu_refuses_without_any_key(self):
  p=self.probe(baseline=self.modal('arbitrary unknown'))
  with self.assertRaises(a.Refusal):a.print_empty(p,self.session,self.quit)
  self.assertEqual(p.trace,[])
 def test_unknown_return_does_not_declare_export(self):
  p=self.probe(returned=self.modal('after-print unknown'))
  with self.assertRaises(a.Refusal):a.print_empty(p,self.session,self.quit)
  self.assertEqual(p.trace[-1],'f7');self.assertEqual(p.exports,[])
 def test_known_empty_frame_and_real_helpers_pass(self):
  p=self.probe();a.print_empty(p,self.session,self.quit);self.assertEqual(p.exports,[('C46PRN.PRN','C46PRN.PRN')]);self.assertIn('shift-f7,4',p.trace);self.assertTrue(all(x[1]for x in p.checks))

class Transition(unittest.TestCase):
 def setUp(self):self.plan={'transition_receipt_sha256':'receipt','transition':{'files':{'private-ledger.json':{'sha256':'old-ledger'}}},'attempts':[{'id':f'wp46ev2-empty-print-{mode}-r{r}','mode':mode,'repetition':r}for mode in ['control','candidate']for r in [1,2]]}
 def grant(self):
  ids=[x['id']for x in self.plan['attempts']];args=types.SimpleNamespace(grant_id='wp46ev2-phase01',attempt=ids);g={'authorized':True,'grant_id':args.grant_id,'plan_sha256':a.canonical(self.plan),'attempt_ids':ids,'maximum_aggregate_attempts':12,'authorization_note':'isolated offline test','transition_authorization':{'authorized_by_root':True,**a.transition_fields(self.plan)}};return args,g
 def test_missing_or_changed_root_transition_ack_refuses(self):
  args,g=self.grant();self.assertEqual(len(a.selected(args,self.plan,g)),4)
  for field,value in [('authorized_by_root',False),('old_accepted_complete',0),('old_accepted_complete',8.0),('cumulative_maximum_including_failures',4),('predecessor_ledger_sha256','wrong')]:
   bad=copy.deepcopy(g);bad['transition_authorization'][field]=value
   with self.assertRaises(a.Refusal)as e:a.selected(args,self.plan,bad)
   self.assertEqual(e.exception.code,'TransitionAuthorization')
 def test_old_ID_duplicate_subset_and_budget_rejected(self):
  args,g=self.grant()
  for ids in [['wp46-empty-print-control-r1'],[args.attempt[0]]*2]:
   args.attempt=ids;g['attempt_ids']=ids
   with self.assertRaises(a.Refusal)as e:a.selected(args,self.plan,g)
   self.assertEqual(e.exception.code,'GrantSelection')
 def test_new_ledger_budget_and_sticky_halt_cannot_reset_old8(self):
  good=a.empty_ledger(self.plan);self.assertEqual(a.validate_ledger(self.plan,good),[])
  for field,value in [('old_accepted_complete',0),('old_accepted_complete',8.0),('new_required_leaves',12),('cumulative_maximum_including_failures',16),('transition_receipt_sha256','wrong')]:
   bad=copy.deepcopy(good);bad[field]=value
   with self.assertRaises(a.Refusal)as e:a.validate_ledger(self.plan,bad)
   self.assertEqual(e.exception.code,'LedgerIdentity')
  bad=copy.deepcopy(good);bad['halted']=True
  with self.assertRaises(a.Refusal)as e:a.validate_ledger(self.plan,bad)
  self.assertEqual(e.exception.code,'PriorFailure')
 def test_failed_duplicate_old_or_overbudget_prior_rows_rejected(self):
  for rows in [[{'id':self.plan['attempts'][0]['id'],'outcome':'incomplete'}],[{'id':self.plan['attempts'][0]['id'],'outcome':'complete-observation'}]*2,[{'id':'wp46-empty-print-control-r1','outcome':'complete-observation'}],[{'id':'x'+str(i),'outcome':'complete-observation'}for i in range(5)]]:
   ledger=a.empty_ledger(self.plan);ledger['attempts']=rows
   with self.assertRaises(a.Refusal):a.validate_ledger(self.plan,ledger)
 def test_predecessor_modified_file_refuses_real_verifier(self):
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);original=root/'old.json';original.write_text('old accepted data');archive=root/'archive.json';archive.write_bytes(original.read_bytes());t={'files':{'old':{'original_path':str(original),'archive_path':'archive.json','size':original.stat().st_size,'sha256':a.sha(original)}}};original.write_text('mutated accepted data')
   with patch.object(a,'ROOT',root):
    with self.assertRaises(a.Refusal)as e:a.verify_predecessor(t)
   self.assertEqual(e.exception.code,'PredecessorIdentity')
 def test_no_allow_vm_refuses_before_check(self):
  with patch.object(a,'check',side_effect=AssertionError('must not evaluate')):
   with self.assertRaises(a.Refusal)as e:a.run(types.SimpleNamespace(allow_vm=False))
  self.assertEqual(e.exception.code,'AuthorizationRequired')

class Routing(unittest.TestCase):
 def setUp(self):
  self.fx=base.Orchestration('test_positive_complete_exports_two_fresh');self.fx.setUp();self.addCleanup(self.fx.doCleanups);f=self.fx
  class Probe:
   def __init__(self,q,out):self.out=out;self.exports=[('C46PRE','C46PRE.WP5'),('C46FIN','C46FIN.WP5'),('C46PRN.PRN','C46PRN.PRN')];self.trace=[];self.checks=[];self.settings=[]
  f.n.MutationProbe=Probe;(f.base/'predecessor.json').write_text('old8 accepted; isolated fixture')
  self.plan={'sources':[],'transition_receipt_sha256':'receipt','transition':{'files':{'private-ledger.json':{'archive_path':'predecessor.json','sha256':a.sha(f.base/'predecessor.json')}}},'cases':[{'id':'empty-print','candidate':'candidate','candidate_sha256':a.sha(f.base/'candidate'),'candidate_size':9}],'master':{n:a.sha(f.master/n)for n in ['boot.img','harddisk.img']},'ledger':str(f.private/'successor.json'),'attempts':[{'id':f'wp46ev2-empty-print-candidate-r{r}','case':'empty-print','mode':'candidate','repetition':r,'private_work':str(f.private/f'work{r}'),'qemu_argv':['qemu']}for r in [1,2]]}
 def copy(self,argv,**kw):
  self.fx.export_calls+=1;Path(argv[-1]).write_bytes(b'candidate'if argv[-2]=='::OUT/C46INPUT'else b'original-output');return subprocess.CompletedProcess(argv,0,b'',b'')
 def invoke(self,perform=None,predecessor=None):
  f=self.fx;grant=f.base/'grant.json';ids=[x['id']for x in self.plan['attempts']];grant.write_text(json.dumps({'authorized':True,'grant_id':'wp46ev2-test','plan_sha256':a.canonical(self.plan),'attempt_ids':ids,'maximum_aggregate_attempts':12,'authorization_note':'isolated fake guest/control, never product evidence','transition_authorization':{'authorized_by_root':True,**a.transition_fields(self.plan)}}));args=types.SimpleNamespace(allow_vm=True,grant=str(grant),grant_id='wp46ev2-test',attempt=ids)
  a.dump(f.here/'preflight.json',{'plan':self.plan,'plan_sha256':a.canonical(self.plan)})
  with patch.multiple(a,HERE=f.here,BASE=f.here,ROOT=f.base,check=lambda:self.plan,verify_predecessor=predecessor or(lambda *x:None),bind_control=lambda *x:None),patch.multiple(a.old,ROOT=f.base,helpers=lambda:(f.session,f.n,None,None,None,None),perform=perform or f.perform,qualify=lambda *x:{'isolated':True}),patch.multiple(a.old.guard,owned_identity=lambda *x:f.identity,same_identity=lambda *x:None,stopped=lambda *x,**kw:{'gone_or_same_zombie':True,'socket_absent':True}),patch.object(a.subprocess,'run',side_effect=self.copy):code=a.run(args)
  return code,json.loads((f.here/'runs/wp46ev2-test/run.json').read_text()),json.loads(Path(self.plan['ledger']).read_text())
 def test_actual_attempt_unknown_guard_halts_after_one_and_keeps_old8(self):
  def reject(*x):raise a.Refusal('EmptyPrintUnknownState','isolated observed unknown; no key')
  code,r,l=self.invoke(perform=reject);self.assertEqual(code,1);self.assertEqual(self.fx.count,1);self.assertFalse(r['complete']);self.assertTrue(l['halted']);self.assertEqual(l['old_accepted_complete'],8);self.assertEqual(r['cumulative_spent'],9);self.assertEqual(r['results'][0]['error_code'],'EmptyPrintUnknownState')
 def test_preboot_predecessor_failure_durable_halt_no_fresh(self):
  def reject(*x):raise a.Refusal('PredecessorIdentity','isolated old8 changed')
  code,r,l=self.invoke(predecessor=reject);self.assertEqual(self.fx.count,0);self.assertTrue(l['halted']);self.assertEqual(l['old_accepted_complete'],8);self.assertEqual(l['attempts'],[]);self.assertEqual(r['batch_error_code'],'PredecessorIdentity')
 def test_two_isolated_positive_attempts_keep_cumulative_accounting(self):
  code,r,l=self.invoke();self.assertEqual(code,0);self.assertEqual(self.fx.count,2);self.assertEqual(r['cumulative_spent'],10);self.assertEqual(l['old_accepted_complete'],8);self.assertFalse(l['halted'])

class EarlyAuthority(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.here=self.root/'successor';self.here.mkdir();self.private=self.root/'private';self.private.mkdir();self.original=self.root/'original';self.archive=self.root/'archive';self.archive.write_bytes(b'accepted');self.original.write_bytes(b'changed!')
  t={'old_accepted_complete':8,'new_required_leaves':4,'cumulative_maximum_including_failures':12,'old_plan_sha256':a.OLD_PLAN,'files':{'private-ledger.json':{'original_path':str(self.original),'archive_path':'archive','size':8,'sha256':a.sha(self.archive)}}};a.dump(self.here/'transition.json',t)
  self.plan={'transition_receipt_sha256':a.sha(self.here/'transition.json'),'transition':t,'ledger':str(self.private/'new.json'),'attempts':[{'id':'wp46ev2-empty-print-control-r1','mode':'control','repetition':1}],'sources':[]}
  a.dump(self.here/'preflight.json',{'plan':self.plan,'plan_sha256':a.canonical(self.plan)})
  self.args=types.SimpleNamespace(allow_vm=True,grant=str(self.root/'grant.json'),grant_id='wp46ev2-offline',attempt=[self.plan['attempts'][0]['id']]);self.grant={'authorized':True,'grant_id':self.args.grant_id,'plan_sha256':a.canonical(self.plan),'attempt_ids':self.args.attempt,'maximum_aggregate_attempts':12,'authorization_note':'isolated integrity control only','transition_authorization':{'authorized_by_root':True,**a.transition_fields(self.plan)}};a.dump(Path(self.args.grant),self.grant)
 def invoke(self):
  # check/plan/transition/verify_predecessor are all UNPATCHED.
  with patch.multiple(a,HERE=self.here,BASE=self.root,ROOT=self.root,PRIVATE=self.private),patch.object(a,'owned_attempt')as launch:
   code=a.run(self.args);self.assertFalse(launch.called);return code
 def test_actual_early_check_drift_sticky_after_restoration_zero_guests(self):
  self.assertEqual(self.invoke(),1);ledger=json.loads(Path(self.plan['ledger']).read_text());self.assertTrue(ledger['halted']);self.assertEqual(ledger['failure_code'],'PredecessorIdentity');self.assertEqual(ledger['attempts'],[]);self.assertEqual(ledger['old_accepted_complete'],8);self.assertEqual(ledger['cumulative_maximum_including_failures'],12)
  failure=json.loads((self.root/'runs'/self.args.grant_id/'authorized-prelaunch-failure.json').read_text());self.assertTrue(failure['durable_halt']);self.assertEqual(failure['cumulative_spent'],8);self.assertRegex(failure['recorded_at'],r'^20[0-9][0-9]-');self.original.write_bytes(b'accepted')
  with self.assertRaises(a.Refusal)as e:self.invoke()
  self.assertEqual(e.exception.code,'PriorFailure');self.assertEqual(json.loads(Path(self.plan['ledger']).read_text()),ledger)
 def test_unauthorized_or_malformed_never_writes_private_state(self):
  for field,value in [('authorized',False),('plan_sha256','wrong'),('maximum_aggregate_attempts',12.0),('transition_authorization',{})]:
   bad=copy.deepcopy(self.grant);bad[field]=value;a.dump(Path(self.args.grant),bad)
   with self.assertRaises(a.Refusal):self.invoke()
   self.assertEqual(list(self.private.iterdir()),[]);self.assertFalse((self.root/'runs').exists())
  Path(self.args.grant).write_text('{invalid')
  with self.assertRaises(json.JSONDecodeError):self.invoke()
  self.assertEqual(list(self.private.iterdir()),[])
 def test_halt_write_failure_never_claims_durability(self):
  real=a.dump
  def fail(path,value):
   if Path(path)==Path(self.plan['ledger']):raise OSError('isolated disk failure')
   return real(path,value)
  with patch.object(a,'dump',side_effect=fail):
   with self.assertRaises(a.Refusal)as e:self.invoke()
  self.assertEqual(e.exception.code,'HaltPersistenceFailed');self.assertFalse(Path(self.plan['ledger']).exists());self.assertFalse((self.root/'runs').exists())
 def test_authorized_archive_setup_failure_halts_without_guest(self):
  with patch.object(a,'check',return_value=self.plan),patch.object(a.shutil,'copyfile',side_effect=OSError('isolated archive copy failure')):
   self.assertEqual(self.invoke(),1)
  ledger=json.loads(Path(self.plan['ledger']).read_text());self.assertTrue(ledger['halted']);self.assertEqual(ledger['attempts'],[]);self.assertEqual(ledger['failure_code'],'OSError')

class ControlPins(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.plan={'frozen':'new successor'};self.leaf={'mode':'candidate','repetition':1};self.ident='wp46ev2-empty-print-control-r1';self.directory=self.root/'runs/grant'/self.ident;self.directory.mkdir(parents=True);(self.directory/'clean-exit').mkdir();(self.directory/'clean-exit/screen.txt').write_text('C:\\WP51>\n');self.raw=self.directory/'C46PRN.PRN';self.raw.write_bytes(b'full-stream')
  self.row={'id':self.ident,'case':'empty-print','mode':'control','repetition':1,'plan_sha256':a.canonical(self.plan),'exports':[{'name':'C46PRN.PRN','present':True,'path':str(self.raw),'size':11,'sha256':a.sha(self.raw)}]};self.report=self.directory/'result.json';a.dump(self.report,self.row);self.prior=[{'id':self.ident,'outcome':'complete-observation','grant_id':'grant','result_sha256':a.canonical(self.row),'result_file_sha256':a.sha(self.report)}]
 def test_exact_new_control_identity_and_actual_raw_bound(self):
  with patch.object(a,'BASE',self.root):pin=a.bind_control(self.plan,self.leaf,self.prior)
  self.assertEqual(pin['result_sha256'],a.canonical(self.row))
 def test_changed_raw_control_refuses_before_boot(self):
  self.raw.write_bytes(b'wrong-bytes')
  with patch.object(a,'BASE',self.root):
   with self.assertRaises(a.Refusal)as e:a.bind_control(self.plan,self.leaf,self.prior)
  self.assertEqual(e.exception.code,'ControlExportIdentity')
 def test_rehashed_wrong_new_plan_or_repetition_refuses(self):
  for key,value in [('plan_sha256','oldplan'),('repetition',2)]:
   row=copy.deepcopy(self.row);row[key]=value;a.dump(self.report,row);self.prior[0].update(result_sha256=a.canonical(row),result_file_sha256=a.sha(self.report))
   with patch.object(a,'BASE',self.root):
    with self.assertRaises(a.Refusal)as e:a.bind_control(self.plan,self.leaf,self.prior)
   self.assertEqual(e.exception.code,'ControlIdentity')

if __name__=='__main__':unittest.main()
