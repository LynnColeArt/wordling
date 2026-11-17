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
                q.type(char)
                time.sleep(.12)
        def mark(label):
            screen = snap(label)
            q.hmp(f'pmemsave 0x450 16 "{out / label / "bios-cursor.bin"}"')
        type_text("before")
        type_text(" inline")
        keys("shift-f8","1","7")
        mark("left-entry")
        type_text('2"')
        keys("ret")
        mark("right-entry")
        type_text('1.5"')
        keys("ret")
        mark("accepted")
        keys("f7")
        q.wait_for("Doc 1 Pg")
        type_text(" after " + "word "*14)
        mark("formatted")
        keys("alt-f3")
        mark("reveal")
        keys("f10")
        q.wait_for("Document to be saved")
        type_text(r"C:\OUT\INLINE.WP")
        keys("ret")
        q.wait_for("INLINE.WP")
        q.wait_absent("Document to be saved:")
        keys("alt-f3", "f7")
        q.wait_for("Save document?")
        keys("n")
        q.wait_for("Exit WP?")
        keys("y")
        q.wait_absent("Doc 1 Pg")
    guest.stop()
    disk = str(private/"harddisk.img")+"@@1048576"
    run(["mcopy", "-i", disk, "::OUT/INLINE.WP", str(out/"INLINE.WP")], check=True)
finally:
    guest.stop()
