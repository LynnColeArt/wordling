import ast,hashlib,json,subprocess
from pathlib import Path
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-e'); O=Path('/tmp/wordling-WP44-stop-diagnosis'); C='bea27c98e57fee5c341d1b74d4c8877bdcc2d42d'; B='internal/document/evidence/wp44/runs/wp44-phase01/'
def sha(b):return hashlib.sha256(b).hexdigest()
def git(p):return subprocess.check_output(['git','-C',str(R),'show',C+':'+p])
j=json.loads(git('internal/document/evidence/wp44/seals.json')); seals=j['sources_and_evidence']; assert len(seals)==485
for p,s in seals.items():
 b=git(p);assert len(b)==s['size'] and sha(b)==s['sha256'];assert (R/p).read_bytes()==b
failure=json.loads(git(B+'failure-seals.json'))
for p,s in failure['files'].items():
 b=git(B+p); assert len(b)==s['size'] and sha(b)==s['sha256']
pre=json.loads(git(B+'prelaunch.json'));run=json.loads(git(B+'run.json'));ledger=git(B+'aggregate-ledger.json');a=json.loads(ledger)
assert len(run['results'])==len(a['attempts'])==1 and not run['complete'] and not run['oracle_released']
assert a['attempts'][0]['outcome']=='incomplete' and run['results'][0]['stop_error_code']=='OwnedStillRunning'
wire=[]
for line in git(B+'wp44-c09-candidate-r1/qmp-wire.jsonl').splitlines():
 w=json.loads(line); raw=bytes.fromhex(w['raw_hex'])
 try:d=json.loads(raw)
 except (ValueError,UnicodeError):continue
 if d.get('execute')=='quit' or d.get('event')=='SHUTDOWN':wire.append({**w,'decoded':d})
# Execute unchanged actual stopped AST with deterministic fake filesystem only. No module imports, guest or private reads.
source=git('internal/document/evidence/wp44/oracle.py').decode();tree=ast.parse(source)
ns={};exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,(ast.FunctionDef,ast.ClassDef)) and x.name in ['Refusal','require','stopped']],type_ignores=[]),'frozen-oracle-AST','exec'),ns)
checks=[]
for state,socket,expected in [('S',False,'OwnedStillRunning'),('Z',False,'ok'),('gone',False,'ok'),('reuse',False,'OwnedStillRunning'),('gone',True,'OwnedSocketPresent')]:
 calls=[]
 class Fake:
  def __init__(self,p):self.p=p
  def __truediv__(self,s):return Fake(self.p+'/'+s)
  def exists(self):calls.append(('exists',self.p));return socket if self.p=='socket' else state!='gone'
  def read_text(self):calls.append(('read',self.p));return '2948208 (qemu) '+('Z' if state=='Z' else 'S')+' '+' '.join(['0']*18+['999' if state=='reuse' else '15065590'])
 ns['Path']=Fake
 try:ns['stopped'](type('Q',(),{'SOCKET':Fake('socket')})(),{'pid':2948208,'startticks':'15065590'});actual='ok'
 except ns['Refusal'] as e:actual=e.code
 assert actual==expected,(state,actual)
 checks.append({'state':state,'socket_present':socket,'expected':expected,'actual':actual,'actual_frozen_function_calls':calls})
result={'commit':C,'485_prelaunch_Git_and_working_seals_exact':True,'failed_run_Git_seals':len(failure['files']),'sources':[{ 'path':p,'sha256':sha(git(p))}for p in ['internal/document/evidence/wp44/oracle.py','scripts/reference/guest.py','scripts/reference/macro_session.py','scripts/reference/qmp.py',B+'run.json',B+'prelaunch.json',B+'release-checkpoint.json',B+'aggregate-ledger.json',B+'wp44-c09-candidate-r1/qmp-wire.jsonl']],'plan_sha256':pre['plan_sha256'],'historical_ledger_sha256':sha(ledger),'wire_shutdown':wire,'actual_stopped_offline_cases':checks,'private_disk_access':False,'VM_or_extraction':False,'tracked_status':subprocess.check_output(['git','-C',str(R),'status','--porcelain']).decode()}
(O/'audit.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps({'prelaunch_seals':485,'failure_seals':len(failure['files']),'actual_stopped_cases':len(checks),'source_clean':not result['tracked_status'],'ledger_sha256':sha(ledger)}))
