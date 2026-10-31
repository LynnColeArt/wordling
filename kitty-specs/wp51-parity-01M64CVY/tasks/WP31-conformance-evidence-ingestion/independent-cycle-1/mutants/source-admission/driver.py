import sys,unittest,importlib.util
sys.path.insert(0,'/tmp/wordling-WP31-independent-review/mutants/source-admission')
import ingest_wp29
spec=importlib.util.spec_from_file_location("tests",'/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-m/tests/conformance/v1/test_ingestion.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
r=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([m.SourceJoin("test_actual_complete_source_join"),m.SourceJoin('test_missing_extra_changed_sources_and_wrong_compiled_set')]))
sys.exit(not r.wasSuccessful())
