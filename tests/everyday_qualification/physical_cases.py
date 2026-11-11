#!/usr/bin/env python3
"""Supplement the production WP84/WP85/WP89 PTY probes with native journeys."""
import argparse
from pathlib import Path

from qualification import (Run, F1, F2, F5, F6, F7, F8, F10, F11, ENTER,
                           HOME, UP, SETUP, SWITCH, RETRIEVE, PROOF, REF, native, choose_suggestion)

F3 = b"\x1bOR"
LEFT, RIGHT, DOWN = b"\x1b[D", b"\x1b[C", b"\x1b[B"
END, DELETE, BACKSPACE, INSERT = b"\x1bOF", b"\x1b[3~", b"\x7f", b"\x1b[2~"
PGDOWN, PGUP, BLOCK = b"\x1b[6~", b"\x1b[5~", b"\x1b[24~"
SEARCH_BACK = b"\x1b[1;2Q"


def press(run, *keys):
    for key in keys:
        run.step(key, "physical " + repr(key))


def body(run, name):
    return native(run.p.work / name)[2]


def help_and_focus(run):
    run.launch()
    run.step("FOCUS", "establish editable content", "FOCUS", 1)
    for cancel, name in ((b"\x1b", "Escape"), (b" ", "Space")):
        run.step(b"\x1b=", "Alt+= focuses inactive bar", "File Edit", 0)
        run.step("l", "open Layout pull-down", "Line", 1)
        run.step("j", "open Justify child", "Left", 14)
        assert run.p.terminal.styles[14][37][1] == 41
        run.step(cancel, name + " returns focus to parent while drawing remains")
        run.wait("Left", 14)
        assert run.p.terminal.styles[14][37][1] != 41
        run.step(UP, "Up reaches neighboring Endnote child", "Create", 12)
        assert run.p.terminal.styles[12][37][1] == 41
        run.step(F7, "leave menus")
    for keys, name in ((F10, "Save"), (F2, "Search"), (F6, "Bold on/off"),
                       (F8, "Underline on/off"), (b"\x1b[13;3~", "Reveal Codes"),
                       (F5, "List")):
        run.step(F3, "enter F3 Help", "WP 5.1   03/09/92", 0)
        run.step(keys, "help topic " + name, name, 0)
        run.step(ENTER, "return to same editing document", "FOCUS", 1)
    run.step("TYPED", "resume ordinary typing", "FOCUSTYPED", 1)
    run.save("FOCUS.WP")
    assert body(run, "FOCUS.WP") == b"FOCUSTYPED"
    run.exit_application()


def flow(run):
    run.launch()
    run.step("A faithful reconstruction needs more than a blue screen. Menus, prompts, wrapping, and cursor movement must work together.",
             "write the original wrapping sample", "A faithful reconstruction")
    press(run, ENTER, ENTER, b"\t")
    run.step("Tab alpha alpha", "ordinary text after a native Tab")
    press(run, ENTER)
    run.step("X" * 66, "write a long unbroken word")
    press(run, ENTER)
    for number in range(1, 111, 10):
        run.step(b"".join(f"Physical line {line:03d}\r".encode() for line in range(number, number + 10)),
                 f"ordinary terminal typing through line {number + 9}")
    run.wait("Doc 1 Pg 3")
    first = run.save("THREE.WP", body_fragment=b"Physical line 110")
    assert b"\xc1\x02" in body(run, "THREE.WP")
    assert b"\x90" in body(run, "THREE.WP")
    run.step("TAIL", "continue after first save", "TAIL")
    assert run.save("THREE.WP", replace=True, prefill=True, body_fragment=b"TAIL") != first
    run.step(SWITCH, "open Doc 2 for real reopen", "Doc 2 Pg")
    run.retrieve("THREE.WP")
    run.wait("A faithful reconstruction")
    run.step("OPENED ", "continue editing the retrieved file", "OPENED")
    run.save("REOPEN.WP", body_fragment=b"OPENED ")
    close_doc2(run)
    run.exit_application()


def close_doc2(run):
    run.step(F7, "F7 on Doc 2", "Save document?")
    run.step("n", "decline another Doc 2 save", "Exit doc 2?")
    run.step("y", "close only Doc 2 and restore Doc 1", "Doc 1 Pg")


def corrections(run):
    run.launch()
    run.step("ABC", "write first paragraph")
    press(run, ENTER)
    run.step("DEF", "write second paragraph")
    run.save("BACK.WP")
    assert body(run, "BACK.WP") == b"ABC\nDEF"
    run.step(SWITCH, "open blank second screen", "Doc 2 Pg")
    run.retrieve("BACK.WP")
    press(run, DELETE, HOME, HOME, DOWN, BACKSPACE, UP, DOWN, BACKSPACE)
    run.step(F1, "preview most recent deletion", "Undelete: 1 Restore")
    assert [ch for i,ch in enumerate(run.rows()[2]) if run.p.terminal.styles[2][i][1] == 41 and ch != " "] == ["E"]
    run.step("2", "Previous Deletion displays F", "Undelete:")
    assert run.rows()[2][1] == "F" and run.p.terminal.styles[2][1][1] == 41
    run.step("2", "Previous Deletion displays oldest A", "Undelete:")
    assert run.rows()[2][1] == "A" and run.p.terminal.styles[2][1][1] == 41
    run.step(F1, "cancel the native preview")
    run.start_of_document()
    press(run, DOWN, BACKSPACE)
    run.wait("BCD")
    run.step(F1, "preview deleted hard return", "Undelete:")
    run.step("1", "restore the native hard return")
    run.save("THREE.WP")
    assert body(run, "THREE.WP") == b"BC\nD"
    close_doc2(run)
    run.step(SWITCH, "fresh Doc 2 after close", "Doc 2 Pg")
    run.step("ABC", "new selection source")
    press(run, BLOCK, LEFT, LEFT, LEFT)
    run.step(DELETE, "delete backward selection", "Delete Block? No (Yes)")
    run.step(ENTER, "default No retains block", "ABC")
    run.step(DELETE, "ask again without discarding selection", "Delete Block? No (Yes)")
    run.step("y", "confirm block removal")
    run.step(F1, "preview deleted block", "Undelete:")
    run.step("1", "restore the selected bytes", "ABC")
    run.start_of_document()
    press(run, INSERT)
    run.step("X", "overwrite the first character", "XBC")
    press(run, INSERT)
    run.start_of_document()
    run.step(b"\x1b[1;3S", "Alt+F4 starts forward native selection")
    press(run, RIGHT, RIGHT)
    assert [ch for i,ch in enumerate(run.rows()[1]) if run.p.terminal.styles[1][i][1] == 41 and ch != " "] == ["X","B"]
    run.step(F1, "cancel forward selection")
    assert all(style[1] != 41 for style in run.p.terminal.styles[1][:3])
    run.save("BLOCK.WP")
    assert body(run, "BLOCK.WP") == b"XBC"
    close_doc2(run)
    run.exit_application()


def attributes(run):
    run.launch()
    press(run, F6)
    run.step("B", "text under Bold")
    press(run, F8)
    run.step("C", "text under Bold and Underline")
    press(run, F6)
    run.step("D", "text under Underline")
    press(run, F8)
    want = b"\xc3\x0c\xc3B\xc3\x0e\xc3C\xc4\x0c\xc4D\xc4\x0e\xc4"
    run.save("ATTR.WP")
    assert body(run, "ATTR.WP") == want
    run.step(SWITCH, "new screen for loaded attributes", "Doc 2 Pg")
    run.retrieve("ATTR.WP")
    run.step(F11, "reveal loaded nested attribute pairs", "Press Reveal Codes")
    run.wait("[BOLD]B[UND]C[bold]D[und]")
    run.step(DELETE, "delete exact Bold pair in Reveal")
    run.wait("B[UND]CD[und]")
    run.step(F2, "begin loaded Reveal code search", "Srch:", 11)
    run.step(F8, "insert native Underline search code", "[UND]", 11)
    run.step(F2, "match the native UnderlineOn owner", 'Pos 1.1"', 11)
    run.step(F11, "close Reveal")
    run.save("NOBOLD.WP")
    assert body(run, "NOBOLD.WP") == b"B\xc3\x0e\xc3CD\xc4\x0e\xc4"
    assert body(run, "ATTR.WP") == want
    close_doc2(run)
    run.exit_application()


def navigation_search(run):
    run.launch()
    run.step(b"ABCDEFGHIJ\rxy\r1234567890", "write unequal physical lines")
    run.start_of_document()
    run.step(END, "End goes to the long first line's end", 'Pos 2"')
    run.step(DOWN, "Down clips to the shorter line", 'Pos 1.2"')
    run.step(DOWN, "Down recovers the desired column", 'Pos 2"')
    run.step(F11, "reveal same native location", 'Pos 2"', 11)
    run.step(UP, "Reveal Up clips to shorter line", 'Pos 1.2"', 11)
    run.step(UP, "Reveal Up recovers desired column", 'Pos 2"', 11)
    run.step(F11, "close Reveal without losing the caret", 'Pos 2"', 24)
    run.step(SWITCH, "new screen for native search", "Doc 2 Pg")
    run.step("alpha beta alpha gamma alpha", "write three literal matches")
    run.save("SEARCH.WP")
    run.start_of_document()
    run.step(F2, "forward search prompt", "-> Srch:")
    run.step("alpha", "enter repeated search text")
    run.step(F2, "first forward match ends after alpha", 'Pos 1.5"')
    run.step(F2, "forward repeat prefill", "Srch: alpha")
    run.step(F2, "repeat ends after second alpha", 'Pos 2.6"')
    run.step(SEARCH_BACK, "backward search prompt", "<- Srch:")
    run.step(SEARCH_BACK, "backward search ends at prior match", 'Pos 1.5"')
    run.step(b"\x1b=", "focus original menu bar")
    run.step("s", "open Search menu", "Next")
    run.step("n", "Search Next reaches the same authoritative caret", 'Pos 2.6"')
    run.step(b"\x1b=", "focus menu bar again")
    run.step("s", "open Search menu", "Previous")
    run.step("p", "Search Previous reaches the same authoritative caret", 'Pos 1.5"')
    run.step(F11, "Reveal uses the same search caret", "Press Reveal Codes")
    run.step(F2, "begin a search to cancel", "Srch:")
    run.step("discardme", "partial query")
    run.step(F1, "cancel partial query", 'Pos 1.5"')
    run.step(F11, "close Reveal")
    run.save("FINDCOPY.WP")
    assert (run.p.work / "FINDCOPY.WP").read_bytes() == (run.p.work / "SEARCH.WP").read_bytes()
    close_doc2(run)
    run.exit_application()


def wrapped_search(run):
    flow = run.repo / "internal/tui/evidence/everyday/FLOW.WP"
    run.seed(flow, "FLOW.WP")
    run.launch()
    run.retrieve("FLOW.WP")
    run.step(F2, "open original forward search", "Srch:", 24)
    run.step("Menus, prompts", "literal match across native soft return")
    run.step(F2, "finish cross-line search at the original caret", 'Ln 1.17" Pos 1.7"', 24)
    run.step(F11, "same physical caret in Reveal", 'Ln 1.17" Pos 1.7"', 11)
    run.step(F2, "open original Reveal code search", "Srch:", 11)
    run.step(F8, "type exact UnderlineOn owner", "[UND]", 11)
    run.step(F2, "land after the original UnderlineOn", 'Ln 1.5" Pos 1.6"', 11)
    run.step(F11, "return to ordinary editing")
    assert run.save("FOUND.WP") == flow.read_bytes()
    run.exit_application()


def files(run):
    flow = run.repo / "internal/tui/evidence/everyday/FLOW.WP"
    other = run.repo / REF / "files/exports/A.WP"
    child = run.p.work / "CHILD"
    child.mkdir()
    (child / "DEEP.WP").write_bytes(other.read_bytes())
    for i in range(42):
        run.seed(other, f"F{i:02d}.WP")
    run.seed(flow, "FLOW.WP")
    run.launch()
    run.step("CURRENT ", "retain this current editor buffer")
    run.step(RETRIEVE, "open Retrieve", "Document to be retrieved:")
    run.step(F5, "F5 from Retrieve", "Dir C:\\*.*")
    run.step(ENTER, "confirm root listing", "Directory C:\\*.*", 0)
    before = run.rows()[3]
    run.step(PGDOWN, "page on overflowing file list")
    assert run.rows()[3] != before
    run.step(PGUP, "page back to first rows")
    assert run.rows()[3] == before
    run.step("n", "find directory")
    run.step(r"\CHILD", "select exact child")
    run.step(ENTER, "finish Name Search")
    run.step("6", "Look enters a selected directory", "Dir C:\\CHILD\\*.*")
    run.step(ENTER, "confirm child listing", "Directory C:\\CHILD\\*.*", 0)
    run.step("n", "select parent")
    run.step("..", "look up parent row")
    run.step(ENTER, "finish parent selection")
    run.step("6", "request parent listing", "Dir C:\\*.*")
    run.step(ENTER, "confirm parent", "Directory C:\\*.*", 0)
    run.step("n", "find exact native file")
    run.step("FLOW.WP", "select original FLOW")
    run.step(ENTER, "finish native selection")
    run.step("1", "ask before inserting into occupied document", "Retrieve into current document? No (Yes)")
    run.step(ENTER, "decline insertion, retain list and selection", "N Name Search:")
    run.step("1", "ask again for same selected entry", "Retrieve into current document? No (Yes)")
    run.step("y", "confirm original occupied retrieval", "Doc 1 Pg 3")
    run.start_of_document()
    run.wait("CURRENT A faithful reconstruction")
    run.save("OCCUPIED.WP", body_fragment=b"CURRENT A faithful reconstruction")
    assert (run.p.work / "FLOW.WP").read_bytes() == flow.read_bytes()
    run.exit_application()


def choose_backup(run, yes):
    run.step(SETUP, "Shift+F1 Setup", "Setup", 0)
    run.step("3", "Setup Environment", "Setup: Environment", 0)
    run.step("1", "Setup Backup", "Setup: Backup", 0)
    run.step("2", "Original Document Backup choice", "Selection: 2", 24)
    run.step("y" if yes else "n", "settle original backup choice", "Selection: 0", 24)
    run.step(F7, "return to ordinary editing")


def save_policy(run):
    run.launch()
    run.step("FIRST", "new document text")
    old = run.save("TARGET.WP")
    (run.folder / "first-save.WP").write_bytes(old)
    choose_backup(run, True)
    run.step(" SECOND", "ordinary changed text")
    after = run.save("TARGET.WP", replace=True, prefill=True)
    (run.folder / "backup-replacement.WP").write_bytes(after)
    backup = run.p.work / "TARGET.BK!"
    assert backup.read_bytes() == old
    run.step(" THIRD", "unsaved third change")
    run.step(F10, "attempt existing replacement", "Document to be saved:")
    run.step(ENTER, "settle filename", "Replace TARGET.WP? No (Yes)")
    run.step(ENTER, "default No returns to filename", "Document to be saved:")
    assert (run.p.work / "TARGET.WP").read_bytes() == after and backup.read_bytes() == old
    run.step(F1, "cancel replacement filename")
    choose_backup(run, False)
    disabled = run.save("TARGET.WP", replace=True, prefill=True)
    (run.folder / "disabled-replacement.WP").write_bytes(disabled)
    assert body(run, "TARGET.WP") == b"FIRST SECOND THIRD" and not backup.exists()
    copy = run.save("COPY.WP")
    assert copy == (run.p.work / "TARGET.WP").read_bytes()
    run.step(SWITCH, "start independent Doc 2", "Doc 2 Pg")
    run.step("INDEPENDENT", "unsaved Doc 2 content")
    run.step(F7, "Doc 2 exit first asks save", "Save document?")
    run.step("y", "Save Yes precedes close", "Document to be saved:")
    run.step("DOC2.WP", "give Doc 2 a native name")
    run.step(ENTER, "save and continue close question", "Exit doc 2?")
    assert body(run, "DOC2.WP") == b"INDEPENDENT"
    run.step("y", "close Doc 2", "Doc 1 Pg")
    run.wait("FIRST SECOND THIRD")
    run.exit_application()


def refusal(run):
    flow = run.repo / REF / "flow/exports/FLOW.WP"
    run.seed(flow, "FLOW.WP")
    _, offset, _ = native(flow)
    assert offset == 564
    run.launch()
    run.step(RETRIEVE, "ordinary Retrieve", "Document to be retrieved:")
    run.step("FLOW.WP", "name exact unsupported original Fast Save file")
    run.step(ENTER, "unsupported original prefix is explicitly refused in a blank document", "UnsupportedPrefix")
    run.step(F1, "cancel filename after refusal", "Doc 1 Pg 1")
    run.step("PRESERVE", "write into the still-usable new document", "PRESERVE")
    run.save("UNTOUCH.WP")
    assert body(run, "UNTOUCH.WP") == b"PRESERVE"
    assert (run.p.work / "FLOW.WP").read_bytes() == flow.read_bytes()
    choose_backup(run, True)
    run.step(" UNSAVED", "retain unsaved text during a stale replacement")
    target = run.p.work / "TARGET.WP"
    backup = run.p.work / "TARGET.BK!"
    sentinel = (run.repo / REF / "files/exports/A.WP").read_bytes()
    target.write_bytes((run.p.work / "UNTOUCH.WP").read_bytes())
    backup.write_bytes(sentinel)
    run.step(F10, "open Save for another existing destination", "Document to be saved:")
    run.step("TARGET.WP", "select existing destination distinct from live source")
    run.step(ENTER, "observe exact old destination", "Replace TARGET.WP? No (Yes)")
    replacement = run.repo / "internal/tui/evidence/everyday/FLOW.WP"
    target.write_bytes(replacement.read_bytes())
    run.step("y", "refuse stale original destination", "DestinationChanged")
    assert target.read_bytes() == replacement.read_bytes() and backup.read_bytes() == sentinel
    run.step(F1, "cancel refused destination")
    run.save("KEPT.WP")
    assert body(run, "KEPT.WP") == b"PRESERVE UNSAVED"
    run.step(SWITCH, "open fresh Doc 2", "Doc 2 Pg")
    run.step("CUSTODY ", "establish admitted occupied receiver")
    run.step(RETRIEVE, "ask to retrieve same 564 source into occupied document", "Document to be retrieved:")
    run.step("FLOW.WP", "name exact original file again")
    run.step(ENTER, "ask before consuming read-only body", "Retrieve into current document? No (Yes)")
    run.step("y", "explicitly authorize read-only body insertion", "Doc 2 Pg 3")
    run.start_of_document()
    run.wait("CUSTODY A faithful reconstruction")
    run.save("INSERT.WP", body_fragment=b"CUSTODY A faithful reconstruction")
    assert (run.p.work / "FLOW.WP").read_bytes() == flow.read_bytes()
    close_doc2(run)
    run.exit_application()


def proof_pages(run):
    original = run.repo / REF / "proof-pages/exports"
    run.seed(original / "BEFORE.WP", "BEFORE.WP")
    run.launch()
    run.retrieve("BEFORE.WP")
    run.step(PGDOWN, "navigate to page two before checking", "Doc 1 Pg 2")
    run.step(PROOF, "Ctrl+F2 Check from the second page", "Check:", 24)
    run.step("2", "Page scope begins on physical page two", "Not Found:", 24)
    run.wait("zorbly")
    run.step(F1, "interrupt the selected page check", "Press any key to continue", 24)
    run.step(" ", "acknowledge interrupted Page and return to Check", "Check:", 24)
    run.step(F7, "leave Check for ordinary editing", "File Edit", 0)
    run.start_of_document()
    run.step(PROOF, "Ctrl+F2 Check from the first page", "Check:", 24)
    run.step("2", "check first page's original formatted words", "Not Found:", 24)
    choose_suggestion(run, "quick")
    choose_suggestion(run, "misspelled")
    run.wait("Press any key to continue", 24)
    run.step(" ", "acknowledge completed Page scope", "Check:", 24)
    run.step(F7, "return to the corrected editing document", "File Edit", 0)
    got = run.save("PAGECOPY.WP")
    want = bytearray((original / "PAGEONLY.WP").read_bytes())
    want[256] |= 0x08
    assert got == want, "Page correction differs from original native owners"
    assert (run.p.work / "BEFORE.WP").read_bytes() == (original / "BEFORE.WP").read_bytes()
    run.exit_application()


CASES = {
    "help-focus": ("EE-A02/A03", help_and_focus),
    "flow": ("EE-A04", flow),
    "corrections": ("EE-A06", corrections),
    "attributes": ("EE-A07/A08", attributes),
    "navigation-search": ("EE-A05/A09", navigation_search),
    "wrapped-search": ("EE-A09", wrapped_search),
    "files": ("EE-A10", files),
    "save-policy": ("EE-A11/A12", save_policy),
    "refusal": ("EE-A13", refusal),
    "proof-pages": ("EE-A15", proof_pages),
}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("repo", type=Path)
    p.add_argument("binary", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("case", choices=CASES)
    opts = p.parse_args()
    if opts.output.exists():
        p.error("output must be fresh")
    run = Run(opts.repo.resolve(), opts.binary.resolve(), opts.output.resolve())
    case, exercise = CASES[opts.case]
    failure = None
    try:
        exercise(run)
    except Exception as err:
        failure = repr(err)
    finally:
        run.finish(failure, case)


if __name__ == "__main__":
    main()
