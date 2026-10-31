import copy,json,sys,unittest
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'scripts/reference'))
import wordling_edits as w
class Driver(unittest.TestCase):
 def test_no_vm_without_flag_and_grant(self):
  for args in [SimpleNamespace(allow_vm=False,grant=Path('/missing')),SimpleNamespace(allow_vm=True,grant=None)]:
   with self.assertRaisesRegex(w.Failure,'AuthorizationRequired'):w.run_oracle(args)
 def test_sticky_attempt_consumption(self):
  a={'id':'a'};b={'id':'b'};plan={'original_leaves':[a,b],'original_guest_cap_including_failures':2};base={'grant_sha256':'x','halted':False,'attempts':[]}
  ledger,attempt=w.consume_leaf(base,'x',plan,a,['actual','leaf']);self.assertTrue(ledger['halted']);self.assertEqual(len(ledger['attempts']),1);self.assertFalse(base['halted']);self.assertEqual(base['attempts'],[])
  for leaf in [a,b]:
   with self.assertRaisesRegex(w.Failure,'GrantHalted'):w.consume_leaf(ledger,'x',plan,leaf,[])
  ledger['halted']=False
  with self.assertRaisesRegex(w.Failure,'LeafOrder'):w.consume_leaf(ledger,'x',plan,a,[])
  ledger,second=w.consume_leaf(ledger,'x',plan,b,[]);ledger['halted']=False
  with self.assertRaisesRegex(w.Failure,'LeafOrder'):w.consume_leaf(ledger,'x',plan,b,[])
 def test_wrong_grant_not_substituted(self):
  with self.assertRaisesRegex(w.Failure,'GrantHalted'):w.consume_leaf({'grant_sha256':'x','halted':False,'attempts':[]},'y',{'original_leaves':[],'original_guest_cap_including_failures':0},{},[])
 def test_real_failed_save_not_false_success(self):
  folder=w.OUT/'preparations/app-a/normal-paired-delete-r1';frames=w.replay_frames(folder)
  with self.assertRaisesRegex(w.Failure,'FalseSuccess'):w.publication_witness(frames,'CANDIDA',1)
 def test_same_feature_wrong_case_rejected(self):
  recipe=next(x for x in w.recipes()if x['id']=='ascii-modes');folder=w.OUT/'preparations/app-a/ascii-modes-r1'
  with self.assertRaisesRegex(w.Failure,'WrongSemanticCase'):w.verify_app(folder,recipe,{'cases':['CMD51-047']})
if __name__=='__main__':unittest.main()
