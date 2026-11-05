"""Finite actual CLI semantic mutants; restore exact owned sources after each challenge."""
from pathlib import Path
import ast,json,sys
from boundaries import process,sha,require
from source import HERE,ROOT
CASES=[
 ('literal-all120',"font=extractor.prefix_font_fields(raw,tokenizer,defs);", "font=extractor.prefix_font_fields(raw,tokenizer,defs);font[0]['literal_u16le_or_u8']=120;",'test_nonfixture_known_value_and_forged_original_rejected'),
 ('phase-promoted',"applicable=phase==obs['phase']and role in obs['roles']","applicable=role in obs['roles']",'test_phase_changes_applicability_not_native_facts'),
 ('units-self-selected',"applicable=phase==obs['phase']and role in obs['roles']","applicable=phase==obs['phase']and (role in obs['roles']or role.startswith('selected_'))",'test_observed_unit_is_not_selected_setup'),
 ('reference-unbound',"require(self.sources.data(ref)==raw,'ReferenceNativeMismatch'","require(True,'ReferenceNativeMismatch'",'test_nonfixture_known_value_and_forged_original_rejected'),
 ('owner-unchecked',"require(len(owners)==1,'FontOwner'","require(len(owners)==1,'FontOwner'",None),
 ('captured-claim-trusted',"require(request['claim']==obs,'ForgedObservation'","require(True,'ForgedObservation'",'test_forged_capture_rehash_not_authority'),
]
def main():
 path=HERE/'qualify.py';original=path.read_bytes();rows=[]
 try:
  for name,old,new,test in CASES:
   if test is None:continue # Owner validation lives in approved reader/extractor, not mutable duplicated code.
   raw=original.decode();require(raw.count(old)==1,'MutantAnchor',name);mutant=raw.replace(old,new);ast.parse(mutant);path.write_text(mutant)
   out,err,code=process([sys.executable,'-B','-m','unittest','test_contract.Contract.'+test],HERE,timeout=120,allow_nonzero=True)
   (HERE/'checks'/('mutant-'+name+'.stdout.log')).write_bytes(out);(HERE/'checks'/('mutant-'+name+'.stderr.log')).write_bytes(err)
   require(code==1 and b'FAIL:'in err and b'SyntaxError'not in err and b'ImportError'not in err,'MutantSurvived',name);rows.append(dict(name=name,test=test,whole_exit=code,AST_valid=True,semantic_failure=True,mutant_sha256=sha(mutant.encode())))
   path.write_bytes(original)
 finally:path.write_bytes(original)
 result=dict(executed=len(rows),killed=len(rows),source_restored_sha256=sha(path.read_bytes()),mutants=rows);(HERE/'checks/mutants.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));return 0
if __name__=='__main__':raise SystemExit(main())
