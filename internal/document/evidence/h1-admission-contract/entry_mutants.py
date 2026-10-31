"""Focused actual-OS R1/R2 falsifiers, in-memory source only."""
import sys
sys.dont_write_bytecode=True
import contextlib,io,json,types,unittest
from pathlib import Path
from unittest.mock import patch
import oracle,accounting,test_entry_os

def changed(source,old,new,name,globals):
 assert source.count(old)==1,old;ns=dict(globals);exec(compile(source.replace(old,new),'<owned-entry-mutant>','exec'),ns);f=ns[name];return types.FunctionType(f.__code__,globals,name,f.__defaults__,f.__closure__)
def run():
 rows=[]
 def check(label,context,cls,name):
  stream=io.StringIO()
  with context,contextlib.redirect_stdout(io.StringIO()):r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.TestSuite([cls(name)]))
  rows.append({'mutation':label,'test':cls.__name__+'.'+name,'killed':not r.wasSuccessful(),'output':stream.getvalue()})
 source=Path(accounting.__file__).read_text();ns=dict(vars(accounting));exec(compile(source.replace('os.O_EXCL|',''),'<without-O_EXCL>','exec'),ns);f=ns['OwnedFile'].__init__;f=types.FunctionType(f.__code__,vars(accounting),f.__name__,f.__defaults__,f.__closure__);check('remove atomic exclusive accounting creation',patch.object(accounting.OwnedFile,'__init__',f),test_entry_os.EntryOS,'test_foreign_ledger_symlink_directory_and_busy_flock_preserved')
 source=Path(oracle.__file__).read_text();f=changed(source,"owner.verify()\n  try:public=", "pass\n  try:public=",'run',vars(oracle));check('omit held owner identity before setup',patch.object(oracle,'run',f),test_entry_os.EntryOS,'test_replaced_owner_inode_never_overwrites_foreign')
 f=changed(source,"print(json.dumps({'notification':'physical-guard-exited-before-offline-audit',**receipt}),flush=True)","pass",'run',vars(oracle));check('omit immediate release notification',patch.object(oracle,'run',f),test_entry_os.PhysicalLease,'test_actual_flock_guest_held_audit_free_reacquire_before_next')
 f=changed(source,"row.get('guest_stopped')is True",'True','run',vars(oracle));check('claim safe release without owned stopped state',patch.object(oracle,'run',f),test_entry_os.PhysicalLease,'test_actual_flock_guest_held_audit_free_reacquire_before_next')
 def held_audit(session,private,callback):
  with session.exclusive(private):return callback()
 f=changed(source,"row['qualification']=qualify(target,row,leaf,p,report['results'])","row['qualification']=_held_audit(session,private,lambda:qualify(target,row,leaf,p,report['results']))",'run',vars(oracle))
 with patch.dict(vars(oracle),{'_held_audit':held_audit}):check('hold actual physical flock during readonly audit',patch.object(oracle,'run',f),test_entry_os.PhysicalLease,'test_actual_flock_guest_held_audit_free_reacquire_before_next')
 return {'scope':'synthetic actual-OS integrity controls only, not original observations','all_killed':all(x['killed']for x in rows),'mutants':rows}
if __name__=='__main__':
 result=run();print(json.dumps(result,indent=2));raise SystemExit(0 if result['all_killed']else 1)
