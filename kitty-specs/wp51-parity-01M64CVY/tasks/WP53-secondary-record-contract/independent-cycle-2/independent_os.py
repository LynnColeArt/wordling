from pathlib import Path
import importlib.util,sys,os,signal,subprocess,tempfile,time,json,ctypes
from unittest.mock import patch
sys.dont_write_bytecode=True
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-w');O=Path('/tmp/wordling-WP53-independent-review/cycle-2');s=importlib.util.spec_from_file_location('c',R/'scripts/reference/secondary_record_contract.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
assert ctypes.CDLL(None).prctl(36,1,0,0,0)==0 # test process only, known own descendants
rows=[]
for case in ['old-orphan','ignore-TERM','output-cap']:
 with tempfile.TemporaryDirectory(prefix='wp53-rereview-own-')as t:
  d=Path(t);ready=d/'child.json';ign=case!='old-orphan';flood=case=='output-cap'
  child=f'''import os,signal,time,json
from pathlib import Path
if {ign!r}:signal.signal(signal.SIGTERM,signal.SIG_IGN)
p=os.getpid();Path({str(ready)!r}).write_text(json.dumps({{'pid':p,'pgid':os.getpgrp(),'sid':os.getsid(0),'stat':Path('/proc/'+str(p)+'/stat').read_text()}}))
if {flood!r}:
 parent=os.getppid()
 until=time.monotonic()+2
 while time.monotonic()<until:
  try:
   if Path('/proc/'+str(parent)+'/stat').read_text().rsplit(')',1)[1].split()[0]=='Z':break
  except FileNotFoundError:break
  time.sleep(.002)
 os.write(1,b'X'*10000)
time.sleep(8)
'''
  parent=f'''import subprocess,sys,time
from pathlib import Path
subprocess.Popen([sys.executable,'-c',{child!r}])
until=time.monotonic()+2
while not Path({str(ready)!r}).exists() and time.monotonic()<until:time.sleep(.002)
'''
  real=subprocess.Popen;real_signal=os.killpg;owned=[];signals=[];argv=[sys.executable,'-c',parent]
  def capture(*a,**kw):
   p=real(*a,**kw);owned.append(p);return p
  def emit(pgid,sig):
   assert owned and pgid==owned[0].pid and owned[0].returncode is None
   observed=os.waitid(os.P_PID,pgid,os.WEXITED|os.WNOHANG|os.WNOWAIT)
   assert os.getpgid(pgid)==pgid==os.getsid(pgid)
   if sig:signals.append({'signal':sig,'known_unreaped_child':True,'child_exit_observation':None if observed is None else observed.si_status,'PGID':pgid,'SID':os.getsid(pgid)})
   return real_signal(pgid,sig)
  started=time.monotonic();info=None
  try:
   with patch.object(C.subprocess,'Popen',side_effect=capture),patch.object(C.os,'killpg',side_effect=emit):
    try:C.bounded(argv,d,timeout=.25,cap=1024)
    except C.Refusal as e:error=str(e)
    else:raise AssertionError('expected timeout or cap')
   assert error==('HelperOutputLimit'if flood else'HelperTimeout')
   info=json.loads(ready.read_text());assert len(owned)==1 and info['pgid']==info['sid']==owned[0].pid
   deadline=time.monotonic()+1;status=None
   while time.monotonic()<deadline:
    got,v=os.waitpid(info['pid'],os.WNOHANG)
    if got:status=v;break
    time.sleep(.005)
   assert status is not None and os.WIFSIGNALED(status);assert os.WTERMSIG(status)==(signal.SIGKILL if ign else signal.SIGTERM);assert owned[0].returncode==0
   try:real_signal(owned[0].pid,0)
   except ProcessLookupError:pass
   else:raise AssertionError('private group survived positive reap')
   assert time.monotonic()-started<3.5
   rows.append({'case':case,'argv':argv,'child_script':child,'error':error,'leader_pid':owned[0].pid,'leader_exit':owned[0].returncode,'child_identity':info,'positive_waitpid_status':status,'private_group_gone_after_reap':True,'signals':signals,'elapsed':time.monotonic()-started})
  finally:
   if info is None and ready.exists():info=json.loads(ready.read_text())
   if info:
    try:
     stat=Path('/proc/'+str(info['pid'])+'/stat').read_text();assert info['pgid']==owned[0].pid
     # Emergency cleanup is only for this independently recorded test group.
     real_signal(info['pgid'],signal.SIGKILL)
    except (FileNotFoundError,ProcessLookupError):pass
    try:os.waitpid(info['pid'],0)
    except ChildProcessError:pass
   for p in owned:
    if p.returncode is None:p.wait(timeout=1)
# A genuinely consumed/reaped child is not a valid authority for any group signal.
p=subprocess.Popen([sys.executable,'-c','pass'],start_new_session=True);p.wait(timeout=2)
with patch.object(C.os,'killpg')as kill:
 try:C._terminate_owned_group(p)
 except C.Refusal as e:assert str(e).startswith('CleanupOwnershipLost')
 else:raise AssertionError('lost child pin accepted')
 assert kill.call_count==0
rows.append({'case':'already-reaped-owner','signals':0,'refusal':'CleanupOwnershipLost'})
(O/'independent-os.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
