"""Verify native page-number owners and printed positions through Linux keys."""
from pathlib import Path
import sys
from qualification import F7, Run, native

SHIFT_F8 = b"\x1b[19;2~"
HARD_PAGE = b"\x1b[13;5u"


def exercise(run, case):
    run.launch()
    run.set_fast_save(False)
    position = "2" if case == "TOP" else "7"
    for key in (SHIFT_F8, "2", "6", "4", position, F7):
        run.step(key, "set Standard Printer page number position")
    if case == "TITLE":
        for key in (SHIFT_F8, "2", "8", "4", "y", F7):
            run.step(key, "suppress only the current page number")
    for key in ("Alpha", HARD_PAGE, "Beta", HARD_PAGE, "Gamma"):
        run.step(key, "type the three explicit pages")
    run.wait("Gamma")
    run.save(case + ".WP")
    ref = run.repo / "docs/research/reference-runs/mission1-page-number-position" / (case + ".WP")
    assert native(run.p.work / (case + ".WP"))[2] == native(ref)[2]
    run.exit_application()


if __name__ == "__main__":
    repo, binary, output = (Path(arg).resolve() for arg in sys.argv[1:4])
    output.mkdir()
    for phase in ("TOP", "BOTTOM", "TITLE"):
        run = Run(repo, binary, output / phase.lower(), classic_canvas=True)
        failure = None
        try:
            exercise(run, phase)
        except Exception as err:
            failure = repr(err)
            raise
        finally:
            run.finish(failure, "page-number-position-" + phase)
