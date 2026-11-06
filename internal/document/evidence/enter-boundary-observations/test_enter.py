"""Public entrypoint and actual safety-seam tests. No reference guest/private resource."""
from pathlib import Path
import json,subprocess,sys,tempfile,unittest
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];CLI=HERE/'enter_oracle.py'
class Public(unittest.TestCase):
 def cli(self,*args,ok=True):
  p=subprocess.run([sys.executable,'-B',str(CLI),*map(str,args)],cwd=ROOT,capture_output=True,timeout=60);self.assertEqual(p.returncode,0 if ok else 1,p.stderr.decode());return json.loads(p.stdout if ok else p.stderr)
 def test_exact_public_startup_signature_refuses_missing_seams(self):
  r=self.cli('source-check');c=r['startup_contract'];self.assertEqual(c['signature'],'(qmp, guest, work, assets)');self.assertTrue(all(c['unsupported_parameters'].values()));self.assertTrue(c['direct_subprocess_calls']);self.assertFalse(c['run_enabled'])
 def test_run_always_refuses_before_original_authority_IO(self):
  r=self.cli('run','--allow-vm','--grant','/absent-no-open-grant','--source-review','/absent-no-open-review',ok=False);self.assertEqual(r['error'],'SourceContractPrereq');self.assertEqual(r['actual_original_launched'],0);self.assertEqual(r['original_tickets_spent'],0);self.assertFalse(r['original_authority_IO'])
 def test_plan_fixed_four_not_current_key_authority(self):
  p=self.cli('plan');self.assertEqual([x['mode']for x in p['leaves']],['Insert','Insert','Typeover','Typeover']);self.assertEqual(len(set(x['private_work']for x in p['leaves'])),4);self.assertFalse(p['run_enabled']);self.assertEqual(p['leaves'][0]['PRE_literal'],p['leaves'][1]['PRE_literal'])
 def test_real_post_launch_unknown_not_zero(self):
  r=self.cli('simulate','--fault','unknown');self.assertEqual(r['counts'],dict(abandoned=3,incomplete=1,launch_unknown=1,not_attempted=0,positively_proved=0,tickets_spent=1));self.assertEqual(len(r['OS_processes']),1);self.assertTrue(all(p['pid_absent']for p in r['OS_processes'].values()));self.assertEqual(r['actual_original_launched'],0)
 def test_real_positive_kernel_identity_retained_then_failure(self):
  r=self.cli('simulate','--fault','proved');self.assertEqual(r['counts']['positively_proved'],1);self.assertEqual(r['counts']['launch_unknown'],0);identity=r['launch_ledger']['attempts'][0]['identity'];pid=next(iter(r['OS_processes'].values()))['fixture_pid'];self.assertEqual(identity['pid'],pid);self.assertTrue(identity['startticks'].isdigit());self.assertEqual(r['counts']['abandoned'],3)
 def test_first_setup_fault_charged_no_child_sticky(self):
  r=self.cli('simulate','--fault','setup');self.assertEqual(r['counts']['tickets_spent'],1);self.assertEqual(r['counts']['not_attempted'],1);self.assertEqual(r['counts']['abandoned'],3);self.assertEqual(r['OS_processes'],{});self.assertTrue(r['ticket_ledger']['halted'])
 def test_audit_and_publication_fault_stop_NEXT(self):
  for kind in ['audit','publish']:
   r=self.cli('simulate','--fault',kind);self.assertEqual(len(r['OS_processes']),1);self.assertEqual(r['counts']['tickets_spent'],1);self.assertTrue(r['ticket_ledger']['halted']);self.assertTrue(r['audit_checks'][0]['physical_free_during_audit']);self.assertFalse(r['audit_checks'][0]['ROOT_logical_release_claimed'])
 def test_real_halt_persistence_refuses_foreign_write(self):
  r=self.cli('simulate','--fault','halt-persistence');self.assertEqual(r['error']['code'],'HaltPersistenceFailed');self.assertTrue(r['foreign_test_ledger_unchanged']);self.assertEqual(r['counts']['tickets_spent'],1);self.assertEqual(r['OS_processes'],{})
 def test_four_harmless_children_same_owner_and_released_lock(self):
  r=self.cli('simulate','--fault','success');self.assertIsNone(r['error']);self.assertEqual(r['counts']['positively_proved'],4);self.assertEqual(len(r['audit_checks']),4);self.assertTrue(all(x['physical_free_during_audit']for x in r['audit_checks']));self.assertTrue(r['fixture_only']);self.assertFalse(r['original_qualification'])
 def test_actual_native72_and_opaque_0A_not_outer_HR(self):
  r=self.cli('native-check');self.assertEqual(r['source_gate'],65536);self.assertEqual(len(r['observations']),2)
  for row in r['observations']:self.assertEqual(len(row['all72_fields']),72);self.assertTrue(row['exact_native_framing_and_export'])
  for row in r['outer_token_corroboration']:self.assertEqual(row['outer_HR_count'],1);self.assertGreater(bytes.fromhex(row['body_hex']).count(b'\x0a'),1)
 def request(self,obj,ok=True):
  with tempfile.TemporaryDirectory()as d:
   p=Path(d)/'request';p.write_text(json.dumps(obj));return self.cli('inspect-rule','--input',p,ok=ok)
 def example(self):return dict(mode='Insert',lines=['a','bc'],caret=[1,0],phase='split',provenance='prospective-manual-and-qualified-components-only')
 def test_finite_semantic_component_never_full_frame_or_permission(self):
  x=self.example();r=self.request(x);self.assertFalse(r['live_full_frame_match']);self.assertFalse(r['key_permission']);self.assertFalse(r['original_qualification']);x['mode']='Typeover';self.assertTrue(self.request(x)['semantic_prospective_match'])
 def test_rehashed_lost_b_mode_doc2_caret_provenance_forgeries(self):
  import copy
  x=self.example()
  for key,value in [('lines',['a','c']),('lines',['abc']),('lines',['a','bc','extra']),('caret',[False,0]),('mode','Doc2'),('provenance','historical-original-qualified')]:
   y=copy.deepcopy(x);y[key]=value;self.request(y,ok=False)
  x['key_permission']=True;self.request(x,ok=False)
 def test_changed_literal_pure_rule_not_historical_permission(self):
  x=self.example();x['literal']='C:\\OUT\\EXAMPLE';r=self.request(x);self.assertEqual(r['literal_ASCII_hex'],x['literal'].encode().hex());self.assertFalse(r['key_permission'])
  for v in ['C:/OUT/EXAMPLE','C:\\OUT\\..','c:\\OUT\\EXAMPLE','C:\\OUT\\TOOLONG99']:
   x['literal']=v;self.request(x,ok=False)
 def test_repeated_plan_sourcecheck_deterministic_copy(self):
  self.assertEqual(self.cli('preflight'),self.cli('preflight'));x=self.cli('plan');x['leaves'][0]['initial_text']='other';self.assertEqual(self.cli('plan')['leaves'][0]['initial_text'],'abc')
 def test_invalid_input_preserves_prior_publication(self):
  p=HERE/'atomic.result.json';p.write_bytes(b'prior')
  try:
   with tempfile.TemporaryDirectory()as d:
    f=Path(d)/'bad';f.write_text('{');self.cli('inspect-rule','--input',f,'--output',p,ok=False);self.assertEqual(p.read_bytes(),b'prior')
   self.cli('plan','--output',HERE/'enter_oracle.py',ok=False)
  finally:p.unlink()
 def test_real_foreign_peer_receives_zero_commands(self):
  r=self.cli('peer-check','--fault','foreign');self.assertEqual(r['error'],'QMPEndpointPeerMismatch');self.assertEqual(r['wire'],'');self.assertFalse(r['original_qualification'])
 def test_real_owned_quit_issued_receipt_and_JSON_retarget_refusal(self):
  r=self.cli('peer-check');self.assertTrue(r['issued_receipt']['actual_quit_command']);self.assertTrue(r['issued_receipt']['successful_quit_reply']);self.assertEqual([json.loads(x)['execute']for x in r['wire'].splitlines()],['qmp_capabilities','quit'])
if __name__=='__main__':unittest.main(verbosity=2)
