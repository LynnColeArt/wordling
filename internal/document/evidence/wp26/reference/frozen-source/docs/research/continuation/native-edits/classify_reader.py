#!/usr/bin/env python3
"""Run the actual approved Go reader against original exports; no duplicate codec."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'scripts/reference'))
import native_edits

def classify(paths):
 with tempfile.TemporaryDirectory(prefix='reader-check-',dir=HERE) as temporary:
  source=Path(temporary)/'main.go';source.write_bytes((HERE/'reader_probe.go.txt').read_bytes())
  subprocess.run(['gofmt','-w',str(source)],check=True)
  rows=json.loads(subprocess.check_output(['go','run',str(source),*[str(p) for p in paths]],cwd=ROOT,text=True))
 for row in rows:
  p=Path(row['path']);row['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();row['bytes']=p.stat().st_size
  try:native_edits.inspect(p.read_bytes(),True)
  except ValueError as refusal:row['mutation_admitted']=False;row['mutation_refusal']=str(refusal);row['mutation_refusal_code']=getattr(refusal,'code','ValueError')
  else:row['mutation_admitted']='conditional-contract-only'
 return {'actual_reader_source_sha256':hashlib.sha256((ROOT/'internal/wp51/native.go').read_bytes()).hexdigest(),'scope':'read-only actual Go admission and separate conditional research mutation admission; no serializer','files':rows}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('paths',nargs='+');a=p.parse_args();print(json.dumps(classify([Path(x).resolve() for x in a.paths]),indent=2))
