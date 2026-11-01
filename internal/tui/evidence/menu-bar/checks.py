"""Finite configured checks and explicit timings; no new original/resource runs."""
from pathlib import Path
import subprocess,time,json,resource,os
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
commands=[('configured-seven',['python3','scripts/review_checks.py','--junitxml='+str(HERE/'configured-seven.xml')]),('race',['go','test','-race','-timeout=120s','./...']),('model',['go','test','-count=1','-json','-run','^TestMenu','./internal/tui']),('tui-regressions',['go','test','-count=1','-timeout=90s','./internal/tui'])]
results=[]
for name,argv in commands:
 started=time.monotonic()
 with (HERE/(name+'.stdout')).open('wb')as out,(HERE/(name+'.stderr')).open('wb')as err:r=subprocess.run(argv,cwd=ROOT,stdout=out,stderr=err,timeout=300)
 results.append(dict(name=name,argv=argv,exit=r.returncode,elapsed=time.monotonic()-started,maxrss_children=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,own_fds=len(os.listdir('/proc/self/fd'))));(HERE/'checks.json').write_text(json.dumps(results,indent=2)+'\n');print(name,r.returncode,flush=True)
 if r.returncode:raise SystemExit(r.returncode)
