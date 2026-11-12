"""External raw-state/whole-file alias/contextual field refusal regressions."""
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from verify import normal_questions,HERE,n
import candidate_mode

def rehash(run,name,path):
 a=next(a for a in run['artifacts'] if a['path']==name);a.update(size=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest())

class FinalContract(unittest.TestCase):
 def question_copy(self,temp):
  path=Path(temp)/'questions';shutil.copytree(HERE/'runs/wp23-c-normal-questions-r1',path);return path,json.loads((path/'run.json').read_text())
 def test_missing_one_of_twelve_question_contexts_cannot_pass(self):
  with tempfile.TemporaryDirectory(dir=HERE) as temp:
   path,r=self.question_copy(temp);r['cases'].pop();(path/'run.json').write_text(json.dumps(r))
   with self.assertRaisesRegex(ValueError,'Missing normal code-question context'):normal_questions(path,{})
 def test_rehashed_wrong_return_state_same_feature_is_rejected(self):
  with tempfile.TemporaryDirectory(dir=HERE) as temp:
   path,r=self.question_copy(temp);first,last=r['cases'][0],r['cases'][3];name=first['id']+'-cursor/vram.bin';target=path/name;target.write_bytes((path/(last['id']+'-cursor/vram.bin')).read_bytes());rehash(r,name,target);(path/'run.json').write_text(json.dumps(r))
   with self.assertRaisesRegex(ValueError,'Wrong directional code-question return gap'):normal_questions(path,{})
 def test_body_only_interop_alias_is_not_exact_native_alias(self):
  with tempfile.TemporaryDirectory(dir=HERE) as temp:
   path,r=self.question_copy(temp);first=r['cases'][0];aliases={n.sha(path/first['final']):[{'path':path/first['source'],'manifest':path/'run.json','case_id':first['case_id'],'role':'invalid body-only alias'}]}
   self.assertNotEqual((path/first['source']).read_bytes(),(path/first['final']).read_bytes())
   with self.assertRaisesRegex(ValueError,'No exact whole-native interoperability alias'):normal_questions(path,aliases)
 def test_matching_text_and_valid_reader_are_insufficient_for_unknown_counter_relation(self):
  with tempfile.TemporaryDirectory(dir=HERE) as temp:
   path=Path(temp)/'candidate';shutil.copytree(HERE/'runs/wp23-c-candidate-r1',path);r=json.loads((path/'run.json').read_text());name=r['cases'][0]['edited'];target=path/name;raw=bytearray(target.read_bytes());info=n.inspect(raw);packet=next(p for p in info['packets'] if p['type']==6);raw[packet['offset']+8]=3;target.write_bytes(raw);rehash(r,name,target)
   result=candidate_mode.compare(path,r);self.assertFalse(result['accepted']);self.assertTrue(any('counter relationship' in x for x in result['unresolved']));self.assertTrue(all(x['accepted'] and x['exact_no_edit_export'] for x in result['actual_reader']['files']))

if __name__=='__main__':unittest.main()
