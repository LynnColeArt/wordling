from pathlib import Path
from tempfile import mkdtemp
from subprocess import run
import shutil, time
import guest, qmp
root = Path.cwd()
out = Path(mkdtemp(prefix="mission1-spreadsheet-refresh-", dir=root/"research/cache"))
shutil.copyfile(__file__, out/"probe.py")
print(out, flush=True)
guest.RUNTIME = qmp.RUNTIME = Path(mkdtemp(prefix="wordling-find-", dir="/tmp"))
guest.SOCKET = qmp.SOCKET = guest.RUNTIME/"qmp.sock"
private = out/"guest"
try:
    command = guest.start(private)
    guest.stop()
    shutil.copyfile(guest.MASTER/"harddisk.img", private/"harddisk.img")
    disk = str(private/"harddisk.img")+"@@1048576"
    refs = root/"docs/research/reference-runs/mission1-spreadsheet"
    updated = out/"RANGE.WK1"
    import sys
    run([sys.executable, str(refs/"fixture.py"), str(updated), "19"], check=True)
    run(["mcopy", "-i", disk, str(updated), "::OUT/RANGE.WK1"], check=True)
    run(["mcopy", "-i", disk, str(refs/"LINK.WP"), "::OUT/LINK.WP"], check=True)
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
        def type_text(value):
            for char in value:
                q.type(char)
                time.sleep(.14)
        keys("shift-f10")
        q.wait_for("Document to be retrieved")
        type_text(r"C:\OUT\LINK.WP")
        keys("ret")
        q.wait_for("Amber")
        snap("before-refresh")
        keys("ctrl-f5","5","4")
        snap("link-options")
        keys("3")
        keys("home","home","up")
        q.wait_for("19")
        snap("updated")
        keys("f10")
        q.wait_for("Document to be saved")
        type_text(r"C:\OUT\UPDATED.WP")
        keys("ret")
        q.wait_absent("Document to be saved")
        keys("f7","n","y")
        q.wait_absent("Exit WP?")
    guest.stop()
    run(["mcopy", "-i", disk, "::OUT/UPDATED.WP", str(out/"UPDATED.WP")], check=True)
finally:
    guest.stop()
