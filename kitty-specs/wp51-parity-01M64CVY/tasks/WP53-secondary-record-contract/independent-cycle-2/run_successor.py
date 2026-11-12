from pathlib import Path
import sys,importlib.util,unittest,os,json,xml.etree.ElementTree as ET,time
sys.dont_write_bytecode=True
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-w');D=R/'docs/research/continuation/secondary-record-contract';F=D/'fix-cycle-1';O=Path('/tmp/wordling-WP53-independent-review/cycle-2');sys.path.insert(0,str(F));import test_cleanup as T;import test_cli as Q
sp=importlib.util.spec_from_file_location('legacy_tests',D/'test_contract.py');L=importlib.util.module_from_spec(sp);sp.loader.exec_module(L)
os.environ['WP53_CLI_RECEIPT']=str(O/'fresh-cli.json');os.environ['WP53_TEST_RECEIPT']=str(O/'selected-legacy.json')
class Result(unittest.TextTestResult):
 def __init__(self,*a,**kw):super().__init__(*a,**kw);self.xml=ET.Element('testsuite',name='independent-WP53-cycle2')
 def startTest(self,t):super().startTest(t);self.t=time.monotonic();self.case=ET.SubElement(self.xml,'testcase',name=t.id())
 def stopTest(self,t):self.case.set('time',str(time.monotonic()-self.t));super().stopTest(t)
 def addFailure(self,t,e):super().addFailure(t,e);ET.SubElement(self.case,'failure').text=self._exc_info_to_string(e,t)
 def addError(self,t,e):super().addError(t,e);ET.SubElement(self.case,'error').text=self._exc_info_to_string(e,t)
suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(T.CleanupTests),unittest.defaultTestLoader.loadTestsFromTestCase(Q.CLITests)])
for n in ['test_bounded_subprocess_timeout_cap_failure_and_no_orphan','test_public_cli_semantic_refusal_preserves_prior_output','test_atomic_reports_and_path_refusals','test_immutable_source_binding_and_partial_helper_fail_atomically']:suite.addTest(L.ContractTests(n))
r=unittest.TextTestRunner(verbosity=2,resultclass=Result).run(suite)
for n,x in [('tests',r.testsRun),('failures',len(r.failures)),('errors',len(r.errors)),('skipped',len(r.skipped))]:r.xml.set(n,str(x))
ET.ElementTree(r.xml).write(O/'successor.xml',encoding='utf-8',xml_declaration=True);(O/'fresh-processes.json').write_text(json.dumps(T.RESULTS,indent=2)+'\n');raise SystemExit(0 if r.wasSuccessful()else 1)
