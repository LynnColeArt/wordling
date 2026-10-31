"""External CLI and read-only semantic adversarial tests. No guest calls."""
import copy
from contextlib import contextmanager
from types import SimpleNamespace
from unittest import mock
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

    def run_fault_case(self, failure):
        # Synthetic owned port fakes: no real session lock, process or reference
        # disk is touched. The actual runner/ledger/report/extractor are exercised.
        with tempfile.TemporaryDirectory() as td:
            base=Path(td);private=base/'private';master=private/'master';master.mkdir(parents=True)
            for name in ['boot.img','harddisk.img']:(master/name).write_bytes(b'synthetic immutable master')
            runtime=private/'runtime';runtime.mkdir();socket=runtime/'qmp.sock'
            previous_attempts=[{'plan_sha256':'older-plan','attempt':i} for i in range(10)]
            (private/'wp42-attempts.json').write_text(json.dumps(previous_attempts))
            events=[];held=[False];starts=[];stops=[]
            @contextmanager
            def guard(path):
                held[0]=True;events.append('guard-enter')
                try:yield
                finally:events.append('guard-exit');held[0]=False
            class FakeQMP:
                def __enter__(self):return self
                def __exit__(self,*args):pass
                def capture(self,path):
                    path.mkdir();(path/'synthetic.txt').write_text('test-only failed state')
            qmp=SimpleNamespace(RUNTIME=runtime,SOCKET=socket,QMP=FakeQMP)
            guest=SimpleNamespace(MASTER=master)
            plan=r.plan();case=plan['cases'][0]
            plan['master']={name:r.sha(master/name) for name in ['boot.img','harddisk.img']}
            def start(q,g,work,assets):
                self.assertTrue(held[0]);starts.append(work);work.mkdir(parents=True)
                (work/'harddisk.img').write_bytes(b'synthetic scratch, not FAT or native')
                (work/'settings-before.SET').write_bytes(b'synthetic private settings')
                if failure=='pre-start':raise RuntimeError('injected pre-start failure')
                (runtime/'qemu.pid').write_text('999999999');socket.write_text('synthetic owned socket')
                return case['qemu_argv'][0]
            def stop(q,g):
                self.assertTrue(held[0]);stops.append(True)
                if failure=='stop':raise RuntimeError('injected stop failure')
                socket.unlink(missing_ok=True)
                return 'QMP quit; own socket terminated'
            def settings(work,label):
                self.assertTrue(held[0]);events.append('extract-settings')
                return {'private_path':'synthetic','sha256':'synthetic'}
            session=SimpleNamespace(configure=lambda *args:(qmp,guest,private),exclusive=guard,
                                    timeout_signal=lambda *args:None,fresh_start=start,stop_owned=stop,
                                    settings_snapshot=settings)
            probe=SimpleNamespace(exports=[('W42S0','W42S0.WP5')],trace=[],checks=[],settings=[],phases=[])
            module=SimpleNamespace(MutationProbe=lambda *args:probe)
            quit_module=SimpleNamespace(finish_original=lambda p:[])
            original_import=r.importlib.import_module
            def imports(name):
                return {'macro_session':session,'macro_quit':quit_module}.get(name) or original_import(name)
            original_dump=r.dump
            def record_dump(path,value):
                if Path(path).name=='run.json':events.append('report-held-'+str(held[0]))
                original_dump(path,value)
            def extract(argv,**kwargs):
                self.assertTrue(held[0]);self.assertEqual(argv[0],'mcopy');events.append('extract-native')
                Path(argv[-1]).write_bytes(b'synthetic extraction, never original evidence')
                return subprocess.CompletedProcess(argv,0,stdout=b'',stderr=b'')
            args=SimpleNamespace(allow_vm=True,run_id=case['run_id'],case=case['id'],grant=None)
            grant={'test_only':True}
            with mock.patch.object(r,'OUT',base/'out'),mock.patch.object(r,'plan',return_value=plan), \
                 mock.patch.object(r,'validate_grant',return_value=grant),mock.patch.object(r,'inspector',return_value=module), \
                 mock.patch.object(r.importlib,'import_module',side_effect=imports), \
                 mock.patch.object(r,'perform',side_effect=r.Refusal('UnknownProtocol','injected first attempt protocol failure')), \
                 mock.patch.object(r,'dump',side_effect=record_dump),mock.patch.object(r.subprocess,'run',side_effect=extract):
                result=r.run(args)
                report=json.loads(Path(result['run_manifest']).read_text())
                ledger=json.loads((private/'wp42-attempts.json').read_text())
                self.assertEqual(len(starts),1);self.assertEqual(len(stops),1)
                self.assertEqual(len(ledger),11);self.assertEqual(ledger[:10],previous_attempts)
                self.assertEqual(len(report['results']),1)
                self.assertEqual(result['status'],'batch-halted');self.assertTrue(result['guard_released'])
                with self.assertRaises(r.Refusal) as refused:r.result(Path(result['run_manifest']))
                self.assertEqual(refused.exception.code,'IncompleteBatch')
                self.assertTrue(report['master_unchanged']);self.assertEqual(report['master_before'],report['master_after'])
                self.assertTrue(report['halted_before_next_attempt']);self.assertFalse(report['mutation_permission'])
                self.assertIn('report-held-True',events);self.assertEqual(events[-2:],['guard-exit','report-held-False'])
                row=report['results'][0]
                if failure=='protocol':
                    self.assertEqual(row['error_code'],'UnknownProtocol');self.assertTrue(row['guest_stopped'])
                    self.assertIn('extract-native',events);self.assertEqual(row['exports'][0]['exit'],0)
                    self.assertTrue(result['oracle_released'])
                else:
                    self.assertFalse(row['guest_stopped']);self.assertFalse(result['oracle_released'])
                    self.assertNotIn('extract-native',events);self.assertIn('extraction_skipped',row)
                with mock.patch.object(r,'OUT',base/'corrected-plan-output'):
                    budget_result=r.run(args)
                self.assertEqual(budget_result['status'],'batch-halted')
                self.assertEqual(len(starts),1)
                self.assertEqual(len(json.loads((private/'wp42-attempts.json').read_text())),11)
                return report

    def test_first_protocol_failure_stops_batch_after_guarded_extraction(self):
        self.run_fault_case('protocol')

    def test_pre_start_failure_cannot_claim_stopped_or_launch_second(self):
        report=self.run_fault_case('pre-start')
        self.assertEqual(report['results'][0]['outcome'],'stop-unproven')

    def test_stop_failure_skips_disk_extraction_and_cannot_claim_oracle_safe(self):
        report=self.run_fault_case('stop')
        self.assertEqual(report['results'][0]['outcome'],'stop-failed')
        self.assertIn('injected stop failure',report['results'][0]['stop_error'])

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
