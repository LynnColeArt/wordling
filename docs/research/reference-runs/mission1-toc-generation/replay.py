from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp
from subprocess import run
import shutil, time
import guest, qmp
out = Path(mkdtemp(prefix="mission1-toc-generate2-", dir=Path.cwd()/"research/cache"))
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
            q.type("Overview")
            keys("home","home","up","alt-f4","end")
            keys("alt-f5")
            time.sleep(1.3)
            snap("mark-menu")
            keys("1")
            time.sleep(.6)
            snap("toc-level")
            keys("1","ret")
            time.sleep(.8)
            snap("marked")
            keys("home","home","up","alt-f5","5","1")
            snap("definition")
            keys("f7")
            snap("defined")
            keys("alt-f5","6")
            time.sleep(.7)
            snap("generate-menu")
            keys("5")
            snap("confirm")
            keys("n")
            snap("declined")
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
    finally:
        guest.stop()
