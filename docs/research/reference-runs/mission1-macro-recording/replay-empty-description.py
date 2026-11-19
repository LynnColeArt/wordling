from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
import sys,time,shutil
import guest,qmp
out=Path(sys.argv[1]); out.mkdir()
with TemporaryDirectory(prefix="wp-wpm-options-") as runtime:
    guest.RUNTIME=qmp.RUNTIME=Path(runtime); guest.SOCKET=qmp.SOCKET=guest.RUNTIME/'qmp.sock'
    try:
        p=out/'guest'
        command=guest.start(p); guest.stop()
        shutil.copyfile(guest.MASTER / "harddisk.img", p / "harddisk.img")
        src=Path('docs/research/reference-runs/mission1-macro-recording/TYPED.WPM')
        disk=str(p/'harddisk.img')+'@@1048576'
        run(['mcopy','-i',disk,str(src),'::OUT/TYPED.WPM'],check=True)
        run(command,check=True)
        with qmp.QMP() as q:
            def keys(*items):
                for item in items:
                    q.key(item);time.sleep(.22)
            def snap(name):
                time.sleep(.7);print(name, repr(q.capture(out/name)),flush=True)
            q.wait_for('Doc 1 Pg',timeout=60)
            keys('ctrl-f10'); q.wait_for('Define macro:')
            q.type(r'C:\OUT\TYPED'); q.wait_for('TYPED'); keys('ret');snap('exists')
            keys('f1','ctrl-f10')
            q.wait_for('Define macro:')
            q.type(r'C:\OUT\EMPTY'); q.wait_for('EMPTY'); keys('ret'); q.wait_for('Description:')
            keys('ret'); q.type('Q'); time.sleep(.5); keys('ctrl-f10'); snap('empty-description')
            keys('f7','n','y');q.wait_absent('Exit WP?')
        guest.stop()
        run(['mcopy','-i',disk,'::OUT/EMPTY.WPM',str(out/'EMPTY.WPM')],check=True)
    finally: guest.stop()
