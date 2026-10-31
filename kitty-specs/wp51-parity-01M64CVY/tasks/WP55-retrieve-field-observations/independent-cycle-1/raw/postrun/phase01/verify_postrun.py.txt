"""Read-only verification of the permanently halted WP55 phase01, never replay/repair."""
from pathlib import Path
import ast,copy,hashlib,json,subprocess,sys,unittest,xml.etree.ElementTree as ET
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;O=P.parents[1];ROOT=O.parents[3];RUN=O/'runs/wp55-entry-one-f1-v1';LEAF=RUN/'wp55-entry-insert-r1';sys.path.insert(0,str(O))
import oracle,ui
from boundaries import Refusal,canonical
H=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def keys():
 result=[]
 for raw in (LEAF/'qmp-wire.jsonl').read_text().splitlines():
  row=json.loads(raw)
  if row['direction']!='tx':continue
  message=json.loads(bytes.fromhex(row['raw_hex']));line=message.get('arguments',{}).get('command-line','')
  if message.get('execute')=='human-monitor-command'and line.startswith('sendkey '):result.append(line)
 return result
EXPECTED=['sendkey '+key+' 80'for key in ['shift-f10','shift-c','shift-semicolon','backslash','shift-o','shift-u','shift-t','backslash','shift-i','5','5','shift-i','shift-n','ret','f10','shift-c','shift-semicolon','backslash','shift-o','shift-u','shift-t','backslash','shift-i','5','5','shift-s','shift-v','ret','f7','n','n','shift-f10','f1','f7']]
def check_accounting(run,ledger,claim):
 assert run['complete']is False and run['error_code']=='UnsafeRelease';assert ledger['halted']is True and ledger['one_shot_no_resume']is True and ledger['ROOT_logical_reservation_released']is False;assert len(ledger['attempts'])==len(run['results'])==1 and ledger['remaining_abandoned']==3;row=run['results'][0];assert row['id']=='wp55-entry-insert-r1'and row['outcome']=='incomplete'and row['error_code']=='UnknownUIFrame';assert row['owned_identity']['pid']==1992304 and row['owned_identity']['startticks']=='19688580';assert row['normal_DOS']is False and row['exports_complete']is False and not row.get('export');assert claim==dict(spent=1,launched=1,qualified=0,incomplete=1,permanently_abandoned=3)
def check_keys(actual):assert actual==EXPECTED,'exact34wirekeys: ONE secondF1 then finalF7; no key afterunknown014'
def check_quit(raw):
 tx=[];rx=[];events=[]
 for line in raw.splitlines():
  r=json.loads(line);m=json.loads(bytes.fromhex(r['raw_hex']))
  if r['direction']=='tx':tx.append(m)
  elif 'event'in m:events.append(m)
  else:rx.append(m)
 assert tx==[{'execute':'quit'}]and rx==[{'return':{}}];assert any(m['event']=='SHUTDOWN'and m['data']['reason']=='host-qmp-quit'for m in events)
def actual_capture(label):
 p=LEAF/label;assert (p/'vram.bin').stat().st_size==4000;return dict(text=(p/'screen.txt').read_text(),vga_hex=(p/'vram.bin').read_bytes().hex(),cursor=load(p/'cursor.json'))
class Postrun(unittest.TestCase):
 def test_actual_counts_not_generic_stderr(self):
  run=load(RUN/'run.json');ledger=load(P/'authority/private-accounting.json.txt');safety=load(P/'authority/root-safety-release.json.txt');check_accounting(run,ledger,safety['actual_counts']);assert H((RUN/'run.json').read_bytes())==safety['run_sha256'];assert H((P/'authority/private-accounting.json.txt').read_bytes())==safety['private_accounting_sha256'];error=json.loads((P/'execution/stderr.log').read_text());assert error['error']=='UnsafeRelease'and error['new_guests']==0 and safety['actual_counts']['launched']==1
 def test_actual_wire_no_extra_behavioral_key(self):check_keys(keys());assert len([p for p in LEAF.iterdir()if p.is_dir()])==14;assert not list(LEAF.rglob('*.WP5'))
 def test_diagnostic_entry_return_and_real_guard_refusal(self):
  p=load(O/'checks/preflight-a.json');ident='wp55-entry-insert-r1';matched=[]
  for hypothesis in ['H-empty','H-priorRetrieve','H-priorSave']:
   request=copy.deepcopy(p['public_rule_examples'][ident][hypothesis]);request['capture']=actual_capture('012-SECOND-Retrieve-ENTRY')
   try:r=oracle.inspect_rule(request);assert r['original_qualification']is False;matched.append(hypothesis)
   except Refusal:pass
  assert matched==['H-empty'];leaf=p['packet']['plan']['leaves'][0];result=ui.match(actual_capture('013-ONE-F1-exact-return'),'after-F1',leaf);assert result['original_qualification']is False
  with self.assertRaises(Refusal)as e:ui.match(actual_capture('014-final-empty-Save-question'),'empty-save',leaf)
  assert e.exception.code=='UnknownUIFrame';actual=actual_capture('014-final-empty-Save-question')['text'];frozen=p['prospective_UI_templates'][ident]['empty-save']['text'];assert actual.split('\n')[24]=='Save document? Yes (No)                            (Text was not modified)'and frozen.split('\n')[24]=='Save document? Yes (No)';assert actual.split('\n')[0]==frozen.split('\n')[0]==''
 def test_actual_quit_kernel_master_no_normalDOS(self):
  r=load(RUN/'run.json')['results'][0];raw=(LEAF/'qmp-stop-wire.jsonl').read_bytes();check_quit(raw);assert H(raw)==r['quit_exchange']['sha256']=='58e977868d524a43a719618e715aea45115bdbbe4f907e7fcffca32481e80c10';assert r['guest_stopped']is True and r['stop_proof']['gone_or_same_zombie']is True and r['stop_proof']['socket_absent']is True;assert r['stop_proof']['observations'][0]['state']=='Z'and r['stop_proof']['observations'][0]['startticks']=='19688580';assert r['master_unchanged']is True and r['master_after']==load(P/'authority/root-safety-release.json.txt')['master_after'];assert r['normal_DOS']is False and r['stop_method']=='Owned audited QMP containment; normal DOS/source authority unproved'
 def test_root_host_release_separate_from_immutable_private_ledger(self):
  initial=load(P/'authority/root-reservation-initial.json.txt');released=load(P/'authority/root-reservation-released.json.txt');safety=load(P/'authority/root-safety-release.json.txt');assert initial['status']=='retained';assert released['status']=='released_after_whole_plan_halt_ROOT_host_safety_diagnosis';assert safety['qualified_behavioral_completion']is False and safety['normal_DOS']is False and safety['native_exports']==0;assert load(P/'authority/private-accounting.json.txt')['ROOT_logical_reservation_released']is False
 def test_frozen_source_and_prelaunch425_still_exact(self):
  rows=load(O/'seals.json')['files'];assert len(rows)==424
  for name,pin in rows.items():
   raw=(O/name).read_bytes();assert len(raw)==pin['size']and H(raw)==pin['sha256'];blob=subprocess.check_output(['git','rev-parse','ee2fb0b51d3b769cb0a0c38e58b461c811bf488c:'+str((O/name).relative_to(ROOT))],cwd=ROOT,text=True).strip();assert blob==pin['git_blob']
  assert H((O/'seals.json').read_bytes())=='4947299073626f6e19f85750c0b1d6addffde28f2793854b3de414427cede2fa'
  for pin in load(O/'checks/preflight-a.json')['packet']['sources']:assert H((ROOT/pin['path']).read_bytes())==pin['sha256']
 def test_authority_copies_exact_and_review_READY_only_prelaunch(self):
  m=load(P/'copy-map.json');assert m['review_files_including_seal']==87
  for row in m['files']:
   raw=(P/row['destination']).read_bytes();assert len(raw)==row['bytes']and H(raw)==row['sha256'];assert raw==Path(row['source']).read_bytes()
  seal=load(P/'authority/prelaunch-cycle3/seals.json.txt');assert len(seal['files'])==86 and seal['verdict']=='READY'
  for row in seal['files']:assert H((P/'authority/prelaunch-cycle3'/(row['path']+'.txt')).read_bytes())==row['sha256']
 def test_in_memory_falsifiers_cannot_relabel_failure(self):
  run=load(RUN/'run.json');ledger=load(P/'authority/private-accounting.json.txt');counts=dict(spent=1,launched=1,qualified=0,incomplete=1,permanently_abandoned=3)
  for name in ['countzero','complete','normalDOS','resume']:
   r=copy.deepcopy(run);l=copy.deepcopy(ledger);c=copy.deepcopy(counts)
   if name=='countzero':c['launched']=0
   if name=='complete':r['complete']=True
   if name=='normalDOS':r['results'][0]['normal_DOS']=True
   if name=='resume':l['halted']=False
   with self.subTest(name=name),self.assertRaises(AssertionError):check_accounting(r,l,c)
  with self.assertRaises(AssertionError):check_keys(keys()+['sendkey n 80'])
  wire=(LEAF/'qmp-stop-wire.jsonl').read_bytes();withoutquit=b'\n'.join(line for line in wire.splitlines()if json.loads(line)['direction']!='tx')
  with self.assertRaises(AssertionError):check_quit(withoutquit)
if __name__=='__main__':
 stream=(P/'verification.log').open('w');suite=unittest.defaultTestLoader.loadTestsFromTestCase(Postrun);result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite);stream.close();xml=ET.Element('testsuite',name='WP55-actual-halted-postrun',tests=str(result.testsRun),failures=str(len(result.failures)),errors=str(len(result.errors)),skipped=str(len(result.skipped)))
 for test,trace in result.failures+result.errors:case=ET.SubElement(xml,'testcase',name=str(test));ET.SubElement(case,'failure').text=trace
 ET.indent(xml);ET.ElementTree(xml).write(P/'verification.xml',encoding='utf-8',xml_declaration=True);print(json.dumps(dict(tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),skips=len(result.skipped),original_controller_reinvocations=0)));raise SystemExit(0 if result.wasSuccessful()else 1)
