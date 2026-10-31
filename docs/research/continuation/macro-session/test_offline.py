"""Offline public-entrypoint preparation checks. Never use --allow-vm."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import runpy
import random
import struct

ROOT=Path(__file__).resolve().parents[4]
CLI=ROOT/'scripts/reference/macro_session.py'
OUT=ROOT/'docs/research/continuation/macro-session'


class OfflinePreparation(unittest.TestCase):
    def call(self,*args):
        return subprocess.run([sys.executable,str(CLI),*args],text=True,capture_output=True)

    def test_check_is_offline_and_bound(self):
        paths=[ROOT/'scripts/reference'/n for n in ['qmp.py','guest.py','smoke.py','extended.py','advanced.py','history_loops.py']]
        before={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}
        result=self.call('check');self.assertEqual(result.returncode,0,result.stdout)
        value=json.loads(result.stdout)
        self.assertFalse(value['vm_launched']);self.assertEqual(value['original_runs_executed'],0)
        self.assertEqual(len(value['pinned_sources']),17)
        self.assertEqual(before,{str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths})

    def test_plan_has_two_fresh_repetitions_and_honest_scope(self):
        result=self.call('plan');self.assertEqual(result.returncode,0)
        rows=json.loads(result.stdout)['recipes'];self.assertEqual(len(rows),9)
        self.assertTrue(all(r['repetitions']==2 and r['status']=='not-run' and r['wordling_tested']is False for r in rows))
        self.assertEqual({r['id']for r in rows if r['id'].startswith('stop-')},{'stop-default','stop-on','stop-off'})

    def test_vm_requires_both_release_flag_and_note_before_writes(self):
        for args in [[],['--authorization-note','not a release'],['--allow-vm']]:
            path=OUT/'runs/unauthorized-offline-test';self.assertFalse(path.exists())
            result=self.call('run','unauthorized-offline-test','--case','stop-default',*args)
            self.assertNotEqual(result.returncode,0);self.assertIn('No VM launch',result.stdout)
            self.assertFalse(path.exists())

    def test_missing_result_is_failure(self):
        result=self.call('result','/tmp/no-such-wordling-original-run.json')
        self.assertNotEqual(result.returncode,0)

    def test_artifact_scope_and_hash_corruption_rejected(self):
        with tempfile.TemporaryDirectory()as temp:
            d=Path(temp);p=d/'run.json';raw=d/'raw.txt';raw.write_bytes(b'synthetic offline custody test')
            base={'scope':'original-reference-only','wordling_tested':False,'results':[],
                  'artifacts':[{'path':'raw.txt','size':raw.stat().st_size,'sha256':hashlib.sha256(raw.read_bytes()).hexdigest()}]}
            p.write_text(json.dumps(base));self.assertEqual(self.call('result',str(p)).returncode,0)
            raw.write_bytes(b'corrupted');self.assertNotEqual(self.call('result',str(p)).returncode,0)
            base['wordling_tested']=True;p.write_text(json.dumps(base))
            self.assertNotEqual(self.call('result',str(p)).returncode,0)

    def test_documentary_fixture_word_mutation_fails_offline_source_guard(self):
        with tempfile.TemporaryDirectory()as temp:
            code=CLI.read_text().replace('ROOT = Path(__file__).resolve().parents[2]', 'ROOT = Path('+repr(str(ROOT))+')')
            code=code.replace("TEMPLATE_SHA = 'e0e71258e6dc4c678b27773831105f0e7fca0b0803d451fb58b80ac02bc20b4e'", "TEMPLATE_SHA = '"+'0'*64+"'")
            p=Path(temp)/'invalid_source.py';p.write_text(code)
            result=subprocess.run([sys.executable,str(p),'check'],text=True,capture_output=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('template hash mismatch',result.stdout)

    def test_body_heartbeat_ignores_status_punctuation(self):
        function=runpy.run_path(str(CLI))['heartbeat_count']
        case=OUT/'runs/wp38-stop-default-01/stop-default-1'
        before=(case/'after-user-f1/screen.txt').read_text()
        after=(case/'manual-recovery-after-user-f1/screen.txt').read_text()
        self.assertNotEqual(before.count('.'),after.count('.'))
        self.assertEqual(function(before),2)
        self.assertEqual(function(after),2)
        off=OUT/'runs/wp38-stop-off-01/stop-off-1'
        self.assertGreater(function((off/'manual-recovery-after-user-f1/screen.txt').read_text()),
                           function((off/'after-user-f1/screen.txt').read_text()))

    def test_post_run_helper_exposure_preserves_executed_inputs(self):
        module=runpy.run_path(str(CLI))
        emit=module['SDKNativeWords'].emit
        self.assertEqual(module['SDKNativeWords'].inspect(emit([0xFC20]))[1],[0xFC20,0])
        with self.assertRaises(ValueError):emit([0xFCFF])
        with self.assertRaises(ValueError):module['configure'](ROOT,'../unsafe')
        for p in (OUT/'runs').glob('*/run.json'):
            report=json.loads(p.read_text())
            for sample in report['results']:
                fixture,_=module['fixture_for'](sample['case'])
                if fixture is not None:
                    archived=p.parent/'input'/'M38.WPM'
                    if archived.exists():self.assertEqual(fixture,archived.read_bytes())
                    else:
                        candidates=list(p.parent.glob('**/input-M38.WPM'))
                        self.assertTrue(candidates,'Missing archived fixture')
                        self.assertTrue(all(fixture==x.read_bytes()for x in candidates))

    def test_audit_rejects_wrapped_and_missing_heartbeat(self):
        module=runpy.run_path(str(OUT/'audit_results.py'))
        with self.assertRaises(AssertionError):module['beats']('unrelated\n'+('\n'*22)+'status')
        with self.assertRaises(AssertionError):module['beats']('D1SENT DIRTY1MSLIVE...\nwrapped\n'+('\n'*21)+'status')
        with self.assertRaises(AssertionError):module['beats']('D1SENT DIRTY1MSLIVE'+'.'*17+'\n'+('\n'*22)+'status')

    def test_inspector_malformed_and_seeded_binary_corpus(self):
        inspect=runpy.run_path(str(CLI))['SDKNativeWords'].inspect
        rng=random.Random(380114)
        for _ in range(2000):
            n=rng.randrange(256)
            data=bytes(rng.randrange(256)for _ in range(n))
            with self.assertRaises(ValueError):inspect(data)
        template=(ROOT/'docs/research/reference-runs/2026-10-29-extended-04/CMD51-131/TESTMAC.WPM').read_bytes()
        for offset in [0,55,len(template)+2,0xffffffff]:
            mutant=bytearray(template);struct.pack_into('<I',mutant,4,offset)
            with self.assertRaises(ValueError):inspect(mutant)
        for mutant in [template[:-1],template+b'\0\0',template[:-2]+b'AA']:
            with self.assertRaises(ValueError):inspect(mutant)


if __name__=='__main__':unittest.main()
