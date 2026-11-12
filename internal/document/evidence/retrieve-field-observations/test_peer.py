"""Real kernel peer PID, actual approved QMP and44 ownership; no guest or grants."""
from pathlib import Path
import copy,json,os,socket,subprocess,sys,tempfile,time,unittest
sys.dont_write_bytecode=True
import host,peer,stopping
SERVER="""import json,os,socket,sys
path,wire=sys.argv[1:3];s=socket.socket(socket.AF_UNIX);s.bind(path);s.listen(1)
open(wire,'w').close()
try:
 c,_=s.accept();f=c.makefile('rwb');f.write(b'{"QMP":{"version":{},"capabilities":[]}}\\n');f.flush()
 while True:
  raw=f.readline()
  if not raw:break
  with open(wire,'a')as w:w.write(raw.decode())
  msg=json.loads(raw);f.write(b'{"return":{}}\\n');f.flush()
  if msg['execute']=='quit':break
 f.close();c.close()
except (OSError,ValueError):pass
finally:
 s.close()
 if os.path.exists(path):os.unlink(path)
"""
class Endpoint(unittest.TestCase):
 def make(self,t,foreign=False):
  work=t/'work';work.mkdir();q=host._module('wp55_peer_actual_qmp',host.ROOT/'scripts/reference/qmp.py');q.RUNTIME=t;q.SOCKET=t/'qmp.sock';wire=t/'wire';args=[sys.executable,'-c',SERVER,str(q.SOCKET),str(wire),str(work/'boot.img'),str(work/'harddisk.img'),'unix:'+str(q.SOCKET)+',server'];server=subprocess.Popen(args,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);deadline=time.monotonic()+2
  while not wire.exists():self.assertIsNone(server.poll());self.assertLess(time.monotonic(),deadline);time.sleep(.005)
  own=server
  if foreign:
   args=[sys.executable,'-c','import time;time.sleep(20)',str(work/'boot.img'),str(work/'harddisk.img'),'unix:'+str(q.SOCKET)+',server'];own=subprocess.Popen(args,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  (t/'qemu.pid').write_text(str(own.pid));g=host._module('wp55_peer_actual44',host.ROOT/'internal/document/evidence/wp44/oracle.py');identity=g.owned_identity(q,work,args);return q,g,identity,server,own,wire
 def cleanup(self,*ps):
  for p in set(ps):
   if p.poll()is None:p.terminate()
   p.wait(timeout=2)
 def commands(self,wire):return [json.loads(x)for x in wire.read_text().splitlines()]
 def test_foreign_main_zero_commands_owner_untouched(self):
  with tempfile.TemporaryDirectory()as d:
   q,g,i,server,own,wire=self.make(Path(d),True)
   try:
    with self.assertRaises(Exception):
     with host.main_connection(q,q.QMP,i,g.same_identity):pass
    server.wait(timeout=2);self.assertEqual(self.commands(wire),[]);self.assertIsNone(own.poll())
   finally:self.cleanup(server,own)
 def test_foreign_stop_zero_commands_owner_untouched(self):
  with tempfile.TemporaryDirectory()as d:
   t=Path(d);q,g,i,server,own,wire=self.make(t,True)
   try:
    with self.assertRaises(Exception):stopping.normal_quit(q,q.QMP,i,g.same_identity,lambda q,i:g.stopped(q,i,timeout=.2),t/'stop')
    server.wait(timeout=2);self.assertEqual(self.commands(wire),[]);self.assertIsNone(own.poll())
   finally:self.cleanup(server,own)
 def test_legitimate_main_control_same_kernel_owner(self):
  with tempfile.TemporaryDirectory()as d:
   q,g,i,server,own,wire=self.make(Path(d))
   try:
    with host.main_connection(q,q.QMP,i,g.same_identity)as c:c.execute('query-status');c.execute('quit')
    self.assertEqual(server.wait(timeout=2),0);self.assertEqual(self.commands(wire),[{'execute':'qmp_capabilities'},{'execute':'query-status'},{'execute':'quit'}])
   finally:self.cleanup(server,own)
 def test_stale_ticks_exe_argv_pid_refuse_before_commands(self):
  for key,value in [('startticks','1'),('executable','/foreign'),('argv',['foreign']),('pid',0)]:
   with self.subTest(key=key),tempfile.TemporaryDirectory()as d:
    q,g,i,server,own,wire=self.make(Path(d));bad=copy.deepcopy(i);bad[key]=value
    try:
     with self.assertRaises(Exception):
      with host.main_connection(q,q.QMP,bad,g.same_identity):pass
     self.assertEqual(self.commands(wire),[]);self.assertIsNone(own.poll())
    finally:self.cleanup(server,own)
 def test_lifetime_socket_retarget_blocks_next_send(self):
  with tempfile.TemporaryDirectory()as d:
   q,g,i,server,own,wire=self.make(Path(d));replacement=None
   try:
    with host.main_connection(q,q.QMP,i,g.same_identity)as c:
     q.SOCKET.unlink();replacement=socket.socket(socket.AF_UNIX);replacement.bind(str(q.SOCKET))
     with self.assertRaises(Exception):c.execute('query-status')
    server.wait(timeout=2);self.assertEqual(self.commands(wire),[{'execute':'qmp_capabilities'}])
   finally:
    if replacement:replacement.close()
    self.cleanup(server,own)
 def test_actual_host_startup_qmp_parameter_is_guarded(self):
  import types,oracle
  with tempfile.TemporaryDirectory()as d:
   t=Path(d);q=host._module('wp55_startup_actual_qmp',host.ROOT/'scripts/reference/qmp.py');q.RUNTIME=t;q.SOCKET=t/'qmp.sock';work=t/'work';wire=t/'wire';masters=t/'masters';masters.mkdir()
   for n in ['boot','harddisk']:(masters/(n+'.img')).write_bytes(b'TEST ONLY nonimage')
   workers=[]
   class Guest:
    MASTER=masters
    def arguments(self,a,b):return [sys.executable,'-c','import time;time.sleep(20)',str(a),str(b),'unix:'+str(q.SOCKET)+',server']
   class Session:
    def fresh_start(inner,passed,g,w,assets):
     w.mkdir();server=subprocess.Popen([sys.executable,'-c',SERVER,str(q.SOCKET),str(wire)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);own=subprocess.Popen(g.arguments(w/'boot.img',w/'harddisk.img'),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);workers.extend([server,own]);(t/'qemu.pid').write_text(str(own.pid));deadline=time.monotonic()+2
     while not wire.exists():self.assertLess(time.monotonic(),deadline);time.sleep(.005)
     with passed.QMP():raise AssertionError('foreign startup handshake bypass')
   guard=host._module('wp55_startup_actual44',host.ROOT/'internal/document/evidence/wp44/oracle.py');leaf=oracle.plan()['leaves'][0];leaf.update(private_work=str(work),installed_input_basename='I55IN');packet=dict(source_sha256='TEST ONLY',master={n:host.digest(masters/(n+'.img'))for n in ['boot','harddisk']})
   try:
    row=host.execute_leaf(packet,leaf,t/'public',lambda:None,(Session(),q,Guest(),guard,None));self.assertTrue(row['error_code'].startswith('QMPEndpoint'));workers[0].wait(timeout=2);self.assertEqual(self.commands(wire),[]);self.assertIsNone(workers[1].poll());self.assertFalse(row['normal_DOS']);self.assertFalse(row['exports_complete'])
   finally:self.cleanup(*workers)
 def test_kernel_unknown_credentials_fail_closed(self):
  s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
  try:
   with self.assertRaises(Exception):peer.credentials(s)
  finally:s.close()
if __name__=='__main__':unittest.main()
