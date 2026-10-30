#!/usr/bin/env python3
"""Verify retained WP16 source/capture hashes and explicit evidence scope."""
import hashlib
import json
from pathlib import Path
import subprocess


def check(path, row):
    raw = path.read_bytes()
    assert len(raw) == row["bytes"] and hashlib.sha256(raw).hexdigest() == row["sha256"], path


def main():
    evidence = Path(__file__).resolve().parent
    root = evidence.parents[3]
    sources = json.loads((evidence/"source-manifest.json").read_text())
    assert sources["scope"] == "WP16-component-and-synthetic-transport-only"
    assert sources["physical_qualified"] is False
    for row in sources["sources"]:
        check(root/row["path"], row)
    cache = Path(subprocess.check_output(["go", "env", "GOMODCACHE"], cwd=root, text=True).strip())
    for row in sources["dependency_sources"]:
        check(cache/row["path"], row)
    for row in sources["governance_inputs"]:
        raw = subprocess.check_output(["git", "show", row["revision"]+":"+row["path"]], cwd=root)
        assert len(raw) == row["bytes"] and hashlib.sha256(raw).hexdigest() == row["sha256"]
    for run in ["run-01", "run-02"]:
        manifest = json.loads((evidence/run/"manifest.json").read_text())
        assert manifest["scope"] == "synthetic-pty-only" and manifest["physical_qualified"] is False
        assert manifest["driver_sha256"] == hashlib.sha256((root/"cmd/wordling-input-probe/pty_test.py").read_bytes()).hexdigest()
        for row in manifest["files"]:
            check(evidence/run/row["path"], row)
        for name in ["synthetic-enhanced", "synthetic-legacy-fast", "synthetic-legacy-slow", "synthetic-host-sigterm"]:
            rows = [json.loads(line) for line in (evidence/run/name/"journal.jsonl").read_text().splitlines()]
            assert rows[0]["kind"] == "profile" and rows[0]["value"]["transport_assertion"] == "synthetic-pty"
            assert rows[0]["value"]["qualification"] == "unqualified-capture"
            assert rows[-1]["kind"] == "end" and rows[-1]["value"]["terminal_state_restored"]
            assert rows[-1]["value"]["deadline_reached"] == (name != "synthetic-host-sigterm")
            assert bool(rows[-1]["value"]["run_error"]) == (name == "synthetic-host-sigterm")
            assert [r["sequence"] for r in rows] == list(range(1, len(rows)+1))
            assert [r["nanoseconds_since_start"] for r in rows] == sorted(r["nanoseconds_since_start"] for r in rows)
            raw = b"".join(bytes.fromhex(r["value"]) for r in rows if r["kind"] == "raw-input")
            sent = json.loads((evidence/run/name/"injected.json").read_text())
            assert raw == b"".join(bytes.fromhex(s["hex"]) for s in sent)
    print("WP16 sources and two independent synthetic PTY repetitions verified; physical delivery unqualified")


if __name__ == "__main__":
    main()
