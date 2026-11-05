"""Formal bounded command telemetry; evidence tooling, never product-imported."""
from pathlib import Path
import hashlib,json,os,resource,subprocess,sys,time,signal
ROOT=Path.cwd();OUT=ROOT/'internal/editor/evidence/new-doc1-macro'
COMMANDS={
 'configured':['python3','scripts/review_checks.py','--junitxml='+str(OUT/'formal-configured.xml')],
 'race':['go','test','-race','-timeout=120s','./...'],
 'new':['go','test','-v','-timeout=90s','./internal/editor','-run','TestNewMacro','-count=1'],
}
if len(sys.argv)==1:
 source={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.joinpath('internal/editor').glob('*.go'))}
 freeze={'scope':'source frozen before these formal positives; development runs remain separately retained','source':source,'inputs_sha256':hashlib.sha256((OUT/'inputs.json').read_bytes()).hexdigest(),'commands':COMMANDS,'cwd':str(ROOT),'env_recorded_only':{'WORDLING_WP36_CANDIDATES':str(OUT/'candidates')},'wall_bound_seconds_per_command':300,'driver_event_bound':4096,'expectations':'19 final compile-valid semantic kills; both original FLOW sources/quota1+16 whole337 raw/only indexed packet06 OR08; ABC third source; assertions, guards, first-binding and all existing loaded regressions'}
 (OUT/'formal-freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
 for name in COMMANDS:
  r=subprocess.run([sys.executable,__file__,name],timeout=305)
  if r.returncode:sys.exit(r.returncode)
 sys.exit(0)
name=sys.argv[1];command=COMMANDS[name];env=os.environ.copy()
if name=='new':env['WORDLING_WP36_CANDIDATES']=str(OUT/'candidates')
before=len(os.listdir('/proc/self/fd'));started=time.monotonic();samples=[];timedout=False
with (OUT/('formal-'+name+'.txt')).open('wb') as stream:
 p=subprocess.Popen(command,stdout=stream,stderr=subprocess.STDOUT,cwd=ROOT,env=env,start_new_session=True)
 while p.poll() is None:
  try:samples.append(len(os.listdir('/proc/'+str(p.pid)+'/fd')))
  except FileNotFoundError:pass
  if time.monotonic()-started>300:
   timedout=True;os.killpg(p.pid,signal.SIGTERM);break
  time.sleep(.02)
 code=p.wait(timeout=3)
u=resource.getrusage(resource.RUSAGE_CHILDREN)
r={'command':command,'cwd':str(ROOT),'exit':code,'elapsed_seconds':round(time.monotonic()-started,6),'wall_bound_seconds':300,'timed_out':timedout,'pid':p.pid,'direct_child_reaped':True,'direct_child_fd_samples':len(samples),'direct_child_fd_min':min(samples) if samples else None,'direct_child_fd_max':max(samples) if samples else None,'parent_fd_before':before,'parent_fd_after':len(os.listdir('/proc/self/fd')),'children_peak_rss_KiB':u.ru_maxrss,'children_user_seconds':u.ru_utime,'children_system_seconds':u.ru_stime,'limitations':'Linux observed child accounting/direct-child FD samples; no all-descendant FD bound, hostile sandbox or hard real-time claim; only owned host subprocesses'}
(OUT/('formal-'+name+'-receipt.json')).write_text(json.dumps(r,indent=2)+'\n')
print(name,code,r['elapsed_seconds'],u.ru_maxrss,flush=True)
sys.exit(code)
