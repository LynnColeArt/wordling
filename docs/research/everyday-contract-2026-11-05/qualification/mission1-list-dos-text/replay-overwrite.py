from pathlib import Path
from tempfile import mkdtemp
from subprocess import run
import shutil, time
import guest, qmp
root = Path.cwd()
out = Path(mkdtemp(prefix="mission1-dos-controls-", dir=root/"research/cache"))
shutil.copyfile(__file__, out/"probe.py")
print(out, flush=True)
guest.RUNTIME = qmp.RUNTIME = Path(mkdtemp(prefix="wordling-ctrl-", dir="/tmp"))
guest.SOCKET = qmp.SOCKET = guest.RUNTIME/"qmp.sock"
private = out/"guest"
try:
    command = guest.start(private)
    guest.stop()
    shutil.copyfile(guest.MASTER/"harddisk.img", private/"harddisk.img")
    disk = str(private/"harddisk.img")+"@@1048576"
    target = out/"BACK.TXT"
    target.write_bytes(b"old bytes\x1a")
    run(["mcopy", "-i", disk, str(target), "::OUT/BACK.TXT"], check=True)
    run(command, check=True)
    with qmp.QMP() as q:
        def keys(*parts):
            for key in parts:
                q.key(key)
        def type_text(text):
            for char in text:
                q.type(char)
                time.sleep(.14)
        def snap(label):
            time.sleep(.55)
            screen = q.capture(out/label)
            print(label, " | ".join(row.strip() for row in screen.splitlines() if row.strip()), flush=True)
            return screen
        q.wait_for("Doc 1 Pg", timeout=60)
        type_text("new text")
        for label, response in [("decline","ret"),("accept","y")]:
            if label == "decline":
                keys("ctrl-f5","1","1")
            q.wait_for("Document to be saved (DOS Text)")
            type_text(r"C:\OUT\BACK.TXT")
            keys("ret")
            q.wait_for("Replace ")
            snap(label+"-question")
            keys(response)
            snap(label+"-after")
        q.key("f10")
        q.wait_for("Document to be saved")
        snap("native-save-after-export")
    guest.stop()
    run(["mcopy", "-o", "-i", disk, "::OUT/BACK.TXT", str(out/"BACK.TXT")], check=True)
    print(repr((out/"BACK.TXT").read_bytes()), flush=True)
finally:
    guest.stop()
