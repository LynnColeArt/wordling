"""Isolated same-module public framing bridge. Never installs a codec/product package."""
from pathlib import Path
import json,os,shutil,tempfile
from boundaries import process,read,sha,require,parse,canonical
from source import HERE,ROOT
REF='44aab36accdf14a370a67fd73945907871ab7193'
def inputs():
 paths=['go.mod','go.sum']+[str(p.relative_to(ROOT))for p in sorted((ROOT/'internal/wp51').glob('*.go'))]
 expected=parse(read(HERE/'reader-inputs.json',1<<20))['files'];require(set(paths)==set(expected),'ReaderSourceSet','actual wp51/module SET')
 observed={p:sha(read(ROOT/p,4<<20))for p in paths};require(all(observed[p]==expected[p]['sha256']for p in paths),'ReaderSourceChanged','frozen approved bytes');return observed
def executable():
 require(not os.environ.get('GOFLAGS')and not os.environ.get('GOWORK'),'GoEnvironment','no overlays/workspace overrides')
 actual_env=parse(process(['go','env','-json','GOMOD','GOFLAGS','GOWORK','GOOS','GOARCH','GOVERSION'],ROOT)[0]);require(actual_env['GOMOD']==str(ROOT/'go.mod')and not actual_env['GOFLAGS']and actual_env['GOWORK']in {'','off'},'GoEnvironment','actual tool settings must exclude workspace/overlay')
 pins=inputs();key=sha(canonical(dict(inputs=pins,bridge=sha(read(HERE/'inspect.go.txt',1<<20)),guard=sha(read(HERE/'bridge.py',1<<20)),Go_environment=actual_env)))
 cache=HERE/'.cache';cache.mkdir(exist_ok=True);binary=cache/'inspect';receipt=cache/'receipt.json'
 if receipt.exists():
  r=parse(read(receipt,4<<20))
  if r['key']==key and binary.exists()and sha(read(binary,8<<20))==r['binary_sha256']:return binary,r
 with tempfile.TemporaryDirectory(prefix='wordling-wp56-same-module-')as d:
  cwd=Path(d)
  for path,digest in pins.items():
   p=cwd/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(read(ROOT/path,4<<20));require(sha(p.read_bytes())==digest,'BridgeCopy',path)
  (cwd/'probe').mkdir();(cwd/'probe/main.go').write_bytes(read(HERE/'inspect.go.txt',1<<20))
  compiler_env=parse(process(['go','env','-json','GOMOD','GOFLAGS','GOWORK','GOOS','GOARCH','GOVERSION'],cwd)[0]);require(compiler_env['GOMOD']==str(cwd/'go.mod')and not compiler_env['GOFLAGS']and compiler_env['GOWORK']in {'','off'},'GoEnvironment','actual isolated compiler configuration')
  out,_=process(['go','list','-deps','-json','./probe'],cwd,timeout=180);dec=json.JSONDecoder();rest=out.decode();packages=[]
  while rest.strip():
   row,end=dec.raw_decode(rest.lstrip());rest=rest.lstrip()[end:]
   if row['ImportPath'].startswith('github.com/lynncoleart/wordling/'):
    directory=Path(row['Dir']);require(directory.is_relative_to(cwd),'GoDirectory',directory);packages.append(dict(import_path=row['ImportPath'],directory=str(directory.relative_to(cwd)),GoFiles={n:sha(read(directory/n,4<<20))for n in row['GoFiles']}))
  require({p['directory']for p in packages}=={'probe','internal/wp51'},'CompiledClosure',packages)
  process(['go','build','-trimpath','-buildvcs=false','-o',str(binary),'./probe'],cwd,timeout=180)
  r=dict(actual_Go_env=compiler_env,host_Go_env=actual_env,toolchain=process(['go','version'],cwd)[0].decode().strip(),actual_go_executable=shutil.which('go'),actual_go_executable_sha256=sha(read(Path(shutil.which('go')),32<<20)),key=key,inputs=pins,binary_sha256=sha(read(binary,8<<20)),bridge_sha256=sha(read(HERE/'inspect.go.txt',1<<20)),actual_cwd=str(cwd),GOMOD=str(cwd/'go.mod'),GOFLAGS='',GOWORK='',compiled_packages=packages,argv=['go','build','-trimpath','-buildvcs=false','-o',str(binary),'./probe'])
  receipt.write_text(json.dumps(r,indent=2)+'\n');(HERE/'checks/bridge-build.json').write_text(json.dumps(r,indent=2)+'\n')
 return binary,r
def inspect(raw):
 binary,r=executable()
 with tempfile.TemporaryDirectory(prefix='wordling-wp56-native-')as d:
  path=Path(d)/'input.WP5';path.write_bytes(raw)
  out,_=process([str(binary),str(path)],ROOT);result=parse(out);require(result['sha256']==sha(raw),'BridgeIdentity','actual input hash');return result,dict(binary_sha256=r['binary_sha256'],bridge_sha256=r['bridge_sha256'],compiled_packages=r['compiled_packages'])
