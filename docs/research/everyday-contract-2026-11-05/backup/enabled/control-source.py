#!/usr/bin/env python3
import sys,json,time,subprocess,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/"scripts/reference"))
import guest,qmp
BASE=Path(__file__).resolve().parent
run,action=sys.argv[1:3]
value=sys.argv[3] if len(sys.argv)>3 else ""
OUT=BASE/run
PRIVATE=ROOT/"research/cache/reference"/("everyday-backup-"+run)
RUNTIME=Path("/tmp/wp51-backup-"+run)
qmp.RUNTIME=guest.RUNTIME=RUNTIME
qmp.SOCKET=guest.SOCKET=RUNTIME/"qmp.sock"
def type_text(q,text):
 for part_i,part in enumerate(text.split("!")):
  if part_i:q.key("shift-1")
  q.type(part)
record={"action":action,"value":value}
try:
 if action=="start":
  OUT.mkdir(parents=True,exist_ok=False)
  (OUT/"control-source.py").write_bytes(Path(__file__).read_bytes())
  record["command"]=guest.start(PRIVATE)
  (OUT/"environment.json").write_text(json.dumps(json.loads(guest.PROFILE.read_text()),indent=2)+"\n")
 elif action=="stop":guest.stop()
 elif action=="export":
  if qmp.SOCKET.exists():raise RuntimeError("Cannot export from running guest")
  image=str(PRIVATE/"harddisk.img")+"@@1048576"
  result=subprocess.run(["mdir","-i",image,"::/OUT/"],capture_output=True,text=True,check=True)
  (OUT/"directory.txt").write_text(result.stdout)
  exports=OUT/"exports";exports.mkdir(exist_ok=True)
  subprocess.run(["mcopy","-i",image,"::/OUT/*",str(exports)],check=True)
  from document import prefix
  files=[]
  for f in sorted(exports.iterdir()):
   data=f.read_bytes();info=prefix(data)
   files.append({"name":f.name,"size":len(data),"sha256":hashlib.sha256(data).hexdigest(),"body_hex":data[info["document_offset"]:].hex(),"body_repr":repr(data[info["document_offset"]:])})
  (OUT/"files.json").write_text(json.dumps(files,indent=2)+"\n")
  print(result.stdout);print(json.dumps(files,indent=2))
 else:
  with qmp.QMP() as q:
   if action=="key":
    for k in value.split(","):q.key(k);time.sleep(.25)
   elif action=="type":type_text(q,value)
   elif action=="wait":q.wait_for(value)
   elif action=="absent":q.wait_absent(value)
   elif action=="capture":
    time.sleep(1.5);print(q.capture(OUT/value))
   elif action=="text":print(q.text(RUNTIME/"inspect"))
   elif action=="dos":
    q.key("ctrl-f1");q.wait_for("DOS Command")
    q.key("2");q.wait_for("DOS Command:")
    type_text(q,value);q.key("ret");q.wait_for("Press any key")
    time.sleep(.5)
    label="dos-"+str(len(list(OUT.glob("dos-*")))+1).zfill(2)
    print(q.capture(OUT/label));record["capture"]=label
    q.key("spc");q.wait_absent("Press any key")
   else:raise ValueError(action)
 record["outcome"]="completed"
except BaseException as e:
 record["outcome"]="failed";record["error"]=repr(e);raise
finally:
 OUT.mkdir(parents=True,exist_ok=True)
 with (OUT/"trace.jsonl").open("a") as f:f.write(json.dumps(record)+"\n")
