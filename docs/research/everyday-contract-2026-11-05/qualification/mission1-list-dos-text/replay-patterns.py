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
    for name, body in {"RICH.TXT":"amber jade", "Z.TXT":"amber slate", "BLUE.TXT":"jade dark", "FOUR-WAY.TXT":"four-way wayward", "PHRASE.TXT":"replace diskette", "EXACT.TXT":"replace disk", "BETWEEN.TXT":"replace the B diskette"}.items():
        data = out/name
        data.write_bytes(body.encode()+b"\x1a")
        run(["mcopy", "-i", disk, str(data), "::OUT/"+name], check=True)
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
            q.wait_for("N Name Search")
        def type_text(text):
            for char in text:
                q.type(char)
                time.sleep(.12)
        open_list()
        for label, scope, value in [
            ("asterisk", "4", "am*er"), ("question", "4", "j?de"),
            ("and", "4", "amber jade"), ("or", "4", "jade,slate"),
            ("not", "4", "amber-slate"), ("exclude", "4", "-amber"),
            ("phrase", "4", '"replace disk"'), ("exact-phrase", "4", '"replace disk "'),
            ("phrase-wildcard", "4", '"replace*disk"'), ("quoted-hyphen","4",'"four-way"'),
            ("filename-wild","1","?ich"), ("filename-quote","1",'"four-way"'),
            ("filename-dot","1","ich.txt")]:
            keys("9",scope)
            for c in value:
                if c in "*?":
                    keys("shift-8" if c=="*" else "shift-slash")
                else:
                    type_text(c)
            keys("ret")
            time.sleep(3)
            snap(label)
            keys("9","6")
            q.wait_for("N Name Search")
finally:
    guest.stop()
