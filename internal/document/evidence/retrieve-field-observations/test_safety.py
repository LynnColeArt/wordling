"""Real local OS tests; no guest, physical reference guard or private ledger."""
from pathlib import Path
import copy,ctypes,fcntl,json,os,signal,subprocess,sys,tempfile,time,unittest
sys.dont_write_bytecode=True
import account,oracle
from boundaries import Refusal,process,atomic_report
class Safety(unittest.TestCase):
 def test_audit_free_flock_same_owner_all_four(self):
  with tempfile.TemporaryDirectory(prefix='wp55-account-test-')as tmp:
   tmp=Path(tmp);lock=tmp/'physical.lock';batch=account.Batch(tmp/'batch.json',oracle.plan(),True);identity=(batch._owner.identity.st_dev,batch._owner.identity.st_ino)
   try:
    for leaf in oracle.plan()['leaves']:
     ticket=batch.begin(leaf['id'])
     with lock.open('a')as physical:
      fcntl.flock(physical,fcntl.LOCK_EX|fcntl.LOCK_NB);batch.physical_enter(ticket)
     batch.physical_release(ticket,dict(normal_DOS=True,owned_normal_stop=True,gone_same_identity=True,exports_complete=True,master_unchanged=True))
     def audit():
      # Actual second process obtains physical flock while original exact batch descriptor remains held.
      code="import fcntl,sys; f=open(sys.argv[1],'a'); fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB); print('audit-physical-free')"
      out,_=process([sys.executable,'-c',code,str(lock)],tmp);self.assertEqual(out,b'audit-physical-free\n');self.assertEqual((batch._owner.identity.st_dev,batch._owner.identity.st_ino),identity)
      with self.assertRaises(Refusal):account.Batch(tmp/'batch.json',oracle.plan(),True)
     batch.audit(ticket,lambda:None,audit)
    self.assertEqual(len(batch.snapshot()['attempts']),4);self.assertFalse(batch.snapshot()['ROOT_logical_reservation_released'])
   finally:batch.close()
   with self.assertRaises(Refusal):account.Batch(tmp/'batch.json',oracle.plan(),True)
 def test_unauthorized_zero_touch_setup_fault_is_spent_and_sticky(self):
  with tempfile.TemporaryDirectory()as tmp:
   p=Path(tmp)/'batch.json'
   with self.assertRaises(Refusal):account.Batch(p,oracle.plan())
   self.assertFalse(p.exists());batch=account.Batch(p,oracle.plan(),True)
   try:
    batch.begin(oracle.plan()['leaves'][0]['id']);error=Refusal('SetupSourceFailure','no launches');batch.halt(error)
    with self.assertRaises(Refusal):batch.begin(oracle.plan()['leaves'][1]['id'])
    data=json.loads(p.read_text());self.assertTrue(data['halted']);self.assertEqual(len(data['attempts']),1);self.assertEqual(data['remaining_abandoned'],3)
   finally:batch.close()
 def test_unknown_stop_no_qualified_release_or_audit(self):
  with tempfile.TemporaryDirectory()as tmp:
   batch=account.Batch(Path(tmp)/'batch.json',oracle.plan(),True)
   try:
    t=batch.begin(oracle.plan()['leaves'][0]['id']);batch.physical_enter(t)
    with self.assertRaises(Refusal):batch.physical_release(t,dict(normal_DOS=False,owned_normal_stop=False,gone_same_identity=True,exports_complete=False,master_unchanged=True))
    with self.assertRaises(Refusal):batch.audit(t,lambda:None,lambda:self.fail('unsafe audit'))
    batch.halt(Refusal('UnsafeRelease','unknown'))
   finally:batch.close()
 def test_stale_ticket_retarget_and_foreign_ledger_preserved(self):
  with tempfile.TemporaryDirectory()as tmp:
   p=Path(tmp)/'batch.json';batch=account.Batch(p,oracle.plan(),True)
   try:
    t=batch.begin(oracle.plan()['leaves'][0]['id'])
    with self.assertRaises(Refusal):batch.physical_enter(object())
    saved=p.with_name('original.json');p.rename(saved);p.write_bytes(b'FOREIGN')
    with self.assertRaises(Exception):batch.begin(oracle.plan()['leaves'][1]['id'])
    self.assertEqual(p.read_bytes(),b'FOREIGN')
   finally:batch.close()
 def test_halt_persistence_failure_remains_one_shot_across_process(self):
  with tempfile.TemporaryDirectory()as tmp:
   p=Path(tmp)/'batch.json';batch=account.Batch(p,oracle.plan(),True)
   try:
    batch.begin(oracle.plan()['leaves'][0]['id']);fd=batch._owner.fd;os.close(fd);batch._owner.fd=None
    with self.assertRaises(Refusal)as e:batch.halt(Refusal('Fault','injected owned descriptor close'))
    self.assertEqual(e.exception.code,'HaltPersistenceFailed')
    code="import account,oracle,sys; account.Batch(sys.argv[1],oracle.plan(),True)"
    with self.assertRaises(Refusal):process([sys.executable,'-c',code,str(p)],Path(__file__).parent)
   finally:batch.close()
 def test_atomic_prior_report_and_foreign_symlink(self):
  with tempfile.TemporaryDirectory()as tmp:
   p=Path(tmp)/'prior';p.write_bytes(b'PRIOR');link=Path(tmp)/'link';link.symlink_to(p)
   with self.assertRaises(Refusal):atomic_report(link,b'NEW')
   self.assertEqual(p.read_bytes(),b'PRIOR')
 def test_leader_exit_or_alive_timeout_and_outputcap_no_orphan(self):
  # TEST ONLY subreaper: adopt/reap our known descendant PID, no production procscan/subreaper.
  libc=ctypes.CDLL(None,use_errno=True);self.assertEqual(libc.prctl(36,1,0,0,0),0);known=[]
  try:
   for leader_exit,output in [(True,False),(False,False),(True,True)]:
    with self.subTest(leader_exit=leader_exit,output=output),tempfile.TemporaryDirectory()as tmp:
     child="import signal,time,os; signal.signal(signal.SIGTERM,signal.SIG_IGN); "+("os.write(1,b'x'*65536); "if output else'')+"time.sleep(20)"
     parent="import subprocess,sys,time,json,os; p=subprocess.Popen([sys.executable,'-c',sys.argv[2]]); open(sys.argv[1],'w').write(str(p.pid)); "+("sys.exit(0)"if leader_exit else'time.sleep(20)')
     pidfile=Path(tmp)/'child';receipts=[];start=time.monotonic()
     with self.assertRaises(Refusal):process([sys.executable,'-c',parent,str(pidfile),child],tmp,timeout=.3,stdout_limit=100,receipts=receipts)
     self.assertLess(time.monotonic()-start,3);pid=int(pidfile.read_text());known.append((pid,(Path('/proc')/str(pid)/'stat').read_text().split(') ',1)[1].split()[19]));deadline=time.monotonic()+1
     while True:
      got,status=os.waitpid(pid,os.WNOHANG)
      if got:break
      self.assertLess(time.monotonic(),deadline);time.sleep(.01)
     self.assertEqual(got,pid);self.assertFalse(Path('/proc',str(pid)).exists());self.assertEqual([r['signal']for r in receipts],['TERM','KILL']);self.assertTrue(all(r['leader_unreaped']and r['pid']==r['pgid']==r['session']for r in receipts))
  finally:
   for pid,ticks in known:
    path=Path('/proc')/str(pid)/'stat'
    if path.exists()and path.read_text().split(') ',1)[1].split()[19]==ticks:
     os.kill(pid,signal.SIGKILL)
     try:os.waitpid(pid,0)
     except ChildProcessError:pass
   self.assertEqual(libc.prctl(36,0,0,0,0),0)
 def test_successful_leader_closed_pipes_descendant_is_gone(self):
  libc=ctypes.CDLL(None,use_errno=True);self.assertEqual(libc.prctl(36,1,0,0,0),0);pid=None
  try:
   with tempfile.TemporaryDirectory()as t:
    p=Path(t)/'child';code="import subprocess,sys; p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(20)'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);open(sys.argv[1],'w').write(str(p.pid))";receipts=[]
    out,err=process([sys.executable,'-c',code,str(p)],t,timeout=1,receipts=receipts);pid=int(p.read_text());self.assertEqual(out,b'');deadline=time.monotonic()+1
    while True:
     got,status=os.waitpid(pid,os.WNOHANG)
     if got:break
     self.assertLess(time.monotonic(),deadline);time.sleep(.01)
    self.assertEqual(got,pid);self.assertFalse(Path('/proc',str(pid)).exists());self.assertEqual([r['signal']for r in receipts],['TERM','KILL'])
  finally:
   if pid is not None and Path('/proc',str(pid)).exists():
    os.kill(pid,signal.SIGKILL)
    try:os.waitpid(pid,0)
    except ChildProcessError:pass
   self.assertEqual(libc.prctl(36,0,0,0,0),0)
 def test_foreign_process_group_never_signalled(self):
  from boundaries import _cleanup
  p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(10)'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  try:
   receipts=[]
   with self.assertRaises(Refusal)as e:_cleanup(p,receipts)
   self.assertEqual(e.exception.code,'CleanupOwnershipLost');self.assertEqual(receipts,[]);self.assertIsNone(p.poll())
  finally:p.terminate();p.wait(timeout=2);p.stdout.close();p.stderr.close()
 def test_startup_wait_failure_stops_only_captured_owned_worker(self):
  import host,types
  with tempfile.TemporaryDirectory()as tmp:
   tmp=Path(tmp);work=tmp/'work';runtime=tmp/'runtime';runtime.mkdir();masters=tmp/'master';masters.mkdir()
   for name in ['boot','harddisk']:(masters/(name+'.img')).write_bytes(b'test-only-not-a-native-image')
   qmp=types.SimpleNamespace(RUNTIME=runtime,SOCKET=runtime/'qmp.sock');worker=[None];stopcalls=[]
   class Guest:
    MASTER=masters
    def arguments(self,boot,disk):return [sys.executable,'-c','import time;time.sleep(20)',str(boot),str(disk),'unix:'+str(qmp.SOCKET)+',server']
    def stop(self):stopcalls.append('test-only-stop');worker[0].terminate()
   guest=Guest()
   class Session:
    def fresh_start(self,q,g,w,assets):
     w.mkdir();worker[0]=subprocess.Popen(g.arguments(w/'boot.img',w/'harddisk.img'),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);(q.RUNTIME/'qemu.pid').write_text(str(worker[0].pid));raise Refusal('StartupWaitFailure','harmless realOS leader launched before source helper returns')
   guard=host._module('wp55_test_actual44_stop',host.ROOT/'internal/document/evidence/wp44/oracle.py');packet=dict(source_sha256='test-only',master={name:host.digest(masters/(name+'.img'))for name in ['boot','harddisk']});leaf=oracle.plan()['leaves'][0];leaf.update(private_work=str(work),installed_input_basename='I55IN')
   try:
    row=host.execute_leaf(packet,leaf,tmp/'public',lambda:None,(Session(),qmp,guest,guard,None));self.assertEqual(stopcalls,[]);self.assertNotEqual(row['stop_method'],'QMP quit; own socket terminated');self.assertTrue(row['guest_stopped']);self.assertFalse(row['normal_DOS']);self.assertFalse(row['exports_complete']);self.assertEqual(row['error_code'],'StartupWaitFailure');self.assertFalse((tmp/'public/I55SV.WP5').exists())
   finally:
    if worker[0]is not None:
     if worker[0].poll()is None:worker[0].terminate()
     worker[0].wait(timeout=2)
 def test_process_nonzero_and_timeout_closed_pipes(self):
  with self.assertRaises(Refusal):process([sys.executable,'-c','raise SystemExit(7)'],Path(__file__).parent)
  with self.assertRaises(Refusal):process([sys.executable,'-c','import os,time;os.close(1);os.close(2);time.sleep(20)'],Path(__file__).parent,timeout=.15)
class DriverOrder(unittest.TestCase):
 def test_real_shared_coordinator_fault_order_and_sticky_NEXt(self):
  from contextlib import contextmanager
  for failure in ['none','setup','source-before-NEXT','unknown-stop','audit','publish']:
   with self.subTest(failure=failure),tempfile.TemporaryDirectory()as tmp:
    tmp=Path(tmp);batch=account.Batch(tmp/'batch.json',oracle.plan(),True);events=[];held=[False];done=[0];published=[0]
    def setup():
     events.append('setup')
     if failure=='setup':raise Refusal('Setup','first authorized error0 launches')
    def source():
     events.append('source')
     if failure=='source-before-NEXT'and published[0]>=1:raise Refusal('SourceDrift','after first audit BEFORE NEXT')
    @contextmanager
    def physical():
     with (tmp/'physical').open('a')as f:
      fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB);held[0]=True;events.append('physical-enter')
      try:yield
      finally:held[0]=False;events.append('physical-release')
    def perform(leaf):
     self.assertTrue(held[0]);events.append('perform');process([sys.executable,'-c',"print('harmless-owned-OS-worker')"],tmp)
     return dict(id=leaf['id'],outcome='complete-observation',normal_DOS=failure!='unknown-stop',stop_method='QMP quit; own socket terminated',stop_proof=dict(gone_or_same_zombie=True),exports_complete=True,master_unchanged=True)
    def audit(row,rows):
     self.assertFalse(held[0]);self.assertEqual(events[-1],'physical-release');events.append('audit');batch._owner.verify()
     with (tmp/'physical').open('a')as f:fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
     if failure=='audit':raise Refusal('Audit','after physical release')
     done[0]+=1
    def publish(rows,error):
     events.append('publish')
     if error is None:published[0]+=1
     if failure=='publish'and error is None:raise Refusal('Publish','real coordinator publication fault')
     (tmp/'public.json').write_text(json.dumps(dict(rows=rows,error=str(error))))
    try:
     if failure=='none':self.assertEqual(len(account.drive(batch,setup,source,physical,perform,audit,publish)),4)
     else:
      with self.assertRaises(Refusal):account.drive(batch,setup,source,physical,perform,audit,publish)
      self.assertTrue(batch.snapshot()['halted']);self.assertEqual(len(batch.snapshot()['attempts']),1)
      self.assertLessEqual(events.count('perform'),1)
      if failure=='unknown-stop':self.assertNotIn('audit',events)
      if failure=='setup':self.assertNotIn('physical-enter',events)
      with self.assertRaises(Refusal):batch.begin(oracle.plan()['leaves'][1]['id'])
    finally:batch.close()
if __name__=='__main__':unittest.main()
