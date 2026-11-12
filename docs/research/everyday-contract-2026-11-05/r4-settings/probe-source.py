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
(OUT/"probe-source.py").write_bytes(Path(__file__).read_bytes())
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
  key(q,"shift-f8");wait(q,"Format")
  type_(q,"2");wait(q,"Format: Page")
  capture(q,"01-page-format")
  key(q,"f7")
  key(q,"ctrl-f8")
  capture(q,"02-font")
  key(q,"f7")
  key(q,"shift-f7")
  capture(q,"03-print")
finally:
 guest.stop()
