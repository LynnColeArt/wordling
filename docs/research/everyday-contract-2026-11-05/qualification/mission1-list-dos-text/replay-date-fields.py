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
        open_list()
        for label, group, offset, value in [
            ("hyphen-from", "5", 0, "03-09-92"),
            ("slash-from", "5", 0, "03/09/92"),
            ("day-before", "5", 0, "03/08/92"),
            ("slash-to", "5", 1, "03/09/92"),
            ("old-from", "5", 0, "01/01/90"),
            ("initial-before", "5", 0, "03-08-92"),
            ("initial-to", "5", 1, "03-09-92"),
            ("future-to", "5", 1, "03-10-92"),
            ("revision-from", "3", 0, "03/09/92"),
            ("revision-to", "3", 1, "03/09/92"),
            ("subject", "5", 6, "Bold"),
        ]:
            keys("9","5","2",group,*(["down"]*offset))
            type_text(value)
            keys("ret","f1")
            snap(label+"-condition")
            keys("1")
            screen = snap(label)
            if "Find: Conditions" in screen:
                keys("f1")
                open_list()
            else:
                keys("9","6")
finally:
    guest.stop()
