import os
"""Independent PUBLIC API adversary: same-session process budget during progress-making readiness."""
from pathlib import Path
import dataclasses,hashlib,importlib.util,json,os,sys,tempfile,time
SOURCE=Path(os.environ['WP58_REVIEW_PROVIDER']);spec=importlib.util.spec_from_file_location('wp58_review_transport',SOURCE);st=importlib.util.module_from_spec(spec);sys.modules[spec.name]=st;spec.loader.exec_module(st)
OUT=Path(os.environ['WP58_REVIEW_OUTPUT'])
body="""import os,time,json,socket,sys
from pathlib import Path
mode=sys.argv[1]
if mode=='readiness':
 s=socket.socket(socket.AF_UNIX);s.bind('endpoint');s.listen(1);c,_=s.accept();assert c.recv(64)==b'TEST ping\\n'
children=[]
for i in range(2):
 p=os.fork()
 if p==0: time.sleep(.55);os._exit(0)
 children.append(p)
Path('observed-children.json').write_text(json.dumps(dict(parent=os.getpid(),session=os.getsid(0),children=children,child_sessions=[os.getsid(p)for p in children],started=time.monotonic())))
if mode=='readiness':
 for i,b in enumerate(b'ABCDEFGHIJKLMNOPQRST'):
  if i==16:
   for p in children:os.waitpid(p,0)
   Path('children-reaped').write_text('yes')
  c.sendall(bytes([b]));time.sleep(.04)
 c.close();s.close()
else:time.sleep(.8)
if mode!='readiness':
 for p in children:os.waitpid(p,0)
 Path('children-reaped').write_text('yes')
"""
rows=[]
for mode in ['control','readiness','readiness']:
 with tempfile.TemporaryDirectory(prefix='wp58-review-ready-',dir='/tmp/wordling-WP58-review-disposables')as td:
  root=Path(td);f=root/'fixture.py';f.write_text(body);tool=st.ArtifactSpec.capture(Path(sys.executable).resolve());source=st.ArtifactSpec.capture(f);cmd=st.CommandSpec(tool,(tool.path,'-B',str(f),mode),str(root),sources=(source,));started=time.monotonic()
  with st.Attempt(root,st.Limits(seconds=2,processes=2))as attempt:
   try:
    result=attempt.run(cmd,readiness=st.EndpointSpec(str(root/'endpoint'),reply=b'ABCDEFGHIJKLMNOPQRST')if mode=='readiness'else None);outcome='returned-success';error=None
   except st.Failure as e:result=e.result;outcome='refused';error=e.code
   record=dict(mode=mode,outcome=outcome,error=error,result=dataclasses.asdict(result)if result else None,journal=attempt.journal,elapsed=time.monotonic()-started,observed_children=json.loads((root/'observed-children.json').read_text())if(root/'observed-children.json').exists()else None,children_reaped=(root/'children-reaped').exists(),argv=cmd.argv,cwd=td,limits=dataclasses.asdict(attempt.limits),source_sha256=hashlib.sha256(f.read_bytes()).hexdigest())
   if record['observed_children']:
    record['all_child_proc_absent_or_zombie']=all(not Path('/proc',str(p)).exists()or Path('/proc',str(p),'stat').read_text().rsplit(')',1)[1].split()[0]=='Z'for p in record['observed_children']['children'])
   rows.append(record)
(OUT/'readiness-adversary-v2.json').write_text(json.dumps(dict(transport_source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),fixture_source=body,observations=rows),indent=2,default=lambda b:b.hex()if isinstance(b,bytes)else str(b))+'\n');print(json.dumps([dict(mode=x['mode'],outcome=x['outcome'],error=x['error'],reported_peak=x['result']['peak_processes']if x['result']else None,ready=x['result']['ready']if x['result']else None,children_reaped=x['children_reaped'],observed_children=x['observed_children'])for x in rows],indent=2))
