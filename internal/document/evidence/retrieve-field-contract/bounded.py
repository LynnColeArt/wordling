"""Finite local subprocess/file boundaries; no shell or guest operations."""
from pathlib import Path
import os,selectors,stat,subprocess,tempfile,time
class Refusal(ValueError):
 def __init__(self,code,detail):self.code=code;super().__init__(detail)
def require(ok,code,detail):
 if not ok:raise Refusal(code,detail)
def read_limited(path,limit):
 try:
  fd=os.open(path,os.O_RDONLY|os.O_NONBLOCK|os.O_NOFOLLOW)
  with os.fdopen(fd,'rb')as f:
   info=os.fstat(f.fileno());require(stat.S_ISREG(info.st_mode),'InputFileType','only regular non-symlink input files')
   require(info.st_size<=limit,'InputBudget',str(path));raw=f.read(limit+1)
  require(len(raw)<=limit,'InputBudget',str(path));return raw
 except OSError as e:raise Refusal('InputIO',str(e))from e
def process(argv,cwd,stdin=b'',timeout=20,stdout_limit=48*1024*1024,stderr_limit=1024*1024):
 """Drain both pipes concurrently, kill+reap on caps/deadline, no orphan/no unlimited capture."""
 require(len(stdin)<=512*1024,'SubprocessInputBudget','finite batch roster')
 with tempfile.TemporaryFile()as inp:
  inp.write(stdin);inp.seek(0)
  try:p=subprocess.Popen(argv,cwd=cwd,stdin=inp,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  except OSError as e:raise Refusal('SubprocessStart',str(e))from e
  data={'stdout':bytearray(),'stderr':bytearray()};limits={'stdout':stdout_limit,'stderr':stderr_limit};deadline=time.monotonic()+timeout
  try:
   with selectors.DefaultSelector()as sel:
    for name in data:sel.register(getattr(p,name),selectors.EVENT_READ,name)
    while sel.get_map():
     require(time.monotonic()<deadline,'SubprocessTimeout','bounded local helper deadline')
     for key,_ in sel.select(min(.05,max(0,deadline-time.monotonic()))):
      raw=os.read(key.fileobj.fileno(),65536)
      if not raw:sel.unregister(key.fileobj);continue
      require(len(data[key.data])+len(raw)<=limits[key.data],'SubprocessOutputBudget',key.data);data[key.data].extend(raw)
   try:code=p.wait(timeout=max(.001,deadline-time.monotonic()))
   except subprocess.TimeoutExpired as e:raise Refusal('SubprocessTimeout','helper outlived closed pipes')from e
   require(code==0,'SubprocessExit',str(code)+': '+bytes(data['stderr'][:1024]).decode(errors='replace'))
   return bytes(data['stdout']),bytes(data['stderr'])
  except BaseException:
   if p.poll()is None:p.kill()
   p.wait();raise
  finally:
   p.stdout.close();p.stderr.close()
def atomic_report(path,raw):
 require(len(raw)<=2*1024*1024,'ReportBudget','report <=2MiB')
 dest=Path(path);require(not dest.is_symlink(),'ReportPath','symlink output refused')
 require(dest.parent.is_dir(),'ReportPath','output parent must already exist')
 name=None
 try:
  fd,name=tempfile.mkstemp(prefix='.retrieve-report-',dir=dest.parent)
  with os.fdopen(fd,'wb')as f:
   count=f.write(raw);require(count==len(raw),'ReportShortWrite','incomplete report write');f.flush();os.fsync(f.fileno())
  os.replace(name,dest);name=None
 except OSError as e:raise Refusal('ReportIO',str(e))from e
 finally:
  if name is not None:
   try:os.unlink(name)
   except OSError as e:raise Refusal('ReportCleanup',str(e))from e
