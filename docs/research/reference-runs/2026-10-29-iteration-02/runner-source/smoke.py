#!/usr/bin/env python3
"""Run bounded original-WP probes; these are not Wordling differential tests."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import re
import shutil
import struct
import time

from guest import start, stop, MASTER, PROFILE
from qmp import QMP, ROOT
from extended import PROBES as EXTENDED, clean_exit
from advanced import PROBES as ADVANCED
from document import prefix, plain_merge
from history_loops import PROBES as HISTORY_LOOPS
from iteration_nesting import PROBES as ITERATION_NESTING
EXTENDED = {**EXTENDED, **ADVANCED, **HISTORY_LOOPS, **ITERATION_NESTING}


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


class Probe:
    def __init__(self, q, out):
        self.q, self.out, self.trace, self.checks = q, out, [], []
        self.exports, self.identical, self.contains, self.same_body = [], [], [], []
        self.page_expectations = []

    def key(self, keys):
        self.trace.append({"key": keys})
        for key in keys.split(","):
            self.q.key(key.strip())

    def type(self, text):
        self.trace.append({"type": text})
        self.q.type(text)

    def capture(self, label):
        self.trace.append({"capture": label, "stable_text_seconds": 0.4})
        last, since = None, None
        def stable(screen):
            nonlocal last, since
            if 'Repositioning' in screen:
                last, since = None, None
                return False
            if screen != last:
                last, since = screen, time.monotonic()
                return False
            return time.monotonic() - since >= 0.4
        self.q.wait_until(stable, "stable text before " + label)
        return self.q.capture(self.out / label)

    def check(self, name, condition):
        self.checks.append({"check": name, "passed": bool(condition)})
        if not condition:
            raise AssertionError(name)


def menus(p):
    p.capture("before")
    p.key("alt-equal")
    p.q.wait_for("File Edit Search")
    s = p.capture("menu-on")
    p.check("Menu bar appears", "File Edit Search Layout" in s)
    p.key("alt-equal")
    p.q.wait_absent("File Edit Search")
    s = p.capture("menu-off")
    p.check("Menu bar disappears", "File Edit Search" not in s)
    p.check("Visible position retained", 'Doc 1 Pg 1 Ln 1" Pos 1"' in s)


def help_space(p):
    p.key("f3")
    p.q.wait_for("WP 5.1   03/09/92")
    s = p.capture("release-and-help")
    p.check("Displayed release identity", "WP 5.1   03/09/92" in s)
    p.key("spc")
    p.q.wait_absent("Press any letter")
    s = p.capture("returned")
    p.check("Help closes without advancing insertion position", 'Ln 1" Pos 1"' in s)


def repeat(p):
    p.key("esc")
    p.type("5")
    p.type("x")
    p.q.wait_for("xxxxx")
    s = p.capture("repeated")
    p.check("Five characters inserted", s.splitlines()[0] == "xxxxx")


def block_seek(p):
    p.type("alpha beta")
    p.q.wait_for("alpha beta")
    p.key("home,home,up")
    p.key("alt-f4")
    p.capture("block-start")
    p.type("b")
    p.q.wait_for("alpha beta")
    # Wait for the key to be consumed by requiring a changed status position.
    p.q.wait_until(lambda s: 'Pos 1"' not in s, "block seek position")
    s = p.capture("seek-result")
    p.check("Typing seeks without replacing selected text", s.splitlines()[0] == "alpha beta")


def typeover(p):
    p.type("abc")
    p.q.wait_for("abc")
    p.key("left,left,insert")
    p.q.wait_for("Typeover")
    p.capture("typeover-active")
    p.type("X")
    p.q.wait_for("aXc")
    p.key("insert")
    p.q.wait_absent("Typeover")
    p.type("Y")
    p.q.wait_for("aXYc")
    s = p.capture("insert-restored")
    p.check("Typeover then insertion yields aXYc", s.splitlines()[0] == "aXYc")


def codes(p):
    p.key("f6")
    p.type("alpha")
    p.key("f6")
    p.type("beta")
    p.q.wait_for("alphabeta")
    p.capture("normal")
    p.key("alt-f3")
    p.q.wait_for("[BOLD]")
    s = p.capture("codes-on")
    p.check("Bold codes exposed", "[BOLD]alpha[bold]beta" in s)
    p.key("alt-f3")
    p.q.wait_absent("[BOLD]")
    s = p.capture("codes-off")
    p.check("Text retained after toggling", s.splitlines()[0] == "alphabeta")


def save(p):
    p.type("WORDLING TEST")
    p.q.wait_for("WORDLING TEST")
    p.key("f10")
    p.q.wait_for("Document to be saved:")
    p.capture("save-prompt")
    p.type("C:\\OUT\\NEWTEST")
    p.key("ret")
    p.q.wait_absent("Document to be saved:")
    s = p.capture("saved")
    p.check("Editing continues after save", "WORDLING TEST" in s)


PROBES = {"CMD51-001": menus, "CMD51-004": help_space, "CMD51-005": repeat,
          "CMD51-028": block_seek, "CMD51-046": typeover, "CMD51-048": codes,
          "CMD51-066": save}
PROBES.update(EXTENDED)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_id")
    parser.add_argument("cases", nargs="*", choices=list(PROBES))
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.run_id):
        parser.error("run_id must contain only letters, digits, underscores and hyphens")
    out = ROOT / "docs/research/reference-runs" / args.run_id
    work = ROOT / "research/cache/reference/runs" / args.run_id
    if out.exists() or work.exists():
        raise FileExistsError("Choose a new run ID; prior evidence is immutable")
    out.mkdir(parents=True)
    run = {"schema_version": 1, "run_id": args.run_id,
           "started_at": datetime.now(timezone.utc).isoformat(),
           "baseline_id": "wp51-dos-us-1992-03-09", "scope": "original-reference-only",
           "wordling_tested": False, "master_disk_sha256": sha(MASTER / "harddisk.img"),
           "master_boot_sha256": sha(MASTER / "boot.img"), "results": []}
    run["runner_sources"] = [{"path": str(p.relative_to(ROOT)), "sha256": sha(p)} for p in
                             [Path(__file__).resolve(), ROOT / "scripts/reference/guest.py", ROOT / "scripts/reference/qmp.py", ROOT / "scripts/reference/extended.py", ROOT / "scripts/reference/advanced.py", ROOT / "scripts/reference/document.py", ROOT / "scripts/reference/history_loops.py", ROOT / "scripts/reference/iteration_nesting.py"]]
    for source in run["runner_sources"]:
        target = out / "runner-source" / Path(source["path"]).name
        target.parent.mkdir(exist_ok=True)
        shutil.copyfile(ROOT / source["path"], target)
    run["scenario_registry_sha256"] = sha(ROOT / "docs/research/command-scenarios.json")
    run["environment_manifest_sha256"] = sha(PROFILE)
    shutil.copyfile(PROFILE, out / "environment.json")
    shutil.copyfile(ROOT / "docs/research/command-scenarios.json", out / "scenario-registry.json")
    run["environment_profile_archive"] = str((out / "environment.json").relative_to(ROOT))
    for case_id in args.cases or list(PROBES):
        directory = out / case_id
        directory.mkdir()
        result = {"case_id": case_id, "result": "error", "observed_scope": "bounded smoke recipe; not complete scenario or differential acceptance"}
        p = None
        try:
            result["qemu_argv"] = start(work / case_id)
            with QMP() as q:
                p = Probe(q, directory)
                PROBES[case_id](p)
                if case_id in EXTENDED:
                    clean_exit(p)
            result["result"] = "observed-matches-smoke-expectations"
        except Exception as e:
            result["error"] = str(e)
            try:
                with QMP() as q:
                    q.capture(directory / "error-screen")
            except Exception:
                pass
        finally:
            stop()
            if p:
                result["trace"], result["checks"] = p.trace, p.checks
            if case_id == "CMD51-066" and result["result"] != "error":
                target = directory / "NEWTEST.WP5"
                extraction = subprocess.run(["mcopy", "-i", str(work / case_id / "harddisk.img") + "@@1048576", "::OUT/NEWTEST", str(target)], capture_output=True, text=True)
                if extraction.returncode:
                    result["result"], result["error"] = "error", extraction.stderr
                else:
                    data = target.read_bytes()
                    result["native_output"] = {"path": str(target.relative_to(ROOT)), "sha256": sha(target),
                                               "size": len(data), "prefix_hex": data[:16].hex(),
                                               "text_present": b"WORDLING TEST" in data}
                    if data[:4] != bytes.fromhex("ff575043") or not result["native_output"]["text_present"]:
                        result["result"] = "error"
            if p and result["result"] != "error":
                try:
                    result["native_outputs"] = []
                    for guest_name, host_name in p.exports:
                        target = directory / host_name
                        subprocess.run(["mcopy", "-i", str(work / case_id / "harddisk.img") + "@@1048576",
                                        "::OUT/"+guest_name, str(target)], check=True, capture_output=True)
                        data = target.read_bytes()
                        p.check("Native signature: "+host_name, data[:4] == bytes.fromhex("ff575043"))
                        result["native_outputs"].append({"path":str(target.relative_to(ROOT)), "size":len(data),
                                                         "sha256":sha(target), "prefix_hex":data[:16].hex()})
                    for left,right in p.identical:
                        p.check("Byte-identical after refusal: "+left+" / "+right,
                                (directory/left).read_bytes() == (directory/right).read_bytes())
                    result["document_comparisons"] = []
                    for left,right in p.same_body:
                        data=[(directory/name).read_bytes() for name in [left,right]]
                        offsets=[struct.unpack_from('<I',b,4)[0] for b in data]
                        if not all(16 <= o <= len(b) for o,b in zip(offsets,data)):
                            raise ValueError('Invalid native document offset')
                        same=data[0][offsets[0]:]==data[1][offsets[1]:]
                        p.check("Native document body preserved: "+left+" / "+right,same)
                        result["document_comparisons"].append({"files":[left,right],"document_offsets":offsets,
                            "body_equal":same,"whole_file_equal":data[0]==data[1],
                            "document_flags":[prefix(b)["document_flags"] for b in data],
                            "prefix_byte_differences":[{"offset":i,"before":a,"after":b} for i,(a,b) in enumerate(zip(data[0][:offsets[0]],data[1][:offsets[1]])) if a!=b]})
                    result["pagination_inspections"] = []
                    for name,count in p.page_expectations:
                        inspection=plain_merge((directory/name).read_bytes())
                        inspection["file"]=name
                        result["pagination_inspections"].append(inspection)
                        p.check("Native hard-page count for "+name+": "+str(count),inspection["hard_page_count"]==count)
                    for name,content in p.contains:
                        p.check("Native body contains "+content.decode('ascii'), content in (directory/name).read_bytes())
                except Exception as e:
                    result["result"],result["error"]="error",str(e)
            result["evidence"] = [{"path": str(f.relative_to(ROOT)), "sha256": sha(f), "size": f.stat().st_size}
                                  for f in sorted(directory.rglob("*")) if f.is_file()]
            run["results"].append(result)
            (out / "run.json").write_text(json.dumps(run, indent=2) + "\n")
            print(case_id, result["result"], result.get("error", ""), flush=True)
    if any(r["result"] == "error" for r in run["results"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
