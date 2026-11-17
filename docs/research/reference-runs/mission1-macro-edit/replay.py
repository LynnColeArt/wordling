from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
import sys,time,shutil
import guest,qmp
root=Path(sys.argv[1]); mode=sys.argv[2]; root.mkdir()
with TemporaryDirectory(prefix="wp-wpm-options-") as runtime:
    guest.RUNTIME=qmp.RUNTIME=Path(runtime); guest.SOCKET=qmp.SOCKET=guest.RUNTIME/'qmp.sock'
    try:
        p=root/'guest'
        command=guest.start(p); guest.stop()
        shutil.copyfile(guest.MASTER / "harddisk.img", p / "harddisk.img")
        src=Path('docs/research/reference-runs/mission1-macro-recording/TYPED.WPM')
        disk=str(p/'harddisk.img')+'@@1048576'
        run(['mcopy','-i',disk,str(src),'::OUT/TYPED.WPM'],check=True)
        run(command,check=True)
        with qmp.QMP() as q:
            def keys(*items):
                for item in items:
                    q.key(item);time.sleep(.23)
            def snap(name):
                time.sleep(.5); s=q.capture(root/name);print(name," | ".join(row.strip() for row in s.splitlines() if row.strip()),flush=True)
            def type_text(value):
                for c in value: q.type(c);time.sleep(.13)
            q.wait_for('Doc 1 Pg',timeout=60)
            keys('ctrl-f10'); q.wait_for('Define macro:')
            type_text(r'C:\OUT\TYPED'); keys('ret');snap('exists')
            keys("3" if mode=="description" else "2")
            if mode=="description":
                q.wait_for("Description:"); snap("prefill")
                keys("end")
                for _ in "Keys and text":keys("backspace")
                type_text("Revised")
                keys("ret")
            q.wait_for("Macro: Action")
            snap("action")
            if mode=="action":
                keys("right")
                type_text("Z")
                snap("insert")
                keys("delete")
                snap("delete")
            if mode in ("commands", "left", "middle"):
                keys("right","right")
                if mode == "middle": keys("right")
                keys("ctrl-v","left");snap("insert-command")
                if mode in ("commands", "middle"): keys("ret");snap("insert-enter")
            if mode=="cancel":
                keys("right");type_text("Z");keys("f1");snap("cancel")
                state=q.text(root/"cancel-state")
                if "Doc 1 Pg" not in state:
                    if "No (Yes)" in state or "Yes (No)" in state: keys("y")
                    else: keys("f7")
            else: keys("f7")
            snap("exit-action")
            s=q.text(root/"state")
            if "Save macro?" in s or "Save changes" in s: keys("y");snap("confirmed")
            q.wait_for("Doc 1 Pg"); keys("f7");q.wait_for("Save document?");keys("n")
            q.wait_for("Exit WP?");keys("y");q.wait_absent("Exit WP?")
        guest.stop()
        run(['mcopy','-i',disk,'::OUT/TYPED.WPM',str(root/'EDITED.WPM')],check=True)
    finally: guest.stop()
