"""Public stopped history/read-only/helper/chunk acceptance on authored files."""
import copy
import dataclasses
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest
ROOT=Path(__file__).resolve().parents[3]
FACADE=Path(os.environ.get('STARTUP_FAMILY_UNDER_TEST',ROOT/'scripts/reference/startup_transport.py'))
sp=importlib.util.spec_from_file_location('readonly_acceptance',FACADE);st=importlib.util.module_from_spec(sp);sp.loader.exec_module(st)
def request(p):
 raw=p.read_bytes();return st.SourceRequest(str(p),len(raw),hashlib.sha256(raw).hexdigest())
class DerivationTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(prefix='readonly-TEST-');self.root=Path(self.tmp.name);self.s=None
 def tearDown(self):
  if self.s:
   try:self.s.close()
   except st.StartupFailure:pass
  output=os.environ.get('DERIVATION_JOURNAL_RESULTS')
  if output and (self.root/'work/session.jsonl').exists():
   dest=Path(output);dest.mkdir(parents=True,exist_ok=True)
   (dest/(self.id()+'.jsonl')).write_bytes((self.root/'work/session.jsonl').read_bytes())
  self.tmp.cleanup()
 def prepare(self,**env):
  now=time.monotonic();self.s=st.open_session(st.NewWorkspace(str(self.root/'work')),st.StreamPolicy(),st.ManagedPolicy(),envelope=st.SharedEnvelopePolicy(origin=now,end=now+15,**env))
  p=self.root/'input';p.write_bytes(b'authored readonly TEST\n'*100)
  self.working=self.s.prepare(self.s.capture(request(p)),'working');py=Path(sys.executable).resolve();self.py=str(py)
  self.tool=self.s.tool(self.s.capture(request(py)));return self.s
 def stopped(self,**env):
  s=self.prepare(**env);p=s.launch(st.LaunchSpec(self.tool,(self.py,'-c','import time;time.sleep(.25)')),resources=(self.working,))
  self.process=p;self.exit=p.finish();self.snapshot=s.snapshot(self.working);self.working=self.snapshot.successor
  self.input=s.seal_stopped(self.working);return s
 def spec(self,body=None,outputs=None,seconds=3):
  if body is None:body='import pathlib,sys,time;time.sleep(.15);p=pathlib.Path(sys.argv[1]);pathlib.Path(sys.argv[2]).write_bytes(p.read_bytes().upper()+b"derived");time.sleep(.1)'
  return st.DerivationSpec(self.tool,(self.py,'-c',body,st.ResourceArgument('',self.input,''),st.OutputArgument(0)),
    outputs or (st.OutputSpec('result',8192),),budget=st.JobBudget(seconds=seconds))
 def read(self,artifact):
  data=bytearray();offset=0
  while True:
   c=self.s.read_chunk(artifact,offset,16384);self.assertLessEqual(len(c.data),16384);self.assertEqual(c.offset,offset)
   data.extend(c.data);offset+=len(c.data)
   if c.eof:break
  return bytes(data)
 def test_genuine_chain_output_and_cumulative_usage(self):
  s=self.stopped();a=s.usage();batch=s.derive_readonly((self.input,),self.spec());b=s.usage()
  self.assertEqual(b.original_state,'STOPPED');self.assertEqual(b.helper_state,'STOPPED');self.assertEqual(b.helper_charged_operations,1)
  self.assertEqual(b.charged_operations,a.charged_operations+1);self.assertGreater(b.source_io,a.source_io)
  expected=(b'authored readonly TEST\n'*100).upper()+b'derived';self.assertEqual(self.read(batch.artifacts[0]),expected)
  self.assertEqual(batch.outputs[0].sha256,hashlib.sha256(expected).hexdigest());self.assertTrue(self.exit.identity_at_exit_unproved);self.assertEqual(self.exit.daemon_state,'UNKNOWN');self.assertTrue(batch.helper_exit.identity_at_exit_unproved);self.assertEqual(batch.helper_exit.daemon_state,'UNKNOWN')
 def test_no_original_no_seal(self):
  self.prepare()
  with self.assertRaises(st.StartupFailure):self.s.seal_stopped(self.working)
 def test_original_stop_requires_actual_snapshot_successor(self):
  s=self.prepare();p=s.launch(st.LaunchSpec(self.tool,(self.py,'-c','import time;time.sleep(.2)')),resources=(self.working,));p.finish()
  with self.assertRaises(st.StartupFailure):s.seal_stopped(self.working)
 def test_old_mutable_consumed(self):
  s=self.stopped()
  with self.assertRaises(st.StartupFailure):s.snapshot(self.working)
 def test_readonly_opaque_and_facts_not_authority(self):
  s=self.stopped()
  with self.assertRaises(TypeError):copy.copy(self.input)
  with self.assertRaises(TypeError):st.StoppedReadLease()
  with self.assertRaises(st.StartupFailure):s.seal_stopped(self.exit)
 def test_retained_readonly_reused_for_sequential_jobs(self):
  s=self.stopped();a=s.derive_readonly((self.input,),self.spec())
  b=s.derive_readonly((self.input,),dataclasses.replace(self.spec(),outputs=(st.OutputSpec('second',8192),)))
  self.assertEqual(self.read(a.artifacts[0]),self.read(b.artifacts[0]));self.assertEqual(s.usage().helper_charged_operations,2)
 def test_no_clobber_prior_bytes(self):
  s=self.stopped();prior=self.root/'work/result';prior.write_bytes(b'foreign prior')
  with self.assertRaises(st.StartupFailure):s.derive_readonly((self.input,),self.spec())
  self.assertEqual(prior.read_bytes(),b'foreign prior')
 def test_required_missing_refuses(self):
  s=self.stopped()
  with self.assertRaises(st.StartupFailure):s.derive_readonly((self.input,),self.spec('import time;time.sleep(.2)'))
 def test_expected_absence_positive(self):
  s=self.stopped();batch=s.derive_readonly((self.input,),self.spec(outputs=(st.OutputSpec('result',8192),st.OutputSpec('absent',0,False))))
  self.assertEqual(len(batch.artifacts),1);self.assertTrue(batch.outputs[1].expected_absent);self.assertTrue(batch.outputs[1].absence_proved)
 def test_changed_input_after_seal_refuses(self):
  s=self.stopped();p=self.root/'work/working';p.chmod(0o600);p.write_bytes(b'changed')
  with self.assertRaises(st.StartupFailure):s.derive_readonly((self.input,),self.spec())
 def test_nonzero_retains_partial_without_handles(self):
  s=self.stopped()
  with self.assertRaises(st.StartupFailure):s.derive_readonly((self.input,),self.spec('import pathlib,sys,time;time.sleep(.15);pathlib.Path(sys.argv[2]).write_bytes(b"partial");sys.exit(7)'))
  self.assertFalse((self.root/'work/result').exists())
 def test_sequential_chunk_replay_denied(self):
  s=self.stopped();b=s.derive_readonly((self.input,),self.spec());s.read_chunk(b.artifacts[0],0,16)
  with self.assertRaises(st.StartupFailure):s.read_chunk(b.artifacts[0],0,16)
 def test_chunk_cap_before_read(self):
  s=self.stopped();b=s.derive_readonly((self.input,),self.spec())
  with self.assertRaises(st.StartupFailure):s.read_chunk(b.artifacts[0],0,16385)
 def test_empty_required_output_is_genuine(self):
  s=self.stopped();body='import pathlib,sys,time;time.sleep(.15);pathlib.Path(sys.argv[2]).write_bytes(b"");time.sleep(.1)'
  b=s.derive_readonly((self.input,),self.spec(body,outputs=(st.OutputSpec('empty',0),)))
  self.assertEqual(self.read(b.artifacts[0]),b'');self.assertEqual(b.outputs[0].size,0)
 def test_helper_reads_prior_derived_input(self):
  s=self.stopped();a=s.derive_readonly((self.input,),self.spec())
  spec=dataclasses.replace(self.spec(),argv=(self.py,'-c','import pathlib,sys,time;time.sleep(.15);p=pathlib.Path(sys.argv[1]);pathlib.Path(sys.argv[2]).write_bytes(p.read_bytes()+b"second");time.sleep(.1)',st.ResourceArgument('',a.artifacts[0],''),st.OutputArgument(0)),outputs=(st.OutputSpec('second',8192),))
  b=s.derive_readonly((a.artifacts[0],),spec)
  self.assertEqual(self.read(b.artifacts[0]),self.read(a.artifacts[0])+b'second')
 def test_helper_parent_is_same_worker(self):
  s=self.stopped();body='import os,pathlib,sys,time;time.sleep(.15);pathlib.Path(sys.argv[2]).write_text(str(os.getppid()));time.sleep(.1)'
  b=s.derive_readonly((self.input,),self.spec(body))
  self.assertEqual(int(self.read(b.artifacts[0])),b.supervisor_pid)
  self.assertNotEqual(b.helper_identity.pid,self.exit.created_pid)
  with self.assertRaises(st.StartupFailure):self.process.verify_current()
 def test_all_required_checked_before_any_handle_or_final(self):
  s=self.stopped();spec=self.spec(outputs=(st.OutputSpec('result',8192),st.OutputSpec('required-second',8192)))
  with self.assertRaises(st.StartupFailure):s.derive_readonly((self.input,),spec)
  self.assertFalse((self.root/'work/result').exists());self.assertFalse((self.root/'work/required-second').exists())
 def test_input_mutation_retains_true_partial(self):
  s=self.stopped();body='import pathlib,sys,time;time.sleep(.15);p=pathlib.Path(sys.argv[1]);p.chmod(0o600);p.write_bytes(b"partial changed");pathlib.Path(sys.argv[2]).write_bytes(b"produced output");time.sleep(.2)'
  with self.assertRaises(st.StartupFailure):s.derive_readonly((self.input,),self.spec(body))
  self.assertEqual((self.root/'work/working').read_bytes(),b'partial changed')
 def test_source_drift_before_job(self):
  s=self.stopped();(self.root/'input').write_bytes(b'source changed')
  with self.assertRaises(st.StartupFailure):s.derive_readonly((self.input,),self.spec())
  self.assertFalse((self.root/'work/result').exists())
 def test_helper_descendant_denies_output(self):
  s=self.stopped();body='import os,time;time.sleep(.15)\nif os.fork()==0:time.sleep(1);os._exit(0)\ntime.sleep(.1)'
  with self.assertRaises(st.StartupFailure):s.derive_readonly((self.input,),self.spec(body))
 def test_helper_progress_cannot_reset_job_deadline(self):
  s=self.stopped();body='import os,time;time.sleep(.1)\nwhile True:os.write(1,b"progress");time.sleep(.02)'
  with self.assertRaises(st.StartupFailure) as e:s.derive_readonly((self.input,),self.spec(body,seconds=.4))
  self.assertEqual(e.exception.code,'HelperDeadline')
 def test_actual_fsize_partial_denied(self):
  s=self.stopped();body='import pathlib,sys,time;time.sleep(.15);pathlib.Path(sys.argv[2]).write_bytes(b"x"*10000);time.sleep(.1)'
  with self.assertRaises(st.StartupFailure):s.derive_readonly((self.input,),self.spec(body,outputs=(st.OutputSpec('result',100),)))
  self.assertFalse((self.root/'work/result').exists())
  partials=list((self.root/'work').glob('.derive-*'));self.assertTrue(partials);self.assertLessEqual(max(p.stat().st_size for p in partials),100)
 def test_actual_journal_persistence_loss_denies_handles(self):
  s=self.stopped();body='import pathlib,sys,time;time.sleep(.15);pathlib.Path(sys.argv[2]).write_bytes(b"partial");pathlib.Path("session.jsonl").write_bytes(b"");time.sleep(.1)'
  with self.assertRaises(st.StartupFailure) as e:s.derive_readonly((self.input,),self.spec(body))
  self.assertFalse(e.exception.observation.journal_durable)
  self.assertFalse((self.root/'work/result').exists())
 def test_chunk_exact_brokered_byte_delta(self):
  s=self.stopped();b=s.derive_readonly((self.input,),self.spec());a=s.usage();chunk=s.read_chunk(b.artifacts[0],0,16);c=s.usage()
  self.assertEqual(c.source_io-a.source_io,16);self.assertEqual(c.control_messages-a.control_messages,6);self.assertEqual(c.sequence-a.sequence,2)
 def test_changed_output_inode_denies_bytes(self):
  s=self.stopped();b=s.derive_readonly((self.input,),self.spec());other=self.root/'other';other.write_bytes(b'foreign');os.replace(other,self.root/'work/result')
  with self.assertRaises(st.StartupFailure):s.read_chunk(b.artifacts[0],0,16)
 def test_hardlink_output_denies_bytes(self):
  s=self.stopped();b=s.derive_readonly((self.input,),self.spec());os.link(self.root/'work/result',self.root/'linked')
  with self.assertRaises(st.StartupFailure):s.read_chunk(b.artifacts[0],0,16)
 def test_symlink_output_preserves_foreign_target(self):
  s=self.stopped();b=s.derive_readonly((self.input,),self.spec());p=self.root/'work/result';p.unlink();p.symlink_to(self.root/'input')
  with self.assertRaises(st.StartupFailure):s.read_chunk(b.artifacts[0],0,16)
  self.assertEqual((self.root/'input').read_bytes(),b'authored readonly TEST\n'*100)
 def test_unexpected_expected_absent_slot_denies_batch(self):
  s=self.stopped();body='import pathlib,sys,time;time.sleep(.15);pathlib.Path(sys.argv[2]).write_bytes(b"ok");pathlib.Path(sys.argv[3]).touch();time.sleep(.1)'
  spec=dataclasses.replace(self.spec(body,outputs=(st.OutputSpec('result',8192),st.OutputSpec('absent',0,False))),argv=(self.py,'-c',body,st.ResourceArgument('',self.input,''),st.OutputArgument(0),st.OutputArgument(1)))
  with self.assertRaises(st.StartupFailure):s.derive_readonly((self.input,),spec)
 def test_cumulative_command_exhaustion_after_first_helper(self):
  s=self.stopped(commands=2);s.derive_readonly((self.input,),self.spec())
  with self.assertRaises(st.StartupFailure):s.derive_readonly((self.input,),dataclasses.replace(self.spec(),outputs=(st.OutputSpec('second',8192),)))
 def test_later_job_io_budget_cannot_reset_existing_spend(self):
  s=self.stopped();before=s.usage();self.assertGreater(before.source_io,0)
  with self.assertRaises(st.StartupFailure):s.derive_readonly((self.input,),dataclasses.replace(self.spec(),budget=st.JobBudget(seconds=3,io_bytes=64)))
  self.assertFalse((self.root/'work/result').exists())
 def test_multiple_chunks_independent_bytes_hash_and_eof_replay(self):
  s=self.stopped();body='import pathlib,sys,time;time.sleep(.15);pathlib.Path(sys.argv[2]).write_bytes(bytes(range(256))*256);time.sleep(.1)'
  b=s.derive_readonly((self.input,),self.spec(body,outputs=(st.OutputSpec('result',65536),)))
  self.assertEqual(self.read(b.artifacts[0]),bytes(range(256))*256)
  with self.assertRaises(st.StartupFailure):s.read_chunk(b.artifacts[0],65536,1)
 def test_bad_spec_path_before_job_effects(self):
  s=self.stopped()
  with self.assertRaises(st.StartupFailure):s.derive_readonly((self.input,),self.spec(outputs=(st.OutputSpec('../outside',4),)))
  self.assertFalse((self.root/'outside').exists())
 def test_no_second_original_after_derivation(self):
  s=self.stopped();s.derive_readonly((self.input,),self.spec())
  with self.assertRaises(st.StartupFailure):s.launch(st.LaunchSpec(self.tool,(self.py,'-c','import time;time.sleep(.2)')))
 def test_real_helper_selected_fd_pressure(self):
  s=self.stopped();body='import pathlib,sys,time,os;time.sleep(.15);fds=[os.open("/dev/null",os.O_RDONLY) for _ in range(25)];pathlib.Path(sys.argv[2]).write_bytes(b"ok");time.sleep(.3)'
  spec=dataclasses.replace(self.spec(body),budget=st.JobBudget(seconds=3,fds=46))
  with self.assertRaises(st.StartupFailure) as e:s.derive_readonly((self.input,),spec)
  self.assertEqual(e.exception.code,'FDLimit')
 def test_helper_fd_pressure_positive_control(self):
  s=self.stopped();body='import pathlib,sys,time,os;time.sleep(.15);fds=[os.open("/dev/null",os.O_RDONLY) for _ in range(25)];pathlib.Path(sys.argv[2]).write_bytes(b"ok");time.sleep(.3)'
  b=s.derive_readonly((self.input,),self.spec(body));self.assertEqual(self.read(b.artifacts[0]),b'ok')
 def test_real_helper_selected_rss_pressure(self):
  s=self.stopped();body='import time;time.sleep(.15);raw=bytearray(96*1048576);time.sleep(.4)'
  with self.assertRaises(st.StartupFailure) as e:s.derive_readonly((self.input,),dataclasses.replace(self.spec(body),budget=st.JobBudget(seconds=3,rss_bytes=100*1048576)))
  self.assertEqual(e.exception.code,'RSSLimit')
 def test_real_helper_selected_process_pressure(self):
  s=self.stopped();body='import os,time;time.sleep(.15)\nif os.fork()==0:time.sleep(.4);os._exit(0)\ntime.sleep(.3);os.wait()'
  with self.assertRaises(st.StartupFailure) as e:s.derive_readonly((self.input,),dataclasses.replace(self.spec(body),budget=st.JobBudget(seconds=3,processes=3)))
  self.assertEqual(e.exception.code,'ProcessLimit')
 def test_stale_pre_snapshot_epoch_cannot_seal(self):
  s=self.prepare();old=self.working
  p=s.launch(st.LaunchSpec(self.tool,(self.py,'-c','import time;time.sleep(.2)')),resources=(old,));p.finish();s.snapshot(old)
  with self.assertRaises(st.StartupFailure):s.seal_stopped(old)
if __name__=='__main__':unittest.main()
