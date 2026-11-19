from pathlib import Path
from tempfile import mkdtemp
from subprocess import run
import shutil, time
import guest, qmp
root = Path.cwd()
out = Path(mkdtemp(prefix="mission1-linenum-print-", dir=root/"research/cache"))
shutil.copyfile(__file__, out/"probe.py")
print(out, flush=True)
guest.RUNTIME = qmp.RUNTIME = Path(mkdtemp(prefix="wordling-find-", dir="/tmp"))
guest.SOCKET = qmp.SOCKET = guest.RUNTIME/"qmp.sock"
private = out/"guest"
try:
    command = guest.start(private)
    guest.stop()
    shutil.copyfile(guest.MASTER/"harddisk.img", private/"harddisk.img")
    disk = str(private/"harddisk.img")+"@@1048576"
    sources = {
        "LINENUM.WP": root/"docs/research/reference-runs/mission1-line-numbering/LINENUM.WP",
    }
    for name, path in sources.items():
        run(["mcopy", "-i", disk, str(path), "::OUT/"+name], check=True)
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
        def open_list():
            keys("f5")
            type_text(r"C:\OUT" + chr(92))
            keys("shift-8", "dot", "shift-8", "ret")
            q.wait_for("RICH    .WP")
        def type_text(text):
            for char in text:
                q.type(char)
                time.sleep(.12)
        for name in sources:
            stem = name.split(".")[0]
            keys("shift-f7")
            q.wait_for("Full Document")
            keys("s","3","2","8")
            q.wait_for("Device or Filename")
            type_text(r"C:\OUT"+chr(92)+stem+".PRN")
            keys("ret","f7","f7","f7")
            q.wait_for("Doc 1 Pg")
            keys("shift-f7","3")
            type_text(r"C:\OUT"+chr(92)+name)
            keys("ret")
            q.wait_for("Page(s)")
            keys("ret")
            time.sleep(2)
            snap(stem+"-printed")
            keys("f7")
            q.wait_for("Doc 1 Pg")
        keys("f7")
        q.wait_for("Save document?")
        keys("n")
        q.wait_for("Exit WP?")
        keys("y")
        q.wait_absent("Exit WP?")
    guest.stop()
    for name in sources:
        name = name.replace(".WP", ".PRN")
        run(["mcopy", "-i", disk, "::OUT/"+name, str(out/name)], check=True)
finally:
    guest.stop()
