"""Public prospective-rule and zero-guest authority contract."""
import copy,json,sys,unittest
from pathlib import Path
sys.dont_write_bytecode=True
import oracle
class Contract(unittest.TestCase):
 def test_known_originals_are_separate_from_rules(self):
  report=oracle.check();self.assertEqual(report['actual_public54_observations'],10);self.assertFalse(report['original_qualification']);self.assertFalse(report['prelaunch_ready'])
 def test_first_empty_and_typed_are_pure(self):
  for phase in ['first-empty','first-typed']:
   request=oracle.example(phase);result=oracle.inspect_rule(request)
   self.assertTrue(result['prospective_rule_match'])
   for key in ['original_qualification','io_authority','native_authority','key_permission']:self.assertIs(result[key],False)
 def test_forgery_source_flags_and_stale_history(self):
  original=oracle.example('first-typed')
  for mutation in [lambda r:r.update(original_qualification=True),lambda r:r['context'].update(mode='Typeover'),lambda r:r['context'].update(phase='second-entry'),lambda r:r['context'].update(plan_sha256='0'*64),lambda r:r['rule'].update(source_commit='0'*40),lambda r:r['capture']['cursor'].update(column=True),lambda r:r['capture'].update(text=r['capture']['text'].replace('I55IN','I55XX'))]:
   with self.subTest(mutation=mutation):
    r=copy.deepcopy(original);mutation(r)
    with self.assertRaises(oracle.Refusal):oracle.inspect_rule(r)
 def test_all_second_hypotheses_one_cancel_only(self):
  for case in oracle.plan()['leaves']:
   for h in ['H-empty','H-priorRetrieve','H-priorSave']:
    request=oracle.example('second-entry',case['id'],h);result=oracle.inspect_rule(request);self.assertTrue(result['prospective_rule_match']);self.assertFalse(result['key_permission'])
    for action in ['ret','type','backspace','esc','f1,f1']:
     with self.assertRaises(oracle.Refusal):oracle.simulate(dict(request=request,action=action))
    x=oracle.simulate(dict(request=request,action='f1'));self.assertEqual(x['simulated_only'],['f1']);self.assertEqual(x['real_keys'],0)
 def test_unknown_frame_halts_before_key(self):
  r=oracle.example('second-entry');r['capture']['text']='unknown\n'*25
  with self.assertRaises(oracle.Refusal):oracle.simulate(dict(request=r,action='f1'))
 def test_plan_has_four_new_same_literals_each_pair(self):
  p=oracle.plan();self.assertEqual(len(p['leaves']),4);self.assertEqual(p['old51'],dict(spent=1,incomplete=1,qualified=0,abandoned=7,permanently_halted=True));self.assertEqual(p['historical46'],13)
  for i in [0,2]:self.assertEqual(p['leaves'][i]['input_literal'],p['leaves'][i+1]['input_literal']);self.assertEqual(p['leaves'][i]['save_literal'],p['leaves'][i+1]['save_literal'])
 def test_run_cannot_upgrade(self):
  with self.assertRaises(oracle.Refusal)as e:oracle.run({'allow_vm':True,'grant':{'prelaunch_ready':True}})
  self.assertEqual(e.exception.code,'OriginalStageBlocked')
if __name__=='__main__':unittest.main()
