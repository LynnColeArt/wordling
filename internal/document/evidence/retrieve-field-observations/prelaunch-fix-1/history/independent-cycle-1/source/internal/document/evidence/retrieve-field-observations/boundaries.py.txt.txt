"""Bounded offline IO/process boundaries. No guest, socket or native write API."""
from pathlib import Path
import json,os,selectors,signal,stat,subprocess,tempfile,time
class Refusal(ValueError):
 def __init__(self,code,detail):self.code=code;super().__init__(detail)
def require(ok,code,detail):
 if not ok:raise Refusal(code,detail)
def canonical(obj):return json.dumps(obj,sort_keys=True,separators=(',',':')).encode()
def read(path,limit=2<<20):
 try:
  fd=os.open(path,os.O_RDONLY|os.O_NONBLOCK|os.O_NOFOLLOW|os.O_CLOEXEC)
  with os.fdopen(fd,'rb')as f:
   s=os.fstat(f.fileno());require(stat.S_ISREG(s.st_mode)and s.st_size<=limit,'InputBoundary','finite regular non-symlink file');raw=f.read(limit+1)
  require(len(raw)<=limit,'InputBoundary','input grew over bound');return raw
 except OSError as e:raise Refusal('InputIO',str(e))from e
def parse(raw):
 require(len(raw)<=2<<20,'JSONBudget','<=2MiB JSON')
 def unique(items):
  d={}
  for k,v in items:require(k not in d,'DuplicateJSON','duplicate key');d[k]=v
  return d
 try:obj=json.loads(raw,object_pairs_hook=unique)
 except(ValueError,UnicodeError,RecursionError)as e:raise Refusal('JSONInput',str(e))from e
 stack=[(obj,0)];nodes=0
 while stack:
  v,depth=stack.pop();nodes+=1;require(depth<=32 and nodes<=32768,'JSONBudget','finite nodes/depth')
  if isinstance(v,dict):stack.extend((x,depth+1)for x in v.values())
  if isinstance(v,list):stack.extend((x,depth+1)for x in v)
 return obj
def atomic_report(path,raw):
 require(len(raw)<=2<<20,'ReportBudget','<=2MiB');dest=Path(path);require(dest.parent.is_dir()and not dest.is_symlink(),'ReportPath','existing parent/non-symlink destination');tmp=None
 try:
  fd,tmp=tempfile.mkstemp(prefix='.r55-',dir=dest.parent)
  with os.fdopen(fd,'wb')as f:require(f.write(raw)==len(raw),'ShortWrite','report write');f.flush();os.fsync(f.fileno())
  os.replace(tmp,dest);tmp=None
 except OSError as e:raise Refusal('ReportIO',str(e))from e
 finally:
  if tmp is not None:os.unlink(tmp)
def _pin(p):
 require(p.returncode is None,'CleanupOwnershipLost','leader must remain unreaped')
 try:
  info=os.waitid(os.P_PID,p.pid,os.WEXITED|os.WNOHANG|os.WNOWAIT)
  pgid=os.getpgid(p.pid);sid=os.getsid(p.pid)
 except(OSError,ChildProcessError)as e:raise Refusal('CleanupOwnershipLost','unreaped private leader unavailable')from e
 require(pgid==sid==p.pid,'CleanupOwnershipLost','exact private PGID/session only');return info

def _cleanup(p,receipts,grace=.10):
 _pin(p);receipts.append({'pid':p.pid,'pgid':p.pid,'session':p.pid,'leader_unreaped':True,'signal':'TERM'});os.killpg(p.pid,signal.SIGTERM)
 # Keep the unreaped leader pin even when it exits first. Never poll/communicate here.
 deadline=time.monotonic()+grace
 while time.monotonic()<deadline:time.sleep(.01)
 _pin(p);os.killpg(p.pid,signal.SIGKILL);receipts.append({'pid':p.pid,'pgid':p.pid,'session':p.pid,'leader_unreaped':True,'signal':'KILL'})
 # Positive pipe EOF bounds descendants inheriting stdout/stderr, even if leader exited0.
 deadline=time.monotonic()+1;selector=selectors.DefaultSelector()
 try:
  for f in [p.stdout,p.stderr]:
   if f is not None and not f.closed:os.set_blocking(f.fileno(),False);selector.register(f,selectors.EVENT_READ)
  while selector.get_map():
   require(time.monotonic()<deadline,'CleanupFailed','owned group pipes not EOF after KILL')
   for key,_ in selector.select(.02):
    b=os.read(key.fileobj.fileno(),65536)
    if not b:selector.unregister(key.fileobj)
 finally:selector.close()
 p.wait(timeout=1)
def process(argv,cwd,stdin=b'',timeout=20,stdout_limit=2<<20,stderr_limit=1<<20,receipts=None,check=True):
 require(type(argv)is list and argv and all(type(x)is str for x in argv),'ProcessArguments','argv list/no shell');require(len(stdin)<=512<<10,'InputBudget','bounded stdin');require(0<timeout<=240,'ProcessDeadline','finite deadline');receipts=[]if receipts is None else receipts
 with tempfile.TemporaryFile()as inp:
  inp.write(stdin);inp.seek(0)
  try:p=subprocess.Popen(argv,cwd=cwd,stdin=inp,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
  except OSError as e:raise Refusal('ProcessStart',str(e))from e
  data={'stdout':bytearray(),'stderr':bytearray()};limits={'stdout':stdout_limit,'stderr':stderr_limit};deadline=time.monotonic()+timeout
  try:
   with selectors.DefaultSelector()as sel:
    for name in data:sel.register(getattr(p,name),selectors.EVENT_READ,name)
    while sel.get_map():
     require(time.monotonic()<deadline,'ProcessTimeout','local helper deadline')
     for key,_ in sel.select(min(.03,max(0,deadline-time.monotonic()))):
      raw=os.read(key.fileobj.fileno(),65536)
      if not raw:sel.unregister(key.fileobj);continue
      require(len(data[key.data])+len(raw)<=limits[key.data],'ProcessOutputLimit',key.data);data[key.data].extend(raw)
   while _pin(p)is None:
    require(time.monotonic()<deadline,'ProcessTimeout','leader outlived closed pipes');time.sleep(.01)
   # Even success0 may leave a child with redirected/closed pipes. Pin and clean
   # the entire private group BEFORE reaping the original leader.
   _cleanup(p,receipts,grace=.001)
  except BaseException:
   try:_cleanup(p,receipts)
   finally:p.stdout.close();p.stderr.close()
   raise
  # Reap only AFTER leaving protected failure region. Exit-status refusal cannot strand a pipe owner.
  code=p.wait(timeout=1);p.stdout.close();p.stderr.close()
  if check:require(code==0,'ProcessExit',str(code)+':'+bytes(data['stderr'][:1024]).decode(errors='replace'));return bytes(data['stdout']),bytes(data['stderr'])
  return bytes(data['stdout']),bytes(data['stderr']),code
