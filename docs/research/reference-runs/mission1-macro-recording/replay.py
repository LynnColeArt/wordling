from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
import sys, time
import guest, qmp

out = Path(sys.argv[1])
out.mkdir()
with TemporaryDirectory(prefix="wp-macro-record-") as runtime:
    guest.RUNTIME = qmp.RUNTIME = Path(runtime)
    guest.SOCKET = qmp.SOCKET = guest.RUNTIME / "qmp.sock"
    try:
        private = out / "guest"
        guest.start(private)
        with qmp.QMP() as q:
            def keys(*items):
                for item in items:
                    q.key(item)
                    time.sleep(.25)
            q.wait_for("Doc 1 Pg", timeout=60)
            keys("ctrl-f10")
            q.wait_for("Define macro:")
            q.capture(out / "name")
            q.type(r"C:\OUT\TYPED")
            q.wait_for("TYPED")
            keys("ret")
            q.wait_for("escription")
            q.capture(out / "description")
            q.type("Keys and text")
            time.sleep(.5)
            keys("ret")
            q.type("A B")
            time.sleep(.5)
            keys("ret")
            q.type("C")
            time.sleep(.5)
            keys("left", "ctrl-f10")
            q.capture(out / "typed")
            keys("f7")
            q.wait_for("Save document?")
            keys("n")
            q.wait_for("Exit WP?")
            keys("y")
            q.wait_absent("Exit WP?")
        guest.stop()
        run(["mcopy", "-i", str(private / "harddisk.img") + "@@1048576",
             "::OUT/TYPED.WPM", str(out / "TYPED.WPM")], check=True)
    finally:
        guest.stop()
