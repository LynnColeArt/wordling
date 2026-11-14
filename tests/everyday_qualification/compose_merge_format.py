"""Compose inside an overlapping Bold/Underline field split by a page."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile

from merge_authoring import CTRL_F9
from physical_cases import close_doc2
from qualification import ENTER, F2, SWITCH, Run, native

repo, binary, output = (Path(arg).resolve() for arg in sys.argv[1:])
fixture = repo / "docs/research/everyday-contract-2026-11-05/native-merge/wide/overlap-page"
destination_page = os.environ.get("WORDLING_COMPOSE_DESTINATION_PAGE") == "1"
primary = "DESTPRI.WP5" if destination_page else "PRIMARY.WP5"
cue = "PlainEnd]" if destination_page else "55=[ATail]"
run = Run(repo, binary, output / "linux", classic_canvas=True)
try:
    run.seed(fixture / primary, "PRIMARY.WP5")
    run.seed(fixture / "SECOND.WP5", "SECOND.WP5")
    run.launch()
    run.set_fast_save(False)
    run.step(SWITCH, "open secondary screen", "Doc 2 Pg")
    run.retrieve("SECOND.WP5")
    run.step(F2, "find the beginning of the overlap", "Srch:")
    run.step("A alpha", "enter search query")
    run.step(F2, "find the match")
    for distance, pair, glyph, identity in (
        (0, "AE", "Æ", "1,36"),
        (70, "'e", "é", "1,41"),
    ):
        for _ in range(distance):
            run.step(b"\x1b[C", "move through the field across the page break")
        run.step(b"\x16", "start Compose", "Key =")
        run.step(pair, "insert composed character", glyph)
        run.step(b"\x1b[1;3R", "open Reveal Codes")
        run.step(b"\x1b[D", "select composed character", f"[{glyph}:{identity}]")
        run.step(b"\x1b[C", "leave the composed character")
        run.step(b"\x1b[1;3R", "close Reveal Codes")
    run.save("EDITED.WP5")
    edited = native(run.p.work / "EDITED.WP5")[2]
    bold_on, under_on = bytes.fromhex("c30cc3"), bytes.fromhex("c30ec3")
    bold_off, under_off = bytes.fromhex("c40cc4"), bytes.fromhex("c40ec4")
    ae, acute = bytes.fromhex("c02401c0"), bytes.fromhex("c02901c0")
    overlap = edited[edited.index(under_on) + len(under_on):edited.index(bold_off)]
    page = overlap.index(bytes.fromhex("d4001c"))
    assert overlap.index(ae) < page < overlap.index(acute), overlap.hex()
    close_doc2(run)
    run.step(SWITCH, "open blank merge destination", "Doc 2 Pg")
    run.set_fast_save(True)
    run.step(CTRL_F9, "open Merge", "1 Merge; 2 Sort")
    run.step("1", "select Merge", "Primary file:")
    run.step("PRIMARY.WP5", "enter the primary")
    run.step(ENTER, "confirm primary", "Secondary file:")
    run.step("EDITED.WP5", "enter Wordling's edited secondary")
    run.step(ENTER, "execute merge", cue)
    run.save("MERGED.WP5", expected_offset=564)
    if destination_page:
        run.start_of_document()
        run.step(F2, "find the plain tail on page two", "Srch:")
        run.step("PlainEnd", "enter search query")
        run.step(F2, "find the tail")
        run.step(" Checked", "edit the merged result", "PlainEnd Checked]")
        run.save("RESAVED.WP5", expected_offset=564)
    close_doc2(run)
    run.exit_application()
except Exception as exc:
    run.finish(repr(exc), "Compose in wrapped and formatted merge fields")
    raise
else:
    run.finish(None, "Compose in wrapped and formatted merge fields")

sys.path.insert(0, str(repo / "scripts/reference"))
import guest
import qmp

def assert_formatted_pages(capture):
    vram = (capture / "vram.bin").read_bytes()
    screen = (capture / "screen.txt").read_text()
    rows = 11 if "Press Reveal Codes" in screen else 24
    glyph_rows = []
    for glyph in ("Æ", "é"):
        code = glyph.encode("cp437")[0]
        matches = [i for i in range(0, rows * 160, 2) if vram[i] == code]
        assert len(matches) == 1, (glyph, matches)
        assert vram[matches[0] + 1] == 0x7f, (glyph, vram[matches[0] + 1])
        glyph_rows.append(matches[0] // 160)
    assert glyph_rows[1] == glyph_rows[0] + 2, glyph_rows

dos = output / "dos"
dos.mkdir()
with tempfile.TemporaryDirectory(prefix="wp-compose-merge-") as tmp:
    guest.RUNTIME = qmp.RUNTIME = Path(tmp)
    guest.SOCKET = qmp.SOCKET = Path(tmp) / "qmp.sock"
    private = Path(tmp) / "guest"
    command = guest.start(private)
    guest.stop()
    shutil.copyfile(guest.MASTER / "harddisk.img", private / "harddisk.img")
    disk = str(private / "harddisk.img") + "@@1048576"
    inputs = ["PRIMARY.WP5", "EDITED.WP5"]
    if destination_page:
        inputs.append("RESAVED.WP5")
    for name in inputs:
        subprocess.run(["mcopy", "-i", disk, str(run.p.work / name), "::OUT/" + name], check=True)
    subprocess.run(command, check=True)
    try:
        with qmp.QMP() as q:
            q.wait_for("Doc 1 Pg 1")
            q.key("f3")
            q.wait_for("03/09/92")
            q.capture(dos / "release")
            q.key("ret")
            q.key("ctrl-f9")
            q.wait_for("Merge")
            q.key("1")
            q.wait_for("Primary file:")
            q.type(r"C:\OUT\PRIMARY.WP5")
            q.key("ret")
            q.wait_for("Secondary file:")
            q.type(r"C:\OUT\EDITED.WP5")
            q.key("ret")
            q.wait_for(cue)
            q.capture(dos / "merged")
            if destination_page:
                assert_formatted_pages(dos / "merged")
            q.key("alt-f3")
            q.wait_for("Press Reveal Codes")
            q.capture(dos / "merged-reveal")
            q.key("f10")
            q.wait_for("Document to be saved")
            q.type(r"C:\OUT\MERGED.WP5")
            q.key("ret")
            q.wait_absent("Document to be saved")
            q.capture(dos / "saved")
            if destination_page:
                q.key("f7")
                q.wait_for("Save document?")
                q.key("n")
                q.wait_for("Exit WP?")
                q.key("n")
                q.wait_absent("Exit WP?")
                q.key("shift-f10")
                q.wait_for("Document to be retrieved")
                q.type(r"C:\OUT\RESAVED.WP5")
                q.key("ret")
                q.wait_for("RESAVED.WP5")
                for key in ("home", "home", "down"):
                    q.key(key)
                q.wait_for("PlainEnd Checked]")
                q.capture(dos / "reopened")
                assert_formatted_pages(dos / "reopened")
                if "Press Reveal Codes" not in q.text(guest.RUNTIME / "inspect"):
                    q.key("alt-f3")
                q.wait_for("Press Reveal Codes")
                q.capture(dos / "reopened-reveal")
    finally:
        guest.stop()
    subprocess.run(["mcopy", "-i", disk, "::OUT/MERGED.WP5", str(dos / "MERGED.WP5")], check=True)

result = native(dos / "MERGED.WP5")[2]
assert result == native(run.p.work / "MERGED.WP5")[2], "Wordling and DOS merged bodies differ"
assert result.index(bold_on) < result.index(under_on) < result.index(ae)
assert result.index(ae) < result.index(acute) < result.index(bold_off) < result.index(under_off)
assert cue.encode() in result
if destination_page:
    overlap = result[result.index(under_on) + len(under_on):result.index(bold_off)]
    assert overlap.index(ae) < overlap.index(bytes.fromhex("d4001c")) < overlap.index(acute)

    resaved = native(run.p.work / "RESAVED.WP5")[2]
    assert resaved == result.replace(b"PlainEnd]", b"PlainEnd Checked]", 1)
