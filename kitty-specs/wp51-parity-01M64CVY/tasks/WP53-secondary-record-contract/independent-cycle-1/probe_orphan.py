from pathlib import Path
import importlib.util,sys,tempfile,os,signal,time,json
from unittest.mock import patch
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-w');sys.dont_write_bytecode=True
s=importlib.util.spec_from_file_location('c',R/'scripts/reference/secondary_record_contract.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
with tempfile.TemporaryDirectory(prefix='wp53-review-child-')as t:
 p=Path(t)/'pid';child=f'import os,time;open({str(p)!r},"w").write(str(os.getpid()));time.sleep(5)';parent=f'import subprocess,sys;subprocess.Popen([sys.executable,"-c",{child!r}])';argv=[sys.executable,'-c',parent];owned=[];real=c.subprocess.Popen
 def capture(*a,**kw):
  proc=real(*a,**kw);owned.append(proc);return proc
 started=time.monotonic()
 with patch.object(c.subprocess,'Popen',side_effect=capture):
  try:c.bounded(argv,Path(t),timeout=.3)
  except c.Refusal as e:code=str(e)
 pid=int(p.read_text());pgid=os.getpgid(pid);state=Path(f'/proc/{pid}/stat').read_text();alive=True
 try:os.kill(pid,0)
 except ProcessLookupError:alive=False
 assert len(owned)==1 and owned[0].poll()==0 and pgid==owned[0].pid and alive
 result={'error':code,'elapsed_seconds':time.monotonic()-started,'timeout_seconds':.3,'actual_production_seam':str(R/'scripts/reference/secondary_record_contract.py')+':bounded','argv':argv,'descendant_argv':[sys.executable,'-c',child],'immediate_parent_pid':owned[0].pid,'immediate_parent_exit':owned[0].returncode,'descendant_alive_after_timeout':alive,'descendant_stat_before_cleanup':state,'child_pid':pid,'owned_process_group':pgid,'synthetic_offline_only':True}
 if alive:os.killpg(pgid,signal.SIGTERM);result['review_cleanup']='SIGTERM only isolated test-owned process group whose PGID equals captured start_new_session parent PID'
 print(json.dumps(result,indent=2));Path('/tmp/wordling-WP53-independent-review/orphan-result.json').write_text(json.dumps(result,indent=2)+'\n')
