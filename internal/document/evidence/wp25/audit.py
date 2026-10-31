#!/usr/bin/env python3
"""Reproduce WP25 custody, semantic association and exact original audit offline."""
import hashlib,importlib.util,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
spec=importlib.util.spec_from_file_location('wp25invocation',HERE/'reference/invoke.py');invocation=importlib.util.module_from_spec(spec);spec.loader.exec_module(invocation)
sha=lambda b:hashlib.sha256(b).hexdigest()

def associations(rows):
 catalogue={r['id']:r for r in json.loads((ROOT/'docs/research/command-scenarios.json').read_text())}
 inventory={r['id']:r for r in json.loads((ROOT/'docs/research/feature-inventory.json').read_text())}
 expected={'CMD51-046':('Toggle typeover and return to insertion','WP51-012'), 'CMD51-047':('Typeover stops short of a code','WP51-012'), 'CMD51-048':('Toggle Reveal Codes without editing','WP51-013'), 'CMD51-149':('Preserve an untouched native file byte for byte','WP51-020'), 'CMD51-065':('Retrieve inserts at the cursor','WP51-019'), 'CMD51-066':('Name a new document with F10','WP51-020'), 'CMD51-145':('Direct original printer output to a disk file','WP51-074')}
 if len(rows)!=len(expected) or {r['id'] for r in rows}!=set(expected):raise ValueError('Wrong semantic case set')
 for row in rows:
  title,feature=expected[row['id']];case=catalogue[row['id']]
  if row['feature_id']!=feature or case['feature_ids']!=[feature]:raise ValueError('Wrong feature association')
  if row['title']!=title or case['title']!=title:raise ValueError('Wrong semantic title')
  if inventory[feature]['title']!=row['feature_title'] or row['id'] not in inventory[feature]['command_scenario_ids']:raise ValueError('Wrong inventory title/membership')
  if not row.get('local_scope'):raise ValueError('Missing bounded scope')
 return len(rows)

def audit():
 plan=json.loads((HERE/'candidates/sealed-plan.json').read_text());cases={r['name']:r for r in plan['cases']}
 for source,digest in plan['source_hashes'].items():
  if sha((ROOT/source).read_bytes())!=digest:raise ValueError('Pinned Go/source changed: '+source)
 rows=json.loads((HERE/'associations.json').read_text());count=associations(rows)
 # Demonstrate a valid-but-unrelated canonical ID/feature cannot satisfy the map.
 wrong=json.loads(json.dumps(rows));wrong[0]['feature_id']='WP51-013'
 try:associations(wrong)
 except ValueError as e:negative=str(e)
 else:raise ValueError('Wrong-feature negative survived')
 if negative!='Wrong feature association':raise ValueError('Negative failed for wrong reason')
 batch=json.loads((HERE/'reference/batch-result.json').read_text())
 if len(batch['attempts'])!=12 or batch['skipped'] or any(r['result']!='completed' for r in batch['attempts']) or 'active' in batch:raise ValueError('Incomplete sealed12 batch')
 raw_count=raw_bytes=0;run_rows=[];paths=[]
 invocation.classify_reader.HERE=HERE/'reference'
 for attempt in batch['attempts']:
  identity=f"wp25-{attempt['kind']}-{attempt['name']}-r{attempt['repeat']}";directory=HERE/'reference/runs'/identity
  run=json.loads((directory/'run.json').read_text());pre=json.loads((HERE/'reference/invocations'/(identity+'.json')).read_text())
  for record in run['artifacts']:
   data=(directory/record['path']).read_bytes()
   if len(data)!=record['size'] or sha(data)!=record['sha256']:raise ValueError('Changed raw witness: '+str(directory/record['path']))
   raw_count+=1;raw_bytes+=len(data)
  for source,record in pre['executing_sources'].items():
   if sha(Path(source).read_bytes())!=record['sha256']:raise ValueError('Executing source changed: '+source)
  if run['runtime']!={'socket':'/home/lynn/projects/wordling/research/cache/reference/runtime/qmp.sock','lock':'/home/lynn/projects/wordling/research/cache/reference/session1.lock'}:raise ValueError('Wrong shared runtime/lock')
  if not run['master_unchanged'] or not run['seed_unchanged']:raise ValueError('Original/master seed changed')
  comparison=invocation.cm.compare(directory,run)
  if attempt['kind']=='candidate':
   if not comparison['accepted']:raise ValueError('Original Go candidate comparison failed')
   if comparison!=json.loads((directory/'comparison.json').read_text()):raise ValueError('Candidate comparison does not reproduce')
   candidate=(HERE/'candidates'/attempt['name']/'candidate.WP5').read_bytes()
   if sha(candidate)!=cases[attempt['name']]['candidate_sha256'] or candidate!=(directory/'inputs/candidate.WP5').read_bytes():raise ValueError('Go candidate custody mismatch')
  else:
   expected_failure=['exact complete reference printer bytes']
   if comparison['unresolved']!=expected_failure:raise ValueError('Unresolved control observation')
   if comparison!=json.loads((directory/'candidate-checks-not-a-candidate-verdict.json').read_text()):raise ValueError('Control diagnostic does not reproduce')
   observation=json.loads((directory/'control-observation.json').read_text());case=run['cases'][0]
   before=invocation.codepane_cursor.gap(directory/case['source'],directory/'control-before-typeover-Q')
   after=invocation.codepane_cursor.gap(directory/case['control_final'],directory/'control-after-typeover-Q')
   if (before['gap'],after['gap'])!=(4,5) or before!=observation['before_cursor'] or after!=observation['after_cursor']:raise ValueError('Wrong actual two-pair code gap')
   if invocation.print_audit.audit(directory/case['after_print'],directory/case['print_stream'])!=observation['literal_ink_audit']:raise ValueError('Changed two-pair literal ink')
  for p in sorted(directory.glob('*.WP5')):paths.append(str(p))
  paths.append(str(directory/'inputs/candidate.WP5'))
  run_rows.append({'id':identity,'role':attempt['kind'],'run_manifest_sha256':sha((directory/'run.json').read_bytes()),'candidate_protocol_accepted':comparison['accepted'] if attempt['kind']=='candidate' else 'not applicable; original Q controls qualified independently','all_other_protocol_checks':all(c['passed'] for c in comparison['checks'] if c['check']!='exact complete reference printer bytes')})
 seal=json.loads((HERE/'reference/two-pair-baseline-seal.json').read_text());streams=[]
 for record in seal['streams']:
  data=(ROOT/record['path']).read_bytes();streams.append(data)
  if len(data)!=record['size'] or sha(data)!=record['sha256']:raise ValueError('Changed sealed two-pair print')
 if len(streams)!=2 or streams[0]!=streams[1]:raise ValueError('Original two-pair fresh print mismatch')
 reopened=json.loads(subprocess.check_output(['go','run','./internal/document/evidence/wp25/reopen',*paths],cwd=ROOT,text=True))
 (HERE/'document-reopen.json').write_text(json.dumps(reopened,indent=2)+'\n')
 return {'source_checkpoint':batch['source_commit'],'scope':'bounded library writer/original interoperability, not product/session/whole M1','semantic_associations':count,'wrong_feature_negative':negative,'original_runs':len(run_rows),'go_candidate_runs':10,'original_two_pair_controls':2,'raw_manifest_artifacts':raw_count,'raw_manifest_bytes':raw_bytes,'all_new_native_document_api_reopens':len(reopened['files']),'runs':run_rows}
if __name__=='__main__':
 result=audit();(HERE/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='runs'},indent=2))
