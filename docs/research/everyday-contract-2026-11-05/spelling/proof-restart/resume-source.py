#!/usr/bin/env python3
import sys,json,hashlib,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'scripts/reference'))
import guest,qmp
private=ROOT/'research/cache/reference/everyday-spelling-proof'
out=Path(__file__).resolve().parent/'proof-restart'
out.mkdir(exist_ok=False)
runtime=Path('/tmp/wp51-spelling-proof-restart')
qmp.RUNTIME=guest.RUNTIME=runtime
qmp.SOCKET=guest.SOCKET=runtime/'qmp.sock'
runtime.mkdir(exist_ok=True)
# Restart only the stopped private disk, never alter the master.
assert not Path('/tmp/wp51-spelling-proof/qmp.sock').exists()
profile=json.loads(guest.PROFILE.read_text())
for path,expected in [(Path(profile['qemu_binary']['path']),profile['qemu_binary']['sha256'])]+[(Path(x['path']),x['sha256']) for x in profile['firmware']]:
 assert hashlib.sha256(path.read_bytes()).hexdigest()==expected
hashes={n:hashlib.sha256((private/n).read_bytes()).hexdigest() for n in ['harddisk.img','boot.img']}
command=guest.arguments(private/'boot.img',private/'harddisk.img')
(out/'start.json').write_text(json.dumps({'hashes':hashes,'command':command},indent=2)+'\n')
(out/'resume-source.py').write_bytes(Path(__file__).read_bytes())
trace=[]
try:
 subprocess.run(command,check=True)
 with qmp.QMP() as q:
  q.wait_for('Doc 1 Pg 1 Ln 1" Pos 1"',timeout=60)
  q.type('zorbly');trace.append('type zorbly')
  q.key('ctrl-f2');q.wait_for('Check:');trace.append('Ctrl-F2')
  q.key('3');q.wait_for('Word count:');trace.append('3 Document')
  print(q.capture(out/'01-default-sup-persisted'))
finally:
 guest.stop()
 (out/'trace.json').write_text(json.dumps(trace,indent=2)+'\n')
