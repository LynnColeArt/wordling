"""Exercise native Advance through the ordinary Linux terminal and F10."""

import argparse
from pathlib import Path

from qualification import ENTER, F7, SWITCH, Run, native

SHIFT_F8 = b"\x1b[19;2~"
ALT_F3 = b"\x1b[1;3R"


def advance(run, option, distance):
    run.step(SHIFT_F8, "open Format")
    run.step("4", "open Other", "Format: Other")
    run.step("1", "open Advance", "6 Position")
    run.step(option, "select the advance direction")
    run.step(distance, "enter inches")
    run.step(ENTER, "insert the Advance owner", "Format: Other")
    run.step(F7, "return to editing", "Doc 1 Pg")


def print_to_disk(run):
    run.step(b"\x1b[18;2~", "open Print", "Full Document")
    for key, cue in [
        ("s", "Select Printer"), ("3", "STANPRIN.PRS"), ("2", "8 Other"),
        ("8", "Device or Filename"), ("ADV.PRN", "ADV.PRN"),
        (ENTER, "ADV.PRN"), (F7, "Full Document"),
    ]:
        run.step(key, "configure the Standard Printer disk port", cue)
    run.step("1", "print the full document")
    output = run.p.work / "ADV.PRN"
    run.until(lambda: output.is_file() and output.read_bytes().count(b"\r\n") == 66,
              "complete Standard Printer page")
    return output.read_bytes()


def expect_exact(run, name, reference):
    assert (run.p.work / name).read_bytes() == reference.read_bytes(), (
        f"{name} differs from {reference}"
    )


def wrapped(run, captures):
    run.launch()
    run.set_fast_save(False)
    advance(run, "5", "1")
    first = "a" * 60
    run.step(first + " betaZ", "wrap a word after Advance Right")
    run.wait('Pg 1 Ln 1.17" Pos 2.1"')
    run.save("WRAP.WP")
    _, _, body = native(run.p.work / "WRAP.WP")
    assert body[13:] == b"a" * 55 + b"\x90" + b"a" * 5 + b" betaZ"
    rows = print_to_disk(run).split(b"\r\n")
    assert rows[6] == b" " * 20 + b"a" * 55
    assert rows[7] == b" " * 10 + b"aaaaa betaZ\r"
    if captures:
        for name in ("WRAP.WP", "ADV.PRN"):
            expect_exact(run, name, captures / "wrapped" / name)
    run.exit_application()


def edited_reopen(run, fast_save, captures):
    case = "loaded-yes" if fast_save else "loaded-no"
    source = run.repo / "docs/research/reference-runs/mission1-advance/BOUNDARY.WP"
    if captures:
        source = captures / case / "INPUT.WP"
    run.seed(source, "INPUT.WP")
    run.launch()
    run.set_fast_save(fast_save)
    run.retrieve("INPUT.WP")
    for key in (b"\x1bOH", b"\x1bOH", b"\x1b[B"):
        run.step(key, "move to the end of the reopened document")
    run.wait('Pg 1 Ln 10" Pos 1.7"')
    run.step("X", "append text after the retained Advance Down code", "bottomZX")
    run.wait('Pg 1 Ln 10" Pos 1.8"')
    _, _, body = native(source)
    run.save("EDITED.WP", expected_offset=564 if fast_save else 324)
    assert native(run.p.work / "EDITED.WP")[2] == body + b"X"
    assert (run.p.work / "INPUT.WP").read_bytes() == source.read_bytes()

    run.step(SWITCH, "open a fresh second document", "Doc 2 Pg")
    run.retrieve("EDITED.WP")
    for key in (b"\x1bOH", b"\x1bOH", b"\x1b[B"):
        run.step(key, "move to the end of the edited save")
    run.wait('Pg 1 Ln 10" Pos 1.8"')
    run.step(ALT_F3, "inspect the saved Advance owner", 'bottom[AdvDn:3"]ZX')
    run.step(ALT_F3, "restore normal editing")
    copy = run.save("COPY.WP", expected_offset=564 if fast_save else 324)
    edited, offset, edited_body = native(run.p.work / "EDITED.WP")
    assert copy[offset:] == edited_body
    if fast_save:
        assert int.from_bytes(edited[22:26], "little") == 270
        assert int.from_bytes(copy[22:26], "little") == 272
    else:
        assert copy == edited
    if captures:
        for name in ("INPUT.WP", "EDITED.WP", "COPY.WP"):
            expect_exact(run, name, captures / case / name)
    close_second_document(run)
    run.exit_application()


def close_second_document(run):
    run.step(F7, "close document two", "Save document?")
    run.step("n", "decline another save", "Exit doc 2?")
    run.step("y", "return to document one", "Doc 1 Pg")


def exercise(run, case, captures):
    ref = run.repo / "docs/research/reference-runs/mission1-advance"
    run.launch()
    run.set_fast_save(False)
    if case == "horizontal":
        advance(run, "6", "3")
        run.step("A", "type at absolute position three inches")
        advance(run, "5", "1")
        run.step("B", "type one inch beyond A", "AB")
        run.wait('Pg 1 Ln 1" Pos 4.2"')
        run.step(ALT_F3, "inspect native Advance codes", '[AdvToPos:3"]A[AdvRgt:1"]B')
        name = "HORIZ.WP"
    else:
        run.step("top", "type the first line")
        for _ in range(51):
            run.step(ENTER, "move one baseline toward the bottom")
        run.step("bottom", "type at nine and a half inches", 'Pg 1 Ln 9.5"')
        advance(run, "2", "3")
        run.step("Z", "type at the clamped baseline", "bottomZ")
        run.wait('Pg 1 Ln 10" Pos 1.7"')
        run.step(ALT_F3, "inspect the requested distance", 'bottom[AdvDn:3"]Z')
        name = "BOUNDARY.WP"
    run.step(ALT_F3, "restore the normal screen")
    reference = captures / "loaded-no" / "INPUT.WP" if captures and case == "boundary" else ref / name
    assert run.save(name) == reference.read_bytes(), f"{name} differs from DOS"

    output = print_to_disk(run)
    if case == "horizontal":
        assert output == (ref / "HORIZ.PRN").read_bytes()
    else:
        # Check disk delivery against the captured status baselines.
        rows = output.split(b"\r\n")[:-1]
        assert len(output) == 180
        assert len(rows) == 66, len(rows)
        assert rows[57] == b"          bottom", rows[57]
        assert rows[60] == b"                Z\r", rows[60]
    run.step(SWITCH, "open a fresh second document", "Doc 2 Pg")
    run.retrieve(name)
    if case == "boundary":
        for key in (b"\x1bOH", b"\x1bOH", b"\x1b[B"):
            run.step(key, "move to the end of the reopened document")
        run.wait('Pg 1 Ln 10" Pos 1.7"')
    run.step(ALT_F3, "inspect the reopened Advance owner",
             '[AdvToPos:3"]' if case == "horizontal" else '[AdvDn:3"]')
    run.step(ALT_F3, "restore normal editing")
    assert run.save("COPY.WP") == reference.read_bytes()
    close_second_document(run)
    run.exit_application()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("binary", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("case", choices=("horizontal", "boundary", "loaded-yes", "loaded-no", "wrapped"))
    parser.add_argument("--captures", type=Path, help="local DOS Advance batch directory")
    args = parser.parse_args()
    case = args.case
    run = Run(args.repo.resolve(), args.binary.resolve(), args.out.resolve(), classic_canvas=True)
    failure = None
    try:
        if case in ("loaded-yes", "loaded-no"):
            edited_reopen(run, case == "loaded-yes", args.captures)
        elif case == "wrapped":
            wrapped(run, args.captures)
        else:
            exercise(run, case, args.captures)
    except Exception as exc:
        failure = repr(exc)
        raise
    finally:
        run.finish(failure, "Advance " + case)
