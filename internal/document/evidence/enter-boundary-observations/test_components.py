"""Actual reusable process/owned-file boundaries and NEW telemetry ownership."""
from pathlib import Path
import ctypes,json,os,signal,sys,tempfile,time,unittest
from enter_sources import B,HERE,ROOT,interfaces
from enter_safety import Telemetry,counts
from enter_oracle import plan
class Components(unittest.TestCase):
 def test_alias_does_not_promote_or_retarget_telemetry(self):
  with tempfile.TemporaryDirectory()as d:
   m=interfaces();batch=m['account'].Batch(Path(d)/'tickets',plan(),True);t=Telemetry(Path(d)/'launches',plan(),batch)
   try:
    batch.begin(plan()['leaves'][0]['id']);t.begin(plan()['leaves'][0]);t.unknown();s=t.snapshot();s['attempts'][0].update(stage='positively-proved',identity={'pid':1});self.assertEqual(counts(batch,t)['launch_unknown'],1);self.assertEqual(counts(batch,t)['positively_proved'],0)
    with self.assertRaises(ValueError):m['account'].Batch(Path(d)/'tickets',plan(),True)
   finally:t.close();batch.close()
 def test_no_authorization_opens_no_test_ledger(self):
  with tempfile.TemporaryDirectory()as d:
   p=Path(d)/'ledger'
   with self.assertRaises(ValueError):interfaces()['account'].Batch(p,plan(),False)
   self.assertFalse(p.exists())
 def test_real_telemetry_retarget_refuses_foreign_write(self):
  with tempfile.TemporaryDirectory()as d:
   root=Path(d);m=interfaces();b=m['account'].Batch(root/'tickets',plan(),True);t=Telemetry(root/'launches',plan(),b);b.begin(plan()['leaves'][0]['id']);t.begin(plan()['leaves'][0]);(root/'launches').rename(root/'old');(root/'launches').write_bytes(b'foreign')
   try:
    with self.assertRaises(ValueError):t.unknown()
    self.assertEqual((root/'launches').read_bytes(),b'foreign')
   finally:t.close();b.close()
 def test_closed_pipe_orphan_and_TERM_ignore_reaped(self):
  libc=ctypes.CDLL(None);self.assertEqual(libc.prctl(36,1,0,0,0),0)
  try:
   for closed in [True,False]:
    with tempfile.TemporaryDirectory()as d:
     pin=Path(d)/'pin';script="import os,signal,sys,time\np=os.fork()\nif p:\n open(sys.argv[1],'w').write(str(p));os._exit(0)\nsignal.signal(signal.SIGTERM,signal.SIG_IGN)\nif sys.argv[2]=='closed':os.close(1);os.close(2)\ntime.sleep(20)";receipts=[];start=time.monotonic()
     if closed:B.process([sys.executable,'-c',script,str(pin),'closed'],ROOT,timeout=.3,receipts=receipts)
     else:
      with self.assertRaises(ValueError):B.process([sys.executable,'-c',script,str(pin),'open'],ROOT,timeout=.3,receipts=receipts)
     child=int(pin.read_text());deadline=time.monotonic()+2
     while True:
      pid,status=os.waitpid(child,os.WNOHANG)
      if pid:break
      self.assertLess(time.monotonic(),deadline);time.sleep(.01)
     self.assertTrue(os.WIFSIGNALED(status));self.assertEqual(os.WTERMSIG(status),signal.SIGKILL);self.assertLess(time.monotonic()-start,3);self.assertTrue(all(r['leader_unreaped']and r['pgid']==r['session']==r['pid']for r in receipts))
  finally:libc.prctl(36,0,0,0,0)
 def test_actual_output_deadline_start_nonzero_bounds(self):
  for args,kwargs in [([sys.executable,'-c','print("x"*2000)'],dict(stdout_limit=10)),([sys.executable,'-c','import time;time.sleep(20)'],dict(timeout=.1)),(['/absent-wp57-command'],{}),([sys.executable,'-c','raise SystemExit(4)'],{})]:
   with self.subTest(args=args),self.assertRaises(ValueError):B.process(args,ROOT,**kwargs)
 def test_actual_import_collision_is_refused_not_patched(self):
  code="import sys,types;sys.modules['boundaries']=types.SimpleNamespace(__file__='/wrong/module.py');import enter_sources";out,err,status=B.process([sys.executable,'-B','-c',code],HERE,check=False);self.assertNotEqual(status,0);self.assertIn(b'ImportCollision: boundaries',err)
 def test_same_inode_rehashed_telemetry_cannot_promote_launch(self):
  with tempfile.TemporaryDirectory()as d:
   root=Path(d);b=interfaces()['account'].Batch(root/'tickets',plan(),True);t=Telemetry(root/'launches',plan(),b);b.begin(plan()['leaves'][0]['id']);t.begin(plan()['leaves'][0]);t.unknown();r=t.snapshot();r['attempts'][0].update(stage='positively-proved',identity={'pid':1});(root/'launches').write_text(json.dumps(r))
   try:
    with self.assertRaisesRegex(ValueError,'durable launch record'):t.snapshot()
   finally:t.close();b.close()
 def test_different_plan_same_leaf_IDs_refused_before_file_creation(self):
  import copy
  with tempfile.TemporaryDirectory()as d:
   root=Path(d);b=interfaces()['account'].Batch(root/'tickets',plan(),True);p=copy.deepcopy(plan());p['leaves'][0]['initial_text']='different'
   try:
    with self.assertRaisesRegex(ValueError,'complete public batch plan'):Telemetry(root/'launches',p,b)
    self.assertFalse((root/'launches').exists())
   finally:b.close()
if __name__=='__main__':unittest.main(verbosity=2)
