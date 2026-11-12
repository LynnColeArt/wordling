#!/usr/bin/env python3
"""Start a fresh, offline QEMU copy of the local WP reference installation."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time

from qmp import QMP, ROOT, RUNTIME, SOCKET

MASTER = ROOT / "research/cache/reference/master"


def arguments(boot, disk):
    return ["qemu-system-i386", "-machine", "pc-i440fx-8.2", "-accel", "tcg,thread=single",
            "-cpu", "486", "-m", "16", "-vga", "std", "-bios", "/usr/share/seabios/bios-256k.bin",
            "-display", "none", "-serial", "none", "-parallel", "none", "-nic", "none",
            "-rtc", "base=1992-03-09T12:00:00,clock=vm",
            "-drive", f"file={boot},format=raw,if=floppy,index=0",
            "-drive", f"file={disk},format=raw,if=ide,index=0",
            "-boot", "order=a", "-qmp", f"unix:{SOCKET},server=on,wait=off",
            "-monitor", "none", "-pidfile", str(RUNTIME / "qemu.pid"), "-daemonize"]


def start(directory):
    manifest = ROOT / "docs/research/reference-environment/environment.json"
    profile = json.loads(manifest.read_text())
    pinned = [(MASTER / "harddisk.img", profile["master_disk_sha256"]),
              (MASTER / "boot.img", profile["master_boot_sha256"]),
              (Path(profile["qemu_binary"]["path"]), profile["qemu_binary"]["sha256"])]
    pinned += [(Path(f["path"]), f["sha256"]) for f in profile["firmware"]]
    for path, digest in pinned:
        with path.open("rb") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
        if actual != digest:
            raise ValueError(f"Reference identity mismatch: {path}; record a new profile instead of silently reusing evidence")
    if SOCKET.exists():
        try:
            with QMP() as q:
                q.execute("query-status")
        except (ConnectionRefusedError, FileNotFoundError):
            SOCKET.unlink(missing_ok=True)
        else:
            raise RuntimeError("Reference guest already running; stop it before replacing disks")
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    if (directory / "harddisk.img").exists():
        raise FileExistsError(f"Refusing to overwrite prior run {directory}")
    for name in ["boot.img", "harddisk.img"]:
        shutil.copyfile(MASTER / name, directory / name)
    RUNTIME.mkdir(parents=True, exist_ok=True)
    command = arguments(directory / "boot.img", directory / "harddisk.img")
    subprocess.run(command, check=True)
    try:
        with QMP() as q:
            q.wait_for('Doc 1 Pg 1 Ln 1" Pos 1"', timeout=60)
    except BaseException:
        stop()
        raise
    return command


def stop():
    if not SOCKET.exists():
        return
    try:
        with QMP() as q:
            q.execute("quit")
    except (ConnectionRefusedError, FileNotFoundError):
        pass
    deadline = time.monotonic() + 5
    while SOCKET.exists() and time.monotonic() < deadline:
        time.sleep(.05)
    if SOCKET.exists():
        raise RuntimeError("Guest did not terminate; do not read or replace live disks")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=["start", "stop"])
    p.add_argument("directory", nargs="?")
    a = p.parse_args()
    if a.action == "start":
        if not a.directory:
            p.error("start requires a new run directory")
        print(start(a.directory))
    else:
        stop()
