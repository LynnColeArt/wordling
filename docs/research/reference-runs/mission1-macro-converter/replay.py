from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
import shutil,sys,time
import guest,qmp
out=Path(sys.argv[1]); out.mkdir()
with TemporaryDirectory(prefix="wp51-util-") as runtime:
    qmp.RUNTIME=guest.RUNTIME=Path(runtime)
    qmp.SOCKET=guest.SOCKET=Path(runtime)/"qmp.sock"
    shutil.copyfile(guest.MASTER/"boot.img",out/"boot.img")
    shutil.copyfile(guest.MASTER/"harddisk.img",out/"harddisk.img")
    try:
        run(guest.arguments(out/"boot.img",out/"harddisk.img"),check=True)
        for _ in range(50):
            if qmp.SOCKET.is_socket(): break
            time.sleep(.1)
        with qmp.QMP() as q:
            q.wait_for("Doc 1 Pg",timeout=60)
            q.key("f7");q.wait_for("Save document?");q.key("n")
            q.wait_for("Exit WP?");q.key("y");q.wait_absent("Exit WP?")
            time.sleep(1)
            
            for c in "MACROCNV":
                q.type(c); time.sleep(.2)
            q.wait_for("MACROCNV")
            time.sleep(.9);q.key("ret");time.sleep(1)
            print(q.capture(out/"utility"),flush=True)
    finally:
        guest.stop()
