from pathlib import Path
import importlib.util
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-u');O=Path('/tmp/wordling-wp49-independent');p=R/'docs/research/continuation/text-flow-contract/tests/fuzz_contract.py';spec=importlib.util.spec_from_file_location('independent_fuzz',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);(O/'fuzz/evidence').mkdir(parents=True);m.t.OUT=O/'fuzz';m.main()
