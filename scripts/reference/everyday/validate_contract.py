#!/usr/bin/env python3
"""Validate reference custody and bounded observed invariants, not product behavior."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'docs/research/everyday-contract-2026-11-05'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def item(p): return {'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)}
def raw(run,name): return (BASE/'qualification'/run/name).read_bytes()
def body(run,name):
 d=raw(run,'exports/'+name);return d[int.from_bytes(d[4:8],'little'):]
def check_ref(r):
 p=ROOT/r['path'];assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],str(p)
checks={}
profile=json.loads((BASE/'profile.json').read_text())
for key in ['release','environment','resources','mouse_variant']: check_ref(profile[key])
checks['profile_references_verified']=True
for manifest in ['evidence-manifest.json','backup/manifest.json','spelling/manifest.json']:
 p=BASE/manifest;j=json.loads(p.read_text());count=0
 for r in j['files']:
  f=p.parent/r['path'];assert f.stat().st_size==r['bytes'] and sha(f)==r['sha256'],str(f);count+=1
 checks['immutable_'+manifest]=count
j=json.loads((BASE/'journey-contract.json').read_text())
for f in j['frames']:
 for k in ['grid','text','image']: check_ref(f[k])
 d=(ROOT/f['grid']['path']).read_bytes();assert len(d)==4000
 assert hashlib.sha256(d[::2]).hexdigest()==f['characters_sha256']
 assert hashlib.sha256(d[1::2]).hexdigest()==f['attributes_sha256']
 if 'bios_page0_cursor' in f: check_ref(f['bios_page0_cursor']['file'])
checks['indexed_frames']=len(j['frames'])
f=json.loads((BASE/'fixture-manifest.json').read_text())
for r in f['fixtures']:
 check_ref(r);d=(ROOT/r['path']).read_bytes();assert d[r['document_offset']:].hex()==r['body_hex']
checks['native_fixtures']=len(f['fixtures'])
for key,n in [('f1',2),('esc',3),('spc',4)]:
 a=raw('focus-r1',f'{n:02d}-{key}-before/vram.bin');b=raw('focus-r1',f'{n:02d}-{key}-after/vram.bin')
 delta=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
 assert delta==[14*160+c*2+1 for c in range(36,44)]
 assert [b[i] for i in delta]==[0x71,0x74,0x71,0x71,0x71,0x71,0x71,0x71]
 for phase in ['before','after','up']:
  assert raw('focus-r1',f'{n:02d}-{key}-{phase}/vram.bin')==raw('focus-r2',f'{n:02d}-{key}-{phase}/vram.bin')
checks['focus_exact_repeated_eight_attribute_bytes']=True
assert raw('flow','exports/FLOW.WP')==raw('flow-reliable','exports/FLOW.WP')
checks['three_page_flow_repeated_byte_identical']=True
assert raw('proof-boundaries','exports/BOUNDARY.WP')==raw('proof-boundaries-repeat','exports/BOUNDARY.WP')
assert body('proof-boundaries','BOUNDARY.WP')==b'quick\xc3\x0c\xc3\xc4\x0c\xc4\nmisspelled\xc3\x0e\xc3\xc4\x0e\xc4\nqUICKXYYYYYYYYYY'
checks['formatted_longword_correction_repeated']=True
for a,b in [('BEFORE.WP','REFUSED.WP'),('WPBACK.WP','REFBACK.WP')]:
 assert raw('files','exports/'+a)==raw('files','exports/'+b)
assert body('files','TXTBACK.WP')==b'SECOND' and body('files','WPBACK.WP')==b'FIRST'
assert body('files','INSERT.WP')==b'SECOND CHANGESECOND CHANGE UNSAVED'
checks['overwrite_refusal_and_shared_basename_backup']=True
checks['browser_retrieval_insertion_native']=True
for run in ['scroll-search-r1','scroll-search-r2']:
 assert raw(run,'exports/FLOW.WP')==raw('flow-reliable','exports/FLOW.WP')
 for label,row in [('11-not-found-burst-00',24),('14-reveal-not-found',11)]:
  d=raw(run,label+'/vram.bin');assert d[row*160:row*160+26:2]==b'* Not found *'
  assert d[row*160+1:row*160+27:2]==bytes([0x1f])*13
 for label in ['03-reveal-start','04-reveal-page-two','05-reveal-page-three','06-reveal-page-up','07-reveal-end','08-reveal-line-scroll','09-normal-restored','12-search-settled','13-search-cancel','15-reveal-search-settled','16-final-normal']:
  assert raw('scroll-search-r1',label+'/vram.bin')==raw('scroll-search-r2',label+'/vram.bin'),label
checks['reveal_scroll_and_search_repeated_exact_grids']=True
for r in (BASE/'qualification').iterdir():
 if r.is_dir(): assert not Path('/tmp/wp78-'+r.name+'/qmp.sock').exists(),r.name
checks['qualification_guests_stopped']=True
# Preserve original manifests; index all artifacts including previously excluded PPMs.
excluded={'qualification-manifest.json','validation.json'}
files=[item(p) for p in sorted(BASE.rglob('*')) if p.is_file() and p.name not in excluded and '__pycache__' not in p.parts]
files += [item(p) for p in sorted((ROOT/'scripts/reference/everyday').glob('*.py'))]
parser=argparse.ArgumentParser();parser.add_argument('--freeze',action='store_true');args=parser.parse_args()
if args.freeze:
 (BASE/'qualification-manifest.json').write_text(json.dumps({'schema_version':1,'scope':'All research artifacts under this directory except this manifest and validation.json; all everyday replay sources. Includes failures and raw PPM derivatives, not just acceptance frames.','files':files},indent=2)+'\n')
else:
 for r in json.loads((BASE/'qualification-manifest.json').read_text())['files']: check_ref(r)
checks['manifest_files']=len(files)
checks['product_parity_asserted']=False
checks['review_status']='pending independent reference review'
checks['commands']=['python3 -m py_compile scripts/reference/everyday/*.py','python3 scripts/reference/everyday/compile_contract.py','python3 scripts/reference/everyday/validate_contract.py --freeze','python3 scripts/reference/everyday/validate_contract.py']
print(json.dumps(checks,indent=2))
if args.freeze:(BASE/'validation.json').write_text(json.dumps(checks,indent=2)+'\n')
