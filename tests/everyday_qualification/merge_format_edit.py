#!/usr/bin/env python3
"""Edit formatting in saved secondary fields over the real terminal."""
import argparse
from pathlib import Path

from merge_authoring import CTRL_F9
from physical_cases import DELETE, RIGHT, close_doc2
from qualification import ENTER, F2, F6, F8, F11, SWITCH, Run

WIDE = "docs/research/everyday-contract-2026-11-05/native-merge/wide"
ALT_F4 = b"\x1b[1;3S"


def exercise(run, case):
    wide = run.repo / WIDE
    fixtures = wide / "edit-format"
    sources = {"BOLD": wide / "55/SECOND.WP5",
               "UNDER": wide / "55/SECOND.WP5",
               "NO-UND": wide / "overlap-page/SECOND.WP5",
               "NO-BOLD": fixtures / "BOLD.WP5"}
    run.seed(sources[case], "SECOND.WP5")
    run.seed(wide / "overlap-page/PRIMARY.WP5", "PRIMARY.WP5")
    run.launch()
    run.set_fast_save(False)
    run.step(SWITCH, "open Doc 2 for the secondary", "Doc 2 Pg")
    run.retrieve("SECOND.WP5")
    query = "BoldStart " if case == "NO-UND" else "A alpha"
    run.step(F2, "search for the beginning of the span", "Srch:")
    run.step(query, "enter the search query")
    run.step(F2, "land after the match", query.rstrip())
    if case in ("BOLD", "UNDER"):
        run.step(ALT_F4, "start Block")
        for _ in range(72):
            run.step(RIGHT, "extend the block by one character")
        run.step(F6 if case == "BOLD" else F8, "format the block across the page")
    else:
        run.step(F11, "open Reveal Codes")
        run.step(DELETE, "remove the attribute pair")
        run.step(F11, "close Reveal Codes")
    expected = (fixtures / (case + ".WP5")).read_bytes()
    actual = run.save("EDITED.WP5")
    assert actual == expected, next((i for i, (a, b) in enumerate(zip(actual, expected)) if a != b), None)
    close_doc2(run)
    run.step(SWITCH, "open a merge receiver", "Doc 2 Pg")
    run.set_fast_save(True)
    run.step(CTRL_F9, "open Merge", "1 Merge; 2 Sort")
    run.step("1", "select Merge", "Primary file:")
    run.step("PRIMARY.WP5", "enter primary filename")
    run.step(ENTER, "accept the primary", "Secondary file:")
    run.step("EDITED.WP5", "enter the edited secondary filename")
    run.step(ENTER, "merge the edited source", "55=")
    assert run.save("MERGED.WP5", expected_offset=564) == (fixtures / (case + "-M.WP5")).read_bytes()
    close_doc2(run)
    run.exit_application()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("repo", "binary", "output"):
        parser.add_argument(key, type=Path)
    parser.add_argument("case", choices=("BOLD", "UNDER", "NO-UND", "NO-BOLD"))
    args = parser.parse_args()
    run = Run(args.repo.resolve(), args.binary.resolve(), args.output.resolve())
    failure = None
    try:
        exercise(run, args.case)
    except Exception as error:
        failure = repr(error)
        raise
    finally:
        run.finish(failure, "format existing merge fields " + args.case)


if __name__ == "__main__":
    main()
