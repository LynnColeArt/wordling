from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp
from subprocess import run
import shutil, time
import guest, qmp
out = Path(mkdtemp(prefix="mission1-decimal-stop-", dir=Path.cwd()/"research/cache"))
shutil.copyfile(__file__,out/"replay.py")
print(out,flush=True)
with TemporaryDirectory(prefix="wordling-tabs-") as runtime:
    guest.RUNTIME = qmp.RUNTIME = Path(runtime)
    guest.SOCKET = qmp.SOCKET = guest.RUNTIME/"qmp.sock"
    try:
        private=out/"guest"
        guest.start(private)
        with qmp.QMP() as q:
            def keys(*parts):
                for key in parts:
                    q.key(key)
                    time.sleep(.14)
            def snap(label):
                time.sleep(.40)
                print(label, " | ".join(row.strip() for row in q.capture(out/label).splitlines() if row.strip()),flush=True)
            q.type("Before")
            keys("tab")
            q.type("old")
            keys("ret","shift-f8","1","8")
            snap("tab-set")
            keys("2","dot","2","ret","d")
            snap("tab-edit")
            keys("f7","f7")
            keys("tab","tab","tab","tab","tab")
            q.type("12.34")
            keys("ret","tab","tab","tab","tab","tab")
            q.type("5.67")
            snap("normal")
            keys("alt-f3")
            snap("reveal")
            keys("f10")
            q.wait_for("Document to be saved")
            q.type(r"C:\OUT\TABS.WP")
            keys("ret")
            q.wait_absent("Document to be saved")
            keys("f7","n","y")
            q.wait_absent("Exit WP?")
        guest.stop()
        run(["mcopy","-i",str(private/"harddisk.img")+"@@1048576","::OUT/TABS.WP",str(out/"TABS.WP")],check=True)
    finally:
        guest.stop()
