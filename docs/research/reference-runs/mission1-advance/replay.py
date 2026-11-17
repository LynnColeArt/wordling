from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
import sys,time
import guest,qmp
root=Path(sys.argv[1]);root.mkdir()
case = sys.argv[2]
if case not in ("horizontal", "boundary"):
    raise SystemExit("expected horizontal or boundary")
with TemporaryDirectory(prefix="wp-advance-") as runtime:
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
            if case == "horizontal":
                keys("shift-f8","4","1");snap("advance")
                keys("6");snap("position-entry")
                keys("3","ret");snap("position-set")
                keys("f7");q.wait_for("Doc 1 Pg")
                q.type("A");snap("position-done")
                keys("shift-f8","4","1","5","1","ret","f7");q.wait_for("Doc 1 Pg")
                q.type("B");snap("right-done")
                keys("alt-f3");snap("reveal")
                keys("alt-f3")
            else:
                q.type("top")
                for _ in range(51):
                    keys("ret")
                q.type("bottom");snap("near-bottom")
                keys("shift-f8","4","1","2");snap("down-entry")
                keys("3","ret");snap("after-entry")
                keys("f7");snap("after-format")
                q.type("Z");snap("after-typing")
                keys("alt-f3");snap("reveal")
                keys("alt-f3")
            keys("f10");q.wait_for("Document to be saved")
            for c in r"C:\OUT\INIT.WP":q.type(c);time.sleep(.13)
            keys("ret");q.wait_absent("Document to be saved");time.sleep(.6)
            keys("f7","n","y");q.wait_absent("Exit WP?")
        guest.stop()
        run(["mcopy","-i",str(p/"harddisk.img")+"@@1048576","::OUT/INIT.WP",str(root/"INIT.WP")],check=True)
    finally: guest.stop()
