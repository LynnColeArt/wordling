"""Real public CLI/atomic report and permission-source negatives;0 real keys/guests."""
from pathlib import Path
import copy,json,os,subprocess,sys,tempfile,unittest
sys.dont_write_bytecode=True
import approved,host,oracle
from boundaries import Refusal,process,canonical
HERE=Path(__file__).resolve().parent
class CLI(unittest.TestCase):
 def invoke(self,*args):return process([sys.executable,str(HERE/'oracle.py'),*args],approved.ROOT,timeout=60)
 def test_actual_example_inspect_simulate_outputs(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t)/'request.json';self.invoke('example','--phase','first-typed','--output',str(p));out,_=self.invoke('inspect-rule','--input',str(p));r=json.loads(out);self.assertTrue(r['prospective_rule_match']);self.assertFalse(r['key_permission']);self.assertFalse(r['original_qualification'])
   request=json.loads(p.read_text());p.write_text(json.dumps(dict(request=request,action='ret')));out,_=self.invoke('simulate','--input',str(p));self.assertEqual(json.loads(out)['real_keys'],0)
 def test_invalid_rehashed_frame_prior_report_unchanged(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t)/'request.json';target=Path(t)/'prior.json';target.write_bytes(b'PRIOR');request=oracle.example('first-typed');v=bytearray.fromhex(request['capture']['vga_hex']);v[3999]^=1;request['capture']['vga_hex']=v.hex();p.write_text(json.dumps(request));before=p.read_bytes()
   with self.assertRaises(Refusal):self.invoke('inspect-rule','--input',str(p),'--output',str(target))
   self.assertEqual(target.read_bytes(),b'PRIOR');self.assertEqual(p.read_bytes(),before)
 def test_duplicateJSON_symlink_nonregular_and_oversize_refuse(self):
  with tempfile.TemporaryDirectory()as t:
   p=Path(t)/'input';link=Path(t)/'link';link.symlink_to(p)
   for raw in [b'{"context":{},"context":{}}',b'x'*(2*1024*1024+1)]:
    p.write_bytes(raw)
    with self.assertRaises(Refusal):self.invoke('inspect-rule','--input',str(p))
   with self.assertRaises(Refusal):self.invoke('inspect-rule','--input',str(link))
   with self.assertRaises(Refusal):self.invoke('inspect-rule','--input',t)
 def test_actual_IO_write_fault_preserves_prior_and_cleans_temp(self):
  with tempfile.TemporaryDirectory()as t:
   target=Path(t)/'prior';target.write_bytes(b'PRIOR')
   code="import resource,signal,oracle,sys;resource.setrlimit(resource.RLIMIT_FSIZE,(128,128));signal.signal(signal.SIGXFSZ,signal.SIG_IGN);sys.exit(oracle.main(['plan','--output',sys.argv[1]]))"
   with self.assertRaises(Refusal):process([sys.executable,'-c',code,str(target)],HERE)
   self.assertEqual(target.read_bytes(),b'PRIOR');self.assertEqual(sorted(p.name for p in Path(t).iterdir()),['prior'])
 def test_known54_payload_rehash_cannot_forge_original(self):
  p=approved.packet('r1/f1/draft');p['text']=p['text'].replace('MISSING','FORGED!');p['source_context']['commit']='0'*40;p['custody']['text_sha256']=oracle.sha(p['text'].encode())
  with self.assertRaises(Refusal):approved.inspect(p)
 def test_unknown_grant_flags_no_source_review_no_private_touch(self):
  for args in [('run',),('run','--allow-vm','--grant','/tmp/not-a-WP55-source-review'),('run','--input','/tmp/forged.json'),('plan','--allow-vm')]:
   with self.subTest(args=args),self.assertRaises(Refusal):self.invoke(*args)
 def test_current_source_inventory_and_exact_grant_schema(self):
  packet=host.prospective_packet();self.assertFalse(packet['prelaunch_ready']);self.assertFalse(packet['physical_guard_or_private_ledger_opened']);self.assertEqual(len(packet['plan']['leaves']),4)
  # No fake source-review or rehashed operator metadata can substitute for required distinct bindings.
  with tempfile.TemporaryDirectory()as t:
   review=Path(t)/'review';grant=Path(t)/'grant';review.write_text(json.dumps(dict(verdict='READY',findings=[],independent=True,source_sha256='0'*64,plan_sha256=packet['plan_sha256'],reviewer='external',reference='test-only')));grant.write_text('{}')
   with self.assertRaises(Refusal)as e:host.authorize(dict(allow_vm=True,source_review=str(review),grant=str(grant)),packet)
   self.assertEqual(e.exception.code,'PrelaunchReviewRequired')
if __name__=='__main__':unittest.main()
