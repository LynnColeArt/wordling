"""R1-only successor checks; preserve previous suites and native/original evidence."""
from pathlib import Path
import importlib.util,json,os,subprocess,sys,time,unittest,xml.etree.ElementTree as ET
from test_cleanup import CleanupTests,RESULTS,C,ROOT
from test_cli import CLITests
F=Path(__file__).resolve().parent;E=F/'evidence';O=F.parent
spec=importlib.util.spec_from_file_location('legacy_contract_tests',O/'test_contract.py');legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
class Result(unittest.TextTestResult):
 def __init__(self,*a,**k):super().__init__(*a,**k);self.xml=ET.Element('testsuite',name='WP53-R1-subprocess-successor')
 def startTest(self,test):super().startTest(test);self.start=time.monotonic();self.case=ET.SubElement(self.xml,'testcase',name=test.id())
 def stopTest(self,test):self.case.set('time',str(time.monotonic()-self.start));super().stopTest(test)
 def addFailure(self,test,err):super().addFailure(test,err);ET.SubElement(self.case,'failure').text=self._exc_info_to_string(err,test)
 def addError(self,test,err):super().addError(test,err);ET.SubElement(self.case,'error').text=self._exc_info_to_string(err,test)
os.environ.pop('WP53_CHECKER_SOURCE',None)
os.environ['WP53_CLI_RECEIPT']=str(E/'final-cli.json');os.environ['WP53_TEST_RECEIPT']=str(E/'selected-legacy-receipt.json')
suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(CleanupTests),unittest.defaultTestLoader.loadTestsFromTestCase(CLITests)])
for name in ['test_bounded_subprocess_timeout_cap_failure_and_no_orphan','test_public_cli_semantic_refusal_preserves_prior_output','test_atomic_reports_and_path_refusals','test_immutable_source_binding_and_partial_helper_fail_atomically']:
 suite.addTest(legacy.ContractTests(name))
result=unittest.TextTestRunner(verbosity=2,resultclass=Result).run(suite)
for name,value in [('tests',result.testsRun),('failures',len(result.failures)),('errors',len(result.errors)),('skipped',len(result.skipped))]:result.xml.set(name,str(value))
ET.ElementTree(result.xml).write(E/'successor.xml',encoding='utf-8',xml_declaration=True)
(E/'final-processes.json').write_text(json.dumps({'checker_source_sha256':C.digest((ROOT/'scripts/reference/secondary_record_contract.py').read_bytes()),'actual_OS_cases':RESULTS,'test_only_subreaper':True,'production_subreaper_or_proc_scan':False},indent=2)+'\n')
if not result.wasSuccessful():raise SystemExit(1)
with C.Session(ROOT)as session:
 for i,argv in enumerate([['go','build','./...'],['go','test','-count=1','./...'],['go','vet','./...'],['go','test','-race','-count=1','./...']]):
  out=session.run(argv);(E/f'helper-{i}.log').write_bytes(out)
 session.build_proof();(E/'fresh-composition.json').write_text(json.dumps(session.receipt,indent=2)+'\n')
argv=[sys.executable,'scripts/review_checks.py','--junitxml='+str(E/'configured.xml')]
p=subprocess.run(argv,cwd=ROOT,capture_output=True,timeout=240);(E/'configured.log').write_bytes(p.stdout+p.stderr)
(E/'checks.json').write_text(json.dumps({'configured_argv':argv,'configured_exit':p.returncode,'successor_tests':result.testsRun,'no_10_original_audit_or_long_parser_fuzz_rerun':True},indent=2)+'\n')
if p.returncode:raise SystemExit(p.returncode)
print(json.dumps({'successor_tests':result.testsRun,'all_pass':True,'configured_exit':0,'real_source_bound_helper_checks':True}))
