import sys,unittest,importlib.util
sys.path.insert(0,'/tmp/wordling-WP31-independent-review/mutants/forced-review')
import ingest_wp29
spec=importlib.util.spec_from_file_location("tests",'/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-m/tests/conformance/v1/test_ingestion.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
r=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([m.SourceJoin("test_actual_complete_source_join"),m.SourceJoin('test_actual_review_event_rejects_force_actor_result_or_missing_identity')]))
sys.exit(not r.wasSuccessful())
