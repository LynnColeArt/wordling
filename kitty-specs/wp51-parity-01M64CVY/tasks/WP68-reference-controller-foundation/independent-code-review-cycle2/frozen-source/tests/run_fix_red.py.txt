"""One bounded unfixed-source regression run, never edits product or retries IDs."""
import hashlib
import json
from pathlib import Path
import sys
import time
import uuid
from deployment import deploy, preflight, run, configure_deadline, configure_home, pin, FILES
S=Path(__file__).resolve().parent.parent
E=S/'evidence'/'fix-cycle1-red'
E.mkdir()
T=Path('/tmp')/('wordling-WP68-fix-red-'+uuid.uuid4().hex[:8])
root='/tmp/wordling-reference-TEST-'+uuid.uuid4().hex[:16]
start=time.monotonic();configure_deadline(start+300);configure_home(T)
source={str(p.relative_to(S)):pin(p) for p in sorted(S.rglob('*')) if p.is_file() and 'evidence' not in p.relative_to(S).parts}
plans=dict(source=source,root=root,logical_controls=['newer-commit-then-older-refusal','older-before-newer-refusal-and-halt','ordinary-two-sequential-commits-and-reuse-refusal'],
 ids=['test_newer_then_older','test_older_before_newer','test_sequential'],
 argv=[['<copied>/bin/python','-I','-B','-m','reference_controller','test-admin','--root',root,'--generation','wp68-v1'],['<copied>/bin/python','-I','-B',str(S/'tests/test_update_order.py'),root]],
 expected='two stale ordering controls RED, ordinary sequential PASS on unchanged rejected production; exact json.dumps ensure_ascii indent2+LF; all prior bytes/ctime unchanged on refusal',
 limits=dict(outer_case_seconds=30,cleanup_seconds=2,combined_output_bytes=2097152,suite_seconds=300))
(E/'freeze.json').write_text(json.dumps(plans,indent=2)+'\n')
i,inventory=deploy(S,T,E/'deployment');preflight(i,inventory)
case_start=time.monotonic();used=0
argv=[str(i),'-I','-B','-m','reference_controller','test-admin','--root',root,'--generation','wp68-v1']
r=run(argv,T,E/'admin',timeout=30-(time.monotonic()-case_start));used+=len(r.stdout)+len(r.stderr)
assert r.returncode==0
preflight(i,inventory)
r=run([str(i),'-I','-B',str(S/'tests/test_update_order.py'),root],T,E/'ordering',timeout=30-(time.monotonic()-case_start));used+=len(r.stdout)+len(r.stderr)
assert used<=2097152
(E/'whole.json').write_text(json.dumps(dict(exit=r.returncode,elapsed=time.monotonic()-start,case_elapsed=time.monotonic()-case_start,combined_output_bytes=used,production_source={f:pin(S/f) for f in FILES}),indent=2)+'\n')
print(json.dumps(dict(red_exit=r.returncode,output_bytes=used)))
raise SystemExit(r.returncode)
