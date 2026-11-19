from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp
from subprocess import run
import shutil, sys, time
import guest, qmp
level = sys.argv[1] if len(sys.argv) > 1 else "1"
if level not in {"1", "5"}:
    raise SystemExit("level must be 1 or 5")
out = Path(mkdtemp(prefix="mission1-toc-native-", dir=Path.cwd()/"research/cache"))
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
            keys(level,"ret")
            time.sleep(.8)
            snap("marked")
            keys("alt-f3")
            snap("reveal")
            keys("home","home","up")
            snap("reveal-first")
            keys("f10")
            q.wait_for("Document to be saved")
            q.type(r"C:\OUT\TOC.WP")
            keys("ret")
            q.wait_absent("Document to be saved")
            keys("f7","n","y")
            q.wait_absent("Exit WP?")
        guest.stop()
        run(["mcopy","-i",str(private/"harddisk.img")+"@@1048576","::OUT/TOC.WP",str(out/("LEVEL"+level+".WP"))],check=True)
    finally:
        guest.stop()
