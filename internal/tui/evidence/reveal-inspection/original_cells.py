#!/usr/bin/env python3
"""Read already-public authored WP14 VGA witnesses, not program/resource files."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent;rows=[]
for family,label in [('L1-HR','[HRt]'),('L2-HP','[HPg]')]:
 for rep in [1,2]:
  p=ROOT/f'docs/research/continuation/text-layout/runs/wp14-r{rep:02d}-{family}/BASE-reveal/vram.bin';v=p.read_bytes();chars=v[0::2];start=chars.index(label.encode());assert chars.count(label.encode())==1
  attributes=list(v[2*start+1:2*(start+len(label)):2]);assert attributes==[0x1f]*len(label)
  rows.append(dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(v).hexdigest(),label=label,character_plane_offset=start,attributes=attributes,claim='exact spelling/inactive1F ONLY; no lowergeometry/cursor/pergap/active47 qualification'))
(HERE/'original-cells.json').write_text(json.dumps(dict(witnesses=rows,original_guests=0),indent=2)+'\n');print('PASS4 existing original VGA label/role witnesses')
