"""Run the real semantic suite and retain its JUnit outcomes, no fabricated cases."""
from pathlib import Path
import importlib.util,os,time,unittest,xml.etree.ElementTree as ET
O=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('contract_tests',O/'test_contract.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class Result(unittest.TextTestResult):
 def startTest(self,test):super().startTest(test);self.started=time.monotonic()
 def stopTest(self,test):self.case.set('time',str(time.monotonic()-self.started));super().stopTest(test)
 def addSuccess(self,test):super().addSuccess(test);self.case=ET.SubElement(self.suite,'testcase',name=test.id())
 def addFailure(self,test,err):super().addFailure(test,err);self.case=ET.SubElement(self.suite,'testcase',name=test.id());ET.SubElement(self.case,'failure').text=self._exc_info_to_string(err,test)
 def addError(self,test,err):super().addError(test,err);self.case=ET.SubElement(self.suite,'testcase',name=test.id());ET.SubElement(self.case,'error').text=self._exc_info_to_string(err,test)
 def __init__(self,*a,**kw):super().__init__(*a,**kw);self.suite=ET.Element('testsuite',name='secondary-checker-semantic')
os.environ['WP53_TEST_RECEIPT']=str(O/'evidence/negative-cases-final.json')
r=unittest.TextTestRunner(verbosity=2,resultclass=Result).run(unittest.defaultTestLoader.loadTestsFromModule(module));r.suite.set('tests',str(r.testsRun));r.suite.set('failures',str(len(r.failures)));r.suite.set('errors',str(len(r.errors)));r.suite.set('skipped',str(len(r.skipped)));ET.ElementTree(r.suite).write(O/'evidence/semantic.xml',encoding='utf-8',xml_declaration=True)
raise SystemExit(0 if r.wasSuccessful()else 1)
