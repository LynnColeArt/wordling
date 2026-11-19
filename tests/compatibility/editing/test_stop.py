import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'scripts/reference'))
import wordling_edits as w
class Clock:
 def __init__(self):self.t=0
 def now(self):return self.t
 def sleep(self,n):self.t+=n
class Socket:
 def __init__(self):self.present=True
 def exists(self):return self.present
class Stop(unittest.TestCase):
 owned={'pid':123,'start_ticks':456,'argv_hex':'71756d7500'}
 def poll(self,states,sockets,timeout=.2):
  clock=Clock();socket=Socket();i=iter(zip(states,sockets));last=None
  def read(pid):
   nonlocal last
   try:last=next(i)
   except StopIteration:pass
   state,present=last;socket.present=present
   return None if state is None else self.owned|{'state':state}
  return w.wait_owned_stop(self.owned,socket,timeout,read,clock.now,clock.sleep)
 def test_qmp_returns_before_process_exit(self):
  result=self.poll(['S','R','Z'],[False,False,False]);self.assertEqual(len(result['observations']),3);self.assertTrue(result['confirmed'])
 def test_process_absent_but_socket_not_yet_gone(self):
  self.assertEqual(len(self.poll([None,None],[True,False])['observations']),2)
 def test_deadline_no_extraction_authority(self):
  with self.assertRaisesRegex(w.Failure,'StopDeadline'):self.poll(['S'],[False])
 def test_reuse_not_stop(self):
  clock=Clock();socket=Socket();socket.present=False
  with self.assertRaisesRegex(w.Failure,'PIDIdentityChanged'):w.wait_owned_stop(self.owned,socket,.2,lambda pid:self.owned|{'state':'S','start_ticks':457},clock.now,clock.sleep)
 def test_zombie_empty_proc_cmdline_keeps_captured_identity(self):
  socket=Socket();socket.present=False
  result=w.wait_owned_stop(self.owned,socket,.2,lambda pid:self.owned|{'state':'Z','argv_hex':''})
  self.assertTrue(result['confirmed'])
 def test_missing_pid_socket_absence_insufficient(self):
  socket=Socket();socket.present=False
  with self.assertRaisesRegex(w.Failure,'MissingOwnedPID'):w.wait_owned_stop({},socket,.2)
 def test_zombie_requires_socket_absent(self):
  with self.assertRaisesRegex(w.Failure,'StopDeadline'):self.poll(['Z'],[True])
if __name__=='__main__':unittest.main()
