from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp
from subprocess import run
import shutil, time
import guest, qmp
out = Path(mkdtemp(prefix="mission1-startup-macro-", dir=Path.cwd()/"research/cache"))
shutil.copyfile(__file__,out/"replay.py")
print(out,flush=True)
with TemporaryDirectory(prefix="wordling-conditional-") as runtime:
    guest.RUNTIME = qmp.RUNTIME = Path(runtime)
    guest.SOCKET = qmp.SOCKET = guest.RUNTIME/"qmp.sock"
    try:
        private=out/"guest"
        command = guest.start(private)
        guest.stop()
        shutil.copyfile(guest.MASTER/"harddisk.img", private/"harddisk.img")
        disk = str(private/"harddisk.img")+"@@1048576"
        fixture = Path.cwd()/"docs/research/reference-runs/mission1-startup-macro/TESTMAC.WPM"
        run(["mcopy","-i",disk,str(fixture),"::WP51/TESTMAC.WPM"],check=True)
        run(command,check=True)
        with qmp.QMP() as q:
            q.wait_for("Doc 1 Pg",timeout=60)
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
            keys("f7")
            q.wait_for("Save document?")
            keys("n")
            q.wait_for("Exit WP?")
            keys("y")
            q.wait_absent("Exit WP?")
            snap("dos")
            for char in "wp /m-TESTMAC":
                q.type(char)
                time.sleep(.14)
            keys("ret")
            q.wait_for("ABC",timeout=20)
            snap("startup")
            save("START.WP")
            keys("f7","n","y")
            q.wait_absent("Exit WP?")
        guest.stop()
        for name in ("START.WP",):
            run(["mcopy","-i",str(private/"harddisk.img")+"@@1048576","::OUT/"+name,str(out/name)],check=True)
    finally:
        guest.stop()
