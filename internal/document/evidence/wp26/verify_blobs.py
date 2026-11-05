#!/usr/bin/env python3
"""Verify actual staged/committed Git blobs, including each original manifest."""
import argparse,hashlib,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def main():
 p=argparse.ArgumentParser();p.add_argument('--revision',default='HEAD');p.add_argument('--staged',action='store_true');p.add_argument('--out',type=Path,required=True);a=p.parse_args();output=a.out.resolve()
 paths=set(x.decode()for x in subprocess.check_output(['git','ls-files','-z','--','internal/document/evidence/wp26'],cwd=ROOT).split(b'\0')if x)
 plan=json.loads((HERE/'candidates/sealed-plan.json').read_text());paths.update(plan['source_hashes']);paths.add('internal/document/evidence/wp25/reopen/main.go')
 process=subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
 rows=[];by_path={};total=0
 try:
  for path in sorted(paths):
   file=ROOT/path
   if file.resolve()==output:continue
   expression=':'+path if a.staged else a.revision+':'+path
   process.stdin.write((expression+'\n').encode());process.stdin.flush();header=process.stdout.readline().decode().strip().split();assert len(header)==3 and header[1]=='blob',(path,header)
   raw=process.stdout.read(int(header[2]));assert process.stdout.read(1)==b'\n';assert raw==file.read_bytes(),path
   item={'path':path,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'git_blob':header[0]};rows.append(item);by_path[path]=item;total+=len(raw)
 finally:process.stdin.close();process.stdout.close();process.wait()
 original=0
 for manifest in sorted((HERE/'reference/runs').glob('*/run.json')):
  run=json.loads(manifest.read_text())
  for x in run['artifacts']:
   key=str((manifest.parent/x['path']).relative_to(ROOT));actual=by_path[key]
   assert actual['bytes']==x['size']and actual['sha256']==x['sha256'],key;original+=1
 assert original==2968,original
 result={'revision':':index'if a.staged else subprocess.check_output(['git','rev-parse',a.revision],cwd=ROOT,text=True).strip(),'source_and_evidence_files':len(rows),'bytes':total,'raw_manifest_blobs_exact':original,'self_excluded':str(output.relative_to(ROOT)),'files':rows}
 output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='files'},indent=2))
if __name__=='__main__':main()
