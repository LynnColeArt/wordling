import importlib,json,sys,unittest
from pathlib import Path
root=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-k')
here=root/'docs/research/continuation/native-edits'
sys.path[:0]=[str(here),str(root/'scripts/reference')]
import analyze,candidate_mode,native_edits
mode=sys.argv[1]
if mode=='ignore-print-semantics':
 analyze.print_audit=lambda *a,**k:{};test='test_evidence.EvidenceTests.test_rehashed_wrong_ink_does_not_match_native_semantics'
elif mode=='ignore-field-relationships':
 candidate_mode.compare_relationships=lambda *a,**k:{};test='test_final_contract.FinalContract.test_matching_text_and_valid_reader_are_insufficient_for_unknown_counter_relation'
elif mode=='ignore-final-full-state':
 analyze.require_final_state=lambda *a,**k:{};test='test_evidence.EvidenceTests.test_correct_DOS_cue_and_cursor_with_stale_rest_of_screen_is_not_final'
elif mode=='allow-third-pair':
 native_edits.PAIR_LIMIT=3;test='test_inspector.InspectorTests.test_third_sequential_pair_refuses_initial_policy_not_original_format'
else:raise ValueError(mode)
result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName(test))
print(json.dumps({'mutant':mode,'tests_run':result.testsRun,'killed':not result.wasSuccessful(),'failures':len(result.failures),'errors':len(result.errors)}))
raise SystemExit(0 if result.testsRun==1 and not result.wasSuccessful() else 1)
