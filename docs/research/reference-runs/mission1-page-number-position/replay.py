from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
import sys,time
import guest,qmp
root=Path(sys.argv[1]);root.mkdir(); choice=sys.argv[2]; suppress=len(sys.argv)>3
with TemporaryDirectory(prefix="wp-page-number-") as runtime:
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
            keys("shift-f8","2","6")
            snap("page-numbering")
            keys("4")
            snap("position")
            keys(choice);snap("selected")
            keys("f7");q.wait_for("Doc 1 Pg")
            if suppress:
                keys("shift-f8","2","8");snap("suppress")
                keys("4","y");snap("suppress-on");keys("f7")
                q.wait_for("Doc 1 Pg")
            q.type("Alpha")
            keys("ctrl-ret");q.type("Beta")
            keys("ctrl-ret");q.type("Gamma")
            keys("home","home","up","alt-f3");snap("reveal")
            keys("alt-f3","f10");q.wait_for("Document to be saved")
            for c in r"C:\OUT\PAGES.WP":q.type(c);time.sleep(.13)
            keys("ret");q.wait_absent("Document to be saved");time.sleep(.5)
            keys("f7","n","y");q.wait_absent("Exit WP?")
        guest.stop()
        run(["mcopy","-i",str(p/"harddisk.img")+"@@1048576","::OUT/PAGES.WP",str(root/"PAGES.WP")],check=True)
    finally: guest.stop()
