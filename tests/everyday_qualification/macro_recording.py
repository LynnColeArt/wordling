#!/usr/bin/env python3
"""Record native WPM files and execute them through actual Linux terminal input."""
import sys
from pathlib import Path

from qualification import ENTER, F7, Run, native

CTRL_F10 = b"\x1b[21;5~"
ALT_F10 = b"\x1b[21;3~"
LEFT = b"\x1b[D"

CASES = {
    "abc": ("TESTMAC", "Recorded test", ("ABC",), b"ABCABC",
            "2026-10-29-extended-04/CMD51-131/TESTMAC.WPM"),
    "editing-keys": ("TYPED", "Keys and text", ("A B", ENTER, "C", LEFT),
                     b"A B\x0aA B\x0aCC", "mission1-macro-recording/TYPED.WPM"),
}


def exercise(run, case, replay_original):
    name, description, keys, expected, relative = CASES[case]
    fixture = run.repo / "docs/research/reference-runs" / relative
    out = run.p.work / "OUT"
    out.mkdir()
    macro = out / (name + ".WPM")
    original = fixture.read_bytes()
    if replay_original:
        macro.write_bytes(original)
    run.launch()
    if replay_original:
        run.step(CTRL_F10, "open the original macro", "Define macro:")
        run.step(r"C:\OUT\TYPED", "enter the existing name")
        run.step(ENTER, "select the existing macro", "Already Exists:")
        run.step("2", "inspect the original macro", "Macro: Action")
        run.wait("{DISPLAY OFF}A·B{Enter}")
        run.wait("C{Left}")
        run.step(F7, "close without changes", "Doc 1 Pg")
        assert macro.read_bytes() == original
        for key in keys:
            run.step(key, "prepare the text and cursor")
    else:
        run.step(CTRL_F10, "begin macro recording", "Define macro:")
        run.step("c:\\out\\" + name.lower(), "name the native macro")
        run.step(ENTER, "accept the macro name", "Description:")
        run.step(description, "describe the recording")
        run.step(ENTER, "begin recording editing keys")
        for key in keys:
            run.step(key, "send a recorded key")
        run.step(CTRL_F10, "finish and write the WPM")
    run.until(macro.is_file, "WPM exists")
    assert macro.read_bytes() == original
    run.step(ALT_F10, "invoke playback", "Macro:")
    run.step("C:\\OUT\\" + name, "select the published WPM")
    run.step(ENTER, "run recorded text, Enter and Left")
    run.wait("Macro complete")
    run.save("PLAYED.WP")
    assert native(run.p.work / "PLAYED.WP")[2] == expected
    assert macro.read_bytes() == original
    run.exit_application()


def replacement(run):
    refs = run.repo / "docs/research/reference-runs/mission1-macro-recording"
    directory = run.p.work / "OUT"
    directory.mkdir()
    path = directory / "TYPED.WPM"
    original = (refs / "TYPED.WPM").read_bytes()
    path.write_bytes(original)
    run.launch()
    run.step(CTRL_F10, "define a macro", "Define macro:")
    run.step(r"C:\OUT\TYPED", "select an existing macro")
    run.step(ENTER, "show collision choices", "Already Exists:")
    run.step("1", "request replacement", "No (Yes)")
    run.step(ENTER, "keep the original", "Already Exists:")
    assert path.read_bytes() == original
    run.step("1", "request replacement again", "No (Yes)")
    run.step("y", "confirm replacement", "Description:")
    run.step("New description", "describe the replacement")
    run.step(ENTER, "record the replacement")
    run.step("Q", "type the replacement key")
    assert path.read_bytes() == original
    run.step(CTRL_F10, "commit replacement")
    run.until(lambda: path.read_bytes() != original, "replacement stored")
    assert path.read_bytes() == (refs / "REPLACED.WPM").read_bytes()
    run.exit_application()


if __name__ == "__main__":
    repo, binary, output = (Path(arg).resolve() for arg in sys.argv[1:4])
    output.mkdir()
    for phase, original in (("abc", False), ("editing-keys", False), ("editing-keys", True), ("replace", False)):
        label = phase + ("-dos-source" if original else "")
        run = Run(repo, binary, output / label, classic_canvas=True)
        failure = None
        try:
            if phase == "replace":
                replacement(run)
            else:
                exercise(run, phase, original)
        except Exception as error:
            failure = repr(error)
            raise
        finally:
            run.finish(failure, "macro-recording-" + label)
