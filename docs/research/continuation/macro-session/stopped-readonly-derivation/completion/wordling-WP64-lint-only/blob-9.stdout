"""Bounded real public suites and per-case JUnit; no metadata assertion cases."""
import argparse
from pathlib import Path
import sys
import time
import unittest
import xml.etree.ElementTree as ET
p=argparse.ArgumentParser();p.add_argument('--suite',choices=('derivation','envelope','family','legacy'),required=True);p.add_argument('--junit',type=Path,required=True);p.add_argument('--pattern');p.add_argument('--expect',type=int);a=p.parse_args()
root=Path(__file__).resolve().parents[3];directory=dict(derivation='stopped-readonly-derivation',envelope='one-leaf-envelope',family='startup-prerequisite',legacy='startup-seam')[a.suite]
suite=unittest.defaultTestLoader.discover(str(root/'tests/reference'/directory),pattern=a.pattern or ('test_transport.py' if a.suite=='legacy' else 'test_*.py'))
if a.expect is not None:assert suite.countTestCases()==a.expect,(suite.countTestCases(),a.expect)
class Result(unittest.TextTestResult):
 def __init__(self,*x,**k):super().__init__(*x,**k);self.times={}
 def startTest(self,test):self.start=time.monotonic();super().startTest(test)
 def stopTest(self,test):self.times[test.id()]=time.monotonic()-self.start;super().stopTest(test)
r=unittest.TextTestRunner(verbosity=2,resultclass=Result).run(suite)
xml=ET.Element('testsuite',name='WP64-'+a.suite,tests=str(r.testsRun),failures=str(len(r.failures)),errors=str(len(r.errors)),skipped=str(len(r.skipped)))
failed={t.id():trace for t,trace in r.failures+r.errors}
for name,seconds in r.times.items():
 c=ET.SubElement(xml,'testcase',name=name,time=f'{seconds:.6f}')
 if name in failed:ET.SubElement(c,'failure').text=failed[name]
ET.indent(xml);a.junit.parent.mkdir(parents=True,exist_ok=True);a.junit.write_bytes(ET.tostring(xml,encoding='utf-8',xml_declaration=True))
sys.exit(0 if r.wasSuccessful() else 1)
