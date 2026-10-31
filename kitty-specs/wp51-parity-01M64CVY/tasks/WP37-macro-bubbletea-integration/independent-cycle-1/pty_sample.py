from pathlib import Path
import importlib.util,sys,json
r=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-h');o=Path('/tmp/wordling-WP37-independent-review');src=r/'docs/research/continuation/macro-executable/pty_test.py';sys.dont_write_bytecode=True;sys.path.insert(0,str(src.parent));spec=importlib.util.spec_from_file_location('wp37_actual_pty',src);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
# Test-artifact destination adapter only; production binary, original inputs,
# public CLI recipes, keys, predicates and native comparator are unchanged.
mod.OUT=o
for name in ['WP39-nested-1','WP38-repeat-doc2-1','negative-strict-flat-cout']:
 sys.argv=[str(src),str(o/'wordling'),str(o/('pty-'+name)),'--only',name];assert mod.main()==0
(o/'PTY-adapter-scope.json').write_text(json.dumps({'adapter':'only harness OUT destination changed to review/tmp; original __file__/ROOT/source/keys/recipes/nativecomparison unchanged','production_sources_changed':False,'VM_attempts':0},indent=2)+'\n')
