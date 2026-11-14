#!/usr/bin/env python3
"""Exercise both shell entry points with an unsaved document."""
import sys
from pathlib import Path

from qualification import Run, SWITCH, native


def exercise(run):
    run.p.env.update(SHELL="/bin/sh", PS1="WORDLING-SHELL> ")
    run.launch(enhancements=False, controlling_terminal=True)
    run.step("KEEP", "type unsaved text", "KEEP")
    run.step(b"\x1b[1;5P", "request shell", "Save document 1 before opening shell?")
    run.step(b"\x1b", "cancel and keep editing")
    run.step(b"\x1b[1;5P", "request shell again", "Save document 1 before opening shell?")
    run.step("y", "choose Save", "Document to be saved:")
    run.step(b"\x1b", "cancel filename and stay in Wordling")
    for entry in ("shortcut", "menu"):
        if entry == "shortcut":
            run.step(b"\x1b[1;5P", "Ctrl+F1")
        else:
            run.step(b"\x1b=", "focus menu bar")
            run.step("f", "open File menu", "Open Shell")
            run.step("h", "select Open Shell")
        run.wait("Save document 1 before opening shell?")
        if entry == "shortcut":
            run.step("n", "keep edits in memory")
        else:
            run.step("y", "save before opening shell", "Document to be saved:")
            run.step("BEFORE.WP", "name the document")
            run.step(b"\r", "commit save")
        run.wait("WORDLING-SHELL>")
        if entry == "menu":
            assert native(run.p.work / "BEFORE.WP")[2] == b"KEEP"
        run.step("printf 'SHELL-%s\\n' OK\r", "run an interactive shell command", "SHELL-OK")
        run.step("exit\r", "return to unsaved document", "KEEP")
        run.wait("Doc 1 Pg")
    run.step("SAFE", "continue at the original caret", "KEEPSAFE")
    run.step(b"\x1b[21~", "save after shell", "Document to be saved:")
    run.step(b"\x1bOP", "cancel save prompt")
    run.step(SWITCH, "open the second document", "Doc 2 Pg")
    run.step("SECOND", "edit the second document", "SECOND")
    run.step(b"\x1b[1;5P", "request shell from document two", "Save document 2 before opening shell?")
    run.step("y", "save document two", "Document to be saved:")
    run.step("SECOND.WP", "name document two")
    run.step(b"\r", "publish document two", "Save document 1 before opening shell?")
    assert native(run.p.work / "SECOND.WP")[2] == b"SECOND"
    run.step("n", "keep document one's edits in memory", "WORDLING-SHELL>")
    run.step("exit\r", "return to the original screen", "Doc 2 Pg")
    run.wait("SECOND")
    run.step(SWITCH, "check unsaved text on document one", "KEEPSAFE")
    run.step(b"\x1b=", "focus menu")
    run.step("f", "open File", "Quit Wordling")
    run.step("q", "quit the application", "Save document 1 before quitting?")
    run.step(b"\x1b", "cancel quitting", "KEEPSAFE")
    run.step(b"\x1b=", "focus menu again")
    run.step("f", "open File again", "Quit Wordling")
    run.step("q", "quit again", "Save document 1 before quitting?")
    run.step("n", "quit without saving")
    run.p.proc.wait(timeout=4)
    assert run.p.proc.returncode == 0


if __name__ == "__main__":
    repo, binary, output = (Path(arg).resolve() for arg in sys.argv[1:])
    run = Run(repo, binary, output)
    failure = None
    try:
        exercise(run)
    except Exception as err:
        failure = repr(err)
        raise
    finally:
        run.finish(failure, "interactive shell and document return")
