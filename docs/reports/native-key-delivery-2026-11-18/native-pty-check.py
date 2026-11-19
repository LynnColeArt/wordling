import fcntl,gzip,hashlib,json,os,pty,select,signal,struct,subprocess,tempfile,termios,time
from pathlib import Path
ROOT=Path(__file__).parent
APP=ROOT/'wordling'
assert hashlib.sha256(APP.read_bytes()).hexdigest()=='4789d95f166a42f2bffa6565919143f21d272c81e0446e58fb5d762eae48ce1f'
OUT=ROOT/'native-pty-check';OUT.mkdir(mode=0o700)
CASES=[('F5',b'\x1b[15~',b'Dir ',False,False),('F10',b'\x1b[21~',b'Document to be saved:',False,False),('CtrlF1',b'\x1b[1;5P',b'Save document 1 before opening shell?',False,True),('CtrlS-convenience',b'\x13',b'Document to be saved:',True,False)]
results=[]
for name,keys,witness,controls,dirty in CASES:
 work=OUT/name;work.mkdir(mode=0o700)
 master,slave=pty.openpty();fcntl.ioctl(slave,termios.TIOCSWINSZ,struct.pack('HHHH',24,80,0,0))
 def setup():
  os.setsid();fcntl.ioctl(0,termios.TIOCSCTTY,0)
 env=dict(os.environ,TERM='xterm-256color');env.pop('TEA_TRACE',None)
 argv=[str(APP),'-root',str(work),'-profile','macro-cout']+(['-control-keys']if controls else[])
 raw=bytearray();started=time.monotonic();proc=None;record={'name':name,'argv':argv,'key_hex':keys.hex(),'witness':witness.decode(),'physical_keyboard':False}
 def read_until(expected,start,seconds):
  end=time.monotonic()+seconds
  while time.monotonic()<end and len(raw)<1048576:
   if expected in raw[start:]:return True
   if select.select([master],[],[],0.05)[0]:
    try:chunk=os.read(master,min(65536,1048576-len(raw)))
    except OSError:break
    if not chunk:break
    raw.extend(chunk)
  return expected in raw[start:]
 try:
  proc=subprocess.Popen(argv,stdin=slave,stdout=slave,stderr=slave,cwd=work,env=env,preexec_fn=setup)
  os.close(slave);slave=None
  record['startup']=read_until(b'Doc 1 Pg',0,3)
  if record['startup']:
   time.sleep(0.2)
   if dirty:
    mark=len(raw);os.write(master,b'KEEP');record['dirty_setup']=read_until(b'KEEP',mark,2)
   mark=len(raw);os.write(master,keys);record['witness_seen']=read_until(witness,mark,3)
  else:record['witness_seen']=False
 except Exception as e:record['exception']=type(e).__name__+':'+str(e)
 finally:
  if proc is not None:
   proc.send_signal(signal.SIGTERM)
   try:proc.wait(timeout=2)
   except subprocess.TimeoutExpired:proc.kill();proc.wait(timeout=2)
   record['process_exit_after_cleanup']=proc.returncode
  if slave is not None:os.close(slave)
  os.close(master)
 record.update(raw_bytes=len(raw),raw_sha256=hashlib.sha256(raw).hexdigest(),elapsed_seconds=time.monotonic()-started)
 with (OUT/(name+'.raw.gz')).open('xb')as f:f.write(gzip.compress(bytes(raw),mtime=0))
 results.append(record)
summary={'candidate':'f6cea1cc62dfc89b49cde1f076aaf52751e2a3b9','status':'NATIVE_PTY_BYTE_DELIVERY_ONLY_NOT_PHYSICAL_ACCEPTANCE','results':results}
(OUT/'results.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
