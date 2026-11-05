#!/usr/bin/env python3
"""Fault real approved candidate comparator on temporary rehashed witnesses."""
import copy,hashlib,importlib.util,json,os,shutil,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
spec=importlib.util.spec_from_file_location('wp26_negative_invocation',HERE/'reference/invoke.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.classify_reader.HERE=HERE/'reference/frozen-source/docs/research/continuation/native-edits'
original=HERE/'reference/runs/wp26-candidate-closing-restore-marker-r2'
run=json.loads((original/'run.json').read_text());case=run['cases'][0]
sha=lambda b:hashlib.sha256(b).hexdigest()
before={x['path']:sha((original/x['path']).read_bytes())for x in run['artifacts']}
rows=[]
def changed_file(directory,record,path,data):
 p=directory/path;p.unlink();p.write_bytes(data)
 found=False
 for x in record['artifacts']:
  if x['path']==path:x.update(size=len(data),sha256=sha(data));found=True
 assert found,path
for name in ['wrong-semantic-lead','changed-native-body','changed-complete-print','stale-final-VGA']:
 with tempfile.TemporaryDirectory(prefix='negative-',dir=HERE)as temporary:
  directory=Path(temporary)/'run';shutil.copytree(original,directory,copy_function=os.symlink)
  record=copy.deepcopy(run);required=None
  if name=='wrong-semantic-lead':record['cases'][0]['canonical_leads']=['CMD51-200'];required='candidate semantic case association'
  elif name=='changed-native-body':
   path=case['edited'];data=bytearray((directory/path).read_bytes());assert data[-1]==ord('Z');data[-1]=ord('Y');changed_file(directory,record,path,data);required='exact edited native body'
  elif name=='changed-complete-print':
   path=case['print_stream'];data=bytearray((directory/path).read_bytes());assert data[-1]==10;data[-1]=13;changed_file(directory,record,path,data);required='exact complete reference printer bytes'
  else:
   data=(directory/'candidate-before-subsequent-edit/vram.bin').read_bytes();changed_file(directory,record,'clean-exit/vram.bin',data);required='Final state differs from exact approved post-DOS-wait vram.bin'
  result=m.cm.compare(directory,record)
  failed=[x['check']for x in result['checks']if not x['passed']]
  assert not result['accepted']and required in failed,(name,result)
  if name!='wrong-semantic-lead':assert 'raw manifest artifacts unchanged'not in failed,(name,'checksum-only failure')
  rows.append({'name':name,'accepted':result['accepted'],'required_semantic_rejection':required,'actual_failed_checks':failed,'temporary_only':True,'mutated_artifact_envelope_rehashed':name!='wrong-semantic-lead'})
assert before=={x['path']:sha((original/x['path']).read_bytes())for x in run['artifacts']}
(HERE/'interop-negatives.json').write_text(json.dumps({'entrypoint':'unchanged approved candidate_mode.compare','actual_raw_witnesses_unchanged':True,'cases':rows},indent=2)+'\n')
print(len(rows),'real comparator faults rejected; originals unchanged')
