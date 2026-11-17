from pathlib import Path
from tempfile import mkdtemp
from subprocess import run
import shutil
import time
import guest, qmp

root = Path.cwd()
out = Path(mkdtemp(prefix="mission1-page-margins-", dir=root/"research/cache"))
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
        text("first page")
        keys("ctrl-ret","shift-f8","2","5")
        snap("top-entry")
        text('2"')
        keys("ret")
        snap("bottom-entry")
        text('1.25"')
        keys("ret","f7")
        text("second page")
        snap("second-page")
        keys("ret")
        text("next line")
        keys("alt-f3")
        snap("reveal")
        keys("f10")
        q.wait_for("Document to be saved", timeout=8)
        text(r"C:\OUT\PAGEMAR.WP")
        keys("ret")
        q.wait_absent("Document to be saved:")
        keys("alt-f3", "f7")
        q.wait_for("Save document?", timeout=8)
        keys("n")
        q.wait_for("Exit WP?", timeout=8)
        keys("y")
        q.wait_absent("Doc 1 Pg")
    guest.stop()
    disk = str(private/"harddisk.img")+"@@1048576"
    run(["mcopy", "-i", disk, "::OUT/PAGEMAR.WP", str(out/"PAGEMAR.WP")], check=True)
finally:
    guest.stop()
