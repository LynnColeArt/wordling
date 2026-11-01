#!/usr/bin/env python3
"""Required bounded real commands, exact argv/whole exit/raw receipts."""
import hashlib,json,os,pathlib,subprocess,time
ROOT=pathlib.Path(__file__).resolve().parents[4];HERE=pathlib.Path(__file__).resolve().parent
commands=[('build',['go','build','./...']),('test',['go','test','-count=1','./...']),('vet',['go','vet','./...']),('race',['go','test','-race','-count=1','./internal/tui','./internal/editor']),('render-resources',['go','test','./internal/tui','-run','^$','-bench','BenchmarkReveal(MaximumWindow|MaximumCodeWindow)$','-benchtime=1x','-benchmem']),('configured-seven',['python3','-B','scripts/review_checks.py','--junitxml',str(HERE/'configured-seven.xml')])]
source={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('internal/tui/*.go')};rows=[]
for name,argv in commands:
 before=time.monotonic()
 try:r=subprocess.run(argv,cwd=ROOT,capture_output=True,timeout=300,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));code=r.returncode;stdout=r.stdout;stderr=r.stderr
 except subprocess.TimeoutExpired as e:code=None;stdout=e.stdout or b'';stderr=(e.stderr or b'')+b'\nACTUAL COMMAND TIMEOUT\n'
 (HERE/(name+'.stdout')).write_bytes(stdout);(HERE/(name+'.stderr')).write_bytes(stderr);rows.append({'name':name,'argv':argv,'cwd':str(ROOT),'exit':code,'elapsed':time.monotonic()-before,'source_go':source});(HERE/'verification-commands.json').write_text(json.dumps(rows,indent=2)+'\n');print(name,code,flush=True)
 if code!=0:break
raise SystemExit(0 if len(rows)==len(commands) and all(r['exit']==0 for r in rows) else 1)
