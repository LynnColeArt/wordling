from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp
from subprocess import run
import shutil, time
import guest, qmp
out = Path(mkdtemp(prefix="mission1-style-form-", dir=Path.cwd()/"research/cache"))
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
                    time.sleep(.10)
            def snap(label):
                time.sleep(.25)
                print(label, " | ".join(row.strip() for row in q.capture(out/label).splitlines() if row.strip()),flush=True)
            keys("alt-f8","3")
            q.wait_for("Styles: Edit")
            keys("1")
            time.sleep(.6)
            q.type("WPTEST")
            time.sleep(1)
            keys("ret")
            snap("named")
            keys("4")
            snap("codes")
            keys("f6","f7","f7")
            snap("created")
            keys("3")
            q.wait_for("Styles: Edit")
            keys("1")
            time.sleep(.6)
            q.type("wptest")
            time.sleep(1)
            keys("ret")
            snap("duplicate")
            keys("f1","f1")
            snap("after-cancel")
            keys("1")
            q.type("Styled text")
            keys("alt-f3")
            snap("reveal")
            keys("home","home","up")
            snap("reveal-first")
            keys("f10")
            q.wait_for("Document to be saved")
            q.type(r"C:\OUT\STYLE.WP")
            keys("ret")
            q.wait_absent("Document to be saved")
            keys("f7","n","y")
            q.wait_absent("Exit WP?")
        guest.stop()
        run(["mcopy","-i",str(private/"harddisk.img")+"@@1048576","::OUT/STYLE.WP",str(out/"STYLE.WP")],check=True)
    finally:
        guest.stop()
