"""Play Wordling-edited WPMs in the pinned WordPerfect DOS guest."""
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
import shutil
import struct
import sys
import time

import guest
import qmp

source, dest = (Path(arg).resolve() for arg in sys.argv[1:3])
dest.mkdir()
cases = (
    ("action", b"Z B\x0aXC", "Z B", "XC"),
    ("description", b"A B\x0aXC", "A B", "XC"),
    ("commands", b"AB\x0aXC ", "AB", "XC"),
)
with TemporaryDirectory(prefix="wordling-recording-replay-") as runtime:
    guest.RUNTIME = qmp.RUNTIME = Path(runtime)
    guest.SOCKET = qmp.SOCKET = guest.RUNTIME / "qmp.sock"
    try:
        private = dest / "guest"
        command = guest.start(private)
        guest.stop()
        disk = str(private / "harddisk.img") + "@@1048576"
        for label, expected, cue, caret in cases:
            shutil.copyfile(guest.MASTER / "harddisk.img", private / "harddisk.img")
            name, file = "TYPED", "TYPED.WPM"
            original = source / label / "files/OUT" / file
            run(["mcopy", "-i", disk, str(original), "::OUT/" + file], check=True)
            run(command, check=True)
            with qmp.QMP() as q:
                q.wait_for("Doc 1 Pg", timeout=60)
                q.key("alt-f10")
                q.wait_for("Macro:")
                q.type("C:\\OUT\\" + name)
                q.wait_for(name)
                q.key("ret")
                q.wait_for(cue)
                time.sleep(.3)
                q.type("X")
                q.wait_for(caret)
                screen = q.capture(dest / label)
                assert caret in screen
                q.key("f10")
                q.wait_for("Document to be saved")
                q.type(r"C:\OUT\PLAYED.WP")
                q.wait_for("PLAYED.WP")
                q.key("ret")
                q.wait_absent("Document to be saved")
                q.wait_for("Doc 1 Pg")
                time.sleep(.6)
                q.key("f7")
                q.wait_for("Save document?")
                q.key("n")
                q.wait_for("Exit WP?")
                q.key("y")
                q.wait_absent("Exit WP?")
            guest.stop()
            output = dest / label / "PLAYED.WP"
            run(["mcopy", "-i", disk, "::OUT/PLAYED.WP", str(output)], check=True)
            saved = output.read_bytes()
            offset, = struct.unpack_from("<I", saved, 4)
            assert saved[offset:] == expected, (saved[offset:], expected)
            copied = dest / label / file
            run(["mcopy", "-i", disk, "::OUT/" + file, str(copied)], check=True)
            assert copied.read_bytes() == original.read_bytes()
            print(label, repr(saved[offset:]), flush=True)
    finally:
        guest.stop()
