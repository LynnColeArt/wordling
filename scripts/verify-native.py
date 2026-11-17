#!/usr/bin/env python3
"""Verify the packaged build for this host without a source checkout or fixtures."""
from pathlib import Path
import hashlib
import json
import platform
import subprocess
import sys
import tempfile
import zipfile


def main():
    host = {"Windows": "windows", "Darwin": "darwin", "Linux": "linux"}[platform.system()]
    arch = {"amd64": "amd64", "x86_64": "amd64", "arm64": "arm64", "aarch64": "arm64"}[platform.machine().lower()]
    name = f"wordling-prerelease-{host}-{arch}"
    source = Path(sys.argv[1]).resolve() / (name + ".zip")
    print(f"Native host: {platform.platform()}; target: {host}/{arch}", flush=True)
    with tempfile.TemporaryDirectory(prefix="wordling-native-smoke-") as temporary:
        with zipfile.ZipFile(source) as archive:
            archive.extractall(temporary)
        root = Path(temporary) / name
        suffix = ".exe" if host == "windows" else ""
        hashes = json.loads((root / "SHA256SUMS.json").read_text())
        for filename, expected in hashes.items():
            if hashlib.sha256((root / filename).read_bytes()).hexdigest() != expected:
                raise RuntimeError(f"package hash mismatch: {filename}")
        candidate = json.loads((root / "candidate.json").read_text())
        if candidate["qa_save_faults"] or candidate["target"] != {"goos": host, "goarch": arch}:
            raise RuntimeError("package is not a normal build for this target")
        if hashes["wordling" + suffix] != candidate["binary_sha256"]:
            raise RuntimeError("candidate record does not match packaged executable")
        for binary, arguments in (
            ("storage-smoke", ["-test.run", "^TestNativePlatform", "-test.v"]),
            ("recovery-smoke", ["-test.run", "^TestNative", "-test.v"]),
            ("wordling", ["-help"]),
        ):
            path = root / (binary + suffix)
            path.chmod(0o755)
            subprocess.run([str(path), *arguments], cwd=root, check=True)


if __name__ == "__main__":
    main()
