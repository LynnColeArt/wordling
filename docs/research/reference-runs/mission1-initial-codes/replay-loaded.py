from pathlib import Path
from tempfile import TemporaryDirectory, mkdtemp
from subprocess import run
import shutil, sys, time
import guest, qmp
root = Path.cwd()
out = Path(mkdtemp(prefix="mission1-initial-codes-loaded-", dir=root/"research/cache"))
shutil.copyfile(__file__, out/"probe.py")
print(out, flush=True)
runtime = TemporaryDirectory(prefix="wp-initial-codes-print-")
guest.RUNTIME = qmp.RUNTIME = Path(runtime.name)
guest.SOCKET = qmp.SOCKET = guest.RUNTIME/"qmp.sock"
private = out/"guest"
try:
    command = guest.start(private)
    guest.stop()
    shutil.copyfile(guest.MASTER/"harddisk.img", private/"harddisk.img")
    disk = str(private/"harddisk.img")+"@@1048576"
    fixture = Path(__file__).resolve().parent / "DOUBLE.WP"
    run(["mcopy", "-i", disk, str(fixture), "::OUT/DOUBLE.WP"], check=True)
    run(command, check=True)
    with qmp.QMP() as q:
        def keys(*parts):
            for key in parts:
                q.key(key)
                time.sleep(.12)
        def snap(label):
            time.sleep(.55)
            screen = q.capture(out/label)
            print(label, " | ".join(row.strip() for row in screen.splitlines() if row.strip()), flush=True)
            return screen
        q.wait_for("Doc 1 Pg", timeout=60)
        def type_text(text):
            for char in text:
                q.type(char)
                time.sleep(.12)
        if sys.argv[1:] == ["no"]:
            keys("shift-f1","3","5","n","f7")
            q.wait_for("Doc 1 Pg")
        elif sys.argv[1:] != ["yes"]:
            raise SystemExit("expected yes or no for Fast Save")
        keys("shift-f10")
        q.wait_for("Document to be retrieved")
        type_text(r"C:\OUT\DOUBLE.WP")
        keys("ret")
        q.wait_for("alpha")
        keys("down");snap("before-reset")
        keys("shift-f8","3","2");snap("initial")
        keys("shift-f8","1","6","1","ret","f7","f7","f7");snap("after-reset")
        type_text("X");snap("after-edit")
        keys("f10");q.wait_for("Document to be saved")
        type_text(r"C:\OUT\EDITED.WP")
        keys("ret")
        q.wait_absent("Document to be saved")
        keys("f7")
        q.wait_for("Save document?")
        keys("n")
        q.wait_for("Exit WP?")
        keys("y")
        q.wait_absent("Exit WP?")
    guest.stop()
    run(["mcopy", "-i", disk, "::OUT/EDITED.WP", str(out/"EDITED.WP")], check=True)
finally:
    guest.stop()
    runtime.cleanup()
