"""WP45 executable offline adversarial tests; never start/configure a guest."""
import copy
import importlib
import json
import os
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT/'scripts/reference'))
import resaved_prefix_relationships as tool

class Relationships(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.value = tool.check()
        cls.rows = cls.value['data']['images']
        cls.inherited, cls.inspector = tool.helpers()
        cls.row = next(x for x in cls.rows if x['case']=='two-bold-baseline' and x['stage']=='W42G3.WP5' and x['repetition']==1)
        cls.raw = (ROOT/cls.row['binding']['path']).read_bytes()

    def test_complete72_reader_fields_and_intervals(self):
        self.assertEqual(len(self.rows),72)
        for row in self.rows:
            d=row['diagnostic'];self.assertTrue(row['actual_go_reader']['accepted']);self.assertTrue(row['actual_go_reader']['exact_export'])
            self.assertEqual(len(d['fields']),72)
            self.assertEqual(sum(x['length'] for x in d['intervals']),d['body_offset'])
            self.assertFalse(d['body_reference_absence_proven']);self.assertFalse(d['mutation_permission'])
            for b in d['blocks']:
                covered=[f for f in d['index_fields'] if b['offset']<=f['offset']<b['offset']+50]
                self.assertEqual(sum(x['width'] for x in covered),50)

    def test_recompute63_promoted_provenance_candidates(self):
        old=json.loads((ROOT/'docs/research/continuation/reordered-prefix-design/existing-564-provenance-observations.json').read_text())['rows']
        self.assertEqual(len(old),63)
        for x in old:
            row=next(y for y in self.rows if y['case']==x['case'] and y['stage']==x['stage'] and y['repetition']==1)
            residual=next(y for y in row['diagnostic']['residuals'] if y['offset']==x['extent']['offset'] and y['length']==x['extent']['length'])
            self.assertEqual(residual['sha256'],x['sha256'])
            oldmatches={(m['stage'],m['type'],m['relative_offset'],m['absolute_offset']) for m in x['matches_known_live_payloads']}
            newmatches={(m['stage'],m['owner_type'],m['relative_offset'],m['absolute_offset']) for m in residual['literal_provenance_candidates']}
            self.assertEqual(oldmatches,newmatches)
            self.assertFalse(residual['unique_origin_proven'])
        self.assertEqual(sum(len(x['diagnostic']['residuals']) for x in self.rows),126)

    def test_partial_font_and_unowned_tail_not_typed_live(self):
        tail=next(x for x in self.row['diagnostic']['residuals'] if x['length']==70)
        self.assertTrue(all(x['relative_offset']==16 for x in tail['literal_provenance_candidates']))
        self.assertTrue(all(x['owner_type']==15 for x in tail['literal_provenance_candidates']))
        self.assertIn('opaque',tail['interpretation'])
        fin=next(x for x in self.rows if x['case']=='two-bold-baseline' and x['stage']=='W42FIN.WP5' and x['repetition']==1)
        gap=next(x for x in fin['diagnostic']['residuals'] if x['kind']=='unowned')
        self.assertEqual((gap['offset'],gap['length']),(252,4))
        self.assertTrue(all(x['owner_type']==12 and x['relative_offset']==86 for x in gap['literal_provenance_candidates']))
        self.assertTrue(any(not f['full_live_field'] for m in gap['literal_provenance_candidates'] for f in m['field_intersections']))

    def test_old_index_locations_not_reactivated_by_same_bytes(self):
        old=self.row['historical_index_ownership']
        self.assertTrue(any(x['historical_extent'][0]==270 and not x['currently_active_same_address'] for x in old))
        roots={n['extent'][0] for n in self.row['diagnostic']['active_root_graph']['nodes'] if n['kind']=='active-index'}
        self.assertEqual(roots,{16,272,512})
        self.assertNotIn(270,roots)

    def test_exact_stage_cache_counter_not_cartesian_union(self):
        for row in self.rows:
            fs=row['diagnostic']['fields'];cache=next(x['raw_hex'] for x in fs if x['name']=='descriptor match hash');counter=next(x['raw_hex'] for x in fs if x['name']=='printer-select counter for equation hash')
            self.assertEqual((cache,counter),('1172','02') if row['stage']=='W42FIN.WP5' else ('e724','01'))
            self.assertFalse(row['diagnostic']['mutation_permission'])

    def test_semantic_mutants_rehashed_envelopes_refused(self):
        # Public result validates actual sources/reader/semantics, not a caller boolean/digest.
        variants=[]
        def variant(label,change):
            value=copy.deepcopy(self.value);change(value);value['data_sha256']=tool.digest(tool.encode(value['data']));variants.append((label,value))
        variant('root',lambda x:x['data']['images'][0]['diagnostic']['active_root_graph']['edges'][0].update(target_offset=564))
        variant('next',lambda x:x['data']['images'][0]['diagnostic']['blocks'][0].update(next=0))
        variant('index',lambda x:x['data']['images'][0]['diagnostic']['index_fields'][0].update(width=4))
        variant('extent',lambda x:x['data']['images'][0]['diagnostic']['packets'][0].update(length=15))
        variant('alias',lambda x:x['data']['images'][0]['diagnostic']['intervals'][0]['owners'].append('packet15'))
        variant('residual',lambda x:x['data']['images'][2]['diagnostic']['residuals'][0].update(unique_origin_proven=True))
        variant('endian',lambda x:x['data']['images'][0]['diagnostic']['fields'][1].update(endian='big'))
        variant('domain',lambda x:x['data']['images'][0]['diagnostic']['active_root_graph']['edges'][0].update(base_domain='body-relative'))
        variant('cache',lambda x:x['data']['images'][0]['diagnostic']['fields'][20].update(raw_hex='1172'))
        variant('false-absence',lambda x:x['data']['images'][0]['diagnostic'].update(body_reference_absence_proven=True))
        variant('unowned-as-live',lambda x:x['data']['images'][-1]['diagnostic']['intervals'][0].update(status='free-safe'))
        variant('input-rehashed',lambda x:x['data']['images'][0]['binding'].update(sha256='0'*64))
        variant('source-rehashed',lambda x:x['data']['sources'][0].update(sha256='0'*64))
        variant('permission',lambda x:x['data']['summary'].update(mutation_permission=True))
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'report.json'
            # check itself ran against real source/Go above. Cache only that exact
            # immutable recomputation for the bounded report-tampering loop.
            with mock.patch.object(tool,'check',return_value=self.value):
                for label,value in variants:
                    with self.subTest(label=label):
                        p.write_text(json.dumps(value))
                        with self.assertRaises(tool.Refusal) as e:tool.result(p)
                        self.assertEqual(e.exception.code,'SemanticMismatch')

    def test_native_substitution_cannot_be_fixed_by_local_rehash(self):
        with tempfile.TemporaryDirectory() as directory:
            r=Path(directory);p=r/'input';p.write_bytes(self.raw[:-1]+b'Q')
            with mock.patch.object(tool,'ROOT',r),mock.patch.object(tool,'git_bytes',return_value=self.raw):
                with self.assertRaises(tool.Refusal) as e:tool.binding('input')
                self.assertEqual(e.exception.code,'ImmutableSourceMismatch')

    def test_malformed_boundary_and_relation_seeds(self):
        cases=[b'',self.raw[:15],self.raw[:40],self.raw+b'X'*65536]
        font=next(p for p in self.row['diagnostic']['packets'] if p['type']==15)
        for a,width,value in [(4,4,65537),(22,4,16),(28,4,65535),(32,4,65530),(font['offset']+18,2,65535)]:
            raw=bytearray(self.raw);raw[a:a+width]=value.to_bytes(width,'little');cases.append(bytes(raw))
        for raw in cases:
            with self.subTest(size=len(raw),sha=tool.digest(raw)):
                with self.assertRaises(ValueError):tool.diagnose(raw,self.inspector)

    def test_no_vm_or_lock_side_effects_and_public_cli(self):
        inherited=self.inherited
        with mock.patch.object(inherited,'plan',side_effect=AssertionError('old VM plan forbidden')),mock.patch.object(inherited,'run',side_effect=AssertionError('VM forbidden')):
            self.assertFalse(tool.plan()['run_enabled'])
        script=ROOT/'scripts/reference/resaved_prefix_relationships.py'
        for argv,expected in [(['plan'],0),(['run'],1),(['plan','--output','/tmp/WP45-forbidden-output'],1)]:
            p=subprocess.run([sys.executable,str(script),*argv],cwd=ROOT,capture_output=True,text=True,timeout=60)
            self.assertEqual(p.returncode,expected,p.stderr)
            if expected:self.assertIn('guest_attempts',p.stderr)

    def test_public_result_real_recomputation_positive_and_rehashed_negative(self):
        script=ROOT/'scripts/reference/resaved_prefix_relationships.py'
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'report.json';path.write_text(json.dumps(self.value))
            p=subprocess.run([sys.executable,str(script),'result',str(path)],cwd=ROOT,capture_output=True,text=True,timeout=60)
            self.assertEqual(p.returncode,0,p.stderr)
            value=copy.deepcopy(self.value);value['data']['summary']['mutation_permission']=True;value['data_sha256']=tool.digest(tool.encode(value['data']));path.write_text(json.dumps(value))
            p=subprocess.run([sys.executable,str(script),'result',str(path)],cwd=ROOT,capture_output=True,text=True,timeout=60)
            self.assertEqual(p.returncode,1);self.assertIn('SemanticMismatch',p.stderr)

    def test_output_alias_never_modifies_native_inode(self):
        script=ROOT/'scripts/reference/resaved_prefix_relationships.py'
        with tempfile.TemporaryDirectory() as external, tempfile.TemporaryDirectory(dir=tool.OUT) as owned:
            native=Path(external)/'native-input';native.write_bytes(self.raw)
            hard=Path(owned)/'report.json';os.link(native,hard)
            p=subprocess.run([sys.executable,str(script),'plan','--output',str(hard)],cwd=ROOT,capture_output=True,text=True,timeout=60)
            self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(native.read_bytes(),self.raw)
            self.assertNotEqual(hard.stat().st_ino,native.stat().st_ino)
            link=Path(owned)/'symlink.json';link.symlink_to(native)
            p=subprocess.run([sys.executable,str(script),'plan','--output',str(link)],cwd=ROOT,capture_output=True,text=True,timeout=60)
            self.assertEqual(p.returncode,1);self.assertIn('OutputScope',p.stderr);self.assertEqual(native.read_bytes(),self.raw)

    def test_bad_json_and_report_size_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'report';p.write_text('{')
            with self.assertRaises(tool.Refusal) as e:tool.result(p)
            self.assertEqual(e.exception.code,'MalformedReport')
            p.write_bytes(b' '* (32*1024*1024+1))
            with self.assertRaises(tool.Refusal) as e:tool.result(p)
            self.assertEqual(e.exception.code,'ReportLimit')

class Recording(unittest.TextTestResult):
    def startTest(self,test):self.started=time.monotonic();super().startTest(test)
    def stopTest(self,test):
        case=ET.SubElement(self.suite,'testcase',name=test.id(),time=f'{time.monotonic()-self.started:.6f}')
        for t,msg in self.failures+self.errors:
            if t is test:ET.SubElement(case,'failure').text=msg
        super().stopTest(test)

if __name__=='__main__':
    runner=unittest.TextTestRunner(resultclass=Recording,verbosity=2)
    Recording.suite=ET.Element('testsuite',name='WP45 offline relationship audit')
    result=runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(Relationships))
    Recording.suite.set('tests',str(result.testsRun));Recording.suite.set('failures',str(len(result.failures)));Recording.suite.set('errors',str(len(result.errors)));Recording.suite.set('skipped',str(len(result.skipped)))
    ET.ElementTree(Recording.suite).write(ROOT/'docs/research/continuation/resaved-prefix-relationships/evidence/tests.xml',encoding='unicode')
    sys.exit(not result.wasSuccessful())
