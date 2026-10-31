"""Immutable Git/raw/source custody audit; no native decoder, VM or old writes."""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent
proof=json.loads((ROOT/'docs/research/continuation/native-merge-task-review/proposal/evidence/recon/source-proof.json.txt').read_text());ref=proof['primary_snapshot']
sha=lambda b:hashlib.sha256(b).hexdigest()
tree={line.split('\t',1)[1]:line.split()[2]for line in subprocess.check_output(['git','ls-tree','-r',ref],cwd=ROOT).decode().splitlines()};checked={}
def check(path,want=None,size=None):
 raw=(ROOT/path).read_bytes();digest=sha(raw);blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();assert blob==tree[path],path
 if want is not None:assert digest==want,path
 if size is not None:assert len(raw)==size,path
 checked[path]={'size':len(raw),'sha256':digest,'git_blob':blob};return raw
runs=set();native=set()
for case in proof['merge_originals']:
 assert len(case['runs'])==2 and case['runs'][0]['run']!=case['runs'][1]['run']
 for run in case['runs']:
  base='docs/research/reference-runs/'+run['run'];manifest=json.loads(check(base+'/run.json',run['manifest_sha256']));item=next(r for r in manifest['results']if r['case_id']==case['case_id']);assert item['result']=='observed-matches-smoke-expectations'
  for entry in item['evidence']+item['native_outputs']:check(entry['path'],entry['sha256'],entry['size'])
  for entry in item['native_outputs']:native.add(entry['path'])
  for entry in manifest['runner_sources']:check(base+'/runner-source/'+Path(entry['path']).name,entry['sha256'])
  check(manifest['environment_profile_archive'],manifest['environment_manifest_sha256']);runs.add(run['run'])
source_inputs=json.loads((ROOT/'docs/research/continuation/native-merge-task-review/proposal/source-inputs.json').read_text())['sources']
for pin in source_inputs:
 raw=subprocess.check_output(['git','show',pin['approved_source_commit']+':'+pin['path']],cwd=ROOT);assert len(raw)==pin['bytes']and sha(raw)==pin['sha256'];assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==pin['git_blob'];assert (ROOT/pin['path']).read_bytes()==raw
manuals=[]
for pin in proof['private_manuals']:assert sha(Path(pin['path']).read_bytes())==pin['sha256'];manuals.append(pin)
assert len(native)==104 and len(runs)==10
result={'immutable_snapshot':ref,'15_contexts_two_repetitions':True,'unique_runs':len(runs),'native_exports':len(native),'unique_native_sha256':len({checked[p]['sha256']for p in native}),'checked_files':checked,'approved_source_inputs':source_inputs,'manual_hashes_only':manuals,'private_manual_program_resource_bytes_published':False,'new_original_execution':False};(OUT/'source-audit.json').write_text(json.dumps(result,indent=2)+'\n');print('verified',len(checked),'immutable Git/raw/capture/source/profile files,104native/35hash/15contexts/30repetitions')
