from pathlib import Path
import importlib.util,sys,tempfile,os,signal,time,json
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-w');sys.dont_write_bytecode=True
s=importlib.util.spec_from_file_location('c',R/'scripts/reference/secondary_record_contract.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
with tempfile.TemporaryDirectory(prefix='wp53-review-child-')as t:
 p=Path(t)/'pid';child=f'import os,time;open({str(p)!r},"w").write(str(os.getpid()));time.sleep(5)';parent=f'import subprocess,sys;subprocess.Popen([sys.executable,"-c",{child!r}])'
 try:
  c.bounded([sys.executable,'-c',parent],Path(t),timeout=.3)
 except c.Refusal as e:code=str(e)
 pid=int(p.read_text());pgid=os.getpgid(pid);alive=True
 try:os.kill(pid,0)
 except ProcessLookupError:alive=False
 result={'error':code,'descendant_alive_after_timeout':alive,'child_pid':pid,'owned_process_group':pgid,'synthetic_offline_only':True}
 if alive:os.killpg(pgid,signal.SIGTERM);result['review_cleanup']='terminated only isolated test-owned process group'
 print(json.dumps(result,indent=2));Path('/tmp/wordling-WP53-independent-review/orphan-result.json').write_text(json.dumps(result,indent=2)+'\n')
