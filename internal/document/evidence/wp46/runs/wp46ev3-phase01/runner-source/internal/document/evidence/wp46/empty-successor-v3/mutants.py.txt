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
# Additional real-public-reader and failure-accounting mutants.
for name,function,oldtext,newtext,case in [
 ('wrong-closed-counter-three',a.closed_postprint,'counter:(1,2)','counter:(1,3)',t.ClosedRelations('test_rehashed_other_fields_cache_counter_flags_and_nonempty_refuse')),
 ('ignore-specific-readonly-refusal',a.closed_postprint,"post.get('refusal')==f'document: UnsupportedMetadata at token -1, span {counter}+1'",'True',t.ClosedRelations('test_actual_readonly_identity_exact_refusal_graph_are_required')),
 ('erase-historical-incomplete-count',a.run,"9+len(aggregate['attempts'])","8+len(aggregate['attempts'])",t.EarlyAuthority('test_actual_early_check_drift_sticky_after_restoration_zero_guests'))]:
 source=inspect.getsource(function);assert oldtext in source;changed=source.replace(oldtext,newtext)
 if name=='wrong-closed-counter-three':changed=changed.replace("want=b'\\x02'","want=b'\\x03'")
 scope=function.__globals__ if function.__name__=='run'else dict(function.__globals__);exec(compile(changed,'<isolated-v3-mutant>','exec'),scope);mutant=scope[function.__name__];log=io.StringIO()
 with patch.object(a,function.__name__,mutant):result=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.TestSuite([case]))
 setattr(a,function.__name__,function)
 assert result.failures and not result.errors,(name,log.getvalue());(HERE/'checks'/('mutant-'+name+'.log')).write_text(log.getvalue());rows.append({'name':name,'original_function_sha256':hashlib.sha256(source.encode()).hexdigest(),'mutant_function_sha256':hashlib.sha256(changed.encode()).hexdigest(),'actual_test':case._testMethodName,'failures':len(result.failures),'errors':len(result.errors),'caught_by_behavior_assertions':True})
(HERE/'mutation-results.json').write_text(json.dumps(rows,indent=2)+'\n');print('5 real-helper/public-reader/accounting mutants caught')
