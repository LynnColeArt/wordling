"""One-shot local accounting/output ownership; never a guest/physical lease."""
import fcntl,json,os,stat
from pathlib import Path
from frames import Refusal,require

class OwnedFile:
 def __init__(self,path,expected_parent=None):
  self.path=Path(path);self.fd=None;self.parent=None
  try:
   self.parent=os.open(self.path.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC);self.parent_identity=os.fstat(self.parent)
   if expected_parent is not None:require((self.parent_identity.st_dev,self.parent_identity.st_ino)==(expected_parent.st_dev,expected_parent.st_ino),'OutputIdentityLost','never create report inside a replacement output')
   self.fd=os.open(self.path.name,os.O_RDWR|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_CLOEXEC,0o600,dir_fd=self.parent);self.identity=os.fstat(self.fd);fcntl.flock(self.fd,fcntl.LOCK_EX|fcntl.LOCK_NB);os.fsync(self.parent)
  except BaseException:
   self.close();raise
 def verify(self):
  require(self.fd is not None,'AccountingClosed','owned descriptor already closed');parent=os.stat(self.path.parent,follow_symlinks=False);current=os.stat(self.path.name,dir_fd=self.parent,follow_symlinks=False);actual=os.fstat(self.fd)
  require((actual.st_dev,actual.st_ino)==(self.identity.st_dev,self.identity.st_ino),'AccountingIdentityLost','held descriptor must still identify the owned file')
  require((parent.st_dev,parent.st_ino)==(self.parent_identity.st_dev,self.parent_identity.st_ino)and(current.st_dev,current.st_ino)==(self.identity.st_dev,self.identity.st_ino)and stat.S_ISREG(current.st_mode),'AccountingIdentityLost','never write replacement/foreign accounting')
 def write(self,obj):
  self.verify();raw=(json.dumps(obj,indent=2)+'\n').encode();require(len(raw)<=32<<20,'AccountingBudget','bounded public/accounting JSON');os.lseek(self.fd,0,os.SEEK_SET);remaining=memoryview(raw)
  while remaining:
   n=os.write(self.fd,remaining);require(n>0,'AccountingWriteFailed','no short zero write');remaining=remaining[n:]
  os.ftruncate(self.fd,len(raw));os.fsync(self.fd);self.verify();os.lseek(self.fd,0,os.SEEK_SET);require(os.read(self.fd,len(raw)+1)==raw,'AccountingReadback','actual owned descriptor readback')
 def close(self):
  for name in ['fd','parent']:
   fd=getattr(self,name,None)
   if fd is not None:os.close(fd);setattr(self,name,None)

class OwnedOutput:
 def __init__(self,path):
  self.path=Path(path);self.fd=None;self.parent=None;self.files={}
  try:
   self.path.parent.mkdir(exist_ok=True);self.parent=os.open(self.path.parent,os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC);self.parent_identity=os.fstat(self.parent);os.mkdir(self.path.name,mode=0o700,dir_fd=self.parent);self.fd=os.open(self.path.name,os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=self.parent);self.identity=os.fstat(self.fd)
  except BaseException:self.close();raise
 def verify(self):
  parent=os.stat(self.path.parent,follow_symlinks=False);current=os.stat(self.path.name,dir_fd=self.parent,follow_symlinks=False);require((parent.st_dev,parent.st_ino)==(self.parent_identity.st_dev,self.parent_identity.st_ino)and(current.st_dev,current.st_ino)==(self.identity.st_dev,self.identity.st_ino)and stat.S_ISDIR(current.st_mode),'OutputIdentityLost','no foreign output writes')
 def write(self,name,obj):
  self.verify();require(name in ['run.json','aggregate-ledger.json','prelaunch.json'],'OutputName','closed public report names')
  if name not in self.files:self.files[name]=OwnedFile(self.path/name,expected_parent=self.identity)
  self.files[name].write(obj)
 def close(self):
  for file in self.files.values():file.close()
  for name in ['fd','parent']:
   fd=getattr(self,name,None)
   if fd is not None:os.close(fd);setattr(self,name,None)
