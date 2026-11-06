"""R1/R2 actual host/public QMP/real OS boundaries. TEST-only documents are never run grants."""
from pathlib import Path
import copy,json,os,socket,subprocess,sys,tempfile,time,types,unittest
sys.dont_write_bytecode=True
import account,approved,host,oracle,stopping
from boundaries import Refusal,canonical
SERVER="""import json,os,socket,sys,time
path,mode=sys.argv[1:3]
s=socket.socket(socket.AF_UNIX);s.bind(path);s.listen(1)
try:
 c,_=s.accept();f=c.makefile('rwb');f.write(b'{"QMP":{"version":{},"capabilities":[]}}\\n');f.flush()
 assert json.loads(f.readline())=={'execute':'qmp_capabilities'};f.write(b'{"return":{}}\\n');f.flush()
 msg=json.loads(f.readline());assert msg=={'execute':'quit'}
 if mode=='reject':f.write(b'{"error":{"class":"GenericError","desc":"TEST rejected quit"}}\\n');f.flush()
 elif mode!='disconnect':f.write(b'{"return":{}}\\n');f.flush()
 if mode=='hold':time.sleep(10)
 f.close();c.close()
finally:s.close();os.unlink(path)
"""
def documents(root,packet):
 review=root/'review';grant=root/'grant';r=dict(verdict='READY',findings=[],independent=True,source_sha256=packet['source_sha256'],plan_sha256=packet['plan_sha256'],execution_contract_sha256=host.contract_sha(packet),reviewer='TEST ONLY isolated reviewer',reference='TEST ONLY NO ORIGINAL GRANT');review.write_text(json.dumps(r));g=dict(schema='wordling.wp55.root-grant/v2',execution_contract_sha256=host.contract_sha(packet),grant_id='wp55-entry-one-f1-v1',source_sha256=packet['source_sha256'],plan_sha256=packet['plan_sha256'],source_review_sha256=oracle.sha(review.read_bytes()),maximum_new_attempts_including_failures=4,ordered_attempt_ids=[x['id']for x in packet['plan']['leaves']],paths=packet['paths'],old51=dict(spent=1,incomplete=1,qualified=0,abandoned=7,permanently_halted=True),historical46=13,ROOT_logical_exclusive_reservation=True,source_prelaunch_approved=True,new_original_only=True,native_permission=False);grant.write_text(json.dumps(g));return dict(allow_vm=True,source_review=str(review),grant=str(grant))
class Binding(unittest.TestCase):
 def test_real_authorize_complete_packet_changes_refuse_old_documents(self):
  packet=host.prospective_packet()
  with tempfile.TemporaryDirectory()as t:
   args=documents(Path(t),packet);host.authorize(args,packet)
   mutations=[]
   for i in range(len(packet['tools'])):
    for field in ['path','sha256']:
     p=copy.deepcopy(packet);p['tools'][i][field]='changed';mutations.append(p)
   for field in ['profile_id','profile_sha256','master','paths','UI_source_facts','sources','plan','mode_authority','native_permission']:
    p=copy.deepcopy(packet);p[field]='changed';mutations.append(p)
   for p in mutations:
    for rehash in [False,True]:
     if rehash:p['execution_contract_sha256']=host.contract_sha(p)
     with self.subTest(rehash=rehash),self.assertRaises(Refusal):host.authorize(args,p)
 def test_actual_host_tool_check_after_authorize_sticky_before_NEXT(self):
  from contextlib import contextmanager
  packet=host.prospective_packet()
  with tempfile.TemporaryDirectory()as t:
   t=Path(t);tool=t/'tool';tool.write_bytes(b'reviewed');packet['tools']=[dict(path=str(tool),sha256=host.digest(tool))];packet['execution_contract_sha256']=host.contract_sha(packet);args=documents(t,packet);host.authorize(args,packet);batch=account.Batch(t/'accounting',packet['plan'],True);calls=[]
   @contextmanager
   def lease():yield
   def perform(leaf):calls.append(leaf['id']);return dict(id=leaf['id'],outcome='complete-observation',normal_DOS=True,stop_method=stopping.NORMAL,stop_proof=dict(gone_or_same_zombie=True),exports_complete=True,master_unchanged=True)
   def publish(rows,error):
    if error is None:tool.write_bytes(b'drift after first completed leaf')
   try:
    with self.assertRaises(Refusal)as e:account.drive(batch,lambda:None,lambda:host.validate_execution(packet),lease,perform,lambda a,b:None,publish)
    self.assertEqual(e.exception.code,'ToolDrift');self.assertEqual(len(calls),1);self.assertEqual(len(batch.snapshot()['attempts']),1);self.assertTrue(batch.snapshot()['halted'])
   finally:batch.close()
class QMPBoundary(unittest.TestCase):
 def worker(self,root,mode):
  runtime=root/'runtime';runtime.mkdir();work=root/'work';work.mkdir();sock=runtime/'qmp.sock';qmp=host._module('wp55_test_actual_public_qmp',host.ROOT/'scripts/reference/qmp.py');qmp.RUNTIME=runtime;qmp.SOCKET=sock
  args=[sys.executable,'-c',SERVER,str(sock),mode,str(work/'boot.img'),str(work/'harddisk.img'),'unix:'+str(sock)+',server'];p=subprocess.Popen(args,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);(runtime/'qemu.pid').write_text(str(p.pid));deadline=time.monotonic()+2
  while not sock.exists():self.assertIsNone(p.poll());self.assertLess(time.monotonic(),deadline);time.sleep(.01)
  guard=host._module('wp55_test_actual44_identity',host.ROOT/'internal/document/evidence/wp44/oracle.py');owned=guard.owned_identity(qmp,work,args);return p,qmp,guard,owned
 def cleanup(self,p):
  if p.poll()is None:p.terminate()
  p.wait(timeout=2)
 def test_valid_actual_public_transport_audited_before_export_gate(self):
  with tempfile.TemporaryDirectory()as t:
   t=Path(t);p,q,g,owned=self.worker(t,'valid')
   try:
    receipt=stopping.normal_quit(q,q.QMP,owned,g.same_identity,g.stopped,t/'stop-wire');row=dict(normal_DOS=True,guest_stopped=True,stop_method=stopping.NORMAL,quit_exchange=receipt.snapshot(),stop_proof=receipt.snapshot()['owned_stopped']);self.assertTrue(stopping.validate(receipt,row,owned));self.assertTrue((t/'stop-wire').exists());self.assertEqual(p.wait(timeout=2),0)
    with self.assertRaises(AttributeError):receipt.wire=b'forged'
    with self.assertRaises(Refusal):stopping.validate(receipt.snapshot(),row,owned)
    for changed in ['valid-shape-changed-raw','rehashed-row','public-wrapper-retarget','missing']:
     raw=(t/'stop-wire').read_bytes();bad=copy.deepcopy(row)
     if changed=='missing':(t/'stop-wire').unlink()
     else:
      records=[json.loads(line)for line in raw.splitlines()];records[0]['monotonic']+=.001;altered=b''.join(canonical(r)+b'\n'for r in records) # valid QMP semantics, changed actual provenance
      if changed=='public-wrapper-retarget':bad['quit_exchange']['path']='foreign'
      else:(t/'stop-wire').write_bytes(altered)
      if changed=='rehashed-row':bad['quit_exchange']['sha256']=oracle.sha(altered);bad['quit_exchange']['size']=len(altered)
     with self.subTest(changed=changed),self.assertRaises((Refusal,OSError)):stopping.validate(receipt,bad,owned)
     (t/'stop-wire').write_bytes(raw)
   finally:self.cleanup(p)
 def test_reject_disconnect_and_bounded_stop_failure_not_normal(self):
  for mode in ['reject','disconnect','hold']:
   with self.subTest(mode=mode),tempfile.TemporaryDirectory()as t:
    t=Path(t);p,q,g,owned=self.worker(t,mode)
    try:
     def observe(q,identity):return g.stopped(q,identity,timeout=.3)
     with self.assertRaises(Exception):stopping.normal_quit(q,q.QMP,owned,g.same_identity,observe,t/'stop-wire')
     self.assertTrue((t/'stop-wire').exists())
    finally:self.cleanup(p)
 def test_absent_refused_socket_and_natural_exit_no_issued_receipt(self):
  with tempfile.TemporaryDirectory()as t:
   t=Path(t);p,q,g,owned=self.worker(t,'valid')
   try:
    q.SOCKET.unlink()
    with self.assertRaises(Refusal):stopping.normal_quit(q,q.QMP,owned,g.same_identity,g.stopped,t/'stop-wire')
    self.assertFalse((t/'stop-wire').exists())
    refused=socket.socket(socket.AF_UNIX);refused.bind(str(q.SOCKET))
    try:
     with self.assertRaises(OSError):stopping.normal_quit(q,q.QMP,owned,g.same_identity,g.stopped,t/'stop-wire')
    finally:refused.close();q.SOCKET.unlink()
   finally:self.cleanup(p)
 def test_actual_execute_leaf_natural_startup_exit_cannot_claim_quit(self):
  with tempfile.TemporaryDirectory()as t:
   t=Path(t);runtime=t/'runtime';runtime.mkdir();masters=t/'masters';masters.mkdir();work=t/'work';q=types.SimpleNamespace(RUNTIME=runtime,SOCKET=runtime/'qmp.sock');worker=[None]
   for n in ['boot','harddisk']:(masters/(n+'.img')).write_bytes(b'TEST ONLY nonimage')
   class Guest:
    MASTER=masters
    def arguments(self,a,b):return [sys.executable,'-c','import time;time.sleep(.3)',str(a),str(b),'unix:'+str(q.SOCKET)+',server']
   class Session:
    def fresh_start(self,q,g,w,assets):w.mkdir();worker[0]=subprocess.Popen(g.arguments(w/'boot.img',w/'harddisk.img'),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);(runtime/'qemu.pid').write_text(str(worker[0].pid));raise RuntimeError('TEST startup fault')
   guard=host._module('wp55_test_real44_natural',host.ROOT/'internal/document/evidence/wp44/oracle.py');leaf=oracle.plan()['leaves'][0];leaf.update(private_work=str(work),installed_input_basename='I55IN');packet=dict(source_sha256='TEST ONLY',master={n:host.digest(masters/(n+'.img'))for n in ['boot','harddisk']})
   try:
    row=host.execute_leaf(packet,leaf,t/'public',lambda:None,(Session(),q,Guest(),guard,None));self.assertNotEqual(row['stop_method'],stopping.NORMAL);self.assertFalse(row['normal_DOS']);self.assertFalse(row['exports_complete']);self.assertNotIn('quit_exchange',row);self.assertFalse((t/'public/qmp-stop-wire.jsonl').exists());self.assertEqual(worker[0].wait(timeout=2),0)
   finally:
    if worker[0]is not None:self.cleanup(worker[0])
if __name__=='__main__':unittest.main()
