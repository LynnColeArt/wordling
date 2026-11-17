from pathlib import Path
from tempfile import mkdtemp
from subprocess import run
import shutil, time
import guest, qmp
root = Path.cwd()
out = Path(mkdtemp(prefix="mission1-find-", dir=root/"research/cache"))
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
    source = root/"docs/research/everyday-contract-2026-11-05/qualification/dos-list-conditions-results/exports"
    for path in sorted(source.glob("*.WP")):
        run(["mcopy", "-m", "-i", disk, str(path), "::OUT/"+path.name], check=True)
    blue = source.parent.parent/"dos-find-export-acceptance"/"exports"/"BLUE.WP"
    run(["mcopy", "-i", disk, str(blue), "::OUT/BLUE.WP"], check=True)
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
        def open_list():
            keys("f5")
            type_text(r"C:\OUT" + chr(92))
            keys("shift-8", "dot", "shift-8", "ret")
            q.wait_for("RICH    .WP")
        def type_text(text):
            for char in text:
                q.type(char)
                time.sleep(.12)
        keys("shift-f7")
        q.wait_for("Full Document")
        keys("s","3","2","8")
        q.wait_for("Device or Filename")
        type_text(r"C:\OUT\LIST.PRN")
        keys("ret","f7","f7","f7")
        q.wait_for("Doc 1 Pg")
        keys("shift-f7","3")
        snap("filename-prompt")
        type_text(r"C:\OUT\Z.WP")
        keys("ret")
        snap("page-prompt")
        keys("ret")
        time.sleep(3)
        snap("settled")
    guest.stop()
    run(["mcopy", "-i", disk, "::OUT/LIST.PRN", str(out/"LIST.PRN")], check=True)
finally:
    guest.stop()
