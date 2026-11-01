"""Actual healthy CLI and source-bound host-worker failure preserve prior report."""
from pathlib import Path
import contextlib,ctypes,hashlib,io,json,os,signal,subprocess,sys,tempfile,time,unittest
from unittest import mock
from test_cleanup import C,ROOT,state,reap

class CLITests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  libc=ctypes.CDLL(None,use_errno=True)
  if libc.prctl(36,1,0,0,0)!=0:raise OSError(ctypes.get_errno(),'test subreaper unavailable')

 def test_public_healthy_and_real_inherited_pipe_failure(self):
  with tempfile.TemporaryDirectory(prefix='wp53-r1-cli-')as directory:
   d=Path(directory);output=d/'report.json';native=d/'input.wp5';ready=d/'child.json';fault=d/'fault-worker'
   authority=json.loads((ROOT/C.OWNED/'authority.json').read_text());pro=ROOT/authority['provenance_directory']
   fixture=pro/'git'/C.READER/'docs/research/reference-runs/2026-10-29-advanced-04/CMD51-207/SECOND.WP5.txt'
   raw=fixture.read_bytes();native.write_bytes(raw)
   argv=[sys.executable,str(ROOT/'scripts/reference/secondary_record_contract.py'),'inspect','--input',str(native),'--role','Secondary','--output',str(output)]
   p=subprocess.run(argv,cwd=ROOT,capture_output=True,timeout=60)
   self.assertEqual(p.returncode,0,p.stderr)
   healthy=json.loads(output.read_text());self.assertTrue(healthy['reader_inspection']['exact_export']);self.assertFalse(healthy['reader_inspection']['supported']);self.assertEqual(len(healthy['closed_shape']),2)
   child=f'''import os,json,signal,time
from pathlib import Path
signal.signal(signal.SIGTERM,signal.SIG_IGN)
pid=os.getpid();fields=Path(f'/proc/{{pid}}/stat').read_text().rsplit(')',1)[1].split()
Path({str(ready)!r}).write_text(json.dumps({{'pid':pid,'ppid':os.getppid(),'pgid':os.getpgid(0),'sid':os.getsid(0),'ticks':int(fields[19])}}))
time.sleep(10)
'''
   launcher=f'''#!{sys.executable}
import subprocess,sys,time
from pathlib import Path
subprocess.Popen([sys.executable,'-c',{child!r}])
until=time.monotonic()+2
while not Path({str(ready)!r}).exists()and time.monotonic()<until:time.sleep(.002)
'''
   fault.write_text(launcher);fault.chmod(0o700)
   prior=b'prior-successful-report';output.write_bytes(prior);real_session=C.Session;launched=[];session_data={};real_popen=subprocess.Popen
   class FaultSession(real_session):
    def __init__(self):
     super().__init__();session_data['production_helper_binary_sha256']=self.receipt['binary_sha256']
     self.binary=fault;self.deadline=time.monotonic()+.3
   def capture(*a,**kw):
    p=real_popen(*a,**kw)
    if a[0][0]==str(fault):launched.append(p)
    return p
   error=io.StringIO();started=time.monotonic();info=None
   try:
    with mock.patch.object(C,'Session',FaultSession),mock.patch.object(C.subprocess,'Popen',side_effect=capture),contextlib.redirect_stderr(error):
     code=C.main(['inspect','--input',str(native),'--role','Secondary','--output',str(output)])
    self.assertEqual(code,1);self.assertIn('HelperTimeout',error.getvalue());self.assertEqual(output.read_bytes(),prior);self.assertEqual(native.read_bytes(),raw)
    self.assertEqual(len(launched),1);info=json.loads(ready.read_text());self.assertEqual(info['pgid'],launched[0].pid);self.assertEqual(info['sid'],launched[0].pid)
    current=state(info['pid'])
    if current:self.assertEqual(current['ticks'],info['ticks'])
    status=reap(info['pid']);self.assertTrue(os.WIFSIGNALED(status));self.assertEqual(os.WTERMSIG(status),signal.SIGKILL)
    self.assertIsNone(state(info['pid']));self.assertEqual(launched[0].returncode,0);self.assertIsNone(state(launched[0].pid))
    with self.assertRaises(ProcessLookupError):os.killpg(launched[0].pid,0)
    record={'checker_sha256':hashlib.sha256((ROOT/'scripts/reference/secondary_record_contract.py').read_bytes()).hexdigest(),'healthy_public_cli_argv':argv,'healthy_cli_exit':p.returncode,'healthy_stdout_hex':p.stdout.hex(),'native_input_sha256':hashlib.sha256(raw).hexdigest(),'fault_injection':'TEST-ONLY subclass replaces a real source-bound Session worker AFTER actual constructor/build; no production override option','injected_launcher':launcher,'injected_child_argv':[sys.executable,'-c',child],'actual_child_identity':info,'parent_pid':launched[0].pid,'parent_exit':launched[0].returncode,'child_wait_status':status,'positive_group_gone_after_reap':True,'main_exit':code,'stderr':error.getvalue(),'prior_report_preserved':True,'elapsed_seconds':time.monotonic()-started,**session_data}
    if os.environ.get('WP53_CLI_RECEIPT'):Path(os.environ['WP53_CLI_RECEIPT']).write_text(json.dumps(record,indent=2)+'\n')
   finally:
    if info is None and ready.exists():info=json.loads(ready.read_text())
    if info:
     now=state(info['pid'])
     if now and now['state']!='Z':
      assert now['ticks']==info['ticks']and now['pgid']==info['pgid']and launched and info['pgid']==launched[0].pid
      os.killpg(info['pgid'],signal.SIGKILL)
     with contextlib.suppress(ChildProcessError):reap(info['pid'])
    for leader in launched:
     if leader.returncode is None:leader.wait(timeout=1)

if __name__=='__main__':unittest.main(verbosity=2)
