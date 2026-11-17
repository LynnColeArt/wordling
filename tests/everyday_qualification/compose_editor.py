"""Qualify Compose in the editing canvas, Reveal Codes and native Save/Retrieve."""
from pathlib import Path
import sys

from qualification import F1, REF, Run, native

repo, binary, output = (Path(arg).resolve() for arg in sys.argv[1:])
run = Run(repo, binary, output, classic_canvas=True)
reference = repo / REF / "compose-body-dos/exports/COMPOSE.WP"
reveal = b"\x1b[1;3R"

try:
    run.launch()
    run.step(b"\x16", "Ctrl+V Compose", "Key =", 24)
    run.step(b"\x1b", "cancel Compose")
    assert "Key =" not in run.rows()[24]
    run.step(b"\x1b=", "focus the pull-down menu")
    run.step("o", "open Font", "Characters")
    run.step("h", "Font → Characters opens Compose", "Key =", 24)
    run.step("1", "numeric WordPerfect character set")
    run.step(b"\r", "Enter as numeric separator")
    run.step("36", "numeric WordPerfect character number", "Key = 1 36", 24)
    run.step(b"\r", "insert the extended character", "Æ")
    run.step(" X", "position counts one cell per composed glyph", 'Pos 1.3"')
    run.step(reveal, "Alt+F3 Reveal Codes")
    assert sum("Æ X" in row for row in run.rows()) == 2, run.rows()
    run.start_of_document()
    run.wait("[Æ:1,36] X")
    run.save("COMPOSE.WP")
    assert native(run.p.work / "COMPOSE.WP")[2] == native(reference)[2]
    run.step(b"\x1b[13;2~", "switch to the other document")
    run.seed(reference, "DOS.WP")
    run.retrieve("DOS.WP")
    run.wait("Æ X")
    run.step(b"\x1b[3~", "delete the complete native owner")
    run.step(F1, "Undelete preview", "Undelete: 1 Restore")
    run.step("1", "restore the complete native owner", "Æ X")
    run.start_of_document()
    run.step(b"\x1b[2~", "enable Typeover")
    run.step(b"\x00", "Ctrl+2 Compose via legacy terminal Ctrl+Space alias")
    run.step("ea", "reverse-order digraph replaces the extended owner", "æ X")
    run.save("REPLACED.WP", expected_offset=564)
    assert native(run.p.work / "REPLACED.WP")[2] == bytes.fromhex("c02501c02058")
    run.step(b"\x1b[18~", "close the second document", "Save document?")
    run.step("n", "skip repeat save", "Exit doc 2?")
    run.step("y", "return to first document", "Doc 1 Pg")
    run.step(b"\x1b[13;2~", "open a blank document for wrapping")
    run.step("A" * 64, "fill 64 of 65 columns")
    run.step(b"\x00", "start silent Compose at the line margin")
    run.step("AE", "compose one more cell")
    run.step("Z", "wrap the next character", "Z", 2)
    run.save("WRAP.WP")
    wrap_reference = repo / REF / "compose-wrap-dos/exports/WRAP.WP"
    assert native(run.p.work / "WRAP.WP")[2] == native(wrap_reference)[2]
    run.step(b"\x1b[18~", "close the wrap test document", "Save document?")
    run.step("n", "skip repeat save", "Exit doc 2?")
    run.step("y", "return to the first document", "Doc 1 Pg")
    run.exit_application()
except Exception as error:
    run.finish(repr(error), "Main editor Compose")
    raise
else:
    run.finish(None, "Main editor Compose")
