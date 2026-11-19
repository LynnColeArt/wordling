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
        run(["mcopy", "-i", disk, str(path), "::OUT/"+path.name], check=True)
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
            q.wait_for("Dir")
            time.sleep(.6)
            type_text(r"C:\OUT" + chr(92))
            keys("shift-8", "dot", "shift-8", "ret")
            q.wait_for("RICH    .WP")
        def type_text(text):
            for char in text:
                q.type(char)
                time.sleep(.12)
        open_list()
        keys("f7")
        q.wait_for("Doc 1 Pg")
        type_text("Summary target")
        keys("alt-equal", "f", "m")
        q.wait_for("Document Summary")
        keys("2")
        type_text("arbutus")
        keys("ret")
        type_text("birch")
        keys("ret")
        q.wait_for("Selection: 0")
        time.sleep(1)
        keys("3")
        type_text("cedar")
        keys("ret")
        type_text("dogwood")
        keys("ret")
        for key, value in [("4","elm"), ("5","fir"), ("6","ginkgo"), ("7","hawthorn")]:
            keys(key)
            type_text(value)
            keys("ret")
        assert "hawthorn" in snap("summary-filled")
        keys("f7")
        time.sleep(1)
        if "Document Summary" in q.text(out/"summary-after-f7"):
            keys("f7")
        q.wait_until(lambda screen: "Summary target" in screen and "Document Summary" not in screen, "back in editor")
        keys("f10")
        q.wait_until(lambda screen: "Enter filename:" in screen or "Document to be saved:" in screen, "save filename prompt")
        type_text(r"C:\OUT\FIELDS.WP")
        keys("ret")
        q.wait_absent("Document to be saved:")
        q.wait_for("FIELDS.WP")
        time.sleep(1.5)
        open_list()
        for offset, value in enumerate(("arbutus","birch","cedar","dogwood","elm","fir","ginkgo","hawthorn"), start=2):
            keys("9","5","2","5",*(["down"]*offset))
            type_text(value)
            keys("ret","f1")
            snap(value+"-condition")
            keys("1")
            time.sleep(.55)
            screen = snap(value+"-result")
            if "Find: Conditions" in screen:
                time.sleep(3)
            keys("9","6")
            q.wait_for("RICH    .WP")
    guest.stop()
    run(["mcopy", "-i", disk, "::OUT/FIELDS.WP", str(out/"FIELDS.WP")], check=True)
finally:
    guest.stop()
