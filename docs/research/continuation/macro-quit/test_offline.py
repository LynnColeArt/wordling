"""WP39 offline public CLI/comparator controls; never launch a guest."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[4]
CLI=ROOT/'scripts/reference/macro_quit.py'
OUT=ROOT/'docs/research/continuation/macro-quit'
sys.path.insert(0,str(ROOT/'scripts/reference'))
spec=importlib.util.spec_from_file_location('wp39_comparator',CLI)
probe=importlib.util.module_from_spec(spec);spec.loader.exec_module(probe)


class Offline(unittest.TestCase):
    def call(self,*args):
        return subprocess.run([sys.executable,str(CLI),*args],capture_output=True,text=True)

    def test_public_check_binds_approved_sources_without_guest(self):
        result=self.call('check');self.assertEqual(result.returncode,0,result.stdout)
        value=json.loads(result.stdout)
        self.assertFalse(value['vm_launched']);self.assertFalse(value['wordling_tested'])
        self.assertFalse(value['full_m1_accepted']);self.assertEqual(len(value['provenance']['historical_sites']),5)
        self.assertEqual(value['provenance']['approved_wp38'],probe.WP38)
        self.assertEqual(len(value['sources']),21)
        self.assertEqual(value['provenance']['private_manuals'][0]['publication'],'metadata only')

    def test_public_plan_is_four_unexecuted_guest_recipes(self):
        p=self.call('plan');self.assertEqual(p.returncode,0,p.stdout)
        value=json.loads(p.stdout);self.assertFalse(value['vm_launched'])
        self.assertEqual([r['repetitions']for r in value['cases']],[2,2])
        self.assertEqual([r['status']for r in value['cases']],['unexecuted-template']*2)
        self.assertEqual([len(r['assets'])for r in value['cases']],[1,2])
        self.assertEqual(value['cases'][1]['alternate_child_return'],probe.DOC1+'P39C39PARENTBACK')

    def test_vm_requires_flag_and_real_release_note_before_output(self):
        for flags in [[],['--allow-vm'],['--authorization-note','not authorization']]:
            name='offline-unauthorized';self.assertFalse((OUT/'runs'/name).exists())
            p=self.call('run',name,'--case','root',*flags)
            self.assertEqual(p.returncode,1);self.assertEqual(json.loads(p.stdout)['code'],'AuthorizationRequired')
            self.assertFalse((OUT/'runs'/name).exists())

    def test_unknown_case_and_missing_result_are_public_failures(self):
        self.assertNotEqual(self.call('run','unused','--case','other').returncode,0)
        p=self.call('result','/tmp/absent-wp39-case.json');self.assertEqual(p.returncode,1)
        self.assertEqual(json.loads(p.stdout)['code'],'FileNotFoundError')

    def test_original_source_sites_and_native_prefix_are_exact(self):
        prefix=(ROOT/probe.session.TEMPLATE).read_bytes()
        offset,_=probe.session.SDKNativeWords.inspect(prefix)
        for case in ['root','nested']:
            for name,raw in probe.fixtures(case).items():
                body,words=probe.session.SDKNativeWords.inspect(raw)
                self.assertEqual(raw[:body],prefix[:offset])
                self.assertIn(0xFC20,words);self.assertEqual(words[-1],0)
                self.assertEqual(words.count(0xFC20),1)
                self.assertEqual(words[0],0xFC0C)
                self.assertNotIn(0xFC0D,words)
                self.assertEqual(words.count(0xFC22),1 if name=='Q39C.WPM'else 0)
                # No handler block contains QUIT; normal-flow instruction only.
                self.assertLess(words.index(0xFC20),words.index(0xFC16))

    def test_synthetic_comparator_controls_do_not_assume_stop_all(self):
        d1,d2=probe.DOC1,probe.DOC2
        self.assertEqual(probe.observed_branch('root',d1+'R39',d1+'R39READY',d2),'stop-all-hypothesis-corroborated')
        self.assertEqual(probe.observed_branch('nested',d1+'P39C39PARENTBACK',d1+'P39C39PARENTBACKREADY',d2),'child-return-observed-not-stop-all')
        self.assertEqual(probe.observed_branch('root',d1+'R39ROOTERR',d1+'R39ROOTERRREADY',d2),'unqualified-observed-discriminator-branch')
        for before,after,other in [('wrong','wrongREADY',d2),(d1+'R39',d1+'R39',d2),(d1+'R39',d1+'R39READY','changed')]:
            with self.assertRaises(probe.ProbeFailure):probe.observed_branch('root',before,after,other)

    def test_unobservable_wrapped_or_modal_screen_cannot_prove_completion(self):
        for screen in ['', 'Macro: C:\\OUT\\Q39R', 'body\nsecond document row\nDoc 1', 'X'*64+'\nDoc 1']:
            with self.assertRaises(probe.ProbeFailure):probe.screen_body(screen)

    def test_source_pin_mutation_fails_public_offline_check(self):
        with tempfile.TemporaryDirectory()as d:
            source=CLI.read_text().replace('ROOT = Path(__file__).resolve().parents[2]','ROOT = Path('+repr(str(ROOT))+')')
            source=source.replace(probe.SESSION_SHA,'0'*64)
            mutant=Path(d)/'probe.py';mutant.write_text(source)
            env={**os.environ,'PYTHONPATH':str(ROOT/'scripts/reference')}
            p=subprocess.run([sys.executable,str(mutant),'check'],capture_output=True,text=True,env=env)
            self.assertEqual(p.returncode,1);self.assertEqual(json.loads(p.stdout)['code'],'HelperDrift')


if __name__=='__main__':unittest.main()
