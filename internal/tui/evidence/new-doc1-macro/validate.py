"""Frozen formal command receipts. Evidence-only; never imported by product."""
from pathlib import Path
import hashlib,json,os,resource,signal,subprocess,sys,time
ROOT=Path.cwd();OUT=ROOT/'internal/tui/evidence/new-doc1-macro'
COMMANDS={
 'configured':['python3','scripts/review_checks.py','--junitxml='+str(OUT/'formal-configured.xml')],
 'race':['go','test','-race','-timeout=120s','./...'],
 'model':['go','test','-v','-timeout=90s','./internal/tui','-run','TestNewMacro|TestMacroPTYNativeArtifacts','-count=1'],
 'build':['go','build','-o','/tmp/wordling-WP66-production-final.bin','./cmd/wordling'],
}
if len(sys.argv)==1:
 source={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['internal/tui','internal/editor'] for p in sorted(ROOT.joinpath(folder).glob('*.go'))}
 evidence={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.glob('*.py'))}
 freeze={'claim_head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'source':source,'evidence_scripts':evidence,'inputs_sha256':hashlib.sha256((OUT/'inputs.json').read_bytes()).hexdigest(),'baseline_sha256':hashlib.sha256((OUT/'baseline.json.gz').read_bytes()).hexdigest(),'commands':COMMANDS,'cwd':str(ROOT),'env_nonsecret_for_model':{'WORDLING_WP66_MODEL':str(OUT/'model'),'WORDLING_WP37_NATIVE':str(OUT/'model-native'),'WORDLING_WP37_PTY_MANIFEST':str(OUT/'pty-native-manifest.json')},'commands_wall_seconds':300,'Model_events_per_case':4096,'PTY':'already completed3 healthy cases, actual production mutants2FLOW pass fixed constant then ABC fails;30s+2cleanup,live2MiB cap; no healthy PTY repetition for telemetry-only adjustments'}
 (OUT/'formal-freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
 for name in COMMANDS:
  run=subprocess.run([sys.executable,__file__,name],timeout=305)
  if run.returncode:sys.exit(run.returncode)
 sys.exit(0)
name=sys.argv[1];argv=COMMANDS[name];env=os.environ.copy()
if name=='model':env.update(WORDLING_WP66_MODEL=str(OUT/'model'),WORDLING_WP37_NATIVE=str(OUT/'model-native'),WORDLING_WP37_PTY_MANIFEST=str(OUT/'pty-native-manifest.json'))
started=time.monotonic();fds_before=len(os.listdir('/proc/self/fd'));samples=[];unavailable=[];timedout=False
with (OUT/('formal-'+name+'.txt')).open('wb') as stream:
 child=subprocess.Popen(argv,cwd=ROOT,env=env,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
 while child.poll() is None:
  try:samples.append(len(os.listdir('/proc/'+str(child.pid)+'/fd')))
  except (FileNotFoundError,PermissionError) as e:unavailable.append({'error':type(e).__name__,'elapsed':time.monotonic()-started,'child_returncode':child.poll()})
  if time.monotonic()-started>300:timedout=True;os.killpg(child.pid,signal.SIGTERM);break
  time.sleep(.02)
 code=child.wait(timeout=3)
usage=resource.getrusage(resource.RUSAGE_CHILDREN)
receipt={'argv':argv,'cwd':str(ROOT),'exit':code,'elapsed':round(time.monotonic()-started,6),'timed_out':timedout,'wall_bound':300,'pid':child.pid,'direct_child_reaped':True,'direct_child_fd_samples':len(samples),'direct_child_fd_min':min(samples) if samples else None,'direct_child_fd_max':max(samples) if samples else None,'unavailable_fd_samples':unavailable,'parent_fd_before':fds_before,'parent_fd_after':len(os.listdir('/proc/self/fd')),'children_peak_rss_KiB':usage.ru_maxrss,'children_user_seconds':usage.ru_utime,'children_system_seconds':usage.ru_stime,'limits':'observed Linux child accounting/direct-child FD samples; unavailable stays unknown; no all-descendant FD/hardRT/hostile sandbox bound'}
(OUT/('formal-'+name+'-receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
print(name,code,receipt['elapsed'],usage.ru_maxrss,flush=True);sys.exit(code)
