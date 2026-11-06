#!/usr/bin/env python3
"""Freeze/build the unchanged production entry; VCS stamp is not source authority."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent;OUT=Path('/tmp/wordling-WP69-build');OUT.mkdir(exist_ok=True)
def digest(p):b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def objects(raw):
 d=json.JSONDecoder()
 while raw.strip():v,n=d.raw_decode(raw.lstrip());raw=raw.lstrip()[n:];yield v
argv=['go','list','-compiled','-deps','-json','./cmd/wordling'];result=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=300);(HERE/'go-list.stderr').write_text(result.stderr);assert result.returncode==0
packages=list(objects(result.stdout));inputs={}
for p in packages:
 for field in ['CompiledGoFiles','SFiles','CFiles','HFiles','EmbedFiles','SysoFiles']:
  for n in p.get(field,[]):
   f=Path(n)if Path(n).is_absolute()else Path(p['Dir'])/n
   inputs[str(f)]=digest(f)
for n in ['go.mod','go.sum']:inputs[str(ROOT/n)]=digest(ROOT/n)
binary=OUT/'wordling-final';cmd=['go','build','-o',str(binary),'./cmd/wordling'];r=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=300);(HERE/'build.stdout').write_bytes(r.stdout);(HERE/'build.stderr').write_bytes(r.stderr);assert r.returncode==0
(HERE/'binary-buildinfo.txt').write_bytes(subprocess.check_output(['go','version','-m',str(binary)],cwd=ROOT))
record=dict(binary=str(binary),binary_digest=digest(binary),cwd=str(ROOT),argv=cmd,go_list_argv=argv,package_count=len(packages),inputs=inputs,packages=[{k:p.get(k)for k in ['ImportPath','Dir','GoFiles','CompiledGoFiles','Module']}for p in packages],environment=json.loads(subprocess.check_output(['go','env','-json','GOMOD','GOFLAGS','GOWORK','GOOS','GOARCH','CGO_ENABLED'],cwd=ROOT)),go_version=subprocess.check_output(['go','version'],text=True).strip(),GoVCS_stamp_NOT_source_authority=True)
(HERE/'build-source.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(dict(binary=record['binary_digest'],packages=len(packages),compiler_inputs=len(inputs))))
