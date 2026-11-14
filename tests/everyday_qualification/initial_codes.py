"""Compare F10 saves, screen spacing and reopening to captured DOS documents."""

from pathlib import Path
import sys

from line_format import ALT_F3, SHIFT_F8
from qualification import ENTER, F1, F7, Run, native


def configure(run, spacing, previous=None):
    run.step(SHIFT_F8, "open Format", "Format:")
    run.step("3", "open Document Format", "Format: Document")
    run.step("2", "open Initial Codes", "Initial Codes:  Press Exit when done")
    if previous is not None:
        run.wait(f"[Ln Spacing:{previous}]")
    run.step(SHIFT_F8, "open Format within Initial Codes", "Format:")
    run.step("1", "open Line Format", "Format: Line")
    run.step("6", "open Line Spacing", "Selection: 6")
    run.step(spacing, "enter line spacing")
    run.step(ENTER, "accept spacing", "Selection: 0")
    run.step(F7, "return to Initial Codes", f"[Ln Spacing:{spacing}]")
    run.step(F1, "F1 leaves the Initial Codes editor open", f"[Ln Spacing:{spacing}]")
    run.step(F7, "return to Document Format", "Format: Document")
    run.step(F7, "return to the body", "Doc 1 Pg")


def exercise(run, case):
    refs = run.repo / "docs/research/reference-runs/mission1-initial-codes"
    reopening = case in {"LOADEDY", "LOADEDN", "ARCHIVE"}
    if reopening:
        source = refs / ("LOADEDY.WP" if case == "ARCHIVE" else "DOUBLE.WP")
        run.seed(source, "INPUT.WP")
    run.launch()
    if reopening:
        if case == "LOADEDN":
            run.set_fast_save(False)
        run.retrieve("INPUT.WP")
        if case == "ARCHIVE":
            run.step(b"\x1b[B", "move down one single-spaced line", 'Ln 1.17"')
            run.save("COPY.WP", expected_offset=576)
            assert (run.p.work / "COPY.WP").read_bytes() == source.read_bytes()
            run.exit_application()
            return
        run.step(b"\x1b[B", "move down by one double-spaced line", 'Ln 1.33"')
        run.save("COPY.WP", expected_offset=336)
        assert (run.p.work / "COPY.WP").read_bytes() == source.read_bytes()
        configure(run, "1", previous="2")
        run.wait('Ln 1.17"')
        run.step("X", "edit in the loaded document at the same caret")
        raw = run.save("EDITED.WP", expected_offset=576 if case == "LOADEDY" else 336)
        assert native(run.p.work / "EDITED.WP")[2] == b"alpha\nXbeta"
        assert raw == (refs / f"{case}.WP").read_bytes()
        assert (run.p.work / "INPUT.WP").read_bytes() == source.read_bytes()
    else:
        configure(run, "1" if case == "SINGLE" else "2")
        if case == "RESET":
            configure(run, "1", previous="2")
        run.step("alpha", "type the first line")
        if case == "PAGES":
            for _ in range(29):
                run.step(ENTER, "advance to the next double-spaced line")
                run.step("beta", "fill the line")
            run.wait('Pg 2 Ln 1.67"')
        elif case != "ALPHA":
            height = 'Ln 1.17"' if case in {"RESET", "SINGLE"} else 'Ln 1.33"'
            run.step(ENTER, "start the second line at the expected height", height)
            run.step("beta", "type the second line")
        run.step(ALT_F3, "show Reveal Codes")
        assert "[Ln Spacing:" not in "\n".join(run.rows())
        run.step(ALT_F3, "close Reveal Codes")
        raw = run.save(case + ".WP", expected_offset=336)
        expected_file = "RESET" if case == "SINGLE" else case
        assert raw == (refs / f"{expected_file}.WP").read_bytes(), case
    run.exit_application()


if __name__ == "__main__":
    repo, binary, output = (Path(arg).resolve() for arg in sys.argv[1:4])
    output.mkdir()
    for case in ("ALPHA", "DOUBLE", "RESET", "SINGLE", "LOADEDY", "LOADEDN", "ARCHIVE", "PAGES"):
        run = Run(repo, binary, output / case.lower(), classic_canvas=True)
        failure = None
        try:
            exercise(run, case)
        except Exception as err:
            failure = repr(err)
            raise
        finally:
            run.finish(failure, "initial-codes-" + case)
