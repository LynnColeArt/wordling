from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp
from subprocess import run
import shutil, time
import guest, qmp
out = Path(mkdtemp(prefix="mission1-sort-", dir=Path.cwd()/"research/cache"))
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
            for first, second in (("Zebra","Keep Z"),("Amber","Keep A")):
                q.type(first)
                q.wait_for(first)
                keys("f9")
                q.type(second)
                q.wait_for(second)
                keys("f9","shift-f9","2")
            save("BEFORE.WP")
            keys("ctrl-f9","2","ret","ret")
            snap("sort")
            keys("7")
            snap("record-type")
            keys("1")
            snap("merge-criteria")
            keys("1")
            q.wait_for("Amber")
            snap("sorted")
            save("SORTED.WP")
            keys("f7","n","y")
            q.wait_absent("Exit WP?")
        guest.stop()
        for name in ("BEFORE.WP","SORTED.WP"):
            run(["mcopy","-i",str(private/"harddisk.img")+"@@1048576","::OUT/"+name,str(out/name)],check=True)
    finally:
        guest.stop()
