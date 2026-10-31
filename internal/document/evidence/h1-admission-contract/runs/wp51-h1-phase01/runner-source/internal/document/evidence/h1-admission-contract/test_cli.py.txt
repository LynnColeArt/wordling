"""Public CLI offline behavior; no actual guard or private runtime acquired."""
import sys
sys.dont_write_bytecode=True
import hashlib,json,os,subprocess,tempfile,unittest
from pathlib import Path
import oracle
class CLI(unittest.TestCase):
 def cli(self,*args):return subprocess.run([sys.executable,str(oracle.HERE/'oracle.py'),*args],cwd=oracle.ROOT,capture_output=True,text=True,timeout=60,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 def test_default_and_check_deterministic_read_only(self):
  paths=[*oracle.HERE.glob('*.py'),oracle.BIN,*[oracle.ROOT/p for p in json.loads((oracle.HERE/'approved-source-preflight.json').read_text())['all_document_Go_byteexact_approved46']]];before={str(p):oracle.sha(p)for p in paths};a=self.cli();b=self.cli('check');self.assertEqual((a.returncode,b.returncode),(0,0));self.assertEqual(json.loads(a.stdout),json.loads(b.stdout));self.assertEqual(before,{str(p):oracle.sha(p)for p in paths});plan=json.loads(a.stdout);self.assertEqual(len(plan['attempts']),8);self.assertFalse(plan['vm_authorized']or plan['native_mutation_permission']);self.assertFalse(Path(plan['ledger']).exists());self.assertFalse(Path(plan['socket']).exists())
 def test_run_without_allow_vm_refuses_without_ledger(self):
  result=self.cli('run','--grant','/nonexistent-isolated-grant','--grant-id','wp51-isolated','--attempt','isolated');self.assertNotEqual(result.returncode,0);self.assertIn('no root grant, offline default',result.stderr)
 def test_result_incomplete_replay_refuses_without_write(self):
  with tempfile.TemporaryDirectory()as t:
   d=Path(t);p={'isolated':'no original evidence'};oracle.dump(d/'prelaunch.json',{'plan':p});oracle.dump(d/'aggregate-ledger.json',{'plan_sha256':oracle.canonical(p),'halted':True,'attempts':[]});oracle.dump(d/'run.json',{'plan_sha256':oracle.canonical(p),'complete':False,'results':[]});before={p.name:oracle.sha(p)for p in d.iterdir()};r=self.cli('result',str(d));self.assertNotEqual(r.returncode,0);self.assertIn('not all eight complete',r.stderr);self.assertEqual(before,{p.name:oracle.sha(p)for p in d.iterdir()})
if __name__=='__main__':unittest.main()
