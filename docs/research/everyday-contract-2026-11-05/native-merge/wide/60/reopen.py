#!/usr/bin/env python3
"""Reopen and merge a two-page secondary in the pinned original DOS guest."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import time

p = argparse.ArgumentParser()
p.add_argument("repo", type=Path)
p.add_argument("out", type=Path)
p.add_argument("secondary", type=Path)
mode = p.add_mutually_exclusive_group()
mode.add_argument("--edit", action="store_true", help="make the two reference edits in DOS first")
mode.add_argument("--untouched", action="store_true", help="merge the originally authored values")
args = p.parse_args()
repo, out, secondary = (x.resolve() for x in (args.repo, args.out, args.secondary))
fixture = repo / "docs/research/everyday-contract-2026-11-05/native-merge/wide/60"
out.mkdir()
sys.path.insert(0, str(repo / "scripts/reference"))
import guest
import qmp

guest.RUNTIME = qmp.RUNTIME = out / "runtime"
guest.SOCKET = qmp.SOCKET = guest.RUNTIME / "qmp.sock"
private = out / "guest"
disk = str(private / "harddisk.img") + "@@1048576"

def guest_name(stem):
    return r"C:\OUT" + "\\" + stem + ".WP5"

def inject(source, stem):
    subprocess.run(["mcopy", "-i", disk, str(source), "::OUT/" + stem + ".WP5"], check=True)

try:
    command = guest.start(private)
    guest.stop()
    shutil.copyfile(guest.MASTER / "harddisk.img", private / "harddisk.img")
    primary = fixture / ("PRIMARY.WP5" if args.untouched else "EDITPRI.WP5")
    inject(primary, "PRIMARY")
    inject(secondary, "SECOND")
    subprocess.run(command, check=True)
    with qmp.QMP() as q:
        q.wait_for("Doc 1 Pg 1", timeout=60)
        q.key("f3")
        q.wait_for("03/09/92")
        q.capture(out / "release")
        q.key("ret")

        def enter_name(stem):
            q.type(guest_name(stem))
            q.key("ret")

        def save(stem):
            q.key("f10")
            q.wait_for("Document to be saved")
            enter_name(stem)
            q.wait_until(lambda s: (stem + ".WP5" in s or stem == "EDITED" and "Field: 55" in s)
                         and "Document to be saved" not in s
                         and "Saving C:" not in s, "settled save")
            time.sleep(0.6)

        def fast_save(enabled):
            q.key("shift-f1")
            q.wait_for("Environment")
            q.key("3")
            s = q.wait_for("Fast Save")
            label = "Yes" if enabled else "No"
            if not any("Fast Save" in line and label in line for line in s.splitlines()):
                q.key("5")
                q.wait_for("(" + label + ")")
                q.key(label[0].lower())
            q.key("f7")

        q.key("shift-f10")
        q.wait_for("Document to be retrieved")
        enter_name("SECOND")
        q.wait_for("A1" if args.edit or args.untouched else "XA1")
        q.capture(out / "retrieved")
        if args.edit:
            fast_save(False)
            q.type("X")
            q.wait_for("XA1")
        q.key("f2")
        q.wait_for("Srch:")
        q.type("A55")
        q.key("f2")
        q.wait_absent("Srch:")
        q.wait_for("A55")
        if args.edit:
            q.type("Y")
        q.wait_for("A55" if args.untouched else "A55Y")
        q.capture(out / "second-page")
        if args.edit:
            save("EDITED")
            fast_save(True)
        q.key("f7")
        q.wait_for("Save document?")
        q.key("n")
        q.wait_for("Exit WP?")
        q.key("n")
        q.wait_absent("Exit WP?")
        q.key("ctrl-f9")
        q.wait_for("1 Merge")
        q.key("1")
        q.wait_for("Primary file:")
        enter_name("PRIMARY")
        q.wait_for("Secondary file:")
        enter_name("EDITED" if args.edit else "SECOND")
        q.wait_for("52=[A52]" if args.untouched else "55=[A55Y]")
        q.wait_for("60=[B60]")
        q.capture(out / "merged")
        save("MERGED")
finally:
    guest.stop()
for stem in ("EDITED", "MERGED") if args.edit else ("MERGED",):
    name = stem + ".WP5"
    subprocess.run(["mcopy", "-i", disk, "::OUT/" + name, str(out / name)], check=True)
