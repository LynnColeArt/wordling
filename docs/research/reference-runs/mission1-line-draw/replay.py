from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp
from subprocess import run
import shutil, time
import guest, qmp
out = Path(mkdtemp(prefix="mission1-line-draw-", dir=Path.cwd()/"research/cache"))
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
            for mode, name in (("1","SINGLE.WP"),("2","DOUBLE.WP")):
                keys("ctrl-f3","2")
                snap("line-menu-"+mode)
                keys(mode,"right","right","right","right","f7")
                snap("drawn-"+mode)
                keys("alt-f3")
                q.wait_for("Press Reveal Codes")
                snap("reveal-"+mode)
                keys("alt-f3")
                save(name)
                keys("f7")
                q.wait_for("Save document?")
                keys("n")
                q.wait_for("Exit WP?")
                keys("y" if mode=="2" else "n")
                q.wait_absent("Exit WP?")
        guest.stop()
        for name in ("SINGLE.WP","DOUBLE.WP"):
            run(["mcopy","-i",str(private/"harddisk.img")+"@@1048576","::OUT/"+name,str(out/name)],check=True)
    finally:
        guest.stop()
