#!/usr/bin/env python3
"""Replay the original line format cases using terminal keys and native saves."""

import sys
from pathlib import Path

from qualification import ENTER, F7, SWITCH, Run, native

SHIFT_F8 = b"\x1b[19;2~"
SHIFT_F4 = b"\x1b[1;2S"
F4 = b"\x1bOS"
SHIFT_TAB = b"\x1b[Z"
SHIFT_F6 = b"\x1b[17;2~"
ALT_F6 = b"\x1b[17;3~"
ALT_F3 = b"\x1b[1;3R"
CTRL_F7 = b"\x1b[18;5~"


def check_save(run, name, directory):
    run.save(name)
    fixture = run.repo / "docs/research/reference-runs" / directory / name
    assert native(run.p.work / name)[2] == native(fixture)[2], name


def close_second_document(run, reveal=False):
    if reveal:
        run.step(ALT_F3, "close Reveal Codes")
    run.step(F7, "close Doc 2", "Save document?")
    run.step("n", "decline another save", "Exit doc 2?")
    run.step("y", "confirm Doc 2 close", "Doc 1 Pg")


def exercise(run):
    run.launch()
    run.set_fast_save(False)
    run.step("before", "type the first paragraph")
    run.step(ENTER, "start the second paragraph")
    run.step(SHIFT_F8, "open Format", "Format:")
    run.step("1", "open Line Format", "Format: Line")
    run.step("7", "edit the margins", "Selection: 7")
    for key in ('2"', ENTER, '1.5"', ENTER, F7):
        run.step(key, "set the left and right margins")
    run.step("after " + "word " * 14, "wrap at the new margin", "          after")
    run.step(ALT_F3, "show margin code", '[L/R Mar:2",1.5"]')
    check_save(run, "MARGINS.WP", "mission1-line-margins")
    run.step(ALT_F3, "close Reveal Codes before switching documents")

    run.step(SWITCH, "open Doc 2", "Doc 2 Pg")
    run.step(SHIFT_F6, "start centering")
    run.step("Heading", "type the centered heading", "                             Heading")
    run.wait('Pos 4.6"')
    for key in (ENTER, "Body", ENTER, ALT_F6, "RIGHT", ENTER, "Second", ENTER):
        run.step(key, "finish the centered and flush-right lines")
    run.wait(" " * 60 + "RIGHT")
    run.step("x " + "a" * 58 + " alpha", "start the last paragraph")
    run.step(b"\x1bOH", "start the Home prefix")
    run.step(" ", "insert the hard space")
    run.step("beta", "wrap after hard space")
    check_save(run, "LINEFMT.WP", "mission1-line-format")
    close_second_document(run)

    run.step(SWITCH, "open a fresh Doc 2", "Doc 2 Pg")
    for key in ("before ", SHIFT_F6, "Heading", SHIFT_F8, "4", "9", " tail"):
        run.step(key, "center a span and append text on the same line")
    run.step(ALT_F3, "show the inline alignment terminator", "[Center]Heading[End C/A] tail")
    check_save(run, "CENTEND.WP", "mission1-line-format")
    close_second_document(run, reveal=True)

    run.step(SWITCH, "open a fresh Doc 2", "Doc 2 Pg")
    for key in ("first page", b"\x1b[13;5u", SHIFT_F8, "2", "5"):
        run.step(key, "open the margin controls at the next page")
    run.wait("Selection: 5")
    for key in ('2"', ENTER, '1.25"', ENTER, F7, "second page", ENTER, "next line"):
        run.step(key, "set top and bottom margins and type the two lines")
    run.wait('Pg 2 Ln 2.17"')
    run.step(ALT_F3, "show the native page margin code", '[T/B Mar:2",1.25"]')
    check_save(run, "PAGEMAR.WP", "mission1-page-margins")
    close_second_document(run, reveal=True)

    run.step(SWITCH, "open a fresh Doc 2", "Doc 2 Pg")
    for key in ("before", ENTER, SHIFT_F8, "1", "6"):
        run.step(key, "open line spacing on the second paragraph")
    run.wait("Selection: 6")
    for key in ("2", ENTER, F7, "second", ENTER, "third"):
        run.step(key, "type two lines at double spacing")
    run.wait('Ln 1.5"')
    for key in (ENTER, SHIFT_F8, "1", "6", "1", ENTER, F7, "fourth", ENTER, "fifth"):
        run.step(key, "restore single spacing for subsequent lines")
    check_save(run, "SPACING.WP", "mission1-line-spacing")
    close_second_document(run)

    run.step(SWITCH, "open a fresh Doc 2", "Doc 2 Pg")
    for key in ("before", ENTER, SHIFT_F8, "1", "4", "2"):
        run.step(key, "open Fixed Line Height")
    run.wait("1 Auto; 2 Fixed: 2")
    for key in ('0.2"', ENTER, F7, "higher", ENTER, "next line"):
        run.step(key, "set and use a fixed 0.2-inch baseline increment")
    run.wait('Ln 1.37"')
    check_save(run, "HEIGHT.WP", "mission1-line-spacing")
    close_second_document(run)

    run.step(SWITCH, "open a fresh Doc 2", "Doc 2 Pg")
    run.step("Sentence", "type before the first note")
    run.step(CTRL_F7, "open the notes menu", "1 Footnote; 2 Endnote")
    run.step("1", "select Footnote", "Footnote: 1 Create")
    run.step("1", "open the note editor", "Footnote:  Press Exit when done")
    run.step("Footnote text", "write the footnote")
    run.step(F7, "return to the reference", "Sentence1")
    run.step(" then", "type before the endnote")
    run.step(CTRL_F7, "open the notes menu", "1 Footnote; 2 Endnote")
    run.step("2", "select Endnote", "Endnote: 1 Create")
    run.step("1", "open the endnote editor", "Endnote:  Press Exit when done")
    run.step("Endnote text", "write the endnote")
    run.step(F7, "return to the reference", "Sentence1 then1")
    run.step(" end", "finish the document")
    check_save(run, "NOTES.WP", "mission1-notes")
    close_second_document(run)

    run.step(SWITCH, "open a fresh Doc 2", "Doc 2 Pg")
    for key in (SHIFT_F8, "2", "3", "1", "2", "My Header", F7, F7):
        run.step(key, "set Header A for every page")
    for key in (SHIFT_F8, "2", "4", "2", "4", "Even Footer", F7, F7):
        run.step(key, "set Footer B for even pages")
    for key in ("First page", b"\x1b[13;5u", "Second page", b"\x1b[13;5u", "Third page"):
        run.step(key, "write a three-page document with running text")
    run.wait('Pg 3 Ln 1.33"')
    check_save(run, "HEADFOOT.WP", "mission1-headers")
    close_second_document(run)

    run.step(SWITCH, "open a fresh Doc 2", "Doc 2 Pg")
    run.step(SHIFT_F4, "indent both sides")
    run.step("double " + "word " * 15, "wrap within the double indent", "     double ")
    run.step(ENTER, "return to the ordinary margins")
    run.step(F4, "indent the next paragraph")
    run.step(SHIFT_TAB, "release the first line to the margin")
    run.step("hanging " + "word " * 15, "wrap within the hanging indent")
    run.step(ENTER, "return to the ordinary margins")
    run.step("normal", "type an unindented final line")
    check_save(run, "INDENTS.WP", "mission1-indents")
    close_second_document(run)

    run.step(SWITCH, "open a fresh Doc 2", "Doc 2 Pg")
    for key in (SHIFT_F8, "2", "5", '2"', ENTER, '7"', ENTER, F7):
        run.step(key, "shorten the page for the conditional break")
    for row in range(1, 9):
        run.step(f"row {row}", "fill the preceding lines")
        run.step(ENTER, "start the next line")
    for key in ("first", ENTER, "second", SHIFT_F8, "4"):
        run.step(key, "open Format Other near the bottom of the page")
    run.step("2", "open Conditional End of Page", "Number of Lines to Keep Together")
    for key in ("3", ENTER, F7, ENTER, "Heading", ENTER, "first protected", ENTER, "second protected"):
        run.step(key, "keep the heading and both lines together")
    run.wait("Pg 2")
    check_save(run, "SHORT.WP", "mission1-conditional-page")
    close_second_document(run)

    run.step(SWITCH, "open a fresh Doc 2", "Doc 2 Pg")
    for key in (SHIFT_F8, "2", "5", '2"', ENTER, '7"', ENTER, F7):
        run.step(key, "shorten the page for the widow test")
    for _ in range(10):
        run.step("row", "fill a line before the protected paragraph")
        run.step(ENTER, "start the next line")
    for key in (SHIFT_F8, "1"):
        run.step(key, "open Line Format")
    run.step("9", "open Widow/Orphan Protection", "No (Yes)")
    run.step("y", "enable widow and orphan protection")
    run.step(F7, "return to the document")
    run.step("test " + "word " * 36, "wrap across the page bottom")
    run.step(ENTER, "close the paragraph and move the preceding line")
    run.step("after", "type the next paragraph")
    check_save(run, "WIDOW.WP", "mission1-widow-protection")
    close_second_document(run)
    run.exit_application()


if __name__ == "__main__":
    repo, binary, out = (Path(arg).resolve() for arg in sys.argv[1:])
    run = Run(repo, binary, out, classic_canvas=True)
    failure = None
    try:
        exercise(run)
    except Exception as error:
        failure = repr(error)
        raise
    finally:
        run.finish(failure, "DOS margins, alignment, spacing, running text, notes and indents")
