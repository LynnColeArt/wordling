import copy,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'scripts/reference'))
import wordling_edits as w
import final_state
class Successor(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(prefix='preflight-test-',dir=w.SUCCESSOR)
  self.root=Path(self.temp.name);(self.root/'reader').mkdir()
  self.known=w.approved_config()
  for name,p in [('field-ledger.json',self.root/'field-ledger.json'),('reader_probe.go.txt',self.root/'reader/reader_probe.go.txt')]:p.write_bytes(self.known[name])
  self.product=json.loads((w.OUT/'preparations/app-b/plan.json').read_text())['product']
 def tearDown(self):self.temp.cleanup()
 def check(self):return w.comparison_preflight(self.root,self.product)
 def test_complete_exact_static_configuration(self):self.assertEqual(self.check()['ledger']['sha256'],w.sha(self.known['field-ledger.json']))
 def test_missing_truncated_mutated_rehashed_owner_width_and_nonregular(self):
  p=self.root/'field-ledger.json';raw=self.known['field-ledger.json']
  changed=json.loads(raw);changed['field_coverage'][0]['width']+=1
  for data in [b'',raw[:-1],raw+b'\n',json.dumps(changed).encode()]:
   p.write_bytes(data)
   with self.assertRaises(w.Failure):self.check()
  p.unlink()
  with self.assertRaises(w.Failure):self.check()
  p.mkdir()
  with self.assertRaises(w.Failure):self.check()
  p.rmdir();p.symlink_to(w.APPROVED/'field-ledger.json')
  with self.assertRaises(w.Failure):self.check()
 def test_reader_missing_and_tampered_before_guest_or_attempt(self):
  p=self.root/'reader/reader_probe.go.txt'
  for data in [b'',self.known['reader_probe.go.txt']+b'\n']:
   p.write_bytes(data)
   with patch.object(w.n,'execute')as execute,patch.object(w,'consume_successor')as consume:
    with self.assertRaises(w.Failure):self.check()
    execute.assert_not_called();consume.assert_not_called()
 def test_wrong_final_root_and_golden_profile_pins(self):
  with patch.object(final_state,'HERE',self.root):
   with self.assertRaisesRegex(w.Failure,'WrongComparisonRoot'):self.check()
  for key in ['docs/research/continuation/native-edits/final-state-golden.json']:
   old=self.product['helper_sources'][key];self.product['helper_sources'][key]={'size':old['size'],'sha256':'0'*64}
   with self.assertRaisesRegex(w.Failure,'ChangedFinalGolden'):self.check()
   self.product['helper_sources'][key]=old
  self.product['profile']={'size':1,'sha256':'0'*64}
  with self.assertRaisesRegex(w.Failure,'ChangedProfile'):self.check()
 def test_golden_source_tamper_uses_actual_file_guard(self):
  p=self.root/'golden-copy';raw=b'raw VGA';p.write_bytes(raw)
  expected=w.identity(p);p.write_bytes(raw+b'X')
  with self.assertRaisesRegex(w.Failure,'GoldenSourceChanged'):w.regular_exact(p,expected,'GoldenSourceChanged')
 def test_actual_public_comparator_exact_and_missing_runtime_ledger(self):
  import classify_reader
  old_out=w.n.OUT;old_here=classify_reader.HERE
  try:
   w.n.OUT=self.root;classify_reader.HERE=self.root/'reader'
   directory=w.APPROVED/'runs/wp23-c-candidate-r1';run=json.loads((directory/'run.json').read_text())
   self.check();self.assertTrue(w.cm.compare(directory,run)['accepted'])
   (self.root/'field-ledger.json').unlink()
   with self.assertRaises(FileNotFoundError):w.cm.compare(directory,run)
   with self.assertRaises(w.Failure):self.check()
   value=json.loads(self.known['field-ledger.json']);value['field_coverage']=[]
   (self.root/'field-ledger.json').write_text(json.dumps(value))
   self.assertFalse(w.cm.compare(directory,run)['accepted'])
   with self.assertRaises(w.Failure):self.check()
  finally:w.n.OUT=old_out;classify_reader.HERE=old_here
 def test_changed_historical_ledger_is_rejected_without_guest_or_consumption(self):
  original=w.identity
  def changed(path):
   result=original(path)
   if Path(path)==w.OUT/'oracle/ledger.json':return result|{'sha256':'0'*64}
   return result
  with patch.object(w,'identity',side_effect=changed),patch.object(w.n,'execute')as execute,patch.object(w,'consume_successor')as consume:
   with self.assertRaisesRegex(w.Failure,'PredecessorLedgerChanged'):w.predecessor_receipt()
   execute.assert_not_called();consume.assert_not_called()
 def test_missing_control_stream_and_wrong_control_binding_before_guest(self):
  row=next(c for c in self.plan()['unique_whole_native_classes']if c['id']=='three-entry-eviction')
  original=json.loads((w.OUT/'oracle/history-control-seal.json').read_text())
  target=self.root/'oracle/history-control-seal.json';target.parent.mkdir()
  for kind in ['missing-stream','wrong-control']:
   value=copy.deepcopy(original)
   if kind=='missing-stream':value['reference_print']['path']=str(self.root/'missing.PRN')
   else:value['control']='unrelated-control'
   target.write_text(json.dumps(value))
   with patch.object(w,'OUT',self.root),patch.object(w,'ORACLE',self.root/('new-'+kind)),patch.object(w.n,'execute')as execute:
    with self.assertRaises((ValueError,OSError)):w.prepared_candidate(row)
    execute.assert_not_called()
 def test_false_helper_pin_before_guest(self):
  actual=w.pins();actual['helper_sources']['scripts/reference/native_edits.py']={'size':1,'sha256':'0'*64}
  with patch.object(w,'pins',return_value=actual),patch.object(w.n,'execute')as execute:
   with self.assertRaisesRegex(w.Failure,'FrozenHelperDrift'):w.check_emission()
   execute.assert_not_called()
 def test_old_v1_grant_cannot_restart_or_consume_successor(self):
  from types import SimpleNamespace
  with patch.object(w.n,'execute')as execute,patch.object(w,'consume_successor')as consume:
   with self.assertRaisesRegex(w.Failure,'GrantShape'):
    w.run_oracle(SimpleNamespace(allow_vm=True,grant=w.OUT/'oracle-fault-01/root-grant.json',leaf='no-edit-two-pair-r1'))
   execute.assert_not_called();consume.assert_not_called()
 def plan(self):
  p=json.loads((w.SUCCESSOR/'plan.json').read_text());return p
 def ledger(self,p):return {'grant_sha256':'unit','attempts':[],'halted':False,'predecessor':p['predecessor'],'prior_spent_attempts':3,'cumulative_cap':19}
 def test_cumulative_three_plus_sixteen_and_sticky_faults(self):
  p=self.plan()
  for error in ['protocol unknown','StopDeadline','extraction mcopy failure','comparison rejected']:
   base=self.ledger(p);ledger,attempt=w.consume_successor(base,'unit',p,p['original_leaves'][0],['no-guest-unit'])
   w.persist_fault(self.root/'ledger.json',ledger,attempt,RuntimeError(error),{})
   stored=json.loads((self.root/'ledger.json').read_text());self.assertTrue(stored['halted']);self.assertEqual(stored['prior_spent_attempts'],3);self.assertEqual(len(stored['attempts']),1);self.assertEqual(stored['attempts'][0]['error'],error);self.assertEqual(base['attempts'],[])
   with self.assertRaises(w.Failure):w.consume_successor(stored,'unit',p,p['original_leaves'][1],[])
 def test_no_relabel_retry_reset_skip_or_extra_candidate(self):
  p=self.plan();base=self.ledger(p)
  for key,value in [('prior_spent_attempts',0),('cumulative_cap',18)]:
   changed=copy.deepcopy(base);changed[key]=value
   with self.assertRaises(w.Failure):w.consume_successor(changed,'unit',p,p['original_leaves'][0],[])
  for alteration in ['reverse','drop','cap']:
   q=copy.deepcopy(p)
   if alteration=='reverse':q['original_leaves'].reverse()
   elif alteration=='drop':q['original_leaves'].pop()
   else:q['cumulative_cap']=18
   with self.assertRaises(w.Failure):w.successor_shape(q)
  with self.assertRaises(w.Failure):w.consume_successor(base,'unit',p,p['original_leaves'][1],[])
 def test_original_custody_receipt_is_exact_not_accepting_candidate(self):
  receipt=w.predecessor_receipt();self.assertEqual(receipt['prior_spent_attempts'],3);self.assertEqual(receipt['qualified_control_count'],2);self.assertEqual(receipt['candidate_incomplete_count'],1);self.assertTrue(receipt['old_ledger_halted'])
if __name__=='__main__':unittest.main()
