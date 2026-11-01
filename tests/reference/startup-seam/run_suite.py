"""Bounded authored acceptance suite runner with honest JUnit outcomes."""
import argparse
import pathlib
import sys
import time
import unittest
import xml.etree.ElementTree as ET

parser=argparse.ArgumentParser()
parser.add_argument('--junit',required=True,type=pathlib.Path)
args=parser.parse_args()
suite=unittest.defaultTestLoader.discover(str(pathlib.Path(__file__).parent),pattern='test_transport.py')
class Result(unittest.TextTestResult):
    def startTest(self,test):
        self.started=time.monotonic()
        super().startTest(test)
    def stopTest(self,test):
        self.times[test.id()]=time.monotonic()-self.started
        super().stopTest(test)
    def __init__(self,*a,**kw):
        super().__init__(*a,**kw)
        self.times={}
result=unittest.TextTestRunner(verbosity=2,resultclass=Result).run(suite)
root=ET.Element('testsuite',name='startup-transport',tests=str(result.testsRun),failures=str(len(result.failures)),errors=str(len(result.errors)),skipped=str(len(result.skipped)))
failures={test.id():trace for test,trace in result.failures+result.errors}
for name,elapsed in sorted(result.times.items()):
    case=ET.SubElement(root,'testcase',name=name,time=f'{elapsed:.6f}')
    if name in failures:
        ET.SubElement(case,'failure').text=failures[name]
ET.indent(root)
args.junit.write_bytes(ET.tostring(root,encoding='utf-8',xml_declaration=True))
sys.exit(0 if result.wasSuccessful() else 1)
