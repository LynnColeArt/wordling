from pathlib import Path
from tempfile import mkdtemp
from subprocess import run
import os, shutil, time
from datetime import datetime
import guest, qmp
root = Path.cwd()
out = Path(mkdtemp(prefix="mission1-find-", dir=root/"research/cache"))
shutil.copyfile(__file__, out/"probe.py")
print(out, flush=True)
guest.RUNTIME = qmp.RUNTIME = Path(mkdtemp(prefix="wordling-find-", dir="/tmp"))
guest.SOCKET = qmp.SOCKET = guest.RUNTIME/"qmp.sock"
private = out/"guest"
try:
    command = guest.start(private)
    guest.stop()
    shutil.copyfile(guest.MASTER/"harddisk.img", private/"harddisk.img")
    run(command, check=True)
    with qmp.QMP() as q:
        def keys(*parts):
            for key in parts:
                q.key(key)
                time.sleep(.12)
        def snap(label):
            time.sleep(.55)
            screen = q.capture(out/label)
            print(label, " | ".join(row.strip() for row in screen.splitlines() if row.strip()), flush=True)
            return screen
        q.wait_for("Doc 1 Pg", timeout=60)
        def type_text(text):
            for char in text:
                if char == chr(39):
                    q.key("apostrophe")
                elif char in "!?":
                    q.key("shift-1" if char == "!" else "shift-slash")
                else:
                    q.type(char)
                time.sleep(.12)
        def mark(label):
            screen = snap(label)
            q.hmp(f'pmemsave 0x450 16 "{out / label / "bios-cursor.bin"}"')
        type_text("BEFORE. I'M HERE! NEXT? THIRD. I SAID i'M HERE. lower.")
        keys("home","home","up","alt-f4")
        keys("home", "right")
        mark("selected")
        keys("shift-f3")
        mark("case-prompt")
        keys("2")
        mark("lower")
finally:
    guest.stop()
