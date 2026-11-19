from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp
from subprocess import run
import shutil, sys, time
import guest, qmp
fixture = sys.argv[1] if len(sys.argv) > 1 else "WIDOW"
if fixture not in {"WIDOW", "WIDEOF", "ORPHAN", "TOGGLE"}:
    raise SystemExit("fixture must be WIDOW, WIDEOF, ORPHAN, or TOGGLE")
out = Path(mkdtemp(prefix="mission1-widow-", dir=Path.cwd()/"research/cache"))
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
            if fixture == "TOGGLE":
                keys("shift-f8", "1", "9", "y", "f7")
                q.type("enabled")
                keys("ret", "shift-f8", "1", "9", "n", "f7")
                q.type("disabled")
            else:
                for _ in range(11 if fixture == "ORPHAN" else 10):
                    q.type("row")
                    keys("ret")
                keys("shift-f8", "1", "9")
                snap("prompt")
                keys("y", "f7")
                q.type("test ")
                for _ in range(36):
                    q.type("word ")
                if fixture != "WIDEOF":
                    keys("ret")
                    q.type("after")
            keys("alt-f3")
            snap("reveal")
            keys("home","home","up")
            snap("reveal-first")
            keys("f10")
            q.wait_for("Document to be saved")
            q.type(r"C:\OUT\WIDOW.WP")
            keys("ret")
            q.wait_absent("Document to be saved")
            keys("f7","n","y")
            q.wait_absent("Exit WP?")
        guest.stop()
        run(["mcopy","-i",str(private/"harddisk.img")+"@@1048576","::OUT/WIDOW.WP",str(out/(fixture+".WP"))],check=True)
    finally:
        guest.stop()
