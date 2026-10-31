"""Exact approved post-DOS-wait state; cue alone is insufficient."""
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]

def require_final_state(directory):
 directory=Path(directory);golden=json.loads((HERE/'final-state-golden.json').read_text())
 for name,identity in golden['files'].items():
  expected=(ROOT/identity['path']).read_bytes();actual=(directory/'clean-exit'/name).read_bytes()
  if len(expected)!=identity['size'] or hashlib.sha256(expected).hexdigest()!=identity['sha256']:raise ValueError('Approved final-state source changed')
  if actual!=expected:raise ValueError('Final state differs from exact approved post-DOS-wait '+name)
 return {'exact_text_vga_cursor':True,'source_commit':golden['source_commit'],'reference_files':golden['files']}
