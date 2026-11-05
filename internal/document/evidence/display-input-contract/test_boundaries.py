"""Actual owned process-group and bounded IO behavior, no reference guest."""
from pathlib import Path
import ctypes,errno,json,os,signal,sys,tempfile,time,unittest
from boundaries import process,Refusal,read,parse
class Boundaries(unittest.TestCase):
 def test_regular_symlink_FIFO_and_growth_limits(self):
  with tempfile.TemporaryDirectory()as d:
   p=Path(d)/'x';p.write_bytes(b'abc');self.assertEqual(read(p,3),b'abc')
   with self.assertRaises(Refusal):read(p,2)
   s=Path(d)/'s';s.symlink_to(p)
   with self.assertRaises(Refusal):read(s,3)
   p.unlink();os.mkfifo(p)
   with self.assertRaises(Refusal):read(p,3)
 def test_strict_JSON(self):
  for raw in [b'{"x":1,"x":2}',b'NaN',b'{',b'['*50+b'0'+b']'*50]:
   with self.subTest(raw=raw[:20]),self.assertRaises(Refusal):parse(raw)
 def test_real_nonzero_and_start_failure(self):
  with self.assertRaisesRegex(Refusal,'exit=3'):process([sys.executable,'-c','import sys;sys.exit(3)'],Path.cwd())
  with self.assertRaises(FileNotFoundError):process(['/absent-wp56-command'],Path.cwd())
 def owned_descendant(self,shape,limit=False):
  # TEST ONLY: adopt/reap direct descendants after process-group termination.
  libc=ctypes.CDLL(None,use_errno=True);self.assertEqual(libc.prctl(36,1,0,0,0),0)
  try:
   with tempfile.TemporaryDirectory()as d:
    pin=Path(d)/'identity.json'
    script="""import json,os,sys,time
pid=os.fork()
if pid:
 open(sys.argv[1],'w').write(json.dumps(dict(leader=os.getpid(),child=pid,pgid=os.getpgrp(),argv=sys.argv)))
 if sys.argv[2]=='alive':time.sleep(20)
 os._exit(0)
if sys.argv[2]=='closed':os.close(1);os.close(2)
if sys.argv[2]=='limit':os.write(1,b'x'*20000)
time.sleep(20)
"""
    start=time.monotonic()
    if shape=='closed':process([sys.executable,'-c',script,str(pin),shape],Path.cwd(),timeout=.4)
    else:
     with self.assertRaises(Refusal)as e:process([sys.executable,'-c',script,str(pin),shape],Path.cwd(),timeout=.4,stdout_limit=1000 if limit else 1<<20)
     self.assertEqual(e.exception.code,'ProcessOutputLimit'if limit else'ProcessDeadline')
    self.assertLess(time.monotonic()-start,3);identity=json.loads(pin.read_text());self.assertEqual(identity['leader'],identity['pgid']);self.assertEqual(identity['argv'][-1],shape)
    deadline=time.monotonic()+2
    while True:
     pid,status=os.waitpid(identity['child'],os.WNOHANG)
     if pid:break
     self.assertLess(time.monotonic(),deadline);time.sleep(.01)
    self.assertTrue(os.WIFSIGNALED(status));self.assertIn(os.WTERMSIG(status),[signal.SIGTERM,signal.SIGKILL])
    with self.assertRaises(ProcessLookupError):os.kill(identity['child'],0)
    with self.assertRaises(ChildProcessError):os.waitpid(identity['leader'],os.WNOHANG)
  finally:self.assertEqual(libc.prctl(36,0,0,0,0),0)
 def test_leader_alive_deadline_group_cleanup(self):self.owned_descendant('alive')
 def test_leader_already_exited_inherited_stdout_cleanup(self):self.owned_descendant('open')
 def test_successful_leader_closed_pipes_still_group_cleanup(self):self.owned_descendant('closed')
 def test_output_limit_group_cleanup(self):self.owned_descendant('limit',True)
 def test_actual_cleanup_failure_is_not_success(self):
  # Inject only the kernel permission failure; direct child still reaped by test cleanup.
  from unittest.mock import patch
  real=os.killpg
  def fail(pgid,sig):
   if sig==signal.SIGTERM:real(pgid,signal.SIGKILL);raise PermissionError(errno.EPERM,'test cleanup failure')
   return real(pgid,sig)
  with patch('boundaries.os.killpg',side_effect=fail),self.assertRaises(Refusal)as e:process([sys.executable,'-c','pass'],Path.cwd())
  self.assertEqual(e.exception.code,'CleanupFailure')
if __name__=='__main__':unittest.main(verbosity=2)
