#!/usr/bin/env python3
"""Author native merge controls over the real Linux terminal and execute them."""
import argparse
from pathlib import Path

from physical_cases import RIGHT, close_doc2
from qualification import ENTER, F1, F10, F11, SWITCH, Run, sha

SHIFT_F9 = b"\x1b[20;2~"
F9 = b"\x1b[20~"
CTRL_ENTER = b"\x1b[13;5u"
CTRL_F9 = b"\x1b[20;5~"
FIXTURES = "docs/research/reference-runs/2026-10-29-extended-04/CMD51-134"


def body(raw):
    return raw[int.from_bytes(raw[4:8], "little"):]


def exercise(run):
    run.launch()
    run.set_fast_save(False)
    run.step("Hello ", "type ordinary primary text", "Hello")
    run.step(SHIFT_F9, "Shift+F9 opens the original Merge Codes prompt", "1 Field; 2 End Record", 24)
    run.step("1", "open numeric Field operand", "Enter Field:", 24)
    run.step("2", "type a draft field number", "Enter Field: 2", 24)
    run.step(F1, "cancel the field draft without modifying text")
    assert not any("{FIELD}" in row for row in run.rows())
    run.step(SHIFT_F9, "reopen Merge Codes", "1 Field; 2 End Record", 24)
    run.step("1", "open Field operand again", "Enter Field:", 24)
    run.step("1", "enter Field 1")
    run.step(ENTER, "confirm native Field insertion", "Hello {FIELD}1~")
    run.step(CTRL_ENTER, "append original primary hard page", "Doc 1 Pg 2")
    run.step(F11, "show the native merge and hard page owners", "Hello [Mrg:FIELD]1~[HPg]")
    run.step(F11, "restore full screen")
    primary = run.save("PRIM.WP")
    assert body(primary) == body((run.repo / FIXTURES / "PRIMARY.WP5").read_bytes())
    run.step(SWITCH, "switch to New Doc 2", "Doc 2 Pg")
    for name in ("Alice", "Bob"):
        run.step(name, "type the data field", name)
        run.step(F9, "F9 inserts the structural End Field and return", name + "{END FIELD}")
        run.wait("Field: 2")
        run.step(SHIFT_F9, "open the original Merge Codes prompt", "1 Field; 2 End Record", 24)
        run.step("2", "insert End Record and page break", "{END RECORD}")
        run.wait("Field: 1")
    run.step(F11, "verify secondary native owner labels", "[Mrg:END FIELD][HRt]")
    run.wait("[Mrg:END RECORD][HPg]")
    run.step(F11, "close Reveal")
    secondary = run.save("SECOND.WP")
    assert body(secondary) == body((run.repo / FIXTURES / "SECOND.WP5").read_bytes())
    close_doc2(run)

    run.step(SWITCH, "fresh receiver in Doc 2", "Doc 2 Pg")
    run.step(CTRL_F9, "original merge command", "1 Merge; 2 Sort")
    run.step("1", "open primary filename", "Primary file:")
    run.step("PRIM.WP", "choose editor-authored primary")
    run.step(ENTER, "open secondary filename", "Secondary file:")
    run.step("SECOND.WP", "choose editor-authored secondary")
    run.step(ENTER, "merge real authored files", "Hello Alice")
    run.wait("Hello Bob")
    close_doc2(run)

    run.step(SWITCH, "fresh screen for structural deletion", "Doc 2 Pg")
    run.retrieve("PRIM.WP")
    run.step(F11, "show retrieved primary code", "[Mrg:FIELD]")
    run.start_of_document()
    for _ in range(3):
        run.step(RIGHT, "move to an ordinary literal inside the merge source")
    run.step(b"\x7f", "Backspace removes just the adjacent ordinary literal", "Helo [Mrg:FIELD]1~")
    run.step("l", "restore the same ordinary literal", "Hello [Mrg:FIELD]1~")
    for _ in range(4):
        run.step(RIGHT, "advance inside the native Field operand")
    run.step("2", "insert a new operand digit", "[Mrg:FIELD]21~")
    run.step(b"\x1b[3~", "remove the old operand digit", "[Mrg:FIELD]2~")
    corrected = run.save("OPERAND.WP")
    assert body(corrected) == body(primary).replace(b"1~", b"2~", 1)
    run.step(b"\x1b[D", "return to the corrected operand")
    run.step("1", "restore the original operand")
    run.step(b"\x1b[3~", "remove the temporary operand digit", "[Mrg:FIELD]1~")
    run.start_of_document()
    for _ in range(6):
        run.step(RIGHT, "advance to the native Field owner")
    run.step(b"\x1b[3~", "Delete removes the Field owner only", "Hello 1~")
    result = run.save("DEL.WP")
    assert body(result) == body(primary).replace(bytes.fromhex("de360400040036de"), b"", 1)
    close_doc2(run)
    delete_secondary_owners(run)
    nested(run)
    wrapper_primary(run)
    wide_secondary(run)
    exact_field_digits(run)
    run.exit_application()


def delete_secondary_owners(run):
    run.step(SWITCH, "fresh screen for secondary owner deletion", "Doc 2 Pg")
    run.retrieve("SECOND.WP")
    run.step(F11, "show original secondary owners", "Alice[Mrg:END FIELD][HRt]")
    run.start_of_document()
    for _ in "Alice":
        run.step(RIGHT, "advance to the native End Field owner")
    for name, cue, expected in (
        ("NOFIELD.WP", "Alice[HRt]", "10aa4f69fbabfbca06fb1e00cb17f82fb5d674f7f5ad16dcfc0b837ca2bdce07"),
        ("NORETURN.WP", "Alice[Mrg:END RECORD][HPg]", "f3bff0f1b58e543c92ca1a3113cd121ab812c4467597dc7d2d203b8e43a7b178"),
        ("NORECORD.WP", "Alice[HPg]", "56d02375129b72eda47d280b60c6af134f73d8bfa82989cbbc19ed6c00f8bf00"),
    ):
        run.step(b"\x1b[3~", "delete only the adjacent visible owner", cue)
        assert sha(run.save(name)) == expected, name
    row = next(i for i, line in enumerate(run.rows()) if "Alice[HPg]" in line)
    assert all(style[1] == 41 for style in run.p.terminal.styles[row][5:10])
    close_doc2(run)


def named(run, name, operand=None):
    run.step(SHIFT_F9, "open original Merge Codes", "1 Field; 2 End Record", 24)
    run.step("6", "open original More chooser", "Name Search", 24)
    run.wait("{ASSIGN}", 1)
    for letter in name:
        run.step(letter, "type original Name Search")
    run.wait("{" + name + "}")
    run.step(ENTER, "select the located native merge function")
    if operand is not None:
        run.wait("Enter Filename:", 24)
        run.step(operand, "enter the native DOS filename operand")
        run.step(ENTER, "commit the filename operand")


def field(run, number):
    run.step(SHIFT_F9, "open original Merge Codes", "1 Field; 2 End Record", 24)
    run.step("1", "open numeric Field operand", "Enter Field:", 24)
    run.step(str(number), "enter field number")
    run.step(ENTER, "commit Field operand", "{FIELD}" + str(number) + "~")


def nested(run):
    originals = run.repo / "docs/research/reference-runs/2026-10-29-iteration-01/CMD51-223"
    (run.p.work / "OUT").mkdir()
    run.step(SWITCH, "fresh screen for nested primary child", "Doc 2 Pg")
    named(run, "PAGE ON")
    run.step("C", "type nested record label", "{PAGE ON}C")
    field(run, 1)
    run.step(ENTER, "append original primary hard return")
    run.step(F10, "save nested primary at exact native DOS path", "Document to be saved:")
    run.step(r"C:\OUT\CHILD", "type destination within workspace")
    run.step(ENTER, "publish authored child")
    child_path = run.p.work / "OUT/CHILD"
    run.until(child_path.is_file, "exact nested file exists")
    assert body(child_path.read_bytes()) == body((originals / "CHILD.WP5").read_bytes())
    close_doc2(run)

    run.step(SWITCH, "fresh screen for nested primary parent", "Doc 2 Pg")
    run.step(SHIFT_F9, "open original Merge Codes", "1 Field; 2 End Record", 24)
    run.step("4", "original direct Page Off", "{PAGE OFF}")
    run.step("P", "type parent record label", "{PAGE OFF}P")
    field(run, 1)
    run.step(ENTER, "append original primary hard return")
    named(run, "NEST PRIMARY", r"C:\OUT\CHILD")
    run.step("R", "type parent resumption text", r"{NEST PRIMARY}C:\OUT\CHILD~R")
    run.step(ENTER, "append parent terminal hard return")
    run.step(F11, "show native page control", "[Mrg:PAGE OFF]")
    run.wait(r"[Mrg:NEST PRIMARY]C:\OUT\CHILD~R[HRt]")
    run.step(F11, "restore editor")
    parent = run.save("NESTED.WP")
    assert body(parent) == body((originals / "PRIMARY.WP5").read_bytes())
    close_doc2(run)

    run.step(SWITCH, "fresh receiver for the authored nested program", "Doc 2 Pg")
    run.step(CTRL_F9, "original merge command", "1 Merge; 2 Sort")
    run.step("1", "open primary filename", "Primary file:")
    run.step("NESTED.WP", "choose editor-authored parent")
    run.step(ENTER, "open secondary filename", "Secondary file:")
    run.step("SECOND.WP", "choose editor-authored secondary")
    run.step(ENTER, "merge all editor-authored native inputs", "PAlice")
    for text in ("CAlice", "PBob", "CBob"):
        run.wait(text)
    close_doc2(run)


def wide_secondary(run):
    original = run.repo / "docs/research/everyday-contract-2026-11-05/native-merge/wide/53/SECOND.WP5"
    run.step(SWITCH, "fresh screen for a wide secondary", "Doc 2 Pg")
    for prefix in ("A", "B"):
        for number in range(1, 54):
            run.step(prefix + str(number), "type a field value")
            run.step(F9, "end the numbered field")
        run.wait("Field: 54")
        run.step(SHIFT_F9, "open Merge Codes", "1 Field; 2 End Record", 24)
        run.step("2", "end the 53-field record")
        run.wait("Field: 1")
    assert run.save("WIDE.WP") == original.read_bytes()
    close_doc2(run)


def wrapper_primary(run):
    original = run.repo / "docs/research/everyday-contract-2026-11-05/native-merge/wide/wrapper1"
    run.step(SWITCH, "fresh screen for the wrapper-only primary", "Doc 2 Pg")
    run.step(SHIFT_F9, "open the original Merge Codes prompt", "1 Field; 2 End Record", 24)
    run.step("4", "insert Page Off", "{PAGE OFF}")
    named(run, "NEST PRIMARY", r"C:\OUT\CHILD")
    assert run.save("WRAPPER.WP") == (original / "PRIMARY.WP5").read_bytes()
    close_doc2(run)

    run.step(SWITCH, "fresh receiver for the authored wrapper", "Doc 2 Pg")
    run.set_fast_save(True)
    run.step(CTRL_F9, "original merge command", "1 Merge; 2 Sort")
    run.step("1", "open primary filename", "Primary file:")
    run.step("WRAPPER.WP", "choose editor-authored wrapper")
    run.step(ENTER, "open secondary filename", "Secondary file:")
    run.step("SECOND.WP", "choose editor-authored secondary")
    run.step(ENTER, "merge from the authored wrapper", "CAlice")
    run.wait("CBob")
    assert run.save("WRAPPED.WP", expected_offset=820) == (original / "MERGED.WP5").read_bytes()
    run.set_fast_save(False)
    close_doc2(run)


def exact_field_digits(run):
    original = run.repo / "docs/research/everyday-contract-2026-11-05/native-merge/wide/DIGITS.WP"
    run.step(SWITCH, "fresh screen for exact Field operands", "Doc 2 Pg")
    for number in ("0", "001", "1000", "32767", "65535", "65536"):
        field(run, number)
    assert run.save("DIGITS.WP") == original.read_bytes()
    close_doc2(run)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("binary", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    run = Run(args.repo.resolve(), args.binary.resolve(), args.output.resolve())
    failure = None
    try:
        exercise(run)
    except Exception as err:
        failure = repr(err)
        raise
    finally:
        run.finish(failure, "original structural merge authoring")


if __name__ == "__main__":
    main()
