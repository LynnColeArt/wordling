#!/usr/bin/env python3
"""Compile inert owned probe in an ephemeral owned path; no archival Go package."""
import hashlib,json,subprocess,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
with tempfile.TemporaryDirectory(prefix='measure-',dir=HERE)as temp:
 source=Path(temp)/'main.go';source.write_bytes((HERE/'probe.go.txt').read_bytes())
 argv=['/usr/bin/time','-v','go','run',str(source)]
 r=subprocess.run(argv,cwd=ROOT,capture_output=True)
 (HERE/'stdout.json').write_bytes(r.stdout);(HERE/'process.txt').write_bytes(r.stderr)
 (HERE/'command.json').write_text(json.dumps({'argv':argv,'exit':r.returncode,'probe_sha256':hashlib.sha256((HERE/'probe.go.txt').read_bytes()).hexdigest(),'source_is_inert_text_outside_temporary_execution':True},indent=2)+'\n')
 print('measurement exit',r.returncode)
 raise SystemExit(r.returncode)
