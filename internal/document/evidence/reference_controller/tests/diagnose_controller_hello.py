"""One source-frozen public TEST syscall diagnostic, no provider instrumentation."""
import json,hashlib,uuid
from pathlib import Path
from deployment import configure_deadline,configure_home
from run_controller_acceptance import Case
import time
S=Path(__file__).resolve().parent.parent
O=S/'evidence/WP70-hello-diagnostic';O.mkdir()
A=S/'evidence/WP70-attempt-01'
runtime=json.loads((A/'deployment/deployment.json').read_text());I=Path(runtime['interpreter']);inventory=json.loads((A/'deployment/deployment-inventory.json').read_text())
T=Path('/tmp/wordling-WP70-hello-diagnostic-'+uuid.uuid4().hex[:8]);T.mkdir();configure_home(T);configure_deadline(time.monotonic()+300)
root='/tmp/wordling-reference-TEST-'+uuid.uuid4().hex[:16]
trace=['/usr/bin/strace','-f','-qq','-e','trace=epoll_create1,mmap,mprotect,munmap,brk,prlimit64,clone,clone3,fork,vfork,exit_group,write,openat,close,newfstatat,fsync']
(O/'freeze.json').write_text(json.dumps(dict(source={str(p.relative_to(S)):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(S.rglob('*')) if p.is_file() and 'evidence' not in p.relative_to(S).parts},root=root,interpreter=str(I),inventory_sha256=hashlib.sha256((A/'deployment/deployment-inventory.json').read_bytes()).hexdigest(),trace_argv_prefix=trace,scenario='healthy',fresh_grant_id='hello-syscalls',seconds=30,cleanup_seconds=2,combined_output=2097152,purpose='ONE diagnostic public repeat, same frozen production source, no provider patches/private fields; not a retry of old spent ID or a qualified positive'),indent=2)+'\n')
c=Case('hello-syscalls',O/'case',I,inventory,root);c.admin();result=c.leaf(extra=trace)
(O/'whole.json').write_text(json.dumps(dict(exit=result[0],combined_output=c.output,qualified_positive=False),indent=2)+'\n');print(json.dumps(dict(exit=result[0],root=root,output=c.output)))
