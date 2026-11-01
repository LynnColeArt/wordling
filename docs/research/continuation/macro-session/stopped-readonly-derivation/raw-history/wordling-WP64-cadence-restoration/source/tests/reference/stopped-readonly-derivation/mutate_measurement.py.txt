"""Finite source-valid measurement mutants through actual public OS operations."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(sys.argv[1]);OUT.mkdir(parents=True,exist_ok=False)
paths=['startup_transport.py']+['startup_family/'+n for n in ('__init__.py','engine.py','artifacts.py','lifetime.py')]
base={p:(ROOT/'scripts/reference'/p).read_text() for p in paths};life='startup_family/lifetime.py'
prefix='test_measurement_completion.'
cases=[
 ('v2-mapped-to10ms',[("'bounded-original-v2':.100","'bounded-original-v2':.010",1)],prefix+'ActualCompletionTests.test_actual_accessible_census_and_full_readonly_chain'),
 ('v1-silently-relaxed',[("'bounded-original-v1':.010","'bounded-original-v1':.100",1)],prefix+'V1ClockTests.test_v1_first_successful_full_census_overshoot_refuses_without_pending'),
 ('strict-auto-completion',[("self.envelope.measurement_completion in (\"bounded-original-v1\",\"bounded-original-v2\")","self.envelope.measurement_completion in (\"strict\",\"bounded-original-v1\",\"bounded-original-v2\")",1),
  ("self.envelope.measurement_completion in ('bounded-original-v1','bounded-original-v2')","self.envelope.measurement_completion in ('strict','bounded-original-v1','bounded-original-v2')",2),
  ("window={'bounded-original-v1':.010,","window={'strict':.100,'bounded-original-v1':.010,",1)],prefix+'LiveRefusalTests.test_omitted_and_explicit_strict_remain_fail_first'),
 ('missing-mismatch-ack',[("or ack!=expected_mode","or False",1)],prefix+'CreationTests.test_real_committed_ack_refusal_keeps_setup_and_charge_facts'),
 ('trailing-numeric-not-validated',[("        for name,maximum in maxima.items():\n","        for name,maximum in maxima.items():\n            if name=='endpoint_bytes':continue\n",1)],prefix+'PolicyTests.test_all_numeric_fields_still_validated'),
 ('origin-excludes-complete-scan',[("                census_complete=True\n","                origin=time.monotonic();end=origin+window;timeout='MeasurementUnknown'\n                census_complete=True\n",1)],prefix+'V1ClockTests.test_v1_first_successful_full_census_overshoot_refuses_without_pending'),
 ('first-success-postcheck-removed',[("                self._measurement_dimensions(count,rss,actors)\n                self._measurement_guard(end,timeout)\n                if pending is not None:","                self._measurement_dimensions(count,rss,actors)\n                if pending is not None:",1)],prefix+'V1ClockTests.test_v1_first_successful_full_census_overshoot_refuses_without_pending'),
 ('earlier-finish-end-excluded',[("                (self.publication_deadline,self.publication_timeout),\n","",1)],'test_measurement_controls.PendingRefusalTests.test_accessible_census_returning_after_earlier_finish_clock_refuses'),
 ('attempt-bound-removed',[("                    if attempts>=3:raise","                    if False:raise",1)],'test_measurement_controls.PendingRefusalTests.test_persistent_unobservable_exhausts_one_finite_transaction'),
 ('completed-violation-discarded',[("                        self._measurement_dimensions(detail['census_processes'],detail['census_rss'],detail.get('completed_actors',()))","                        pass",1)],'test_measurement_controls.ResourcePriorityTests.test_simultaneous_rss_violation_wins_before_pending'),
 ('helper-borrows-original-role',[("and job is self.original_job and self.foreground_launched","and self.foreground_launched",1),
  ("and not job.helper and not job.mode_mutation and not job.reaped","and not job.mode_mutation and not job.reaped",1)],prefix+'OtherRoleRefusalTests.test_helper_cannot_borrow_original_window'),
 ('prior-fault-operational-reentry',[("or (self._fault and not allow_fault)","or False",1),("if self._fault and not allow_fault:","if False:",1),
  ("if self.first_fault:raise engine.Failure(self.first_fault)\n","if False:raise engine.Failure(self.first_fault)\n",1),
  ("        if self.first_fault:\n            raise engine.Failure(self.first_fault)","        if False:\n            raise engine.Failure(self.first_fault)",2)],'test_measurement_controls.PendingRefusalTests.test_persistent_unobservable_exhausts_one_finite_transaction'),
 ('gap-erases-real-peaks',[("                    self.event('MEASUREMENT_COMPLETED',", "                    self.peak_processes=self.peak_rss=self.peak_fds=0;self.actor_fd_peaks={}\n                    self.event('MEASUREMENT_COMPLETED',",1)],prefix+'ActualCompletionTests.test_actual_accessible_census_and_full_readonly_chain'),
 ('original-member-omitted',[("actors,count,rss=engine.sample_actors(sessions,(self.parent,os.getpid()),completed_dimensions=True)","actors,count,rss=engine.sample_actors((),(self.parent,os.getpid()),completed_dimensions=True)",1)],prefix+'ActualCompletionTests.test_actual_accessible_census_and_full_readonly_chain'),
 ('lost-end-release-raises-again',[("if error.errno!=errno.EBADF:raise","raise",1)],'test_measurement_loss.PendingLossTests.test_control_loss_during_pending'),
]
(OUT/'roster.json').write_text(json.dumps([dict(name=n,test=t,edits=e) for n,e,t in cases],indent=2)+'\n')
rows=[]
for name,edits,test in cases:
 folder=OUT/name;folder.mkdir();source=base[life];valid=True
 for before,after,expected in edits:
  count=source.count(before)
  if count!=expected:
   rows.append(dict(name=name,construction_error=dict(actual=count,expected=expected,needle=before),killed=False));valid=False;break
  source=source.replace(before,after)
 if not valid:continue
 compile(source,life,'exec');(folder/'lifetime.py.txt').write_text(source)
 with tempfile.TemporaryDirectory(prefix='measurement-mutant-TEST-') as tmp:
  root=Path(tmp)
  for path,raw in base.items():
   dest=root/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(source if path==life else raw)
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',STARTUP_FAMILY_UNDER_TEST=str(root/'startup_transport.py'),PYTHONPATH=str(ROOT/'tests/reference/stopped-readonly-derivation'),MEASUREMENT_RESULTS=str(folder/'observations'),DERIVATION_JOURNAL_RESULTS=str(folder/'journals'))
  argv=[sys.executable,'-B','-m','unittest',test,'-v'];start=time.monotonic()
  try:result=subprocess.run(argv,cwd=ROOT,env=env,capture_output=True,timeout=25)
  except subprocess.TimeoutExpired as error:
   (folder/'stdout').write_bytes(error.stdout or b'');(folder/'stderr').write_bytes(error.stderr or b'');rows.append(dict(name=name,timeout=True,killed=False));continue
  (folder/'stdout').write_bytes(result.stdout);(folder/'stderr').write_bytes(result.stderr)
  imported=all(x not in result.stderr for x in (b'SyntaxError',b'ImportError',b'_FailedTest')) and b'Ran 1 test' in result.stderr
  killed=result.returncode!=0 and b'FAILED' in result.stderr and imported
  rows.append(dict(name=name,test=test,argv=argv,exit=result.returncode,compile_valid=True,import_valid=imported,killed=killed,seconds=time.monotonic()-start,
   actual_inputs={path:hashlib.sha256((source if path==life else raw).encode()).hexdigest() for path,raw in base.items()}))
  print(name,'KILLED' if killed else 'SURVIVED',flush=True)
 (OUT/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
raise SystemExit(0 if len(rows)==len(cases) and all(row.get('killed') for row in rows) else 1)
