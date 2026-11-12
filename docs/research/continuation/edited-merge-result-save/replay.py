#!/usr/bin/env python3
"""Measure native saves of edited merge results in a private WP 5.1 DOS guest."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time


def edit_at_start(q):
    for key in ("home", "home", "up"):
        q.key(key)
    q.wait_for('Doc 1 Pg 1 Ln 1" Pos 1"')


def advance_five(q):
    edit_at_start(q)
    for _ in range(5):
        q.key("right")


def file_name(name):
    return "C:\\OUT\\" + name + ".WP5"


def configure(q, yes, out):
    q.key("shift-f1")
    q.wait_for("Environment")
    q.key("3")
    initial = q.wait_for("Fast Save")
    name = "Yes" if yes else "No"
    if not any("Fast Save" in line and name in line for line in initial.splitlines()):
        q.key("5")
        q.wait_for("(" + name + ")")
        q.key("y" if yes else "n")
    q.wait_until(lambda screen: any("Fast Save" in line and name in line
                                  for line in screen.splitlines()), name)
    q.capture(out / ("fast-save-" + name))
    q.key("f7")
    q.wait_for("Doc 1 Pg 1")


def merge(q):
    q.key("ctrl-f9")
    q.wait_for("Merge")
    q.key("1")
    q.wait_for("Primary file:")
    q.type(file_name("PRIMARY"))
    q.key("ret")
    q.wait_for("Secondary file:")
    q.type(file_name("SECOND"))
    q.key("ret")
    q.wait_for("Hello Alice")
    q.wait_for("Hello Bob")


def save(q, name, out):
    q.key("f10")
    q.wait_for("Document to be saved")
    q.type(file_name(name))
    q.key("ret")
    q.wait_until(lambda screen: "Document to be saved" not in screen and
                 "Saving C:" not in screen and "Doc 1 Pg" in screen,
                 "settled save " + name, timeout=35)
    time.sleep(0.8)
    q.capture(out / ("saved-" + name))


def close(q):
    q.key("f7")
    q.wait_for("Save document?")
    q.key("n")
    q.wait_for("Exit WP?")
    q.key("n")
    q.wait_absent("Exit WP?")


def retrieve(q, name, out, cue="EDIT Hello Alice"):
    q.key("shift-f10")
    q.wait_for("Document to be retrieved")
    q.type(file_name(name))
    q.key("ret")
    q.wait_for(cue)
    q.capture(out / ("retrieved-" + name))


def run(q, out, mode):
    files = []

    def publish(name):
        save(q, name, out)
        files.append(name)

    for fast, prefix in ((True, "Y"), (False, "N")):
        configure(q, fast, out)
        if mode != "product":
            merge(q)
            q.capture(out / ("merged-" + prefix))
            edit_at_start(q)
            q.type("EDIT ")
            q.wait_for("EDIT Hello Alice")
            publish(prefix + "FIRST")
        if mode == "toggle":
            configure(q, not fast, out)
            advance_five(q)
            q.type("OTHER ")
            publish(prefix + "OTHER")
            if fast:
                configure(q, True, out)
                advance_five(q)
                q.type("BACK ")
                publish("YBACK")
            close(q)
            continue
        if mode == "fixed":
            advance_five(q)
            q.type("MORE ")
            q.wait_for("EDIT MORE Hello Alice")
            publish(prefix + "AGAIN")
            close(q)
        retrieve(q, prefix + "FIRST", out)
        edit_at_start(q)
        q.type("OPEN ")
        q.wait_for("OPEN EDIT Hello Alice")
        publish(prefix + "OPEN")
        if mode == "fixed":
            advance_five(q)
            q.type("NEXT ")
            q.wait_for("OPEN NEXT EDIT Hello Alice")
            publish(prefix + "NEXT")
        close(q)
    return files


def run_loaded_no(q, out):
    configure(q, False, out)
    retrieve(q, "PAIR", out, "ABCD")
    q.key("right")
    q.type("SAFE")
    q.wait_for("ASAFEBCD")
    save(q, "EDITPAIR", out)
    close(q)

    retrieve(q, "PROOF", out, "quik")
    edit_at_start(q)
    q.key("ctrl-f2")
    q.wait_for("Check:")
    q.key("2")
    q.wait_for("Not Found:")
    q.capture(out / "proof-first")
    q.key("c")
    q.wait_for("A. misspelled")
    q.key("a")
    q.wait_for("Press any key")
    q.key("spc")
    q.wait_for("Check:")
    q.key("f7")
    save(q, "EDITPAGE", out)
    close(q)

    retrieve(q, "INPUT", out, "Alpha beta")
    q.type("EDIT ")
    q.wait_for("EDIT Alpha beta")
    save(q, "PLAIN", out)
    configure(q, True, out)
    edit_at_start(q)
    q.type("BACK ")
    q.wait_for("BACK EDIT Alpha beta")
    save(q, "BACK", out)
    close(q)
    return ["EDITPAIR", "EDITPAGE", "PLAIN", "BACK"]


def result(path):
    raw = path.read_bytes()
    offset = int.from_bytes(raw[4:8], "little")
    middle = int.from_bytes(raw[22:26], "little")
    state = raw[80 if offset == 564 else 66]
    return {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
            "body_offset": offset, "middle_index": middle, "active_state": state}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("mode", choices=("fixed", "toggle", "product", "loaded-no"))
    parser.add_argument("--yes-product", type=Path)
    parser.add_argument("--no-product", type=Path)
    args = parser.parse_args()
    if args.mode == "product" and not (args.yes_product and args.no_product):
        parser.error("product mode needs both Wordling FIRST outputs")
    repo, out = args.repo.resolve(), args.out.resolve()
    out.mkdir()
    sys.path.insert(0, str(repo / "scripts/reference"))
    import guest
    import qmp

    guest.RUNTIME = qmp.RUNTIME = out / "runtime"
    guest.SOCKET = qmp.SOCKET = qmp.RUNTIME / "qmp.sock"
    private = out / "guest"
    disk = str(private / "harddisk.img") + "@@1048576"
    reference = repo / "docs/research/reference-runs/2026-10-29-extended-04/CMD51-134"
    expected = repo / "internal/editor/testdata/merge_result_save"
    if args.mode == "product":
        inputs = {"YFIRST.WP5": args.yes_product, "NFIRST.WP5": args.no_product}
    elif args.mode == "loaded-no":
        docs = repo / "docs/research"
        inputs = {
            "PAIR.WP5": docs / "reference-runs/2026-10-29-advanced-03/CMD51-203/ORIGIN.WP5",
            "PROOF.WP5": docs / "everyday-contract-2026-11-05/qualification/proof-pages/exports/BEFORE.WP",
            "INPUT.WP5": repo / "internal/document/testdata/fast_save_yes/SECOND.WP",
        }
        expected = Path(__file__).resolve().parent / "loaded-no"
    else:
        inputs = {name: reference / name for name in ("PRIMARY.WP5", "SECOND.WP5")}
    try:
        command = guest.start(private)
        guest.stop()
        shutil.copyfile(guest.MASTER / "harddisk.img", private / "harddisk.img")
        for name, source in inputs.items():
            subprocess.run(["mcopy", "-i", disk, str(source), "::OUT/" + name], check=True)
        subprocess.run(command, check=True)
        (out / "command.json").write_text(json.dumps(command, indent=2) + "\n")
        with qmp.QMP() as q:
            q.wait_for('Doc 1 Pg 1 Ln 1" Pos 1"', timeout=60)
            q.key("f3")
            q.wait_for("03/09/92")
            q.capture(out / "release")
            q.key("ret")
            outputs = run_loaded_no(q, out) if args.mode == "loaded-no" else run(q, out, args.mode)
    finally:
        guest.stop()
    manifest = {}
    for stem in outputs:
        name = stem + ".WP5"
        target = out / name
        subprocess.run(["mcopy", "-i", disk, "::OUT/" + name, str(target)], check=True)
        manifest[name] = result(target)
        assert target.read_bytes() == (expected / name).read_bytes(), name
    (out / "result.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
