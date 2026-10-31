#!/usr/bin/env python3
"""Verify actual Git object bytes for every raw artifact and emitted Go candidate."""
import argparse,hashlib,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
p=argparse.ArgumentParser();p.add_argument('--revision',default='HEAD');p.add_argument('--index',action='store_true');p.add_argument('--output',required=True);args=p.parse_args()
expected={}
for manifest in (HERE/'reference/runs').glob('*/run.json'):
 run=json.loads(manifest.read_text())
 for row in run['artifacts']:
  path=str((manifest.parent/row['path']).relative_to(ROOT));value=(row['size'],row['sha256'])
  if path in expected and expected[path]!=value:raise ValueError('Conflicting raw manifest')
  expected[path]=value
for row in json.loads((HERE/'candidates/sealed-plan.json').read_text())['cases']:
 path=HERE/'candidates'/row['name']/'candidate.WP5';expected[str(path.relative_to(ROOT))]=(path.stat().st_size,row['candidate_sha256'])
command=['git','ls-files','--stage','-z'] if args.index else ['git','ls-tree','-rz',args.revision]
objects={}
for row in subprocess.check_output(command,cwd=ROOT).split(b'\0'):
 if not row:continue
 metadata,path=row.split(b'\t',1);fields=metadata.split();objects[path.decode()]=fields[1 if args.index else 2].decode()
by_blob={}
for path,value in expected.items():
 if path not in objects:raise ValueError('Missing tracked raw artifact: '+path)
 blob=objects[path]
 if blob in by_blob and by_blob[blob]!=value:raise ValueError('Conflicting expected bytes for one object')
 by_blob[blob]=value
process=subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
try:
 for blob,(size,digest) in sorted(by_blob.items()):
  process.stdin.write((blob+'\n').encode());process.stdin.flush();header=process.stdout.readline().split()
  if header!=[blob.encode(),b'blob',str(size).encode()]:raise ValueError('Wrong Git blob header: '+blob)
  h=hashlib.sha256();remaining=size
  while remaining:
   data=process.stdout.read(min(1048576,remaining))
   if not data:raise ValueError('Truncated Git blob')
   h.update(data);remaining-=len(data)
  if process.stdout.read(1)!=b'\n' or h.hexdigest()!=digest:raise ValueError('Raw Git blob bytes differ: '+blob)
finally:
 process.stdin.close();process.stdout.close();code=process.wait()
 if code:raise ValueError('Git object process failed')
result={'revision':'index' if args.index else subprocess.check_output(['git','rev-parse',args.revision],cwd=ROOT,text=True).strip(),'raw_manifest_paths':len(expected)-5,'go_candidate_paths':5,'unique_git_blobs':len(by_blob),'raw_and_candidate_manifest_bytes':sum(v[0] for v in expected.values()),'all_size_sha256_equal':True,'scope':'actual Git object bytes, never only workingtree hashes; includes duplicate artifact paths'}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
