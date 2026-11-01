"""Reproduce the finite source index from immutable, already reviewed planning data.
No native parsing/mutation, guest, imports of archived code or private disk access.
"""
from pathlib import Path
import hashlib,json,subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
AUTHORITY='c026805e6936f01cf946974fdf0b9bf35bc0122f'
BASE='docs/research/continuation/retrieve-field-history-task-review/proposal-revision2/kitty-specs/wp51-parity-01M64CVY/tasks/WP54-retrieve-field-history-contract/provenance/Retrieve-recon/'
def original(path):
 return subprocess.run(['git','show',AUTHORITY+':'+path],cwd=ROOT,capture_output=True,check=True,timeout=20).stdout
def build():
 proof=json.loads(original(BASE+'source-proof.json.txt.txt'));coverage=json.loads(original(BASE+'second-retrieve-coverage.json.txt.txt'));items={}
 for row in proof['files']:
  items[(row['source_commit'],row['path'])]={k:row[k]for k in ['source_commit','path','size','sha256','git_blob']}
 for group in coverage['inventories']:
  for row in group['scanned_screens']:
   key=(group['ref'],row['path']);pin=dict(row,source_commit=group['ref']);items.setdefault(key,pin)
 data=dict(schema='wordling.retrieve.sources/v1',planning_authority=AUTHORITY,refs=proof['refs'],files=[items[k]for k in sorted(items)],copied_sources=269,inventory_screens=1085,inventory_roots=[{k:g[k]for k in ['ref','root','screen_count']}for g in coverage['inventories']],approved51_event='01M69KR6RPZBA9WXQJYPEWZBW8',approved51_source='5975c5f72775f3b3c07675ecb806c460886c9027')
 helper=subprocess.run(['git','show',proof['refs']['approved13']+':scripts/reference/qmp.py'],cwd=ROOT,capture_output=True,check=True,timeout=20).stdout
 data['helper']=dict(source_commit=proof['refs']['approved13'],path='scripts/reference/qmp.py',size=len(helper),sha256=hashlib.sha256(helper).hexdigest(),public_API='QMP.text')
 return (json.dumps(data,indent=2)+'\n').encode()
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args();raw=build();target=HERE/'source-index.json'
 if a.check:
  if target.read_bytes()!=raw:raise SystemExit('source-index drift')
 else:target.write_bytes(raw)
 print(json.dumps(dict(files=len(json.loads(raw)['files']),size=len(raw),sha256=hashlib.sha256(raw).hexdigest(),no_native_guest_or_private_input=True)))
