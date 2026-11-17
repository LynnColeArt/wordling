#!/usr/bin/env python3
"""Compare a startup macro invocation with the pinned DOS /m capture."""
import sys
from pathlib import Path

from qualification import Run, native


def execute(run):
    refs = run.repo / "docs/research/reference-runs/mission1-startup-macro"
    run.seed(refs / "TESTMAC.WPM", "TESTMAC.WPM")
    run.p.argv.append("/m-TESTMAC")
    run.launch()
    run.wait("ABC")
    run.wait("Macro")
    run.set_fast_save(False)
    run.save("START.WP")
    assert native(run.p.work / "START.WP")[2] == native(refs / "START.WP")[2] == b"ABC"
    assert (run.p.work / "TESTMAC.WPM").read_bytes() == (refs / "TESTMAC.WPM").read_bytes()
    run.exit_application()


if __name__ == "__main__":
    repo, binary, output = (Path(arg).resolve() for arg in sys.argv[1:])
    run = Run(repo, binary, output, classic_canvas=True)
    failure = None
    try:
        execute(run)
    except Exception as error:
        failure = repr(error)
        raise
    finally:
        run.finish(failure, "startup-macro")
