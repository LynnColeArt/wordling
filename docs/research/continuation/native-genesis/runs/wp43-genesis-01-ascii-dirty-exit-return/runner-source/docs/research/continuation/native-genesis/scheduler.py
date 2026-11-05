#!/usr/bin/env python3
"""Serial finite WP43 schedule; first failed pair stops without retry."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'scripts/reference'))
import native_genesis as g
p=argparse.ArgumentParser();p.add_argument('--allow-vm',action='store_true');p.add_argument('--authorization-note',default='');p.add_argument('--prefix',required=True);a=p.parse_args()
if not a.allow_vm or not a.authorization_note.strip():raise SystemExit('No explicit root grant/control; no guest authorized')
rows=[]
for case in g.cases():
    argv=[sys.executable,str(ROOT/'scripts/reference/native_genesis.py'),'run',a.prefix+'-'+case['id'],'--case',case['id'],'--allow-vm','--authorization-note',a.authorization_note]
    r=subprocess.run(argv,capture_output=True,text=True)
    row={'case':case['id'],'argv':argv,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr};rows.append(row)
    print(json.dumps(row),flush=True)
    if r.returncode:raise SystemExit(r.returncode)
