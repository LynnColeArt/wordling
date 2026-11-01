"""Finite closed CLI evidence capture; no recipes, originals or private paths."""
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

root=Path(__file__).resolve().parents[3]
evidence=root/'docs/research/continuation/macro-session/startup-seam/cycle-3/cli'
evidence.mkdir(exist_ok=True)
roster=('success','nonzero','stdout','stderr','hang','orphan','observer-fail','readiness')
environment={'PATH':'/usr/bin:/bin','LC_ALL':'C.UTF-8','PYTHONDONTWRITEBYTECODE':'1'}
records=[]
def cap():
    resource.setrlimit(resource.RLIMIT_FSIZE,(131072,131072))
for case in roster:
    argv=['/usr/bin/time','-v','-o',str(evidence/(case+'.time')),sys.executable,'-B',str(root/'scripts/reference/startup_transport.py'),'fixture',case]
    started=time.monotonic()
    with (evidence/(case+'.stdout')).open('wb') as out, (evidence/(case+'.stderr')).open('wb') as err:
        completed=subprocess.run(argv,cwd=root,env=environment,stdout=out,stderr=err,timeout=8,preexec_fn=cap)
    raw=(evidence/(case+'.stdout')).read_bytes()
    assert len(raw)<=65536
    value=json.loads(raw)
    assert value['ok']==(case in ('success','readiness'))
    assert completed.returncode==(0 if value['ok'] else 1)
    records.append(dict(case=case,argv=argv,cwd=str(root),env=environment,exit=completed.returncode,elapsed=time.monotonic()-started,stdout_bytes=len(raw),stdout_sha256=hashlib.sha256(raw).hexdigest(),stderr_bytes=(evidence/(case+'.stderr')).stat().st_size))
    print(case,completed.returncode,flush=True)
(evidence/'commands.json').write_text(json.dumps(records,indent=2)+'\n')
