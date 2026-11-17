from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp
from subprocess import run
import shutil, time
import guest, qmp
out = Path(mkdtemp(prefix="mission1-cross-renumber-", dir=Path.cwd()/"research/cache"))
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
            q.type("See page ")
            keys("alt-f5","1")
            snap("cross-reference")
            keys("1")
            snap("reference-type")
            keys("1")
            snap("reference-name")
            q.type("Mixed")
            keys("ret")
            snap("reference-mark")
            keys("ctrl-ret")
            keys("shift-f8","2","6","1")
            snap("new-page-number")
            keys("7","f7","f7")
            snap("renumbered")
            q.type("Chapter")
            keys("alt-f5","1","2")
            snap("target-name")
            q.type("mixed")
            keys("ret","alt-f3")
            snap("marked")
            save("BEFORE.WP")
            keys("alt-f5","6","5","y")
            snap("generated")
            keys("home","home","up")
            snap("generated-reveal")
            save("AFTER.WP")
            keys("f7","n","y")
            q.wait_absent("Exit WP?")
        guest.stop()
        for name in ("BEFORE.WP", "AFTER.WP"):
            run(["mcopy","-i",str(private/"harddisk.img")+"@@1048576","::OUT/"+name,str(out/name)],check=True)
    finally:
        guest.stop()
