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
    run.step("X" * 26, "fill the cell", "X" * 26)
    run.step("Y", "refuse a character beyond the cell boundary", "UnsupportedBody")
    run.exit_application()


def create(run):
    run.launch()
    for key, cue in (
        (b"\x1b[18;3~", "2 Tables"),
        ("2", "1 Create"),
        ("1", "Number of Columns"),
        ("2", "Columns: 2"),
        (b"\r", "Number of Rows"),
        ("2", "Rows: 2"),
        (b"\r", "1 Size"),
        (F7, "Cell A1"),
    ):
        run.step(key, "create default table", cue)
    assert run.save("EMPTY.WP") == (run.repo / FIXTURES / "EMPTY.WP").read_bytes()
    run.exit_application()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("repo", "binary", "output"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--fast-save", choices=("yes", "no", "create"), required=True)
    args = parser.parse_args()
    run = Run(args.repo.resolve(), args.binary.resolve(), args.output.resolve())
    failure = None
    try:
        if args.fast_save == "create":
            create(run)
        else:
            exercise(run, args.fast_save == "yes")
    except Exception as err:
        failure = repr(err)
        raise
    finally:
        run.finish(failure, "native table edit")


if __name__ == "__main__":
    main()
