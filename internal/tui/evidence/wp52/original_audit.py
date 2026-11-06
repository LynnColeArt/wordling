#!/usr/bin/env python3
"""Read-only recomputation from actual immutable Git blobs and raw original VGA.
No guest, private media, autocalibration or fixture-derived product output.
"""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def main():
 p=json.loads((HERE/'recon/source-proof.json.txt').read_bytes())
 seals=json.loads((HERE/'recon/seals.json.txt').read_bytes())
 for name,entry in seals['files'].items():
  b=(HERE/'recon'/(name+'.txt')).read_bytes();assert len(b)==entry['bytes'] and sha(b)==entry['sha256']
 for x in p['sources']:
  b=(ROOT/x['path']).read_bytes() if x['path'].startswith('docs/research/continuation/session1/') else subprocess.check_output(['git','show',x['commit']+':'+x['path']],cwd=ROOT)
  assert sha(b)==x['sha256'] and len(b)==x['bytes']
  assert subprocess.check_output(['git','rev-parse',x['commit']+':'+x['path']],cwd=ROOT,text=True).strip()==x['git_blob']
  # Check the actual historical Git object as well as current raw evidence.
  historical=subprocess.check_output(['git','cat-file','blob',x['git_blob']],cwd=ROOT);assert b==historical
 for x in p['original_cursor_states']:
  base=ROOT/x['capture_path'];raw=(base/'vram.bin').read_bytes();cursor=json.loads((base/'cursor.json').read_bytes());g=x['semantic_gap_from_recipe']
  assert len(raw)==4000 and cursor['row']==0 and cursor['column']==[0,1,1,2,3,3,4][g]
  if x['view']=='codes':
   chars=bytes(raw[13*160:14*160:2]);attrs=raw[13*160+1:14*160:2]
   assert chars[:16]==b'A[BOLD]BC[bold]D'
   active=[i for i,v in enumerate(attrs) if v==0x47]
   assert active==[[0],list(range(1,7)),[7],[8],list(range(9,15)),[15],[16]][g]
   for col in range(16):
    if col not in active:assert attrs[col]==(0x1f if col in list(range(1,7))+list(range(9,15)) else 0x17)
 result={'schema':'wordling.wp52.original-recomputed/v1','captures':len(p['original_cursor_states']),'assets_per_capture':6,'sources_and_artifacts':len(p['sources']),'all_historical_git_and_SHA_exact':True,'new_original_guests':0,'facts':p['facts'],'scope':'selected native spans/raw attributes/hardware columns; full geometry and physical palette unqualified'}
 (HERE/'original-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
