from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp
from subprocess import run
import shutil, time
import guest, qmp
out = Path(mkdtemp(prefix="mission1-table-vertical-", dir=Path.cwd()/"research/cache"))
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
                    time.sleep(.23)
            def snap(label):
                time.sleep(.25)
                print(label, " | ".join(row.strip() for row in q.capture(out/label).splitlines() if row.strip()),flush=True)
            def save(name):
                keys("f10")
                q.wait_for("Document to be saved")
                q.type("C:\\OUT\\" + name)
                keys("ret")
                q.wait_absent("Document to be saved")
            keys("alt-f7","2","1","2","ret","2","ret","f7")
            q.type("ALPHA")
            keys("tab")
            q.type("BETA")
            keys("tab")
            q.type("GAMMA")
            keys("tab")
            q.type("DELTA")
            q.wait_for("DELTA")
            snap("cells")
            keys("shift-tab","shift-tab","shift-tab")
            q.wait_for("Cell A1")
            keys("alt-f7")
            q.wait_for("7 Join")
            snap("table-edit")
            keys("alt-f4","down")
            snap("block")
            keys("7")
            q.wait_for("Yes")
            snap("join")
            keys("y")
            snap("joined")
            keys("f7")
            snap("editing")
            save("VERT.WP")
            keys("f7","n","y")
            q.wait_absent("Exit WP?")
        guest.stop()
        for name in ("VERT.WP",):
            run(["mcopy","-i",str(private/"harddisk.img")+"@@1048576","::OUT/"+name,str(out/name)],check=True)
    finally:
        guest.stop()
