"""Finite real owned-source mutants; each selected public/component test must falsify it.
Never alters approved dependency code. Restores exact original bytes in finally.
"""
from pathlib import Path
import ast,hashlib,json,sys
sys.dont_write_bytecode=True
from boundaries import process,Refusal
HERE=Path(__file__).resolve().parent;OUT=HERE/'checks/mutants-final'
CASES=[
 ('permission-true','oracle.py','prospective_rule_match=True,original_qualification=False','prospective_rule_match=True,original_qualification=True','test_contract.py','Contract.test_first_empty_and_typed_are_pure'),
 ('skip-full-frame','oracle.py',"require(canonical(f)==canonical(expected),'UnknownFrame'","require(True,'UnknownFrame'",'test_cli.py','CLI.test_invalid_rehashed_frame_prior_report_unchanged'),
 ('second-Enter','ui.py',"self.key('f1');self.ui('after-F1'","self.key('ret');self.ui('after-F1'",'test_protocol.py','ProtocolContract.test_twelve_component_traces_firsthistory_insert_second_f1_only'),
 ('skip-post-clear-mode','ui.py',"if self.leaf['mode']=='Typeover':self.key('insert')","if False:self.key('insert')",'test_protocol.py','ProtocolContract.test_twelve_component_traces_firsthistory_insert_second_f1_only'),
 ('source-after-NEXT','account.py','if i:before_each()','if i:pass','test_safety.py','DriverOrder.test_real_shared_coordinator_fault_order_and_sticky_NEXt'),
 ('unknown-stop-qualified','account.py',"and all(v is True for v in proof.values()),'UnsafeRelease'",",'UnsafeRelease'",'test_safety.py','Safety.test_unknown_stop_no_qualified_release_or_audit'),
 ('volatile-halt','account.py',"try:self._owner.write(self._ledger)\n  except BaseException as e:raise Refusal('HaltPersistenceFailed'","try:pass\n  except BaseException as e:raise Refusal('HaltPersistenceFailed'",'test_safety.py','Safety.test_unauthorized_zero_touch_setup_fault_is_spent_and_sticky'),
 ('leader-exit-skips-KILL','boundaries.py','os.killpg(p.pid,signal.SIGKILL);receipts.append',"(os.killpg(p.pid,signal.SIGKILL)if os.waitid(os.P_PID,p.pid,os.WEXITED|os.WNOHANG|os.WNOWAIT)is None else None);receipts.append",'test_safety.py','Safety.test_leader_exit_or_alive_timeout_and_outputcap_no_orphan'),
 ('stale-owner-key','ui.py',"self.current_authority();require(key in [","require(key in [",'test_protocol.py','ProtocolContract.test_authority_lost_between_capture_and_key'),
]
def main():
 OUT.mkdir(exist_ok=True);results=[]
 for name,file,old,new,test,selector in CASES:
  p=HERE/file;original=p.read_bytes();text=original.decode();assert text.count(old)==1,(name,text.count(old));changed=text.replace(old,new);ast.parse(changed);dest=OUT/(name+'.py.txt');dest.write_text(changed)
  try:
   p.write_text(changed)
   try:
    stdout,stderr,code=process([sys.executable,'-B',str(HERE/test),selector],HERE,timeout=60,stdout_limit=256<<10,stderr_limit=256<<10,check=False)
   except Refusal as e:stdout=b'';stderr=str(e).encode();code=1
   (OUT/(name+'.stdout.log')).write_bytes(stdout);(OUT/(name+'.stderr.log')).write_bytes(stderr)
   # Current process wrapper retains precise failing unittest stderr in ProcessExit detail.
   assert code!=0 and (b'FAIL'in stderr or b'ERROR'in stderr),(name,stderr)
   results.append(dict(name=name,source=file,selector=selector,AST_compiled=True,real_test_executed=True,killed=True,raw_capture='complete bounded raw stdout/stderr and actual whole exit',original_sha256=hashlib.sha256(original).hexdigest(),mutant_sha256=hashlib.sha256(changed.encode()).hexdigest()))
  finally:p.write_bytes(original)
 (OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(dict(executed=len(results),killed=len(results),source_restored=True)))
if __name__=='__main__':main()
