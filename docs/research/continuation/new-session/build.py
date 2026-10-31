#!/usr/bin/env python3
"""Freeze actual cmd/wordling compilation; no source injection or VCS authority."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
def digest(p):b=p.read_bytes();return {'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def objects(raw):
 decoder=json.JSONDecoder()
 while raw.strip():
  value,n=decoder.raw_decode(raw.lstrip());raw=raw.lstrip()[n:];yield value
out=Path(sys.argv[1]).resolve();assert out.is_relative_to(Path(__file__).resolve().parent);out.mkdir()
argv=['go','list','-deps','-json','./cmd/wordling'];packages=list(objects(subprocess.check_output(argv,cwd=ROOT,text=True)));local=[p for p in packages if p.get('Module',{}).get('Main')]
inputs={str(p.relative_to(ROOT)):digest(p) for x in local for name in x.get('GoFiles',[])+x.get('CgoFiles',[])+x.get('EmbedFiles',[]) for p in [Path(x['Dir'])/name]}
for name in ['go.mod','go.sum']:inputs[name]=digest(ROOT/name)
allgo={str(p.relative_to(ROOT)):digest(p) for prefix in ['internal','cmd'] for p in sorted((ROOT/prefix).rglob('*.go'))}
binary=out/'wordling.bin';build=['go','build','-o',str(binary),'./cmd/wordling'];v=subprocess.run(build,cwd=ROOT,capture_output=True);(out/'build.stdout').write_bytes(v.stdout);(out/'build.stderr').write_bytes(v.stderr);assert v.returncode==0
(out/'binary-buildinfo.txt').write_bytes(subprocess.check_output(['go','version','-m',str(binary)],cwd=ROOT))
record={'cwd':str(ROOT),'build_argv':build,'exit':v.returncode,'go_list_argv':argv,'actual_compiled_project_inputs':inputs,'complete_local_Go_SET':allgo,'actual_compiled_packages':[{k:p.get(k,[]) for k in ['ImportPath','Dir','GoFiles','CgoFiles','EmbedFiles']} for p in local],'dependencies':[{k:p.get(k) for k in ['ImportPath','Dir','GoFiles','Module']}for p in packages if not p.get('Standard')],'GoVersion':subprocess.check_output(['go','version'],text=True).strip(),'environment':{k:subprocess.check_output(['go','env',k],text=True,cwd=ROOT).strip() for k in ['GOMOD','GOFLAGS','GOWORK','GOOS','GOARCH','CGO_ENABLED']},'context_head_NOT_compiled_source_authority':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'binary':digest(binary),'binary_path':str(binary),'VCS_stamp_is_not_source_authority':True}
(out/'source.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'binary':record['binary'],'project_files':len(inputs),'Go_SET':len(allgo)}))
