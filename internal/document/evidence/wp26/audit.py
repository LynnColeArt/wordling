#!/usr/bin/env python3
"""Offline complete Go-candidate/native/stream/source audit; never starts a guest."""
import hashlib,importlib.util,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
invocation=module('wp26_invocation',HERE/'reference/invoke.py')
association=module('wp26_associations',HERE/'associations.py')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,why):
 if not ok:raise ValueError(why)
def run():
 plan=invocation.check();semantic=association.run();batch=json.loads((HERE/'reference/batch-result.json').read_text())
 expected={(c['name'],repeat)for c in plan['unique_whole_byte_candidates']for repeat in(1,2)}
 require(len(batch['attempts'])==14 and not batch['skipped']and 'active'not in batch,'Incomplete finite14 original batch')
 require({(a['name'],a['repeat'])for a in batch['attempts']}==expected,'Wrong original branches/repetitions')
 raw_count=raw_bytes=0;rows=[];native_paths=[];drives=set()
 invocation.classify_reader.HERE=HERE/'reference/frozen-source/docs/research/continuation/native-edits'
 for attempt in batch['attempts']:
  require(attempt['result']=='complete','Failed original attempt retained, cannot accept')
  identity=f"wp26-candidate-{attempt['name']}-r{attempt['repeat']}";directory=HERE/'reference/runs'/identity
  r=json.loads((directory/'run.json').read_text());pre=json.loads((HERE/'reference/invocations'/(identity+'.json')).read_text())
  require(r['run_id']==identity and pre['run_id']==identity,'Wrong run identity')
  require(pre['function_call']=={'call':'invoke','name':attempt['name'],'repeat':attempt['repeat']},'Wrong actual per-run invocation')
  require(r['runtime']=={'socket':'/home/lynn/projects/wordling/research/cache/reference/runtime/wp26.sock','lock':'/home/lynn/projects/wordling/research/cache/reference/session1.lock'},'Wrong actual shared runtime/lock')
  require(r['master_unchanged']and r['seed_unchanged']and r['result']=='observed'and r['clean_exit'],'Original/master/seed incomplete')
  for name,record in pre['executing_sources'].items():
   actual=ROOT/name;archive=ROOT/record['archive']
   require(sha(actual)==sha(archive)==record['sha256'],'Changed executing/archived source: '+name)
   require(not archive.name.endswith('.go'),'Active archival Go source package')
  require(r['runner_sources'],'Missing actual runner archive')
  for item in r['artifacts']:
   p=directory/item['path'];require(p.stat().st_size==item['size']and sha(p)==item['sha256'],'Raw original bytes changed: '+str(p));raw_count+=1;raw_bytes+=item['size']
  candidate=HERE/'candidates'/attempt['name']/'candidate.WP5'
  require(candidate.read_bytes()==(directory/'inputs/candidate.WP5').read_bytes(),'Candidate guest seed is not actual Go output')
  require(sha(candidate)==r['candidate']['candidate_sha256'],'Candidate provenance changed')
  require(r['exports']and all((directory/x['path']).stat().st_size==x['size']and sha(directory/x['path'])==x['sha256']for x in r['exports']),'Missing/mutated stopped native extraction')
  qemu=r['qemu_argv'];private=[qemu[i+1]for i,v in enumerate(qemu[:-1])if v=='-drive']
  require(any('candidate.img'in x and'readonly=on'in x for x in private),'Candidate seed not readonly')
  for drive in private:
   if 'native-edit-runs/'in drive and('boot.img'in drive or'harddisk.img'in drive):
    require(drive not in drives,'Private original drive reused');drives.add(drive)
  result=invocation.cm.compare(directory,r)
  require(result['accepted']and result==json.loads((directory/'comparison.json').read_text()),'Exact original candidate comparison does not reproduce')
  native_paths.extend(str(p.resolve())for p in sorted(directory.glob('*.WP5')));native_paths.append(str((directory/'inputs/candidate.WP5').resolve()))
  rows.append({'run_id':identity,'accepted':True,'manifest_sha256':sha(directory/'run.json'),'complete_stream_sha256':sha(directory/r['cases'][0]['print_stream']),'candidate_sha256':sha(candidate)})
 require(len(drives)==28,'Fresh original boot/harddisk count differs')
 # Existing approved external client calls the current actual Document API, not
 # only the framing reader. All outputs retain opaque/deleted metadata literally.
 command=['go','run','./internal/document/evidence/wp25/reopen',*native_paths]
 reopened=json.loads(subprocess.check_output(command,cwd=ROOT,text=True));(HERE/'document-reopen.json').write_text(json.dumps(reopened,indent=2)+'\n')
 return {'scope':'bounded document/history plus actual original candidate interop; no full FR/group/M1/physical claim','source_freeze':'0193d4292f392bdedb56b4707290d0e65f1190fd plus owned inert-archive wrapper fix edcd2e1','semantic_associations':semantic,'original_runs':14,'fresh_private_drives':28,'raw_manifest_artifacts':raw_count,'raw_manifest_bytes':raw_bytes,'actual_document_reopen_paths':len(reopened['files']),'runs':rows}
if __name__=='__main__':
 x=run();(HERE/'audit-result.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps({k:v for k,v in x.items()if k!='runs'},indent=2))
