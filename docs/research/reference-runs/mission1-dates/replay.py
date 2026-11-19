from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp
from subprocess import run
import shutil, sys, time
import guest, qmp
literal_only = len(sys.argv) > 1 and sys.argv[1] == "literal"
out = Path(mkdtemp(prefix="mission1-dates-", dir=Path.cwd()/"research/cache"))
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
            q.type("Literal: ")
            keys("shift-f5")
            time.sleep(1.75)
            snap("menu")
            keys("1","ret")
            if not literal_only:
                q.type("Dynamic: ")
                keys("shift-f5","2")
            keys("alt-f3")
            snap("reveal")
            keys("home","home","up")
            snap("reveal-first")
            keys("f10")
            q.wait_for("Document to be saved")
            q.type(r"C:\OUT\DATES.WP")
            keys("ret")
            q.wait_absent("Document to be saved")
            keys("f7","n","y")
            q.wait_absent("Exit WP?")
        guest.stop()
        run(["mcopy","-i",str(private/"harddisk.img")+"@@1048576","::OUT/DATES.WP",str(out/("LITERAL.WP" if literal_only else "DATES.WP"))],check=True)
    finally:
        guest.stop()
