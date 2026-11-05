#!/usr/bin/env python3
"""Bounded original reference observations for the everyday editing milestone."""
import sys,json,time,hashlib,subprocess,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/"scripts/reference"))
import guest,qmp
from document import prefix
BASE=Path(__file__).resolve().parent
run=sys.argv[1]
OUT=BASE/run
PRIVATE=ROOT/"research/cache/reference"/("everyday-"+run)
RUNTIME=Path("/tmp/wp51-everyday-"+run)
OUT.mkdir(parents=True,exist_ok=False)
qmp.RUNTIME=guest.RUNTIME=RUNTIME
qmp.SOCKET=guest.SOCKET=RUNTIME/"qmp.sock"
trace=[]
def log(data):
 trace.append(data)
 (OUT/"trace.json").write_text(json.dumps(trace,indent=2)+"\n")
def key(q,k):
 log({"key":k})
 q.key(k)
 time.sleep(.25)
def type_(q,s):
 log({"type":s})
 q.type(s)
def capture(q,label,delay=1.5):
 time.sleep(delay)
 screen=q.capture(OUT/label)
 log({"capture":label,"delay_seconds":delay,"screen":screen})
 print(label,repr(screen.splitlines()[-2:]),flush=True)
 return screen
def wait(q,s):
 q.wait_for(s)
 log({"wait":s})
try:
 command=guest.start(PRIVATE)
 (OUT/"environment.json").write_text(json.dumps({"command":command,"profile":json.loads(guest.PROFILE.read_text())},indent=2)+"\n")
 with qmp.QMP() as q:
  capture(q,"01-startup")
  key(q,"alt-equal");wait(q,"File Edit Search")
  type_(q,"l");wait(q,"Justify")
  type_(q,"j");wait(q,"Full")
  capture(q,"02-justify")
  key(q,"f1")
  capture(q,"03-after-f1-immediate",.05)
  capture(q,"04-after-f1-settled",2)
  key(q,"up")
  capture(q,"04b-after-up-focus")
  key(q,"esc")
  capture(q,"05-after-escape")
  key(q,"spc")
  capture(q,"06-after-space")
  if "File Edit Search" in q.text(RUNTIME/"inspect"): key(q,"f7")
  q.wait_absent("File Edit Search")
  # Explicit original visible-menu configuration, and focus behavior.
  key(q,"shift-f1"); wait(q,"Setup")
  type_(q,"2");wait(q,"Setup: Display")
  type_(q,"4");wait(q,"Menu Bar Remains Visible")
  capture(q,"07-menu-options")
  type_(q,"8");wait(q,"No (Yes)")
  type_(q,"y");capture(q,"08-visible-enabled")
  key(q,"f7");wait(q,"File Edit Search")
  capture(q,"09-visible-editor")
  text="A faithful reconstruction needs more than a blue screen. Menus, prompts, wrapping, and cursor movement must work together."
  type_(q,text);wait(q,"work together.")
  capture(q,"10-wrapped")
  key(q,"ret");key(q,"ret")
  type_(q,"Plain ");wait(q,"Plain")
  key(q,"f8");type_(q,"UNDER");wait(q,"UNDER");key(q,"f8")
  type_(q," after");wait(q,"after")
  key(q,"alt-f3");wait(q,"[UND]")
  capture(q,"11-underline-reveal")
  key(q,"alt-f3");q.wait_absent("[UND]")
  key(q,"f10");wait(q,"Document to be saved:")
  type_(q,"C:\\OUT\\EVERY.WP");key(q,"ret");q.wait_absent("Document to be saved:")
  capture(q,"12-saved")
  key(q,"f7");wait(q,"Save document?")
  type_(q,"n");wait(q,"Exit WP?")
  type_(q,"y");wait(q,"C:\\WP51>")
  capture(q,"13-dos")
 guest.stop()
 subprocess.run(["mcopy","-i",str(PRIVATE/"harddisk.img")+"@@1048576","::/OUT/EVERY.WP",str(OUT/"EVERY.WP")],check=True)
 data=(OUT/"EVERY.WP").read_bytes(); info=prefix(data); body=data[info["document_offset"]:]
 result={"native_sha256":hashlib.sha256(data).hexdigest(),"native_size":len(data),**info,"body_hex":body.hex(),"body_ascii_repr":repr(body)}
 (OUT/"native.json").write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps(result,indent=2))
except BaseException as e:
 log({"failure":repr(e)})
 raise
finally:
 guest.stop()
