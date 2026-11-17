#!/usr/bin/env python3
"""Compare screen and disk in Wordling through actual terminal key bytes."""
import sys
from pathlib import Path

from qualification import ENTER, Run, native


def exercise(run, multiple):
    refs = run.repo / "docs/research/reference-runs/mission1-document-compare"
    run.seed(refs / ("MULBEFR.WP" if multiple else "BEFORE.WP"), "BEFORE.WP")
    run.launch()
    run.set_fast_save(False)
    run.retrieve("BEFORE.WP")
    if multiple:
        run.step(b"\x1b[B", "move to the changed line")
    for _ in range(6):
        run.step(b"\x1b[C", "move to the changed word")
    for _ in range(3):
        run.step(b"\x1b[3~", "remove the old word")
    run.step("new", "type the replacement", "Alpha new tail")
    for key in (b"\x1b[15;3~", "6", "2"):
        run.step(key, "open Mark, Generate, Compare")
    run.wait("Other Document: BEFORE.WP")
    run.step(ENTER, "use the default disk document", "Alpha old tail")
    run.step(b"\x1b[1;3R", "inspect the original change codes",
             "[REDLN]Alpha new tail[HRt]" if multiple else "[REDLN]Alpha new tail[redln][STKOUT]Alpha old tail[stkout]")
    if multiple:
        run.wait("[redln][STKOUT]Alpha old tail[HRt]")
    run.step(b"\x1b[1;3R", "return to ordinary editing")
    run.save("COMPARE.WP")
    assert native(run.p.work / "COMPARE.WP")[2] == native(refs / ("MULTI.WP" if multiple else "COMPARE.WP"))[2]
    assert (run.p.work / "BEFORE.WP").read_bytes() == (refs / ("MULBEFR.WP" if multiple else "BEFORE.WP")).read_bytes()
    for key in (b"\x1b[15;3~", "6", "1"):
        run.step(key, "open comparison cleanup")
    run.wait("Remove redline markings and strikeout text?")
    run.step(ENTER, "keep marks by default", "Alpha old tail")
    for key in (b"\x1b[15;3~", "6", "1"):
        run.step(key, "reopen comparison cleanup")
    run.step("y", "confirm comparison cleanup", "Alpha new tail")
    run.step("!", "verify cursor moved to document end")
    run.save("CLEAN.WP")
    expected = b"Overview\nAlpha new tail\nClosing!" if multiple else b"Alpha new tail!"
    assert native(run.p.work / "CLEAN.WP")[2] == expected
    assert native(run.p.work / "COMPARE.WP")[2] == native(refs / ("MULTI.WP" if multiple else "COMPARE.WP"))[2]
    run.exit_application()


if __name__ == "__main__":
    repo, binary, output = (Path(arg).resolve() for arg in sys.argv[1:4])
    output.mkdir()
    for phase in ("single", "with-surrounding-lines"):
        run = Run(repo, binary, output / phase, classic_canvas=True)
        failure = None
        try:
            exercise(run, phase != "single")
        except Exception as error:
            failure = repr(error)
            raise
        finally:
            run.finish(failure, "document-compare-" + phase)

        reopened = Run(repo, binary, output / (phase + "-reopened"), classic_canvas=True)
        failure = None
        try:
            reopened.seed(run.p.work / "CLEAN.WP", "CLEAN.WP")
            reopened.launch()
            reopened.retrieve("CLEAN.WP")
            reopened.wait("Alpha new tail!") if phase == "single" else reopened.wait("Closing!")
            reopened.exit_application()
        except Exception as error:
            failure = repr(error)
            raise
        finally:
            reopened.finish(failure, "document-compare-reopened-" + phase)
