"""External CLI and read-only semantic adversarial tests. No guest calls."""
import copy
import importlib.util
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[5]
SCRIPT=ROOT/'scripts/reference/resaved_prefix.py'
sys.path.insert(0,str(SCRIPT.parent))
spec=importlib.util.spec_from_file_location('wp42',SCRIPT)
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
SOURCE=ROOT/'docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5'

class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=r.audit(SOURCE)
    def test_actual_reader_and_relocated_deleted_originals_stay_read_only(self):
        kinds=set()
        for p in r.corpus():
            report=r.audit(p)
            self.assertTrue(report['actual_go_reader']['accepted'])
            self.assertTrue(report['actual_go_reader']['exact_export'])
            self.assertFalse(report['mutation_permission'])
            self.assertFalse(report['wordling_tested'])
            if 'prefix_regions' in report:
                self.assertEqual(sum(x['length'] for x in report['prefix_regions']),report['body_offset'])
                kinds.add(report['body_offset'])
        self.assertIn(324,kinds);self.assertIn(564,kinds)
    def test_rehashed_field_owner_link_deleted_and_slack_claims_rejected(self):
        mutations=[lambda x:x.update(mutation_permission=True),
                   lambda x:x.update(body_offset=564),
                   lambda x:x['packets'][0].update(type=65535),
                   lambda x:x['blocks'][0].update(next=0),
                   lambda x:x['prefix_regions'][0].update(owners=['slack-free-to-edit']),
                   lambda x:x['inherited_field_observations'][0].update(name='safe-body-length'),
                   lambda x:x['candidate_relationships'][0].update(target=999),
                   lambda x:x['candidate_relationships'][1].update(body_reference=True)]
        for change in mutations:
            report=copy.deepcopy(self.report);change(report)
            # A fresh digest is deliberately not semantic evidence.
            self.assertNotEqual(r.plan_hash(report),r.plan_hash(self.report))
            with self.assertRaises(r.Refusal):r.assert_report(SOURCE,report)
    def test_malformed_native_bounds_cycle_and_resource_references(self):
        raw=SOURCE.read_bytes()
        with tempfile.TemporaryDirectory() as td:
            cases=[b'',raw[:15],b'X'+raw[1:],raw[:4]+b'\xff'*4+raw[8:],raw[:-1],raw[:20]]
            for i,data in enumerate(cases):
                p=Path(td)/str(i);p.write_bytes(data);report=r.audit(p)
                self.assertFalse(report['mutation_permission'])
            p=Path(td)/'large';p.write_bytes(b'x'*(r.LIMIT+1))
            with self.assertRaises(r.Refusal):r.audit(p)
    def test_wrong_rehashed_reference_not_accepted_as_relationship_permission(self):
        raw=bytearray(SOURCE.read_bytes())
        packet=next(p for p in self.report['packets'] if p['type']==15)
        raw[packet['offset']+18:packet['offset']+20]=b'\xff\xff'
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'bad-pool';p.write_bytes(raw);report=r.audit(p)
            self.assertTrue(report['actual_go_reader']['accepted'])
            self.assertFalse(report['candidate_relationships'][0]['bounds_valid'])
            self.assertFalse(report['mutation_permission'])
    def test_public_cli_unknown_and_missing_grant_refuse_without_side_effects(self):
        for argv in [['run','--run-id','no-grant','--case','ascii-baseline'],
                     ['run','--run-id','no-grant','--case','ascii-baseline','--allow-vm'],
                     ['run','--case','unknown'],['plan','--bogus'],['result','/missing/wp42.json']]:
            proc=subprocess.run([sys.executable,str(SCRIPT),*argv],cwd=ROOT,capture_output=True,timeout=30)
            self.assertNotEqual(proc.returncode,0,argv)
        self.assertFalse((r.OUT/'runs/no-grant').exists())
    def test_frozen_plan_source_profile_case_and_argv_binding(self):
        plan=r.plan();self.assertEqual(len(plan['cases']),6)
        self.assertEqual(sum(len(x['fresh_repetitions']) for x in plan['cases']),12)
        self.assertIn('native_edits.py',' '.join(x['path'] for x in plan['sources']))
        self.assertIn('macro_quit.py',' '.join(x['path'] for x in plan['sources']))
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'grant.json'
            grant={'schema':'wordling.wp42.grant/v1','plan_sha256':r.plan_hash(plan),'run_id':'r',
                   'case':'ascii-baseline','repetitions':[1,2],'authorization_note':'test-only; no run'}
            args=type('Args',(),{'allow_vm':True,'grant':p,'run_id':'r','case':'ascii-baseline'})()
            p.write_text(json.dumps(grant));self.assertEqual(r.validate_grant(args,plan),grant)
            for key,value in [('plan_sha256','0'*64),('case','one-bold-baseline'),('run_id','wrong'),
                              ('repetitions',[1]),('authorization_note','')]:
                bad={**grant,key:value};p.write_text(json.dumps(bad))
                with self.assertRaises(r.Refusal):r.validate_grant(args,plan)
    def test_public_check_and_plan_are_real_offline_interfaces(self):
        for command in ['plan','check']:
            proc=subprocess.run([sys.executable,str(SCRIPT),command],cwd=ROOT,capture_output=True,timeout=120)
            self.assertEqual(proc.returncode,0,proc.stderr.decode())
            value=json.loads(proc.stdout)
            self.assertFalse(value.get('mutation_permission',False))
            if command=='check':self.assertFalse(value['vm_launched']);self.assertEqual(value['guest_attempts'],0)
    def test_rehashed_hidden_save_or_view_interleaving_is_rejected(self):
        recipe=r.recipes()[0]
        phases=[]
        for name,wanted in r.expected_phases(recipe):
            if wanted is None:
                wanted=[['key',x] for x in ['f3','spc','shift-f7','s','f7','shift-f8','3','3','f7','shift-f8','2','f7','shift-f8','1','f7']]
            phases.append({'name':name,'commands':wanted})
        trace=[{command:value} for phase in phases for command,value in phase['commands']]
        row={'phases':phases,'exit_actions':[],'trace':trace}
        r.verify_actions(recipe,row)
        for key in ['f10','alt-f3','alt-f2']:
            bad=copy.deepcopy(row);bad['phases'][2]['commands'].insert(0,['key',key]);bad['trace'].insert(0,{'key':key})
            with self.assertRaises(r.Refusal):r.verify_actions(recipe,bad)

    def test_bounded_mutation_fuzz_never_grants_writes(self):
        rng=random.Random(4201);raw=SOURCE.read_bytes()
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'mutant'
            for _ in range(100):
                mutant=bytearray(raw)
                for _ in range(rng.randint(1,4)):mutant[rng.randrange(len(mutant))]=rng.randrange(256)
                p.write_bytes(mutant)
                try:report=r.audit(p)
                except (ValueError,r.Refusal):continue
                self.assertFalse(report['mutation_permission'])

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
    names=[str(test) for test in suite]
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    target=Path(sys.argv[1]) if len(sys.argv)>1 else None
    if target:
        root=ET.Element('testsuite',name='wp42-offline',tests=str(result.testsRun),
                        failures=str(len(result.failures)),errors=str(len(result.errors)))
        failures={str(test):detail for test,detail in result.failures+result.errors}
        for name in names:
            case=ET.SubElement(root,'testcase',name=name)
            if name in failures:ET.SubElement(case,'failure').text=failures[name]
        target.parent.mkdir(parents=True,exist_ok=True)
        ET.ElementTree(root).write(target,encoding='utf-8',xml_declaration=True)
    sys.exit(not result.wasSuccessful())
