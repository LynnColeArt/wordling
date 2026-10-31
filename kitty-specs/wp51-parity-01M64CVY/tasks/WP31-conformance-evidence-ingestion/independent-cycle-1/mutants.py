from pathlib import Path
import json,subprocess,sys,tempfile
ROOT=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-m');OUT=Path('/tmp/wordling-WP31-independent-review/mutants');OUT.mkdir(exist_ok=False)
w=(ROOT/'scripts/conformance/v1/ingest_wp29.py').read_text();c=(ROOT/'scripts/conformance/v1/conformance.py').read_text();rows=[]
for name,old,new,test in [('source-admission',"    inputs = product['product_inputs']","    return\n    inputs = product['product_inputs']",'test_missing_extra_changed_sources_and_wrong_compiled_set'),('forced-review',"event['force'] is False",'True','test_actual_review_event_rejects_force_actor_result_or_missing_identity'),('import-identity','    expected, _ = proposed(root, BUNDLE_COMMIT)','    return\n    expected, _ = proposed(root, BUNDLE_COMMIT)',None)]:
 d=OUT/name;d.mkdir();assert w.count(old)==1;mut=w.replace(old,new);compile(mut,str(d/'ingest_wp29.py'),'exec');(d/'ingest_wp29.py').write_text(mut);(d/'conformance.py').write_text(c)
 if test:
  driver=d/'driver.py';driver.write_text('import sys,unittest,importlib.util\nsys.path.insert(0,'+repr(str(d))+')\nimport ingest_wp29\nspec=importlib.util.spec_from_file_location("tests",'+repr(str(ROOT/'tests/conformance/v1/test_ingestion.py'))+')\nm=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)\nr=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([m.SourceJoin("test_actual_complete_source_join"),m.SourceJoin('+repr(test)+')]))\nsys.exit(not r.wasSuccessful())\n')
  p=subprocess.run([sys.executable,str(driver)],capture_output=True,text=True,timeout=90);raw=p.stdout+p.stderr;assert p.returncode==1 and '... ok' in raw and 'AssertionError' in raw,raw
  rows.append({'mutant':name,'baseline_actual_source_join_passed':True,'killed_by_behavioral_assertion':True,'exit':p.returncode});(d/'result.txt').write_text(raw)
 else:
  proposal=json.loads((ROOT/'docs/conformance/v1/registry.json').read_text());proposal['evidence'][0]['id']='WP29-forged-renamed-identity';q=d/'proposal.json';q.write_text(json.dumps(proposal));outcomes=[]
  for label,cli in [('actual',ROOT/'scripts/conformance/v1/conformance.py'),('mutant',d/'conformance.py')]:
   p=subprocess.run([sys.executable,str(cli),'--root',str(ROOT),'validate','--registry',str(q)],capture_output=True,text=True,timeout=120);(d/(label+'.txt')).write_text(p.stdout+p.stderr);outcomes.append(p.returncode)
  assert outcomes==[1,0],outcomes;rows.append({'mutant':name,'actual_refuses':1,'mutant_accepts':0,'killed_by_public_negative':True})
(OUT/'results.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows))
