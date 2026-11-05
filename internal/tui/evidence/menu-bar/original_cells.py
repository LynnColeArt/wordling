"""Read only public captured outputs, never originals or native resources."""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
PIN='3aa5d343c8cef0c328b161a2d0845dfaa0b10ea0'
results=[]
for run in ['2026-10-29-smoke-02','2026-10-29-smoke-03']:
 manifest=f'docs/research/reference-runs/{run}/run.json';b=(ROOT/manifest).read_bytes();assert b==subprocess.check_output(['git','show',PIN+':'+manifest],cwd=ROOT)
 d=json.loads(b);case=next(c for c in d['results'] if c['case_id']=='CMD51-001');objects=[];vga={}
 for phase in ['before','menu-on','menu-off']:
  for name in ['screen.txt','vram.bin','guest-status.json']:
   path=f'docs/research/reference-runs/{run}/CMD51-001/{phase}/{name}';entry=next(x for x in case['evidence'] if x['path']==path);raw=(ROOT/path).read_bytes();assert len(raw)==entry['size'] and sha(raw)==entry['sha256'];objects.append(entry)
   if name=='vram.bin':assert len(raw)==4000;vga[phase]=raw
 assert vga['before']==vga['menu-off'] and vga['before'][160:]==vga['menu-on'][160:]
 text=vga['menu-on'][:160:2].decode('ascii');roles=list(vga['menu-on'][1:160:2]);assert len(text)==80
 assert text=='File Edit Search Layout Mark Tools Font Graphics Help        (Press F3 for Help)'
 assert roles==[0x47 if i<4 else 0x74 if i in [5,10,17,24,29,36,40,49] else 0x71 for i in range(80)]
 results.append(dict(run=run,manifest=dict(path=manifest,size=len(b),sha256=sha(b)),objects=objects,text=text,roles=roles,before_off_all4000_equal=True,on_only_row0=True,trace=case['trace'],smoke02_archive_limitation=run.endswith('02')))
(HERE/'original-cells.json').write_text(json.dumps(dict(pin=PIN,results=results,no_new_original_runs=True,no_native_save_or_caret_proof=True),indent=2)+'\n')
print('2 public manifests / 18 objects exact; 80 cells and whole4000 restoration')
