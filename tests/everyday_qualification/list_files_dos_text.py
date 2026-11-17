#!/usr/bin/env python3
"""Replay original-backed List Files search, print and DOS text conversion."""

import sys
from pathlib import Path

from qualification import ENTER, F5, F7, REF, Run, native

TEXT_IN_OUT = b"\x1b[15;5~"
SHIFT_F7 = b"\x1b[18;2~"
DOWN = b"\x1b[B"


def exercise(run):
    fixture = run.repo / REF / "mission1-list-dos-text"
    run.seed(fixture / "CTRL.TXT", "CTRL.TXT")
    run.seed(fixture / "FIELDS.WP", "FIELDS.WP")
    run.seed(run.repo / REF / "dos-list-conditions-results/exports/Z.WP", "Z.WP")
    run.launch()
    run.step(F5, "list files", "Dir C:")
    run.step(ENTER, "show directory", "Name Search")
    run.step("9", "open Find", "Conditions")
    run.step("5", "open Conditions", "Find: Conditions")
    run.step("5", "edit Summary conditions")
    for _ in range(6):
        run.step(DOWN, "move to the Summary Subject")
    run.step("elm", "enter the original fixture subject")
    run.step(ENTER, "accept the subject criterion")
    run.step("1", "filter by Subject", "FIELDS")
    assert "Z       .WP" not in "\n".join(run.rows())
    run.step("9", "open Find")
    run.step("6", "undo the filter", "Z       .WP")
    run.step(F7, "return to editing")
    run.step(SHIFT_F7, "open Print", "Full Document")
    for key, cue in (
        ("s", "Select Printer"), ("3", "STANPRIN.PRS"), ("2", "8 Other"),
        ("8", "Device or Filename"), ("PRINT.PRN", "PRINT.PRN"),
        (ENTER, "PRINT.PRN"), (F7, "Full Document"),
    ):
        run.step(key, "set the Standard Printer disk port", cue)
    run.step("3", "print document on disk", "Document name:")
    run.step("Z.WP", "select the original two-page document")
    run.step(ENTER, "open the page prompt", "Page(s): (All)")
    run.step("2", "select page two")
    run.step(ENTER, "print the selected page")
    output = run.p.work / "PRINT.PRN"
    run.until(output.is_file, "printer output exists")
    assert output.read_bytes() == (fixture / "PAGE2.PRN").read_bytes()
    run.step(F7, "close Print")
    run.set_fast_save(False)
    for key in (TEXT_IN_OUT, "1", "2", "CTRL.TXT", ENTER):
        run.step(key, "retrieve DOS text")
    run.wait("00A^@B")
    run.wait("01A^AB")
    run.save("CONTROL.WP")
    assert native(run.p.work / "CONTROL.WP")[2] == native(fixture / "CTRL.WP")[2]
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
        run.finish(failure, "DOS List Files and text conversion")
