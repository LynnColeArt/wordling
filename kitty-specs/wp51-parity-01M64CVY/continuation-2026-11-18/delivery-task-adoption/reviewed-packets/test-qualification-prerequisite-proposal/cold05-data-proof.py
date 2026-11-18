"""Source-derived path/guard DATA proof only; no operational import or filesystem poison."""
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
S=Path('/home/lynn/projects/wordling/internal/document/evidence/reference_controller/tests/runtime_qualification.py')
text=S.read_text();tree=ast.parse(text)
strict=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='strict_layout')
cfg=next(n for n in strict.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='cfg'for t in n.targets))
expected=next(n for n in strict.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='expected_cfg'for t in n.targets))
guard=next(n for n in strict.body if isinstance(n,ast.If)and isinstance(n.test,ast.Compare)and isinstance(n.test.left,ast.Name)and n.test.left.id=='cfg')
assert isinstance(cfg.value,ast.Call)and isinstance(cfg.value.func,ast.Attribute)and cfg.value.func.attr=='read_text'
assert ast.unparse(cfg.value.func.value)=="v / 'pyvenv.cfg'"
assert ast.unparse(guard.test)=='cfg != expected_cfg'
assert len(guard.body)==1 and isinstance(guard.body[0],ast.Raise)
assert ast.unparse(guard.body[0].exc)=="RuntimeError('ExactVenvConfig')"
base_node=next(n for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='BASE'for t in n.targets))
base=PurePosixPath(ast.literal_eval(base_node.value.args[0]))
v=PurePosixPath('/tmp/wordling-WP70-current-test-qualification-v2/disposable-cold/venv')
env=dict(BASE=base,v=v,str=str,RuntimeError=RuntimeError)
expected_text=eval(compile(ast.Expression(expected.value),str(S),'eval'),env)
config_path=eval(compile(ast.Expression(cfg.value.func.value),str(S),'eval'),env)
assert config_path==v/'pyvenv.cfg'and config_path.is_relative_to(v)
assert not config_path.is_relative_to(base.parent.parent)
assert expected_text.count('version = 3.12.14\n')==1
poison=expected_text.replace('version = 3.12.14\n','version = 3.12.13\n',1)
fragment=compile(ast.fix_missing_locations(ast.Module(body=[guard],type_ignores=[])),str(S),'exec')
exec(fragment,{**env,'cfg':expected_text,'expected_cfg':expected_text})
try:exec(fragment,{**env,'cfg':poison,'expected_cfg':expected_text})
except RuntimeError as error:assert str(error)=='ExactVenvConfig'
else:raise AssertionError('SOURCE_GUARD_DATA_POISON_SURVIVED')
preflight=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='preflight')
layout_call=next(n for n in preflight.body if isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)and isinstance(n.value.func,ast.Name)and n.value.func.id=='strict_layout')
assert layout_call.lineno < next(n.lineno for n in preflight.body if isinstance(n,ast.For))
print(json.dumps(dict(schema='wordling.cold05-source-DATA-proof/v1',source=str(S),source_sha256=hashlib.sha256(text.encode()).hexdigest(),source_locations=dict(cfg_read=cfg.lineno,expected_cfg=expected.lineno,exact_guard=guard.lineno,canonical_preflight_layout_call=layout_call.lineno),config_path=str(config_path),BASE_source_literal=str(base),positive_DATA='exact canonical config passes extracted comparison',negative_DATA='version-only3.12.13 yields exact canonical ExactVenvConfig raise',guard_fragment_sha256=hashlib.sha256(ast.get_source_segment(text,guard).encode()).hexdigest(),operational_module_imported=False,canonical_full_preflight_executed=False,fixture_or_BASE_written=False,candidate_executed=False,case_count=33,OS_minimum=13),sort_keys=True,indent=2))
