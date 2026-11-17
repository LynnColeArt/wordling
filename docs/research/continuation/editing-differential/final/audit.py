"""Read-only final WP29 evidence audit. No app or original guest is launched.

Use --git-ref HEAD after committing to compare every artifact to its Git blob.
Actual executions and synthetic negative mutations remain separately archived.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'scripts/reference'))
import wordling_edits as w

def main():
 p=argparse.ArgumentParser();p.add_argument('--git-ref');args=p.parse_args()
 _,plan=w.check_plan();out=w.OUT;verdict=json.loads((out/'final/verdict.json').read_text())
 assert verdict['original_attempts_inclusive']==19 and verdict['successor']['accepted']==16
 ledger=json.loads((w.ORACLE/'ledger.json').read_text())
 assert not ledger['halted']and len(ledger['attempts'])==16 and ledger['prior_spent_attempts']==3 and ledger['cumulative_cap']==19
 expected=plan['original_leaves'];resources=[]
 for i,leaf in enumerate(expected):
  a=ledger['attempts'][i];assert a['leaf']==leaf and a['outcome']=='accepted'and a['guest_start_requested_at']
  d=w.ORACLE/'runs'/('wp29-s01-'+leaf['id']);run=json.loads((d/'run.json').read_text());w.validate_owned_run(d,run)
  assert w.safe_original_compare(d,run)['accepted']
  for source in w.APPROVED.glob('*.py'):assert (d/'approved-helper-inputs'/source.name).read_bytes()==source.read_bytes()
  for source in w.APPROVED.glob('*.json'):assert (d/'approved-helper-inputs'/source.name).read_bytes()==source.read_bytes()
  assert (d/'comparison-configuration/field-ledger.json').read_bytes()==(w.ORACLE/'field-ledger.json').read_bytes()
  release=json.loads((d/'oracle-slot-release.json').read_text());assert release['owned_process_stop_confirmed']and release['before_offline_comparison']
  assert json.loads((d/'leaf-complete.json').read_text())['outcome']=='accepted';resources.append(run['resources'])
 assert all(r==resources[0]for r in resources)
 installed=json.loads((ROOT/'docs/research/reference-environment/installed-files.json').read_text())['files']
 by={Path(r['path']).name.upper():r for r in installed}
 for resource in resources[0]:
  if resource['path']=='WP{WP}.SET':continue
  pin=by[resource['path']];assert all(pin[k]==resource[k]for k in ['size','sha256'])
 report=json.loads((out/'reopen/successor-01/reopen-report.json').read_text());assert report['paths']==60 and len(report['unique_whole_native_inputs'])==29 and len(report['aliases'])==31
 events=[b'\x1b[?31u',w.KEYS['retrieve'],b'ORIGIN',w.KEYS['enter'],w.KEYS['save'],b'CANDIDA',w.KEYS['enter'],b'X',w.KEYS['f7'],w.KEYS['f1'],w.KEYS['f7'],b'n',b'y']
 classified={'recognized-readonly-refused-edit':0,'mutation-admitted-at-this-specific-gap':0};workers=set();expected_paths=set()
 for leaf in expected:
  directory=w.ORACLE/'runs'/('wp29-s01-'+leaf['id']);run=json.loads((directory/'run.json').read_text());expected_paths.update(str(directory/r['path'])for r in run['exports']if r['path'].upper().endswith('.WP5'))
 for repeat in [1,2]:
  directory=out/'oracle/runs'/('wp29-history-control-r'+str(repeat));run=json.loads((directory/'run.json').read_text());expected_paths.update(str(directory/r['path'])for r in run['exports']if r['path'].upper().endswith('.WP5'))
 assert len(expected_paths)==60
 for row in report['unique_whole_native_inputs']:
  d=ROOT/row['folder'];process=json.loads((d/'process.json').read_text());frames=w.replay_frames(d)
  assert process['returncode']==0 and process['error']is None and process['binary']==plan['binary']
  assert process['argv']==[plan['binary_path'],'-root',str((d/'files').resolve()),'-profile','local-flat']
  assert process['pid_identity']['pid']==process['pid']and process['pid_identity']['start_ticks']>0
  assert bytes.fromhex(process['pid_identity']['argv_hex']).split(b'\0')[:-1]==[x.encode()for x in process['argv']]
  assert [x['hex']for x in json.loads((d/'injected.json').read_text())]==[e.hex()for e in events]
  w.publication_witness(frames,'CANDIDA',0);assert frames[-1]['state']['mode']=='ExitQuestion'
  source=Path(row['source']).read_bytes();assert source==(d/'files/ORIGIN').read_bytes()==(d/'files/CANDIDA').read_bytes()
  assert w.identity(d/'files/ORIGIN')==process['before_source']==row['identity'];classified[row['actual_mutation_probe']]+=1
  probe=next(f for f in frames if f['label']=='actual mutation admission probe, not saved');assert probe==row['probe_frame']
  if row['actual_mutation_probe']=='recognized-readonly-refused-edit':
   assert not probe['state']['dirty']and probe['state']['gap']==0 and 'document: UnsupportedPrefix at token -1, span 0+564'in '\n'.join(probe['screen']['rows'])
  else:assert probe['state']['dirty']and probe['state']['gap']==1
  workers.add((process['pid'],process['pid_identity']['start_ticks']))
 for alias in report['aliases']:
  a=Path(alias['source']);b=Path(alias['whole_native_alias_of']);assert a.read_bytes()==b.read_bytes()and w.identity(a)==w.identity(b)==alias['identity']
 assert classified=={'recognized-readonly-refused-edit':27,'mutation-admitted-at-this-specific-gap':2}and len(workers)==29
 assert {r['source']for r in report['unique_whole_native_inputs']}|{r['source']for r in report['aliases']}==expected_paths
 assert all(r['whole_native_alias_of']in{u['source']for u in report['unique_whole_native_inputs']}for r in report['aliases'])
 assert json.loads((out/'negative-results.json').read_text())['all_rejected']
 assert w.identity(out/'oracle/ledger.json')['sha256']==w.OLD_LEDGER and not(out/'oracle/field-ledger.json').exists()
 manifest_path=out/'final/artifact-manifest.json'
 if manifest_path.exists():
  manifest=json.loads(manifest_path.read_text())
  for r in manifest['records']:w.regular_exact(ROOT/r['path'],{k:r[k]for k in ['size','sha256']},'FinalArtifactChanged')
  if args.git_ref:
   import tempfile
   with tempfile.TemporaryFile()as requests:
    requests.write(''.join(args.git_ref+':'+r['path']+'\n'for r in manifest['records']).encode());requests.seek(0)
    proc=subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=requests,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for r in manifest['records']:
     header=proc.stdout.readline().split();assert len(header)==3 and header[1]==b'blob';size=int(header[2]);left=size;digest=hashlib.sha256()
     while left:
      chunk=proc.stdout.read(min(left,65536));assert chunk;digest.update(chunk);left-=len(chunk)
     assert proc.stdout.read(1)==b'\n'and size==r['size']and digest.hexdigest()==r['sha256'],r['path']
    assert proc.stdout.read(1)==b'';assert proc.wait(timeout=60)==0,proc.stderr.read().decode()
 print(json.dumps({'static_audit':'pass','successor_originals':16,'prior_controls':2,'historical_candidate_incomplete':1,'cumulative_attempts':19,'actual_app_reopens':29,'native_paths':60,'readonly':27,'initial_gap_edit_admitted':2,'guest_or_app_launched_by_audit':False,'Git_ref':args.git_ref}))
if __name__=='__main__':main()
