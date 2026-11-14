"""Confirm a replacement spanning a formatted automatic page break."""
from pathlib import Path
import sys

from qualification import F2, REF, Run, native

repo, binary, output = (Path(arg).resolve() for arg in sys.argv[1:4])
backward = "--backward" in sys.argv[4:]
cancel = "--cancel" in sys.argv[4:]
revisit = "--revisit" in sys.argv[4:]
reference = "replace-backward-accept-dos" if backward else "replace-cross-page-dos"
if cancel:
    reference = "backward-save-cancel"
elif revisit:
    reference = "backward-save-end"
fixtures = repo / REF / reference / "exports"
run = Run(repo, binary, output, classic_canvas=True)
try:
    run.seed(fixtures / "SOURCE.WP", "SOURCE.WP")
    run.launch()
    run.retrieve("SOURCE.WP")
    if backward:
        for key in (b"\x1bOH", b"\x1bOH", b"\x1b[B"):
            run.step(key, "move to document end")
    run.step(b"\x1b=", "focus the menu bar")
    run.step("s", "open Search", "Replace")
    run.step("r", "select Replace", "w/Confirm?")
    run.step("y", "enable confirmation", "Srch:")
    if backward:
        run.step(b"\x1b[A", "choose backward direction", "<- Srch:")
    run.step("delta A alpha", "enter a match that occurs across the page break")
    run.step(F2, "advance to replacement", "Replace with:")
    run.step("omega Q theta", "enter replacement")
    run.step(F2, "find first match", "Confirm?")
    if backward:
        first_match_x = run.p.terminal.x
        run.step("y", "accept the cross-page match first", "Confirm?")
        assert run.p.terminal.x < first_match_x, "confirmation must resume at the earlier match"
        if cancel:
            run.step(b"\x1bOP", "cancel at the earlier match", "Q theta beta")
        else:
            run.step("n", "skip the earlier match", "Q theta beta")
        if revisit:
            for key in (b"\x1bOH", b"\x1bOH", b"\x1b[B"):
                run.step(key, "revisit page two")
    else:
        run.step("n", "skip the first match", "Confirm?")
        run.step("y", "replace the match across the page break", "Q theta beta")
    run.save("RESULT.WP", expected_offset=564)
    assert native(run.p.work / "RESULT.WP")[2] == native(fixtures / "RESULT.WP")[2]
    if backward and not (cancel or revisit):
        assert (run.p.work / "RESULT.WP").read_bytes() == (fixtures / "RESULT.WP").read_bytes()
    run.exit_application()
except Exception as exc:
    run.finish(repr(exc), "Confirm Replace across an automatic page break")
    raise
else:
    run.finish(None, "Confirm Replace across an automatic page break")

# Reopen the actual Wordling output in a fresh copy of the pinned DOS guest.
import shutil
import subprocess
import tempfile

sys.path.insert(0, str(repo / "scripts/reference"))
import guest
import qmp

with tempfile.TemporaryDirectory(prefix="wp-cross-page-") as temp:
    guest.RUNTIME = qmp.RUNTIME = Path(temp)
    guest.SOCKET = qmp.SOCKET = Path(temp) / "qmp.sock"
    private = Path(temp) / "guest"
    command = guest.start(private)
    guest.stop()
    shutil.copyfile(guest.MASTER / "harddisk.img", private / "harddisk.img")
    disk = str(private / "harddisk.img") + "@@1048576"
    subprocess.run(["mcopy", "-i", disk, str(run.p.work / "RESULT.WP"),
                    "::OUT/RESULT.WP"], check=True)
    subprocess.run(command, check=True)
    try:
        with qmp.QMP() as q:
            q.wait_for("Doc 1 Pg 1")
            q.key("f3")
            q.wait_for("03/09/92")
            q.capture(output / "dos-release")
            q.key("ret")
            q.key("shift-f10")
            q.wait_for("Document to be retrieved")
            q.type(r"C:\OUT\RESULT.WP")
            q.key("ret")
            q.wait_for("RESULT.WP")
            for key in ("home", "home", "down"):
                q.key(key)
            q.wait_for("Q theta beta")
            q.capture(output / "dos-reopened")
            vram = (output / "dos-reopened/vram.bin").read_bytes()
            rows = []
            for text in ("omega", "Q theta", "Æ", "é"):
                cells = vram[0:24 * 160:2]
                offset = cells.index(text.encode("cp437"))
                assert offset // 80 == (offset + len(text) - 1) // 80
                assert all(vram[2 * i + 1] == 0x7F for i in range(offset, offset + len(text))), text
                rows.append(offset // 80)
            assert rows[0] + 2 == rows[1] and rows[:2] == rows[2:], rows
    finally:
        guest.stop()
