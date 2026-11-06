"""Harmless test-only Unix server; actual approved client/peer code is unchanged."""
import json,os,socket,sys,time
from pathlib import Path
pidfile,boot,harddisk,endpoint,wire=sys.argv[1:];path=Path(endpoint.removeprefix('unix:').removesuffix(','));server=socket.socket(socket.AF_UNIX);server.bind(str(path));server.listen();server.settimeout(1.8);Path(pidfile).write_text(str(os.getpid()));stop=False
try:
 while not stop:
  conn,_=server.accept();conn.settimeout(1);f=conn.makefile('rwb');f.write(b'{"QMP":{}}\n');f.flush()
  try:
   while line:=f.readline():
    with Path(wire).open('ab')as audit:audit.write(line)
    m=json.loads(line)
    if m['execute']=='quit':f.write(b'{"event":"SHUTDOWN","data":{"reason":"host-qmp-quit"}}\n');f.write(b'{"return":{}}\n');f.flush();stop=True;break
    f.write(b'{"return":{}}\n');f.flush()
  except (OSError,ValueError):pass
  finally:f.close();conn.close()
finally:server.close();path.unlink(missing_ok=True)
