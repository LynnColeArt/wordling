#!/usr/bin/env python3
"""Check original structural Undelete against the normal Wordling CLI."""
import argparse
from pathlib import Path

from merge_authoring import FIXTURES, body
from physical_cases import RIGHT, close_doc2
from qualification import ENTER, F1, F7, F11, SWITCH, Run, sha

DELETE = b"\x1b[3~"
BACKSPACE = b"\x7f"
PROMPT = "Undelete: 1 Restore; 2 Previous Deletion: 0"
TRIPLE_DOS_SHA = "3130c4eb60a245fff778dbe6605be0dbd658480c4b2930919edbd676e5c66ad2"
CROSS_DOS_SHA = "976f6e23b93a8fbecd9e39848a611980d54015462a5cec9dd0f55556d6a94c8f"
PLAIN = "docs/research/reference-runs/2026-10-29-smoke-03/CMD51-066/NEWTEST.WP5"


def right(run, count):
    for _ in range(count):
        run.step(RIGHT, "advance over one native owner")


def fresh(run, name):
    run.step(SWITCH, "switch to a fresh document screen", "Doc 2 Pg")
    run.retrieve(name)
    if not any("Press Reveal Codes" in row for row in run.rows()):
        run.step(F11, "open the original Reveal Codes pane", "Press Reveal Codes")


def preview(run, lower, active=None):
    run.wait(PROMPT, 11)
    run.wait("Press Reveal Codes to restore screen", 24)
    assert run.p.terminal.roles(11)[0] == 0x1f
    assert run.p.terminal.roles(11)[9] == 0x17
    assert run.p.terminal.roles(11)[42] == 0x1f
    run.wait(lower)
    if active is None:
        return
    row, col = next((i, text.index(lower)) for i, text in enumerate(run.rows()) if lower in text)
    assert run.p.terminal.roles(row)[col + active] == 0x47


def ring(run, original):
    fresh(run, "PRIMARY.WP")
    run.step(DELETE, "remove H")
    right(run, 1)
    run.step(DELETE, "remove the first l in a new group")
    right(run, 1)
    run.step(DELETE, "remove o in a third group")
    right(run, 1)
    run.step(DELETE, "remove the FIELD owner in a fourth group", "el 1~")
    run.step(F1, "preview the latest retained owner")
    preview(run, "el [Block][Mrg:FIELD]1~[HPg]", 21)
    run.step("2", "preview the prior o")
    preview(run, "el [Block]o1~[HPg]")
    run.step("2", "preview the prior l")
    preview(run, "el [Block]l1~[HPg]")
    run.step("2", "wrap the original three-entry history ring")
    preview(run, "el [Block][Mrg:FIELD]1~[HPg]", 21)
    run.step(ENTER, "default zero cancels without publishing the preview")
    run.wait("el 1~")
    run.step(F1, "reopen for a literal zero answer")
    run.wait(PROMPT)
    run.step("0", "cancel without publishing the preview")
    run.wait("el 1~")
    run.step(F1, "reopen for Escape cancellation")
    run.wait(PROMPT)
    run.step(b"\x1b", "cancel with Escape")
    run.wait("el 1~")
    run.step(F1, "reopen the unchanged history")
    preview(run, "el [Block][Mrg:FIELD]1~[HPg]", 21)
    run.step("1", "restore FIELD at the current insertion gap", "el [Mrg:FIELD]1~[HPg]")
    assert body(run.save("RING.WP")) == b"el " + original[6:]
    close_doc2(run)


def operand(run, original):
    fresh(run, "PRIMARY.WP")
    right(run, 3)
    run.step(BACKSPACE, "remove an ordinary literal", "Helo ")
    run.step("l", "restore the literal by typing without discarding history", "Hello ")
    right(run, 4)
    run.step("2", "insert a valid operand digit", "[Mrg:FIELD]21~")
    run.step(DELETE, "remove the old operand digit", "[Mrg:FIELD]2~")
    run.step(F1, "preview the operand digit")
    preview(run, "Hello [Mrg:FIELD]2[Block]1~[HPg]", 26)
    run.step("1", "restore only the native digit", "[Mrg:FIELD]21~[HPg]")
    assert body(run.save("OPERAND.WP")) == original.replace(b"1~", b"21~", 1)
    close_doc2(run)


def adjacent(run, original):
    fresh(run, "PRIMARY.WP")
    right(run, 6)
    run.step(DELETE, "remove the FIELD owner", "Hello 1~")
    run.step(DELETE, "remove the now-literal digit without moving", "Hello ~")
    run.step(F1, "preview both owners as one group")
    preview(run, "Hello [Block][Mrg:FIELD]1~[HPg]", 25)
    run.step("1", "restore the whole adjacent group", "Hello [Mrg:FIELD]1~[HPg]")
    assert body(run.save("ADJACENT.WP")) == original
    close_doc2(run)


def secondary(run, original, owner, expected_offset=324, expected_sha=None):
    fresh(run, "SECOND.WP")
    if owner == "end-record":
        right(run, 7)
        lower = "[Block][Mrg:END RECORD][HPg]"
        active = 23
        restored = "[Mrg:END RECORD][HPg]"
    else:
        right(run, 5)
        lower = "Alice[Block][Mrg:END FIELD][HRt]"
        active = 27
        restored = "Alice[Mrg:END FIELD][HRt]"
    run.step(DELETE, "remove the native " + owner)
    if owner in ("cache", "triple"):
        run.step(DELETE, "remove the exposed return and regenerate its cache")
        active = None
    if owner == "triple":
        run.step(DELETE, "remove the remaining End Record in the same group")
    run.step(F1, "preview " + owner)
    preview(run, lower, active)
    run.step("1", "restore native " + owner)
    run.wait(restored)
    data = run.save(owner.upper().replace("-", "")[:8] + ".WP", expected_offset=expected_offset)
    assert body(data) == original
    if expected_sha is not None:
        assert sha(data) == expected_sha, sha(data)
    close_doc2(run)


def delete_doc1_field(run):
    run.retrieve("PRIMARY.WP")
    run.step(F11, "open Reveal Codes in Doc 1", "Press Reveal Codes")
    right(run, 6)
    run.step(DELETE, "remove the Doc 1 FIELD owner", "Hello 1~")
    run.step(SWITCH, "switch to blank Doc 2", "Doc 2 Pg")
    run.step(F11, "open Reveal Codes in blank Doc 2", "Press Reveal Codes")
    run.step(F1, "Doc 2 previews the owner deleted in Doc 1")
    preview(run, "[Block][Mrg:FIELD]")


def cross_restore(run):
    delete_doc1_field(run)
    run.step("1", "restore the exact stand-alone FIELD in blank Doc 2", "[Mrg:FIELD]")
    data = run.save("CROSS.WP")
    assert len(data) == 332 and sha(data) == CROSS_DOS_SHA
    close_doc2(run)
    run.wait("Hello 1~")


def cross_lifecycle(run):
    delete_doc1_field(run)
    run.step(F1, "cancel the cross-screen preview")
    run.retrieve("PLAIN.WP")
    run.step(F1, "history survives Retrieve on the blank screen")
    preview(run, "[Block][Mrg:FIELD]")
    run.step(F1, "leave the retrieved Doc 2 untouched")
    run.step("q", "type a literal at the beginning of the loaded source")
    run.start_of_document()
    run.step(DELETE, "delete q to add the newest shared group")
    run.step(SWITCH, "return to Doc 1", "Doc 1 Pg")
    run.step(F1, "Doc 1 previews the q deleted in Doc 2")
    preview(run, "Hello [Block]q1~[HPg]", 14)
    run.step("2", "the older FIELD is still in the same ring")
    preview(run, "Hello [Block][Mrg:FIELD]1~[HPg]")
    run.step(F1, "cancel to leave Doc 1 unchanged")
    run.step(SWITCH, "return to Doc 2", "Doc 2 Pg")
    close_doc2(run)
    run.step(F1, "closing Doc 2 retains its newest group")
    preview(run, "Hello [Block]q1~[HPg]", 14)
    run.step(F1, "cancel to open a fresh Doc 2")
    run.step(SWITCH, "acquire fresh Doc 2", "Doc 2 Pg")
    run.step(F11, "open Reveal Codes")
    run.step(F1, "fresh Doc 2 sees the same newest q")
    preview(run, "[Block]q")
    run.step(F1, "cancel before closing Doc 2")
    close_doc2(run)
    run.step(F7, "leave the remaining screen", "Save document?")
    run.step("n", "decline saving the deleted FIELD", "Exit WP?")
    run.step("n", "clear Doc 1 and continue")
    run.wait("Doc 1 Pg")
    if not any("Press Reveal Codes" in row for row in run.rows()):
        run.step(F11, "open Reveal Codes in renewed Doc 1")
    run.step(F1, "renewed Doc 1 still previews q")
    preview(run, "[Block]q")
    run.step(F1, "cancel before exiting")


def ordinary_cross_restore(run):
    run.step("AZ", "type ordinary text in Doc 1", "AZ")
    for _ in range(2):
        run.step(b"\x1b[D", "move left to A")
    run.step(DELETE, "delete A in Doc 1", "Z", 1)
    run.step(SWITCH, "switch to blank Doc 2", "Doc 2 Pg")
    run.step(F1, "preview the ordinary deletion in Doc 2", PROMPT, 24)
    assert run.rows()[1].strip() == "A"
    run.step("1", "restore A in Doc 2", "Doc 2 Pg")
    assert run.rows()[1].strip() == "A"
    close_doc2(run)
    assert run.rows()[1].strip() == "Z"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("binary", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--case", choices=("structural", "cross-restore", "cross-lifecycle", "triple-original", "ordinary-cross"), default="structural")
    args = parser.parse_args()
    run = Run(args.repo.resolve(), args.binary.resolve(), args.output.resolve())
    failure = None
    try:
        fixture = run.repo / FIXTURES
        primary, data = fixture / "PRIMARY.WP5", fixture / "SECOND.WP5"
        run.seed(primary, "PRIMARY.WP")
        run.seed(data, "SECOND.WP")
        if args.case == "cross-lifecycle":
            run.seed(run.repo / PLAIN, "PLAIN.WP")
        run.launch()
        if args.case == "structural":
            run.set_fast_save(False)
            original = body(primary.read_bytes())
            ring(run, original)
            operand(run, original)
            adjacent(run, original)
            for owner in ("end-field", "end-record", "cache", "triple"):
                secondary(run, body(data.read_bytes()), owner)
        elif args.case == "cross-restore":
            cross_restore(run)
        elif args.case == "triple-original":
            secondary(run, body(data.read_bytes()), "triple", 564, TRIPLE_DOS_SHA)
        elif args.case == "ordinary-cross":
            ordinary_cross_restore(run)
        else:
            cross_lifecycle(run)
        run.exit_application()
    except Exception as err:
        failure = repr(err)
        raise
    finally:
        run.finish(failure, "structural merge Undelete")


if __name__ == "__main__":
    main()
