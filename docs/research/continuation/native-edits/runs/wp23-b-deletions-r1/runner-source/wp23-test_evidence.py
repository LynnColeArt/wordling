"""Negative actual-evidence copies; never edit sealed original artifacts."""
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from analyze import validate_run,HERE

class EvidenceTests(unittest.TestCase):
 def copy_run(self,directory):
  source=HERE/'runs/wp23-a-modes-r1';target=Path(directory)/'copy'
  shutil.copytree(source,target);return target,json.loads((target/'run.json').read_text())
 def test_valid_same_feature_case_cannot_substitute_for_ascii_mode_sequence(self):
  with tempfile.TemporaryDirectory(dir=HERE) as temp:
   path,run=self.copy_run(temp);run['cases'][0]['case_id']='CMD51-047'
   (path/'run.json').write_text(json.dumps(run))
   with self.assertRaisesRegex(ValueError,'ASCII mode source/intermediate association'):validate_run(path)
 def test_missing_original_print_cannot_be_accepted(self):
  with tempfile.TemporaryDirectory(dir=HERE) as temp:
   path,run=self.copy_run(temp);stream=run['cases'][0]['interop']['print_stream'];(path/stream).unlink()
   with self.assertRaises((ValueError,FileNotFoundError)):validate_run(path)
 def test_missing_native_cannot_be_accepted(self):
  with tempfile.TemporaryDirectory(dir=HERE) as temp:
   path,run=self.copy_run(temp);(path/run['cases'][0]['final']).unlink()
   with self.assertRaises((ValueError,FileNotFoundError)):validate_run(path)
 def test_hashed_stale_transition_is_not_final_DOS(self):
  with tempfile.TemporaryDirectory(dir=HERE) as temp:
   path,run=self.copy_run(temp);stale=(path/'source-0/screen.txt').read_bytes();target=path/'clean-exit/screen.txt';target.write_bytes(stale)
   artifact=next(x for x in run['artifacts'] if x['path']=='clean-exit/screen.txt');artifact.update(size=len(stale),sha256=hashlib.sha256(stale).hexdigest())
   (path/'run.json').write_text(json.dumps(run))
   with self.assertRaisesRegex(ValueError,'No actual final DOS capture'):validate_run(path)

if __name__=='__main__':unittest.main()
