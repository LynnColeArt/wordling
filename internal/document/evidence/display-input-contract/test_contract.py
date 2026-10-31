"""Actual public CLI qualification tests; synthetic natives are never original candidates."""
from pathlib import Path
import copy,json,os,subprocess,sys,tempfile,unittest
O=Path(__file__).resolve().parent;ROOT=O.parents[3];CLI=O/'qualify.py'
class Contract(unittest.TestCase):
 def cli(self,*args,ok=True):
  p=subprocess.run([sys.executable,'-B',str(CLI),*map(str,args)],cwd=ROOT,capture_output=True,timeout=180)
  self.assertEqual(p.returncode,0 if ok else 1,p.stderr.decode());return json.loads(p.stdout if ok else p.stderr)
 def request(self,x,ok=True):
  with tempfile.TemporaryDirectory()as d:
   p=Path(d)/'request.json';p.write_text(json.dumps(x));return self.cli('qualify',p,ok=ok)
 def catalog(self):return self.cli('catalog')
 def baseline(self):return self.catalog()['examples']['native']
 def test_six_known_literals_unknown_config_preserves_values(self):
  r=self.request(self.baseline());self.assertEqual([f['literal_u16le_or_u8']for f in r['native']['font_fields']],[120,120,120,10,1,0]);self.assertFalse(r['runtime_display_ready']);self.assertEqual(r['selected_GENERAL']['status'],'unresolved');self.assertEqual(r['selected_STATUS']['status'],'unresolved')
 def test_phase_changes_applicability_not_native_facts(self):
  x=self.catalog()['examples']['later43'];later=self.request(x);self.assertEqual(later['observation']['status'],'captured_setting');x['phase']='first-save';earlier=self.request(x);self.assertEqual(earlier['observation']['status'],'supported_but_insufficient');self.assertEqual(later['native'],earlier['native'])
 def test_nonfixture_known_value_and_forged_original_rejected(self):
  x=self.baseline();a=self.request(x);raw=bytearray((ROOT/x['native']).read_bytes());f=a['native']['font_fields'][0];raw[f['absolute_offset']:f['absolute_offset']+2]=(137).to_bytes(2,'little')
  with tempfile.TemporaryDirectory()as d:
   p=Path(d)/'changed.WP5';p.write_bytes(raw);x['native']=str(p);x.pop('reference',None);r=self.request(x);self.assertEqual(r['native']['font_fields'][0]['literal_u16le_or_u8'],137);x['reference']=self.baseline()['reference'];e=self.request(x,ok=False);self.assertEqual(e['code'],'ReferenceNativeMismatch')
 def test_observed_unit_is_not_selected_setup(self):
  x=self.catalog()['examples']['later43'];x['requested_role']='selected_GENERAL';r=self.request(x);self.assertEqual(r['observation']['status'],'supported_but_insufficient');x['requested_role']='selected_STATUS';r=self.request(x);self.assertEqual(r['observation']['status'],'supported_but_insufficient')
 def test_forged_capture_rehash_not_authority(self):
  x=self.catalog()['examples']['later43'];x['claim']={'text':'arbitrary','sha256':'0'*64};self.assertEqual(self.request(x,ok=False)['code'],'ForgedObservation')
 def test_real_menu_unit_and_status_separate(self):
  c=self.catalog();x=c['examples']['later43'];x['requested_role']='observed_menu_unit';r=self.request(x);self.assertEqual(r['observation']['status'],'observed_menu_unit');self.assertTrue(r['observation']['source_fact']['unit_evidence_lines'])
  x['observation']='wp43-status-r1';x['phase']='before-first-save';x['requested_role']='observed_status_unit';r=self.request(x);self.assertEqual(r['observation']['status'],'observed_status_unit');self.assertEqual(r['selected_STATUS']['status'],'unresolved')
 def test_cross_run_source_forgery(self):
  x=self.catalog()['examples']['later43'];x['observation']=x['observation'].replace('/r1/','/r2/');self.assertEqual(self.request(x,ok=False)['code'],'ObservationBinding')
 def test_14_height_distinct_from_43_Auto(self):
  c=self.catalog();obs=next(o for o in c['observations'].values()if o['label']=='line-height-fixed');ref=next(r for r in c['references'].values()if r['run']==obs['run']);x=dict(native=ref['id'],reference=ref['id'],phase=obs['phase'],observation=obs['id']);r=self.request(x);self.assertIn('0.2',r['observation']['source_fact']['text']);r=self.request(c['examples']['later43']);self.assertIn('Auto',r['observation']['source_fact']['text'])
 def test_current_revision_does_not_self_qualify(self):
  x=self.baseline();r=self.request(x);x['current']=dict(native_sha256=r['native']['sha256'],configuration_revision='my-current-revision');r=self.request(x);self.assertEqual(r['current_applicability']['status'],'unresolved');x['current']['native_sha256']='0'*64;self.assertEqual(self.request(x,ok=False)['code'],'CurrentNativeMismatch')
 def test_malformed_native_and_selector(self):
  x=self.baseline();x['phase']='made-up-phase';self.assertEqual(self.request(x,ok=False)['code'],'PhaseSelector')
  with tempfile.TemporaryDirectory()as d:
   p=Path(d)/'bad';p.write_bytes(b'not native');x=dict(native=str(p));self.assertEqual(self.request(x,ok=False)['code'],'ProcessExit')
 def test_output_atomic_invalid_request_and_source_protection(self):
  out=O/'atomic-test.result.json';out.write_bytes(b'prior')
  try:
   with tempfile.TemporaryDirectory()as d:
    p=Path(d)/'request';p.write_bytes(b'{"native":1}');self.cli('qualify',p,'--output',out,ok=False);self.assertEqual(out.read_bytes(),b'prior')
   self.cli('catalog','--output',O/'qualify.py',ok=False)
  finally:out.unlink()
 def test_request_duplicate_deep_partial_and_nonregular(self):
  with tempfile.TemporaryDirectory()as d:
   p=Path(d)/'packet'
   for raw in [b'{"native":0,"native":1}',b'{',b'['*60+b'0'+b']'*60,b'x'*65537]:
    p.write_bytes(raw);self.cli('qualify',p,ok=False)
   p.unlink();os.mkfifo(p);self.cli('qualify',p,ok=False)
 def test_symlink_native_and_output_refused(self):
  x=self.baseline()
  with tempfile.TemporaryDirectory()as d:
   p=Path(d)/'link';p.symlink_to(ROOT/x['native']);x['native']=str(p);self.assertEqual(self.request(x,ok=False)['code'],'SymlinkInput')
  p=O/'symlink-test.result.json'
  try:p.symlink_to(O/'authority.json');self.assertEqual(self.cli('catalog','--output',p,ok=False)['code'],'OutputType')
  finally:p.unlink(missing_ok=True)
 def test_packet6_raw_values_not_CPI_DPI_percentage(self):
  r=self.request(self.baseline());fs={f['name']:f for f in r['native']['prefix_fields']if f['owner']=='packet-6'};self.assertEqual(fs['screen character width']['value'],120);self.assertEqual(fs['display pitch']['value'],0);self.assertEqual(fs['screen resolution']['value'],0);self.assertIn('observed0',fs['display pitch']['unit'])
 def test_repeat_and_permutation_are_independent(self):
  x=self.baseline();a=self.request(x);x=dict(reversed(list(x.items())));b=self.request(x);self.assertEqual(a,b);a['native']['font_fields'][0]['literal_u16le_or_u8']=999;self.assertEqual(self.request(x),b)
 def test_changed_owner_index_not_unchecked_value_claim(self):
  x=self.baseline();r=self.request(x);packet=next(p for p in r['native']['inspection']['Packets']if p['Type']==15);raw=bytearray((ROOT/x['native']).read_bytes());start=packet['Index']['Offset'];raw[start:start+2]=(14).to_bytes(2,'little')
  with tempfile.TemporaryDirectory()as d:
   p=Path(d)/'owner.WP5';p.write_bytes(raw);x=dict(native=str(p));self.assertEqual(self.request(x,ok=False)['code'],'FontOwner')
  x=self.baseline();x['font_fields']=[dict(owner='packet-15',value=120)];self.assertEqual(self.request(x,ok=False)['code'],'RequestShape')
 def test_old_new_full_operand_frames_and_unknown_payload_retained(self):
  c=self.catalog();ref=next(r for r in c['references'].values()if 'L1-WRAP-L3-LR' in r['run']and 'CHANGE' in r['phase']);r=self.request(dict(native=ref['id'],reference=ref['id'],phase=ref['phase']));fields=[f for outer in r['native']['format_fields']for f in outer['fields']];labels=[f['label']for f in fields];self.assertIn('old left',labels);self.assertIn('new left',labels);self.assertTrue(all('raw_hex'in outer for outer in r['native']['format_fields']))
 def test_owned_source_pin_and_actual_Go_SET_failure(self):
  p=O/'authority.json';before=p.read_bytes()
  try:
   x=json.loads(before);x['sources'][0]['sha256']='0'*64;p.write_text(json.dumps(x));self.assertEqual(self.cli('catalog',ok=False)['code'],'SourceGitMismatch')
  finally:p.write_bytes(before)
  p=O/'reader-inputs.json';before=p.read_bytes()
  try:
   x=json.loads(before);x['files'].pop('internal/wp51/native.go');p.write_text(json.dumps(x));self.assertEqual(self.request(self.baseline(),ok=False)['code'],'ReaderSourceSet')
  finally:p.write_bytes(before)
 def test_actual_Go_env_overlay_refused_before_compile(self):
  x=self.baseline()
  with tempfile.TemporaryDirectory()as d:
   env=Path(d)/'goenv';env.write_text('GOFLAGS=-overlay=/absent-test-overlay\n');packet=Path(d)/'request';packet.write_text(json.dumps(x));inherited=os.environ.copy();inherited['GOENV']=str(env);inherited.pop('GOFLAGS',None)
   p=subprocess.run([sys.executable,'-B',str(CLI),'qualify',str(packet)],cwd=ROOT,env=inherited,capture_output=True,timeout=30);self.assertEqual(p.returncode,1);self.assertEqual(json.loads(p.stderr)['code'],'GoEnvironment')
 def test_selected_raw14_corroboration_and_actual13_status(self):
  c=self.catalog();self.assertEqual(c['unselected_report_only14'],546);obs14=[o for o in c['observations'].values()if o['document_family'].startswith('wp14/')];self.assertEqual(len(obs14),126)
  for o in obs14:self.assertEqual((ROOT/o['source']).read_text(),o['text'])
  obs=next(o for o in c['observations'].values()if o['document_family']=='wp13-CURSOR');ref=next(r for r in c['references'].values()if r['run']==obs['run']);r=self.request(dict(native=ref['id'],reference=ref['id'],observation=obs['id'],phase=obs['phase'],requested_role='observed_status_unit'));self.assertEqual(r['observation']['status'],'observed_status_unit');self.assertFalse(r['runtime_display_ready']);self.assertEqual(r['selected_STATUS']['status'],'unresolved')
if __name__=='__main__':unittest.main(verbosity=2)





