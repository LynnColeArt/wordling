#!/usr/bin/env python3
"""Execute real offline unittest assertions and retain their JUnit outcomes."""
import importlib.util,sys,unittest,xml.etree.ElementTree as ET
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('wp48_original_plan_checks',HERE/'test_adapter.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
entry_spec=importlib.util.spec_from_file_location('wp48_setup_entry_checks',HERE/'test_setup_entry.py');entry=importlib.util.module_from_spec(entry_spec);entry_spec.loader.exec_module(entry)
suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromModule(module),unittest.defaultTestLoader.loadTestsFromModule(entry)]);names=[]
def collect(s):
 for x in s:
  if isinstance(x,unittest.TestSuite):collect(x)
  else:names.append(x.id())
collect(suite);result=unittest.TextTestRunner(verbosity=2).run(suite);xml=ET.Element('testsuite',name='WP48 R1 offline original-plan controls',tests=str(result.testsRun),failures=str(len(result.failures)),errors=str(len(result.errors)),skipped=str(len(result.skipped)))
errors={x.id():trace for x,trace in result.errors};failures={x.id():trace for x,trace in result.failures};skipped={x.id():why for x,why in result.skipped}
for name in names:
 case=ET.SubElement(xml,'testcase',name=name)
 if name in errors:ET.SubElement(case,'error').text=errors[name]
 if name in failures:ET.SubElement(case,'failure').text=failures[name]
 if name in skipped:ET.SubElement(case,'skipped').text=skipped[name]
ET.indent(xml);ET.ElementTree(xml).write(HERE/'checks/offline.xml',encoding='utf-8',xml_declaration=True);raise SystemExit(not result.wasSuccessful())
