#!/usr/bin/env python3
"""Exercise DOS-backed navigation, deletion and block editing via terminal keys."""

import sys
from pathlib import Path

from qualification import ENTER, F1, F6, F7, SWITCH, Run, native

CTRL_LEFT = b"\x1b[1;5D"
CTRL_RIGHT = b"\x1b[1;5C"
CTRL_DELETE = b"\x1b[3;5~"
CTRL_HOME = b"\x1b[1;5H"
CTRL_PAGE_DOWN = b"\x1b[6;5~"
ALT_F3 = b"\x1b[1;3R"
ALT_F4 = b"\x1b[1;3S"
CTRL_F4 = b"\x1b[1;5S"


def exercise(run):
    run.launch()
    run.set_fast_save(False)
    for key in ("alpha ", F6, "beta", F6, " gamma", ENTER, "next alpha"):
        run.step(key, "compose the formatted document")
    run.start_of_document()
    run.step(CTRL_RIGHT, "move to the first character of beta", 'Pos 1.6"')
    run.step(CTRL_RIGHT, "move through the closing pair and separator", 'Pos 2.1"')
    run.step(CTRL_LEFT, "return to the first character of beta", 'Pos 1.6"')
    run.step(b"\x1b[C", "move inside the formatted word", 'Pos 1.7"')
    run.step(ALT_F3, "show native formatting")
    run.step(CTRL_DELETE, "delete the formatted word and separator", "alpha [BOLD][bold]gamma")
    run.step(F1, "open Undelete", "Undelete")
    run.step("1", "restore the removed text after the pair", "alpha [BOLD][bold]beta gamma")
    run.start_of_document()
    run.step(CTRL_HOME, "open Go To", "Go to")
    run.step("g", "go to the next g", 'Pos 2.2"')
    run.step(CTRL_HOME, "open Go To again", "Go to")
    run.step(ENTER, "go through the next hard return", 'Ln 1.17" Pos 1"')
    run.save("MOTION.WP")
    assert native(run.p.work / "MOTION.WP")[2] == b"alpha \xc3\x0c\xc3\xc4\x0c\xc4beta gamma\nnext alpha"

    run.step(SWITCH, "switch to Doc 2 without an active block", "Doc 2 Pg")
    sample = "BEFORE. I'M HERE! NEXT? THIRD. I SAID i'M HERE. lower."
    run.step(sample, "enter the original mixed-case fixture")
    run.start_of_document()
    run.step(ALT_F4, "begin a block")
    run.step(b"\x1b[C" * len(sample), "extend the block through the fixture")
    run.step(SWITCH, "open Convert Case with an active block", "1 Uppercase; 2 Lowercase: 0")
    run.step("2", "apply WordPerfect lowercase rules", "before. I'm here! Next? Third. I said i'm here. lower.")
    run.save("CASE.WP")
    assert native(run.p.work / "CASE.WP")[2] == b"before. I'm here! Next? Third. I said i'm here. lower."
    run.step(F7, "close the saved second document", "Save document?")
    run.step("n", "decline another Doc 2 save", "Exit doc 2?")
    run.step("y", "return to the saved first document", "Doc 1 Pg")

    run.step(SWITCH, "open a clean Doc 2 for Move/Copy", "Doc 2 Pg")
    for key in (F6, "alpha", F6, " beta"):
        run.step(key, "prepare the original styled copy fixture")
    run.start_of_document()
    run.step(ALT_F4, "begin the source block")
    run.step(b"\x1b[C" * len("alpha"), "select the styled source word")
    run.step(CTRL_F4, "open Move", "Move: 1 Block")
    run.step("1", "choose Block", "1 Move; 2 Copy; 3 Delete; 4 Append: 0")
    run.step("2", "choose Copy", "Move cursor; press Enter to retrieve.")
    run.step(b"\x1bOF", "move to the end of the destination line")
    run.step(ENTER, "retrieve the block at the destination", "alpha betaalpha")
    run.save("BLOCK.WP")
    _, _, expected = native(run.repo / "docs/research/reference-runs/mission1-block-copy/BLOCK.WP")
    assert native(run.p.work / "BLOCK.WP")[2] == expected
    run.step(F7, "close the saved copy fixture", "Save document?")
    run.step("n", "decline another Doc 2 save", "Exit doc 2?")
    run.step("y", "return to the saved first document", "Doc 1 Pg")

    run.step(SWITCH, "open a clean Doc 2 for Append", "Doc 2 Pg")
    run.step("BEGIN", "prepare an existing Append target")
    run.save("APPEND.WP")
    run.step(F7, "close the target before Append", "Save document?")
    run.step("n", "decline another target save", "Exit doc 2?")
    run.step("y", "return to the first document", "Doc 1 Pg")
    run.step(SWITCH, "open a clean Doc 2 for the source", "Doc 2 Pg")
    for key in (F6, "APPEND", F6):
        run.step(key, "prepare the attributed Append selection")
    run.start_of_document()
    run.step(ALT_F4, "begin the Append block")
    run.step(b"\x1b[C" * len("APPEND"), "select the styled Append word")
    run.step(CTRL_F4, "open Move", "Move: 1 Block")
    run.step("1", "choose Block", "1 Move; 2 Copy; 3 Delete; 4 Append: 0")
    run.step("4", "choose Append", "Append to:")
    run.step("APPEND.WP", "name the existing native target")
    run.step(ENTER, "append the selected text")
    target = run.p.work / "APPEND.WP"
    _, _, expected = native(run.repo / "docs/research/reference-runs/mission1-block-copy/APPEND.WP")
    run.until(lambda: native(target)[2] == expected, "native Append body matches the original")
    run.wait("Doc 2 Pg")
    run.start_of_document()
    run.step(ALT_F4, "begin the block for a new target")
    run.step(b"\x1b[C" * len("APPEND"), "select the same attributed source")
    run.step(CTRL_F4, "reopen Move", "Move: 1 Block")
    run.step("1", "choose Block", "1 Move; 2 Copy; 3 Delete; 4 Append: 0")
    run.step("4", "choose Append", "Append to:")
    run.step("NEWAPP.WP", "name an absent target")
    run.step(ENTER, "publish a new native target")
    target = run.p.work / "NEWAPP.WP"
    _, _, expected = native(run.repo / "docs/research/reference-runs/mission1-block-copy/NEWAPP.WP")
    run.until(lambda: target.is_file() and native(target)[2] == expected, "new native Append body matches DOS")
    run.wait("Doc 2 Pg")
    run.save("SOURCE.WP")
    assert native(run.p.work / "SOURCE.WP")[2] == b"\xc3\x0c\xc3APPEND\xc4\x0c\xc4"
    run.step(F7, "close the saved Append source", "Save document?")
    run.step("n", "decline another source save", "Exit doc 2?")
    run.step("y", "return to the saved first document", "Doc 1 Pg")

    run.step(SWITCH, "open a clean Doc 2 for the hard-space fixture", "Doc 2 Pg")
    prefix = "x " + "a" * 58
    run.step(prefix + " alpha", "type sixty cells and a word at the right edge")
    run.step(b"\x1bOH", "start the Home prefix")
    run.step(" ", "insert a nonbreaking space")
    run.step("beta", "force a wrap before the joined words", "alpha beta")
    run.step(ALT_F3, "verify the hard-space code", "alpha[ ]beta")
    run.save("HSPACE.WP")
    _, _, original = native(run.repo / "docs/research/reference-runs/mission1-line-format/LINEFMT.WP")
    assert native(run.p.work / "HSPACE.WP")[2] == original[original.index(prefix.encode()):]
    run.step(F7, "close the hard-space fixture", "Save document?")
    run.step("n", "decline another fixture save", "Exit doc 2?")
    run.step("y", "return to the saved first document", "Doc 1 Pg")

    run.step(SWITCH, "open a clean Doc 2 for page deletion", "Doc 2 Pg")
    for key in ("keep remove", ENTER, "remove again", b"\x1b[13;5u", "next page"):
        run.step(key, "create the original two-page fixture")
    run.start_of_document()
    run.step(b"\x1b[C" * len("keep "), "choose where to delete to the page boundary")
    run.step(CTRL_PAGE_DOWN, "start Delete Remainder of page", "Delete Remainder of page? No (Yes)")
    run.step(ENTER, "decline using the default response", "remove again")
    run.step(CTRL_PAGE_DOWN, "repeat Delete Remainder of page", "Delete Remainder of page? No (Yes)")
    run.step("y", "confirm deletion while preserving the next page", "next page")
    run.save("DELPG.WP")
    _, _, expected = native(run.repo / "docs/research/reference-runs/mission1-page-delete/DELPG.WP")
    assert native(run.p.work / "DELPG.WP")[2] == expected
    run.step(F7, "close the page-deletion fixture", "Save document?")
    run.step("n", "decline another fixture save", "Exit doc 2?")
    run.step("y", "return to the saved first document", "Doc 1 Pg")
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
        run.finish(failure, "DOS navigation and deletion")
