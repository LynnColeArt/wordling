# Run from the repo root: PYTHONPATH=scripts/reference python3 replay.py OUTPUT
from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
import shutil
import sys,time
import guest,qmp
out=Path(sys.argv[1])
out.mkdir()
with TemporaryDirectory(prefix="wp-compare-") as t:
    guest.RUNTIME=qmp.RUNTIME=Path(t)
    guest.SOCKET=qmp.SOCKET=guest.RUNTIME/'qmp.sock'
    try:
        p=out/'guest'
        guest.start(p)
        with qmp.QMP() as q:
            def keys(*items):
                for item in items:
                    q.key(item);time.sleep(.18)
            def snap(label):
                time.sleep(.4)
                print(label, " | ".join(row.strip() for row in q.capture(out/label).splitlines() if row.strip()),flush=True)
            q.wait_for("Doc 1 Pg",timeout=60)
            q.type("Overview")
            keys("ret")
            q.type("Alpha old tail")
            keys("ret")
            q.type("Closing")
            time.sleep(.3)
            keys("f10")
            q.wait_for("Document to be saved")
            q.type(r"C:\OUT\BEFORE.WP")
            keys("ret")
            q.wait_absent("Document to be saved")
            time.sleep(.6)
            keys("home","home","up","down")
            q.wait_for("Alpha old tail")
            for _ in range(6): keys("right")
            for _ in range(3): keys("delete")
            q.type("new")
            snap("edited")
            keys("alt-f5","6")
            snap("generate")
            keys("2")
            snap("compare")
            q.wait_for("Other Document:")
            keys("ret")
            snap("result")
            keys("alt-f3","home","home","up")
            snap("reveal")
            keys("alt-f3","f10")
            q.wait_for("Document to be saved")
            q.type(r"C:\OUT\COMPARE.WP")
            snap("save-name")
            keys("ret")
            q.wait_absent("Document to be saved")
            snap("saved")
            keys("f7","n","y")
            q.wait_absent("Exit WP?")
        guest.stop()
        disk = str(p / "harddisk.img") + "@@1048576"
        for name in ("BEFORE.WP", "COMPARE.WP"):
            run(["mcopy", "-i", disk, "::OUT/" + name, str(out / name)], check=True)
    finally:
        guest.stop()
