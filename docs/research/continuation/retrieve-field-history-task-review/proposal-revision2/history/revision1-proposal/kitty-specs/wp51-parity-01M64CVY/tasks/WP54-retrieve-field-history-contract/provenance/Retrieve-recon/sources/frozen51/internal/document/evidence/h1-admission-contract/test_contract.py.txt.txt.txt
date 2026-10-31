"""Offline integrity controls only; no original guests or permission experiments."""
import sys
sys.dont_write_bytecode=True
import unittest,json,copy,tempfile,types,subprocess
from pathlib import Path
from unittest.mock import patch
import frames,protocol,oracle,stage1,families,recipes
class Frames(unittest.TestCase):
 def setUp(self):self.spec=frames.normal('ABCD','H1INPUT',2);self.good=frames.expected(self.spec);self.cursor={'row':0,'column':2}
 def test_actual_blank_Typeover_and_Reveal_sources_match_full_composition(self):
  atlas=frames.atlas()
  for name,spec in [('blank',frames.normal('',None,0)),('typeover',frames.normal('aXc',None,2,True)),('reveal',frames.normal('AD','N0048',1,False,True))]:
   pin=atlas['templates'][name];cursor=json.loads((frames.ROOT/pin['path']).with_name('cursor.json').read_text());self.assertEqual(frames.expected(spec),pin['text']);frames.check(pin['text'],spec,cursor)
 def test_real_helper_unknown_centered_modal_is_not_main_authority(self):
  lines=frames.rows(self.good);lines[10]=' '*25+'No text to print';bad='\n'.join(lines)+'\n';self.assertTrue(frames.macro_session.main_document(bad));self.assertEqual(frames.macro_quit.exit_state(bad),'main')
  with self.assertRaises(frames.Refusal)as e:frames.check(bad,self.spec,self.cursor)
  self.assertEqual(e.exception.code,'UnknownFrame')
 def test_all_middle_rows_status_mode_doc_cursor_and_shapes(self):
  for row in range(1,24):
   lines=frames.rows(self.good);lines[row]='unqualified modal/ruler';bad='\n'.join(lines)+'\n'
   with self.assertRaises(frames.Refusal):frames.check(bad,self.spec,self.cursor)
  for bad in [self.good.replace('ABCD','ABCE'),self.good.replace('Doc 1','Doc 2'),self.good.replace('Pg 1','Pg 2'),self.good.replace('Pos 1.2','Pos 1.3'),self.good+'\n',self.good.replace('C:\\OUT\\H1INPUT','Typeover')]:
   with self.assertRaises(frames.Refusal):frames.check(bad,self.spec,self.cursor)
  for cursor in [None,{'row':1,'column':2},{'row':0,'column':True},{'row':0,'column':3}]:
   with self.assertRaises(frames.Refusal):frames.check(self.good,self.spec,cursor)
 def test_known_normal_and_Reveal_actual_helper_composition_and_ruler(self):
  frames.check(self.good,self.spec,self.cursor);s=frames.normal('ABCD','H51S0',2,False,True);text=frames.expected(s);self.assertFalse(frames.macro_session.main_document(text));self.assertEqual(frames.macro_quit.exit_state(text),'unknown');self.assertEqual(len(frames.rows(text)),25);self.assertGreater(len(text.splitlines()),25);frames.check(text,s,self.cursor)
  with self.assertRaises(frames.Refusal):frames.check(text.replace('\x1e',' '),s,self.cursor)
 def test_unknown_before_key_no_dispatch_and_after_key_no_second_dispatch(self):
  for when in ['before','after']:
   with tempfile.TemporaryDirectory()as tmp:
    core=types.SimpleNamespace(out=Path(tmp),trace=[],exports=[]);calls=[];screens=[self.good,self.good];lines=frames.rows(self.good);lines[12]='centered unknown';screens[0 if when=='before'else 1]='\n'.join(lines)+'\n'
    def capture(label):
     d=core.out/label;d.mkdir();(d/'cursor.json').write_text(json.dumps(self.cursor));return screens.pop(0)
    core.capture=capture;core.key=lambda key:calls.append(key);p=protocol.Protocol(core)
    with self.assertRaises(frames.Refusal):p.step('right',self.spec,self.spec,'fault')
    self.assertEqual(calls,[]if when=='before'else['right'])
 def test_unknown_save_clear_print_and_DOS_refuse(self):
  for kind in ['save','clear-save','exit-wp','print-C46PRN-menu','dos']:
   spec={'kind':kind,'body':'ABCD','name':'H51S0'};text=frames.expected(spec);lines=frames.rows(text);lines[10]='unknown centered dialog';bad='\n'.join(lines)+'\n'
   with self.assertRaises(frames.Refusal):frames.check(bad,spec)
class ReadOnlyFacts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.rows=json.loads((oracle.HERE/'readonly-probe-84.json').read_text())
 def test_actual84_native_export_and72_field_facts(self):
  self.assertEqual(len(self.rows),84)
  for r in self.rows:
   f=stage1.facts(r);self.assertEqual(len(f['all72_fields']),72);self.assertTrue(r['ExportExact']and r['OriginalExact'])
   if r['Admitted']:self.assertEqual(next(x['hex']for x in f['all72_fields']if x['owner']=='packet-6'and'printer-select counter'in x['name']),'01')
 def test_H1_fourFIN_one_class_refusal_and_PRE_Q_separation(self):
  fin=[r for r in self.rows[-12:]if r['Path'].endswith('C46FIN.WP5')];self.assertEqual(len(fin),4);self.assertEqual({r['SHA256']for r in fin},{oracle.H1})
  for r in fin:
   self.assertEqual(families.classify(r,'')['family'],'H1-R-e72402');self.assertFalse(r['Admitted']);self.assertEqual(r['Failure']['Span'],{'Offset':74,'Length':1})
  for r in self.rows[-12:]:
   if r['Path'].endswith('second-Go-edit.WP5'):self.assertEqual(r['BodyHex'],'51');self.assertTrue(r['Admitted'])
 def test_rehashed_wrong_source_graph_counter_refusal_and_field_drop(self):
  row=next(r for r in self.rows if r['SHA256']==oracle.H1)
  for transform in [lambda r:r.update(SHA256='0'*64),lambda r:r.update(Admitted=True),lambda r:r['Failure']['Span'].update(Offset=75),lambda r:r['Inspection']['Packets'].pop(),lambda r:r['Inspection']['Blocks'][0].update(Next=0)]:
   bad=copy.deepcopy(row);transform(bad)
   with self.assertRaises((AssertionError,frames.Refusal,ValueError)):families.classify(bad,'')
 def test_all72_rehashed_actual_decoder_field_faults_block(self):
  row=next(r for r in self.rows if r['SHA256']==oracle.H1);facts=stage1.facts(row);raw=(stage1.ROOT/row['Path']).read_bytes()
  with tempfile.TemporaryDirectory()as tmp:
   paths=[]
   for index,field in enumerate(facts['all72_fields']):
    altered=bytearray(raw);altered[field['absolute']]^=0x80;p=Path(tmp)/str(index);p.write_bytes(altered);paths.append(p)
   rows=oracle.probe(paths);self.assertEqual(len(rows),72)
   for index,r in enumerate(rows):
    with self.subTest(field=facts['all72_fields'][index]['name']):
     with self.assertRaises((AssertionError,frames.Refusal,ValueError,KeyError)):families.classify(r,'')
 def test_actual_profile_drift_refuses_offline(self):
  original=json.loads
  def loads(text,*args,**kwargs):
   value=original(text,*args,**kwargs)
   if isinstance(value,dict)and 'master_boot_sha256'in value and 'profile_id'in value:value['master_boot_sha256']='0'*64
   return value
  with patch.object(oracle.json,'loads',side_effect=loads):
   with self.assertRaises(frames.Refusal)as e:oracle.plan()
  self.assertEqual(e.exception.code,'MasterDrift')
 def test_no_qualified_stage2_or_sufficient_permission_from_partial(self):
  with self.assertRaises(frames.Refusal):families.decision([])
  rows=[{'qualification':{'prospective_branch':'uniform-known-reordered01-alternate'}}for _ in range(8)];d=families.decision(rows);self.assertFalse(d['future_structural_or_fallback_permission']);self.assertIn('BLOCKED',d['B_disposition']);rows[-1]['qualification']['prospective_branch']='uniform-H1-reload-known-print-transition'
  with self.assertRaises(frames.Refusal):families.decision(rows)
class Recipe(unittest.TestCase):
 def test_four_exact_initial_and_reload_logical_sequences_no_native_emission(self):
  class Dry(protocol.Protocol):
   def capture(self,spec,label):self.count+=1;frames.check(frames.expected(spec),spec,{'row':0,'column':spec['gap']}if spec['kind']in ['normal','reveal']else None);return frames.expected(spec)
  for index in range(4):
   p=Dry(types.SimpleNamespace(type=lambda x:None,key=lambda x:None));p.name='H1INPUT';p.operations(recipes.operation_plan(index)['before_Save_S0']);self.assertEqual(p.body,recipes.EXPECTED[index][0]);p.gap=0;p.operations(recipes.operation_plan(index)['after_clear_Retrieve_S0']);self.assertEqual(p.body,recipes.EXPECTED[index][1])
 def test_ledger_exact_types_sticky_halt_cap_no_reset(self):
  p={'pinned':'isolated'};l=oracle.empty_ledger(p);oracle.ledger_check(p,l)
  for field,value in [('historical46_spent',0),('maximum_new_attempts_including_failures',8.0),('halted',True),('halted',0)]:
   bad=copy.deepcopy(l);bad[field]=value
   with self.assertRaises(frames.Refusal):oracle.ledger_check(p,bad)
 def test_unauthorized_run_no_private_authority(self):
  with patch.object(oracle,'check',side_effect=AssertionError('must not check')):
   with self.assertRaises(frames.Refusal)as e:oracle.run(types.SimpleNamespace(allow_vm=False))
  self.assertEqual(e.exception.code,'AuthorizationRequired')
 def test_exact_eight_selection_no_subset_float_cap_or_old_ID(self):
  p={'attempts':recipes.leaves(Path('/isolated'))};args=types.SimpleNamespace(grant_id='wp51-test',attempt=[r['id']for r in p['attempts']]);g={'authorized':True,'grant_id':args.grant_id,'attempt_ids':args.attempt,'plan_sha256':oracle.canonical(p),'maximum_new_attempts_including_failures':8,'historical46_spent_unchanged':13,'authorization_note':'isolated unit only'};oracle.selected(args,p,g)
  for field,value in [('authorized',False),('maximum_new_attempts_including_failures',8.0),('historical46_spent_unchanged',0),('historical46_spent_unchanged',13.0)]:
   bad=copy.deepcopy(g);bad[field]=value
   with self.assertRaises(frames.Refusal):oracle.selected(args,p,bad)
  args.attempt=args.attempt[:1]
  with self.assertRaises(frames.Refusal):oracle.selected(args,p,g)
if __name__=='__main__':unittest.main()
