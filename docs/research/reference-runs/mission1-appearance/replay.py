from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
import sys,time
import guest,qmp
out=Path(sys.argv[1]);out.mkdir(exist_ok=True)
with TemporaryDirectory(prefix="wp-appearance-") as runtime:
    guest.RUNTIME=qmp.RUNTIME=Path(runtime); guest.SOCKET=qmp.SOCKET=guest.RUNTIME/'qmp.sock'
    try:
        p=out/'guest';guest.start(p)
        with qmp.QMP() as q:
            def keys(*items):
                for item in items:
                    q.key(item);time.sleep(.24)
            def snap(name):
                time.sleep(.6); print(name," | ".join(i.strip() for i in q.capture(out/name).splitlines() if i.strip()),flush=True)
            q.wait_for("Doc 1 Pg",timeout=60)
            keys("ctrl-f8");snap("font")
            keys("2");snap("appearance")
            keys("4")
            q.type("alpha"); time.sleep(.6)
            keys("ctrl-f8","2","4")
            q.type("beta"); time.sleep(.6)
            snap("typed")
            keys("alt-f3","home","home","up"); snap("reveal")
            keys("alt-f3","f10"); q.wait_for("Document to be saved")
            q.type(r"C:\OUT\ITALICS.WP"); q.wait_for("ITALICS.WP")
            keys("ret"); q.wait_absent("Document to be saved"); time.sleep(.7)
            keys("f7","n","y"); q.wait_absent("Exit WP?")
        guest.stop()
        run(["mcopy", "-i", str(p/"harddisk.img")+"@@1048576", "::OUT/ITALICS.WP", str(out/"ITALICS.WP")], check=True)
    finally:guest.stop()
