#!/usr/bin/env python3
"""Check ordinary terminal input and function keys carrying lock-state flags."""
import sys
from pathlib import Path

from qualification import F5, F7, F10, Run


def exercise(run):
    run.launch(enhancements=False)
    run.step(b"\x1bOR", "VTE F3", "03/09/92")
    run.step(b"\r", "close Help", "Doc 1 Pg")
    for key, name in ((b"\x1b=", "main keyboard Alt+Equals"),
                      (b"\x1b+", "main keyboard Alt+Plus"),
                      (b"\x1bO3k", "VTE Alt+keypad Plus"),
                      (b"\x1b[57413;131u", "enhanced Alt+keypad Plus with Num Lock")):
        run.step(key, name)
        run.step(b"\r", "open the focused File menu", "List Files F5")
        run.step(b"\x1b", "close the menu")
    run.wait("Doc 1 Untitled", 1)
    assert "Doc 2" not in run.rows()[1]
    run.step(b"\x1b[25~", "F13 hides document tabs")
    assert "Doc 1 Untitled" not in run.rows()[1]
    run.step(b"\x1b=", "focus menu bar")
    run.step("t", "open Tools", "Document Tabs Off F13")
    run.step(b"\r", "toggle tabs from Tools", "Doc 1 Untitled", 1)
    run.step(b"\x1b[1;2P", "open Setup", "Setup", 0)
    run.step("2", "open Display", "Document Tabs")
    run.step("7", "hide tabs from Display")
    run.step(F7, "return to editing")
    assert "Doc 1 Untitled" not in run.rows()[1]
    run.step(b"\x1b[25~", "F13 shows document tabs", "Doc 1 Untitled", 1)
    run.step(F5, "legacy F5", "Dir C:")
    run.step(F7, "legacy F7", "Doc 1 Pg")
    run.step(F10, "legacy F10", "Document to be saved:")
    run.step(b"\x1bOP", "legacy F1", "Doc 1 Pg")

    run.step(b"\x1b", "Escape focuses menu")
    run.step("f", "F opens File menu", "List Files F5")
    for _ in range(5):
        run.step(b"\x1b[B", "select next File command")
    run.step(b"\r", "select List Files without function keys", "Dir C:")
    run.step(b"\x1b", "close List Files without function keys", "Doc 1 Pg")

    run.step(b"\x1b[15;193~", "F5 with Num Lock and Caps Lock", "Dir C:")
    run.step(b"\x1b[18;193~", "F7 with Num Lock and Caps Lock", "Doc 1 Pg")
    run.step(b"\x1b[21;193~", "F10 with Num Lock and Caps Lock", "Document to be saved:")
    run.step(b"\x1bOP", "cancel Save")
    run.exit_application()


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
        run.finish(failure, "legacy terminal input and lock modifiers")
