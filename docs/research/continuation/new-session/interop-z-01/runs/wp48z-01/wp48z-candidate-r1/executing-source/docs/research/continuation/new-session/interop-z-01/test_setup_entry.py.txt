"""Actual run()/OS setup controls in isolated paths; no helper/run/check mocks.
Only HERE and declared lease/ledger/output paths are redirected. Their source
mismatch stops before configure; all grants here are TEST authority, never real.
"""
import copy,fcntl,hashlib,importlib.util,json,os,tempfile,types,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('wp48_setup_entry_current',HERE/'adapter.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
ORIGINAL=json.loads((HERE/'history/prelaunch-cycle1/proposal/preflight.json.txt').read_text())['plan']

def fixture(module,root,authorized=True,output_blocked=False):
 module.HERE=root/'proposal';module.HERE.mkdir();plan=copy.deepcopy(ORIGINAL);blocked=root/'blocked';blocked.mkdir();outparent=root/'reports';outparent.mkdir();plan.update(ledger=str(root/'ledger.json'),batch_lease=str(blocked/'batch.lock'),public_output=str(outparent/'output'))
 (module.HERE/'preflight.json').write_text(json.dumps({'plan':plan,'plan_sha256':module.canonical(plan)}));argv=[str(HERE/'adapter.py'),'run','--allow-vm','--grant',str(root/'grant.json')];grant={'authorized':authorized,'grant_id':module.GRANT_ID,'plan_sha256':module.canonical(plan),'attempt_ids':module.ids(),'maximum_attempts_including_failures':4,'authorization_note':'ISOLATED OFFLINE TEST ONLY; not a real grant','argv':[module.sys.executable,*argv]};(root/'grant.json').write_text(json.dumps(grant));return plan,types.SimpleNamespace(allow_vm=True,grant=str(root/'grant.json')),argv,blocked,outparent

def execute(module,args,argv):
 try:return {'return':module.run(args,argv)}
 except Exception as error:return {'exception':type(error).__name__,'code':getattr(error,'code',None),'error':str(error)}

def old_module():
 source=(HERE/'history/prelaunch-cycle1/proposal/adapter.py.txt').read_bytes();m=types.ModuleType('wp48_old_red');m.__file__=str(HERE/'adapter.py');exec(compile(source,m.__file__,'exec'),m.__dict__);return m

class EntryTests(unittest.TestCase):
 def setUp(self):self.saved=a.HERE;self.addCleanup(setattr,a,'HERE',self.saved)
 def test_red_original_unmocked_permission_gap(self):
  old=old_module()
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);p,args,argv,blocked,out=fixture(old,root);blocked.chmod(0o500)
   try:result=execute(old,args,argv)
   finally:blocked.chmod(0o700)
   self.assertEqual(result['exception'],'PermissionError');self.assertFalse(Path(p['ledger']).exists());self.assertFalse((root/'reports/output').exists())
   print('RED old actual entry:',json.dumps(result))
 def test_green_permission_failure_sticky_zero_guest_and_restored_retry(self):
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);p,args,argv,blocked,out=fixture(a,root);blocked.chmod(0o500)
   try:result=execute(a,args,argv)
   finally:blocked.chmod(0o700)
   self.assertEqual(result,{'return':1});ledger=Path(p['ledger']);record=json.loads(ledger.read_text());self.assertTrue(record['halted']);self.assertEqual(record['attempts'],[]);report=json.loads((root/'reports/output/run.json').read_text());self.assertEqual(report['positive_owned_start_identities'],0);self.assertEqual(report['charged_attempts_including_failures'],0);marker=a.setup.owner_path(p);self.assertEqual(json.loads(marker.read_text())['state'],'halted')
   before={x:x.read_bytes()for x in [ledger,marker,root/'reports/output/run.json']};retry=execute(a,args,argv);self.assertEqual(retry['code'],'PriorSetup');self.assertEqual(before,{x:x.read_bytes()for x in before});self.assertFalse(Path(p['batch_lease']).exists());print('GREEN sticky permission failure/restored retry:',json.dumps(retry))
 def test_unauthorized_entry_creates_nothing(self):
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);p,args,argv,blocked,out=fixture(a,root,False);blocked.chmod(0o500)
   try:result=execute(a,args,argv)
   finally:blocked.chmod(0o700)
   self.assertEqual(result['code'],'GrantMismatch');self.assertFalse(Path(p['ledger']).exists());self.assertFalse(a.setup.owner_path(p).exists());self.assertFalse((root/'reports/output').exists());self.assertFalse(Path(p['batch_lease']).exists())
 def test_real_busy_foreign_lease_does_not_write_or_poison(self):
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);p,args,argv,blocked,out=fixture(a,root);lease=Path(p['batch_lease']);lease.write_bytes(b'FOREIGN OWNER')
   with lease.open('rb')as handle:
    fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB);result=execute(a,args,argv);self.assertEqual(result['code'],'ForeignLease');self.assertEqual(lease.read_bytes(),b'FOREIGN OWNER');self.assertFalse(Path(p['ledger']).exists());self.assertFalse(a.setup.owner_path(p).exists());self.assertFalse((root/'reports/output').exists())
 def test_preexisting_foreign_ledger_and_output_are_not_replaced(self):
  for which in ['ledger','output','symlink-lease']:
   with self.subTest(which=which),tempfile.TemporaryDirectory()as tmp:
    root=Path(tmp);p,args,argv,blocked,out=fixture(a,root);ledger=Path(p['ledger']);output=root/'reports/output';target=root/'foreign';target.write_bytes(b'untouched')
    if which=='ledger':ledger.write_bytes(b'FOREIGN LEDGER')
    elif which=='output':output.mkdir();(output/'FOREIGN').write_bytes(b'FOREIGN OUTPUT')
    else:Path(p['batch_lease']).symlink_to(target)
    result=execute(a,args,argv);self.assertIn(result['code'],['PriorAttempt','ForeignLease']);self.assertFalse(a.setup.owner_path(p).exists());self.assertEqual(target.read_bytes(),b'untouched')
    if which=='ledger':self.assertEqual(ledger.read_bytes(),b'FOREIGN LEDGER')
    if which=='output':self.assertEqual((output/'FOREIGN').read_bytes(),b'FOREIGN OUTPUT')
 def test_owned_healthy_setup_then_real_source_fault_is_sticky(self):
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);p,args,argv,blocked,out=fixture(a,root);result=execute(a,args,argv);self.assertEqual(result,{'return':1});l=json.loads(Path(p['ledger']).read_text());self.assertTrue(l['halted']);self.assertEqual(l['attempts'],[]);self.assertEqual(json.loads(a.setup.owner_path(p).read_text())['state'],'halted');self.assertEqual(execute(a,args,argv)['code'],'PriorSetup')
 def test_halt_report_persistence_failure_is_truthful_and_marker_blocks_retry(self):
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);p,args,argv,blocked,out=fixture(a,root);blocked.chmod(0o500);out.chmod(0o500)
   try:result=execute(a,args,argv)
   finally:blocked.chmod(0o700);out.chmod(0o700)
   self.assertEqual(result['code'],'HaltPersistenceFailed');self.assertFalse((root/'reports/output/run.json').exists());self.assertTrue(json.loads(Path(p['ledger']).read_text())['halted']);self.assertEqual(json.loads(a.setup.owner_path(p).read_text())['state'],'halted');self.assertEqual(execute(a,args,argv)['code'],'PriorSetup')
 def test_no_writable_claim_location_reports_HaltPersistenceFailed_not_success(self):
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);p,args,argv,blocked,out=fixture(a,root);private=root/'unwritable';private.mkdir();p['ledger']=str(private/'ledger.json');(a.HERE/'preflight.json').write_text(json.dumps({'plan':p,'plan_sha256':a.canonical(p)}));g=json.loads(Path(args.grant).read_text());g['plan_sha256']=a.canonical(p);Path(args.grant).write_text(json.dumps(g));private.chmod(0o500)
   try:result=execute(a,args,argv)
   finally:private.chmod(0o700)
   self.assertEqual(result['code'],'HaltPersistenceFailed');self.assertFalse(Path(p['ledger']).exists());self.assertFalse(a.setup.owner_path(p).exists());self.assertFalse(Path(p['batch_lease']).exists());self.assertFalse((root/'reports/output').exists())

if __name__=='__main__':unittest.main(verbosity=2)
