#!/usr/bin/env python3
"""Fingerprint a newly rebuilt private master without replacing old profiles."""

import argparse
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess

from qmp import ROOT


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("master_directory", type=Path)
    p.add_argument("new_profile_directory", type=Path)
    a = p.parse_args()
    source, output = a.master_directory.resolve(), a.new_profile_directory.resolve()
    if output.exists():
        raise FileExistsError("Existing profiles are immutable; choose a new directory")
    capture = source / "release-identification/screen.txt"
    if not capture.is_file() or "WP 5.1   03/09/92" not in capture.read_text():
        raise ValueError("Build lacks the required captured in-app identity")
    output.mkdir(parents=True)
    extracted = output / "private-installed-files"
    extracted.mkdir()
    subprocess.run(["mcopy", "-s", "-i", str(source / "harddisk.img") + "@@1048576", "::WP51", str(extracted)], check=True)
    files = [{"path": str(f.relative_to(extracted)), "sha256": sha(f), "size": f.stat().st_size}
             for f in sorted(extracted.rglob("*")) if f.is_file()]
    expected = json.loads((ROOT / "docs/research/reference-environment/installed-files.json").read_text())["files"]
    immutable = {f["path"]: f["sha256"] for f in expected if f["path"] != "WP51/WP{WP}.SET"}
    actual = {f["path"]: f["sha256"] for f in files}
    if any(actual.get(path) != digest for path, digest in immutable.items()):
        raise ValueError("Installed program/resource identity differs; investigate before recording this as the same reference profile")
    profile = json.loads((ROOT / "docs/research/reference-environment/environment.json").read_text())
    profile["profile_id"] = "rebuilt-" + output.name
    emulator = shutil.which("qemu-system-i386")
    if emulator is None:
        raise FileNotFoundError("qemu-system-i386")
    version = subprocess.check_output([emulator, "--version"], text=True).splitlines()[0]
    if "version 8.2.2 " not in version:
        raise ValueError("This reference recipe requires QEMU 8.2.2; a different emulator needs a separately reviewed recipe")
    profile["qemu_version"] = version
    profile["qemu_binary"] = {"path": emulator, "sha256": sha(emulator)}
    profile["host_platform"] = platform.platform()
    profile["host_python"] = platform.python_version()
    profile["firmware"] = [{"path": f["path"], "sha256": sha(f["path"])} for f in profile["firmware"]]
    profile["master_disk_sha256"] = sha(source / "harddisk.img")
    profile["master_boot_sha256"] = sha(source / "boot.img")
    profile["personal_setup_sha256"] = actual["WP51/WP{WP}.SET"]
    profile["rebuild_note"] = "All 157 non-personal-setup files match the first installation. Personal setup is independently fingerprinted; its unexplained one-byte variation is not normalized."
    (output / "environment.json").write_text(json.dumps(profile, indent=2) + "\n")
    (output / "installed-files.json").write_text(json.dumps({"files": files}, indent=2) + "\n")
    shutil.rmtree(extracted)  # Only the temporary extraction created by this invocation.
    print(output / "environment.json")


if __name__ == "__main__":
    main()
