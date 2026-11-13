#!/usr/bin/env python3
"""Edit an original two-by-two table and compare native DOS saves."""
import argparse
from pathlib import Path

from physical_cases import DELETE, DOWN, END
from qualification import F7, Run

FIXTURES = "docs/research/everyday-contract-2026-11-05/tables"


def exercise(run, fast_save):
    fixtures = run.repo / FIXTURES
    source = fixtures / "TABLE.WP"
    run.seed(source, "TABLE.WP")
    run.launch()
    run.set_fast_save(fast_save)
    run.retrieve("TABLE.WP")
    run.wait("╔")
    run.wait("DELTA")
    run.step(DOWN, "enter first cell", "Cell A1")
    run.step(END, "end of first cell")
    run.step("X", "append within cell", "ALPHAX")
    run.step(b"\t", "next cell", "Cell B1")
    run.step(DELETE, "delete first letter")
    run.step("Z", "insert replacement", "ZETA")
    run.step(b"\t", "move to next row", "Cell A2")
    expected = fixtures / ("EDITYES.WP" if fast_save else "EDITNO.WP")
    assert run.save("EDIT.WP", expected_offset=564 if fast_save else 324) == expected.read_bytes()
    assert (run.p.work / "TABLE.WP").read_bytes() == source.read_bytes()
    run.exit_application()


def create(run, columns=2, rows=2, fixture="EMPTY.WP"):
    run.launch()
    for key, cue in (
        (b"\x1b[18;3~", "2 Tables"),
        ("2", "1 Create"),
        ("1", "Number of Columns"),
        (str(columns), f"Columns: {columns}"),
        (b"\r", "Number of Rows"),
        *((digit, None) for digit in str(rows)),
        (b"\r", "1 Size"),
        (F7, "Cell A1"),
    ):
        run.step(key, "create default table", cue)
    if fixture == "MULTI.WP":
        run.step("ALPHA", "type first line", "ALPHA")
        run.step(b"\r", "insert a line in A1", "Cell A1")
        run.step("SECOND", "type second line", "SECOND")
        run.step(b"\t", "navigate to next cell", "Cell B1")
        run.step("BETA", "type in adjacent cell", "BETA")
    if fixture == "MIDDLE.WP":
        for cell in ("B1", "C1", "A2", "B2"):
            run.step(b"\t", "navigate to the middle cell", "Cell " + cell)
        for i, line in enumerate(("MID", "SECOND", "THIRD")):
            if i:
                run.step(b"\r", "insert a line in B2")
            run.step(line, "type cell line", line)
    if fixture in ("WRAP.WP", "LONG.WP", "BOTH.WP"):
        value = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if fixture == "LONG.WP" else "ALPHA BETA GAMMA DELTA EPSILON"
        run.step(value, "type text that wraps")
        run.wait("TUVWXYZ" if fixture == "LONG.WP" else "DELTA EPSILON")
        run.step(b"\t", "move to next cell", "Cell B1")
        run.step("BETA", "type into B1", "BETA")
    if rows > 32:
        run.step(b"\x1b[6~", "navigate to second page", "Cell A33" if fixture != "BOTH.WP" else "Cell A32")
    output = run.save("OUT.WP")
    if fixture == "BOTH.WP":
        # The DOS first save keeps the older page break. Wordling
        # repaginates immediately, moving the first break up one row.
        assert b"ALPHA BETA GAMMA\rDELTA EPSILON" in output
        run.step(b"\x1b[5~", "return to the first page", "Cell A1")
        run.wait("DELTA EPSILON")
        run.step(b"\x1b[6~", "return to the second page", "Cell A32")
        run.step("AFTERBREAK", "edit after the page break", "AFTERBREAK")
        assert b"AFTERBREAK" in run.save("EDITPAGE.WP")
    else:
        assert output == (run.repo / FIXTURES / fixture).read_bytes()
    run.exit_application()


def edit_multiline(run):
    fixtures = run.repo / FIXTURES
    run.seed(fixtures / "MULTI.WP", "TABLE.WP")
    run.launch()
    run.set_fast_save(False)
    run.retrieve("TABLE.WP")
    run.wait("SECOND")
    run.step(DOWN, "enter A1", "Cell A1")
    run.step(DOWN, "move to second line", "Cell A1")
    run.step(END, "end of second line")
    run.step("X", "append to second line", "SECONDX")
    assert run.save("OUT.WP") == (fixtures / "MULTINO.WP").read_bytes()
    run.exit_application()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("repo", "binary", "output"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--fast-save", choices=("yes", "no", "create", "multi", "four", "middle", "edit-multi", "five", "wrap", "long", "pages", "three", "both"), required=True)
    args = parser.parse_args()
    run = Run(args.repo.resolve(), args.binary.resolve(), args.output.resolve())
    failure = None
    try:
        if args.fast_save == "create":
            create(run)
        elif args.fast_save in ("wrap", "long", "pages", "three", "both"):
            columns, rows = {"wrap": (3, 2), "long": (3, 2), "pages": (3, 35),
                             "three": (4, 70), "both": (3, 34)}[args.fast_save]
            create(run, columns, rows, args.fast_save.upper() + ".WP")
        elif args.fast_save == "multi":
            create(run, 3, 3, "MULTI.WP")
        elif args.fast_save == "edit-multi":
            edit_multiline(run)
        elif args.fast_save == "middle":
            create(run, 3, 3, "MIDDLE.WP")
        elif args.fast_save == "five":
            create(run, 4, 5, "FIVE.WP")
        elif args.fast_save == "four":
            create(run, 4, 4, "FOUR.WP")
        else:
            exercise(run, args.fast_save == "yes")
    except Exception as err:
        failure = repr(err)
        raise
    finally:
        run.finish(failure, "native table edit")


if __name__ == "__main__":
    main()
