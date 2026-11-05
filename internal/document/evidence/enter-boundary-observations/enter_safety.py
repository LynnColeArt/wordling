"""Harmless OS backend composes actual approved coordinator and launch accounting.
No function can launch QEMU or acquire the reference guard/ledger. This is a
component challenge of NEW telemetry, not an enabled original protocol.
"""
from pathlib import Path
from contextlib import contextmanager
import copy,fcntl,hashlib,importlib.util,json,os,sys,tempfile,threading,time
from enter_sources import B,ROOT,HERE,interfaces,sha,verify
class Telemetry:
 def __init__(self,path,plan,owner):
  B.require(owner.snapshot()['plan_sha256']==sha(B.canonical(plan)),'TelemetryPlanBinding','complete public batch plan/source context before creating launch record')
  self._owner=owner;self._path=Path(path);self._file=interfaces()['OwnedFile'](path);self._plan=copy.deepcopy(plan);self._row=dict(schema='wordling.wp57.harmless-launch-accounting/v1',plan_sha256=sha(B.canonical(plan)),kind='TEST_ONLY_NOT_ORIGINAL_AUTHORITY',attempts=[]);self._write()
 def _write(self):self._file.write(self._row)
 def begin(self,leaf):
  B.require(self._owner.snapshot()['attempts'][-1]['id']==leaf['id'],'TicketBinding','charged public batch snapshot before telemetry');B.require(len(self._row['attempts'])<4 and leaf['id']==self._plan['leaves'][len(self._row['attempts'])]['id'],'TelemetryOrder','exact whole4');self._row['attempts'].append(dict(id=leaf['id'],stage='not-attempted',identity=None));self._write()
 def unknown(self):
  B.require(self._row['attempts'][-1]['stage']=='not-attempted','LaunchStage','one fallible launch boundary');self._row['attempts'][-1]['stage']='launch-unknown';self._write()
 def proved(self,identity,check):
  check(identity);B.require(self._row['attempts'][-1]['stage']=='launch-unknown','LaunchStage','proof only after unknown boundary');self._row['attempts'][-1].update(stage='positively-proved',identity=copy.deepcopy(identity));self._write()
 def snapshot(self):
  self._file.verify();B.require(B.canonical(B.parse(B.read(self._path)))==B.canonical(self._row),'TelemetryBytesDrift','actual durable launch record differs; no rehashed stage/PID promotion');return copy.deepcopy(self._row)
 def close(self):self._file.close()
def counts(batch,telemetry):
 ledger=batch.snapshot();record=telemetry.snapshot();B.require(ledger['plan_sha256']==record['plan_sha256'],'AccountingPlanDisagreement','complete captured plan binding');ids=[r['id']for r in ledger['attempts']];rows=record['attempts'];B.require([r['id']for r in rows]==ids[:len(rows)]and len(rows)<=len(ids),'AccountingDisagreement','durable ticket/launch identities must agree');stages=[r['stage']for r in rows];return dict(tickets_spent=len(ids),positively_proved=stages.count('positively-proved'),launch_unknown=stages.count('launch-unknown'),not_attempted=stages.count('not-attempted')+len(ids)-len(rows),incomplete=sum(r['outcome']=='incomplete'for r in ledger['attempts']),abandoned=ledger.get('remaining_abandoned',0))
def guard():
 path=ROOT/'internal/document/evidence/wp44/oracle.py';spec=importlib.util.spec_from_file_location('wp57_approved44_identity',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def os_child(work,mode,telemetry):
 """A real owned Python process, never a guest. Source is our fixed fixture only."""
 runtime=work/'runtime';runtime.mkdir();socket=runtime/'qmp.sock';argv=[sys.executable,'-B',str(HERE/'fixture_child.py'),str(runtime/'qemu.pid'),str(work/'boot.img'),str(work/'harddisk.img'),'unix:'+str(socket)+',',mode];receipt=[];result={}
 def worker():
  try:out,err=B.process(argv,ROOT,timeout=.45,stdout_limit=1024,stderr_limit=1024,receipts=receipt);result.update(stdout=out.hex(),stderr=err.hex())
  except BaseException as e:result.update(error=getattr(e,'code',type(e).__name__),detail=str(e))
 telemetry.unknown();t=threading.Thread(target=worker);t.start();deadline=time.monotonic()+2
 try:
  while not(runtime/'qemu.pid').exists()and t.is_alive():B.require(time.monotonic()<deadline,'FixtureStartupDeadline','owned local fixture');time.sleep(.005)
  if mode=='proved':
   q=type('FixturePaths',(),dict(RUNTIME=runtime,SOCKET=socket));g=guard();identity=g.owned_identity(q,work,argv);telemetry.proved(identity,g.same_identity)
  # mode unknown models exception AFTER actual OS launch but BEFORE usable identity.
 finally:t.join(timeout=3);B.require(not t.is_alive(),'PendingFixtureWorker','all owned workers settle before snapshot')
 B.require(receipt and all(r['pgid']==r['pid']==r['session']for r in receipt),'FixtureCleanup','positive private-group signal receipts');return dict(argv=argv,cleanup=receipt,worker=result,fixture_pid=int((runtime/'qemu.pid').read_text()),original_guest=False,pid_absent=not Path('/proc',str(int((runtime/'qemu.pid').read_text()))).exists())

def simulate(plan,fault):
 B.require(fault in {'setup','unknown','proved','audit','success','publish','halt-persistence'},'FixtureSelector','closed harmless OS faults');mods=interfaces();account=mods['account'];rows=[];capture={};error=None
 with tempfile.TemporaryDirectory(prefix='wordling-wp57-harmless-')as temp:
  root=Path(temp);batch=account.Batch(root/'tickets.json',plan,True);telemetry=Telemetry(root/'launches.json',plan,batch);lock=root/'physical.lock';lock.touch();checks=[]
  def source():verify();telemetry._file.verify() # our owned capability, no private Batch access.
  def setup():
   if fault=='halt-persistence':
    (root/'tickets.json').rename(root/'retained-owned-tickets.json');(root/'tickets.json').write_text('FOREIGN-REPLACEMENT-MUST-NOT-BE-WRITTEN');raise B.Refusal('FixtureSetupFault','retarget owned TEST ledger to exercise real halt-persistence refusal')
   if fault=='setup':raise B.Refusal('FixtureSetupFault','charged BEFORE fallible setup; no launch')
  @contextmanager
  def physical():
   with lock.open('r')as f:fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB);yield
  def perform(leaf):
   telemetry.begin(leaf);work=root/leaf['id'];work.mkdir();mode='proved'if fault in {'proved','success','audit','publish'}else'unknown';child=os_child(work,mode,telemetry);capture[leaf['id']]=child
   if fault in {'unknown','proved'}:return dict(id=leaf['id'],outcome='incomplete',normal_DOS=False,exports_complete=False,master_unchanged=False,error='FIXTURE failure after OS launch',original_guest=False)
   # TEST backend only: synthetic boundary conditions drive the REAL coordinator;
   # these flags never pass an original-run/quit/export authority boundary.
   return dict(id=leaf['id'],outcome='complete-observation',normal_DOS=True,stop_method='QMP quit; own socket terminated',stop_proof=dict(gone_or_same_zombie=True),exports_complete=True,master_unchanged=True,original_guest=False)
  def audit(row,prior):
   source()
   with lock.open('r')as f:fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB);checks.append(dict(physical_free_during_audit=True,same_telemetry_owner_retained=True,ROOT_logical_release_claimed=False))
   if fault=='audit':raise B.Refusal('FixtureAuditFault','no NEXT after failed audit')
  def publish(current,failure):
   if fault=='publish'and failure is None:raise B.Refusal('FixturePublishFault','no NEXT after publication failure')
   rows[:]=copy.deepcopy(current)
  try:account.drive(batch,setup,source,physical,perform,audit,publish)
  except BaseException as e:error=dict(code=getattr(e,'code',type(e).__name__),detail=str(e))
  try:
   result=dict(schema='wordling.wp57.harmless-OS-proof/v1',fixture_only=True,actual_original_launched=0,original_qualification=False,error=error,counts=counts(batch,telemetry),ticket_ledger=batch.snapshot(),launch_ledger=telemetry.snapshot(),OS_processes=capture,audit_checks=checks,logical_reservation='NO ROOT reservation acquired/released; same test owner held',test_backend_boundary_flags_are_not_original_proofs=True,foreign_test_ledger_unchanged=(root/'tickets.json').read_text()=='FOREIGN-REPLACEMENT-MUST-NOT-BE-WRITTEN'if fault=='halt-persistence'else None)
  finally:telemetry.close();batch.close()
 return result
