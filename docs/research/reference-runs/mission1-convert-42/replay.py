from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
import shutil,sys,time
import guest,qmp
out=Path(sys.argv[1]); out.mkdir()
with TemporaryDirectory(prefix="wp51-util-") as runtime:
    qmp.RUNTIME=guest.RUNTIME=Path(runtime)
    qmp.SOCKET=guest.SOCKET=Path(runtime)/"qmp.sock"
    private = out / "guest"
    command = guest.start(private)
    guest.stop()
    shutil.copyfile(guest.MASTER/"harddisk.img", private/"harddisk.img")
    run(["mcopy", "-i", str(private/"harddisk.img")+"@@1048576",
         "docs/research/reference-runs/mission1-formatting-search/SEARCH.WP", "::OUT/SOURCE.WP"], check=True)
    try:
        run(command,check=True)
        for _ in range(50):
            if qmp.SOCKET.is_socket(): break
            time.sleep(.1)
        with qmp.QMP() as q:
            q.wait_for("Doc 1 Pg",timeout=60)
            q.key("f7");q.wait_for("Save document?");q.key("n")
            q.wait_for("Exit WP?");q.key("y");q.wait_absent("Exit WP?")
            time.sleep(1)
            
            for c in "CONVERT":
                q.type(c); time.sleep(.2)
            q.wait_for("CONVERT")
            time.sleep(.9);q.key("ret");time.sleep(1)
            print(q.capture(out/"utility"),flush=True)
            time.sleep(1.2)
            for char in r"C:\OUT\SOURCE.WP":
                q.type(char)
                time.sleep(.18)
            q.wait_for("SOURCE.WP")
            q.key("ret")
            q.wait_for("Name of Output File")
            print(q.capture(out/"output-prompt"),flush=True)
            for char in r"C:\OUT\LEGACY.WP4":
                q.type(char)
                time.sleep(.15)
            q.key("ret")
            time.sleep(1.2)
            menu = q.capture(out/"target-format")
            assert "8 WordPerfect 4.2 to WordPerfect 5.1" in menu
            print(menu, flush=True)
            q.key("1")
            q.wait_for("Enter number of output file format desired")
            formats = q.capture(out/"wp-target")
            assert "WordPerfect 4.2" not in formats
            print(formats, flush=True)
    finally:
        guest.stop()
