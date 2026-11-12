#!/usr/bin/env python3
"""Retrieve and merge saved secondary data in the pinned WordPerfect DOS guest."""
import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("repo", "out", "primary", "secondary"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--edit", action="store_true", help="insert XXXX at the start and save with Fast Save No")
    parser.add_argument("--edit-after", help="search for this text before inserting XXXX with --edit")
    parser.add_argument("--find", help="find a value on a later page after Retrieve")
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir()
    sys.path.insert(0, str(args.repo.resolve() / "scripts/reference"))
    import guest
    import qmp

    guest.RUNTIME = qmp.RUNTIME = out / "runtime"
    guest.SOCKET = qmp.SOCKET = guest.RUNTIME / "qmp.sock"
    private = out / "guest"
    disk = str(private / "harddisk.img") + "@@1048576"

    try:
        command = guest.start(private)
        guest.stop()
        shutil.copyfile(guest.MASTER / "harddisk.img", private / "harddisk.img")
        for name, source in (("PRIMARY", args.primary), ("SECOND", args.secondary)):
            subprocess.run(["mcopy", "-i", disk, str(source), "::OUT/" + name + ".WP5"], check=True)
        subprocess.run(command, check=True)
        with qmp.QMP() as q:
            def name(stem):
                q.type("C:\\OUT\\" + stem + ".WP5")
                q.key("ret")

            def save(stem):
                q.key("f10")
                q.wait_for("Document to be saved")
                name(stem)
                q.wait_until(lambda s: "Document to be saved" not in s and "Saving C:" not in s
                             and "Doc 1 Pg" in s, "settled save")
                time.sleep(0.8)

            def set_fast_save(enabled):
                label = "Yes" if enabled else "No"
                q.key("shift-f1")
                q.wait_for("Environment")
                q.key("3")
                screen = q.wait_for("Fast Save")
                if not any("Fast Save" in line and label in line for line in screen.splitlines()):
                    q.key("5")
                    q.wait_for("(" + label + ")")
                    q.key(label[0].lower())
                q.key("f7")

            q.wait_for("Doc 1 Pg 1", timeout=60)
            q.key("f3")
            q.wait_for("03/09/92")
            q.capture(out / "release")
            q.key("ret")
            q.key("shift-f10")
            q.wait_for("Document to be retrieved")
            name("SECOND")
            q.wait_absent("Document to be retrieved")
            q.wait_for("{END FIELD}")
            def find(value):
                q.key("f2")
                q.wait_for("Srch:")
                q.type(value)
                q.key("f2")
                q.wait_absent("Srch:")
                q.wait_for(value)

            if args.edit:
                set_fast_save(False)
                if args.edit_after:
                    find(args.edit_after)
                q.type("XXXX")
                q.wait_for("XXXX")
                save("EDITED")
                set_fast_save(True)
            if args.find:
                find(args.find)
            q.capture(out / "retrieved")
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
            name("PRIMARY")
            q.wait_for("Secondary file:")
            name("EDITED" if args.edit else "SECOND")
            q.wait_for("1=[")
            q.capture(out / "merged")
            save("MERGED")
    finally:
        guest.stop()
    for stem in ("EDITED", "MERGED") if args.edit else ("MERGED",):
        filename = stem + ".WP5"
        subprocess.run(["mcopy", "-i", disk, "::OUT/" + filename, str(out / filename)], check=True)


if __name__ == "__main__":
    main()
