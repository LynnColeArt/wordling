"""Open, reveal and edit a Wordling Compose save in the pinned DOS release."""
import json
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile

from qualification import native, native_info

repo, candidate, out = (Path(arg).resolve() for arg in sys.argv[1:])
sys.path.insert(0, str(repo / "scripts/reference"))
import guest
import qmp

out.mkdir()
with tempfile.TemporaryDirectory(prefix="wp-compose-") as tmp:
    guest.RUNTIME = qmp.RUNTIME = Path(tmp)
    guest.SOCKET = qmp.SOCKET = Path(tmp) / "qmp.sock"
    private = Path(tmp) / "guest"
    command = guest.start(private)
    guest.stop()
    shutil.copyfile(guest.MASTER / "harddisk.img", private / "harddisk.img")
    disk = str(private / "harddisk.img") + "@@1048576"
    subprocess.run(["mcopy", "-i", disk, str(candidate), "::OUT/WPLIVE.WP"], check=True)
    subprocess.run(command, check=True)
    try:
        with qmp.QMP() as q:
            q.wait_for("Doc 1 Pg 1", timeout=60)
            q.key("f3")
            q.wait_for("03/09/92")
            q.capture(out / "release")
            q.key("ret")
            q.key("shift-f10")
            q.wait_for("Document to be retrieved")
            q.type(r"C:\OUT\WPLIVE.WP")
            q.key("ret")
            q.wait_for("Æ X")
            q.capture(out / "reopened")
            q.key("alt-f3")
            q.wait_for("Press Reveal Codes")
            screen = q.capture(out / "reveal")
            assert "Æ X" in screen.splitlines() and "[Æ:1,36] X" in screen.splitlines(), screen
            q.key("alt-f3")
            q.type("A")
            q.wait_for("AÆ X")
            q.key("f10")
            q.wait_for("Document to be saved")
            q.type(r"C:\OUT\ROUND.WP")
            q.key("ret")
            q.wait_until(lambda screen: any("ROUND.WP" in line and "Doc 1 Pg" in line for line in screen.splitlines())
                         and "Saving C:" not in screen, "settled DOS Save", timeout=35)
            q.capture(out / "resaved")
    finally:
        guest.stop()
    returned = out / "ROUND.WP"
    subprocess.run(["mcopy", "-i", disk, "::OUT/ROUND.WP", str(returned)], check=True)
    assert native(returned)[2] == b"A" + native(candidate)[2]
    (out / "result.json").write_text(json.dumps({
        "reference": "WordPerfect 5.1 DOS 03/09/92",
        "candidate": native_info(candidate), "returned": native_info(returned),
        "result": "pass",
    }, indent=2) + "\n")
