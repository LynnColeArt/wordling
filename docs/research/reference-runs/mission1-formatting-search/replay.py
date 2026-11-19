from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
import sys,time
import guest,qmp
root=Path(sys.argv[1]);root.mkdir()
with TemporaryDirectory(prefix="wp-formatting-search-") as runtime:
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
            keys("bracket_left")
            q.type("UND")
            keys("bracket_right","spc","f8")
            q.type("word")
            keys("f8","home","home","up","alt-f3");snap("before")
            keys("f2","f8");snap("query")
            keys("f2");snap("matched")
            q.type("X");snap("caret-witness")
            keys("alt-f3")
            keys("f10");q.wait_for("Document to be saved")
            for c in r"C:\OUT\INIT.WP":q.type(c);time.sleep(.13)
            keys("ret");q.wait_absent("Document to be saved");time.sleep(.6)
            keys("f7","n","y");q.wait_absent("Exit WP?")
        guest.stop()
        run(["mcopy","-i",str(p/"harddisk.img")+"@@1048576","::OUT/INIT.WP",str(root/"INIT.WP")],check=True)
    finally: guest.stop()
