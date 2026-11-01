"""Finite semantic falsifiers of the actual five-file compiler/import inputs."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(sys.argv[1]).resolve();OUT.mkdir(parents=True,exist_ok=False)
paths=['scripts/reference/startup_transport.py']+['scripts/reference/startup_family/'+x for x in ('__init__.py','engine.py','artifacts.py','lifetime.py')]
base={p:(ROOT/p).read_text() for p in paths}
life='scripts/reference/startup_family/lifetime.py';art='scripts/reference/startup_family/artifacts.py';fac='scripts/reference/startup_transport.py'
cases=(
 ('absolute-clock',life,[("if self.envelope is not None and time.monotonic()>=self.envelope.end:","if False:")],
  'test_backpressure.BackpressureTests.test_usage_absolute_clock_during_backpressure'),
 ('phase-counter-reset',life,[("        self.publication_operation=operation;self.publication_deadline=None", "        self.store.io=self.store.transfer_io=0\n        self.publication_operation=operation;self.publication_deadline=None")],
  'test_envelope.EnvelopeTests.test_live_usage_and_exact_known_byte_trace'),
 ('response-reservation',life,[("        self.reserved_wire=65540+256;self.reserved_messages=2", "        self.reserved_wire=0;self.reserved_messages=0")],
  'test_envelope.EnvelopeTests.test_live_usage_and_exact_known_byte_trace'),
 ('coordinator-fd-omitted',life,[("actors=engine.sample_actors(sessions,(self.parent,os.getpid()))", "actors=engine.sample_actors(sessions,(os.getpid(),))")],
  'test_envelope.EnvelopeTests.test_actual_coordinator_fd_pressure'),
 ('transfer-io-omitted',art,[("offset+=n;self.transfer_io+=n","offset+=n;self.transfer_io+=0")],
  'test_envelope.EnvelopeTests.test_live_usage_and_exact_known_byte_trace'),
 ('provisional-usage-accepted',life,[("candidate=value;candidate_sha=hashlib.sha256(raw).hexdigest()", "candidate=value;candidate_sha=hashlib.sha256(raw).hexdigest()\n                        if request is not None and request.get('operation')=='usage':return candidate")],
  'test_backpressure.BackpressureTests.test_fully_queued_provisional_usage_no_commit'),
 ('usage-commit-inconsistent',life,[("sha256=hashlib.sha256(payload).hexdigest()),", "sha256=('0'*64 if self.publication_operation=='usage' else hashlib.sha256(payload).hexdigest())),")],
  'test_envelope.EnvelopeTests.test_exact_control_frame_trace'),
 ('observation-trusted',life,[("    def usage(self):\n        value=self._rpc('usage')", "    def usage(self,observation=None):\n        if observation is not None:return observation\n        value=self._rpc('usage')")],
  'test_envelope.EnvelopeTests.test_observation_is_not_usage_input'),
 ('commands-reset',life,[("if self.commands>min(self.policy.commands,self.envelope.commands if self.envelope else self.policy.commands):", "if self.commands>self.policy.commands:")],
  'test_cli.CLITests.test_commands'),
 ('root-alias-trusted',fac,[("            if (getattr(existing, '_source_binding', None) != binding", "            if (False"),
   ("or getattr(existing, 'API_VERSION', None) != 1):","or False):"),
   ("if module is None or module.__spec__.origin != str(root/name):","if module is None:"),
   ("if list(existing.__path__) != [str(root)]:","if False:")],
  'old_family.LoadingTests.test_same_bytes_different_root_cannot_share_authority'),
)
rows=[]
for name,file,edits,test in cases:
    folder=OUT/name;folder.mkdir();source=base[file];valid=True
    for before,after in edits:
        if source.count(before)!=1:
            rows.append(dict(name=name,construction_error='needle count '+str(source.count(before)),killed=False));valid=False;break
        source=source.replace(before,after)
    if not valid:continue
    compile(source,file,'exec')
    (folder/(Path(file).name+'.txt')).write_text(source)
    with tempfile.TemporaryDirectory(prefix='one-leaf-mutant-TEST-') as temporary:
        root=Path(temporary)
        for path,raw in base.items():
            target=root/Path(path).relative_to('scripts/reference');target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text(source if path==file else raw)
        facade=root/'startup_transport.py'
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',STARTUP_FAMILY_UNDER_TEST=str(facade),
                 PYTHONPATH=str(ROOT/'tests/reference/one-leaf-envelope'))
        if test.startswith('old_family.'):
            # Exact unchanged public source test, copied only into this disposable
            # import path; its own test source and path binding are recorded.
            # Import the exact old public test in place, with only its
            # documented facade selector redirected to actual mutant inputs.
            test=test.replace('old_family.','test_family.');env['PYTHONPATH']=str(ROOT/'tests/reference/startup-prerequisite')
        argv=[sys.executable,'-B','-m','unittest',test,'-v']
        start=time.monotonic()
        try:p=subprocess.run(argv,cwd=ROOT,env=env,capture_output=True,timeout=20)
        except subprocess.TimeoutExpired as error:
            (folder/'stdout').write_bytes(error.stdout or b'');(folder/'stderr').write_bytes(error.stderr or b'')
            rows.append(dict(name=name,killed=False,timeout=True,compile_valid=True));continue
        (folder/'stdout').write_bytes(p.stdout);(folder/'stderr').write_bytes(p.stderr)
        import_valid=b'SyntaxError' not in p.stderr and b'ImportError' not in p.stderr and b'Failed to import test module' not in p.stderr and b'_FailedTest' not in p.stderr and b'Ran 1 test' in p.stderr
        killed=p.returncode!=0 and b'FAILED' in p.stderr and import_valid
        rows.append(dict(name=name,file=file,test=test,argv=argv,exit=p.returncode,
                         source_sha256=hashlib.sha256(source.encode()).hexdigest(),
                         compiler_inputs={path:hashlib.sha256((source if path==file else raw).encode()).hexdigest() for path,raw in base.items()},
                         compile_valid=True,import_valid=import_valid,killed=killed,seconds=time.monotonic()-start))
        print(name,'KILLED' if killed else 'SURVIVED',flush=True)
(OUT/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
raise SystemExit(0 if len(rows)==len(cases) and all(r.get('killed') for r in rows) else 1)
