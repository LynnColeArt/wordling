#!/usr/bin/env python3
"""Run each independent qualification case against one exact CLI executable."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from physical_cases import CASES


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("repo", type=Path)
    p.add_argument("binary", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--candidate-record", type=Path,
                   help="bind the binary and exact production tree from build_candidate.py")
    p.add_argument("--reference-repo", type=Path,
                   help="checkout containing the separately pinned private original guest")
    p.add_argument("--without-original", action="store_true")
    p.add_argument("--without-proof", action="store_true", help="preflight only")
    args = p.parse_args()
    repo, binary, output = (x.resolve() for x in (args.repo, args.binary, args.output))
    output.mkdir()
    here = Path(__file__).resolve().parent
    evidence = repo / "internal/tui/evidence"
    digest = lambda: hashlib.sha256(binary.read_bytes()).hexdigest()
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    source_status = subprocess.check_output(
        ["git", "status", "--porcelain", "--", "cmd", "internal", "go.mod", "go.sum"], cwd=repo, text=True)
    candidate = None
    if args.candidate_record:
        candidate = json.loads(args.candidate_record.read_text())
        assert candidate["binary_sha256"] == digest(), "candidate binary SHA-256 differs"
        for name, tree in candidate["production_tree"].items():
            actual = subprocess.check_output(
                ["git", "rev-parse", f"{commit}:{name}"], cwd=repo, text=True).strip()
            assert actual == tree, f"production tree differs for {name}"
    record = {"schema": 1, "source_commit": commit, "binary": str(binary), "binary_sha256": digest(),
              "candidate_preflight": (args.without_proof or args.without_original or
                                      bool(source_status) or candidate is None),
              "candidate_source": candidate["source_commit"] if candidate else None,
              "cases": [], "production_source_status": source_status}
    reference_repo = args.reference_repo
    if reference_repo is None:
        common_dir = subprocess.check_output(
            ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], cwd=repo, text=True)
        reference_repo = Path(common_dir.strip()).parent
    manifest = output / "suite.json"

    def run(label, program, *params, kind="product-pty"):
        args = [str(part) for part in (program, *params)]
        log = output / (label + ".log")
        if digest() != record["binary_sha256"]:
            raise RuntimeError("candidate bytes changed mid-suite")
        with log.open("w") as stream:
            status = subprocess.run(args, cwd=repo, stdout=stream, stderr=subprocess.STDOUT).returncode
        if digest() != record["binary_sha256"]:
            raise RuntimeError("candidate bytes changed mid-suite")
        record["cases"].append({"name": label, "argv": args, "evidence_kind": kind,
                                "returncode": status, "log": str(log)})
        manifest.write_text(json.dumps(record, indent=2) + "\n")
        return status == 0

    def pty(label, script, *params):
        return run(label, sys.executable, script, repo, binary, output / label, *params)

    pty("menus", evidence / "everyday-menus/pty-menus.py")
    pty("files-reveal", evidence / "everyday-menus/pty-wp84.py")
    for key in CASES:
        if key != "proof-pages" or not args.without_proof:
            pty(key, here / "physical_cases.py", key)
    pty("preservation-corpus", here / "preservation_corpus.py")
    run("storage-faults", "go", "test", "-count=1", "-v", "./internal/storage", "-run",
        "^(TestEverydaySaveFailureConservation|TestEverydayStalePreparedRequests|"
        "TestEverydayMatchesOriginalCompleteBackupSnapshots|TestEverydayFailureWithoutPriorBackupAndNewTarget|"
        "TestEverydayRollbackCannotOverwriteConcurrentWriter|TestEditedPublicationFailureBoundaries)$",
        kind="component-owned-fault-injection")
    if not args.without_proof:
        pty("proofreading", evidence / "proofreading/run_pty.py")
    flags = ["--preflight-no-proof"] if args.without_proof else []
    if pty("continuous", here / "qualification.py", *flags) and not args.without_original:
        source = output / "continuous/files/WPLIVE.WP"
        original = output / "original"
        if run("original", sys.executable, here / "original_roundtrip.py", reference_repo.resolve(), source, original,
               kind="original-03-09-92"):
            pty("reopen", here / "qualification.py", "--reopen", original / "ROUND.WP")
    if not args.without_original:
        for name in ("first-save", "backup-replacement", "disabled-replacement"):
            source = output / "save-policy" / (name + ".WP")
            if source.is_file():
                label = "original-" + name
                run(label, sys.executable, here / "original_roundtrip.py", reference_repo.resolve(),
                    source, output / label, "--plain", kind="original-03-09-92")
    record["passed_executed_cases"] = all(row["returncode"] == 0 for row in record["cases"])
    manifest.write_text(json.dumps(record, indent=2) + "\n")
    return 0 if record["passed_executed_cases"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
