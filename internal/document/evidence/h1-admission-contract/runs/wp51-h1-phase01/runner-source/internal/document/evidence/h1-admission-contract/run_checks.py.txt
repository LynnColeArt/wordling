#!/usr/bin/env python3
"""Run actual offline WP51 integrity tests, emit per-case JUnit; no guest."""
import sys
sys.dont_write_bytecode=True
import argparse,contextlib,io,time,unittest,xml.etree.ElementTree as ET
from pathlib import Path
HERE=Path(__file__).resolve().parent
class Result(unittest.TextTestResult):
 def __init__(self,*args,**kw):super().__init__(*args,**kw);self.cases=[]
 def startTest(self,test):super().startTest(test);self.start=time.monotonic();self.row=ET.Element('testcase',name=test.id(),classname='wp51.offline-integrity')
 def stopTest(self,test):self.row.set('time',str(time.monotonic()-self.start));self.cases.append(self.row);super().stopTest(test)
 def addFailure(self,test,error):super().addFailure(test,error);ET.SubElement(self.row,'failure').text=self._exc_info_to_string(error,test)
 def addError(self,test,error):super().addError(test,error);ET.SubElement(self.row,'error').text=self._exc_info_to_string(error,test)
 def addSkip(self,test,reason):super().addSkip(test,reason);ET.SubElement(self.row,'skipped',message=reason)
def main():
 p=argparse.ArgumentParser();p.add_argument('--junitxml',type=Path,required=True);args=p.parse_args();suite=unittest.defaultTestLoader.discover(str(HERE),pattern='test_*.py');r=unittest.TextTestRunner(verbosity=2,resultclass=Result).run(suite);root=ET.Element('testsuite',name='wp51-offline-integrity',tests=str(r.testsRun),failures=str(len(r.failures)),errors=str(len(r.errors)),skipped=str(len(r.skipped)));root.extend(r.cases);ET.indent(root);args.junitxml.parent.mkdir(parents=True,exist_ok=True);ET.ElementTree(root).write(args.junitxml,encoding='utf-8',xml_declaration=True);return 0 if r.wasSuccessful()else 1
if __name__=='__main__':raise SystemExit(main())
