from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
import sys,time
import guest,qmp
root=Path(sys.argv[1]);root.mkdir()
branch = sys.argv[2] if len(sys.argv) > 2 else "alpha"
if branch not in ("alpha", "double", "reset", "single", "pages"):
    raise SystemExit("expected alpha, double, reset, single, or pages")
with TemporaryDirectory(prefix="wp-initial-codes-") as runtime:
    guest.RUNTIME=qmp.RUNTIME=Path(runtime)
    guest.SOCKET=qmp.SOCKET=guest.RUNTIME/'qmp.sock'
    try:
        p=root/'guest';guest.start(p)
        with qmp.QMP() as q:
            def keys(*items):
                for item in items: q.key(item);time.sleep(.20)
            def snap(name):
                time.sleep(.5)
                s=q.capture(root/name)
                print(name," | ".join(row.strip() for row in s.splitlines() if row.strip()),flush=True)
            q.wait_for('Doc 1 Pg',timeout=60)
            keys("shift-f8","3")
            snap("document")
            keys("2")
            snap("initial")
            keys("shift-f8","1","6","1" if branch == "single" else "2","ret");snap("spacing")
            keys("f7","f7","f7");snap("exit-initial")
            q.wait_for("Doc 1 Pg")
            if branch == "reset":
                keys("shift-f8","3","2");snap("reopened")
                keys("shift-f8","1","6","1","ret","f7","f7","f7");snap("reset")
            for c in "alpha":q.type(c);time.sleep(.13)
            if branch == "pages":
                for _ in range(29):
                    keys("ret");q.type("beta")
                snap("page-two")
            elif branch != "alpha":
                keys("ret");q.type("beta")
            keys("f10");q.wait_for("Document to be saved")
            for c in r"C:\OUT\INIT.WP":q.type(c);time.sleep(.13)
            keys("ret");q.wait_absent("Document to be saved");time.sleep(.6)
            keys("f7","n","y");q.wait_absent("Exit WP?")
        guest.stop()
        run(["mcopy","-i",str(p/"harddisk.img")+"@@1048576","::OUT/INIT.WP",str(root/"INIT.WP")],check=True)
    finally: guest.stop()
