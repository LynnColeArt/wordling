#!/usr/bin/env python3
"""Compare F4 and its native output with WordPerfect 5.1 DOS captures."""
import sys
from pathlib import Path

from qualification import Run, native


def exercise(run, case):
    run.launch(enhancements=False)
    if case == "mid":
        run.step("HELLO", "type before the indent")
    run.step(b"\x1bOS", "F4 Indent")
    if case == "double":
        run.step(b"\x1bOS", "advance to the next indent stop")
    if case == "back":
        run.step(b"\x7f", "remove the indent")
    else:
        value = {"mid": "WORLD", "wrap2": "ALPHA BETA GAMMA " * 5 + "END"}.get(case, "INDENT")
        run.step(value, "type indented text")
        if case == "wrap2":
            assert any(line.startswith("     BETA GAMMA") for line in run.rows())
        run.step(b"\r", "end the indent with a hard return")
    run.step("NEXT", "type at the ordinary margin", "NEXT")
    assert any(line.startswith("NEXT") for line in run.rows())
    run.save("OUT.WP")
    fixture = run.repo / "docs/research/everyday-contract-2026-11-05/indent" / (case + ".WP")
    assert native(run.p.work / "OUT.WP")[2] == native(fixture)[2]
    run.exit_application()


if __name__ == "__main__":
    repo, binary, output = (Path(arg).resolve() for arg in sys.argv[1:])
    for case in ("plain", "mid", "double", "wrap2", "back"):
        run = Run(repo, binary, output / case)
        failure = None
        try:
            exercise(run, case)
        except Exception as err:
            failure = repr(err)
            raise
        finally:
            run.finish(failure, case)
