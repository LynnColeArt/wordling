from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp
from subprocess import run
import shutil, time
import guest, qmp
out = Path(mkdtemp(prefix="mission1-tab-chain-", dir=Path.cwd()/"research/cache"))
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
            keys("ctrl-f6")
            q.type("12")
            keys("tab")
            q.type("after tab")
            keys("ret","ctrl-f6")
            q.type("5")
            keys("ctrl-f6")
            q.type("2.50")
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
