"""Unchanged production entry, actual decoder and finite external cell observation."""
import errno,fcntl,hashlib,importlib.util,json,os,pty,select,signal,struct,subprocess,sys,termios,time,resource
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('approved_style_observer',ROOT/'internal/tui/evidence/wp52/run_pty.py');prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
class Observer(prior.Styled):
 def roles(self,y):
  return [0x47 if (f,b,k)==(37,41,False) else 0x74 if (f,b,k)==(31,47,False) else 0x71 if (f,b,k)==(34,47,False) else 0 for f,b,k in self.styles[y]]
def execute(binary,out):
 out.mkdir();work=out/'files';work.mkdir();master,slave=pty.openpty();fcntl.ioctl(slave,termios.TIOCSWINSZ,struct.pack('HHHH',25,80,0,0));before=termios.tcgetattr(slave);wire=bytearray();errors=bytearray();sent=[];frames=[];term=Observer();started=time.monotonic();p=None;failure=None;restored=False
 env=dict(os.environ,TERM='xterm-256color',LANG='C.UTF-8',COLORTERM='truecolor');env.pop('NO_COLOR',None)
 argv=[str(binary),'-root',str(work),'-profile','local-flat']
 def collect(seconds=.1):
  until=time.monotonic()+seconds
  while time.monotonic()<until:
   if time.monotonic()-started>30:raise TimeoutError('PTY30s')
   for fd in select.select([master,p.stderr.fileno()],[],[],.01)[0]:
    try:raw=os.read(fd,min(65536,2*1024*1024-len(wire)-len(errors)+1))
    except OSError as e:
     if e.errno==errno.EIO:continue
     raise
    if len(wire)+len(errors)+len(raw)>2*1024*1024:raise ValueError('PTY2MiB overflow refused')
    if fd==master:wire.extend(raw);term.feed(raw)
    else:errors.extend(raw)
 def send(raw,label):
  os.write(master,raw);sent.append(dict(label=label,hex=raw.hex(),wire_before=len(wire)));collect()
 def capture(name):
  assert not term.unknown,term.unknown
  x=dict(name=name,rows=term.rows(),styles=[row[:] for row in term.styles],roles=term.roles(0),cursor=[term.x,term.y],wire_bytes=len(wire));frames.append(x);return x
 try:
  p=subprocess.Popen(argv,cwd=ROOT,stdin=slave,stdout=slave,stderr=subprocess.PIPE,env=env,start_new_session=True);collect(.4);assert 'bounded native editing' in term.text();send(b'\x1b[?31u','synthetic capability response');base=capture('before')
  send(b'\x1b[61;3u','delivered primary61 Alt press');on=capture('on')
  oracle=json.loads((HERE/'original-cells.json').read_text())['results'][0]
  assert on['rows'][0]==oracle['text'] and on['roles']==oracle['roles'],on
  assert on['rows'][1:]==base['rows'][1:] and on['styles'][1:]==base['styles'][1:] and on['cursor']==base['cursor'],'body shifted'
  send(b'\x1b[61;3u','same exact hide');off=capture('off');assert off['rows']==base['rows'] and off['styles']==base['styles'] and off['cursor']==base['cursor']
  # Separate shown-input refusal is observable before any save or macro command.
  send(b'\x1b[61;3u','show again');send(b'\x1b[21;3~','unsupported Macro');shown=capture('unsupported');assert shown['rows'][0]==oracle['text'] and shown['rows'][2].rstrip()=='Menu bar display only; Alt+= hides; action unsupported';send(b'\x1b[61;3u','hide after refusal');assert term.rows()==base['rows']
  send(b'\x1b[18~','F7 exit');send(b'n','No save');send(b'y','Yes exit');p.wait(timeout=2);collect(.1);assert p.returncode==0;assert not list(work.iterdir())
 except Exception as e:failure=repr(e)
 finally:
  if p is not None and p.poll() is None:
   assert os.getpgid(p.pid)==p.pid;os.killpg(p.pid,signal.SIGTERM)
   try:p.wait(timeout=1)
   except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=1)
  restored=termios.tcgetattr(slave)==before
  (out/'wire.bin').write_bytes(wire);(out/'stderr.raw').write_bytes(errors);(out/'sent.json').write_text(json.dumps(sent,indent=2)+'\n');(out/'frames.json').write_text(json.dumps(frames,indent=2)+'\n');(out/'result.json').write_text(json.dumps(dict(failure=failure,argv=argv,cwd=str(ROOT),environment={k:env.get(k) for k in ['TERM','LANG','COLORTERM','NO_COLOR']},returncode=p.returncode if p else None,termios_restored=restored,elapsed=time.monotonic()-started,bytes=len(wire)+len(errors),empty_disposable_directory=not list(work.iterdir()),maxrss_children=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,own_fds=len(os.listdir('/proc/self/fd')),owned_processes=1),indent=2)+'\n');os.close(master);os.close(slave)
  if p:p.stderr.close()
 if failure or not restored:raise AssertionError(failure or 'terminal not restored')
 return dict(case=out.name,bytes=len(wire),elapsed=time.monotonic()-started)
if __name__=='__main__':
 build=json.loads((HERE/'build-source.json').read_text());binary=Path(sys.argv[1]) if len(sys.argv)>1 else Path(build['binary']);out=Path(sys.argv[2]) if len(sys.argv)>2 else HERE/'pty-01';out=out.resolve();out.mkdir();results=[execute(binary,out/('r'+str(n)))for n in [1,2]];(out/'results.json').write_text(json.dumps(results,indent=2)+'\n');print(results)
