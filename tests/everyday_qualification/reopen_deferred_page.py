"""Reopen the DOS deferred-page save, edit page two, and compare native output."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from qualification import REF, Run

repo, binary, output = (Path(arg).resolve() for arg in sys.argv[1:])
fixtures = repo / REF / "reopen-deferred-dos/exports"
run = Run(repo, binary, output, classic_canvas=True)
try:
    run.seed(fixtures / "SOURCE.WP", "SOURCE.WP")
    run.launch()
    run.retrieve("SOURCE.WP")
    assert run.save("COPY.WP", expected_offset=564) == (fixtures / "SOURCE.WP").read_bytes()
    for key in (b"\x1bOH", b"\x1bOH", b"\x1b[B", b"\x1b[D"):
        run.step(key, "move to the end of page two")
    run.step(" OK", "edit the reopened document", "PlainEnd Checked OK]")
    run.save("EDIT.WP", expected_offset=564)
    assert (run.p.work / "EDIT.WP").read_bytes() == (fixtures / "EDIT.WP").read_bytes()
    run.exit_application()
except Exception as exc:
    run.finish(repr(exc), "Reopen deferred soft page")
    raise
else:
    run.finish(None, "Reopen deferred soft page")

sys.path.insert(0, str(repo / "scripts/reference"))
import guest
import qmp

with tempfile.TemporaryDirectory(prefix="wp-deferred-") as tmp:
    guest.RUNTIME = qmp.RUNTIME = Path(tmp)
    guest.SOCKET = qmp.SOCKET = Path(tmp) / "qmp.sock"
    private = Path(tmp) / "guest"
    command = guest.start(private)
    guest.stop()
    shutil.copyfile(guest.MASTER / "harddisk.img", private / "harddisk.img")
    disk = str(private / "harddisk.img") + "@@1048576"
    subprocess.run(["mcopy", "-i", disk, str(run.p.work / "EDIT.WP"), "::OUT/EDIT.WP"], check=True)
    subprocess.run(command, check=True)
    try:
        with qmp.QMP() as q:
            q.wait_for("Doc 1 Pg 1")
            q.key("f3")
            q.wait_for("03/09/92")
            q.key("ret")
            q.key("shift-f10")
            q.wait_for("Document to be retrieved")
            q.type(r"C:\OUT\EDIT.WP")
            q.key("ret")
            q.wait_for("EDIT.WP")
            for key in ("home", "home", "down"):
                q.key(key)
            q.wait_for("PlainEnd Checked OK]")
            q.capture(output / "dos-reopened")
            raw = (output / "dos-reopened/vram.bin").read_bytes()
            rows = []
            for glyph in "Æé":
                offset = raw[:24 * 160:2].index(glyph.encode("cp437"))
                assert raw[offset * 2 + 1] == 0x7F
                rows.append(offset // 80)
            assert rows[1] == rows[0] + 2
    finally:
        guest.stop()
