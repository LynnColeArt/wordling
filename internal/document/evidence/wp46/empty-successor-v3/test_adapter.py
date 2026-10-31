"""Real-helper frame composition and isolated successor accounting/orchestration."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import shutil
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
  screen=(HERE.parent/'empty-successor/diagnosis/counterexample-screen.txt').read_text();self.assertTrue(self.session.main_document(screen));self.assertEqual(self.quit.exit_state(screen),'main')
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
 def setUp(self):self.plan={'transition_receipt_sha256':'receipt','transition':{'failed_plan_sha256':'failed-plan','failed_files':{'ledger':{'original_path':'wp46-empty-v2-attempts.json','sha256':'failed-ledger','archive_path':'predecessor.json'}},'files':{'private-ledger.json':{'sha256':'old-ledger'}}},'attempts':[{'id':f'wp46ev3-empty-print-{mode}-r{r}','mode':mode,'repetition':r}for mode in ['control','candidate']for r in [1,2]]}
 def grant(self):
  ids=[x['id']for x in self.plan['attempts']];args=types.SimpleNamespace(grant_id='wp46ev3-phase01',attempt=ids);g={'authorized':True,'grant_id':args.grant_id,'plan_sha256':a.canonical(self.plan),'attempt_ids':ids,'maximum_aggregate_attempts':13,'authorization_note':'isolated offline test','transition_authorization':{'authorized_by_root':True,**a.transition_fields(self.plan)}};return args,g
 def test_missing_or_changed_root_transition_ack_refuses(self):
  args,g=self.grant();self.assertEqual(len(a.selected(args,self.plan,g)),4)
  for field,value in [('authorized_by_root',False),('old_accepted_complete',0),('old_accepted_complete',8.0),('old_incomplete',0),('old_incomplete',1.0),('cumulative_maximum_including_failures',12),('cumulative_maximum_including_failures',4),('predecessor_ledger_sha256','wrong')]:
   bad=copy.deepcopy(g);bad['transition_authorization'][field]=value
   with self.assertRaises(a.Refusal)as e:a.selected(args,self.plan,bad)
   self.assertEqual(e.exception.code,'TransitionAuthorization')
 def test_old_ID_duplicate_subset_and_budget_rejected(self):
  args,g=self.grant()
  for ids in [['wp46-empty-print-control-r1'],[args.attempt[0]]*2]:
   args.attempt=ids;g['attempt_ids']=ids
   with self.assertRaises(a.Refusal)as e:a.selected(args,self.plan,g)
   self.assertEqual(e.exception.code,'GrantSelection')
 def test_all_subsets_and_reordering_refuse_before_authorized_entry(self):
  args,g=self.grant();full=list(args.attempt)
  for ids in [[x]for x in full]+[full[:2],full[2:],list(reversed(full))]:
   args.attempt=ids;g['attempt_ids']=ids
   with self.assertRaises(a.Refusal)as e:a.selected(args,self.plan,g)
   self.assertEqual(e.exception.code,'GrantSelection')
 def test_new_ledger_budget_and_sticky_halt_cannot_reset_old8(self):
  good=a.empty_ledger(self.plan);self.assertEqual(a.validate_ledger(self.plan,good),[])
  for field,value in [('old_accepted_complete',0),('old_accepted_complete',8.0),('old_incomplete',0),('old_incomplete',1.0),('new_required_leaves',12),('cumulative_maximum_including_failures',16),('transition_receipt_sha256','wrong')]:
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
  original_init=Probe.__init__
  def probe_init(probe,q,out):
   original_init(probe,q,out)
   if '-control-'in out.name:probe.exports.insert(0,('C46SEED','C46SEED.WP5'))
  Probe.__init__=probe_init
  f.n.MutationProbe=Probe;(f.base/'predecessor.json').write_text('old8 accepted; isolated fixture')
  self.plan={'sources':[],'transition_receipt_sha256':'receipt','transition':{'failed_plan_sha256':'failed-plan','failed_files':{'ledger':{'original_path':'wp46-empty-v2-attempts.json','sha256':'failed-ledger','archive_path':'predecessor.json'}},'files':{'private-ledger.json':{'archive_path':'predecessor.json','sha256':a.sha(f.base/'predecessor.json')}}},'cases':[{'id':'empty-print','candidate':'candidate','candidate_sha256':a.sha(f.base/'candidate'),'candidate_size':9}],'master':{n:a.sha(f.master/n)for n in ['boot.img','harddisk.img']},'ledger':str(f.private/'successor.json'),'attempts':[{'id':f'wp46ev3-empty-print-{mode}-r{r}','case':'empty-print','mode':mode,'repetition':r,'private_work':str(f.private/f'{mode}{r}'),'qemu_argv':['qemu']}for mode in ['control','candidate']for r in [1,2]]}
 def copy(self,argv,**kw):
  self.fx.export_calls+=1;Path(argv[-1]).write_bytes(b'candidate'if argv[-2]=='::OUT/C46INPUT'else b'original-output');return subprocess.CompletedProcess(argv,0,b'',b'')
 def invoke(self,perform=None,predecessor=None):
  f=self.fx;self.plan['transition']['failed_files']['ledger']['sha256']=a.sha(f.base/'predecessor.json');grant=f.base/'grant.json';ids=[x['id']for x in self.plan['attempts']];grant.write_text(json.dumps({'authorized':True,'grant_id':'wp46ev3-test','plan_sha256':a.canonical(self.plan),'attempt_ids':ids,'maximum_aggregate_attempts':13,'authorization_note':'isolated fake guest/control, never product evidence','transition_authorization':{'authorized_by_root':True,**a.transition_fields(self.plan)}}));args=types.SimpleNamespace(allow_vm=True,grant=str(grant),grant_id='wp46ev3-test',attempt=ids)
  a.dump(f.here/'preflight.json',{'plan':self.plan,'plan_sha256':a.canonical(self.plan)})
  with patch.multiple(a,HERE=f.here,BASE=f.here,ROOT=f.base,check=lambda:self.plan,verify_predecessor=predecessor or(lambda *x:None),bind_control=lambda *x:None,qualify=lambda *x:{'isolated':True}),patch.multiple(a.old,ROOT=f.base,helpers=lambda:(f.session,f.n,None,None,None,None),perform=perform or f.perform,qualify=lambda *x:{'isolated':True}),patch.multiple(a.old.guard,owned_identity=lambda *x:f.identity,same_identity=lambda *x:None,stopped=lambda *x,**kw:{'gone_or_same_zombie':True,'socket_absent':True}),patch.object(a.subprocess,'run',side_effect=self.copy):code=a.run(args)
  return code,json.loads((f.here/'runs/wp46ev3-test/run.json').read_text()),json.loads(Path(self.plan['ledger']).read_text())
 def test_actual_attempt_unknown_guard_halts_after_one_and_keeps_old8(self):
  def reject(*x):raise a.Refusal('EmptyPrintUnknownState','isolated observed unknown; no key')
  code,r,l=self.invoke(perform=reject);self.assertEqual(code,1);self.assertEqual(self.fx.count,1);self.assertFalse(r['complete']);self.assertTrue(l['halted']);self.assertEqual(l['old_accepted_complete'],8);self.assertEqual(r['cumulative_spent'],10);self.assertEqual(r['results'][0]['error_code'],'EmptyPrintUnknownState')
 def test_preboot_predecessor_failure_durable_halt_no_fresh(self):
  def reject(*x):raise a.Refusal('PredecessorIdentity','isolated old8 changed')
  code,r,l=self.invoke(predecessor=reject);self.assertEqual(self.fx.count,0);self.assertTrue(l['halted']);self.assertEqual(l['old_accepted_complete'],8);self.assertEqual(l['attempts'],[]);self.assertEqual(r['batch_error_code'],'PredecessorIdentity')
 def test_four_isolated_positive_attempts_keep_cumulative_accounting(self):
  code,r,l=self.invoke();self.assertEqual(code,0);self.assertEqual(self.fx.count,4);self.assertEqual(r['cumulative_spent'],13);self.assertEqual(l['old_accepted_complete'],8);self.assertFalse(l['halted'])

class EarlyAuthority(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.here=self.root/'successor';self.here.mkdir();self.private=self.root/'private';self.private.mkdir();self.original=self.root/'original';self.archive=self.root/'archive';self.archive.write_bytes(b'accepted');self.original.write_bytes(b'changed!')
  t={'old_accepted_complete':8,'old_incomplete':1,'new_required_leaves':4,'cumulative_maximum_including_failures':13,'old_plan_sha256':a.OLD_PLAN,'failed_plan_sha256':'failed-plan','failed_files':{'ledger':{'original_path':'wp46-empty-v2-attempts.json','sha256':'failed-ledger','archive_path':'predecessor.json'}},'files':{'private-ledger.json':{'original_path':str(self.original),'archive_path':'archive','size':8,'sha256':a.sha(self.archive)}}};a.dump(self.here/'transition.json',t)
  self.plan={'transition_receipt_sha256':a.sha(self.here/'transition.json'),'transition':t,'ledger':str(self.private/'new.json'),'attempts':[{'id':f'wp46ev3-empty-print-{mode}-r{r}','mode':mode,'repetition':r}for mode in ['control','candidate']for r in [1,2]],'sources':[]}
  a.dump(self.here/'preflight.json',{'plan':self.plan,'plan_sha256':a.canonical(self.plan)})
  self.args=types.SimpleNamespace(allow_vm=True,grant=str(self.root/'grant.json'),grant_id='wp46ev3-offline',attempt=[x['id']for x in self.plan['attempts']]);self.grant={'authorized':True,'grant_id':self.args.grant_id,'plan_sha256':a.canonical(self.plan),'attempt_ids':self.args.attempt,'maximum_aggregate_attempts':13,'authorization_note':'isolated integrity control only','transition_authorization':{'authorized_by_root':True,**a.transition_fields(self.plan)}};a.dump(Path(self.args.grant),self.grant)
 def invoke(self):
  # check/plan/transition/verify_predecessor are all UNPATCHED.
  with patch.multiple(a,HERE=self.here,BASE=self.root,ROOT=self.root,PRIVATE=self.private),patch.object(a,'owned_attempt')as launch:
   code=a.run(self.args);self.assertFalse(launch.called);return code
 def test_actual_early_check_drift_sticky_after_restoration_zero_guests(self):
  self.assertEqual(self.invoke(),1);ledger=json.loads(Path(self.plan['ledger']).read_text());self.assertTrue(ledger['halted']);self.assertEqual(ledger['failure_code'],'PredecessorIdentity');self.assertEqual(ledger['attempts'],[]);self.assertEqual(ledger['old_accepted_complete'],8);self.assertEqual(ledger['cumulative_maximum_including_failures'],13)
  failure=json.loads((self.root/'runs'/self.args.grant_id/'authorized-prelaunch-failure.json').read_text());self.assertTrue(failure['durable_halt']);self.assertEqual(failure['cumulative_spent'],9);self.assertRegex(failure['recorded_at'],r'^20[0-9][0-9]-');self.original.write_bytes(b'accepted')
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
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.plan={'frozen':'new successor'};self.leaf={'mode':'candidate','repetition':1};self.ident='wp46ev3-empty-print-control-r1';self.directory=self.root/'runs/grant'/self.ident;self.directory.mkdir(parents=True);(self.directory/'clean-exit').mkdir();(self.directory/'clean-exit/screen.txt').write_text('C:\\WP51>\n');self.raw=self.directory/'C46PRN.PRN';self.raw.write_bytes(b'full-stream')
  self.row={'id':self.ident,'case':'empty-print','mode':'control','repetition':1,'plan_sha256':a.canonical(self.plan),'exports':[{'name':'C46PRN.PRN','present':True,'path':str(self.raw),'size':11,'sha256':a.sha(self.raw)}]};self.report=self.directory/'result.json';a.dump(self.report,self.row);self.prior=[{'id':self.ident,'outcome':'complete-observation','grant_id':'grant','result_sha256':a.canonical(self.row),'result_file_sha256':a.sha(self.report)}]
 def test_exact_new_control_identity_and_actual_raw_bound(self):
  with patch.object(a,'BASE',self.root):pin=a.verified_control(self.plan,1,self.prior)
  self.assertEqual(pin['result_sha256'],a.canonical(self.row))
 def test_changed_raw_control_refuses_before_boot(self):
  self.raw.write_bytes(b'wrong-bytes')
  with patch.object(a,'BASE',self.root):
   with self.assertRaises(a.Refusal)as e:a.verified_control(self.plan,1,self.prior)
  self.assertEqual(e.exception.code,'ControlExportIdentity')
 def test_rehashed_wrong_new_plan_or_repetition_refuses(self):
  for key,value in [('plan_sha256','oldplan'),('repetition',2)]:
   row=copy.deepcopy(self.row);row[key]=value;a.dump(self.report,row);self.prior[0].update(result_sha256=a.canonical(row),result_file_sha256=a.sha(self.report))
   with patch.object(a,'BASE',self.root):
    with self.assertRaises(a.Refusal)as e:a.verified_control(self.plan,1,self.prior)
   self.assertEqual(e.exception.code,'ControlIdentity')

class ActualFailedPredecessorEntry(unittest.TestCase):
 def test_real_check_old8_passes_then_changed_failed_source_halts_zero_and_retry_refuses(self):
  # Real complete accepted-old8 verification is retained; isolate only the
  # first failed-predecessor source and the NEW authority/output/ledger paths.
  sealed=a.check()
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);here=root/'proposal';here.mkdir();shutil.copytree(HERE/'history',here/'history');original=root/'old-source';archive=root/'archive';original.write_bytes(b'changed!');archive.write_bytes(b'accepted');t=copy.deepcopy(sealed['transition']);first=next(iter(t['failed_files']));t['failed_files'][first]={'original_path':str(original),'archive_path':str(archive),'size':8,'sha256':a.sha(archive)};a.dump(here/'transition.json',t);p=copy.deepcopy(sealed);p.update(transition=t,transition_receipt_sha256=a.sha(here/'transition.json'),ledger=str(root/'new-ledger'));a.dump(here/'preflight.json',{'plan':p,'plan_sha256':a.canonical(p)})
   ident=p['attempts'][0]['id'];args=types.SimpleNamespace(allow_vm=True,grant=str(root/'grant'),grant_id='wp46ev3-entry',attempt=[x['id']for x in p['attempts']]);g={'authorized':True,'grant_id':args.grant_id,'plan_sha256':a.canonical(p),'attempt_ids':args.attempt,'maximum_aggregate_attempts':13,'authorization_note':'isolated unpatched real check only, no guest authority','transition_authorization':{'authorized_by_root':True,**a.transition_fields(p)}};a.dump(Path(args.grant),g)
   with patch.multiple(a,HERE=here,BASE=root),patch.object(a,'owned_attempt')as launch:
    self.assertEqual(a.run(args),1);self.assertFalse(launch.called);l=json.loads(Path(p['ledger']).read_text());self.assertEqual(l['failure_code'],'FailedPredecessorIdentity');self.assertEqual(l['attempts'],[]);self.assertEqual(l['old_incomplete'],1);original.write_bytes(b'accepted')
    with self.assertRaises(a.Refusal)as e:a.run(args)
    self.assertEqual(e.exception.code,'PriorFailure');self.assertFalse(launch.called)

class ClosedRelations(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.d=HERE.parent/'runs/wp46ev2-phase01/wp46ev2-empty-print-control-r1';self.pre=self.d/'C46PRE.WP5';self.fin=self.d/'C46FIN.WP5';self.preinfo=a.old.product('-verify',self.pre);self.fininfo=a.old.product('-verify',self.fin)
 def relation(self,path=None,info=None):return a.closed_postprint(self.pre,path or self.fin,self.preinfo,info or self.fininfo)
 def mutant(self,raw):
  p=self.root/'mutant.WP5';p.write_bytes(raw);return p,a.old.product('-verify',p)
 def test_historical_sample_only_supports_prospective_H1_not_qualification(self):
  x=self.relation();self.assertEqual(x['prospective_outcome'],'H1-empty-counter-only-e72402');self.assertEqual(len(x['PRE_all72']),72);self.assertEqual(len(x['FIN_all72']),72);self.assertFalse(x['mutation_admitted']);self.assertEqual(x['exact_byte_differences'],[{'offset':74,'PRE':1,'FIN':2}]);self.assertEqual(self.fininfo['refusal'],'document: UnsupportedMetadata at token -1, span 74+1')
 def test_finitely_named_H2_counter_cache_only_integrity_fixture(self):
  raw=bytearray(self.fin.read_bytes());raw[117:119]=bytes.fromhex('1172');path,info=self.mutant(raw);x=self.relation(path,info);self.assertEqual(x['prospective_outcome'],'H2-empty-formatted-117202');self.assertEqual(len(x['FIN_all72']),72);self.assertFalse(info['admitted'])
 def test_rehashed_other_fields_cache_counter_flags_and_nonempty_refuse(self):
  for offset,value in [(74,0),(74,1),(74,3),(117,0),(118,0),(75,1),(66,8),(90,1),(126,1),(200,1),(300,1)]:
   with self.subTest(offset=offset,value=value):
    raw=bytearray(self.fin.read_bytes());raw[offset]=value;path,info=self.mutant(raw)
    with self.assertRaises(a.Refusal):self.relation(path,info)
  raw=self.fin.read_bytes()+b'X';path,info=self.mutant(raw)
  with self.assertRaises(a.Refusal):self.relation(path,info)
 def test_actual_readonly_identity_exact_refusal_graph_are_required(self):
  for field,value in [('admitted',0),('exact_no_edit',False),('origin_loaded',False),('refusal','document: UnsupportedMetadata at token -1, span 75+1'),('sha256','0'*64)]:
   info=copy.deepcopy(self.fininfo);info[field]=value
   with self.assertRaises(a.Refusal):self.relation(info=info)
  info=copy.deepcopy(self.fininfo);info['inspection']['Packets'][0]['Index']['Offset']+=1
  with self.assertRaises(a.Refusal)as e:self.relation(info=info)
  self.assertEqual(e.exception.code,'EmptyGraphChanged')
 def row(self,target):
  return {'mode':'control','exports':[{'name':'C46PRN.PRN','present':True,'path':str(target/'C46PRN.PRN'),'size':(target/'C46PRN.PRN').stat().st_size,'sha256':a.sha(target/'C46PRN.PRN')}]}
 def setup_target(self,name='wp46ev3-empty-print-control-r1'):
  target=self.root/name;target.mkdir();(target/'C46PRE.WP5').write_bytes(self.pre.read_bytes());(target/'C46FIN.WP5').write_bytes(self.fin.read_bytes());(target/'C46PRN.PRN').write_bytes(b'\r\r'+b'\r\n'*66);return target
 def test_actual_qualifier_prospective_integrity_control_not_original_acceptance(self):
  target=self.setup_target();x=a.qualify(target,{'id':'empty-print'},self.row(target));self.assertEqual(x['closed_relation']['prospective_outcome'],'H1-empty-counter-only-e72402');self.assertEqual(x['full_PRN_bytes'],134);self.assertTrue((target/'second-Go-edit.WP5').exists())
 def test_rehashed_printable_zero_absence_and_changed_control_stream_refuse(self):
  for index,raw in enumerate([b'',b'X'+b'\r'*133,b'\r\r'+b'\n\r'*66]):
   target=self.setup_target('variant'+str(index));(target/'C46PRN.PRN').write_bytes(raw)
   with self.assertRaises(a.Refusal)as e:a.qualify(target,{'id':'empty-print'},self.row(target))
   self.assertEqual(e.exception.code,'ControlExportIdentity'if raw==b''else'EmptyPrintStreamUnexpected')
  target=self.setup_target('absent');row={'mode':'control','exports':[{'name':'C46PRN.PRN','present':False,'path':str(target/'absent')} ]}
  with self.assertRaises(a.Refusal)as e:a.qualify(target,{'id':'empty-print'},row)
  self.assertEqual(e.exception.code,'EmptyPrintStreamUnexpected')
 def test_inconsistent_second_control_halts_after_observation(self):
  first=self.setup_target();row=self.row(first);row.update(outcome='complete-observation',required_output_qualification=a.qualify(first,{'id':'empty-print'},row));a.dump(first/'result.json',row)
  second=self.setup_target('wp46ev3-empty-print-control-r2');raw=bytearray((second/'C46FIN.WP5').read_bytes());raw[117:119]=bytes.fromhex('1172');(second/'C46FIN.WP5').write_bytes(raw)
  with self.assertRaises(a.Refusal)as e:a.qualify(second,{'id':'empty-print'},self.row(second))
  self.assertEqual(e.exception.code,'EmptyRepetitionInconsistent')

class SequenceEntry(unittest.TestCase):
 def setUp(self):
  self.fixture=Routing('test_four_isolated_positive_attempts_keep_cumulative_accounting');self.fixture.setUp();self.addCleanup(self.fixture.doCleanups);self.f=self.fixture.fx;self.plan=self.fixture.plan;self.starts=[];self.native=HERE.parent/'runs/wp46ev2-phase01/wp46ev2-empty-print-control-r1';schema='docs/research/continuation/native-constructor-design/schema.json';destination=self.f.base/schema;destination.parent.mkdir(parents=True);shutil.copyfile(a.ROOT/schema,destination)
 def invoke(self,scenario='matching',ids=None):
  f=self.f;p=self.plan;p['transition']['failed_files']['ledger']['sha256']=a.sha(f.base/'predecessor.json');ids=ids or a.frozen_order();args=types.SimpleNamespace(allow_vm=True,grant=str(f.base/'grant'),grant_id='wp46ev3-sequence',attempt=ids);g={'authorized':True,'grant_id':args.grant_id,'plan_sha256':a.canonical(p),'attempt_ids':ids,'maximum_aggregate_attempts':13,'authorization_note':'isolated entry integrity control, zero real guests','transition_authorization':{'authorized_by_root':True,**a.transition_fields(p)}};a.dump(Path(args.grant),g);a.dump(f.here/'preflight.json',{'plan':p,'plan_sha256':a.canonical(p)})
  def attempt(session,qmp,guest,n,case,leaf,target,work):
   self.starts.append(leaf['id']);row={'id':leaf['id'],'case':'empty-print','mode':leaf['mode'],'repetition':leaf['repetition'],'outcome':'complete-observation','normal_DOS':True,'guest_stopped':True,'exports_complete':True,'exports':[]};(target/'clean-exit').mkdir();(target/'clean-exit/screen.txt').write_text('C:\\WP51>\n')
   for name in ['C46PRE.WP5','C46FIN.WP5','C46PRN.PRN']:
    path=target/name;path.write_bytes((self.native/name).read_bytes())
    if scenario=='mixed'and leaf['mode']=='control'and leaf['repetition']==2 and name=='C46FIN.WP5':raw=bytearray(path.read_bytes());raw[117:119]=bytes.fromhex('1172');path.write_bytes(raw)
    row['exports'].append({'name':'C46PRN.PRN'if name.endswith('.PRN')else name[:-4],'present':True,'path':str(path),'size':path.stat().st_size,'sha256':a.sha(path)})
   return row
  actual=a.qualify
  def qualify(target,case,row,control):
   result=actual(target,case,row,control)
   if scenario=='missing'and row['mode']=='control'and row['repetition']==2:(target.parent/'wp46ev3-empty-print-control-r1/result.json').unlink()
   return result
  with patch.multiple(a,HERE=f.here,BASE=f.here,ROOT=f.base,check=lambda:p,verify_predecessor=lambda *x:None,owned_attempt=attempt,qualify=qualify),patch.object(a.old,'helpers',return_value=(f.session,f.n,None,None,None,None)):
   code=a.run(args)
  return code,json.loads((f.here/'runs'/args.grant_id/'run.json').read_text()),json.loads(Path(p['ledger']).read_text())
 def test_actual_entry_missing_control_refuses_before_candidate_consumption_or_boot(self):
  code,r,l=self.invoke('missing');self.assertEqual(code,1);self.assertEqual(self.starts,a.frozen_order()[:2]);self.assertEqual(len(l['attempts']),2);self.assertTrue(l['halted']);self.assertEqual(r['batch_error_code'],'ControlResultChanged');self.assertEqual(r['cumulative_spent'],11)
 def test_actual_entry_mixed_controls_halts_before_candidates(self):
  code,r,l=self.invoke('mixed');self.assertEqual(code,1);self.assertEqual(self.starts,a.frozen_order()[:2]);self.assertEqual(len(l['attempts']),2);self.assertTrue(l['halted']);self.assertEqual(r['results'][1]['qualification_error_code'],'EmptyRepetitionInconsistent')
 def test_actual_entry_matching_controls_all_four_pass_with_real_public_comparison(self):
  code,r,l=self.invoke();self.assertEqual(code,0);self.assertEqual(self.starts,a.frozen_order());self.assertEqual(len(l['attempts']),4);self.assertFalse(l['halted']);self.assertEqual(r['cumulative_spent'],13);self.assertTrue(all(x['required_output_qualification']['full_control_equal']for x in r['results'][2:]))
 def test_actual_entry_subset_rejected_before_any_output_or_ledger_write(self):
  with self.assertRaises(a.Refusal)as e:self.invoke(ids=a.frozen_order()[:2])
  self.assertEqual(e.exception.code,'GrantSelection');self.assertEqual(self.starts,[]);self.assertFalse(Path(self.plan['ledger']).exists());self.assertFalse((self.f.here/'runs').exists())

class LedgerPairs(unittest.TestCase):
 def setUp(self):
  self.entry=SequenceEntry('test_actual_entry_matching_controls_all_four_pass_with_real_public_comparison');self.entry.setUp();self.addCleanup(self.entry.doCleanups);self.entry.invoke();self.base=self.entry.f.here;self.plan=self.entry.plan;self.prior=json.loads(Path(self.plan['ledger']).read_text())['attempts']
 def test_missing_second_ledger_row_refuses(self):
  with patch.object(a,'BASE',self.base):
   with self.assertRaises(a.Refusal)as e:a.bind_control(self.plan,{'mode':'candidate','repetition':1},self.prior[:1])
  self.assertEqual(e.exception.code,'MissingControl')
 def test_rehashed_mixed_class_refuses_even_if_complete_rows_present(self):
  entry=self.prior[1];path=self.base/'runs'/entry['grant_id']/entry['id']/'result.json';row=json.loads(path.read_text());row['required_output_qualification']['closed_relation']['prospective_outcome']='H2-empty-formatted-117202';a.dump(path,row);entry.update(result_sha256=a.canonical(row),result_file_sha256=a.sha(path))
  with patch.object(a,'BASE',self.base):
   with self.assertRaises(a.Refusal)as e:a.bind_control(self.plan,{'mode':'candidate','repetition':1},self.prior)
  self.assertEqual(e.exception.code,'EmptyRepetitionInconsistent')
 def test_controls_split_across_grants_are_unsupported_even_when_matching(self):
  entry=self.prior[1];oldpath=self.base/'runs'/entry['grant_id']/entry['id'];entry['grant_id']='different';newpath=self.base/'runs/different'/entry['id'];newpath.parent.mkdir();shutil.copytree(oldpath,newpath)
  with patch.object(a,'BASE',self.base):
   with self.assertRaises(a.Refusal)as e:a.bind_control(self.plan,{'mode':'candidate','repetition':2},self.prior)
  self.assertEqual(e.exception.code,'ControlBatchMismatch')

if __name__=='__main__':unittest.main()
