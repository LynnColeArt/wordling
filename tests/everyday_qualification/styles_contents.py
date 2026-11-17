#!/usr/bin/env python3
"""Exercise the DOS structured document workflows through the terminal."""
import sys
from pathlib import Path

from qualification import ENTER, F7, Run, native

ALT_F5 = b"\x1b[15;3~"
SHIFT_F5 = b"\x1b[15;2~"
ALT_F8 = b"\x1b[19;3~"
F6 = b"\x1b[17~"
ALT_F7 = b"\x1b[18;3~"
TAB = b"\t"
UP, LEFT, DOWN = b"\x1b[A", b"\x1b[D", b"\x1b[B"
HOME, DELETE = b"\x1bOH", b"\x1b[3~"
F1 = b"\x1bOP"


def exercise(run, case):
    if case == "merge-sort":
        source = run.repo / "docs/research/reference-runs/mission1-sort"
        run.seed(source / "BEFORE.WP", "BEFORE.WP")
    run.launch()
    run.set_fast_save(False)
    if case == "styles":
        for key in (ALT_F8, "3", "1", "EMPHASIS", ENTER, "4", F6, F7, F7):
            run.step(key, "create a paired Bold style")
        for key in ("3", "1", "emphasis", ENTER):
            run.step(key, "attempt a duplicate style name")
        run.wait("Style name already exists")
        for key in (F1, F1, "1", "Styled text"):
            run.step(key, "apply the original named style")
        run.save("STYLE.WP", expected_offset=418)
        _, _, body = native(run.p.work / "STYLE.WP")
        assert body.count(b"EMPHASIS") == 2 and b"\xc3\x0c\xc3" in body and b"Styled text" in body
    elif case == "italics":
        ctrl_f8 = b"\x1b[19;5~"
        for key in (ctrl_f8, "2", "4", "alpha", ctrl_f8, "2", "4", "beta"):
            run.step(key, "turn Italics on, type alpha, turn it off and type beta")
        run.wait("alphabeta")
        run.step(b"\x1b[1;3R", "inspect the original Italics codes", "[ITALC]alpha[italc]beta")
        run.step(b"\x1b[1;3R", "return to ordinary editing")
        run.save("ITALICS.WP")
        ref = run.repo / "docs/research/reference-runs/mission1-appearance/ITALICS.WP"
        assert native(run.p.work / "ITALICS.WP")[2] == native(ref)[2]
    elif case in ("single-line-draw", "double-line-draw"):
        single = case == "single-line-draw"
        for key in (b"\x1b[1;5R", "2", "1" if single else "2"):
            run.step(key, "choose a line drawing style")
        for _ in range(4):
            run.step(b"\x1b[C", "draw one cell to the right")
        run.step(F7, "return to ordinary editing")
        run.wait("───" if single else "═══")
        name = "SINGLE.WP" if single else "DOUBLE.WP"
        run.save(name)
        ref = run.repo / "docs/research/reference-runs/mission1-line-draw" / name
        assert native(run.p.work / name)[2] == native(ref)[2]
    elif case == "kerning":
        for key in ("AV ", b"\x1b[19;2~", "4", "6", "1", "y", F7, "AV"):
            run.step(key, "enable kerning between two text runs")
        run.wait("AV AV")
        run.save("KERN.WP")
        ref = run.repo / "docs/research/reference-runs/mission1-kerning/KERN.WP"
        assert native(run.p.work / "KERN.WP")[2] == native(ref)[2]
    elif case == "language":
        for key in ("Before", b"\x1b[19;2~", "4", "4", "UK", ENTER, F7, "After"):
            run.step(key, "insert a UK language code at the cursor")
        run.wait("BeforeAfter")
        run.save("LANGUAGE.WP")
        ref = run.repo / "docs/research/reference-runs/mission1-language/LANGUAGE.WP"
        assert native(run.p.work / "LANGUAGE.WP")[2] == native(ref)[2]
    elif case == "column-math":
        for key in (ALT_F7, "3", "1", "N", TAB, "3", ENTER, "S", TAB, "5", ENTER, "T", TAB, "+"):
            run.step(key, "enter a column subtotal")
        for key in (ALT_F7, "3", "4"):
            run.step(key, "calculate the subtotal")
        run.wait("8.00+")
        for key in (ENTER, ALT_F7, "3", "2", "After"):
            run.step(key, "leave Math before ordinary typing")
        run.save("TOTAL.WP")
        ref = run.repo / "docs/research/reference-runs/mission1-column-math/TOTAL.WP"
        assert native(run.p.work / "TOTAL.WP")[2] == native(ref)[2]
    elif case == "merge-sort":
        run.retrieve("BEFORE.WP")
        for key in (b"\x1b[20;5~", "2", ENTER, ENTER, "7", "1"):
            run.step(key, "sort on-screen merge records by the default ascending key")
        run.wait("Sort Secondary Merge File")
        run.step("1", "perform the sort")
        run.wait("Amber")
        run.save("SORTED.WP")
        assert native(run.p.work / "SORTED.WP")[2] == native(source / "SORTED.WP")[2]
        assert (run.p.work / "BEFORE.WP").read_bytes() == (source / "BEFORE.WP").read_bytes()
    elif case == "outline":
        for key in (SHIFT_F5, "4", "1", ENTER, "First", ENTER, TAB, "Child"):
            run.step(key, "create two default outline levels")
        run.wait("I.First")
        run.wait("     A.Child")
        run.save("OUTLINE.WP")
        ref = run.repo / "docs/research/reference-runs/mission1-outline/OUTLINE.WP"
        assert native(run.p.work / "OUTLINE.WP")[2] == native(ref)[2]
    elif case == "authority":
        citation = "Sample v. Example"
        run.step(citation, "type the citation")
        for _ in citation:
            run.step(LEFT, "move to the start of the citation")
        for key in (b"\x1b[1;3S", b"\x1bOF", ALT_F5, "4", "1", ENTER):
            run.step(key, "mark the text as a full authority")
        run.wait("ToA Full Form:")
        run.step(F7, "accept the full form")
        run.wait("Short Form: " + citation)
        run.step(ENTER, "accept the short form")
        run.save("CITE.WP")
        ref = run.repo / "docs/research/reference-runs/mission1-authorities/CITE.WP"
        assert native(run.p.work / "CITE.WP")[2] == native(ref)[2]
    elif case == "table-join":
        for key in (ALT_F7, "2", "1", "2", ENTER, "2", ENTER, F7):
            run.step(key, "create a default two-by-two table")
        for key in ("ALPHA", TAB, "BETA", TAB, "GAMMA", TAB, "DELTA", UP, HOME, LEFT, ALT_F7):
            run.step(key, "return to the first cell in Table Edit")
        for key in (b"\x1b[1;3S", b"\x1b[C", "7"):
            run.step(key, "select the first row and request Join")
        run.wait("Join cells? No (Yes)")
        run.step("y", "confirm join")
        run.step(F7, "leave Table Edit")
        run.wait("ALPHA                           BETA")
        run.save("ROWJOIN.WP")
        ref = run.repo / "docs/research/reference-runs/mission1-table-join/ROWJOIN.WP"
        assert native(run.p.work / "ROWJOIN.WP")[2] == native(ref)[2]
    elif case in ("table-calculate", "table-copy"):
        for key in (ALT_F7, "2", "1", "2", ENTER, "2", ENTER, F7):
            run.step(key, "create a default two-by-two table")
        if case == "table-calculate":
            for key in ("2", TAB, "3", TAB, ALT_F7, "5", "2", "A1+B1", ENTER, F7):
                run.step(key, "enter the formula")
            run.wait("5.00")
            for key in (UP, HOME, DELETE, "7"):
                run.step(key, "change the first input")
            run.wait("5.00")
            for key in (ALT_F7, "5", "1", F7):
                run.step(key, "explicitly recalculate")
            name = "RECALC.WP"
        else:
            for key in (TAB, "3", TAB, TAB, "5", UP, LEFT, LEFT, ALT_F7, "5", "2", "B1+B1", ENTER):
                run.step(key, "enter the source formula")
            run.wait("6.00")
            for key in ("5", "3", "1", DOWN, ENTER, F7):
                run.step(key, "copy the relative formula to the lower row")
            run.wait("=B2+B2")
            name = "COPY.WP"
        run.wait("10.00")
        run.save(name)
        ref = run.repo / "docs/research/reference-runs/mission1-table-math" / name
        assert native(run.p.work / name)[2] == native(ref)[2]
    elif case == "cross-reference":
        for key in ("See page ", ALT_F5, "1", "1", "1", "Mixed", ENTER):
            run.step(key, "mark a page reference")
        run.wait("See page ?")
        for key in (b"\x1b[13;5u", "Chapter", ALT_F5, "1", "2", "mixed", ENTER):
            run.step(key, "mark the target on page two")
        for key in (ALT_F5, "6", "5", "y"):
            run.step(key, "generate the reference")
        run.wait("See page 2")
        run.save("AFTER.WP")
        ref = run.repo / "docs/research/reference-runs/mission1-cross-references/AFTER.WP"
        assert native(run.p.work / "AFTER.WP")[2] == native(ref)[2]
    elif case == "subdocument":
        for key in ("Chapter ", ALT_F5, "2", "chapter.wp", ENTER, " end"):
            run.step(key, "insert a condensed subdocument link")
        run.wait("Subdoc: CHAPTER.WP")
        run.save("MASTER.WP")
        ref = run.repo / "docs/research/reference-runs/mission1-subdocuments/MASTER.WP"
        assert native(run.p.work / "MASTER.WP")[2] == native(ref)[2]
    else:
        for key in (ALT_F5, "5", "1", F7, "Overview"):
            run.step(key, "define the table and type the heading")
        for _ in range(len("Overview")):
            run.step(b"\x1b[D", "move back to the beginning of the heading")
        for key in (b"\x1b[1;3S", b"\x1bOF", ALT_F5, "1", "1", ENTER):
            run.step(key, "mark the heading for level one")
        for key in (ALT_F5, "6", "5"):
            run.step(key, "open the generation confirmation")
        run.wait("Existing tables, lists, and indexes will be replaced.")
        run.step("n", "decline generation")
        run.save("DEFIN.WP")
        for key in (ALT_F5, "6", "5", "y"):
            run.step(key, "approve contents generation")
        run.wait("Overview . . .")
        run.save("GEN.WP")
        for name in ("DEFIN.WP", "GEN.WP"):
            ref = run.repo / "docs/research/reference-runs/mission1-toc-generation" / name
            assert native(run.p.work / name)[2] == native(ref)[2], name
    run.exit_application()


if __name__ == "__main__":
    repo, binary, output = (Path(arg).resolve() for arg in sys.argv[1:4])
    case = sys.argv[4]
    run = Run(repo, binary, output, classic_canvas=True)
    failure = None
    try:
        exercise(run, case)
    except Exception as error:
        failure = repr(error)
        raise
    finally:
        run.finish(failure, case)
