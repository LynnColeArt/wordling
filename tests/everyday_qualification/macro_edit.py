"""Edit original WPMs with terminal keys, then play the published files."""
from pathlib import Path
import sys

from macro_recording import ALT_F10, CTRL_F10
from qualification import ENTER, F1, F7, Run, native

RIGHT = b"\x1b[C"
END = b"\x1bOF"
DELETE = b"\x1b[3~"
CTRL_V = b"\x16"
LEFT = b"\x1b[D"
BACKSPACE = b"\x7f"


def exercise(run, case):
    refs = run.repo / "docs/research/reference-runs"
    out = run.p.work / "OUT"
    out.mkdir()
    source = out / "TYPED.WPM"
    source.write_bytes((refs / "mission1-macro-recording/TYPED.WPM").read_bytes())
    original = source.read_bytes()
    run.launch()
    run.step(CTRL_F10, "define macro", "Define macro:")
    run.step(r"C:\OUT\TYPED", "select original WPM")
    run.step(ENTER, "open existing actions", "Already Exists:")
    if case == "description":
        run.step("3", "open description", "Description: Keys and text")
        run.step(END, "move to end of description")
        for _ in "Keys and text":
            run.step(BACKSPACE, "remove one character")
        run.step("Revised", "enter the revised description")
        run.step(ENTER, "return to the action", "Description      Revised")
        expected_file, expected_text = "DESCR.WPM", b"A B\x0aC"
    else:
        run.step("2", "open the WPM action", "Macro: Action")
        run.step(RIGHT, "move past Display Off")
        if case == "commands":
            run.step(RIGHT, "move past the first literal")
            run.step(RIGHT, "move past the space")
            run.step(CTRL_V, "quote the next command")
            run.step(LEFT, "insert Left", "{DISPLAY OFF}A·{Left}B{Enter}")
            run.step(ENTER, "insert an Action display line break")
            run.wait("║B{Enter}")
            expected_file, expected_text = "MIDDLE.WPM", b"AB\x0aC "
        else:
            run.step("Z", "insert a literal")
            run.step(DELETE, "delete the old literal", "{DISPLAY OFF}Z·B{Enter}")
            expected_file, expected_text = "ACTION.WPM", b"Z B\x0aC"
    assert source.read_bytes() == original
    if case == "cancel":
        run.step(F1, "request cancellation", "Cancel changes? No (Yes)")
        run.step(ENTER, "default keeps the unsaved action", "{DISPLAY OFF}Z·B{Enter}")
        run.step(F1, "request cancellation again", "Cancel changes? No (Yes)")
        run.step("y", "discard the changes", "Doc 1 Pg")
        assert source.read_bytes() == original
        expected_text = b"A B\x0aC"
    else:
        run.step(F7, "save the edited WPM", "Doc 1 Pg")
        assert source.read_bytes() == (refs / "mission1-macro-edit" / expected_file).read_bytes()
    result = source.read_bytes()
    run.step(ALT_F10, "execute the WPM", "Macro:")
    run.step(r"C:\OUT\TYPED", "select edited native macro")
    run.step(ENTER, "replay the result")
    run.wait("Macro complete")
    run.save("PLAYED.WP")
    assert native(run.p.work / "PLAYED.WP")[2] == expected_text
    assert source.read_bytes() == result
    run.exit_application()


if __name__ == "__main__":
    repo, binary, output = (Path(arg).resolve() for arg in sys.argv[1:4])
    output.mkdir()
    for case in ("action", "description", "commands", "cancel"):
        run = Run(repo, binary, output / case, classic_canvas=True)
        failure = None
        try:
            exercise(run, case)
        except Exception as error:
            failure = repr(error)
            raise
        finally:
            run.finish(failure, "macro-edit-" + case)
