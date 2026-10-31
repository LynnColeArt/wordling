#!/usr/bin/env python3
"""Owned14-candidate invocation; approved WP23 reference engine unchanged.

No VM at import/check. Explicit destination routing and a short per-WP socket are
owned configuration adapters; no native/edit/print/exit semantic helper is patched.
"""
import argparse,hashlib,json,shutil,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
APPROVED=ROOT/'docs/research/continuation/native-edits'
sys.path[:0]=[str(ROOT/'scripts/reference'),str(APPROVED)]
import native_edits as n
import candidate_mode as cm
import classify_reader
CANDIDATES=HERE.parent/'candidates'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def frozen_sources():
 result={}
 paths=[*APPROVED.glob('*.py'),*APPROVED.glob('*.json'),APPROVED/'reader_probe.go.txt',*sorted((ROOT/'scripts/reference').glob('*.py')),*sorted((ROOT/'internal/document').glob('*.go')),ROOT/'internal/wp51/native.go',HERE/'invoke.py',HERE/'batch.py',HERE/'plan.json',HERE.parent/'producer/main.go']
 for p in paths:
  relative=p.relative_to(ROOT);target=HERE/'frozen-source'/relative
  target.parent.mkdir(parents=True,exist_ok=True)
  if target.exists()and target.read_bytes()!=p.read_bytes():raise ValueError('Frozen executing source changed: '+str(relative))
  if not target.exists():shutil.copyfile(p,target)
  result[str(relative)]={'sha256':sha(p),'archive':str(target.relative_to(ROOT))}
 return result

def check():
 if Path.cwd()!=ROOT:raise ValueError('Run from actual declared lane checkout')
 plan=json.loads((CANDIDATES/'sealed-plan.json').read_text())
 assert len(plan['cases'])==23 and len(plan['unique_whole_byte_candidates'])==7 and plan['guest_count']==14
 for p,digest in plan['source_hashes'].items():assert sha(ROOT/p)==digest,p
 for c in plan['cases']:
  directory=CANDIDATES/c['name'];alias=CANDIDATES/c['whole_byte_alias_of']
  assert (directory/'candidate.WP5').read_bytes()==(alias/'candidate.WP5').read_bytes(),c['name']
  for filename,field in [('candidate.WP5','candidate_sha256'),('provenance.json','provenance_sha256'),('expectations.json','expectations_sha256')]:assert sha(directory/filename)==c[field],(c['name'],filename)
  cm.prepare(directory/'candidate.WP5',directory/'provenance.json',directory/'expectations.json')
 return plan

def invoke(name,repeat):
 plan=check()
 if repeat not in(1,2)or name not in[c['name']for c in plan['unique_whole_byte_candidates']]:raise ValueError('Only sealed seven classes x two fresh repetitions')
 sources=frozen_sources();directory=CANDIDATES/name
 prepared=cm.prepare(directory/'candidate.WP5',directory/'provenance.json',directory/'expectations.json')
 run_id=f'wp26-candidate-{name}-r{repeat}'
 invocations=HERE/'invocations';invocations.mkdir(exist_ok=True);invocation=invocations/(run_id+'.json')
 if invocation.exists():raise FileExistsError('Fresh original invocation required')
 write(invocation,{'scheduler_argv':sys.argv,'function_call':{'call':'invoke','name':name,'repeat':repeat},'run_id':run_id,'name':name,'repeat':repeat,'executing_sources':sources,'prepared_metadata':prepared['metadata'],'routing':'n.OUT=owned reference during execute; approved configure then qmp/guest socket=primary/runtime/wp26.sock; classify_reader.HERE=owned reference only for temporary unchanged reader client','engine_sha256':sha(n.__file__),'master':'private unchanged primary master; fresh execute work identity, normal original exit then stopped extraction under shared session1.lock'})
 original_out=n.OUT;original_configure=n.configure
 def configure():
  original_configure()
  for module in(n.guest,n.qmp):module.SOCKET=n.PRIVATE/'runtime/wp26.sock'
 try:
  n.OUT=HERE;n.configure=configure;configure()
  r=n.execute(run_id,'candidate',lambda p:cm.run(p,prepared),prepared)
 finally:n.OUT=original_out;n.configure=original_configure
 classify_reader.HERE=HERE/'frozen-source/docs/research/continuation/native-edits'
 result=cm.compare(HERE/'runs'/run_id,r)if r['result']=='observed'else{'accepted':False,'run_error':r.get('error')}
 write(HERE/'runs'/run_id/'comparison.json',result)
 if not result['accepted']:raise ValueError('Original candidate interoperability incomplete: '+run_id)
 print(run_id,'accepted exact candidate interoperability',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['check','run']);p.add_argument('--name');p.add_argument('--repeat',type=int);a=p.parse_args()
 if a.command=='check':x=check();print(json.dumps({'status':'sealed offline input checks pass; NO guest','semantic_outputs':len(x['cases']),'whole_native_classes':7,'guests':14}))
 else:invoke(a.name,a.repeat)
