import json,copy,sys,hashlib
from pathlib import Path
ROOT=Path.cwd();H=ROOT/'docs/research/continuation/text-layout'
sys.path.insert(0,str(ROOT/'scripts/reference'));import text_layout
plan=json.loads((H/'recipe-plan.json').read_text());cases={c['id']:c for c in json.loads((ROOT/'docs/research/command-scenarios.json').read_text())}
def check(rows):
 for row in rows:
  frozen={k:v for k,v in row.items() if k not in ('id','canonical_cases')}
  assert frozen==text_layout.VARIANTS[row['id']]
  assert [x['id'] for x in row['canonical_cases']]==row['cases']
  for c in row['canonical_cases']:
   assert all(c[k]==cases[c['id']][k] for k in c)
  for path in (H/'runs').glob('*/run.json'):
   r=json.loads(path.read_text())
   if r['variant']==row['id'] and r['result']=='observed-local-variant':assert r['variant_input']==frozen
check(plan['variants'])
bad=copy.deepcopy(plan['variants']);bad[0]['text']='changed text'
try:check(bad)
except AssertionError:pass
else:raise AssertionError('Changed frozen input accepted')
bad=copy.deepcopy(plan['variants']);bad[0]['cases']=['CMD51-001'];bad[0]['canonical_cases']=[{k:cases['CMD51-001'][k] for k in ('id','title','feature_ids','oracle_status')}]
try:check(bad)
except AssertionError:pass
else:raise AssertionError('Valid wrong-feature replacement accepted')
for source in json.loads((H/'source-manifest.json').read_text())['historical_input_hashes']:
 p=Path(source['path']);p=p if p.is_absolute() else ROOT/p
 assert p.stat().st_size==source['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==source['sha256']
# Compile sources without touching even bytecode files.
for p in [ROOT/'scripts/reference/text_layout.py',H/'analyze.py',H/'verify.py',H/'test_analysis.py']:compile(p.read_text(),str(p),'exec')
print('Nine exact frozen recipe definitions, canonical semantic leads and historical profile/master/firmware hashes pass; changed-input and valid wrong-feature substitutions fail. Python compile passes.')
