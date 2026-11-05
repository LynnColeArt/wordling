"""Fresh existing8+15+14 CLI outputs, only inside the selected owned destination."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[3];OUT=Path(sys.argv[1]);OUT.mkdir(parents=True,exist_ok=False)
FACADE=Path(os.environ.get('STARTUP_FAMILY_UNDER_TEST',ROOT/'scripts/reference/startup_transport.py'))
rosters=(('fixture',('success','nonzero','stdout','stderr','hang','orphan','observer-fail','readiness'),{'success','readiness'}),
 ('managed-fixture',('streaming64m','mutable-success','mutable-failure','handoff','parent-loss','cancel','foreign-endpoint','unknown-launch','process-progress','readiness-deadline-progress','exec-reply-exit','prior-no-clobber','worker-death','stale-handle','wrong-root-load'),{'streaming64m','mutable-success','handoff'}),
 ('envelope-fixture',('positive','expired','absolute-progress','source-io','prepared','commands','output','fd','process','rss','wire','observation','response-loss','external-peer'),{'positive','external-peer'}))
rows=[]
for command,cases,positive in rosters:
 for case in cases:
  argv=[sys.executable,'-B',str(FACADE),command,case];start=time.monotonic();p=subprocess.run(argv,cwd=ROOT,capture_output=True,timeout=30)
  (OUT/(command+'-'+case+'.stdout')).write_bytes(p.stdout);(OUT/(command+'-'+case+'.stderr')).write_bytes(p.stderr)
  try:ok=json.loads(p.stdout)['ok']
  except Exception:ok=None
  expected=0 if case in positive else 1;matched=p.returncode==expected and not p.stderr and ok==(expected==0)
  rows.append(dict(command=command,case=case,argv=argv,exit=p.returncode,expected_exit=expected,matched=matched,seconds=time.monotonic()-start));print(command,case,matched,flush=True)
(OUT/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
sys.exit(0 if all(r['matched'] for r in rows) else 1)
