#!/usr/bin/env python3
"""Audit exact canonical semantics, accepted original states and sealed source bytes."""
import copy
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).parent

def audit(rows):
 cases={c['id']:c for c in json.loads((ROOT/'docs/research/command-scenarios.json').read_text())}
 index=json.loads((ROOT/'docs/research/continuation/session1/state-index.json').read_text())
 accepted=set(json.loads((ROOT/'docs/research/continuation/session1/accepted-branches.json').read_text())['accepted_run_ids'])
 count=0
 for row in rows:
  case=cases[row['case_id']]
  assert (row['title'],row['feature_ids'])==(case['title'],case['feature_ids'])
  assert case['oracle_status']=='partially-observed'
  branch=index['branches'][row['branch']]
  assert row['case_id'] in branch['case_ids'],'Unrelated valid case cannot substitute'
  assert len(branch['runs'])==2
  for selected in branch['runs']:
   assert selected['run_id'] in accepted
   manifest=ROOT/selected['manifest'];raw=manifest.read_bytes()
   assert hashlib.sha256(raw).hexdigest()==selected['sha256']
   run=json.loads(raw);assert run['scope']=='original-reference-only' and not run['wordling_tested']
   result=next(r for r in run['results'] if r['case_id']==row['case_id'])
   assert result['result']=='observed-matches-smoke-expectations' and all(c['passed'] for c in result['checks'])
   for artifact in result['evidence']:
    data=(ROOT/artifact['path']).read_bytes()
    assert (len(data),hashlib.sha256(data).hexdigest())==(artifact['size'],artifact['sha256'])
   for source in run['runner_sources']:
    assert hashlib.sha256((manifest.parent/'runner-source'/Path(source['path']).name).read_bytes()).hexdigest()==source['sha256']
  for label in row['state_labels']:
   if row['case_id']=='CMD51-019':assert label.endswith('-after'),'Wrong after-initial state'
   if row['case_id']=='CMD51-020':assert label.endswith('-before'),'Wrong before-initial state'
   if row['case_id']=='CMD51-237':assert label.startswith('retrieve-f1-')
   if row['case_id']=='CMD51-238':assert label.startswith('retrieve-esc-')
   facts=branch['states'][label];assert len(facts)==2
   for fact in facts:
    data=(ROOT/fact['screen_path']).read_bytes()
    assert hashlib.sha256(data).hexdigest()==fact['screen_sha256']
    assert Path(fact['screen_path']).parent.name==label
    if row['case_id']=='CMD51-244':
     assert label=='exit-dos-result' and b'C:\\WP51>' in data
     assert fact['hardware_cursor']=={'row':0,'column':8}
   count+=2
 return count

if __name__=='__main__':
 rows=json.loads((HERE/'observations.json').read_text())['observations']
 count=audit(rows)
 # WP11 O6/O7: earlier Reveal toggles use independent original alpha/beta text,
 # not a claim that the domain ORIGIN projection is that complete workflow.
 cases={c['id']:c for c in json.loads((ROOT/'docs/research/command-scenarios.json').read_text())}
 assert cases['CMD51-048']['title']=='Toggle Reveal Codes without editing'
 assert cases['CMD51-048']['feature_ids']==['WP51-013']
 for run_id in ('2026-10-29-smoke-02','2026-10-29-smoke-03'):
  path=ROOT/'docs/research/reference-runs'/run_id/'run.json'
  assert str(path.relative_to(ROOT)) in cases['CMD51-048']['evidence_paths']
  run=json.loads(path.read_text());result=next(r for r in run['results'] if r['case_id']=='CMD51-048')
  assert result['result']=='observed-matches-smoke-expectations'
  for label,cue in [('codes-on','[BOLD]alpha[bold]beta'),('codes-off','alphabeta')]:
   artifact=next(a for a in result['evidence'] if a['path'].endswith('/'+label+'/screen.txt'))
   data=(ROOT/artifact['path']).read_bytes()
   assert cue in data.decode() and hashlib.sha256(data).hexdigest()==artifact['sha256']
 bad=copy.deepcopy(rows)
 cases={c['id']:c for c in json.loads((ROOT/'docs/research/command-scenarios.json').read_text())}
 wrong=cases['CMD51-001']
 bad[0].update({k:wrong[k] for k in ('title','feature_ids')});bad[0]['case_id']=wrong['id']
 try:audit(bad)
 except (AssertionError,KeyError):pass
 else:raise AssertionError('Wrong-feature negative accepted')
 bad=copy.deepcopy(rows);bad[-1]['state_labels']=['exit-choice-result']
 try:audit(bad)
 except (AssertionError,KeyError):pass
 else:raise AssertionError('Stale quit terminal negative accepted')
 bad=copy.deepcopy(rows);next(r for r in bad if r['case_id']=='CMD51-019')['state_labels']=['prefix-normal-before']
 try:audit(bad)
 except (AssertionError,KeyError):pass
 else:raise AssertionError('Wrong same-feature cursor state accepted')
 print(f'Validated{len(rows)} semantic associations/{count} WP13 state witnesses, four WP11 Reveal witnesses and three negatives; no original execution.')
