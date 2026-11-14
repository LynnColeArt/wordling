"""Exercise native Document Summary through File and ordinary Save/Retrieve."""
from pathlib import Path
import struct
import sys

from qualification import F1, F7, Run, native

repo, binary, output = (Path(arg).resolve() for arg in sys.argv[1:])
run = Run(repo, binary, output, classic_canvas=True)
fixture = repo / "docs/research/everyday-contract-2026-11-05/qualification/mission1-summary-edit/exports/SUMMARY.WP"

def summary_packet(raw):
    for index in range(26, 66, 10):
        kind, length, offset = struct.unpack_from("<HII", raw, index)
        if kind == 1:
            return raw[offset:offset + length]
    raise AssertionError("missing native Summary packet")

def open_summary():
    run.step(b"\x1b=", "focus menu")
    run.step("f", "open File", "Summary")
    run.step("m", "open Summary", "Document Summary", 0)

try:
    run.seed(fixture, "DOS.WP")
    run.launch()
    reference = fixture.parents[2]
    fast = reference / "mission1-summary-fast/exports"
    run.seed(fast / "FIRST.WP", "FAST.WP")
    run.retrieve("FAST.WP")
    run.step(" edit", "edit loaded summary document")
    saved = run.save("FASTOUT.WP", expected_offset=704)
    expected = (fast / "THIRD.WP").read_bytes()
    assert saved == expected
    run.step(b"\x1b[13;2~", "open second document", "Doc 2 Pg")
    run.set_fast_save(False)
    run.retrieve("DOS.WP")
    open_summary()
    run.wait("ORIGINAL SUBJECT")
    run.step("4", "edit subject", "Selection: 4")
    run.step(" CANCELLED", "type a discarded edit")
    run.step(F1, "cancel field", "Selection: 0")
    assert "CANCELLED" not in "\n".join(run.rows())
    run.step("4", "edit subject")
    run.step(" DISCARDED", "change the draft")
    run.step(b"\r", "accept field inside the form")
    run.step(F1, "discard the whole form", "Doc 2 Pg")
    open_summary()
    assert "DISCARDED" not in "\n".join(run.rows())
    run.step("4", "edit subject")
    run.step(" UPDATED", "append to subject")
    run.step(b"\r", "accept field", "ORIGINAL SUBJECT UPDATED")
    run.step(F7, "commit summary", "Doc 2 Pg")
    output_bytes = run.save("UPDATED.WP", expected_offset=481)
    assert b"ORIGINAL SUBJECT UPDATED\0" in output_bytes
    assert native(run.p.work / "UPDATED.WP")[2] == native(fixture)[2]
    open_summary()
    run.step(b"\x1b[3~", "remove summary", "Delete Document Summary?")
    run.step("y", "confirm removal", "Doc 2 Pg")
    removed = run.save("REMOVED.WP")
    assert b"ORIGINAL SUBJECT" not in removed
    run.step(F7, "close updated document", "Save document?")
    run.step("n", "skip save", "Exit doc 2?")
    run.step("y", "return to first document", "Doc 1 Pg")
    run.step(b"\x1b[13;2~", "switch to a new document", "Doc 2 Pg")
    run.step("NEW BODY", "type a fresh document")
    open_summary()
    run.step("4", "create subject")
    run.step("NEW SUBJECT", "type subject")
    run.step(b"\r", "accept subject")
    run.step("3", "open Author and Typist")
    run.step("ANN", "enter author")
    run.step(b"\r", "accept author")
    run.step("BOB", "enter typist")
    run.step(b"\r", "accept typist")
    run.step(F7, "commit summary")
    created = run.save("CREATED.WP", expected_offset=474)
    assert b"NEW SUBJECT\0" in created
    assert native(run.p.work / "CREATED.WP")[2] == b"NEW BODY"
    open_summary()
    run.wait("NEW SUBJECT")
    run.step(F1, "close form")
    run.step(F7, "close second document", "Save document?")
    run.step("n", "skip save", "Exit doc 2?")
    run.step("y", "return to first document", "Doc 1 Pg")
    run.step(b"\x1b[13;2~", "open a fresh capture document", "Doc 2 Pg")
    run.step("RE: Budget", "type subject heading")
    run.step(b"\r", "insert hard return")
    run.step("The project starts today.", "type abstract text")
    open_summary()
    run.step(b"\x1b[21;2~", "request capture", "Capture Document Summary Fields?")
    run.step(b"\r", "decline capture", "Selection: 0")
    run.step(b"\x1b[21;2~", "request capture again", "Capture Document Summary Fields?")
    run.step("y", "capture body text", "RE: Budget; The project starts today.")
    run.step("1", "edit date", "Selection: 1")
    run.step(b"\x1b[H", "go to start of date")
    for _ in "07-04-01 02:35p":
        run.step(b"\x1b[3~", "delete the next date character")
    run.step("7/4/2001 2:35p", "enter DOS date")
    run.step(b"\r", "apply date", "07-04-01 02:35p")
    run.step(F7, "commit captured summary")
    captured = run.save("CAPTURE.WP", expected_offset=506)
    assert b"Budget\0ANN\0BOB\0RE: Budget; The project starts today.\0" in captured
    dos_capture = summary_packet((reference / "mission1-summary-names/exports/CAPTURE.WP").read_bytes())
    dos_date = summary_packet((reference / "mission1-summary-date/exports/DATE.WP").read_bytes())
    assert summary_packet(captured) == dos_date[:26] + dos_capture[26:-12] + dos_date[-12:]
    run.step(F7, "close capture document", "Save document?")
    run.step("n", "skip save", "Exit doc 2?")
    run.step("y", "return to first document", "Doc 1 Pg")
    run.step(b"\x1b[13;2~", "open a fresh rich summary document", "Doc 2 Pg")
    run.step("Rich summary", "type DOS fixture body")
    open_summary()
    run.step("4", "open Subject")
    run.step(b"\x1b[17~", "start Bold")
    run.step("Bold", "enter bold text")
    run.step(b"\x1b[17~", "end Bold")
    run.step(" ", "separate the runs")
    run.step(b"\x1b[19~", "start Underline")
    run.step("Underline", "enter underlined text")
    run.step(b"\x1b[19~", "end Underline")
    run.step(b"\r", "accept formatted subject")
    row = run.rows()[12]
    bold_at, underline_at = row.index("Bold"), row.index("Underline")
    assert run.p.terminal.styles[12][bold_at] != run.p.terminal.styles[12][underline_at]
    run.step(F7, "commit formatted summary")
    rich_reference = (reference / "mission1-summary-rich/exports/RICH.WP").read_bytes()
    rich = run.save("RICH.WP", expected_offset=int.from_bytes(rich_reference[4:8], "little"))
    assert summary_packet(rich)[26:-12] == summary_packet(rich_reference)[26:-12]
    run.step(F7, "close rich summary document", "Save document?")
    run.step("n", "skip save", "Exit doc 2?")
    run.step("y", "return to first document", "Doc 1 Pg")
    run.step(b"\x1b[13;2~", "open Compose document", "Doc 2 Pg")
    run.step("Compose", "type DOS fixture body")
    open_summary()
    run.step("4", "open Subject")
    run.step(b"\x00", "Ctrl+2 Compose")
    run.step("1,36", "enter the native character identity")
    run.step(b"\r", "insert ligature", "Æ")
    for pair in ("ae", "ss", "co", "ro", "tm", "ox", "ao"):
        run.step(" ", "separate composed characters")
        run.step(b"\x00", "start digraph Compose")
        run.step(pair, "enter digraph")
    dos_display = (reference / "summary-digraph-dos/glyphs/screen.txt").read_text().splitlines()[12]
    observed_glyphs = " ".join(dos_display.split()[3:11])
    assert run.rows()[12][23:].strip() == observed_glyphs
    run.step(b"\r", "accept composed field")
    run.step(F7, "commit composed summary")
    dos_compose = (reference / "mission1-summary-compose/exports/COMPOSE.WP").read_bytes()
    composed = run.save("COMPOSE.WP", expected_offset=int.from_bytes(dos_compose[4:8], "little") + 35)
    dos_digraph = (reference / "summary-digraph-dos/exports/DIGRAPH.WP").read_bytes()
    observed_field = summary_packet(dos_digraph)[115:115 + 8 * 4 + 7]
    assert summary_packet(composed)[115:-12] == observed_field + b"\0" * 6
    run.step(F7, "close Compose document", "Save document?")
    run.step("n", "skip save", "Exit doc 2?")
    run.step("y", "return to first document", "Doc 1 Pg")
    run.step(b"\x1b[13;2~", "open a fresh diacritics document", "Doc 2 Pg")
    run.step("Diacritics", "type the DOS fixture body")
    open_summary()
    run.step("4", "open Subject")
    pairs = ("'e", "'E", "'a", "'i", "'o", "'u", '"u', '"U', '"a', '"o',
             "~n", "~N", ",c", ",C", "@a", "@A", "^a", "^e", "^i", "^o", "^u",
             "`a", "`e", "`i", "`o", "`u")
    for index, pair in enumerate(pairs):
        run.step(b"\x00", "start Compose")
        run.step(pair[::-1] if index % 2 else pair, "compose with either key order")
        if index != len(pairs) - 1:
            run.step(" ", "separate diacritics")
    accent_dos = reference / "summary-accent-dos"
    dos_row = (accent_dos / "glyphs/screen.txt").read_text().splitlines()[12]
    assert run.rows()[12][23:].strip() == dos_row[23:].strip()
    run.step(b"\r", "accept accented Subject")
    run.step(F7, "commit Summary")
    accent = run.save("ACCENT.WP", expected_offset=324 + 133 + 4 * len(pairs) + len(pairs) - 1)
    dos_packet = summary_packet((accent_dos / "exports/ACCENT.WP").read_bytes())
    native_subject = dos_packet[115:115 + 5 * len(pairs) - 1]
    assert summary_packet(accent)[115:-12] == native_subject + b"\0" * 6
    run.step(F7, "close diacritics document", "Save document?")
    run.step("n", "skip save", "Exit doc 2?")
    run.step("y", "return to first document", "Doc 1 Pg")
    run.exit_application()
except Exception as error:
    run.finish(repr(error), "Document Summary")
    raise
else:
    run.finish(None, "Document Summary")
