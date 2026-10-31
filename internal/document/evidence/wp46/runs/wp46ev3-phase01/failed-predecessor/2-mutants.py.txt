"""Two compiled in-memory classifier faults; real helpers, no VM/source mutation."""
import hashlib
import importlib.util
import inspect
import io
from pathlib import Path
import unittest
from unittest.mock import patch
import json
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('successor_frame_tests',HERE/'test_adapter.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t);a=t.a
source=inspect.getsource(a.strict_empty_frame)
condition="len(lines)==25 and all(len(x)<=80 and set(x)<=set(' ')for x in lines[:24])and lines[24]==expected"
assert condition in source
rows=[]
for name,replacement,test in [('first-line-only',"not lines[0].strip()",'test_actual_helpers_misclassify_modal_but_owned_guard_stops_before_next_key'),('ignore-status',"len(lines)==25 and all(len(x)<=80 and set(x)<=set(' ')for x in lines[:24])",'test_changed_name_Doc2_page_line_position_or_extra_status_refuses')]:
 changed=source.replace(condition,replacement);scope={'old':a.old,'require':a.require};exec(compile(changed,'<isolated-classifier-mutant>','exec'),scope);mutant=scope['strict_empty_frame'];log=io.StringIO();suite=unittest.TestSuite([t.Frames(test)])
 with patch.object(a,'strict_empty_frame',mutant):result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
 assert result.failures and not result.errors,(name,log.getvalue());(HERE/'checks'/str('mutant-'+name+'.log')).write_text(log.getvalue());rows.append({'name':name,'original_function_sha256':hashlib.sha256(source.encode()).hexdigest(),'mutant_function_sha256':hashlib.sha256(changed.encode()).hexdigest(),'actual_test':test,'failures':len(result.failures),'errors':len(result.errors),'caught_by_behavior_assertions':True})
(HERE/'mutation-results.json').write_text(json.dumps(rows,indent=2)+'\n');print('2 real-helper classifier mutants caught')
