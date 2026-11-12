#!/usr/bin/env python3
"""Compare PAGE and nested Ctrl+F9 terminal output with the original DOS exports."""
import argparse
from pathlib import Path

from merge_cases import enter_primary, select
from physical_cases import RIGHT, press
from qualification import ENTER, Run, sha

CASES = {
    "208": "2026-10-29-advanced-03",
    "216": "2026-10-29-history-01",
    "217": "2026-10-29-history-01",
    "223": "2026-10-29-iteration-01",
    "224": "2026-10-29-iteration-01",
    "225": "2026-10-29-iteration-01",
    "233": "2026-10-30-values-01",
    "234": "2026-10-30-values-01",
    "235": "2026-10-30-values-01",
    "236": "2026-10-30-values-01",
}
FRESH = "docs/research/everyday-contract-2026-11-05/native-merge/fresh"
ORDINALS = ("ordinals", "field3", "literal-tilde")


def compare(path, data):
    want = path.read_bytes()
    assert data == want, (sha(data), sha(want))


def exercise(run, case):
    fixtures = run.repo / "docs/research/reference-runs" / CASES[case] / ("CMD51-" + case)
    (run.p.work / "OUT").mkdir()
    inputs = ("PRIMARY", "SECOND", "CHILD") if (fixtures / "CHILD.WP5").exists() else ("PRIMARY", "SECOND")
    for name in inputs:
        guest_name = name if name == "CHILD" else name + ".WP5"
        run.seed(fixtures / (name + ".WP5"), "OUT/" + guest_name)
    run.launch()
    enter_primary(run)
    run.step(r"C:\OUT\PRIMARY.WP5", "type the original primary")
    run.step(ENTER, "accept exact primary", "Secondary file:", 24)
    run.step(r"C:\OUT\SECOND.WP5", "type the original secondary")
    run.step(ENTER, "evaluate all source records")
    run.wait("Alice")
    run.wait("Bob")
    data = run.save("MERGED.WP5", expected_offset=564)
    compare(fixtures / "MERGED.WP5", data)
    for name in inputs:
        guest_name = name if name == "CHILD" else name + ".WP5"
        assert (run.p.work / "OUT" / guest_name).read_bytes() == (fixtures / (name + ".WP5")).read_bytes()
    run.exit_application()


def missing_nested(run, role):
    case = "223" if role == "primary" else "234"
    fixtures = run.repo / "docs/research/reference-runs" / CASES[case] / ("CMD51-" + case)
    (run.p.work / "OUT").mkdir()
    run.seed(fixtures / "PRIMARY.WP5", "OUT/PRIMARY.WP5")
    run.seed(fixtures / "SECOND.WP5", "SECOND.WP5")
    # The DOS operand is extensionless. A file with the capture's
    # convenience suffix must remain a different file.
    run.seed(fixtures / "CHILD.WP5", "OUT/CHILD.WP5")
    run.launch()
    run.step("KEPT", "retain an occupied receiver", "KEPT")
    enter_primary(run)
    run.step(r"C:\OUT\PRIMARY.WP5", "type the original primary")
    run.step(ENTER, "accept exact primary", "Secondary file:", 24)
    if role == "primary":
        run.step("SECOND.WP5", "type the original secondary")
        run.step(ENTER, "run with missing child")
    else:
        select(run, "SECOND.WP5")
    run.wait("nested file not found")
    run.wait("KEPTPAlice" if role == "primary" else "KEPTHello Alice")
    data = run.save("PARTIAL.WP5")
    compare(run.repo / FRESH / ("missing-" + role) / "MERGED.WP5", data)
    for name, file in (("OUT/PRIMARY.WP5", "PRIMARY.WP5"), ("SECOND.WP5", "SECOND.WP5"), ("OUT/CHILD.WP5", "CHILD.WP5")):
        assert (run.p.work / name).read_bytes() == (fixtures / file).read_bytes()
    run.exit_application()


def relative_nested(run):
    fixtures = run.repo / "docs/research/reference-runs" / CASES["223"] / "CMD51-223"
    (run.p.work / "OUT").mkdir()
    fresh = run.repo / FRESH / "relative"
    run.seed(fresh / "PRIMARY.WP5", "OUT/PRIMARY.WP5")
    run.seed(fixtures / "SECOND.WP5", "OUT/SECOND.WP5")
    run.seed(fixtures / "CHILD.WP5", "CHILD")
    run.launch()
    run.step("KEPT", "retain an occupied receiver", "KEPT")
    enter_primary(run)
    run.step(r"C:\OUT\PRIMARY.WP5", "type the primary in another directory")
    run.step(ENTER, "accept exact primary", "Secondary file:", 24)
    run.step(r"C:\OUT\SECOND.WP5", "type the secondary in another directory")
    run.step(ENTER, "resolve bare child in the working directory", "CAlice")
    run.wait("CBob")
    data = run.save("RELATIVE.WP5")
    compare(fresh / "MERGED.WP5", data)
    run.exit_application()


def ordinal_merge(run, case):
    fresh = run.repo / FRESH
    run.seed(fresh / case / "PRIMARY.WP5", "PRIMARY.WP5")
    run.seed(fresh / "ordinals" / "SECOND.WP5", "SECOND.WP5")
    run.launch()
    enter_primary(run)
    run.step("PRIMARY.WP5", "use the replayed ordinal primary")
    run.step(ENTER, "accept primary", "Secondary file:", 24)
    run.step("SECOND.WP5", "use the two explicit fields")
    run.step(ENTER, "resolve the qualified ordinals")
    run.wait("FILLED")
    run.wait("EMPTY")
    data = run.save("MERGED.WP5", expected_offset=564)
    compare(fresh / case / "MERGED.WP5", data)
    run.exit_application()


def loaded_eof(run):
    fixtures = run.repo / "docs/research/reference-runs/2026-10-29-extended-04/CMD51-134"
    run.seed(fixtures / "PRIMARY.WP5", "PRIMARY.WP5")
    run.seed(fixtures / "SECOND.WP5", "SECOND.WP5")
    run.seed(run.repo / "internal/document/testdata/fast_save_yes/SECOND.WP", "RECEIVER.WP5")
    run.launch()
    run.retrieve("RECEIVER.WP5")
    run.wait("Alpha beta")
    press(run, *([RIGHT] * len("Alpha beta")))
    enter_primary(run)
    run.step("PRIMARY.WP5", "use original compact primary")
    run.step(ENTER, "accept primary", "Secondary file:", 24)
    run.step("SECOND.WP5", "use original secondary")
    run.step(ENTER, "merge at acquired receiver EOF", "Alpha betaHello Alice")
    data = run.save("MERGED.WP5", expected_offset=564)
    compare(run.repo / FRESH / "loaded-eof" / "MERGED.WP5", data)
    run.exit_application()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("binary", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("case", choices=(*CASES, "missing-primary", "missing-secondary", "relative", *ORDINALS, "loaded-eof"))
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output must be fresh")
    run = Run(args.repo.resolve(), args.binary.resolve(), args.output.resolve())
    failure = None
    try:
        if args.case.startswith("missing-"):
            missing_nested(run, args.case.removeprefix("missing-"))
        elif args.case == "relative":
            relative_nested(run)
        elif args.case in ORDINALS:
            ordinal_merge(run, args.case)
        elif args.case == "loaded-eof":
            loaded_eof(run)
        else:
            exercise(run, args.case)
    except Exception as error:
        failure = repr(error)
    finally:
        run.finish(failure, "native PAGE and nested merge " + args.case)


if __name__ == "__main__":
    main()
