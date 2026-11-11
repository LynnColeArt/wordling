#!/usr/bin/env python3
"""Pass one real Wordling output through a private original 03/09/92 copy."""
import argparse
from pathlib import Path
import json
import re
import shutil
import subprocess
import sys

from qualification import native, native_info


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("repo", type=Path)
    p.add_argument("candidate", type=Path, help="WPLIVE.WP written by the tested CLI")
    p.add_argument("output", type=Path)
    p.add_argument("--plain", action="store_true",
                   help="verify one of the ordinary plain save-policy snapshots")
    args = p.parse_args()
    repo, candidate, out = (x.resolve() for x in (args.repo, args.candidate, args.output))
    if out.exists():
        p.error("output must be fresh")
    _, offset, original_body = native(candidate)
    assert offset == 324
    if args.plain:
        cue = original_body.decode("ascii")
        assert cue and cue.isprintable(), "plain snapshot contains native owners"
        edit_gap = 0
    else:
        assert original_body.startswith(b"\xc3\x0c\xc3Wordling "), "candidate does not carry the checked BoldOn/edit"
        cue = "Wordling"
        edit_gap = 3
    out.mkdir()
    sys.path.insert(0, str(repo / "scripts/reference"))
    import guest
    import qmp

    guest.RUNTIME = qmp.RUNTIME = out / "runtime"
    guest.SOCKET = qmp.SOCKET = guest.RUNTIME / "qmp.sock"
    private = out / "guest"
    returned = out / "ROUND.WP"
    evidence = {"reference": "WP 5.1 DOS 03/09/92", "candidate": native_info(candidate),
                "producer_profile": "Standard Printer, original Fast Save No"}
    try:
        command = guest.start(private)
        guest.stop()
        shutil.copyfile(guest.MASTER / "harddisk.img", private / "harddisk.img")
        disk = str(private / "harddisk.img") + "@@1048576"
        subprocess.run(["mcopy", "-i", disk, str(candidate), "::OUT/WPLIVE.WP"], check=True)
        subprocess.run(command, check=True)
        evidence["command"] = command
        with qmp.QMP() as q:
            q.wait_for('Doc 1 Pg 1 Ln 1" Pos 1"', timeout=60)
            q.key("f3")
            q.wait_for("03/09/92")
            q.capture(out / "reference-release")
            q.key("ret")
            q.key("shift-f1")
            q.wait_for("Environment")
            q.key("3")
            row = q.wait_for("Fast Save")
            q.capture(out / "original-fast-save-before")
            if re.search(r"5[^\n]*Fast Save[^\n]*Yes", row, re.I):
                q.key("5")
                q.wait_until(lambda t: any("Fast Save" in line and "(No)" in line for line in t.splitlines()), "Fast Save choice")
                q.key("n")
            q.wait_until(lambda t: bool(re.search(r"5[^\n]*Fast Save[^\n]*No", t, re.I)), "Fast Save No")
            q.capture(out / "original-fast-save-off")
            q.key("f7")
            q.wait_for("Doc 1 Pg 1")
            q.key("shift-f10")
            q.wait_for("Document to be retrieved")
            q.type(r"C:\OUT\WPLIVE.WP")
            q.key("ret")
            q.wait_for(cue)
            q.capture(out / "original-retrieved")
            for key in ("home", "home", "up"):
                q.key(key)
            q.type("Original ")
            q.wait_for("Original")
            q.capture(out / "original-reedited")
            q.key("f10")
            q.wait_for("Document to be saved")
            q.type(r"C:\OUT\ROUND.WP")
            q.key("ret")
            q.wait_until(lambda screen: any("ROUND.WP" in line and "Doc 1 Pg" in line
                                            for line in screen.splitlines()) and "Saving C:" not in screen,
                         "settled original save and document status", timeout=35)
            q.capture(out / "original-resaved")
        guest.stop()
        subprocess.run(["mcopy", "-i", disk, "::OUT/ROUND.WP", str(returned)], check=True)
        _, offset, returned_body = native(returned)
        assert offset == 324, offset
        expected = original_body[:edit_gap] + b"Original " + original_body[edit_gap:]
        assert returned_body == expected, "original edit changed an unrelated native owner"
        evidence["returned"] = native_info(returned)
        evidence["result"] = "pass"
    except Exception as err:
        evidence.update(result="fail", failure=repr(err))
        raise
    finally:
        guest.stop()
        (out / "original-roundtrip.json").write_text(json.dumps(evidence, indent=2) + "\n")


if __name__ == "__main__":
    main()
