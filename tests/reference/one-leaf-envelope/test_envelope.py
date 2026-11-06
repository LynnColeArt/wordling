"""Public one-leaf envelope acceptance, using only authored harmless processes."""
import dataclasses
import hashlib
import importlib.util
import os
import json
import struct
from pathlib import Path
import sys
import tempfile
import time
import unittest

ROOT=Path(__file__).resolve().parents[3]
FACADE=Path(os.environ.get('STARTUP_FAMILY_UNDER_TEST',ROOT/'scripts/reference/startup_transport.py'))
spec=importlib.util.spec_from_file_location('envelope_public',FACADE)
st=importlib.util.module_from_spec(spec);spec.loader.exec_module(st)

def request(path):
    raw=path.read_bytes()
    return st.SourceRequest(str(path),len(raw),hashlib.sha256(raw).hexdigest())

class EnvelopeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='one-leaf-TEST-')
        self.root=Path(self.tmp.name);self.session=None
    def tearDown(self):
        if self.session:
            try:self.session.close()
            except st.StartupFailure:pass
        self.tmp.cleanup()
    def open(self,seconds=5,**kw):
        now=time.monotonic()
        policy=st.SharedEnvelopePolicy(origin=now,end=now+seconds,**kw)
        self.session=st.open_session(st.NewWorkspace(str(self.root/'work')),
                                    st.StreamPolicy(),st.ManagedPolicy(),envelope=policy)
        return self.session
    def launch(self,body,**kw):
        session=self.open(**kw)
        script=self.root/'child.py';script.write_text(body)
        source=session.capture(request(script));python=Path(sys.executable).resolve()
        tool=session.tool(session.capture(request(python)))
        p=session.launch(st.LaunchSpec(tool,(str(python),'-B',st.ResourceArgument('',source,''))))
        return session,p
    def test_live_usage_and_exact_known_byte_trace(self):
        s=self.open();p=self.root/'data';p.write_bytes(b'abcde'*7)
        a=s.usage();r=s.capture(request(p));b=s.usage();w=s.prepare(r,'copy');c=s.usage()
        self.assertEqual(b.source_io-a.source_io,35)
        self.assertEqual(c.source_io-b.source_io,140) # read+write+source verify+target verify
        self.assertEqual(c.prepared_bytes,35)
        self.assertEqual(c.charged_operations,0)
        self.assertGreater(c.control_messages,b.control_messages)
        self.assertGreater(c.control_wire_bytes,b.control_wire_bytes)
        self.assertGreater(c.reserved_response_bytes,0)
        self.assertEqual(c.reserved_response_messages,2)
        self.assertEqual(c.sequence-b.sequence,2)
        self.assertGreater(c.current_fds,0)
        self.assertEqual(sum(x[2] for x in c.actor_fds),c.current_fds)
        self.assertIsNone(c.helper_state)
        self.assertIsNone(c.helper_charged_operations)
        self.assertEqual(s.snapshot(w).sha256,request(p).sha256)
        with self.assertRaises(dataclasses.FrozenInstanceError):c.source_io=0
    def test_exact_control_frame_trace(self):
        s=self.open();a=s.usage();b=s.usage()
        # Independent reconstruction from public immutable facts, not private
        # Session counters or a submitted accounting assertion.
        raw=json.dumps(dict(stage='provisional',generation=a.session_id,sequence=a.sequence,
                            ok=True,value=dataclasses.asdict(a)),separators=(',',':')).encode()
        commit=json.dumps(dict(stage='commit',generation=a.session_id,sequence=a.sequence,
                sha256=hashlib.sha256(raw).hexdigest()),separators=(',',':')).encode()
        request_raw=json.dumps(dict(generation=a.session_id,sequence=b.sequence,
                operation='usage',args={}),separators=(',',':')).encode()
        self.assertEqual(b.control_wire_bytes-a.control_wire_bytes,len(raw)+len(commit)+len(request_raw)+12)
        self.assertEqual(a.control_messages,3) # HELLO provisional+commit, usage request
        self.assertEqual(b.control_messages-a.control_messages,3)
        self.assertEqual(b.sequence,a.sequence+1)
        self.assertEqual(a.lost_response_bytes,0)

    def test_three_positional_default(self):
        self.session=st.open_session(st.NewWorkspace(str(self.root/'work')),st.StreamPolicy(),st.ManagedPolicy())
        self.assertIsInstance(self.session.usage(),st.UsageObservation)
    def test_expired_before_effect(self):
        now=time.monotonic()
        policy=st.SharedEnvelopePolicy(origin=now-2,end=now-1)
        with self.assertRaises(st.StartupFailure):
            st.open_session(st.NewWorkspace(str(self.root/'work')),st.StreamPolicy(),st.ManagedPolicy(),envelope=policy)
        self.assertFalse((self.root/'work').exists())
    def test_invalid_policy(self):
        for key,value in [('origin',float('nan')),('end',float('inf')),('fds',65),('fds',True),
                          ('commands',17),('source_io',4294967297),('control_messages',4097)]:
            with self.subTest(key=key,value=value):
                fields=dict(origin=time.monotonic(),end=time.monotonic()+1);fields[key]=value
                with self.assertRaises(st.Failure):st.SharedEnvelopePolicy(**fields)
    def test_abs_clock_remains_during_idle_and_sticky(self):
        s=self.open(seconds=.15);time.sleep(.22)
        with self.assertRaises(st.StartupFailure) as e:s.usage()
        self.assertIn(e.exception.code,('EnvelopeDeadline','ControlLost','CleanupUnknown'))
        with self.assertRaises(st.StartupFailure):s.usage()
    def test_output_pressure(self):
        s,p=self.launch('import os,time;time.sleep(.12);os.write(1,b"x"*4096);time.sleep(.2)',output_bytes=1024)
        with self.assertRaises(st.StartupFailure):p.finish()
    def test_actual_coordinator_fd_pressure(self):
        s=self.open(fds=40)
        fds=[os.open('/dev/null',os.O_RDONLY) for _ in range(40)]
        try:
            with self.assertRaises(st.StartupFailure) as e:s.usage()
            self.assertEqual(e.exception.code,'FDLimit')
        finally:
            for f in fds:os.close(f)
    def test_process_pressure(self):
        s,p=self.launch('import os,time;time.sleep(.15)\nif os.fork()==0:time.sleep(.3);os._exit(0)\ntime.sleep(.4);os.wait()',processes=3)
        with self.assertRaises(st.StartupFailure) as e:p.finish()
        self.assertEqual(e.exception.code,'ProcessLimit')
    def test_observation_is_not_usage_input(self):
        s=self.open();value=s.usage()
        with self.assertRaises(TypeError):s.usage(value)
        self.assertGreater(s.usage().sequence,value.sequence)

    def test_usage_observation_cannot_authorize_capture(self):
        s=self.open();u=s.usage()
        with self.assertRaises(st.StartupFailure):s.capture(u)
    def test_source_io_cumulative(self):
        s=self.open(source_io=100);p=self.root/'data';p.write_bytes(b'x'*30)
        r=s.capture(request(p))
        with self.assertRaises(st.StartupFailure):s.prepare(r,'copy')
        with self.assertRaises(st.StartupFailure):s.usage()
    def test_wire_reservation_refuses_before_large_effect(self):
        s=self.open(control_wire_bytes=140000);p=self.root/'data';p.write_bytes(b'x')
        r=s.capture(request(p));s.usage()
        # Drain available cumulative credits with real committed measurements.
        count=0
        try:
            while count<150:s.usage();count+=1
        except st.StartupFailure:pass
        else:self.fail('wire budget never enforced')
        with self.assertRaises(st.StartupFailure):s.prepare(r,'must-not-exist')
        self.assertFalse((self.root/'work/must-not-exist').exists())
    def test_preparation_active_stopped_share_io_credit(self):
        python=Path(sys.executable).resolve();n=python.stat().st_size
        s=self.open(source_io=5*n+10000)
        data=self.root/'data';data.write_bytes(b'leaf')
        working=s.prepare(s.capture(request(data)),'copy')
        tool=s.tool(s.capture(request(python)))
        p=s.launch(st.LaunchSpec(tool,(str(python),'-c','import time;time.sleep(.4)')),resources=(working,))
        before=s.usage();p.finish();snap=s.snapshot(working);after=s.usage()
        self.assertGreater(after.source_io,before.source_io)
        self.assertEqual(after.charged_operations,1)
        with self.assertRaises(st.StartupFailure):s.snapshot(snap.successor)
        with self.assertRaises(st.StartupFailure):s.usage()
    def test_alias_new_types_and_exact_policy_class(self):
        alias_spec=importlib.util.spec_from_file_location('envelope_alias',FACADE)
        alias=importlib.util.module_from_spec(alias_spec);alias_spec.loader.exec_module(alias)
        self.assertIs(alias.SharedEnvelopePolicy,st.SharedEnvelopePolicy)
        self.assertIs(alias.UsageObservation,st.UsageObservation)
        class Pretender(st.SharedEnvelopePolicy):pass
        now=time.monotonic()
        with self.assertRaises(st.StartupFailure):
            st.open_session(st.NewWorkspace(str(self.root/'work')),st.StreamPolicy(),st.ManagedPolicy(),
                            envelope=Pretender(origin=now,end=now+1))
        self.assertFalse((self.root/'work').exists())
    def test_real_rss_pressure(self):
        s,p=self.launch('import time;time.sleep(.15);a=bytearray(96*1048576);time.sleep(.4)',rss_bytes=100*1048576)
        with self.assertRaises(st.StartupFailure) as e:p.finish()
        self.assertEqual(e.exception.code,'RSSLimit')
    def test_usage_source_drift_is_sticky(self):
        s=self.open();data=self.root/'data';data.write_bytes(b'leaf');s.capture(request(data))
        data.write_bytes(b'changed')
        with self.assertRaises(st.StartupFailure) as e:s.usage()
        self.assertEqual(e.exception.code,'SourceChanged')
        with self.assertRaises(st.StartupFailure):s.usage()

    def test_actual_checked_endpoint_bytes(self):
        s,p=self.launch('import socket,time; s=socket.socket(socket.AF_UNIX);s.bind("peer");s.listen(1);c,_=s.accept();assert c.recv(4)==b"ping";c.sendall(b"ok");time.sleep(2)')
        channel=p.open_endpoint('peer');channel.exchange(b'ping',b'ok',1)
        usage=s.usage();self.assertEqual(usage.endpoint_bytes_tx,4);self.assertEqual(usage.endpoint_bytes_rx,2)
        self.assertEqual(usage.original_state,'READY');channel.close();p.finish()

    def test_64m_streaming_exact_bytes_and_usage(self):
        size=64*1048576;chunk=bytes(range(256))*256
        source=self.root/'large';digest=hashlib.sha256()
        with source.open('xb') as output:
            for _ in range(size//len(chunk)):
                self.assertEqual(output.write(chunk),len(chunk));digest.update(chunk)
        expected=digest.hexdigest();s=self.open(seconds=25)
        r=s.capture(st.SourceRequest(str(source),size,expected));w=s.prepare(r,'copy');usage=s.usage()
        compared=0;actual=hashlib.sha256()
        with source.open('rb') as left,(self.root/'work/copy').open('rb') as right:
            while a:=left.read(65536):
                b=right.read(65536);self.assertEqual(a,b);compared+=len(a);actual.update(b)
            self.assertEqual(right.read(1),b'')
        self.assertEqual(compared,size);self.assertEqual(actual.hexdigest(),expected)
        self.assertEqual(usage.source_io,5*size);self.assertEqual(usage.prepared_bytes,size)
        self.assertEqual(usage.max_chunk,65536);self.assertLess(usage.peak_rss,268435456)
        output=os.environ.get('ENVELOPE_LARGE_RESULTS')
        if output:
            Path(output).write_text(json.dumps(dict(size=size,compared=compared,sha256=expected,
                generator='1024 repetitions of bytes(range(256))*256',usage=dataclasses.asdict(usage)),indent=2)+'\n')

    def test_live_original_and_stopped_history(self):
        s,p=self.launch('import time;time.sleep(1.2)')
        a=s.usage();self.assertEqual(a.charged_operations,1)
        self.assertEqual(a.original_state,'OWNED');self.assertGreaterEqual(a.current_processes,3)
        self.assertEqual(p.verify_current().pid,p.identity().pid)
        p.finish();b=s.usage();self.assertEqual(b.original_state,'STOPPED')
        self.assertIsNone(b.current_original_identity)
        self.assertEqual(b.charged_operations,1)
        with self.assertRaises(st.StartupFailure):s.launch(None)
    def test_no_global_unready_deadline(self):
        now=time.monotonic();self.session=st.open_session(st.NewWorkspace(str(self.root/'work')),
           st.StreamPolicy(),st.ManagedPolicy(readiness_seconds=.05),
           envelope=st.SharedEnvelopePolicy(origin=now,end=now+4))
        s=self.session;python=Path(sys.executable).resolve();tool=s.tool(s.capture(request(python)))
        p=s.launch(st.LaunchSpec(tool,(str(python),'-c','import time;time.sleep(1)' )))
        time.sleep(.12);self.assertGreater(p.verify_current().pid,0);self.assertEqual(s.usage().original_state,'OWNED');p.finish()

if __name__=='__main__':unittest.main()
