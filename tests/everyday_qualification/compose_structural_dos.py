"""Reopen Wordling's structural Compose saves in the pinned DOS guest."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

from qualification import native

repo, files, output = (Path(arg).resolve() for arg in sys.argv[1:])
sys.path.insert(0, str(repo / "scripts/reference"))
import guest
import qmp

output.mkdir()
for role in ("table", "merge", "primary"):
    source = files / role / "files/COMPOSE.WP"
    with tempfile.TemporaryDirectory(prefix="wp-structural-") as tmp:
        guest.RUNTIME = qmp.RUNTIME = Path(tmp)
        guest.SOCKET = qmp.SOCKET = Path(tmp) / "qmp.sock"
        private = Path(tmp) / "guest"
        command = guest.start(private)
        guest.stop()
        shutil.copyfile(guest.MASTER / "harddisk.img", private / "harddisk.img")
        disk = str(private / "harddisk.img") + "@@1048576"
        subprocess.run(["mcopy", "-i", disk, str(source), "::OUT/WORDLING.WP"], check=True)
        subprocess.run(command, check=True)
        try:
            with qmp.QMP() as q:
                q.wait_for("Doc 1 Pg 1", timeout=60)
                q.key("f3")
                q.wait_for("03/09/92")
                q.key("ret")
                q.key("shift-f10")
                q.wait_for("Document to be retrieved")
                q.type(r"C:\OUT\WORDLING.WP")
                q.key("ret")
                q.wait_for("Æ")
                q.capture(output / role / "reopened")
                q.key("alt-f3")
                if role == "table":
                    q.key("down")
                else:
                    q.key("right")
                    if role == "merge":
                        # Navigate directly to the second field's composed character.
                        q.key("down")
                if role != "table":
                    screen = q.text(guest.RUNTIME / "position")
                    if "[Æ:1,36]" not in screen:
                        q.key("left")
                        q.key("right")
                q.wait_for("[Æ:1,36]")
                q.capture(output / role / "reveal")
                q.key("f10")
                q.wait_for("Document to be saved")
                q.type(r"C:\OUT\ROUND.WP")
                q.key("ret")
                q.wait_until(lambda screen: "Doc 1 Pg" in screen and "Saving C:" not in screen
                             and "Document to be saved" not in screen,
                             "settled original save and document status", timeout=35)
                q.capture(output / role / "resaved")
                q.key("alt-f3")
                q.key("f7")
                q.wait_for("Save document?")
                q.key("n")
                q.wait_for("Exit WP?")
                q.key("y")
                q.wait_absent("Doc 1 Pg")
                time.sleep(.25)
        finally:
            guest.stop()
        returned = output / role / "ROUND.WP"
        subprocess.run(["mcopy", "-i", disk, "::OUT/ROUND.WP", str(returned)], check=True)
        assert native(returned)[2] == native(source)[2], role
