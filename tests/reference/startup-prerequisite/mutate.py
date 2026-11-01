"""Finite source mutants through real public API/OS tests; no helper patching."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parents[3]
FAMILY=ROOT/'scripts/reference/startup_family'
OUT=Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True,exist_ok=False)
BASE={p.name:p.read_text() for p in FAMILY.glob('*.py')}
FACADE=(ROOT/'scripts/reference/startup_transport.py').read_text()
# Each tuple is an explicit semantic edit of the actual compiler/import input.
new=(
 ('managed-parent-deadman','lifetime.py',[
  ("        if select.select([self.parent_fd],[],[],0)[0]:\n            raise engine.Failure('ParentLost')","        if False:\n            raise engine.Failure('ParentLost')"),
  ("if any(flags&(select.POLLHUP|select.POLLERR) for _,flags in poll.poll(0)):","if False:"),
  ("engine.sample_processes(sessions,(self.parent,os.getpid()))","engine.sample_processes(sessions,(os.getpid(),))"),
  ("                if not chunk:\n                    self.fault('ControlLost');break","                if not chunk:\n                    time.sleep(.01);continue")],
  'FailureTests.test_real_coordinator_kill_contains_term_ignoring_child'),
 ('managed-foreign-peer','lifetime.py',[
  ("if (pid,uid,gid)!=(self.pid,obs['uid'],obs['gid']):","if False:")],
  'LiveSourceTests.test_closed_foreign_endpoint_sends_zero_bytes'),
 ('managed-ready-cached-authority','lifetime.py',[
  ("                    self.identity.verify()","                    pass"),
  ("    def current(self):\n        if self.identity is None", "    def current(self):\n        if self.last_identity is not None:return dict(self.last_identity)\n        if self.identity is None")],
  'ChannelTests.test_exec_full_reply_exit_refused'),
 ('source-hash','artifacts.py',[("if (actual,sha)!=(size,digest):","if False:")],
  'BoundaryTests.test_wrong_declared_hash_refuses'),
 ('source-io','artifacts.py',[("if self.io > self.policy.io_bytes:","if False:")],
  'StreamingTests.test_aggregate_source_io_cap'),
 ('copied-aggregate','artifacts.py',[("self.copied+row['size']>self.policy.copied_bytes","False")],
  'BoundaryTests.test_preparation_aggregate_preserves_existing_working'),
 ('retained-fd-cap','artifacts.py',[("if len(self.resource_descriptors)>=self.policy.resource_fds:","if False:")],
  'BoundaryTests.test_resource_descriptor_cap'),
 ('atomic-no-replace','artifacts.py',[("os.link(temporary,name,src_dir_fd=self.fd,dst_dir_fd=self.fd,follow_symlinks=False)",
  "os.replace(temporary,name,src_dir_fd=self.fd,dst_dir_fd=self.fd)")],
  'BoundaryTests.test_existing_foreign_target_bytes_unchanged'),
 ('epoch','artifacts.py',[("if row['epoch']!=ref['epoch']:","if False:")],
  'SuccessorTests.test_old_mutation_handle_stale_before_effect'),
 ('successor','lifetime.py',[("return MutationResult(**result,successor=successor)","return MutationResult(**result,successor=target)")],
  'SuccessorTests.test_successive_mutation_delivers_opaque_successor'),
 ('readonly-snapshot-epoch','artifacts.py',[("self.event('SNAPSHOT_VERIFIED',resource=ref['token'],epoch=row['epoch'])",
  "row['epoch']+=1")],'SuccessorTests.test_ready_snapshot_same_object_no_epoch_churn'),
 ('managed-process-limit','lifetime.py',[("if count>self.policy.processes:raise engine.Failure('ProcessLimit')","if False:raise engine.Failure('ProcessLimit')")],
  'ChannelTests.test_process_limit_during_progress'),
 ('managed-output-limit','lifetime.py',[("if self.buffers[index]>self.policy.stream_bytes or self.output>self.policy.output_bytes:","if False:")],
  'FailureTests.test_handoff_silence_does_not_stop_stream_monitor'),
 ('managed-lifetime','lifetime.py',[("if self.spawn_time is not None and now-self.spawn_time>=self.policy.total_seconds:","if False:")],
  'BoundaryTests.test_selected_total_lifetime_never_resets_at_handoff'),
 ('preparation-deadline','artifacts.py',[("if self.operation_deadline is not None and now >= self.operation_deadline:","if False:")],
  'BoundaryTests.test_selected_preparation_deadline'),
 ('ready-deadline-reset','lifetime.py',[("if time.monotonic()>=deadline:raise engine.Failure('ReadinessDeadline')",
   "deadline=time.monotonic()+1")],'ChannelTests.test_readiness_absolute_deadline'),
 ('immutable-source-stamp','lifetime.py',[("if engine._current_stamp(row['path'])!=tuple(row['stamp']):","if False:")],
  'LiveSourceTests.test_idle_resource_change_refuses_current_identity'),
)
# The old semantic falsifiers are replayed against their extracted actual locations.
old=(
 ('old-output','engine.py',[("if len(chunk) > allowed:","if False:")],'OSTests.test_stdout_limit'),
 ('old-before-observer','engine.py',[("self.run(dataclasses.replace(before_spawn, input_bytes=facts))","pass")],
  'OSTests.test_before_observer_failure_no_main_launch'),
 ('old-foreign-peer','engine.py',[("if pid != owner.pid or uid != os.getuid():","if False:")],
  'OSTests.test_foreign_endpoint_zero_commands'),
 ('old-source-validation','artifacts.py',[("            source.verify(limits.file_bytes)","            pass")],
  'OSTests.test_sources_changed_before_launch'),
 ('old-prior-publication','engine.py',[("os.link(temporary, name, src_dir_fd=self.fd, dst_dir_fd=self.fd, follow_symlinks=False)",
   "os.replace(temporary, name, src_dir_fd=self.fd, dst_dir_fd=self.fd)")],
  'OSTests.test_no_replace_publication_and_prior_json'),
 ('old-kernel-lifetime','engine.py',[("if identity is not None and observed is not None and observed != identity:","if False:")],
  'AdditionalOSTests.test_kernel_exec_change_after_binding_refuses'),
 ('old-journal-retarget','engine.py',[("if (os.fstat(fd).st_nlink != 1\n            or _stamp(os.stat(name,dir_fd=directory_fd,follow_symlinks=False))[:3] != identity):","if False:")],
  'AdditionalOSTests.test_journal_retarget_after_launch_refuses'),
 ('old-nested-monitor','engine.py',[("                self._monitor()","                pass")],
  'AdditionalOSTests.test_callback_cannot_hide_parent_output_or_deadline'),
 ('old-readiness-monitor','engine.py',[("        monitor()","        pass")],
  'ReadinessSupervisionTests.test_transient_same_owned_processes_cannot_hide_in_reply'),
 ('old-readiness-deadline','engine.py',[("min(deadline, readiness_deadline)","deadline")],
  'ReadinessSupervisionTests.test_readiness_budget_expires_after_observed_progress'),
 ('old-ready-acceptance','engine.py',[
  ("            wait_for(selectors.EVENT_READ)\n            owner.verify()\n","            wait_for(selectors.EVENT_READ)\n"),
  ("            checkpoint()\n            owner.verify()\n","            checkpoint()\n"),
  ("        owner.verify()\n        return True","        return True"),
  ("                                identity.verify()\n                                ready = matched","                                ready = matched")],
  'ReadinessIdentityTests.test_fast_exec_full_reply_exit_first'),
)
records=[]
for legacy,items in ((False,new),(True,old)):
 for name,file,edits,test in items:
  source=BASE[file]
  for before,after in edits:
   count=source.count(before)
   if count!=1:
    records.append(dict(name=name,construction_error='needle count '+str(count),killed=False))
    print(name,'INVALID_NEEDLE',count,flush=True);break
   source=source.replace(before,after)
  else:
   compile(source,file,'exec')
   folder=OUT/name;folder.mkdir()
   (folder/(file+'.txt')).write_text(source)
   with tempfile.TemporaryDirectory(prefix='startup-source-mutant-') as temporary:
    root=Path(temporary);package=root/'startup_family';package.mkdir()
    for part,raw in BASE.items():(package/part).write_text(source if part==file else raw)
    facade=root/'startup_transport.py';facade.write_text(FACADE)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    env['STARTUP_TRANSPORT_UNDER_TEST' if legacy else 'STARTUP_FAMILY_UNDER_TEST']=str(facade)
    env['PYTHONPATH']=str(ROOT/('tests/reference/startup-seam' if legacy else 'tests/reference/startup-prerequisite'))
    argv=[sys.executable,'-B','-m','unittest',('test_transport.' if legacy else 'test_family.')+test,'-v']
    started=time.monotonic()
    p=subprocess.run(argv,cwd=ROOT,env=env,capture_output=True,timeout=12)
    (folder/'stdout').write_bytes(p.stdout);(folder/'stderr').write_bytes(p.stderr)
    valid=b'SyntaxError' not in p.stderr and b'ImportError' not in p.stderr
    killed=p.returncode!=0 and b'FAILED' in p.stderr and valid
    row=dict(name=name,file=file,sha256=hashlib.sha256(source.encode()).hexdigest(),test=test,
             argv=argv,exit=p.returncode,compile_valid=True,import_valid=valid,killed=killed,
             seconds=time.monotonic()-started)
    records.append(row);print(name,'KILLED' if killed else 'SURVIVED',flush=True)
(OUT/'results.json').write_text(json.dumps(records,indent=2)+'\n')
raise SystemExit(0 if all(x['killed'] for x in records) else 1)
