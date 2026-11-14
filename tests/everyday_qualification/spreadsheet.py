#!/usr/bin/env python3
"""Exercise WK1 import and link refresh using actual Linux terminal key bytes."""
import subprocess
import sys
from pathlib import Path

from qualification import ENTER, F10, Run, native

CTRL_F5 = b"\x1b[15;5~"


def link_without_time(body):
    assert body.startswith(b"\xd2\x0d")
    return body[:8] + body[12:]


def create(run, command):
    for key in (CTRL_F5, "5", command, "1", r"C:\OUT\RANGE.WK1", ENTER,
                "2", "A1..B2", ENTER, "4"):
        run.step(key, "choose the worksheet and exact range")
    rows = run.wait("│       7 ")
    assert any("Amber" in row for row in rows)
    assert all("Outside" not in row for row in rows)


def exercise(run, phase, refs, initial):
    source = run.p.work / "OUT" / "RANGE.WK1"
    source.parent.mkdir()
    if phase in ("refresh", "fast-refresh", "original-refresh"):
        run.seed(initial, "LINK.WP")
        subprocess.run([sys.executable, refs / "fixture.py", source, "7" if phase == "original-refresh" else "19"], check=True)
        worksheet = source.read_bytes()
    else:
        worksheet = initial.read_bytes()
        source.write_bytes(worksheet)
    run.launch()
    run.set_fast_save(False)
    if phase == "import":
        create(run, "1")
        run.save("IMPORT.WP")
        assert native(run.p.work / "IMPORT.WP")[2] == native(refs / "IMPORT.WP")[2]
    elif phase == "offset":
        (source.parent / "OFFSET.WK1").write_bytes((refs / "OFFSET.WK1").read_bytes())
        for key in (CTRL_F5, "5", "1", "1", r"C:\OUT\OFFSET.WK1", ENTER,
                    "2", "B2..C3", ENTER, "4"):
            run.step(key, "select an offset range with a negative value")
        run.wait("║     -19  │      91 ║")
        run.save("OFFSET.WP")
        assert native(run.p.work / "OFFSET.WP")[2] == native(refs / "OFFSET.WP")[2]
    elif phase == "link":
        create(run, "2")
        run.wait(r"Link: C:\OUT\RANGE.WK1  A1..B2")
        run.save("LINK.WP")
        assert link_without_time(native(run.p.work / "LINK.WP")[2]) == link_without_time(native(refs / "LINK.WP")[2])
    else:
        run.retrieve("LINK.WP")
        run.wait("│      19 " if phase == "original-refresh" else "│       7 ")
        run.step(F10, "F10 save the unopened cache", "Document to be saved:")
        run.step(ENTER, "save back to the original link", "Replace LINK.WP")
        run.step("y", "accept replacement without changes")
        run.until(lambda: "Replace LINK.WP" not in "\n".join(run.rows()), "unchanged save settled")
        assert (run.p.work / "LINK.WP").read_bytes() == initial.read_bytes()
        for key in (CTRL_F5, "5", "4", "3"):
            run.step(key, "explicitly update all links")
        run.wait("│       7 " if phase == "original-refresh" else "│      19 ")
        if phase == "fast-refresh":
            run.set_fast_save(True)
        run.save("UPDATED.WP", expected_offset=564 if phase == "fast-refresh" else 324)
        got, offset, got_body = native(run.p.work / "UPDATED.WP")
        want, dos_offset, want_body = native(refs / ("LINK.WP" if phase == "original-refresh" else "UPDATED.WP"))
        assert link_without_time(got_body) == link_without_time(want_body)
        if phase == "fast-refresh":
            assert got[:offset] == want[:dos_offset]
    assert source.read_bytes() == worksheet
    run.exit_application()


if __name__ == "__main__":
    repo, binary, output = (Path(arg).resolve() for arg in sys.argv[1:4])
    refs = repo / "docs/research/reference-runs/mission1-spreadsheet"
    output.mkdir()
    for phase in ("import", "offset", "link", "refresh", "fast-refresh", "original-refresh"):
        run = Run(repo, binary, output / phase, classic_canvas=True)
        failure = None
        try:
            exercise(run, phase, refs,
                     refs / "UPDATED.WP" if phase == "original-refresh" else
                     output / "link/files/LINK.WP" if phase in ("refresh", "fast-refresh") else refs / "RANGE.WK1")
        except Exception as error:
            failure = repr(error)
            raise
        finally:
            run.finish(failure, "spreadsheet-" + phase)
