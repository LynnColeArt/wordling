"""Bounded in-memory integrity mutations; never edit executing/protected source."""
import sys
sys.dont_write_bytecode=True
import contextlib,io,json,unittest,types
from pathlib import Path
from unittest.mock import patch
import frames,protocol,oracle,families,test_contract,test_orchestration

def mutant(module,old,new):
 source=Path(module.__file__).read_text();assert source.count(old)==1,(module.__name__,old);namespace=dict(vars(module));exec(compile(source.replace(old,new),'<isolated-mutant-'+module.__name__+'>','exec'),namespace);return {name:types.FunctionType(value.__code__,vars(module),name,value.__defaults__,value.__closure__)if isinstance(value,types.FunctionType)and value.__module__==module.__name__ else value for name,value in namespace.items()}

def run():
 cases=[
  (frames,'text==want','True','check',test_contract.Frames,'test_real_helper_unknown_centered_modal_is_not_main_authority'),
  (families,"row['Admitted']is False","True",'classify',test_contract.ReadOnlyFacts,'test_rehashed_wrong_source_graph_counter_refusal_and_field_drop'),
  (frames,"cursor['column']==spec['gap']","True",'check',test_contract.Frames,'test_all_middle_rows_status_mode_doc_cursor_and_shapes'),
  (oracle,"not l['halted']","True",'ledger_check',test_contract.Recipe,'test_ledger_exact_types_sticky_halt_cap_no_reset'),
  (oracle,"args.attempt==ids","True",'selected',test_contract.Recipe,'test_exact_eight_selection_no_subset_float_cap_or_old_ID'),
  (oracle,"row['stop_method']=='QMP quit; own socket terminated'","True",'attempt',test_orchestration.Attempt,'test_containment_not_normal_stopped_no_extract'),
  (oracle,"p.returncode==0 and path.is_file()","path.is_file()",'export',test_orchestration.Attempt,'test_actual_mcopy_nonzero_missing_and_oversize_refuse'),
  (oracle,"projection(receipts)==projection(expected['receipts'])","True",'verify_observations',test_orchestration.Trace,'test_reported_recipe_cannot_replace_complete_state_trace'),
  (oracle,"for prior in report['results']:prior_control(p,prior)","for prior in []:prior_control(p,prior)",'run',test_orchestration.Entry,'test_prior_PRN_tamper_in_actual_run_refuses_before_second_attempt'),
 ]
 rows=[]
 for module,old,new,name,cls,test in cases:
  namespace=mutant(module,old,new);suite=unittest.TestSuite([cls(test)]);stream=io.StringIO()
  with patch.object(module,name,namespace[name]),contextlib.redirect_stdout(io.StringIO()):r=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
  rows.append({'module':module.__name__,'mutation':old+' -> '+new,'test':cls.__name__+'.'+test,'killed':not r.wasSuccessful(),'raw_test_output':stream.getvalue()})
 return {'scope':'integrity mutants only, not native candidate/permission or original evidence','mutants':rows,'all_killed':all(x['killed']for x in rows)}
if __name__=='__main__':
 report=run();print(json.dumps(report,indent=2));raise SystemExit(0 if report['all_killed']else 1)
