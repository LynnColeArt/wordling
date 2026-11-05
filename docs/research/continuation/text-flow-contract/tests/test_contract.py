"""Source-backed WP49 public CLI/semantic/custody negatives; never a guest."""
import copy,importlib,json,os,time
import xml.etree.ElementTree as ET
from pathlib import Path
import subprocess,sys,tempfile,unittest
from unittest import mock
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'scripts/reference'))
import text_flow_contract as t

class Contract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.value=t.check();cls.rows=cls.value['data']['runs'];cls.c=t.Custody();cls.tokenizer,cls.analyzer=t.helpers(cls.c)
        cls.raw=(ROOT/cls.rows[0]['states'][0]['after_path']).read_bytes()
    def test_complete_source_reader_pairs_and_fields(self):
        d=self.value['data'];self.assertEqual(len(d['runs']),18);self.assertEqual(len(d['actual_reader']['outputs']),64)
        self.assertTrue(all(x['accepted']and x['exact_export']for x in d['actual_reader']['outputs']))
        self.assertEqual(len({x['variant']for x in self.rows}),9);self.assertEqual(sum(len(x['states'])for x in self.rows),32)
        self.assertFalse(d['summary']['closed_layout_or_emitter']);self.assertFalse(d['summary']['stage2_justified'])
        for r in self.rows:
            self.assertTrue(r['actual_settings']);self.assertTrue(r['trace'])
            for s in r['states']:
                for f in s['after']['format_fields']:
                    for field in f['fields']:
                        native=(ROOT/s['after_path']).read_bytes();start=field['absolute_offset'];self.assertEqual(native[start:start+field['width']].hex(),field['raw_hex'])
    def test_literal_font_fields_are_sourced_not_CPI_inference(self):
        defs=self.c.json('docs/research/continuation/native-edits/field-ledger.json',t.WP43)['field_coverage']
        for r in self.rows:
            for s in r['states']:
                fs=s['after']['selected_font_fields'];self.assertEqual(len(fs),6)
                width=next(x for x in fs if x['name']=='printed character width')
                self.assertEqual(width['units'],'WPU');self.assertEqual(width['literal_u16le_or_u8'],120)
                raw=(ROOT/s['after_path']).read_bytes()
                for f in fs:self.assertEqual(raw[f['absolute_offset']:f['absolute_offset']+f['width']].hex(),f['raw_hex'])
        wrong=copy.deepcopy(defs);next(x for x in wrong if x['name']=='printed character width')['offset']=65535
        with self.assertRaises(t.Refusal):t.prefix_font_fields(self.raw,self.tokenizer,wrong)
        with self.assertRaises(ValueError):t.prefix_font_fields(b'',self.tokenizer,defs)
    def test_real_flow_dormant_and_full_stream_rules(self):
        rules={x['id']:x for x in self.value['data']['rules']};self.assertEqual(rules['FLOW-HR']['observable']['native_lines'],['alpha','beta'])
        self.assertTrue(rules['FLOW-AUTO-DORMANT']['observable']['BASE_DORMANT_full_PRN_equal'])
        self.assertTrue(rules['FLOW-AUTO-DORMANT']['observable']['CHANGE_full_PRN_different'])
        self.assertEqual(rules['FLOW-WRAP-MARGINS']['observable']['changed_LR_soft_0d'],7)
        self.assertTrue(all(not x['layout_or_emitter_permission']for x in rules.values()))
    def test_protocol_body_difference_is_preserved_not_masked(self):
        row=next(x for x in self.rows if x['variant']=='L2-DORMANT'and x['repetition']==1)
        change=next(x for x in row['states']if x['id']=='CHANGE')
        self.assertNotEqual(change['before']['body_sha256'],change['after']['body_sha256'])
        self.assertFalse(change['native_difference']['equal'])
        self.assertIn('no single-action',change['difference_scope'])
    def test_outer_opaque_payload_does_not_invent_returns(self):
        # Change one payload byte in a complete variable function; outer framing
        # remains real, no host file/fixture is rewritten.
        info=self.tokenizer.annotate(self.raw);token=next(x for x in info['tokens']if x['kind']=='opaque-function'and len(bytes.fromhex(x['hex']))>=12)
        raw=bytearray(self.raw);raw[token['offset']+4]=0x0a
        result=t.observe_native(bytes(raw),self.tokenizer,self.analyzer)
        self.assertEqual(result['counts'].get('hard-return'),info['counts'].get('hard-return'))
        self.assertFalse(result['generator_permission'])
    def test_malformed_frame_and_limits(self):
        info=self.tokenizer.annotate(self.raw);B=info['document_offset']
        for raw in [b'',self.raw[:15],self.raw[:B]+b'\x00',self.raw[:B]+b'\xd0\x01\xff\xff',b'x'*(self.tokenizer.LIMIT+1)]:
            with self.subTest(length=len(raw)):
                with self.assertRaises(ValueError):t.observe_native(raw,self.tokenizer,self.analyzer)
    def test_rehashed_owners_units_profile_case_PRN_and_permission_refused(self):
        changes=[('owner',lambda x:next(f for f in x['data']['runs'][0]['states'][0]['after']['format_fields']if f['fields'])['fields'][0].update(owner='invented')),
         ('width',lambda x:next(f for f in x['data']['runs'][0]['states'][0]['after']['format_fields']if f['fields'])['fields'][0].update(width=1)),
         ('unit',lambda x:next(f for f in x['data']['runs'][0]['states'][0]['after']['format_fields']if f['fields'])['fields'][0].update(unit='DPI')),
         ('boundary',lambda x:x['data']['runs'][0]['states'][0]['after']['tokens'][0].update(kind='hard-page')),
         ('setting',lambda x:x['data']['runs'][0]['intended_settings'].update(line_height_inches='1')),
         ('profile',lambda x:x['data']['runs'][0].update(profile_sha256='0'*64)),
         ('resource',lambda x:x['data']['runs'][0]['resource_metadata'][0].update(sha256='0'*64)),
         ('PRN-truncate',lambda x:x['data']['runs'][0]['states'][0]['full_PRN'].update(full_hex='41')),
         ('PRN-swap',lambda x:x['data']['runs'][0]['states'][0].update(full_PRN=x['data']['runs'][-1]['states'][0]['full_PRN'])),
         ('samebytes-wrongcase',lambda x:x['data']['runs'][0].update(variant='L2-AUTO')),
         ('samebytes-wrongrepeat',lambda x:x['data']['runs'][0].update(repetition=2)),
         ('stalesource',lambda x:x['data']['sources'][0].update(sha256='0'*64)),
         ('permission',lambda x:x['data']['rules'][0].update(layout_or_emitter_permission=True))]
        with tempfile.TemporaryDirectory()as d,mock.patch.object(t,'check',return_value=self.value):
            p=Path(d)/'report'
            for name,change in changes:
                value=copy.deepcopy(self.value);change(value);value['data_sha256']=t.sha(t.canonical(value['data']));p.write_text(json.dumps(value))
                with self.subTest(name=name):
                    with self.assertRaises(t.Refusal)as e:t.result(p)
                    self.assertEqual(e.exception.code,'SemanticMismatch')
    def test_immutable_Git_input_not_local_rehash(self):
        with tempfile.TemporaryDirectory()as d:
            p=Path(d)/'raw';p.write_bytes(b'changed')
            with mock.patch.object(t,'ROOT',Path(d)),mock.patch.object(t.Custody,'tree',return_value={'raw':'0'*40}):
                with self.assertRaises(t.Refusal)as e:t.Custody().read('raw')
                self.assertEqual(e.exception.code,'ImmutableSourceMismatch')
    def test_bad_JSON_limit_and_regular_files(self):
        with tempfile.TemporaryDirectory()as d:
            p=Path(d)/'report';p.write_text('{')
            with self.assertRaises(t.Refusal):t.result(p)
            p.write_bytes(b'x'*(t.REPORT_LIMIT+1))
            with self.assertRaises(t.Refusal):t.result(p)
            link=Path(d)/'link';link.symlink_to(p)
            with self.assertRaises(t.Refusal):t.bounded(link)
    def test_output_aliases_preserve_input_inode(self):
        with tempfile.TemporaryDirectory(dir=t.OUT)as own,tempfile.TemporaryDirectory()as ext:
            source=Path(ext)/'native';source.write_bytes(self.raw);dest=Path(own)/'report';os.link(source,dest)
            t.publish(dest,'{"offline":true}')
            self.assertEqual(source.read_bytes(),self.raw);self.assertNotEqual(dest.stat().st_ino,source.stat().st_ino)
            link=Path(own)/'link';link.symlink_to(source)
            with self.assertRaises(t.Refusal):t.publish(link,'no')
            self.assertEqual(source.read_bytes(),self.raw)
    def test_real_public_CLI_recompute_and_no_run(self):
        script=ROOT/'scripts/reference/text_flow_contract.py'
        with tempfile.TemporaryDirectory()as d:
            path=Path(d)/'report';path.write_text(json.dumps(self.value))
            for args,code in [(['result',str(path)],0),(['plan'],0),(['run'],1),(['plan','--output','/tmp/WP49-unowned-output'],1)]:
                p=subprocess.run([sys.executable,str(script),*args],cwd=ROOT,capture_output=True,text=True,timeout=60)
                self.assertEqual(p.returncode,code,p.stderr)
            value=copy.deepcopy(self.value);value['data']['summary']['closed_layout_or_emitter']=True;value['data_sha256']=t.sha(t.canonical(value['data']));path.write_text(json.dumps(value))
            p=subprocess.run([sys.executable,str(script),'result',str(path)],cwd=ROOT,capture_output=True,text=True,timeout=60)
            self.assertEqual(p.returncode,1);self.assertIn('SemanticMismatch',p.stderr)

class Recording(unittest.TextTestResult):
    def startTest(self,test):self.at=time.monotonic();super().startTest(test)
    def stopTest(self,test):
        row=ET.SubElement(self.suite,'testcase',name=test.id(),time=f'{time.monotonic()-self.at:.6f}')
        for t,msg in self.failures+self.errors:
            if t is test:ET.SubElement(row,'failure').text=msg
        super().stopTest(test)

if __name__=='__main__':
    Recording.suite=ET.Element('testsuite',name='WP49 offline text-flow evidence')
    result=unittest.TextTestRunner(resultclass=Recording,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Contract))
    for k,v in [('tests',result.testsRun),('failures',len(result.failures)),('errors',len(result.errors)),('skipped',len(result.skipped))]:Recording.suite.set(k,str(v))
    ET.ElementTree(Recording.suite).write(ROOT/'docs/research/continuation/text-flow-contract/evidence/tests.xml',encoding='unicode')
    sys.exit(not result.wasSuccessful())
