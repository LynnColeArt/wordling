"""Public entry-point acceptance tests; no guest or private disk access."""
from pathlib import Path
import json,subprocess,sys,tempfile,unittest
HERE=Path(__file__).resolve().parent
class Invoke(unittest.TestCase):
 def invoke(self,*args):
  return subprocess.run([sys.executable,str(HERE/'oracle.py'),*map(str,args)],capture_output=True,text=True,timeout=30)

class CLI(Invoke):
 def test_plan_is_blocked_and_has_zero_attempts(self):
  p=self.invoke('plan');self.assertEqual(p.returncode,0,p.stderr);d=json.loads(p.stdout);self.assertFalse(d['prelaunch_ready']);self.assertEqual(d['new_original_attempts'],0);self.assertEqual(d['old51']['abandoned'],7)
 def test_run_is_refused_without_importing_any_guest(self):
  p=self.invoke('run');self.assertNotEqual(p.returncode,0);self.assertEqual(json.loads(p.stdout)['error']['code'],'OriginalStageBlocked')
 def test_actual_paired_three_contexts(self):
  p=self.invoke('check');self.assertEqual(p.returncode,0,p.stdout+p.stderr);d=json.loads(p.stdout);self.assertEqual(len(d['observations']),10);self.assertEqual(len(d['diagnostic_only']),2);self.assertFalse(d['prelaunch_ready']);self.assertEqual(d['source_audit']['inventory_screens'],1085)

class PublicContract(Invoke):
 @classmethod
 def setUpClass(cls):
  cls.cache={}
  for ident in ['r1/f1/prompt','r1/f1/draft','r1/retry','r2/f1/draft','diagnosis/014-retrieve-name-after']:
   p=subprocess.run([sys.executable,str(HERE/'oracle.py'),'packet','--id',ident],capture_output=True,text=True,timeout=30)
   if p.returncode:raise AssertionError(p.stdout+p.stderr)
   cls.cache[ident]=json.loads(p.stdout)
 def packet(self,ident='r1/f1/draft',synthetic=True):
  import copy
  x=copy.deepcopy(self.cache[ident]);x['authority']='synthetic'if synthetic else x['authority'];return x
 def rehash(self,x):
  import hashlib
  h=lambda b:hashlib.sha256(b).hexdigest();x['custody']={'text_sha256':h(x['text'].encode()),'vga_sha256':h(bytes.fromhex(x['vga_hex'])),'cursor_sha256':h(json.dumps(x['cursor'],sort_keys=True,separators=(',',':')).encode())};return x
 def alter_text(self,p,text):
  # Well-framed synthetic counterexample: consistent text and VGA character bytes.
  p['text']=text;v=bytearray.fromhex(p['vga_hex']);rows=text.split('\n')[:-1]
  if len(rows)==25 and all(len(r)<=80 for r in rows):
   for row,s in enumerate(rows):v[row*160:row*160+160:2]=s.ljust(80).encode('ascii')
   p['vga_hex']=v.hex()
  return self.rehash(p)
 def inspect_packet(self,packet,command='inspect'):
  with tempfile.TemporaryDirectory()as tmp:
   path=Path(tmp)/'packet.json';path.write_text(json.dumps(packet));return self.invoke(command,'--packet',path)
 def assert_refusal(self,p,code=None):
  self.assertEqual(p.returncode,2,p.stdout+p.stderr);d=json.loads(p.stdout);self.assertFalse(d['prelaunch_ready']);self.assertEqual(d['real_guest_keys'],0)
  if code:self.assertEqual(d['error']['code'],code)
  return d
 def test_synthetic_does_not_become_original_qualification(self):
  p=self.inspect_packet(self.packet());self.assertEqual(p.returncode,0,p.stdout);self.assertFalse(json.loads(p.stdout)['original_source_bound']);self.assertFalse(json.loads(p.stdout)['original_qualification'])
 def test_rehashed_wrong_cue_framed_semantics(self):
  x=self.packet();s=x['text'].split('\n');s[24]=s[24].ljust(67)+'(List Files)';self.assert_refusal(self.inspect_packet(self.alter_text(x,'\n'.join(s))),'PromptShape')
 def test_retry_is_distinct_positive_and_not_fresh(self):
  x=self.packet('r1/retry');p=self.inspect_packet(x);self.assertEqual(p.returncode,0,p.stdout);self.assertEqual(json.loads(p.stdout)['kind'],'missing-file-error-return')
  x['kind']='fresh-whole-field-typed';self.assert_refusal(self.inspect_packet(x),'TransitionContext')
 def test_state_ignored_mutant_witness(self):
  x=self.packet();x['kind']='missing-file-error-return';self.assert_refusal(self.inspect_packet(x),'TransitionContext')
 def test_rehashed_body_modal_status_RS_filename_line_forgery(self):
  for row,content in [(0,'Q'),(10,'No text to print'),(23,'Doc 2 Pg 1'),(12,'\x1e')]:
   with self.subTest(row=row):
    x=self.packet();s=x['text'].split('\n');s[row]=content;self.assert_refusal(self.inspect_packet(self.alter_text(x,'\n'.join(s))),'DocumentRows')
  x=self.packet();self.assert_refusal(self.inspect_packet(self.alter_text(x,x['text'].replace('MISSING','MISSINX'))),'PromptShape')
  for change in [lambda s:s+'\n',lambda s:s[:-1],lambda s:s.replace('\n','\r\n'),lambda s:s.replace('\n','\x1e',1)]:
   x=self.packet();self.assert_refusal(self.inspect_packet(self.alter_text(x,change(x['text']))),'FrameShape')
 def test_rehashed_VGA_attributes_and_characters(self):
  for offset,code in [(1,'VGAAttributes'),(0,'VGAText')]:
   x=self.packet();v=bytearray.fromhex(x['vga_hex']);v[offset]^=1;x['vga_hex']=v.hex();self.assert_refusal(self.inspect_packet(self.rehash(x)),code)
 def test_cursor_ignored_mutant_witness(self):
  x=self.packet();x['cursor']['column']=37;x['cursor']['cursor_word']=1957;x['cursor']['crtc']['15']=165;self.assert_refusal(self.inspect_packet(self.rehash(x)),'CursorFrame')
 def test_rehashed_cursor_schema_registers_and_missing_context(self):
  for k,v in [('row',0),('column',True),('display_start_word',80),('cursor_word',None),('selected_index',14)]:
   x=self.packet();x['cursor'][k]=v;self.assert_refusal(self.inspect_packet(self.rehash(x)),'CursorFrame')
  x=self.packet();x['cursor']['crtc']['10']=True;self.assert_refusal(self.inspect_packet(self.rehash(x)),'CursorRegisters')
  for k in ['document_body','document_source','document_mode','document_status','document_gap','document_name']:
   x=self.packet();x['source_context'].pop(k);self.assert_refusal(self.inspect_packet(x),'SourceContext')
 def test_trace_source_caller_and_stale_wrapper_forgery(self):
  x=self.packet();x['trace'][-2]={'type':'C:\\OTHER'};self.assert_refusal(self.inspect_packet(x),'TraceContext')
  x=self.packet();x['source_context']['run_id']='another';self.assert_refusal(self.inspect_packet(x),'SourceContext')
  x=self.packet();x['id']='r2/f1/draft';self.assert_refusal(self.inspect_packet(x),'SourceContext')
 def test_source_rehashed_substitution_mutant_witness(self):
  x=self.packet(synthetic=False);x['cursor']['note']='forged but semantically ignored note';self.assert_refusal(self.inspect_packet(self.rehash(x)),'OriginalSourceBinding')
 def test_failed014_diagnostic_cannot_relabel(self):
  x=self.packet('diagnosis/014-retrieve-name-after',False);p=self.inspect_packet(x);self.assertEqual(p.returncode,0,p.stdout);self.assertTrue(json.loads(p.stdout)['diagnosis_only'])
  x['authority']='existing-original';self.assert_refusal(self.inspect_packet(x),'DiagnosticRelabel')
 def test_real_public_replay_refuses_before_dispatch_and_after_type(self):
  before=self.packet('r1/f1/prompt');after=self.packet();p=self.inspect_packet({'before':before,'after':after},'simulate');self.assertEqual(p.returncode,0,p.stdout);d=json.loads(p.stdout);self.assertEqual(len(d['actions']),1);self.assertFalse(d['enter_or_next_key_authorized']);self.assertEqual(d['real_guest_keys'],0)
  before=self.alter_text(before,before['text'].replace('(List Files)','(Other Menu)'));p=self.inspect_packet({'before':before,'after':after},'simulate');self.assertEqual(self.assert_refusal(p)['simulated_actions_before_refusal'],[])
  before=self.packet('r1/f1/prompt');after=self.alter_text(after,after['text'].replace('MISSING','MISSINX'));d=self.assert_refusal(self.inspect_packet({'before':before,'after':after},'simulate'));self.assertEqual(len(d['simulated_actions_before_refusal']),1);self.assertEqual(d['simulated_actions_before_refusal'][0]['simulated_only'],'type-field')
 def test_local_hashes_are_not_original_authority(self):
  x=self.packet();x['custody']['text_sha256']='0'*64;self.assert_refusal(self.inspect_packet(x),'LocalIntegrity')
 def test_no_source_input_or_nonregular_IO(self):
  import os
  p=self.invoke('plan','--output',HERE/'oracle.py');self.assert_refusal(p,'ReportOwnership')
  with tempfile.TemporaryDirectory()as tmp:
   tmp=Path(tmp);packet=tmp/'packet';packet.write_text(json.dumps(self.packet()))
   self.assert_refusal(self.invoke('inspect','--packet',packet,'--output',packet),'ReportInputCollision')
   fifo=tmp/'fifo';os.mkfifo(fifo);self.assert_refusal(self.invoke('inspect','--packet',fifo),'InputFileType')
   link=tmp/'link';link.symlink_to(packet);self.assert_refusal(self.invoke('inspect','--packet',link),'InputIO')
 def test_individual_frame_cursor_VGA_budgets(self):
  x=self.packet();x['text']='x'*8193;self.assert_refusal(self.inspect_packet(x),'FrameBudget')
  for raw in ['G'*8000,'0'*7999]:
   x=self.packet();x['vga_hex']=raw;self.assert_refusal(self.inspect_packet(x),'VGAEnvelope')
  x=self.packet();x['cursor']['oversized']='x'*8193;self.assert_refusal(self.inspect_packet(x),'CursorSchema')
 def test_invalid_budgets_atomic_report_and_run_grant_refusal(self):
  with tempfile.TemporaryDirectory()as tmp:
   tmp=Path(tmp);packet=tmp/'large';packet.write_bytes(b' '*32769);out=tmp/'report';out.write_bytes(b'KEEP')
   self.assert_refusal(self.invoke('inspect','--packet',packet,'--output',out),'InputBudget');self.assertEqual(out.read_bytes(),b'KEEP')
   packet.write_text('{');self.assert_refusal(self.invoke('inspect','--packet',packet,'--output',out),'PacketJSON');self.assertEqual(out.read_bytes(),b'KEEP')
   self.assert_refusal(self.invoke('check','--bad-flag','--output',out),'CLIArguments');self.assertEqual(out.read_bytes(),b'KEEP')
   self.assert_refusal(self.invoke('run','--grant',tmp/'not-read','--allow-vm','--output',out),'OriginalStageBlocked');self.assertEqual(out.read_bytes(),b'KEEP')
   result=self.invoke('plan','--output',out);self.assertEqual(result.returncode,0);self.assertEqual(json.loads(out.read_text()),json.loads(result.stdout))

if __name__=='__main__':unittest.main()
