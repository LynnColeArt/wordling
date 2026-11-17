from pathlib import Path
from tempfile import mkdtemp
from subprocess import run
import shutil, time
import guest, qmp
root = Path.cwd()
out = Path(mkdtemp(prefix="mission1-spreadsheet-offset-", dir=root/"research/cache"))
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
    fixture = root/"docs/research/reference-runs/mission1-spreadsheet/RANGE.WK1"
    from struct import pack
    raw = fixture.read_bytes()
    marker = bytes.fromhex("0d000700ff010001000700")
    assert raw.count(marker) == 1
    modified = out / "RANGE.WK1"
    modified.write_bytes(raw.replace(marker, marker[:-2] + pack("<h", -19)))
    run(["mcopy", "-i", disk, str(modified), "::OUT/RANGE.WK1"], check=True)
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
        keys("ctrl-f5","5")
        snap("spreadsheet-menu")
        keys("1")
        snap("import-menu")
        def type_text(value):
            for char in value:
                q.type(char)
                time.sleep(.14)
        keys("1")
        snap("file-entry")
        type_text(r"C:\OUT\RANGE.WK1")
        keys("ret","2")
        q.wait_for("Enter Range:")
        type_text("B2..C3")
        keys("ret")
        snap("range")
        keys("4")
        snap("imported")
        keys("f10")
        q.wait_for("Document to be saved")
        type_text(r"C:\OUT\OFFSET.WP")
        keys("ret")
        q.wait_absent("Document to be saved")
        keys("f7","n","y")
        q.wait_absent("Exit WP?")
    guest.stop()
    run(["mcopy", "-i", disk, "::OUT/OFFSET.WP", str(out/"OFFSET.WP")], check=True)
finally:
    guest.stop()
