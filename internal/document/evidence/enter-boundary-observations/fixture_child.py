"""Fixed harmless PID/argv fixture. Cannot start reference programs or read disks."""
import os,signal,sys,time
from pathlib import Path
# Disk/socket arguments are markers for the approved identity checker only.
Path(sys.argv[1]).write_text(str(os.getpid()))
if sys.argv[-1]=='term-ignore':signal.signal(signal.SIGTERM,signal.SIG_IGN)
time.sleep(20)
