"""Execute bounded in-memory poll mutants against deterministic integrity tests."""
import inspect
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sys.path.insert(0,str(BASE))
import test_stop_protocol as t
source=inspect.getsource(t.ACTUAL_STOP)
mutants=[
 ('one-shot-no-wait','  pause(min(interval,remaining)) # scheduling between observations, never proof',"  raise Refusal('OwnedStillRunning','mutant one-shot')",['test_live_then_same_zombie_waits_and_logs','test_live_then_gone_waits']),
 ('accept-reused-PID',"  require(kind!='pid-reused','OwnedPIDReused','PID reused/changed startticks; refuse immediately')","  if kind=='pid-reused':kind='gone';entry['pid_present']=False",['test_reused_zombie_refuses_immediately_without_wait']),
 ('accept-present-socket',"  if kind in ['gone','zombie']and not entry['socket_present']:","  if kind in ['gone','zombie']:",['test_zombie_and_gone_wait_for_socket_absence','test_terminal_PID_with_socket_forever_refuses'])]
rows=[]
for name,old,new,tests in mutants:
 assert source.count(old)==1,name
 code=source.replace(old,new);namespace=dict(t.o.__dict__);exec(compile(code,'<owned-'+name+'>','exec'),namespace);mutant=namespace['stopped']
 suite=unittest.TestSuite(t.StopPoll(test)for test in tests);log=io.StringIO()
 with patch.object(t,'ACTUAL_STOP',mutant):result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
 assert not result.wasSuccessful(),('survived',name)
 (HERE/(name+'.log')).write_text(log.getvalue())
 rows.append({'name':name,'exact_mutation':{'from':old,'to':new},'valid_compiled_mutant':True,'tests':tests,'failures':len(result.failures),'typed_refusals_or_test_errors':len(result.errors),'detected':True,'actual_source_changed':False})
(HERE/'poll-mutation-results.json').write_text(json.dumps(rows,indent=2)+'\n');print('3 valid in-memory poll mutants detected; no source/helper/guest mutation')
