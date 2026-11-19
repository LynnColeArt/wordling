from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp
from subprocess import run
import shutil, sys, time
import guest, qmp
fixture = sys.argv[1] if len(sys.argv) > 1 else "ROOM"
if fixture not in {"ROOM", "SHORT", "EDGE"}:
    raise SystemExit("fixture must be ROOM, SHORT, or EDGE")
out = Path(mkdtemp(prefix="mission1-conditional-", dir=Path.cwd()/"research/cache"))
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
            keys("shift-f8","2","5","2","shift-apostrophe","ret","7","shift-apostrophe","ret","f7")
            snap("short-page")
            if fixture == "SHORT":
                for i in range(8):
                    q.type(f"row {i+1}")
                    keys("ret")
            elif fixture == "EDGE":
                for _ in range(10):
                    q.type("row")
                    keys("ret")
            q.type("first")
            keys("ret")
            q.type("second")
            keys("shift-f8","4","2")
            snap("prompt")
            keys("3","ret","f7")
            snap("inserted")
            keys("ret")
            q.type("Heading")
            keys("ret")
            q.type("first protected")
            keys("ret")
            q.type("second protected")
            keys("alt-f3")
            snap("reveal")
            keys("home","home","up")
            snap("reveal-first")
            keys("f10")
            q.wait_for("Document to be saved")
            q.type(r"C:\OUT\COND.WP")
            keys("ret")
            q.wait_absent("Document to be saved")
            keys("f7","n","y")
            q.wait_absent("Exit WP?")
        guest.stop()
        run(["mcopy","-i",str(private/"harddisk.img")+"@@1048576","::OUT/COND.WP",str(out/(fixture+".WP"))],check=True)
    finally:
        guest.stop()
