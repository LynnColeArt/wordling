"""One-shot accounting ownership, not VM/storage transaction authority.

The exclusive journal is derived from the declared ledger path. It is never
replaced/deleted after an owned setup starts. Existing/unknown/busy foreign
state is refused without writing its ledger. All callers must authorize first.
"""
from contextlib import contextmanager
import fcntl,json,os,secrets,stat
from pathlib import Path

class SetupRefusal(ValueError):
 def __init__(self,code,detail):self.code=code;super().__init__(detail)
class SetupHalted(SetupRefusal):pass

def owner_path(plan):return Path(plan['ledger']).with_name(Path(plan['ledger']).name+'.owner')
def absent(path,code):
 try:os.lstat(path)
 except FileNotFoundError:return
 except OSError as error:raise SetupRefusal('HaltPersistenceFailed','cannot establish absent/foreign state without ownership: '+str(error))from error
 raise SetupRefusal(code,'preexisting state is not owned by this invocation: '+str(path))
def write_fd(fd,value):
 data=(json.dumps(value,indent=2,sort_keys=True)+'\n').encode();os.lseek(fd,0,os.SEEK_SET);os.ftruncate(fd,0);offset=0
 while offset<len(data):
  n=os.write(fd,data[offset:])
  if n<=0:raise OSError('zero accounting write')
  offset+=n
 os.fsync(fd)
 if os.pread(fd,len(data)+1,0)!=data:raise OSError('accounting readback differs')
def sync_parent(path):
 fd=os.open(Path(path).parent,os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
def create_exclusive(path,value):
 fd=os.open(path,os.O_RDWR|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 try:write_fd(fd,value);sync_parent(path)
 finally:os.close(fd)
def remove_own(path,fd):
 """Only an unconsumed claim we just created, with the SAME live inode."""
 actual=os.lstat(path);owned=os.fstat(fd)
 if not stat.S_ISREG(actual.st_mode)or(actual.st_dev,actual.st_ino)!=(owned.st_dev,owned.st_ino):raise SetupRefusal('HaltPersistenceFailed','claim path changed; never unlink foreign state')
 os.unlink(path);sync_parent(path)

@contextmanager
def claim(plan,out,ledger,report,adapter):
 # Rejection before ownership must not create/poison another owner's files.
 marker=owner_path(plan);lease=Path(plan['batch_lease']);out=Path(out)
 for path,code in [(marker,'PriorSetup'),(Path(plan['ledger']),'PriorAttempt'),(out,'PriorAttempt'),(lease,'ForeignLease')]:absent(path,code)
 try:fd=os.open(marker,os.O_RDWR|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 except FileExistsError as error:raise SetupRefusal('PriorSetup','another setup claimed the namespace')from error
 except OSError as error:raise SetupRefusal('HaltPersistenceFailed','cannot create a durable accounting ownership claim; zero guests; do not retry this grant: '+str(error))from error
 leased=None;record={'schema':'wordling.wp48.setup-owner/v1','plan_sha256':adapter.canonical(plan),'claim':secrets.token_hex(16),'pid':os.getpid(),'uid':os.geteuid(),'state':'owned-setup','guest_attempts':0,'invocation':report['actual_argv']}
 try:
  try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB);write_fd(fd,record);sync_parent(marker)
  except OSError as error:raise SetupRefusal('HaltPersistenceFailed','new accounting claim cannot be durably initialized; zero guests; retained claim blocks retry: '+str(error))from error
  # A preexisting/arriving foreign lease is NOT an ownerless setup failure.
  try:
   for path,code in [(Path(plan['ledger']),'PriorAttempt'),(out,'PriorAttempt'),(lease,'ForeignLease')]:absent(path,code)
   leased=os.open(lease,os.O_RDWR|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
   fcntl.flock(leased,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except (FileExistsError,BlockingIOError)as error:
   remove_own(marker,fd)
   raise SetupRefusal('ForeignLease','foreign/busy batch lease; no ledger/output written')from error
  except SetupRefusal:
   remove_own(marker,fd);raise
  except OSError as error:
   # We have the exclusive accounting claim, no lease was created, and no
   # ledger/output/lease exists. This is the bounded NOOWNER setup failure.
   try:
    if leased is not None:raise SetupRefusal('HaltPersistenceFailed','lease acquisition partly took effect; ownership uncertain')
    for path,code in [(Path(plan['ledger']),'PriorAttempt'),(out,'PriorAttempt'),(lease,'ForeignLease')]:absent(path,code)
    adapter.failure_state(ledger,report,error)
    record.update(state='halted',failure_phase='ownerless-lease-setup',failure_code=report['error_code'],guest_attempts=0)
    write_fd(fd,record)
    # Exclusive creation, not replace/dump over any foreign ledger/output.
    create_exclusive(Path(plan['ledger']),ledger)
    out.parent.mkdir(parents=True,exist_ok=True);sync_parent(out.parent);out.mkdir();sync_parent(out)
    adapter.dump(out/'aggregate-ledger.json',ledger);adapter.dump(out/'run.json',report)
   except Exception as persistence:
    raise SetupRefusal('HaltPersistenceFailed','authorized ownerless setup failed; full halt persistence not established; retained accounting claim blocks retry; zero guests: '+str(persistence))from persistence
   raise SetupHalted('SetupHalted','authorized ownerless lease setup durably halted with zero guests')from error
  try:yield leased
  finally:
   record.update(state='complete'if report.get('complete')else'halted',guest_attempts=len(ledger['attempts']))
   try:write_fd(fd,record)
   except OSError as error:raise SetupRefusal('HaltPersistenceFailed','final accounting claim state not durably established; no retry: '+str(error))from error
 finally:
  if leased is not None:os.close(leased)
  os.close(fd)
