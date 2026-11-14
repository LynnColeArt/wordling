"""Exercise the DOS Conditions form, temporary miss, Reset, and Undo over PTY."""

from datetime import datetime
import os
from pathlib import Path
import sys

from qualification import ENTER, F5, F7, REF, Run

DOWN = b"\x1b[B"
ALL = {"RICH    .WP", "Z       .WP", "FIELDS  .WP"}


def listed(run, expected):
    run.wait("Name Search")
    screen = "\n".join(run.rows())
    assert {name for name in ALL if name in screen} == expected, screen


def find(run, fields, expected):
    run.step("9", "open Find", "Conditions")
    run.step("5", "open Conditions", "Find: Conditions")
    run.step("2", "clear the previous conditions")
    for group, offset, value in fields:
        run.step(group, "select the Conditions group")
        for _ in range(offset):
            run.step(DOWN, "descend to the target field")
        run.step(value, "enter the condition")
        run.step(ENTER, "accept the field")
    run.step("1", "perform the search")
    if not expected:
        run.wait("* Not found *")
    listed(run, expected)


def undo(run, expected):
    run.step("9", "open Find")
    run.step("6", "undo one filtered listing")
    listed(run, expected)


def exercise(run):
    source = run.repo / REF
    directory = source / "dos-list-conditions-results/exports"
    run.seed(directory / "RICH.WP", "RICH.WP")
    run.seed(directory / "Z.WP", "Z.WP")
    run.seed(source / "mission1-list-dos-text/FIELDS.WP", "FIELDS.WP")
    for name, day in (("RICH.WP", 9), ("Z.WP", 10), ("FIELDS.WP", 11)):
        epoch = datetime(1992, 3, day, 12).timestamp()
        os.utime(run.p.work / name, (epoch, epoch))
    run.launch()
    run.step(F5, "list files")
    run.step(ENTER, "show all three test files")
    listed(run, ALL)

    summarized = {"RICH    .WP", "FIELDS  .WP"}
    for fields, matches in (
        ([("5", 0, "03-09-92")], set()),
        ([("5", 0, "03-08-92")], summarized),
        ([("5", 1, "03-09-92")], summarized),
        ([("3", 0, "03-08-92")], set()),
        ([("3", 1, "03-08-92")], set()),
        ([("3", 0, "03-09-92"), ("3", 1, "03-09-92")], {"RICH    .WP"}),
        ([("3", 0, "03-09-92"), ("3", 1, "03-10-92")], {"RICH    .WP", "Z       .WP"}),
    ):
        find(run, fields, matches)
        undo(run, ALL)
    for index, term in enumerate(("arbutus", "birch", "cedar", "dogwood", "elm", "fir", "ginkgo", "hawthorn")):
        find(run, [("5", index + 2, term)], {"FIELDS  .WP"})
        undo(run, ALL)
    find(run, [("5", 6, "elm")], {"FIELDS  .WP"})
    find(run, [("5", 6, "absent")], set())
    find(run, [], set())
    undo(run, set())
    undo(run, {"FIELDS  .WP"})
    undo(run, ALL)
    run.step(F7, "close List Files", "Doc 1 Pg")
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
        run.finish(failure, "List Files Conditions")
