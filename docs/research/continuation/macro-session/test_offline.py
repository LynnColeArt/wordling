"""Offline public-entrypoint preparation checks. Never use --allow-vm."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

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


if __name__=='__main__':unittest.main()
