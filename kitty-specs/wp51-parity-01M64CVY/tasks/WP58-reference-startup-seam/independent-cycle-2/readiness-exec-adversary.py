"""Actual public readiness peer exec changes argv during wait, no component monkeypatch."""
from pathlib import Path
import dataclasses,hashlib,importlib.util,json,sys,tempfile
P=Path(__file__).resolve().parent;S=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-p/scripts/reference/startup_transport.py');sp=importlib.util.spec_from_file_location('wp58_review_exec2',S);st=importlib.util.module_from_spec(sp);sys.modules[sp.name]=st;sp.loader.exec_module(st)
main="""import os,socket,time,sys,json
from pathlib import Path
s=socket.socket(socket.AF_UNIX);s.bind('endpoint');s.listen(1);c,_=s.accept();assert c.recv(64)==b'TEST ping\\n'
time.sleep(.15)
fd=c.fileno();os.set_inheritable(fd,True)
Path('before-exec.json').write_text(json.dumps(dict(pid=os.getpid(),argv=sys.argv)))
os.execv(sys.executable,[sys.executable,'-B',str(Path('after.py').absolute()),str(fd),sys.argv[1]])
"""
after="""import os,sys,time,json
from pathlib import Path
Path('after-exec.json').write_text(json.dumps(dict(pid=os.getpid(),argv=sys.argv,cmdline=Path('/proc/self/cmdline').read_bytes().hex())))
os.write(int(sys.argv[1]),b'ABCDEFGHIJKLMNOPQRST')
time.sleep(float(sys.argv[2]))
"""
rows=[]
for delay in [.3,0,0]:
 with tempfile.TemporaryDirectory(prefix='wp58-review-exec-',dir='/tmp/wordling-WP58-cycle2-disposables')as td:
  r=Path(td);a=r/'main.py';b=r/'after.py';a.write_text(main);b.write_text(after);tool=st.ArtifactSpec.capture(Path(sys.executable).resolve());command=st.CommandSpec(tool,(tool.path,'-B',str(a),str(delay)),str(r),sources=(st.ArtifactSpec.capture(a),st.ArtifactSpec.capture(b)))
  with st.Attempt(r,st.Limits(seconds=2))as attempt:
   try:result=attempt.run(command,readiness=st.EndpointSpec(str(r/'endpoint'),reply=b'ABCDEFGHIJKLMNOPQRST'));outcome='returned-success';error=None
   except st.Failure as e:result=e.result;outcome='refused';error=e.code
   rows.append(dict(delay_after_reply=delay,outcome=outcome,error=error,result=dataclasses.asdict(result)if result else None,journal=attempt.journal,command_argv=command.argv,before_exec=json.loads((r/'before-exec.json').read_text())if(r/'before-exec.json').exists()else None,after_exec=json.loads((r/'after-exec.json').read_text())if(r/'after-exec.json').exists()else None))
(P/'readiness-exec-adversary.json').write_text(json.dumps(dict(provider_sha256=hashlib.sha256(S.read_bytes()).hexdigest(),fixture_main=main,fixture_after=after,observations=rows),indent=2,default=lambda b:b.hex()if isinstance(b,bytes)else str(b))+'\n');print(json.dumps([dict(delay=x['delay_after_reply'],outcome=x['outcome'],error=x['error'],ready=x['result']['ready']if x['result']else None,before_pid=x['before_exec']['pid']if x['before_exec']else None,after_pid=x['after_exec']['pid']if x['after_exec']else None)for x in rows],indent=2))
