#!/usr/bin/env python3
"""Compare actual Git object bytes to immutable raw SHA256 manifests."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]

def verify(revision=None):
 expected={}
 for path in sorted((HERE/'runs').glob('*/run.json')):
  r=json.loads(path.read_text())
  for a in r['artifacts']:expected[str((path.parent/a['path']).relative_to(ROOT))]=(a['size'],a['sha256'])
 for r in json.loads((HERE/'diagnostic-extractions.json').read_text()):expected[r['artifact']]=(r['bytes'],r['sha256'])
 if revision:
  raw=subprocess.check_output(['git','ls-tree','-r',revision,'--','docs/research/continuation/native-edits'],cwd=ROOT,text=True)
  objects={line.split('\t',1)[1]:line.split()[2] for line in raw.splitlines()}
 else:
  raw=subprocess.check_output(['git','ls-files','-s','--','docs/research/continuation/native-edits'],cwd=ROOT,text=True)
  objects={line.split('\t',1)[1]:line.split()[1] for line in raw.splitlines()}
 absent=set(expected)-set(objects)
 if absent:raise ValueError('Raw evidence missing from Git '+str(sorted(absent)[:3]))
 cache={};total=0
 with subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE) as process:
  for path,(size,digest) in expected.items():
   oid=objects[path]
   if oid not in cache:
    process.stdin.write((oid+'\n').encode());process.stdin.flush();header=process.stdout.readline().decode().split()
    if len(header)!=3 or header[1]!='blob':raise ValueError('Git blob missing')
    length=int(header[2]);remaining=length;hasher=hashlib.sha256()
    while remaining:
     block=process.stdout.read(min(65536,remaining))
     if not block:raise ValueError('Truncated Git blob')
     hasher.update(block);remaining-=len(block)
    if process.stdout.read(1)!=b'\n':raise ValueError('Git protocol boundary')
    cache[oid]=(length,hasher.hexdigest())
   if cache[oid]!=(size,digest):raise ValueError('Git changed raw bytes '+path)
   total+=size
  process.stdin.close()
  if process.wait():raise ValueError('Git blob process failed')
 return {'git_revision':revision or 'staged-index','raw_artifact_paths':len(expected),'unique_blobs_hashed':len(cache),'raw_manifest_bytes':total,'all_git_blob_sizes_and_sha256_exact':True}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--revision');p.add_argument('--output');a=p.parse_args();result=verify(a.revision);text=json.dumps(result,indent=2)+'\n'
 if a.output:Path(a.output).write_text(text)
 else:print(text)
