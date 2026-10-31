"""External read-only admission negatives; synthesized bytes are safety cases only."""
from pathlib import Path
import struct
import subprocess
import json
import tempfile
import sys
import unittest
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'scripts/reference'))
import native_edits as n

class InspectorTests(unittest.TestCase):
 def setUp(self):self.raw=n.ORIGIN.read_bytes();self.info=n.inspect(self.raw)
 def reject(self,data):
  before=bytes(data)
  with self.assertRaises(ValueError):n.inspect(data,True)
  self.assertEqual(bytes(data),before)
 def test_original_exact_admission_and_owner_coverage(self):
  r=n.inspect(self.raw,True);self.assertEqual(r['body_hex'],'41c30cc34243c40cc444');self.assertEqual(r['body_offset'],324);self.assertEqual(self.raw,n.ORIGIN.read_bytes())
 def test_malformed_header_index_packet_and_graphics(self):
  for offset,width,value in [(4,4,len(self.raw)+1),(18,2,65535),(22,4,16),(32,4,0xffffffff),(38,4,0xffffffff),(322,2,1),(12,2,1),(14,2,1)]:
   raw=bytearray(self.raw);struct.pack_into('<H' if width==2 else '<I',raw,offset,value);self.reject(raw)
  for length in range(16):self.reject(self.raw[:length])
 def test_unknown_deleted_and_unqualified_resource_fields(self):
  for offset,value in [(26,9),(26,255),(80+18,13),(80+50+12,1),(80+20,1),(256,16),(166+82,0)]:
   raw=bytearray(self.raw);raw[offset]=value;self.reject(raw)
 def test_unpaired_nested_opaque_and_unsupported_character(self):
  for body in [b'\xc3\x0c',bytes.fromhex('c40cc4'),bytes.fromhex('c30cc3'),bytes.fromhex('c30cc3c30cc3c40cc4c40cc4'),bytes.fromhex('c02401c0'),bytes.fromhex('d00108000a0b0c0d080001d0'),b'A\x0aB']:
   self.reject(self.raw[:324]+body)
 def test_size_and_token_bounds(self):
  self.reject(self.raw[:324]+b'A'*(n.TOKEN_LIMIT+1));self.reject(bytes(n.LIMIT+1))
  r=n.inspect(self.raw[:324]+b'A'*n.TOKEN_LIMIT,True);self.assertEqual(len(r['tokens']),n.TOKEN_LIMIT)
 def test_flag_location_is_indexed_not_fixture_constant(self):
  raw=bytearray(self.raw);raw[166:182]=self.raw[256:272];raw[182:272]=self.raw[166:256]
  struct.pack_into('<I',raw,52,182);struct.pack_into('<I',raw,62,166)
  r=n.inspect(raw,True);self.assertEqual(next(p['offset'] for p in r['packets'] if p['type']==6),166)
 def test_terminator_cannot_hide_next_index_pointer(self):
  raw=bytearray(self.raw);struct.pack_into('<I',raw,278,16);self.reject(raw)
 def test_qualified_hash_variants_are_preserved_not_recomputed(self):
  raw=bytearray(self.raw);raw[101:103]=bytes.fromhex('1172');before=bytes(raw)
  n.inspect(raw,True);self.assertEqual(bytes(raw),before)
  raw[101]^=1;self.reject(raw)
 def test_unqualified_printer_counter_refuses_mutation(self):
  raw=bytearray(self.raw);raw[264]=2;self.reject(raw)
 def test_diagnostic_opaque_body_is_not_decoded_as_inner_bold(self):
  body=bytes.fromhex('d0010800c30cc3080001d0');raw=self.raw[:324]+body
  diagnostic=n.inspect(raw,False);self.assertEqual(diagnostic['body_hex'],body.hex());self.assertEqual(diagnostic['tokens'],[]);self.assertTrue(diagnostic['body_grammar_refusal'])
  with self.assertRaises(n.AdmissionRefusal) as refused:n.inspect(raw,True)
  self.assertEqual(refused.exception.code,'UnsupportedBodyGrammar')
 def test_typed_public_refusal_keeps_metadata_and_bounds_distinct(self):
  raw=bytearray(self.raw);raw[264]=2
  with self.assertRaises(n.AdmissionRefusal) as refused:n.inspect(raw,True)
  self.assertEqual(refused.exception.code,'UnsupportedDocumentMetadata')
  with self.assertRaises(n.AdmissionRefusal) as refused:n.inspect(bytes(n.LIMIT+1),True)
  self.assertEqual(refused.exception.code,'ResourceLimit')
 def test_cli_oversized_sparse_input_fails_with_bounded_refusal(self):
  with tempfile.TemporaryDirectory(dir=HERE) as temp:
   path=Path(temp)/'oversize.WP5'
   with path.open('wb') as out:out.seek(n.LIMIT*100);out.write(b'X')
   result=subprocess.run([sys.executable,str(ROOT/'scripts/reference/native_edits.py'),'inspect',str(path),'--admit'],capture_output=True,text=True,timeout=5)
   self.assertEqual(result.returncode,2);self.assertEqual(json.loads(result.stdout)['code'],'ResourceLimit')
 def test_actual_read_only_save_variant_is_not_mutation_permission(self):
  p=ROOT/'docs/research/continuation/session1/runs/2026-10-31-session1-b01-r1/CMD51-049/CURSOR.WP5'
  r=n.inspect(p.read_bytes());self.assertEqual(r['body_offset'],564);self.reject(p.read_bytes())

if __name__=='__main__':unittest.main()
