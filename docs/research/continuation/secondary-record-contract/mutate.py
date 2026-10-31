"""Finite checker faults, only owned sources, restored exactly in finally."""
from pathlib import Path
import ast,hashlib,importlib.util,json,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;E=O/'evidence';SCRIPT=ROOT/'scripts/reference/secondary_record_contract.py';HELPER=O/'inspect.go.txt';TEST=O/'test_contract.py';H=lambda b:hashlib.sha256(b).hexdigest()
base=SCRIPT.read_bytes();gobase=HELPER.read_bytes()
mutants=[
 ('count-minus-one',SCRIPT,
  [("{2: 'de3406000200060034de', 3: 'de3406000300060034de'}", "{2: 'de3406000200060034de', 3: 'de3406000300060034de', 4: 'de3406000400060034de'}"),("{'RecordCountUnresolved', 'FormatterUnresolved'}", "{'RecordCountUnresolved', 'FormatterUnresolved', 'UnobservedRecordCount'}"),
   ("(r['stored_count'], len(fields)) in {(2, 1), (3, 2)}", "r['stored_count'] == len(fields) + 1")],
  'test_unproved_three_explicit_fields_count4_is_not_count_minus_one'),
 ('missing-is-empty',SCRIPT,
  [("require(all(number <= len(r['explicit_values_hex']) for r in records), 'OutsideExplicitFields')", "require(True, 'OutsideExplicitFields')"),
   ("[r['explicit_values_hex'][number - 1] for r in records]", "[r['explicit_values_hex'][number - 1] if number <= len(r['explicit_values_hex']) else '' for r in records]")],
  'test_genuine_empty_missing_and_space_distinct'),
 ('strip-result-controls',SCRIPT,
  [("selected.extend(raw)", "selected.extend(raw if token['kind'] == 1 else b'')"),
   ("metadata.append(token['raw'])", "pass  # incorrect blanket metadata/control removal")],
  'test_result_projection_retains_metadata_and_controls'),
 ('unbound-paired-source',SCRIPT,
  [("src['run'] == run and src['path'] ==\n                f'docs/research/reference-runs/{run}/{case_id}/{names[role]}'", "True")],
  'test_rehashed_case_role_result_source_swaps'),
 ('foreign-span-fallback',HELPER,
  [("if !ok || !valid {\n\t\treturn nil\n\t}", "if !valid { return nil }; if !ok { raw := v.Export(); if x.Offset+x.Length > len(raw) { return nil }; b = raw[x.Offset:x.Offset+x.Length] }")],
  'test_reader_ownership_and_race_go')]
rows=[]
try:
 for name,path,replacements,test in mutants:
  original=path.read_bytes();s=original.decode()
  for old,new in replacements:
   assert s.count(old)==1,(name,old,s.count(old));s=s.replace(old,new)
  path.write_text(s)
  if path==SCRIPT:ast.parse(s)
  (E/('mutant-'+name+('.py.txt'if path==SCRIPT else'.go.txt'))).write_text(s)
  start=time.monotonic()
  if path==HELPER:
   sp=importlib.util.spec_from_file_location('checker',SCRIPT);c=importlib.util.module_from_spec(sp);sp.loader.exec_module(c)
   with c.Session(ROOT) as session:
    session.build_proof();(E/'mutant-foreign-span-composition.json').write_text(json.dumps(session.receipt,indent=2)+'\n')
    code,out,err=c.bounded(['go','test','-count=1','-run','TestPublicOwnedBoundary','./internal/secondary-contract'],session.cwd)
   p=subprocess.CompletedProcess(['go','test'],code,out,err)
  else:p=subprocess.run([sys.executable,str(TEST),'-k',test],cwd=ROOT,capture_output=True,timeout=120)
  log=p.stdout+p.stderr;(E/('mutant-'+name+'.log')).write_bytes(log)
  # Build success is established by setUpClass's real Go build, and Go mutant
  # specifically must reach its semantic assertion, not a compiler failure.
  assert p.returncode==1 and (b'FAILED (failures='in log or (path==HELPER and b'helper accepted foreign span'in log)),(name,p.returncode,log[-2000:])
  if path==HELPER:assert b'helper accepted foreign span'in log,log
  assert b'AuthorityBinding'not in log and b'syntax error'not in log.lower(),log
  rows.append({'name':name,'test':test,'argv':[sys.executable,str(TEST),'-k',test],
   'exit':p.returncode,'seconds':time.monotonic()-start,'compiled_and_semantically_killed':True,
   'mutant_sha256':H(s.encode()),'log_sha256':H(log)})
  path.write_bytes(original)
finally:
 SCRIPT.write_bytes(base);HELPER.write_bytes(gobase)
assert SCRIPT.read_bytes()==base and HELPER.read_bytes()==gobase
(E/'mutation-results.json').write_text(json.dumps({'mutants':rows,'restored_exact_source_sha256':H(base),'restored_exact_helper_sha256':H(gobase),'approved_native50_never_changed':True},indent=2)+'\n')
print(json.dumps({'killed':len(rows),'sources_restored':True}))
