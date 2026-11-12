from pathlib import Path
import sys,importlib.util,types,unittest,io,json
sys.dont_write_bytecode=True
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-w');D=R/'docs/research/continuation/secondary-record-contract';O=Path('/tmp/wordling-WP53-independent-review')
s=importlib.util.spec_from_file_location('tests',D/'test_contract.py');T=importlib.util.module_from_spec(s);s.loader.exec_module(T);original=T.C;rows=[]
for name,method in [('count-minus-one','test_unproved_three_explicit_fields_count4_is_not_count_minus_one'),('missing-is-empty','test_genuine_empty_missing_and_space_distinct'),('strip-result-controls','test_result_projection_retains_metadata_and_controls'),('unbound-paired-source','test_rehashed_case_role_result_source_swaps')]:
 m=types.ModuleType('mutant_'+name);m.__file__=str(R/'scripts/reference/secondary_record_contract.py');sys.modules[m.__name__]=m;source=(D/'evidence'/('mutant-'+name+'.py.txt')).read_text();exec(compile(source,m.__file__,'exec'),m.__dict__);T.C=m;stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.TestSuite([T.ContractTests(method)]));raw=stream.getvalue();(O/('mutant-'+name+'.log')).write_text(raw);assert len(result.failures)>0 and not result.errors,raw;rows.append({'name':name,'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'killed_semantically':True})
T.C=original
with original.Session(R)as ss:
 p=ss.cwd/'internal/secondary-contract/main.go';p.write_bytes((D/'evidence/mutant-foreign-span-fallback.go.txt').read_bytes());code,out,err=original.bounded(['go','test','-count=1','-run','TestPublicOwnedBoundary','./internal/secondary-contract'],ss.cwd);raw=out+err;(O/'mutant-foreign-span-fallback.log').write_bytes(raw);assert code==1 and b'helper accepted foreign span'in raw;rows.append({'name':'foreign-span-fallback','exit':code,'compiled_and_killed_semantically':True})
(O/'mutant-replay.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
