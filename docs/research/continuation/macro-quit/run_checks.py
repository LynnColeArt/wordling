#!/usr/bin/env python3
"""Run actual offline WP39 unittest cases and emit their genuine JUnit outcomes."""
import argparse
from pathlib import Path
import sys
import time
import unittest
import xml.etree.ElementTree as ET

OUT=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--junitxml',type=Path,required=True);args=parser.parse_args()
    suite_xml=ET.Element('testsuite',name='WP39-offline-and-original-evidence')
    class Result(unittest.TextTestResult):
        def startTest(self,test):
            super().startTest(test);self.started=time.monotonic()
            self.node=ET.SubElement(suite_xml,'testcase',name=test.id())
        def stopTest(self,test):
            self.node.set('time',f'{time.monotonic()-self.started:.6f}');super().stopTest(test)
        def addFailure(self,test,err):
            super().addFailure(test,err);ET.SubElement(self.node,'failure').text=self._exc_info_to_string(err,test)
        def addError(self,test,err):
            super().addError(test,err);ET.SubElement(self.node,'error').text=self._exc_info_to_string(err,test)
        def addSkip(self,test,reason):
            super().addSkip(test,reason);ET.SubElement(self.node,'skipped',message=reason)
    suite=unittest.defaultTestLoader.discover(str(OUT),pattern='test_*.py')
    result=unittest.TextTestRunner(verbosity=2,resultclass=Result).run(suite)
    suite_xml.set('tests',str(result.testsRun));suite_xml.set('failures',str(len(result.failures)))
    suite_xml.set('errors',str(len(result.errors)));suite_xml.set('skipped',str(len(result.skipped)))
    args.junitxml.parent.mkdir(parents=True,exist_ok=True)
    ET.indent(suite_xml);ET.ElementTree(suite_xml).write(args.junitxml,encoding='utf-8',xml_declaration=True)
    return 0 if result.wasSuccessful()else 1


if __name__=='__main__':sys.exit(main())
