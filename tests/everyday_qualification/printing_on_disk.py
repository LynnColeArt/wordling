"""Print a complete on-disk document while an unsaved document is open."""

from pathlib import Path
import sys

from qualification import ENTER, F7, REF, Run, native

SHIFT_F7 = b"\x1b[18;2~"


def exercise(run):
    refs = run.repo / REF
    source = refs / "dos-list-conditions-results/exports/Z.WP"
    run.seed(source, "Z.WP")
    run.launch()
    run.step("UNSAVED", "type the working document", "UNSAVED")
    run.step(SHIFT_F7, "open Print", "Full Document")
    for key, cue in (
        ("s", "Select Printer"), ("3", "STANPRIN.PRS"), ("2", "8 Other"),
        ("8", "Device or Filename"), ("PRINT.PRN", "PRINT.PRN"),
        (ENTER, "PRINT.PRN"), (F7, "Full Document"),
    ):
        run.step(key, "set the Standard Printer filename", cue)
    run.step("3", "select Document on Disk", "Document name:")
    run.step("Z.WP", "name the existing document")
    run.step(ENTER, "open the page prompt", "Page(s): (All)")
    run.step(ENTER, "print every page")
    output = run.p.work / "PRINT.PRN"
    run.until(output.is_file, "wait for the printer output")
    assert output.read_bytes() == (refs / "mission1-list-dos-text/LIST.PRN").read_bytes()
    run.step(F7, "return to the unsaved document", "UNSAVED")
    run.step("X", "mark the original cursor position", "UNSAVEDX")
    run.save("KEPT.WP")
    assert native(run.p.work / "KEPT.WP")[2] == b"UNSAVEDX"
    assert (run.p.work / "Z.WP").read_bytes() == source.read_bytes()
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
        run.finish(failure, "Print Document on Disk")
