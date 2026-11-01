"""Replay unchanged 8+15 TEST callers, storing fresh raw outputs only here."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(sys.argv[1]);OUT.mkdir(parents=True,exist_ok=False)
FACADE=Path(os.environ.get('STARTUP_FAMILY_UNDER_TEST',ROOT/'scripts/reference/startup_transport.py'))
old=('success','nonzero','stdout','stderr','hang','orphan','observer-fail','readiness')
managed=('streaming64m','mutable-success','mutable-failure','handoff','parent-loss','cancel',
 'foreign-endpoint','unknown-launch','process-progress','readiness-deadline-progress','exec-reply-exit',
 'prior-no-clobber','worker-death','stale-handle','wrong-root-load')
rows=[]
for command,cases,positive in (('fixture',old,{'success','readiness'}),
 ('managed-fixture',managed,{'streaming64m','mutable-success','handoff'})):
    for case in cases:
        argv=[sys.executable,'-B',str(FACADE),command,case];start=time.monotonic()
        p=subprocess.run(argv,cwd=ROOT,capture_output=True,timeout=30)
        name=command+'-'+case;(OUT/(name+'.stdout')).write_bytes(p.stdout);(OUT/(name+'.stderr')).write_bytes(p.stderr)
        try:value=json.loads(p.stdout);ok=value.get('ok')
        except Exception:ok=None
        expected=0 if case in positive else 1
        rows.append(dict(command=command,case=case,argv=argv,exit=p.returncode,expected_exit=expected,
            matched=p.returncode==expected and ok==(expected==0) and not p.stderr,seconds=time.monotonic()-start))
        print(command,case,p.returncode,expected,rows[-1]['matched'],flush=True)
(OUT/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
raise SystemExit(0 if all(x['matched'] for x in rows) else 1)
