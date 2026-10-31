"""Offline controls: real inherited helpers, replay transport only; NO original VM."""
import copy,importlib.util,json,subprocess,tempfile,time,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('wp48_ui333_adapter',HERE/'adapter.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)

class ReplayQMP:
 """No socket or process. Real MutationProbe/print_disk execute against recorded text."""
 def __init__(self,screen,column=9):self.screen=screen;self.sent=[];self.column=column;self.index=15
 def key(self,chord):self.sent.append(chord)
 def type(self,text):self.sent.append(('type',text))
 def wait_until(self,predicate,description,timeout=3):
  until=time.monotonic()+min(timeout,2)
  while time.monotonic()<until:
   if predicate(self.screen):return self.screen
   time.sleep(.01)
  raise AssertionError(description)
 def wait_for(self,text,**kw):
  if text not in self.screen:raise AssertionError('recorded frame lacks actual helper cue '+text)
  return self.screen
 def wait_absent(self,text,**kw):return self.screen
 def capture(self,directory):directory.mkdir(parents=True,exist_ok=True);(directory/'screen.txt').write_text(self.screen);return self.screen
 def execute(self,command):return {'running':False}
 def hmp(self,command):
  if command.startswith('o /b 0x3d4 '):self.index=int(command.rsplit(' ',1)[1]);return ''
  return hex({14:0,15:self.column}.get(self.index,0))

class MenuReplayQMP(ReplayQMP):
 """Recorded approved46 menu responses; only submitted frame is a negative mutant."""
 def __init__(self,submitted):
  super().__init__(a.MENU_PINS['menu'].read_text());self.submitted=submitted;self.f7s=0
 def key(self,chord):
  super().key(chord)
  states={'s':'list','3':'edit','2':'ports','8':'path','ret':'accepted'}
  if chord in states:self.screen=a.MENU_PINS[states[chord]].read_text()
  elif chord=='f7':self.f7s+=1;self.screen=a.MENU_PINS['list'if self.f7s==1 else'menu'].read_text()
  elif chord=='1':self.screen=self.submitted

class Tests(unittest.TestCase):
 def refused(self,fn,code=None):
  with self.assertRaises(a.Refusal)as result:fn()
  if code:self.assertEqual(result.exception.code,code)
 def test_exact_real_UI_and_public_consumer(self):
  row=a.provenance();self.assertEqual(row['body_hex'],a.TEXT.encode().hex());self.assertTrue(row['admitted']);self.assertEqual(row['bytes'],333)
 def test_real_normal_baseline_and_prospective_Reveal(self):
  normal=a.FRAME_PINS['normal9'].read_text();self.assertTrue(a.strict_frame(normal,'C46INPUT',pos='1.9')['actual_main_document'])
  old=a.FRAME_PINS['reveal8'].read_text();self.assertEqual(a.expected_frame('C46INPUT','G43ASCII',reveal=True),old)
  nine=a.expected_frame('C48INPUT',reveal=True);proof=a.strict_frame(nine,'C48INPUT',reveal=True);self.assertEqual(proof['actual_exit_state'],'unknown');self.assertFalse(proof['actual_main_document']);self.assertTrue(proof['prospective_Reveal9_not_prior_observation'])
 def test_every_full_frame_mutant_refuses_before_actual_probe_key(self):
  session,n,fields,quit_module,layout,genesis=a.old.helpers()
  for view in [False,True]:
   good=a.expected_frame('C48PRE',pos='1'if view else'1.9',reveal=view);rows=a.screen_rows(good)
   mutations={}
   for label,index,value in [('centered-modal',5,'                      ERROR: Cannot open file'),('wrong-doc',11 if view else 24,rows[11 if view else 24].replace('Doc 1','Doc 2')),('wrong-name',11 if view else 24,rows[11 if view else 24].replace('C48PRE','WRONG')),('wrong-status',11 if view else 24,rows[11 if view else 24].replace('Pg 1','Pg 2')),('wrong-body',0,'G43ASCIJZ')]:
    changed=rows.copy();changed[index]=value;mutations[label]='\n'.join(changed)+'\n'
   if view:
    changed=rows.copy();changed[12]=changed[12].replace('\x1e','x',1);mutations['ruler']='\n'.join(changed)+'\n'
   mutations['truncated']='\n'.join(rows[:-1])+'\n'
   for label,screen in mutations.items():
    with self.subTest(view=view,mutation=label),tempfile.TemporaryDirectory()as tmp:
     q=ReplayQMP(screen,0 if view else 9);p=a.probe_class(n)(q,Path(tmp))
     # Executes actual inherited MutationProbe.capture/SessionProbe VGA capture.
     def act():a.assert_frame(p,'before-real-key','C48PRE',pos='1'if view else'1.9',reveal=view);p.key('alt-f3'if view else'shift-f7')
     self.refused(act);self.assertEqual(q.sent,[])
 def test_actual_print_helper_cannot_send_queue_key_after_unknown_submit(self):
  session,n,fields,quit_module,layout,genesis=a.old.helpers();rows=a.screen_rows(a.expected_frame('C48PRE',pos='1.9'));rows[8]='                     No text selected';screen='\n'.join(rows)+'\n'
  self.assertTrue(session.main_document(screen));self.assertEqual(quit_module.exit_state(screen),'main')
  with tempfile.TemporaryDirectory()as tmp:
   q=MenuReplayQMP(screen);p=a.probe_class(n)(q,Path(tmp));self.refused(lambda:layout.print_disk(p,'C48PRN'),'UnknownFrame');self.assertIn('1',q.sent);self.assertNotIn('4',q.sent)
 def test_wrong_cursor_refuses_before_key(self):
  _,n,*_=a.old.helpers()
  with tempfile.TemporaryDirectory()as tmp:
   q=ReplayQMP(a.expected_frame('C48INPUT'),9);p=a.probe_class(n)(q,Path(tmp));self.refused(lambda:a.assert_frame(p,'input','C48INPUT'),'CursorFrameMismatch');self.assertEqual(q.sent,[])
 def test_exact_full_nonempty_postprint_from_approved46(self):
  pre=a.old.product('-verify',a.BASE/'C46PRE.WP5','-require-preprint');post=a.old.product('-verify',a.BASE/'C46FIN.WP5');r=a.postprint_relation(a.BASE/'C46PRE.WP5',a.BASE/'C46FIN.WP5',pre,post);self.assertEqual(len(r['PRE_all72']),72);self.assertEqual(len(r['FIN_all72']),72);self.assertFalse(r['mutation_permission'])
  with tempfile.TemporaryDirectory()as tmp:
   raw=bytearray((a.BASE/'C46FIN.WP5').read_bytes());raw[-1]^=1;p=Path(tmp)/'changed';p.write_bytes(raw);self.refused(lambda:a.postprint_relation(a.BASE/'C46PRE.WP5',p,pre,post),'PostprintWholeBytes')
 def test_ledger_type_order_failure_cap_refusals(self):
  p={'x':1};base=a.empty_ledger(p);self.assertEqual(a.ledger_ok(p,base),[])
  for change in [{'halted':True},{'maximum':True},{'maximum':5},{'plan_sha256':'wrong'},{'attempts':[{'id':a.ids()[1],'outcome':'complete-observation'}]},{'attempts':[{'id':a.ids()[0],'outcome':'incomplete'}]}]:
   row=copy.deepcopy(base);row.update(change);self.refused(lambda:a.ledger_ok(p,row))
 def test_grant_exact_fields_false_cap_order_argv_and_plan(self):
  p={'x':1};args=[str(HERE/'adapter.py'),'run','--allow-vm','--grant','/tmp/wordling-WP48-z-root-grant.json'];g={'authorized':True,'grant_id':a.GRANT_ID,'plan_sha256':a.canonical(p),'attempt_ids':a.ids(),'maximum_attempts_including_failures':4,'authorization_note':'TEST ONLY; no execution','argv':[a.sys.executable,*args]};a.grant(args,p,g)
  for k,v in [('authorized',False),('maximum_attempts_including_failures',True),('maximum_attempts_including_failures',5),('attempt_ids',a.ids()[::-1]),('plan_sha256','wrong'),('argv',['wrong']),('authorization_note','')]:
   row=copy.deepcopy(g);row[k]=v;self.refused(lambda:a.grant(args,p,row),'GrantMismatch')
  row=copy.deepcopy(g);row['extra']=True;self.refused(lambda:a.grant(args,p,row),'GrantMismatch')
 def test_stopped_extraction_requires_positive_stop_and_exact_roster(self):
  row={'guest_stopped':False};self.refused(lambda:a.extract(Path('/missing'),Path('/missing'),SimpleNamespace(exports=[]),row,{'mode':'control'},None),'StopUnproven')
  row={'guest_stopped':True};session=SimpleNamespace(settings_snapshot=lambda *x:[]);self.refused(lambda:a.extract(Path('/missing'),Path('/missing'),SimpleNamespace(exports=[]),row,{'mode':'control'},session),'ExportRoster')
 def test_durable_halt_has_zero_fabricated_starts(self):
  with tempfile.TemporaryDirectory()as tmp:
   path=Path(tmp);p={'ledger':str(path/'private-ledger.json')};l=a.empty_ledger(p);r={'results':[]};a.halt(p,l,r,a.Refusal('SourceDrift','test'),path/'out');self.assertEqual(json.loads((path/'private-ledger.json').read_text())['halted'],True);self.assertEqual(json.loads((path/'out/run.json').read_text())['charged_attempts_including_failures'],0);self.refused(lambda:a.ledger_ok(p,l),'LedgerIdentity')
 def test_no_implicit_VM_default(self):
  result=subprocess.run([a.sys.executable,str(HERE/'adapter.py'),'run','--grant','/missing'],capture_output=True,text=True);self.assertNotEqual(result.returncode,0);self.assertIn('default offline',result.stderr)
 def test_control_gate_rejects_absent_or_incomplete_before_input(self):
  p={'public_output':'docs/research/continuation/new-session/interop-z-01/ABSENT'}
  self.refused(lambda:a.control_rows(p,[]),'MissingControl');self.refused(lambda:a.control_rows(p,[{'id':a.ids()[0],'outcome':'incomplete'}]),'MissingControl')

 def test_source_plan_rehash_and_profile_forgery_refuse(self):
  original=a.check()
  for key in ['profile_sha256','sources','candidate']:
   p=copy.deepcopy(original)
   if key=='profile_sha256':p[key]='0'*64
   elif key=='sources':p[key][0]['sha256']='0'*64
   else:p[key]['sha256']='0'*64
   self.refused(lambda:a.verify_plan(p),'SealedPlanIdentity')
 def test_missing_and_tampered_real_candidate_refuse_before_reader(self):
  with tempfile.TemporaryDirectory()as tmp:
   p=Path(tmp)/'candidate';raw=(a.ROOT/a.CANDIDATE).read_bytes();p.write_bytes(raw[:-1]+b'Q')
   with patch.object(a,'CANDIDATE',str(p)):
    self.refused(a.provenance,'CandidateIdentity')
   with patch.object(a,'CANDIDATE',str(Path(tmp)/'MISSING')):
    with self.assertRaises(FileNotFoundError):a.provenance()
 def test_positive_old_actual_owned_stop_and_mutants(self):
  row=json.loads((a.BASE.parent/'wp46-ascii-edit-control-r1/result.json').read_text());ident=row['owned_start_identity'];work=str(Path(ident['private_disks'][0]).parent);leaf={'qemu_argv':row['qemu_argv'],'private_work':work}
  before=Path(work)/'settings-before.SET';settings={'private_path':str(before),'size':before.stat().st_size,'sha256':a.sha(before)};row['settings_before']=settings;row['master_before']=row['master_after'];row['physical_guard_released']=True;row['guard_release_utc']='TEST-only existing released source proof'
  p={'master':row['master_after'],'socket':ident['socket'],'preboot_resources':[{'path':'WP51/WP{WP}.SET','size':settings['size'],'sha256':settings['sha256']}]};self.assertTrue(a.custody_record(p,leaf,row))
  for field,value in [('owned_start_identity',{}),('stop_method','Host containment'),('stop_proof',{}),('master_after',{}),('settings_before',{}),('physical_guard_released',False)]:
   changed=copy.deepcopy(row);changed[field]=value;self.refused(lambda:a.custody_record(p,leaf,changed),'ControlCustody')
  changed=copy.deepcopy(row);changed['stop_proof']['observations'][-1]['socket_present']=True;self.refused(lambda:a.custody_record(p,leaf,changed),'ControlCustody')
  changed=copy.deepcopy(row);changed['stop_proof']['observations'][-1]['observation_complete_monotonic']=changed['stop_proof']['observations'][-1]['deadline_monotonic']+1;self.refused(lambda:a.custody_record(p,leaf,changed),'ControlCustody')

 def test_whole_PRN_tamper_actual_reader_and_export_failure(self):
  import shutil
  with tempfile.TemporaryDirectory()as tmp:
   directory=Path(tmp)
   for old,new in [('C46PRE.WP5','C48PRE.WP5'),('C46FIN.WP5','C48FIN.WP5'),('C46PRN.PRN','C48PRN.PRN')]:shutil.copyfile(a.BASE/old,directory/new)
   stream=directory/'C48PRN.PRN';stream.write_bytes(stream.read_bytes()+b'X')
   self.refused(lambda:a.qualify(directory,{'mode':'candidate'},emit_Q=False),'FullPRNMismatch')
   session=SimpleNamespace(settings_snapshot=lambda *args:[]);probe=SimpleNamespace(exports=[('C48PRE','C48PRE.WP5'),('C48FIN','C48FIN.WP5'),('C48PRN.PRN','C48PRN.PRN')])
   self.refused(lambda:a.extract(directory/'missing-private-disk',directory,probe,{'guest_stopped':True},{'mode':'candidate'},session),'RequiredExportFailed')

if __name__=='__main__':unittest.main(verbosity=2)
