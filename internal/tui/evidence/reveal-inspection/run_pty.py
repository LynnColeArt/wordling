#!/usr/bin/env python3
"""Real unchanged cmd/wordling; paired original-authored INPUTS, zero original guests."""
import fcntl,hashlib,importlib.util,json,os,signal,struct,subprocess,sys,termios,time,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('approved52_style_observer',ROOT/'internal/tui/evidence/wp52/run_pty.py');prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
sha=lambda b:hashlib.sha256(b).hexdigest()
class Observer(prior.Styled):
 def __init__(self):super().__init__();self.cursor_visible=None
 def csi(self,body,final):
  if body=='?25'and final in 'hl':self.cursor_visible=final=='h'
  super().csi(body,final)
class Process(prior.old.PTY):
 def __init__(self,binary,folder):
  super().__init__(binary,folder,{'profile':'local-flat'});self.started=time.monotonic();self.env.pop('NO_COLOR',None);self.env['COLORTERM']='truecolor';self.terminal=Observer();self.error_file=open(folder/'stderr.raw','w+b');fcntl.ioctl(self.slave,termios.TIOCSWINSZ,struct.pack('HHHH',25,80,0,0))
 def launch(self):
  self.proc=subprocess.Popen(self.argv,stdin=self.slave,stdout=self.slave,stderr=self.error_file,env=self.env,start_new_session=True)
  self.collect(.3);self.cue('bounded native editing');self.send(b'\x1b[?31u','synthetic keyboard enhancement response')
 def collect(self,seconds=.035):
  if time.monotonic()-self.started>10:raise TimeoutError('bounded hostPTY10s')
  if self.error_file.tell()>65536:raise ValueError('bounded stderr64KiB')
  super().collect(seconds)
 def finish(self):
  if self.proc is not None and self.proc.poll()is None:
   # Only our child-created session; containment is never a normal exit proof.
   assert os.getpgid(self.proc.pid)==self.proc.pid
   os.killpg(self.proc.pid,signal.SIGTERM)
   try:self.proc.wait(timeout=2)
   except subprocess.TimeoutExpired:os.killpg(self.proc.pid,signal.SIGKILL);self.proc.wait(timeout=2)
  self.collect(.02);restored=termios.tcgetattr(self.slave)==self.before
  (self.folder/'wire.bin').write_bytes(self.wire);(self.folder/'sent.json').write_text(json.dumps(self.sent,indent=2)+'\n');self.error_file.close();os.close(self.master);os.close(self.slave);return restored

def main():
 build=json.loads((HERE/'build-source.json').read_text());binary=Path(build['binary']);assert sha(binary.read_bytes())==build['binary_digest']['sha256'];out=HERE/'pty-03';out.mkdir();results=[]
 for family,label in [('L1-HR','[HRt]'),('L2-HP','[HPg]'),('L4-ABS',None),('L4-REL',None)]:
  for rep in [1,2]:
   folder=out/f'{family}-r{rep}';folder.mkdir();p=Process(binary,folder);src=ROOT/f'docs/research/continuation/text-layout/runs/wp14-r{rep:02d}-{family}/BASEA.WP5';raw=src.read_bytes();(p.work/'ORIGIN').write_bytes(raw);native_stat=lambda:{k:getattr((p.work/'ORIGIN').stat(),k)for k in ['st_dev','st_ino','st_mode','st_size','st_mtime_ns']};before_stat=native_stat();witness=[];error=None;normal_exit=False
   def capture(name,partial):
    rows=p.terminal.rows();roles=p.terminal.roles(3);record=dict(name=name,rows=rows,roles=roles,cursor_visible=p.terminal.cursor_visible,unknown_controls=p.terminal.unknown,wire_bytes=len(p.wire))
    assert not p.terminal.unknown,record
    assert 'Unsupported document presentation:'in rows[1],record
    if partial:
     assert 'Partial Reveal inspection | HOST'in rows[2]and '?0'in rows[3],record
     assert 0x47 not in roles,record
     if label:
      at=rows[3].find(label);assert at>=0 and at+5<=80,record;assert roles[at:at+5]==[0x1f]*5,record
     else:assert '[Tab]'not in rows[3],record
    assert p.terminal.cursor_visible is False,record
    assert (p.work/'ORIGIN').read_bytes()==raw and native_stat()==before_stat
    witness.append(record)
   try:
    p.launch();p.retrieve();p.send(b'\x1b[13;3~','AltF3 actual production input');capture('on',True)
    p.send(b'\x1b[13;3~','AltF3 off');capture('off',False)
    p.send(b'\x1b[13;3~','AltF3 on');capture('on-again',True)
    # No edit/Save/movement is needed or claimed. Existing F7 normal clean exit.
    p.exit();normal_exit=p.proc.returncode==0;assert normal_exit
   except Exception as e:error=repr(e)
   finally:
    restored=p.finish();record=dict(case=f'{family}-r{rep}',failure=error,normal_exit=normal_exit,termios_restored=restored,argv=p.argv,cwd=str(ROOT),source=str(src.relative_to(ROOT)),native_sha256=sha(raw),native_stat_before=before_stat,native_stat_after=native_stat(),binary_sha256=sha(binary.read_bytes()),wire_sha256=sha(bytes(p.wire)),witnesses=witness,scope='observable80colHOSTinspection only; no private Model state/physical/original geometry authority');(folder/'result.json').write_text(json.dumps(record,indent=2)+'\n');results.append(record)
   if error or not restored:raise AssertionError(error or 'terminal not restored')
 suite=ET.Element('testsuite',name='actual-production-partial-Reveal-PTY',tests=str(len(results)),failures='0',skipped='0')
 for r in results:ET.SubElement(suite,'testcase',name=r['case'])
 ET.ElementTree(suite).write(HERE/'pty.xml');(HERE/'pty-results.json').write_text(json.dumps(dict(processes=len(results),original_guests=0,results=results),indent=2)+'\n');print(json.dumps(dict(processes=len(results),witnesses=sum(len(r['witnesses'])for r in results),failures=0)))
if __name__=='__main__':main()
