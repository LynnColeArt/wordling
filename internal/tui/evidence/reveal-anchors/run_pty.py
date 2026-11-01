#!/usr/bin/env python3
"""Bounded real production CLI PTYs; observer-only imports of approved VT reader."""
import errno, fcntl, hashlib, importlib.util, json, os, select, signal, struct, subprocess, sys, termios, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('approved_style_observer',ROOT/'internal/tui/evidence/wp52/run_pty.py')
observer=importlib.util.module_from_spec(spec);spec.loader.exec_module(observer)
sha=lambda b:hashlib.sha256(b).hexdigest()
class Run(observer.old.PTY):
 def __init__(self,binary,folder):
  super().__init__(binary,folder,{'profile':'local-flat'})
  self.origin=time.monotonic();self.end=self.origin+30;self.terminal=observer.Styled();self.stderr=bytearray();self.witnesses=[]
  fcntl.ioctl(self.slave,termios.TIOCSWINSZ,struct.pack('HHHH',25,80,0,0))
  self.env.pop('NO_COLOR',None);self.env['COLORTERM']='truecolor'
 def collect(self,seconds=.04):
  if time.monotonic()>=self.end:raise TimeoutError('30s owned PTY limit')
  end=min(time.monotonic()+seconds,self.end)
  while time.monotonic()<end:
   descriptors=[self.master]
   if self.proc is not None:descriptors.append(self.proc.stderr.fileno())
   for fd in select.select(descriptors,[],[],min(.005,max(0,end-time.monotonic())))[0]:
    try:raw=os.read(fd,65536)
    except OSError as e:
     if e.errno!=errno.EIO:raise
     continue
    if len(self.wire)+len(self.stderr)+len(raw)>2*1024*1024:raise ValueError('2MiB live combined output cap before append')
    if fd==self.master:self.wire.extend(raw);self.terminal.feed(raw)
    else:self.stderr.extend(raw)
 def launch(self):
  self.proc=subprocess.Popen(self.argv,stdin=self.slave,stdout=self.slave,stderr=subprocess.PIPE,env=self.env,start_new_session=True)
  self.collect(.25);self.send(b'\x1b[?31u','keyboard protocol response')
 def retrieve(self):
  self.send(b'\x1b[21;2~','ShiftF10 Retrieve');self.send(b'ORIGIN','native source basename');self.send(b'\r','Retrieve Enter',.10)
 def capture(self,g,view='codes'):
  t=self.terminal;assert not t.unknown,t.unknown
  rows=t.rows();record={'gap':g,'view':view,'wire_bytes':len(self.wire),'rows':list(rows),'upper_roles':list(t.roles(0)),'lower_roles':list(t.roles(13)),'footer_roles':list(t.roles(24)),'cursor':[t.x,t.y]}
  assert rows[0][:4]=='ABCD' and rows[0][4:]==' '*76,record
  assert [t.x,t.y]==[[0,0],[1,0],[1,0],[2,0],[3,0],[3,0],[4,0]][g],record
  if view=='codes':
   assert rows[24]=='Press Reveal Codes to restore screen'+' '*44,record
   assert record['footer_roles']==[23]*6+[31]*12+[23]*62,record
   want=[[0],list(range(1,7)),[7],[8],list(range(9,15)),[15],[16]][g]
   assert [i for i,r in enumerate(record['lower_roles']) if r==71]==want,record
   for rep in [1,2]:
    v=(ROOT/f'docs/research/continuation/session1/runs/2026-10-31-session1-b01-r{rep}/CMD51-049/codes-gap-{g}/vram.bin').read_bytes()
    for x in range(17 if g==6 else 16):assert v[13*160+2*x]==ord(rows[13][x]) and v[13*160+2*x+1]==record['lower_roles'][x],(rep,g,x)
  else:assert rows[13]==' '*80 and rows[24]==' '*80,record
  self.witnesses.append(record)
 def close(self):
  containment=[]
  if self.proc is not None:
   if self.proc.poll() is None:
    os.killpg(self.proc.pid,signal.SIGTERM);containment.append('owned group TERM')
    try:self.proc.wait(timeout=1)
    except subprocess.TimeoutExpired:os.killpg(self.proc.pid,signal.SIGKILL);containment.append('owned group KILL');self.proc.wait(timeout=1)
   # Drain only the retained owned endpoints after actual wait/reap.
   try:self.collect(.01)
   except TimeoutError:containment.append('post-limit drain refused; retained capture partial')
   self.proc.stderr.close()
  restored=termios.tcgetattr(self.slave)==self.before
  (self.folder/'wire.bin').write_bytes(self.wire);(self.folder/'stderr.raw').write_bytes(self.stderr)
  (self.folder/'sent.json').write_text(json.dumps(self.sent,indent=2)+'\n')
  os.close(self.master);os.close(self.slave)
  return {'termios_restored':restored,'returncode':None if self.proc is None else self.proc.returncode,'direct_child_reaped':self.proc is not None and self.proc.returncode is not None,'owned_cleanup':containment,'descriptors_closed':True,'elapsed':time.monotonic()-self.origin}

def main():
 binary=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir();results=[]
 raw=(ROOT/'docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5').read_bytes()
 for rep in [1,2]:
  folder=out/f'r{rep}';folder.mkdir();p=Run(binary,folder);(p.work/'ORIGIN').write_bytes(raw);error=None
  try:
   p.launch();p.retrieve();p.send(b'\x1b[13;3~','AltF3');p.capture(0)
   for g in range(1,7):p.send(b'\x1b[C','Right');p.capture(g)
   for g in range(5,-1,-1):p.send(b'\x1b[D','Left');p.capture(g)
   p.send(b'\x1b[13;3~','AltF3 off');p.capture(0,'normal');p.send(b'\x1b[13;3~','AltF3 on');p.capture(0)
   p.send(b'\x1b[21~','F10 Save As');p.send(b'COPY','absent destination');p.send(b'\r','publish candidate',.12)
   assert (p.work/'COPY').read_bytes()==raw,'full native no-edit readback differs'
   assert (p.work/'ORIGIN').read_bytes()==raw
   p.send(b'\x1b[18~','F7');p.send(b'n','No save');p.send(b'y','Yes exit',.10);p.proc.wait(timeout=min(1,max(.001,p.end-time.monotonic())))
   assert p.proc.returncode==0
  except Exception as e:error=repr(e)
  finally:
   cleanup=p.close();result={'failure':error,'argv':p.argv,'binary_sha256':sha(binary.read_bytes()),'nonsecret_env':{k:p.env.get(k) for k in ['TERM','LANG','COLORTERM','NO_COLOR']},'source_sha256':sha(raw),'cleanup':cleanup,'witnesses':p.witnesses,'scope':'actual unmodified production CLI synthetic Linux PTY; no physical/raster or fullframe parity','COPY_sha256':sha((p.work/'COPY').read_bytes()) if (p.work/'COPY').exists() else None};(folder/'result.json').write_text(json.dumps(result,indent=2)+'\n');results.append(result)
  if error or not cleanup['termios_restored']:break
 (out/'results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps({'completed':len(results),'failures':sum(r['failure'] is not None or not r['cleanup']['termios_restored'] for r in results)}))
 return 0 if len(results)==2 and all(r['failure'] is None and r['cleanup']['termios_restored'] for r in results) else 1
if __name__=='__main__':raise SystemExit(main())
