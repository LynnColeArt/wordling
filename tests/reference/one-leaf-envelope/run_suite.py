"""Actual bounded public suite runner; per-test timings and truthful JUnit."""
import argparse
from pathlib import Path
import sys
import time
import unittest
import xml.etree.ElementTree as ET

parser=argparse.ArgumentParser()
parser.add_argument('--suite',choices=('envelope','family','legacy'),required=True)
parser.add_argument('--junit',type=Path,required=True)
args=parser.parse_args();root=Path(__file__).resolve().parents[3]
folder=root/'tests/reference'/dict(envelope='one-leaf-envelope',family='startup-prerequisite',legacy='startup-seam')[args.suite]
pattern='test_*.py' if args.suite!='legacy' else 'test_transport.py'
suite=unittest.defaultTestLoader.discover(str(folder),pattern=pattern)
class Results(unittest.TextTestResult):
    def __init__(self,*a,**k):super().__init__(*a,**k);self.times={}
    def startTest(self,test):self.start=time.monotonic();super().startTest(test)
    def stopTest(self,test):self.times[test.id()]=time.monotonic()-self.start;super().stopTest(test)
result=unittest.TextTestRunner(verbosity=2,resultclass=Results).run(suite)
xml=ET.Element('testsuite',name='one-leaf-'+args.suite,tests=str(result.testsRun),
    failures=str(len(result.failures)),errors=str(len(result.errors)),skipped=str(len(result.skipped)))
failures={t.id():trace for t,trace in result.failures+result.errors}
for name,elapsed in result.times.items():
    case=ET.SubElement(xml,'testcase',name=name,time=f'{elapsed:.6f}')
    if name in failures:ET.SubElement(case,'failure').text=failures[name]
ET.indent(xml);args.junit.parent.mkdir(parents=True,exist_ok=True)
args.junit.write_bytes(ET.tostring(xml,encoding='utf-8',xml_declaration=True))
sys.exit(0 if result.wasSuccessful() else 1)
