"""Reopen Linux worksheet import and link saves in WordPerfect 5.1 DOS."""
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
import shutil
import sys

import guest
import qmp

source, dest = (Path(arg).resolve() for arg in sys.argv[1:3])
if len(sys.argv) > 3:
    guest.MASTER = Path(sys.argv[3]).resolve() / guest.MASTER.relative_to(guest.ROOT)
dest.mkdir()
cases = (
    ("IMPORT", source / "import/files/IMPORT.WP", "7"),
    ("LINK", source / "link/files/LINK.WP", "7"),
    ("UPDATED", source / "fast-refresh/files/UPDATED.WP", "19"),
)
with TemporaryDirectory(prefix="wordling-worksheet-reopen-") as runtime:
    guest.RUNTIME = qmp.RUNTIME = Path(runtime)
    guest.SOCKET = qmp.SOCKET = guest.RUNTIME / "qmp.sock"
    try:
        private = dest / "guest"
        command = guest.start(private)
        guest.stop()
        disk = str(private / "harddisk.img") + "@@1048576"
        for name, file, value in cases:
            shutil.copyfile(guest.MASTER / "harddisk.img", private / "harddisk.img")
            run(["mcopy", "-i", disk, str(file), "::OUT/" + name + ".WP"], check=True)
            run(command, check=True)
            with qmp.QMP() as q:
                q.wait_for("Doc 1 Pg", timeout=60)
                q.key("shift-f10")
                q.wait_for("Document to be retrieved")
                q.type("C:\\OUT\\" + name + ".WP")
                q.key("ret")
                q.wait_for("Amber")
                q.wait_for("│" + value.rjust(8) + " ║")
                screen = q.capture(dest / name)
                if name != "IMPORT":
                    assert r"Link: C:\OUT\RANGE.WK1  A1..B2" in screen
                assert "Outside" not in screen
                print(name, value, flush=True)
                q.key("f7")
                q.wait_for("Save document?")
                q.key("n")
                q.wait_for("Exit WP?")
                q.key("y")
                q.wait_absent("Exit WP?")
            guest.stop()
    finally:
        guest.stop()
