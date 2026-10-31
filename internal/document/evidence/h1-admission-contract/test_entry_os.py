"""Actual entry OS ownership/lease faults; all resources isolated, never real VM."""
import sys
sys.dont_write_bytecode=True
import contextlib,copy,fcntl,io,json,multiprocessing,os,resource,signal,tempfile,types,unittest
from pathlib import Path
from unittest.mock import patch
import oracle,accounting,frames,test_orchestration

def setup(base):
 (base/'harddisk.img').write_bytes(b'isolated non-disk sentinel');return test_orchestration.Entry().setup_entry(base)
def invoke(base,p,args,*,check=None,attempt=None,qualify=None,exclusive=None):
 calls=[];qmp=types.SimpleNamespace(SOCKET=base/'socket');guest=types.SimpleNamespace(MASTER=base)
 def imported(name):
  calls.append('configure')
  if name!='macro_session':return types.SimpleNamespace()
  return types.SimpleNamespace(configure=lambda *a:(qmp,guest,base),timeout_signal=lambda *a:None,exclusive=exclusive or(lambda *a:contextlib.nullcontext()))
 with patch.object(oracle,'HERE',base),patch.object(oracle,'check',side_effect=check,return_value=p),patch.object(oracle.importlib,'import_module',side_effect=imported),patch.object(oracle,'attempt',side_effect=attempt or AssertionError('no guest')),patch.object(oracle,'qualify',side_effect=qualify or AssertionError('no audit')):
  code=oracle.run(args)
 return code,calls

def contender(path,ready,release,result):
 try:
  owner=accounting.OwnedFile(Path(path));owner.write({'actual_child_owner':os.getpid()});ready.set();release.wait(10);owner.close();result.put('owned')
 except Exception as error:result.put(type(error).__name__)

class EntryOS(unittest.TestCase):
 def test_existing_output_preserved_and_owned_halt_blocks_restore(self):
  with tempfile.TemporaryDirectory()as t:
   b=Path(t);p,args=setup(b);out=b/'runs'/args.grant_id;out.mkdir(parents=True);foreign=out/'run.json';foreign.write_bytes(b'{"foreign":"opaque sentinel"}\n');before=foreign.stat();raw=foreign.read_bytes();code,calls=invoke(b,p,args);self.assertEqual((code,calls),(1,[]));self.assertEqual(foreign.read_bytes(),raw);self.assertEqual(foreign.stat().st_ino,before.st_ino);self.assertEqual(sorted(x.name for x in out.iterdir()),['run.json']);ledger=json.loads((b/'ledger.json').read_text());self.assertTrue(ledger['halted']);self.assertEqual(ledger['attempts'],[]);foreign.unlink();out.rmdir()
   with self.assertRaises(frames.Refusal)as e:invoke(b,p,args)
   self.assertEqual(e.exception.code,'ExistingAccounting');print(json.dumps({'actual_OS':'foreign-output','sentinel_preserved':True,'configuration':0,'attempts':0,'restored_retry':'ExistingAccounting'}))
 def test_real_chmod_public_parent_failure_restore_cannot_configure(self):
  self.assertNotEqual(os.geteuid(),0,'must exercise actual non-root filesystem permission denial')
  with tempfile.TemporaryDirectory()as t:
   b=Path(t);p,args=setup(b);parent=b/'runs';parent.mkdir();parent.chmod(0o500)
   try:code,calls=invoke(b,p,args)
   finally:parent.chmod(0o700)
   self.assertEqual((code,calls),(1,[]));ledger=json.loads((b/'ledger.json').read_text());self.assertEqual(ledger['failure_code'],'PermissionError');self.assertTrue(ledger['halted']);self.assertFalse((parent/args.grant_id).exists());before=(b/'ledger.json').read_bytes()
   with self.assertRaises(frames.Refusal)as e:invoke(b,p,args)
   self.assertEqual(e.exception.code,'ExistingAccounting');self.assertEqual((b/'ledger.json').read_bytes(),before);print(json.dumps({'actual_OS':'chmod0500-public-parent','halt_durable':True,'attempts':0,'restored_configuration':0}))
 def test_foreign_ledger_symlink_directory_and_busy_flock_preserved(self):
  for kind in ['valid','invalid','symlink','directory','busy']:
   with self.subTest(kind=kind),tempfile.TemporaryDirectory()as t:
    b=Path(t);p,args=setup(b);ledger=b/'ledger.json';held=None
    if kind=='directory':ledger.mkdir()
    elif kind=='symlink':(b/'sentinel').write_bytes(b'foreign target');ledger.symlink_to(b/'sentinel')
    else:ledger.write_bytes(b'{}'if kind=='valid'else b'foreign opaque bytes')
    if kind=='busy':held=ledger.open('r+');fcntl.flock(held.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
    before=ledger.lstat();raw=None if kind=='directory'else ledger.read_bytes()
    try:
     with self.assertRaises(frames.Refusal)as e:invoke(b,p,args)
     self.assertEqual(e.exception.code,'ExistingAccounting');self.assertEqual(ledger.lstat().st_ino,before.st_ino);self.assertFalse((b/'runs').exists())
     if raw is not None:self.assertEqual(ledger.read_bytes(),raw)
    finally:
     if held:held.close()
 def test_actual_process_concurrent_O_EXCL_claim_only_one_owner(self):
  with tempfile.TemporaryDirectory()as t:
   path=Path(t)/'owner';ctx=multiprocessing.get_context('fork');ready=ctx.Event();release=ctx.Event();result=ctx.Queue();child=ctx.Process(target=contender,args=(str(path),ready,release,result));child.start()
   try:
    self.assertTrue(ready.wait(5));before=path.read_bytes()
    with self.assertRaises(FileExistsError):accounting.OwnedFile(path)
    self.assertEqual(path.read_bytes(),before)
   finally:release.set();child.join(5)
   self.assertEqual(child.exitcode,0);self.assertEqual(result.get(timeout=1),'owned');print(json.dumps({'actual_OS':'concurrent-child-O_EXCL','owners':1,'loser_preserves_winner':True}))
 def test_replaced_owner_inode_never_overwrites_foreign(self):
  with tempfile.TemporaryDirectory()as t:
   b=Path(t);p,args=setup(b)
   def changed():
    (b/'ledger.json').rename(b/'retained-owner');(b/'ledger.json').write_bytes(b'foreign replacement');return p
   code,calls=invoke(b,p,args,check=changed);self.assertEqual((code,calls),(1,[]));self.assertEqual((b/'ledger.json').read_bytes(),b'foreign replacement');self.assertFalse((b/'runs').exists());self.assertTrue((b/'retained-owner').exists())
 def test_real_unpersistable_initial_write_retains_one_shot_claim(self):
  with tempfile.TemporaryDirectory()as t:
   b=Path(t);p,args=setup(b);pid=os.fork()
   if pid==0:
    try:
     signal.signal(signal.SIGXFSZ,signal.SIG_IGN);resource.setrlimit(resource.RLIMIT_FSIZE,(0,0));captured=io.StringIO()
     with contextlib.redirect_stdout(captured):code,calls=invoke(b,p,args)
     receipt=json.loads(captured.getvalue().splitlines()[-1]);os._exit(0 if code==1 and calls==[]and(b/'ledger.json').exists()and receipt['error_code']=='HaltPersistenceFailed'and receipt['halt_durable']is False else 2)
    except BaseException:os._exit(3)
   _,status=os.waitpid(pid,0);self.assertEqual(os.waitstatus_to_exitcode(status),0);self.assertEqual((b/'ledger.json').stat().st_size,0)
   with self.assertRaises(frames.Refusal)as e:invoke(b,p,args)
   self.assertEqual(e.exception.code,'ExistingAccounting');self.assertFalse((b/'runs').exists());print(json.dumps({'actual_OS':'RLIMIT_FSIZE0','halt_durable':False,'retained_empty_claim':True,'restored_retry':'ExistingAccounting','configuration':0}))
 def test_public_report_failure_cannot_prevent_owned_halt(self):
  with tempfile.TemporaryDirectory()as t:
   b=Path(t);p,args=setup(b)
   def imported(name):
    out=b/'runs'/args.grant_id;out.chmod(0o500);raise frames.Refusal('SourceSetupFault','owned output made unwritable after prelaunch')
   try:
    with patch.object(oracle,'HERE',b),patch.object(oracle,'check',return_value=p),patch.object(oracle.importlib,'import_module',side_effect=imported):self.assertEqual(oracle.run(args),1)
    self.assertTrue(json.loads((b/'ledger.json').read_text())['halted'])
   finally:(b/'runs'/args.grant_id).chmod(0o700)
   with self.assertRaises(frames.Refusal):invoke(b,p,args)

class PhysicalLease(unittest.TestCase):
 def test_actual_flock_guest_held_audit_free_reacquire_before_next(self):
  for fault in [None,'audit','stop','export','master','busy']:
   with self.subTest(fault=fault),tempfile.TemporaryDirectory()as t:
    b=Path(t);p,args=setup(b);lock=b/'isolated-session1.lock';events=[];attempts=[];notices=io.StringIO();foreign=None
    @contextlib.contextmanager
    def lease(*a):
     with lock.open('a+')as held:
      fcntl.flock(held,fcntl.LOCK_EX|fcntl.LOCK_NB);events.append('acquire')
      try:yield
      finally:fcntl.flock(held,fcntl.LOCK_UN);events.append('release')
    def is_free():
     with lock.open('a+')as other:
      try:fcntl.flock(other,fcntl.LOCK_EX|fcntl.LOCK_NB);fcntl.flock(other,fcntl.LOCK_UN);return True
      except BlockingIOError:return False
    def attempt(session,qmp,guest,n,leaf,target,work,plan):
     self.assertFalse(is_free());events.append('guest');attempts.append(leaf['id'])
     if fault=='master':(b/'harddisk.img').write_bytes(b'wrong master')
     return {'id':leaf['id'],'case':leaf['case'],'repetition':leaf['repetition'],'outcome':'incomplete'if fault in ['stop','export']else 'complete-observation','guest_stopped':fault!='stop','normal_DOS':True,'exports_complete':fault!='export','stop_method':'QMP quit; own socket terminated'}
    def qualify(*a):
     self.assertTrue(is_free());self.assertIn('physical-guard-exited-before-offline-audit',notices.getvalue());events.append('audit')
     if fault=='audit':raise frames.Refusal('UnknownField','isolated first-audit failure')
     return {'prospective_branch':'uniform-H1-reload-counter-retained'}
    if fault=='busy':foreign=lock.open('a+');fcntl.flock(foreign,fcntl.LOCK_EX|fcntl.LOCK_NB)
    try:
     with contextlib.redirect_stdout(notices),patch.object(oracle,'prior_control',return_value=True),patch.object(oracle.families,'decision',return_value={'integrity_fixture_only':True}):code,calls=invoke(b,p,args,attempt=attempt,qualify=qualify,exclusive=lease)
    finally:
     if foreign:foreign.close()
    self.assertEqual(code,0 if fault is None else 1);self.assertEqual(len(attempts),8 if fault is None else 0 if fault=='busy'else 1);report=json.loads((b/'runs'/args.grant_id/'run.json').read_text());self.assertEqual(report['oracle_released'],fault not in ['stop','export','master','busy']);self.assertEqual(events,(['acquire','guest','release','audit']*8)if fault is None else ['acquire','guest','release','audit']if fault=='audit'else []if fault=='busy'else ['acquire','guest','release']);self.assertEqual(len(json.loads((b/'ledger.json').read_text())['attempts']),len(attempts));print(json.dumps({'actual_OS':'isolated-flock','fault':fault,'events':events,'attempts':len(attempts),'oracle_released':report['oracle_released']}))
if __name__=='__main__':unittest.main()
