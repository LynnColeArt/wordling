from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
import shutil, sys
import guest, qmp

source, out = (Path(arg).resolve() for arg in sys.argv[1:])
out.mkdir()
with TemporaryDirectory(prefix="wp-compare-reopen-") as runtime:
    guest.RUNTIME = qmp.RUNTIME = Path(runtime)
    guest.SOCKET = qmp.SOCKET = guest.RUNTIME / "qmp.sock"
    try:
        private = out / "guest"
        command = guest.start(private)
        guest.stop()
        shutil.copyfile(guest.MASTER / "harddisk.img", private / "harddisk.img")
        disk = str(private / "harddisk.img") + "@@1048576"
        run(["mcopy", "-i", disk, str(source), "::OUT/COMPARE.WP"], check=True)
        run(command, check=True)
        with qmp.QMP() as q:
            q.wait_for("Doc 1 Pg", timeout=60)
            q.key("shift-f10")
            q.wait_for("Document to be retrieved")
            q.type(r"C:\OUT\COMPARE.WP")
            q.wait_for("COMPARE.WP")
            q.key("ret")
            q.wait_for("Alpha new tailAlpha old tail")
            q.key("alt-f3")
            q.wait_for("[REDLN]Alpha new tail[redln][STKOUT]Alpha old tail[stkout]")
            q.capture(out / "compare")
            q.key("alt-f3")
            q.key("f7")
            q.wait_for("Save document?")
            q.key("n")
            q.wait_for("Exit WP?")
            q.key("y")
            q.wait_absent("Exit WP?")
    finally:
        guest.stop()
