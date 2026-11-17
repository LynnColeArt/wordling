"""Replace one attribute across a page and compare against the DOS editor."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from qualification import F2, F6, F8, Run, native

repo, binary, source, output = (Path(arg).resolve() for arg in sys.argv[1:])
output.mkdir()
sys.path.insert(0, str(repo / "scripts/reference"))
import guest
import qmp

for name, key, dos_key, removed, style in (
    ("NOBOLD", F6, "f6", ("c30cc3", "c40cc4"), 0x71),
    ("NOUNDER", F8, "f8", ("c30ec3", "c40ec4"), 0x1F),
):
    folder = output / name
    run = Run(repo, binary, folder, classic_canvas=True)
    try:
        run.seed(source, "SOURCE.WP")
        run.launch()
        run.set_fast_save(False)
        run.retrieve("SOURCE.WP")
        run.step(b"\x1b=", "focus menu bar")
        run.step("s", "open Search", "Replace")
        run.step("r", "select Replace", "w/Confirm?")
        run.step("n", "replace all", "Srch:")
        run.step(key, "search for opening code")
        run.step(F2, "advance to empty replacement", "Replace with:")
        run.step(F2, "remove the matched pair")
        run.save("OUTPUT.WP")
        run.exit_application()
    except Exception as exc:
        run.finish(repr(exc), name)
        raise
    else:
        run.finish(None, name)

    product = run.p.work / "OUTPUT.WP"
    expected = native(source)[2]
    for owner in removed:
        expected = expected.replace(bytes.fromhex(owner), b"", 1)
    assert native(product)[2] == expected

    with tempfile.TemporaryDirectory(prefix="wp-replace-") as temp:
        guest.RUNTIME = qmp.RUNTIME = Path(temp)
        guest.SOCKET = qmp.SOCKET = Path(temp) / "qmp.sock"
        private = Path(temp) / "guest"
        command = guest.start(private)
        guest.stop()
        shutil.copyfile(guest.MASTER / "harddisk.img", private / "harddisk.img")
        disk = str(private / "harddisk.img") + "@@1048576"
        for path, filename in ((source, "SOURCE.WP"), (product, "OUTPUT.WP")):
            subprocess.run(["mcopy", "-i", disk, str(path), "::OUT/" + filename], check=True)
        subprocess.run(command, check=True)
        try:
            with qmp.QMP() as q:
                def retrieve(filename):
                    q.key("shift-f10")
                    q.wait_for("Document to be retrieved")
                    q.type("C:\\OUT\\" + filename)
                    q.key("ret")
                    q.wait_for(filename)

                q.wait_for("Doc 1 Pg 1")
                q.key("f3")
                q.wait_for("03/09/92")
                q.key("ret")
                retrieve("SOURCE.WP")
                q.key("alt-f2")
                q.wait_for("w/Confirm?")
                for chord in ("n", dos_key, "f2", "f2"):
                    q.key(chord)
                q.wait_absent("Replace with:")
                q.key("f10")
                q.wait_for("Document to be saved")
                q.type(r"C:\OUT\DOS.WP")
                q.key("ret")
                q.wait_absent("Document to be saved")
                q.capture(folder / "dos-replaced")
                q.key("f7")
                q.wait_for("Save document?")
                q.key("n")
                q.wait_for("Exit WP?")
                q.key("n")
                q.wait_absent("Exit WP?")
                retrieve("OUTPUT.WP")
                for chord in ("home", "home", "down"):
                    q.key(chord)
                q.wait_for("PlainEnd Checked]")
                q.capture(folder / "dos-reopened")
                vram = (folder / "dos-reopened/vram.bin").read_bytes()
                screen = (folder / "dos-reopened/screen.txt").read_text()
                rows = 11 if "Press Reveal Codes" in screen else 24
                glyph_rows = []
                for glyph in ("Æ", "é"):
                    code = glyph.encode("cp437")[0]
                    cells = [i for i in range(0, rows * 160, 2) if vram[i] == code]
                    assert len(cells) == 1 and vram[cells[0] + 1] == style, (name, glyph, cells)
                    glyph_rows.append(cells[0] // 160)
                assert glyph_rows[1] == glyph_rows[0] + 2, glyph_rows
        finally:
            guest.stop()
        returned = folder / "DOS.WP"
        subprocess.run(["mcopy", "-i", disk, "::OUT/DOS.WP", str(returned)], check=True)
        assert native(returned)[2] == native(product)[2], name
