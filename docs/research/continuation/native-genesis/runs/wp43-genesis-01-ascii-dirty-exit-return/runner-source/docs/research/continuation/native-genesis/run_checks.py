#!/usr/bin/env python3
"""Actual WP43 unittest/JUnit; no guest authorization."""
import argparse
from pathlib import Path
import time
import unittest
import xml.etree.ElementTree as ET
p=argparse.ArgumentParser();p.add_argument('--junitxml',type=Path,required=True)
a=p.parse_args();root=ET.Element('testsuite',name='WP43-offline')
class Result(unittest.TextTestResult):
    def startTest(self,test):
        super().startTest(test);self.start=time.monotonic();self.node=ET.SubElement(root,'testcase',name=test.id())
    def stopTest(self,test):self.node.set('time',str(time.monotonic()-self.start));super().stopTest(test)
    def addFailure(self,test,err):super().addFailure(test,err);ET.SubElement(self.node,'failure').text=self._exc_info_to_string(err,test)
    def addError(self,test,err):super().addError(test,err);ET.SubElement(self.node,'error').text=self._exc_info_to_string(err,test)
    def addSkip(self,test,reason):super().addSkip(test,reason);ET.SubElement(self.node,'skipped',message=reason)
suite=unittest.defaultTestLoader.discover(str(Path(__file__).parent),pattern='test_*.py')
r=unittest.TextTestRunner(verbosity=2,resultclass=Result).run(suite)
for k,v in [('tests',r.testsRun),('failures',len(r.failures)),('errors',len(r.errors)),('skipped',len(r.skipped))]:root.set(k,str(v))
a.junitxml.parent.mkdir(parents=True,exist_ok=True);ET.indent(root);ET.ElementTree(root).write(a.junitxml,encoding='utf-8',xml_declaration=True)
raise SystemExit(0 if r.wasSuccessful()else 1)
