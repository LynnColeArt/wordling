from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp
from subprocess import run
import shutil, time
import guest, qmp
out = Path(mkdtemp(prefix="mission1-toc-clean-", dir=Path.cwd()/"research/cache"))
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
            keys("alt-f5","5","1")
            q.wait_for("Table of Contents Definition")
            keys("f7","down")
            q.type("Overview")
            keys("home","left","alt-f4","end","alt-f5","1","1","ret")
            snap("marked")
            keys("alt-f5","6")
            time.sleep(.7)
            snap("generate-menu")
            keys("5")
            snap("confirm")
            keys("n")
            snap("declined")
            keys("f10")
            q.wait_for("Document to be saved")
            q.type(r"C:\OUT\DEFIN.WP")
            keys("ret")
            q.wait_absent("Document to be saved")

            keys("alt-f5","6","5","y")
            time.sleep(1.4)
            snap("generated")
            keys("alt-f3")
            snap("reveal")
            keys("home","home","up")
            snap("reveal-first")
            keys("f10")
            q.wait_for("Document to be saved")
            q.type(r"C:\OUT\GEN.WP")
            keys("ret")
            q.wait_absent("Document to be saved")
            keys("f7","n","y")
            q.wait_absent("Exit WP?")
        guest.stop()
        run(["mcopy","-i",str(private/"harddisk.img")+"@@1048576","::OUT/GEN.WP",str(out/"GEN.WP")],check=True)
        run(["mcopy","-i",str(private/"harddisk.img")+"@@1048576","::OUT/DEFIN.WP",str(out/"DEFIN.WP")],check=True)
    finally:
        guest.stop()
