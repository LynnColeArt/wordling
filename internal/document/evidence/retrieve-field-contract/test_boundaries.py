"""Failure injection at the local process/file boundary; never a reference guest."""
from pathlib import Path
from contextlib import redirect_stdout
from unittest.mock import patch
import io,json,os,sys,tempfile,unittest
import bounded,oracle,sources
class Boundaries(unittest.TestCase):
 def error(self,code,call):
  with self.assertRaises(bounded.Refusal)as e:call()
  self.assertEqual(e.exception.code,code)
 def test_actual_subprocess_caps_timeout_start_and_no_orphan(self):
  with tempfile.TemporaryDirectory()as tmp:
   tmp=Path(tmp);pid=tmp/'pid'
   for channel in ['stdout','stderr']:
    code="import os,sys,time;open(sys.argv[1],'w').write(str(os.getpid()));sys.%s.write('x'*80000);sys.%s.flush();time.sleep(5)"%(channel,channel)
    self.error('SubprocessOutputBudget',lambda:bounded.process([sys.executable,'-c',code,str(pid)],tmp,stdout_limit=32,stderr_limit=32))
    with self.assertRaises(ProcessLookupError):os.kill(int(pid.read_text()),0)
   code="import os,sys,time;open(sys.argv[1],'w').write(str(os.getpid()));os.close(1);os.close(2);time.sleep(5)"
   self.error('SubprocessTimeout',lambda:bounded.process([sys.executable,'-c',code,str(pid)],tmp,timeout=.15))
   with self.assertRaises(ProcessLookupError):os.kill(int(pid.read_text()),0)
   self.error('SubprocessStart',lambda:bounded.process([str(tmp/'absent')],tmp))
   self.error('SubprocessExit',lambda:bounded.process([sys.executable,'-c','raise SystemExit(7)'],tmp))
   self.error('SubprocessInputBudget',lambda:bounded.process(['NEVER'],tmp,b'x'*(512*1024+1)))
 def test_public_entry_truncated_source_helper_preserves_report(self):
  with tempfile.TemporaryDirectory()as tmp:
   out=Path(tmp)/'report';out.write_bytes(b'KEEP');s=io.StringIO()
   with patch.object(sources,'process',return_value=(b'truncated\n',b'')),redirect_stdout(s):code=oracle.main(['check','--output',str(out)])
   self.assertEqual(code,2);self.assertEqual(json.loads(s.getvalue())['error']['code'],'SourceFraming');self.assertEqual(out.read_bytes(),b'KEEP')
 def test_report_short_write_close_replace_and_cleanup_failures(self):
  with tempfile.TemporaryDirectory()as tmp:
   out=Path(tmp)/'report';out.write_bytes(b'KEEP')
   with patch.object(bounded.os,'fsync',side_effect=OSError('write/flush failure')):self.error('ReportIO',lambda:bounded.atomic_report(out,b'NEW'))
   self.assertEqual(out.read_bytes(),b'KEEP');self.assertEqual(list(Path(tmp).iterdir()),[out])
   with patch.object(bounded.os,'replace',side_effect=OSError('replace failure')):self.error('ReportIO',lambda:bounded.atomic_report(out,b'NEW'))
   self.assertEqual(out.read_bytes(),b'KEEP');self.assertEqual(list(Path(tmp).iterdir()),[out])
   with patch.object(bounded.os,'replace',side_effect=OSError('replace failure')),patch.object(bounded.os,'unlink',side_effect=OSError('cleanup failure')):self.error('ReportCleanup',lambda:bounded.atomic_report(out,b'NEW'))
   self.assertEqual(out.read_bytes(),b'KEEP');self.assertEqual(len(list(Path(tmp).glob('.retrieve-report-*'))),1)
   self.error('ReportBudget',lambda:bounded.atomic_report(out,b'x'*(2*1024*1024+1)))
 def test_actual_report_short_write_and_close_error_do_not_replace(self):
  original=bounded.os.fdopen
  for fault,code in [('short','ReportShortWrite'),('close','ReportIO')]:
   with tempfile.TemporaryDirectory()as tmp:
    out=Path(tmp)/'report';out.write_bytes(b'KEEP')
    class Stream:
     def __init__(self,fd):self.real=original(fd,'wb')
     def __enter__(self):return self
     def write(self,data):return self.real.write(data[:1]if fault=='short'else data)
     def flush(self):return self.real.flush()
     def fileno(self):return self.real.fileno()
     def __exit__(self,*unused):
      self.real.close()
      if fault=='close':raise OSError('explicit close failure')
    with patch.object(bounded.os,'fdopen',side_effect=lambda fd,mode:Stream(fd)):self.error(code,lambda:bounded.atomic_report(out,b'NEW'))
    self.assertEqual(out.read_bytes(),b'KEEP');self.assertEqual(list(Path(tmp).iterdir()),[out])
 def test_public_packet_deep_duplicate_and_invalid_hex(self):
  import subprocess
  with tempfile.TemporaryDirectory()as tmp:
   p=Path(tmp)/'input'
   for raw,code in [(b'{"x":1,"x":2}','PacketJSON'),(b'{"x":'+b'['*50+b'0'+b']'*50+b'}','PacketComplexity')]:
    p.write_bytes(raw);q=subprocess.run([sys.executable,str(oracle.HERE/'oracle.py'),'inspect','--packet',str(p)],capture_output=True,text=True,timeout=20);self.assertEqual(q.returncode,2);self.assertEqual(json.loads(q.stdout)['error']['code'],code)
if __name__=='__main__':unittest.main()
