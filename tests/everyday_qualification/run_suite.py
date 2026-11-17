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
    p.add_argument("--fault-binary", type=Path, required=True,
                   help="separate wordling_qa build used ONLY by save-failure")
    p.add_argument("--fault-candidate-record", type=Path, required=True,
                   help="build_candidate.py --qa-save-faults provenance")
    args = p.parse_args()
    repo, binary, output = (x.resolve() for x in (args.repo, args.binary, args.output))
    output.mkdir()
    here = Path(__file__).resolve().parent
    evidence = repo / "internal/tui/evidence"
    digest = lambda: hashlib.sha256(binary.read_bytes()).hexdigest()
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    source_status = subprocess.check_output(
        ["git", "status", "--porcelain", "--", "cmd", "internal", "go.mod", "go.sum"], cwd=repo, text=True)
    fault_candidate = json.loads(args.fault_candidate_record.read_text())
    assert fault_candidate["qa_save_faults"] is True
    assert "internal/storage/qualification_fault_linux.go" in fault_candidate["compiled_local_input_sha256"]
    assert "internal/storage/qualification_normal_linux.go" not in fault_candidate["compiled_local_input_sha256"]
    assert fault_candidate["source_commit"] == commit
    assert fault_candidate["binary_sha256"] == hashlib.sha256(args.fault_binary.read_bytes()).hexdigest()
    for name, expected in fault_candidate["compiled_local_input_sha256"].items():
        assert hashlib.sha256((repo / name).read_bytes()).hexdigest() == expected, name
    candidate = None
    if args.candidate_record:
        if source_status:
            p.error("--candidate-record requires a clean production tree")
        candidate = json.loads(args.candidate_record.read_text())
        assert not candidate.get("qa_save_faults", False), "primary suite binary must be a normal build"
        assert "internal/storage/qualification_normal_linux.go" in candidate["compiled_local_input_sha256"]
        assert "internal/storage/qualification_fault_linux.go" not in candidate["compiled_local_input_sha256"]
        assert candidate["binary_sha256"] == digest(), "candidate binary SHA-256 differs"
        for name, expected in candidate["compiled_local_input_sha256"].items():
            assert hashlib.sha256((repo / name).read_bytes()).hexdigest() == expected, (
                f"compiled input differs: {name}"
            )
        for name, tree in candidate["production_tree"].items():
            actual = subprocess.check_output(
                ["git", "rev-parse", f"{commit}:{name}"], cwd=repo, text=True).strip()
            assert actual == tree, f"production tree differs for {name}"
    record = {"schema": 1, "source_commit": commit, "binary": str(binary), "binary_sha256": digest(),
              "candidate_preflight": (args.without_proof or args.without_original or
                                      bool(source_status) or candidate is None),
              "candidate_source": candidate["source_commit"] if candidate else None,
              "fault_candidate_record": str(args.fault_candidate_record.resolve()),
              "fault_binary": str(args.fault_binary.resolve()),
              "fault_binary_sha256": hashlib.sha256(args.fault_binary.read_bytes()).hexdigest(),
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
    pty("navigation-deletion", here / "navigation_deletion.py")
    pty("line-format", here / "line_format.py")
    pty("initial-codes", here / "initial_codes.py")
    for case in ("horizontal", "boundary", "loaded-yes", "loaded-no", "wrapped"):
        pty("advance-" + case, here / "advance.py", case)
    pty("page-number-position", here / "page_number_position.py")
    pty("custom-tabs", here / "tabs_and_notes.py", "tabs")
    pty("ruler-decimal", here / "tabs_and_notes.py", "ruler-decimal")
    pty("screen-rewrite", here / "tabs_and_notes.py", "rewrite")
    pty("toc-mark", here / "tabs_and_notes.py", "toc-mark")
    pty("contents-generation", here / "styles_contents.py", "contents")
    pty("named-styles", here / "styles_contents.py", "styles")
    pty("document-compare", here / "document_compare.py")
    pty("subdocument-link", here / "styles_contents.py", "subdocument")
    pty("page-cross-reference", here / "styles_contents.py", "cross-reference")
    pty("full-authority", here / "styles_contents.py", "authority")
    pty("successive-outline-levels", here / "styles_contents.py", "outline")
    pty("sort-secondary-merge", here / "styles_contents.py", "merge-sort")
    pty("column-math", here / "styles_contents.py", "column-math")
    if pty("spreadsheet", here / "spreadsheet.py") and not args.without_original:
        run("original-spreadsheet", "env", f"PYTHONPATH={reference_repo / 'scripts/reference'}",
            sys.executable, repo / "docs/research/reference-runs/mission1-spreadsheet/replay-wordling.py",
            output / "spreadsheet", output / "original-spreadsheet", reference_repo.resolve(),
            kind="original-03-09-92")
    pty("startup-macro", here / "startup_macro.py")
    pty("macro-control", here / "macro_control.py")
    if pty("macro-recording", here / "macro_recording.py") and not args.without_original:
        run("original-macro-recording", "env", f"PYTHONPATH={reference_repo / 'scripts/reference'}",
            sys.executable, repo / "docs/research/reference-runs/mission1-macro-recording/replay-wordling.py",
            output / "macro-recording", output / "original-macro-recording",
            kind="original-03-09-92")
    if pty("macro-edit", here / "macro_edit.py") and not args.without_original:
        run("original-macro-edit", "env", f"PYTHONPATH={reference_repo / 'scripts/reference'}",
            sys.executable, repo / "docs/research/reference-runs/mission1-macro-edit/replay-wordling.py",
            output / "macro-edit", output / "original-macro-edit", kind="original-03-09-92")
    pty("literal-printer-command", here / "printing.py", "literal")
    pty("line-draw-single", here / "styles_contents.py", "single-line-draw")
    pty("line-draw-double", here / "styles_contents.py", "double-line-draw")
    pty("language-code", here / "styles_contents.py", "language")
    pty("kerning-code", here / "styles_contents.py", "kerning")
    pty("font-italics", here / "styles_contents.py", "italics")
    pty("table-join", here / "styles_contents.py", "table-join")
    pty("table-calculate", here / "styles_contents.py", "table-calculate")
    pty("table-copy-formula", here / "styles_contents.py", "table-copy")
    pty("document-comment", here / "tabs_and_notes.py", "comment")
    pty("note-continuation", here / "tabs_and_notes.py", "note-continuation")
    pty("note-continuation-asymmetric", here / "tabs_and_notes.py", "note-continuation-asymmetric")
    pty("list-files-dos-text", here / "list_files_dos_text.py")
    pty("list-find-conditions", here / "list_find_conditions.py")
    pty("print-on-disk", here / "printing_on_disk.py")
    for key in CASES:
        if key != "proof-pages" or not args.without_proof:
            pty(key, here / "physical_cases.py", key)
    pty("preservation-corpus", here / "preservation_corpus.py")
    pty("summary", here / "summary.py")
    if pty("compose-editor", here / "compose_editor.py") and not args.without_original:
        run("original-compose", sys.executable, here / "compose_roundtrip.py",
            reference_repo.resolve(), output / "compose-editor/files/COMPOSE.WP",
            output / "original-compose", kind="original-03-09-92")
    if pty("compose-structural", here / "compose_structural.py") and not args.without_original:
        run("original-compose-structural", sys.executable, here / "compose_structural_dos.py",
            reference_repo.resolve(), output / "compose-structural",
            output / "original-compose-structural", kind="original-03-09-92")
    if not args.without_original:
        if run("compose-merged-resave", "env", "WORDLING_COMPOSE_DESTINATION_PAGE=1",
            sys.executable, here / "compose_merge_format.py", repo, binary,
            output / "compose-merged-resave", kind="product-pty-and-original-03-09-92"):
            run("replace-format-page", sys.executable, here / "replace_format_page.py",
                repo, binary, output / "compose-merged-resave/linux/files/RESAVED.WP5",
                output / "replace-format-page", kind="product-pty-and-original-03-09-92")
        run("replace-cross-page", sys.executable, here / "replace_cross_page.py",
            repo, binary, output / "replace-cross-page", kind="product-pty-and-original-03-09-92")
        for suffix, flags in (("", ()), ("-cancel", ("--cancel",)), ("-revisit", ("--revisit",))):
            label = "replace-backward-page" + suffix
            run(label, sys.executable, here / "replace_cross_page.py",
                repo, binary, output / label, "--backward", *flags,
                kind="product-pty-and-original-03-09-92")
        run("reopen-deferred-page", sys.executable, here / "reopen_deferred_page.py",
            repo, binary, output / "reopen-deferred-page", kind="product-pty-and-original-03-09-92")
    pty("replace-compose", here / "replace_compose.py")
    pty("replace-format", here / "replace_format.py")
    assert hashlib.sha256(args.fault_binary.read_bytes()).hexdigest() == record["fault_binary_sha256"]
    run("save-failure", sys.executable, here / "save_failure.py", repo, args.fault_binary.resolve(), output / "save-failure", kind="qa-build-product-pty-phase-fault")
    assert hashlib.sha256(args.fault_binary.read_bytes()).hexdigest() == record["fault_binary_sha256"]
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
            label = "original-" + name
            run(label, sys.executable, here / "original_roundtrip.py", reference_repo.resolve(),
                source, output / label, "--plain", kind="original-03-09-92")
    record["passed_executed_cases"] = all(row["returncode"] == 0 for row in record["cases"])
    manifest.write_text(json.dumps(record, indent=2) + "\n")
    return 0 if record["passed_executed_cases"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
