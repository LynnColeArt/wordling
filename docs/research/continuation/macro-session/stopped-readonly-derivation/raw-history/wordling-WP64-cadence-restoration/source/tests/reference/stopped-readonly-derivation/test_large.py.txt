"""Lawful64MiB opaque input -> tiny deterministic helper output, bounded IO."""
import dataclasses
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest
import test_derivation as public
st=public.st
class LargeTests(unittest.TestCase):
 def test_64m_input_actual_seal_helper_and_bounded_output(self):
  with tempfile.TemporaryDirectory(prefix='derive-large-TEST-') as temporary:
   root=Path(temporary);path=root/'source';chunk=bytes(range(256))*256;digest=hashlib.sha256()
   with path.open('xb') as output:
    for _ in range(1024):self.assertEqual(output.write(chunk),65536);digest.update(chunk)
   expected=digest.hexdigest();now=time.monotonic()
   s=st.open_session(st.NewWorkspace(str(root/'work')),st.StreamPolicy(),st.ManagedPolicy(),envelope=st.SharedEnvelopePolicy(origin=now,end=now+28))
   try:
    working=s.prepare(s.capture(st.SourceRequest(str(path),67108864,expected)),'working')
    actual=hashlib.sha256();compared=0
    with path.open('rb') as a,(root/'work/working').open('rb') as b:
     while left:=a.read(65536):
      right=b.read(65536);self.assertEqual(left,right);actual.update(right);compared+=len(right)
     self.assertEqual(b.read(1),b'')
    self.assertEqual(actual.hexdigest(),expected)
    python=Path(sys.executable).resolve();tool=s.tool(s.capture(public.request(python)))
    p=s.launch(st.LaunchSpec(tool,(str(python),'-c','import time;time.sleep(.2)')),resources=(working,));p.finish()
    sealed=s.seal_stopped(s.snapshot(working).successor)
    body='import hashlib,pathlib,sys,time;time.sleep(.15);h=hashlib.sha256()\nwith open(sys.argv[1],"rb") as f:\n while b:=f.read(65536):h.update(b)\npathlib.Path(sys.argv[2]).write_text(h.hexdigest());time.sleep(.1)'
    batch=s.derive_readonly((sealed,),st.DerivationSpec(tool,(str(python),'-c',body,st.ResourceArgument('',sealed,''),st.OutputArgument(0)),(st.OutputSpec('digest',64),),budget=st.JobBudget(seconds=15)))
    c=s.read_chunk(batch.artifacts[0],0,16384);self.assertTrue(c.eof);self.assertEqual(c.data,expected.encode());usage=s.usage()
    output=os.environ.get('DERIVATION_LARGE_RESULTS')
    if output:Path(output).write_text(json.dumps(dict(input_bytes=67108864,compared=compared,input_sha256=expected,output_bytes=len(c.data),usage=dataclasses.asdict(usage),helper_exit=dataclasses.asdict(batch.helper_exit)),indent=2)+'\n')
   finally:s.close()
if __name__=='__main__':unittest.main()
