"""Preserve initial46 result; run45 unaffected tests, explicitly exclude old fresh-path premise."""
import importlib.util,sys,unittest,xml.etree.ElementTree as ET
from pathlib import Path
H=Path.cwd()/'internal/document/evidence/h1-admission-contract';sys.path.insert(0,str(H));suite=unittest.defaultTestLoader.discover(str(H),pattern='test_*.py');selected=[];excluded=[]
def walk(s):
 for x in s:
  if isinstance(x,unittest.TestSuite):walk(x)
  elif x.id()=='test_cli.CLI.test_default_and_check_deterministic_read_only':excluded.append({'id':x.id(),'reason':'historical prelaunch phase assumes real ledger absent; retained halted ledger must remain after actual attempt'})
  else:selected.append(x)
walk(suite);assert len(selected)==45 and len(excluded)==1;from run_checks import Result
r=unittest.TextTestRunner(verbosity=2,resultclass=Result).run(unittest.TestSuite(selected));root=ET.Element('testsuite',tests=str(r.testsRun),failures=str(len(r.failures)),errors=str(len(r.errors)),skipped=str(len(r.skipped)));root.extend(r.cases);ET.SubElement(root,'properties');ET.ElementTree(root).write('/tmp/wordling-wp51-independent/phase-independent.xml',encoding='utf-8',xml_declaration=True)
import json
Path('/tmp/wordling-wp51-independent/phase-exclusion.json').write_text(json.dumps({'original_suite':'offline.xml:46tests/1prelaunch-premise-failure','excluded_phase_premise':excluded,'fresh_independent_tests':r.testsRun,'failures':len(r.failures),'errors':len(r.errors)},indent=2)+'\n');raise SystemExit(not r.wasSuccessful())
