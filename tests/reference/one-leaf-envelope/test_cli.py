"""Closed CLI integration; real public API calls, actual exit/JSON/cleanup."""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
ROOT=Path(__file__).resolve().parents[3]
FACADE=Path(os.environ.get('STARTUP_FAMILY_UNDER_TEST',ROOT/'scripts/reference/startup_transport.py'))

class CLITests(unittest.TestCase):
    def run_case(self,case,positive=False):
        argv=[sys.executable,'-B',str(FACADE),'envelope-fixture',case]
        p=subprocess.run(argv,cwd=ROOT,capture_output=True,timeout=20)
        self.assertEqual(p.stderr,b'',p.stderr.decode(errors='replace'))
        value=json.loads(p.stdout);self.assertEqual(value['original_guests'],0)
        self.assertEqual(p.returncode,0 if positive else 1,value)
        self.assertEqual(value['ok'],positive,value)
        if positive:
            self.assertTrue(value['same_worker']);self.assertEqual(value['outcome']['charged_operations'],2)
            self.assertEqual(value['history'][-1]['original_state'],'STOPPED')
        if case=='response-loss':
            self.assertTrue(value['fixture_child_observed_stopped'],value)
            self.assertEqual(value['outcome']['cleanup'],'UNKNOWN')
        output=os.environ.get('ENVELOPE_CLI_RESULTS')
        if output:
            folder=Path(output);folder.mkdir(parents=True,exist_ok=True)
            (folder/(case+'.stdout')).write_bytes(p.stdout);(folder/(case+'.stderr')).write_bytes(p.stderr)
        return value

def make(case,positive):
    def check(self):self.run_case(case,positive)
    return check
for case in ('positive','expired','absolute-progress','source-io','prepared','commands','output','fd',
             'process','rss','wire','observation','response-loss','external-peer'):
    setattr(CLITests,'test_'+case.replace('-','_'),make(case,case in ('positive','external-peer')))

if __name__=='__main__':unittest.main()
