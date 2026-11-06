"""Candidate preflight safety, before any original launch."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import candidate_mode as c

class CandidatePreflight(unittest.TestCase):
 def setUp(self):
  self.candidate=c.ROOT/'docs/research/continuation/native-edits/runs/wp23-cal-modes-02/N0002.WP5'
  self.provenance=json.loads((c.HERE/'candidate-smoke-provenance.json').read_text())
  self.expected=json.loads((c.HERE/'candidate-smoke-expectations.json').read_text())
 def prepare(self,p=None,e=None):
  with tempfile.TemporaryDirectory(dir=c.HERE) as temp:
   pp=Path(temp)/'p.json';ep=Path(temp)/'e.json';pp.write_text(json.dumps(p or self.provenance));ep.write_text(json.dumps(e or self.expected))
   return c.prepare(self.candidate,pp,ep)
 def test_lawful_surrogate_preflight_keeps_source_and_expected_body(self):
  before=self.candidate.read_bytes();r=self.prepare();self.assertEqual(r['candidate_bytes'],before);self.assertEqual(self.candidate.read_bytes(),before);self.assertEqual(r['metadata']['expectations']['subsequent_edit']['expected_body_hex'],b'aXYcZ'.hex())
 def test_wrong_digest_resource_environment_and_semantics_refuse(self):
  for key,value in [('candidate_sha256','0'*64),('environment_sha256','0'*64),('input_body_hex','41')]:
   e=copy.deepcopy(self.expected);e[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):self.prepare(e=e)
  e=copy.deepcopy(self.expected);e['reference_print']['sha256']='0'*64
  with self.assertRaises(ValueError):self.prepare(e=e)
 def test_missing_rights_or_empty_producer_refuses(self):
  for key,value in [('rights','unqualified'),('producer','')]:
   p=copy.deepcopy(self.provenance);p[key]=value
   with self.assertRaises(ValueError):self.prepare(p=p)
 def test_unselected_edit_protocol_refuses(self):
  e=copy.deepcopy(self.expected);e['subsequent_edit']['command']='replace-source'
  with self.assertRaises(ValueError):self.prepare(e=e)

if __name__=='__main__':unittest.main()
