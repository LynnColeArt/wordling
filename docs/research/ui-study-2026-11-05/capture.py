#!/usr/bin/env python3
"""Capture an independent, fingerprint-checked WP 5.1 reference VM session."""
import sys, json, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/"scripts/reference"))
import qmp, guest
OUT=Path(__file__).resolve().parent
PRIVATE=ROOT/"research/cache/reference/ui-study-2026-11-05"
RUNTIME=Path("/tmp/wordling-ui-study-20261105")
qmp.RUNTIME=guest.RUNTIME=RUNTIME
qmp.SOCKET=guest.SOCKET=RUNTIME/"qmp.sock"
action=sys.argv[1]
value=sys.argv[2] if len(sys.argv)>2 else ""
record={"action":action,"value":value}
try:
    if action=="start":
        record["command"]=guest.start(PRIVATE)
        record["profile"]=json.loads(guest.PROFILE.read_text())
    elif action=="stop":
        guest.stop()
    else:
        with qmp.QMP() as q:
            if action=="key":
                for key in value.split(","): q.key(key.strip())
            elif action=="type": q.type(value)
            elif action=="wait": q.wait_for(value)
            elif action=="absent": q.wait_absent(value)
            elif action=="capture":
                previous=None
                stable=time.monotonic()
                deadline=stable+20
                while time.monotonic()<deadline:
                    current=q.text(RUNTIME/"inspect")
                    if current!=previous: previous=current; stable=time.monotonic()
                    elif time.monotonic()-stable>1.5: break
                    time.sleep(.15)
                else: raise TimeoutError("Screen did not settle")
                print(q.capture(OUT/value))
            elif action=="text": print(q.text(RUNTIME/"inspect"))
            else: raise ValueError(action)
    record["outcome"]="completed"
except BaseException as e:
    record["outcome"]="failed"
    record["error"]=repr(e)
    raise
finally:
    with (OUT/"trace.jsonl").open("a") as f: f.write(json.dumps(record)+"\n")
