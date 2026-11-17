#!/usr/bin/env python3
"""Rebuild a private WP reference installation from checksum-pinned media."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import time
import urllib.request
from zipfile import ZipFile

from guest import arguments, stop
from qmp import QMP, ROOT, RUNTIME

BASE = ROOT / "research/cache/reference"
SOURCES = [
    ("wp51-1992-03.zip", "https://archive.org/download/word-perfect-5.1-for-dos-5.1-1992-03-3.5-720-kb-english/WordPerfect%205.1%20for%20DOS%20%285.1%29%20%281992-03%29%20%283.5%27%27-720KB%29%20%5BEnglish%5D.zip", "ac221a63b034567a2b5605604e684fee1d7ed45cf57166c20005025fda51d002"),
    ("FD14-FloppyEdition.zip", "https://download.freedos.org/1.4/FD14-FloppyEdition.zip", "45b1fa7c52dd996c3bfa5e352ffcd410781b952a6ad629f15a4c9ec4bbaefc5a"),
]
CONFIG = "FILES=40\r\nBUFFERS=20\r\nLASTDRIVE=Z\r\nSHELL=\\FREEDOS\\BIN\\COMMAND.COM \\FREEDOS\\BIN /E:2048 /P=\\FDAUTO.BAT\r\n"
AUTO = "@echo off\r\nset PATH=A:\\FREEDOS\\BIN;C:\\WP51\r\nset LANG=EN\r\nset TZ=UTC\r\nprompt $P$G\r\nC:\r\n"


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def media():
    directory = BASE / "media"
    directory.mkdir(parents=True, exist_ok=True)
    for filename, url, digest in SOURCES:
        path = directory / filename
        if not path.exists():
            temporary = path.with_suffix(".download")
            try:
                with urllib.request.urlopen(url, timeout=60) as response, temporary.open("wb") as output:
                    shutil.copyfileobj(response, output)
                if sha(temporary) != digest:
                    raise ValueError(f"Downloaded media checksum mismatch: {filename}")
                temporary.replace(path)
            finally:
                temporary.unlink(missing_ok=True)
        if sha(path) != digest:
            raise ValueError(f"Cached media checksum mismatch: {filename}")
    disks = directory / "wp-disks"
    disks.mkdir(exist_ok=True)
    with ZipFile(directory / SOURCES[0][0]) as archive:
        for name in archive.namelist():
            if name.endswith(".img"):
                (disks / Path(name).name).write_bytes(archive.read(name))
    with ZipFile(directory / SOURCES[1][0]) as archive:
        (directory / "fd14-boot-original.img").write_bytes(archive.read("144m/x86BOOT.img"))
    return directory


def chs(lba):
    cylinder, rem = divmod(lba, 16 * 63)
    head, sector = divmod(rem, 63)
    return bytes([head, ((sector + 1) & 63) | ((cylinder >> 2) & 0xC0), cylinder & 255])


def inject(boot, directory, name, content):
    path = directory / name
    path.write_bytes(content.encode("ascii"))
    os.utime(path, (700142400, 700142400))
    subprocess.run(["mcopy", "-o", "-m", "-i", str(boot), str(path), "::" + name],
                   env={**os.environ, "TZ": "UTC"}, check=True)


def build(directory, source):
    directory.mkdir(parents=True)
    disk, boot = directory / "harddisk.img", directory / "boot.img"
    with disk.open("wb") as stream:
        stream.truncate(64 * 1024 * 1024)
    start, sectors = 2048, disk.stat().st_size // 512 - 2048
    mbr = bytearray(512)
    mbr[446:462] = struct.pack("<B3sB3sII", 128, chs(start), 6, chs(start + sectors - 1), start, sectors)
    mbr[510:512] = bytes.fromhex("55aa")
    with disk.open("r+b") as stream:
        stream.write(mbr)
    subprocess.run(["mkfs.fat", "--offset", "2048", "-F", "16", "-n", "WORDLINGREF", "-i", "19920309", str(disk)], check=True)
    shutil.copyfile(source / "fd14-boot-original.img", boot)
    inject(boot, directory, "FDCONFIG.SYS", CONFIG)
    inject(boot, directory, "FDAUTO.BAT", AUTO)
    command = arguments(boot, disk)
    command[-1:-1] = ["-drive", f"file={source / 'wp-disks/install.img'},format=raw,if=floppy,index=1,readonly=on,id=wpmedia"]
    subprocess.run(command, check=True)
    trace = []
    try:
        with QMP() as q:
            q.wait_for("C:\\>", 30)
            q.type("B:\\INSTALL"); q.key("ret")
            deadline, previous = time.monotonic() + 180, ""
            while time.monotonic() < deadline:
                screen = q.text(RUNTIME / "inspect")
                if screen == previous:
                    time.sleep(.15)
                    continue
                previous = screen
                action = None
                if "Installation Complete." in screen:
                    break
                elif "Do you want to Continue?" in screen:
                    action = "y"
                elif "red, green, and blue" in screen or "Installing to a Hard Disk?" in screen:
                    action = "y"
                elif "1 - Basic" in screen and "Selection: 1" in screen:
                    action = "ret"
                elif "Do you want to install" in screen and "another printer" not in screen and ("(No)" in screen or "(Yes)" in screen):
                    action = "y"
                elif "not found.  Create it?" in screen:
                    action = "n"
                elif "Insert the" in screen and "master diskette into" in screen:
                    names = {"Program 1": "prog1.img", "Spell/Thesaurus 1": "spell_th.img",
                             "PTR Program": "ptrgraph.img", "Graphics 1": "ptrgraph.img",
                             "Printer master": "printer1.img"}
                    filename = next((v for k, v in names.items() if "Insert the " + k in screen), None)
                    if filename is None:
                        raise RuntimeError("Unrecognized installation disk request:\n" + screen)
                    result = q.hmp(f'change wpmedia "{source / "wp-disks" / filename}" raw')
                    if result:
                        raise RuntimeError(result)
                    action = "ret"
                elif "N Name Search;" in screen and "Selection: 0" in screen:
                    q.key("n"); q.type("Standard Printer"); q.key("ret")
                    screen = q.wait_until(lambda s: re.search(r"^\s*\d+\s+Standard Printer(?:\s|$)", s, re.M) is not None and "Selection: 0" in s, "Standard Printer search result")
                    number = re.search(r"^\s*(\d+)\s+Standard Printer(?:\s|$)", screen, re.M).group(1)
                    q.type(number); action = "ret"
                elif "Select printer Standard Printer?" in screen:
                    action = "y"
                elif "Do you want to install another printer?" in screen:
                    action = "n"
                elif "Enter license number:" in screen:
                    action = "ret"  # This original optional display field is left blank.
                elif "Press any key to exit" in screen:
                    action = "ret"
                if action:
                    trace.append({"screen": screen, "key": action})
                    q.key(action)
                time.sleep(.15)
            else:
                raise TimeoutError("Unrecognized/stalled installer:\n" + screen)
            q.wait_for("C:\\>")
            q.type("CD \\WP51"); q.key("ret"); q.type("WP"); q.key("ret")
            q.wait_for('Doc 1 Pg 1 Ln 1" Pos 1"', 60)
            q.key("f3"); q.wait_for("WP 5.1   03/09/92")
            q.capture(directory / "release-identification")
            q.key("ret"); q.key("f7"); q.wait_for("Save document?")
            q.key("n"); q.key("y"); q.wait_for("C:\\WP51>")
    finally:
        stop()
        (directory / "installation-trace.json").write_text(json.dumps(trace, indent=2) + "\n")
    subprocess.run(["mmd", "-i", str(disk) + "@@1048576", "::OUT"], check=True)
    inject(boot, directory, "FDAUTO.BAT", AUTO + "cd \\WP51\r\nWP\r\n")
    (directory / "build-manifest.json").write_text(json.dumps({"boot_sha256": sha(boot), "disk_sha256": sha(disk), "qemu_argv": command}, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build_id", help="New private build directory; existing outputs are never overwritten")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.build_id):
        parser.error("build_id must contain only letters, digits, underscores and hyphens")
    destination = BASE / "build" / args.build_id
    if destination.exists():
        raise FileExistsError(destination)
    if (RUNTIME / "qmp.sock").exists():
        raise RuntimeError("Stop the reference guest before rebuilding")
    build(destination, media())
    print("Built", destination)
