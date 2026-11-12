#!/usr/bin/env python3
"""Compare two structural Undelete interleavings with stopped DOS saves."""
import argparse
from pathlib import Path

from physical_cases import RIGHT
from qualification import F1, F11, Run


def exercise(run, move):
    source = run.repo / "docs/research/reference-runs/2026-10-29-extended-04/CMD51-134/PRIMARY.WP5"
    reference = run.repo / "docs/research/everyday-contract-2026-11-05/native-merge/undelete-mixed"
    run.seed(source, "PRIM.WP")
    run.launch()
    run.retrieve("PRIM.WP")
    run.step(F11, "Reveal the single merge code", "Hello [Mrg:FIELD]1~")
    run.start_of_document()
    for _ in "Hello ":
        run.step(RIGHT, "advance to the Field owner")
    run.step(b"\x1b[3~", "delete the sole merge owner", "Hello 1~")
    if move:
        run.start_of_document()
        before, after, name = "", "Hello 1~[HPg]", "RESTGAP.WP"
    else:
        run.step("X", "type into the remaining ordinary text", "Hello X1~")
        before, after, name = "Hello X", "1~[HPg]", "REST.WP"
    run.step(F1, "preview the retained structural deletion", before + "[Block][Mrg:FIELD]" + after)
    run.wait("Undelete: 1 Restore; 2 Previous Deletion: 0", 11)
    run.step("1", "restore at the current caret", before + "[Mrg:FIELD]" + after)
    run.until(lambda: not any("Undelete:" in row for row in run.rows()), "restore settled")
    restored = before + "[Mrg:FIELD]" + after
    row = next(i for i, line in enumerate(run.rows()) if line.startswith(restored))
    assert [i for i, style in enumerate(run.p.terminal.styles[row]) if style[1] == 41] == [len(before + "[Mrg:FIELD]")]
    expected = (reference / name).read_bytes()
    assert run.save(name, expected_offset=564) == expected
    assert (run.p.work / "PRIM.WP").read_bytes() == source.read_bytes()
    run.exit_application()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("repo", "binary", "output"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--move", action="store_true")
    args = parser.parse_args()
    run = Run(args.repo.resolve(), args.binary.resolve(), args.output.resolve())
    failure = None
    try:
        exercise(run, args.move)
    except Exception as error:
        failure = repr(error)
    finally:
        run.finish(failure, "structural restore across text edit or cursor motion")


if __name__ == "__main__":
    main()
