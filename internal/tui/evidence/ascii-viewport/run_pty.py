#!/usr/bin/env python3
"""Owned long-ASCII public CLI transport; no product telemetry/cursor setter."""
import sys
sys.dont_write_bytecode=True
import os,errno,select,time,json,hashlib,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
spec=importlib.util.spec_from_file_location('approved69transport',ROOT/'internal/tui/evidence/reveal-anchors/run_pty.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
sha=lambda b:hashlib.sha256(b).hexdigest()
class Run(base.Run):
 def __init__(self,binary,folder,body):
  super().__init__(binary,folder);self.body=body;self.events=0
  os.set_blocking(self.master,False)
 def send(self,raw,label,delay=.035):
  sent=0;origin=time.monotonic()
  while sent<len(raw):
   if time.monotonic()>=self.end:raise TimeoutError('PTY30s write deadline')
   try:n=os.write(self.master,raw[sent:]);sent+=n
   except BlockingIOError:self.collect(.005)
  self.sent.append({'label':label,'hex':raw.hex(),'bytes_written':sent,'monotonic':origin,'wire_before':len(self.wire)})
  self.collect(delay)
 def matches(self,g,codes):
  t=self.terminal;rows=t.rows();start=max(0,g-40);text=self.body[start:min(start+80,len(self.body))].decode('ascii');want=text.ljust(80)
  if rows[0]!=want or [t.x,t.y]!=[g-start,0]:return False
  if codes:
   low=(text+(' ' if g==len(self.body) else '')).ljust(80)
   return rows[13]==low and [i for i,r in enumerate(t.roles(13)) if r==71]==[g-start] and rows[24]=='Press Reveal Codes to restore screen'+' '*44 and list(t.roles(24))==[23]*6+[31]*12+[23]*62
  return rows[13]==' '*80 and rows[24]==' '*80
 def capture(self,g,codes=True):
  # Real cells/roles/caret establish delivery, rather than input byte count.
  end=min(self.end,time.monotonic()+2)
  while not self.matches(g,codes) and time.monotonic()<end:self.collect(.005)
  t=self.terminal;record={'gap':g,'codes':codes,'rows':t.rows(),'lower_roles':list(t.roles(13)),'footer_roles':list(t.roles(24)),'cursor':[t.x,t.y],'wire_bytes':len(self.wire),'monotonic':time.monotonic()}
  self.witnesses.append(record)
  assert not t.unknown,t.unknown
  assert self.matches(g,codes),record
 def move(self,a,b):
  n=abs(b-a);self.events+=n
  if self.events>40000:raise ValueError('explicit event bound')
  self.send((b'\x1b[C' if b>a else b'\x1b[D')*n,f'{n} ordinary '+('Right' if b>a else 'Left'),.04)
  self.capture(b)
def main():
 binary=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir();results=[]
 prefix=(ROOT/'docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5').read_bytes();at=int.from_bytes(prefix[4:8],'little')
 for num,n in enumerate([4097,16384]):
  body=bytes(33+(i*37+i//89+i//7919+num*17)%94 for i in range(n));raw=prefix[:at]+body
  folder=out/f'r{num+1}';folder.mkdir();p=Run(binary,folder,body);(p.work/'ORIGIN').write_bytes(raw);error=None
  try:
   p.launch();p.retrieve();p.send(b'\x1b[13;3~','AltF3 on');p.capture(0)
   checkpoints=sorted(set([0,4095,4096,4097,n//2,n]))
   g=0
   for target in checkpoints[1:]:
    p.move(g,target);g=target
    p.send(b'\x1b[13;3~','AltF3 off');p.capture(g,False);p.send(b'\x1b[13;3~','AltF3 on');p.capture(g)
   for target in checkpoints[-2::-1]:p.move(g,target);g=target
   p.send(b'\x1b[21~','F10 Save As');p.send(b'COPY','absent name');p.send(b'\r','actual publication',.1)
   end=min(p.end,time.monotonic()+2)
   while not (p.work/'COPY').exists() and time.monotonic()<end:p.collect(.01)
   assert (p.work/'COPY').read_bytes()==raw,'COPY native bytes differ'
   assert (p.work/'ORIGIN').read_bytes()==raw,'ORIGIN changed'
   p.send(b'\x1b[18~','F7');p.send(b'n','No');p.send(b'y','Yes exit',.08);p.proc.wait(timeout=min(1,max(.001,p.end-time.monotonic())));assert p.proc.returncode==0
  except Exception as e:error=repr(e)
  finally:
   cleanup=p.close();record={'failure':error,'cleanup':cleanup,'n':n,'events':p.events,'argv':p.argv,'binary_sha256':sha(binary.read_bytes()),'source_sha256':sha(raw),'COPY_sha256':sha((p.work/'COPY').read_bytes()) if (p.work/'COPY').exists() else None,'env':{k:p.env.get(k) for k in ['TERM','LANG','COLORTERM','NO_COLOR']},'witnesses':p.witnesses};(folder/'result.json').write_text(json.dumps(record,indent=2)+'\n');results.append(record)
  if error or not cleanup['termios_restored']:break
 (out/'results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps({'completed':len(results),'failures':[r['failure'] for r in results],'cleanup':[r['cleanup'] for r in results]}))
 return 0 if len(results)==2 and all(r['failure'] is None and r['cleanup']['termios_restored'] for r in results) else 1
if __name__=='__main__':raise SystemExit(main())
