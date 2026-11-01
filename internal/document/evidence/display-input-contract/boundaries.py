"""Finite host IO; no reference process, guest, master or runtime authority."""
from pathlib import Path
import hashlib,json,os,selectors,signal,stat,subprocess,tempfile,time
class Refusal(ValueError):
 def __init__(self,code,detail):self.code=code;super().__init__(detail)
def require(ok,code,detail):
 if not ok:raise Refusal(code,str(detail))
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(path,limit):
 p=Path(path).absolute();cur=Path(p.anchor)
 for part in p.parts[1:]:
  cur/=part;require(not stat.S_ISLNK(cur.lstat().st_mode),'SymlinkInput',cur)
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
 try:
  before=os.fstat(fd);require(stat.S_ISREG(before.st_mode),'RegularInput',p);require(before.st_size<=limit,'InputLimit',p)
  with os.fdopen(fd,'rb',closefd=False)as f:raw=f.read(limit+1)
  after=os.fstat(fd);require(len(raw)<=limit,'InputLimit',p);require((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns),'ChangedInput',p);return raw
 finally:os.close(fd)
def pairs(rows):
 out={}
 for k,v in rows:require(k not in out,'DuplicateJSON',k);out[k]=v
 return out
def parse(raw,depth=48,nodes=750000):
 try:
  value=json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in()).throw(Refusal('JSONConstant',v)))
 except (ValueError,RecursionError)as e:
  if isinstance(e,Refusal):raise
  raise Refusal('MalformedJSON',str(e))from e
 stack=[(value,1)];count=0
 while stack:
  v,d=stack.pop();count+=1;require(count<=nodes and d<=depth,'JSONShape','finite nodes/depth')
  if isinstance(v,dict):stack.extend((x,d+1)for x in v.values())
  elif isinstance(v,list):stack.extend((x,d+1)for x in v)
 return value
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def process(argv,cwd,timeout=60,stdout_limit=64<<20,stderr_limit=1<<20,input_bytes=None,allow_nonzero=False):
 """Keep leader unreaped while private process group is terminated, even after EOF."""
 feed=tempfile.TemporaryFile() if input_bytes is not None else None
 if feed is not None:feed.write(input_bytes);feed.seek(0)
 try:p=subprocess.Popen(argv,cwd=cwd,stdin=feed if feed is not None else subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
 except BaseException:
  if feed is not None:feed.close()
  raise
 if feed is not None:feed.close()
 sel=selectors.DefaultSelector();out=[bytearray(),bytearray()];failure=None;start=time.monotonic()
 for i,f in enumerate([p.stdout,p.stderr]):os.set_blocking(f.fileno(),False);sel.register(f,selectors.EVENT_READ,i)
 try:
  while sel.get_map():
   require(time.monotonic()-start<timeout,'ProcessDeadline',argv[0])
   for key,_ in sel.select(min(.05,max(0,timeout-(time.monotonic()-start)))):
    b=os.read(key.fd,65536)
    if not b:sel.unregister(key.fileobj);continue
    i=key.data;out[i]+=b;require(len(out[i])<=[stdout_limit,stderr_limit][i],'ProcessOutputLimit',argv[0])
  while not os.waitid(os.P_PID,p.pid,os.WEXITED|os.WNOHANG|os.WNOWAIT):
   require(time.monotonic()-start<timeout,'ProcessDeadline',argv[0]);time.sleep(.01)
 except BaseException as e:failure=e
 finally:
  # p has never been polled/waited: its PID anchors this setsid group until cleanup.
  try:
   require(os.getpgid(p.pid)==p.pid and os.getsid(p.pid)==p.pid,'ProcessOwnership',p.pid)
   os.killpg(p.pid,signal.SIGTERM);time.sleep(.05);os.killpg(p.pid,signal.SIGKILL)
  except ProcessLookupError:pass
  except BaseException as e:failure=Refusal('CleanupFailure',str(e))
  for f in [p.stdout,p.stderr]:f.close()
  sel.close()
  try:code=p.wait(timeout=2)
  except BaseException as e:raise Refusal('CleanupFailure',str(e))from e
 if failure:raise failure
 if allow_nonzero:return bytes(out[0]),bytes(out[1]),code
 require(code==0,'ProcessExit',f'{argv[0]} exit={code}; stderr={bytes(out[1])[:512]!r}')
 return bytes(out[0]),bytes(out[1])
def publish(path,value,owned):
 raw=json.dumps(value,indent=2,sort_keys=True).encode()+b'\n';require(len(raw)<=4<<20,'ReportLimit',len(raw));p=Path(path).absolute();require(p.parent==owned.absolute()and p.name.endswith('.result.json'),'OutputScope',p)
 require(not p.is_symlink(),'OutputType',p)
 if p.exists():require(stat.S_ISREG(p.lstat().st_mode)and not p.is_symlink(),'OutputType',p)
 fd,tmp=tempfile.mkstemp(prefix='.wp56-',dir=p.parent)
 try:
  with os.fdopen(fd,'wb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
  os.replace(tmp,p)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
