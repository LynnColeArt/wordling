from pathlib import Path
from tempfile import mkdtemp
from subprocess import run
import shutil
import time
import guest, qmp

root = Path.cwd()
out = Path(mkdtemp(prefix="mission1-line-format-", dir=root/"research/cache"))
shutil.copyfile(__file__, out/"replay.py")
print(out, flush=True)
guest.RUNTIME = qmp.RUNTIME = Path(mkdtemp(prefix="wordling-block-copy-", dir="/tmp"))
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
            time.sleep(.45)
            screen = q.capture(out/label)
            print(label, " | ".join(row.strip() for row in screen.splitlines() if row.strip()), flush=True)
        def text(string):
            for char in string:
                q.type(char)
                time.sleep(.10)
        q.wait_for("Doc 1 Pg", timeout=60)
        text("alpha")
        keys("home","spc")
        text("beta")
        keys("ctrl-f5","1","1")
        q.wait_for("Document to be saved (DOS Text)",timeout=8)
        text(r"C:\OUT\HSPACE.TXT")
        keys("ret")
        q.wait_absent("Document to be saved (DOS Text)")
        keys("f7")
        q.wait_for("Save document?",timeout=8)
        keys("n")
        q.wait_for("Exit WP?",timeout=8)
        keys("y")
        q.wait_absent("Doc 1 Pg")
    guest.stop()
    disk = str(private/"harddisk.img")+"@@1048576"
    run(["mcopy", "-i", disk, "::OUT/HSPACE.TXT", str(out/"HSPACE.TXT")], check=True)
finally:
    guest.stop()
