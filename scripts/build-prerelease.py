#!/usr/bin/env python3
"""Build normal native prerelease ZIPs with source provenance and native smoke tests."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {f"{host}/{arch}" for host in ("linux", "darwin", "windows") for arch in ("amd64", "arm64")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", action="append", choices=sorted(TARGETS), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    for target in dict.fromkeys(args.target):
        host, arch = target.split("/")
        name = f"wordling-prerelease-{host}-{arch}"
        folder = output / name
        subprocess.run([sys.executable, str(ROOT / "tests/everyday_qualification/build_candidate.py"),
                        str(ROOT), str(folder), "--goos", host, "--goarch", arch], cwd=ROOT, check=True)
        env = dict(os.environ, GOOS=host, GOARCH=arch, CGO_ENABLED="0")
        suffix = ".exe" if host == "windows" else ""
        for package, binary in (("./internal/storage", "storage-smoke"), ("./internal/tui", "recovery-smoke")):
            subprocess.run(["go", "test", "-tags=", "-trimpath", "-buildvcs=false", "-c", "-o",
                            str(folder / (binary + suffix)), package], cwd=ROOT, env=env, check=True)
        windows = host == "windows"
        prefix = ".\\" if windows else "./"
        lines = [
            "Wordling native prerelease — engineering test build",
            "",
            "Run the fixture-free smoke tests first (they use temporary directories):",
            f"{prefix}storage-smoke{suffix} -test.run '^TestNativePlatform' -test.v",
            f"{prefix}recovery-smoke{suffix} -test.run '^TestNative' -test.v",
            "",
            "Then open a scratch directory in your terminal:",
            f'{prefix}wordling{suffix} -root "ABSOLUTE_SCRATCH_DIRECTORY" -control-keys',
            "",
            "Test F10 Save, Shift+F10 Retrieve, menus, terminal keys, mouse, and restart recovery.",
            "Use scratch copies; this build is not full WordPerfect parity acceptance.",
            "candidate.json records the exact source commit, target and compiled inputs.",
            "SHA256SUMS.json covers every file in this package except itself.",
        ]
        if windows:
            lines += ["", "Windows limitations:",
                      "Save to a NEW filename. Existing-file replacement is explicitly refused.",
                      "File contents are flushed; directory-entry power-loss durability is unqualified.",
                      "Recovery uses native byte-range locking; test crashes/restarts on your actual volume."]
        else:
            lines += ["", "The filesystem must support atomic exclusive rename and atomic file exchange.",
                      "Unsupported filesystems must return an error; no multi-rename fallback is used."]
        (folder / "README.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        files = sorted(p for p in folder.iterdir() if p.is_file())
        hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
        (folder / "SHA256SUMS.json").write_text(json.dumps(hashes, indent=2) + "\n")
        archive = output / (name + ".zip")
        with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as zipped:
            for path in sorted(folder.iterdir()):
                if path.is_file():
                    zipped.write(path, arcname=f"{name}/{path.name}")
        print(archive, flush=True)


if __name__ == "__main__":
    main()
