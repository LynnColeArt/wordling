"""Finite real public CLI semantic mutants; no dependency source edits."""
import ast,json,sys
from enter_sources import B,HERE,sha
CASES=[('unknown-zero','enter_safety.py',"launch_unknown=stages.count('launch-unknown')","launch_unknown=0",'test_real_post_launch_unknown_not_zero'),('proved-zero','enter_safety.py',"positively_proved=stages.count('positively-proved')","positively_proved=0",'test_real_positive_kernel_identity_retained_then_failure'),('spent-zero','enter_safety.py',"tickets_spent=len(ids)","tickets_spent=0",'test_first_setup_fault_charged_no_child_sticky'),('historical-forgery','enter_oracle.py',"request['provenance']=='prospective-manual-and-qualified-components-only'","True",'test_rehashed_lost_b_mode_doc2_caret_provenance_forgeries'),('key-permission','enter_oracle.py',"original_qualification=False,key_permission=False,live_full_frame_match=False","original_qualification=False,key_permission=True,live_full_frame_match=False",'test_finite_semantic_component_never_full_frame_or_permission')]
def main():
 originals={name:(HERE/name).read_bytes()for _,name,_,_,_ in CASES};rows=[]
 try:
  for ident,name,old,new,test in CASES:
   text=originals[name].decode();B.require(text.count(old)==1,'MutantAnchor',ident);changed=text.replace(old,new);ast.parse(changed);(HERE/name).write_text(changed);out,err,code=B.process([sys.executable,'-B','-m','unittest','test_enter.Public.'+test],HERE,timeout=60,check=False);(HERE/'checks'/('mutant-'+ident+'.stdout.log')).write_bytes(out);(HERE/'checks'/('mutant-'+ident+'.stderr.log')).write_bytes(err);B.require(code==1 and b'FAIL:'in err and b'SyntaxError'not in err and b'ImportError'not in err,'MutantSurvived',ident);rows.append(dict(id=ident,test=test,whole_exit=code,AST_valid=True,actual_CLI_semantic_failure=True,mutant_sha256=sha(changed.encode())));(HERE/name).write_bytes(originals[name])
 finally:
  for name,raw in originals.items():(HERE/name).write_bytes(raw)
 result=dict(executed=len(rows),killed=len(rows),mutants=rows,restored={name:sha((HERE/name).read_bytes())for name in originals});(HERE/'checks/mutants.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
