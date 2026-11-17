from pathlib import Path
from tempfile import mkdtemp
from subprocess import run
import shutil
import time
import guest, qmp

root = Path.cwd()
out = Path(mkdtemp(prefix="mission1-footnote-", dir=root/"research/cache"))
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
        keys("ctrl-f7","1","4")
        snap("footnote-options")
        keys("2")
        snap("keep-prompt")
        keys("1","dot","2","5","ret")
        snap("keep-set")
        keys("f7")
        snap("returned")
        text("Body")
        keys("ctrl-f7","1","1")
        snap("note-editor")
        for line in ("First note line","Second note line","Third note line","Fourth note line","Fifth note line"): 
            text(line)
            keys("ret")
        text("Last note line")
        keys("f7")
        snap("note-close")
        keys("alt-f3")
        snap("reveal")
        keys("f10")
        q.wait_for("Document to be saved")
        text(r"C:\OUT\NOTEKEEP.WP")
        keys("ret")
        q.wait_absent("Document to be saved")
        keys("f7","n","y")
        q.wait_absent("Exit WP?")
    guest.stop()
    disk=str(private/"harddisk.img")+"@@1048576"
    run(["mcopy","-i",disk,"::OUT/NOTEKEEP.WP",str(out/"NOTEKEEP.WP")],check=True)
finally:
    guest.stop()
