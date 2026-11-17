from pathlib import Path
from tempfile import mkdtemp
from subprocess import run
import shutil, time
import guest, qmp
root = Path.cwd()
out = Path(mkdtemp(prefix="mission1-dos-controls-", dir=root/"research/cache"))
shutil.copyfile(__file__, out/"probe.py")
print(out, flush=True)
guest.RUNTIME = qmp.RUNTIME = Path(mkdtemp(prefix="wordling-ctrl-", dir="/tmp"))
guest.SOCKET = qmp.SOCKET = guest.RUNTIME/"qmp.sock"
private = out/"guest"
try:
    command = guest.start(private)
    guest.stop()
    shutil.copyfile(guest.MASTER/"harddisk.img", private/"harddisk.img")
    disk = str(private/"harddisk.img")+"@@1048576"
    source = out/"CTRL.TXT"
    source.write_bytes(b"".join(f"{i:02X}A".encode()+bytes([i])+b"B\r\n" for i in range(0x7f, 0x100))+b"\x1a")
    run(["mcopy", "-i", disk, str(source), "::OUT/CTRL.TXT"], check=True)
    run(command, check=True)
    with qmp.QMP() as q:
        def keys(*parts):
            for key in parts:
                q.key(key)
        def type_text(text):
            for char in text:
                q.type(char)
                time.sleep(.14)
        def snap(label):
            time.sleep(.55)
            screen = q.capture(out/label)
            print(label, " | ".join(row.strip() for row in screen.splitlines() if row.strip()), flush=True)
            return screen
        q.wait_for("Doc 1 Pg", timeout=60)
        keys("ctrl-f5","1","2")
        q.wait_for("Document to be retrieved")
        type_text(r"C:\OUT\CTRL.TXT")
        q.key("ret")
        q.wait_for("7FA")
        snap("imported")
        q.key("alt-f3")
        snap("revealed")
        q.key("f10")
        q.wait_for("Document to be saved:")
        type_text(r"C:\OUT\CTRL.WP")
        q.key("ret")
        q.wait_absent("Document to be saved:")
        q.wait_for("CTRL.WP")
        snap("saved")
        q.key("ctrl-f5")
        keys("1","1")
        q.wait_for("Document to be saved (DOS Text)")
        snap("export-prompt")
        type_text(r"C:\OUT\BACK.TXT")
        q.key("ret")
        q.wait_absent("Document to be saved (DOS Text)")
        snap("after-export")
    guest.stop()
    run(["mcopy", "-i", disk, "::OUT/BACK.TXT", str(out/"BACK.TXT")], check=True)
    run(["mcopy", "-i", disk, "::OUT/CTRL.WP", str(out/"CTRL.WP")], check=True)
    print((out/"BACK.TXT").read_bytes().hex(), flush=True)
finally:
    guest.stop()
