"""Actual owned entry/attempt integrity tests. All writes use isolated temp dirs."""
import sys
sys.dont_write_bytecode=True
import contextlib,copy,json,tempfile,types,unittest
from pathlib import Path
from unittest.mock import patch
import oracle,protocol,frames,recipes

class Trace(unittest.TestCase):
 def test_full_planned_protocol_budgets_and_exact_roster(self):
  for index in range(4):
   for clear,reload in ([(False,False)]if index<2 else[(False,False),(False,True),(True,False),(True,True)]):
    obs=protocol.preview(index,clear,reload);self.assertLessEqual(len(obs['receipts']),240);self.assertEqual(obs['receipts'][-1]['expected'],{'kind':'dos'});self.assertEqual(obs['body'],recipes.EXPECTED[index][1]);self.assertEqual(len([x for x in obs['receipts']if 'mode_observed'in x]),3)
    for receipt in obs['receipts']:
     spec=receipt['expected'];frames.check(frames.expected(spec),spec,{'row':0,'column':spec['gap']}if spec['kind']in ['normal','reveal']else None)
 def test_missing_duplicate_or_unpinned_exports_cannot_qualify(self):
  for exports in [[],[{'name':'H51S0','path':'/foreign'}]*4]:
   with self.assertRaises(frames.Refusal)as e:oracle.qualify(Path('/isolated'),{'exports':exports},{},{},[])
   self.assertEqual(e.exception.code,'ExportRoster')
 def test_reported_recipe_cannot_replace_complete_state_trace(self):
  leaf=recipes.leaves(Path('/unused'))[0];obs=protocol.preview(0);obs['receipts'][0]['expected']={'kind':'dos'}
  with self.assertRaises(frames.Refusal)as e:oracle.verify_observations(Path('/unused'),{'observations':obs},leaf)
  self.assertEqual(e.exception.code,'OperationTraceMismatch')
 def test_unqualified_grouped_key_refused_before_dispatch(self):
  class P(protocol.Protocol):
   def capture(self,spec,label):pass
  core=types.SimpleNamespace(key=lambda k:self.fail('no grouped dispatch'))
  with self.assertRaises(frames.Refusal)as e:P(core).step('f7,n',{}, {},'fault')
  self.assertEqual(e.exception.code,'UnqualifiedKeyGroup')

class Attempt(unittest.TestCase):
 def exercise(self,fault):
  with tempfile.TemporaryDirectory()as temp:
   base=Path(temp);target=base/'target';target.mkdir();qmp=types.SimpleNamespace(SOCKET=base/'socket',QMP=lambda:contextlib.nullcontext(None));work=base/'private';argv=['frozen-qemu'];leaf={'id':'isolated','case':'isolated','repetition':1,'class_index':0,'qemu_argv':argv};calls=[]

   def fresh(*args):
    calls.append('fresh_start');session.QMP_AUDIT_FILE.write_text('{"isolated-integrity-fixture":true}\n');return argv
   session=types.SimpleNamespace(fresh_start=fresh,stop_owned=lambda *a:(calls.append('normal-stop')or('containment'if fault=='containment'else 'QMP quit; own socket terminated')),settings_snapshot=lambda *a:{'metadata':'only'});core=types.SimpleNamespace(exports=[(x,x)for x in ['H51S0.WP5','H51S1.WP5','H51FIN.WP5','H51PRN.PRN']],trace=[])
   class UI:
    def __init__(self,p):self.receipts=[{'capture':'last','expected':{'kind':'dos'}}]
    def perform(self,index):
     if fault=='ui':raise frames.Refusal('UnknownFrame','actual recipe state unknown')
     d=target/'last';d.mkdir();(d/'screen.txt').write_text(frames.expected({'kind':'dos'}));return {'integrity_fixture':True}
   def identity(*args):
    if fault=='missingPID':raise frames.Refusal('MissingOwnedPID','positive PID absent')
    return {'isolated-test':True}
   def stop(*args,**kwargs):
    calls.append('poll')
    if fault=='stop':raise frames.Refusal('OwnedStopDeadline','actual stop proof missing')
    return {'bounded':'actual test seam'}
   def exp(work,target,name,host):
    calls.append('export')
    if fault=='export':raise frames.Refusal('RequiredExportMissing',name)
    return {'sha256':oracle.H1,'size':324}
   with patch.object(oracle.guard,'owned_identity',side_effect=identity),patch.object(oracle.guard,'validate_stop_identity'),patch.object(oracle.guard,'same_identity'),patch.object(oracle.guard,'stopped',side_effect=stop),patch.object(protocol,'Protocol',UI),patch.object(oracle,'export',side_effect=exp):
    row=oracle.attempt(session,qmp,types.SimpleNamespace(),types.SimpleNamespace(MutationProbe=lambda *a:core),leaf,target,work,{})
   self.assertEqual(calls.count('fresh_start'),1)
   if fault:
    self.assertEqual(row['outcome'],'incomplete')
    if fault in ['missingPID','stop','containment','ui']:self.assertNotIn('export',calls);self.assertFalse(row.get('exports_complete',False))
   else:self.assertEqual(row['outcome'],'complete-observation');self.assertTrue(row['guest_stopped']and row['normal_DOS']and row['exports_complete']);self.assertLess(calls.index('poll'),calls.index('export'))
   if fault in ['containment','stop']:self.assertFalse(row['guest_stopped'])
   if fault=='containment':self.assertNotIn('poll',calls)
   if fault=='export':self.assertEqual(row['extraction_error_code'],'RequiredExportMissing');self.assertEqual(calls.count('export'),1)
   return row
 def test_exact_normal_stop_then_exports_positive_integrity_fixture(self):self.exercise(None)
 def test_missing_positivePID_no_extract(self):self.exercise('missingPID')
 def test_bounded_stop_failure_no_extract(self):self.exercise('stop')
 def test_containment_not_normal_stopped_no_extract(self):self.exercise('containment')
 def test_unknownUI_no_extract_even_owned_stop(self):self.exercise('ui')
 def test_required_export_first_failure_incomplete(self):self.exercise('export')
 def test_actual_mcopy_nonzero_missing_and_oversize_refuse(self):
  with tempfile.TemporaryDirectory()as t:
   for mode in ['exit','exit-file','missing','oversize','empty']:
    def mcopy(argv,**kw):
     if mode in ['oversize','empty','exit-file']:Path(argv[-1]).write_bytes(b'x'*65537 if mode=='oversize'else b'x'if mode=='exit-file'else b'')
     return types.SimpleNamespace(returncode=1 if mode in ['exit','exit-file']else 0)
    with patch.object(oracle.subprocess,'run',side_effect=mcopy):
     with self.assertRaises(frames.Refusal)as e:oracle.export(Path(t),Path(t),mode,mode)
    self.assertEqual(e.exception.code,'RequiredExportMissing')

class StopWitness(unittest.TestCase):
 def actual(self):
  directory=oracle.ROOT/'internal/document/evidence/wp46/runs/wp46ev3-phase01';row=copy.deepcopy(json.loads((directory/'run.json').read_text())['results'][0]);target=directory/row['id'];wire=target/'qmp-wire.jsonl';row['stop_wire']={'path':str(wire),'size':wire.stat().st_size,'sha256':oracle.sha(wire)};identity=row['owned_start_identity'];leaf={'qemu_argv':row['qemu_argv'],'private_work':str(Path(identity['private_disks'][0]).parent)};p={'socket':identity['socket'],'tools':[{'name':'qemu-system-i386','path':identity['executable']}]};return target,row,leaf,p
 def test_actual_approved_original_stop_witness_replayed_not_WP51_observation(self):
  target,row,leaf,p=self.actual();self.assertTrue(oracle.verify_stop(target,row,leaf,p)['actual_wire_quit'])
 def test_passed_booleans_without_actual_bound_stop_wire_refuse(self):
  target,row,leaf,p=self.actual()
  for kind,code in [('proof','StopWitnessMissing'),('PID','MissingOwnedPID'),('ticks','StopWitnessMissing'),('argv','StopLaunchIdentity'),('socket','MissingOwnedIdentity'),('method','StopWitnessMissing'),('wire','WireIdentity'),('terminal','StopTerminalMissing')]:
   bad=copy.deepcopy(row)
   if kind=='proof':bad.pop('stop_proof')
   if kind=='PID':bad['owned_start_identity']['pid']=0
   if kind=='ticks':bad['owned_start_identity']['startticks']='999'
   if kind=='argv':bad['owned_start_identity']['argv'].append('foreign')
   if kind=='socket':bad['owned_start_identity']['socket']='/foreign/socket'
   if kind=='method':bad['stop_method']='host containment'
   if kind=='wire':bad['stop_wire']['path']='/foreign/wire'
   if kind=='terminal':bad['stop_observations'][-1]['socket_present']=True;bad['stop_proof']['observations'][-1]['socket_present']=True
   with self.subTest(kind=kind):
    with self.assertRaises(Exception)as e:oracle.verify_stop(target,bad,leaf,p)
    self.assertEqual(e.exception.code,code)

 def test_raw_QMP_rehashed_missing_quit_and_tamper_refuse(self):
  target,row,leaf,p=self.actual()
  with tempfile.TemporaryDirectory()as t:
   directory=Path(t);wire=directory/'qmp-wire.jsonl';original=(target/'qmp-wire.jsonl').read_bytes();wire.write_bytes(original);row['stop_wire']={'path':str(wire),'size':len(original),'sha256':oracle.sha(wire)};oracle.verify_stop(directory,row,leaf,p);wire.write_bytes(original+b' ')
   with self.assertRaises(Exception)as e:oracle.verify_stop(directory,row,leaf,p)
   self.assertEqual(e.exception.code,'ControlExportIdentity');events=[json.loads(line)for line in original.splitlines()];events=[event for event in events if json.loads(bytes.fromhex(event['raw_hex'])).get('execute')!='quit'];wire.write_text(''.join(json.dumps(x)+'\n'for x in events));row['stop_wire'].update(size=wire.stat().st_size,sha256=oracle.sha(wire))
   with self.assertRaises(frames.Refusal)as e:oracle.verify_stop(directory,row,leaf,p)
   self.assertEqual(e.exception.code,'NormalQMPMissing')

class Entry(unittest.TestCase):
 def setup_entry(self,base):
  p={'attempts':recipes.leaves(base),'ledger':str(base/'ledger.json'),'sources':[],'master':{'harddisk.img':oracle.sha(base/'harddisk.img')},'socket':str(base/'socket')};args=types.SimpleNamespace(allow_vm=True,grant_id='wp51-isolated',grant=str(base/'grant.json'),attempt=[x['id']for x in p['attempts']]);g={'authorized':True,'grant_id':args.grant_id,'attempt_ids':args.attempt,'plan_sha256':oracle.canonical(p),'maximum_new_attempts_including_failures':8,'historical46_spent_unchanged':13,'authorization_note':'isolated integrity fixture; no guest authority'};oracle.dump(base/'preflight.json',{'plan':p});oracle.dump(base/'grant.json',g);return p,args
 def test_actual_check_early_source_failure_zero_guest_durable_no_resume(self):
  with tempfile.TemporaryDirectory()as t:
   base=Path(t);(base/'harddisk.img').write_bytes(b'master');bad=base/'source';bad.write_bytes(b'bad');p,args=self.setup_entry(base)
   with patch.object(oracle,'HERE',base),patch.object(oracle,'SOURCE',bad),patch.object(oracle,'attempt',side_effect=AssertionError('no guest')):
    self.assertEqual(oracle.run(args),1);ledger=json.loads((base/'ledger.json').read_text());self.assertEqual(ledger['attempts'],[]);self.assertTrue(ledger['halted']);self.assertEqual(ledger['failure_code'],'InitialH1Identity');bad.write_bytes(b'restored-but-plan-already-halted')
    with self.assertRaises(frames.Refusal)as e:oracle.run(args)
    self.assertEqual(e.exception.code,'ExistingAccounting')
 def test_malformed_unauthorized_and_subset_no_private_writes(self):
  with tempfile.TemporaryDirectory()as t:
   base=Path(t);(base/'harddisk.img').write_bytes(b'master');p,args=self.setup_entry(base)
   for mode in ['unauthorized','subset','malformed']:
    g=json.loads((base/'grant.json').read_text());g['authorized']=False if mode=='unauthorized'else True;oracle.dump(base/'grant.json',g);args.attempt=[x['id']for x in p['attempts']][:1 if mode=='subset'else 8]
    if mode=='malformed':(base/'grant.json').write_text('{')
    with patch.object(oracle,'HERE',base):
     with self.assertRaises((frames.Refusal,json.JSONDecodeError)):oracle.run(args)
    self.assertFalse((base/'ledger.json').exists());self.assertFalse((base/'runs').exists())
 def test_first_incomplete_or_master_drift_one_attempt_and_halt(self):
  for fault in ['incomplete','master','source','lock']:
   with self.subTest(fault=fault),tempfile.TemporaryDirectory()as t:
    base=Path(t);(base/'harddisk.img').write_bytes(b'master');p,args=self.setup_entry(base);calls=[];qmp=types.SimpleNamespace(SOCKET=base/'socket');guest=types.SimpleNamespace(MASTER=base)
    def attempt(*args):
     calls.append('attempt')
     if fault=='master':(base/'harddisk.img').write_bytes(b'changed')
     return {'id':p['attempts'][0]['id'],'case':p['attempts'][0]['case'],'repetition':1,'outcome':'incomplete'if fault=='incomplete'else 'complete-observation','guest_stopped':True,'normal_DOS':True,'exports_complete':True,'stop_method':'QMP quit; own socket terminated','error':'injected unknown'if fault=='incomplete'else None}
    def exclusive(*args):
     if fault=='lock':raise frames.Refusal('LeaseBusy','isolated lock fault')
     return contextlib.nullcontext()
    session=types.SimpleNamespace(configure=lambda *a:(qmp,guest,base),timeout_signal=lambda *a:None,exclusive=exclusive);imports=lambda name:session if name=='macro_session'else types.SimpleNamespace()
    with patch.object(oracle,'HERE',base),patch.object(oracle,'check',return_value=p),patch.object(oracle.importlib,'import_module',side_effect=imports),patch.object(oracle,'attempt',side_effect=attempt),patch.object(oracle,'qualify',side_effect=frames.Refusal('SourceDrift','isolated')if fault=='source'else None,return_value={}):
     self.assertEqual(oracle.run(args),1)
    ledger=json.loads((base/'ledger.json').read_text());self.assertTrue(ledger['halted']);self.assertEqual(len(calls),0 if fault=='lock'else 1);self.assertEqual(len(ledger['attempts']),len(calls));self.assertFalse(json.loads((base/'runs/wp51-isolated/run.json').read_text())['complete'])
 def test_prior_PRN_tamper_in_actual_run_refuses_before_second_attempt(self):
  with tempfile.TemporaryDirectory()as t:
   base=Path(t);(base/'harddisk.img').write_bytes(b'master');p,args=self.setup_entry(base);calls=[];raw=base/'PRN';raw.write_bytes(b'original');pin={'path':str(raw),'size':8,'sha256':oracle.sha(raw)};qmp=types.SimpleNamespace(SOCKET=base/'socket');guest=types.SimpleNamespace(MASTER=base)
   def attempt(*args):
    calls.append('attempt');return {'id':p['attempts'][0]['id'],'case':p['attempts'][0]['case'],'repetition':1,'outcome':'complete-observation','guest_stopped':True,'normal_DOS':True,'exports_complete':True,'stop_method':'QMP quit; own socket terminated','exports':[pin]}
   session=types.SimpleNamespace(configure=lambda *a:(qmp,guest,base),timeout_signal=lambda *a:None,exclusive=lambda *a:contextlib.nullcontext());imports=lambda name:session if name=='macro_session'else types.SimpleNamespace();real=oracle.accounting.OwnedFile.write
   def tamper_after_committed_result(owned,obj):
    real(owned,obj)
    if owned.path==base/'ledger.json'and obj['attempts']and obj['attempts'][0]['outcome']=='complete-observation':raw.write_bytes(b'tampered')
   with patch.object(oracle,'HERE',base),patch.object(oracle,'check',return_value=p),patch.object(oracle.importlib,'import_module',side_effect=imports),patch.object(oracle,'attempt',side_effect=attempt),patch.object(oracle,'qualify',return_value={}),patch.object(oracle.accounting.OwnedFile,'write',tamper_after_committed_result):self.assertEqual(oracle.run(args),1)
   self.assertEqual(calls,['attempt']);ledger=json.loads((base/'ledger.json').read_text());self.assertTrue(ledger['halted']);self.assertEqual(ledger['failure_code'],'ControlExportIdentity');self.assertEqual(len(ledger['attempts']),1)
 def test_prior_control_raw_tamper_refuses_before_next_boot(self):
  with tempfile.TemporaryDirectory()as t:
   base=Path(t);p={'ledger':str(base/'ledger.json')};raw=base/'PRN';raw.write_bytes(b'original');prior={'id':'isolated','directory':str(base),'exports':[{'path':str(raw),'size':8,'sha256':oracle.sha(raw)}]};oracle.dump(base/'result.json',prior);oracle.dump(base/'ledger.json',{'plan_sha256':oracle.canonical(p),'attempts':[{'id':'isolated','outcome':'complete-observation','result_sha256':oracle.canonical(prior),'result_file_sha256':oracle.sha(base/'result.json')}]});oracle.prior_control(p,prior);raw.write_bytes(b'tampered')
   with self.assertRaises(Exception):oracle.prior_control(p,prior)
   self.assertIn('for prior in report[\'results\']:prior_control(p,prior)',(oracle.HERE/'oracle.py').read_text())
if __name__=='__main__':unittest.main()
