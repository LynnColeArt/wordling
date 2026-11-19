from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp
from subprocess import run
import shutil, time
import guest, qmp
out = Path(mkdtemp(prefix="mission1-printer-command-", dir=Path.cwd()/"research/cache"))
shutil.copyfile(__file__,out/"replay.py")
print(out,flush=True)
with TemporaryDirectory(prefix="wordling-conditional-") as runtime:
    guest.RUNTIME = qmp.RUNTIME = Path(runtime)
    guest.SOCKET = qmp.SOCKET = guest.RUNTIME/"qmp.sock"
    try:
        private=out/"guest"
        guest.start(private)
        with qmp.QMP() as q:
            def keys(*parts):
                for key in parts:
                    q.key(key)
                    time.sleep(.23)
            def snap(label):
                time.sleep(.25)
                print(label, " | ".join(row.strip() for row in q.capture(out/label).splitlines() if row.strip()),flush=True)
            def save(name):
                keys("f10")
                q.wait_for("Document to be saved")
                q.type("C:\\OUT\\" + name)
                keys("ret")
                q.wait_absent("Document to be saved")
            q.type("Before")
            q.wait_for("Before")
            keys("shift-f8","4","6","2","1")
            snap("command-input")
            for char in "<36>TEST":
                q.type(char)
                time.sleep(.20)
            keys("ret")
            snap("command-menu")
            keys("f7")
            q.type("After")
            q.wait_for("After")
            keys("alt-f3")
            q.wait_for("Press Reveal Codes")
            snap("reveal")
            save("PRTCMD.WP")
            keys("f7","n","y")
            q.wait_absent("Exit WP?")
        guest.stop()
        for name in ("PRTCMD.WP",):
            run(["mcopy","-i",str(private/"harddisk.img")+"@@1048576","::OUT/"+name,str(out/name)],check=True)
    finally:
        guest.stop()
