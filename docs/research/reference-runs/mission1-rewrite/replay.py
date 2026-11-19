from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp
from subprocess import run
import shutil, time
import guest, qmp
out = Path(mkdtemp(prefix="mission1-rewrite-confirm-", dir=Path.cwd()/"research/cache"))
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
                    time.sleep(.10)
            def snap(label):
                time.sleep(.25)
                print(label, " | ".join(row.strip() for row in q.capture(out/label).splitlines() if row.strip()),flush=True)
            q.type("Rewrite keeps this text.")
            keys("left","left")
            time.sleep(2.0)
            snap("before")
            keys("ctrl-f3")
            time.sleep(1.3)
            snap("screen-menu")
            keys("3")
            snap("after")
            keys("alt-f3")
            snap("reveal")
            keys("home","home","up")
            snap("reveal-first")
            keys("f10")
            q.wait_for("Document to be saved")
            q.type(r"C:\OUT\REWRITE.WP")
            keys("ret")
            q.wait_absent("Document to be saved")
            keys("f7","n","y")
            q.wait_absent("Exit WP?")
        guest.stop()
        run(["mcopy","-i",str(private/"harddisk.img")+"@@1048576","::OUT/REWRITE.WP",str(out/"REWRITE.WP")],check=True)
    finally:
        guest.stop()
