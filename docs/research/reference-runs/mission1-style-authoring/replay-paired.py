from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp
from subprocess import run
import shutil, time
import guest, qmp
out = Path(mkdtemp(prefix="mission1-style-formatted-", dir=Path.cwd()/"research/cache"))
shutil.copyfile(__file__,out/"replay.py")
print(out,flush=True)
with TemporaryDirectory(prefix="wordling-conditional-") as runtime:
    guest.RUNTIME = qmp.RUNTIME = Path(runtime)
    guest.SOCKET = qmp.SOCKET = guest.RUNTIME/"qmp.sock"
    try:
        private=out/"guest"
        command = guest.start(private)
        guest.stop()
        run(["mdel", "-i", str(private/"harddisk.img")+"@@1048576", "::WP51/LIBRARY.STY"], check=True)
        run(command, check=True)
        with qmp.QMP() as boot:
            boot.wait_for("Are other copies", timeout=45)
            boot.key("n")
        with qmp.QMP() as q:
            def keys(*parts):
                for key in parts:
                    q.key(key)
                    time.sleep(.10)
            def snap(label):
                time.sleep(.25)
                print(label, " | ".join(row.strip() for row in q.capture(out/label).splitlines() if row.strip()),flush=True)
            q.wait_for("Doc 1 Pg", timeout=60)
            keys("shift-f1","3","5","n","f7")
            keys("alt-f8")
            snap("initial")
            keys("3")
            q.wait_for("Styles: Edit")
            keys("1")
            time.sleep(.6)
            q.type("EMPHASIS")
            time.sleep(1)
            keys("ret")
            snap("named")
            keys("4")
            snap("codes")
            keys("f6","f7","f7")
            snap("created")
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
