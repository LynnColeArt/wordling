#!/usr/bin/env python3
"""Exercise the actual executable using labelled synthetic Linux PTY input.

Usage: pty_test.py BINARY NEW_OUTPUT_DIR. No physical-delivery qualification.
"""
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path
import pty
import select
import signal
import struct
import subprocess
import sys
import termios
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
FIXTURE = ROOT/'docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5'

def digest(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def execute(binary, output, name, interrupt=False):
    folder = output/name
    folder.mkdir()
    work = folder/'files'
    work.mkdir()
    native = FIXTURE.read_bytes()
    assert digest(native) == {'bytes':334,'sha256':'c6cffde251e03b1f884c8e209afb426fced87d8c633ee4d1e3e4eb7e7c34aa3d'}
    (work/'ORIGIN').write_bytes(native)
    (work/'OTHER').write_bytes(native)
    master, slave = pty.openpty()
    fcntl.ioctl(slave,termios.TIOCSWINSZ,struct.pack('HHHH',25,100,0,0))
    before = termios.tcgetattr(slave)
    argv = [str(binary),'-root',str(work.resolve()),'-profile','local-flat']
    env = dict(os.environ,TERM='xterm-256color',LANG='C.UTF-8')
    proc = subprocess.Popen(argv,stdin=slave,stdout=slave,stderr=subprocess.PIPE,env=env)
    wire = bytearray()
    sent = []
    checks = []
    def collect(seconds=.15):
        deadline = time.monotonic()+seconds
        while time.monotonic()<deadline:
            if select.select([master],[],[],.01)[0]:
                try:
                    b = os.read(master,65536)
                    if not b: break
                    wire.extend(b)
                except OSError as exc:
                    if exc.errno!=errno.EIO: raise
                    break
    def send(raw,label):
        os.write(master,raw)
        sent.append({'label':label,'hex':raw.hex()})
        collect()
    try:
        collect(.5)
        assert b'Wordling 5.2' in wire, wire
        send(b'\x1b[?31u','synthetic enhancement response, not terminal capability proof')
        send(b'\x1b[21;2~','Shift+F10 retrieve')
        send(b'ORIGIN','flat original name')
        send(b'\r','retrieve Enter')
        assert b'ORIGIN' in wire
        if interrupt:
            proc.send_signal(signal.SIGTERM)
        else:
            send(b'\x1b[13;3~','Alt+F3 Reveal')
            send(b'\x1b[C','Right ASCII')
            send(b'\x1b[C','Right Bold code')
            send(b'\x1b[13;3~','Alt+F3 normal')
            send(b'\x1b[999;8~','unknown CSI')
            send(b'\x1b[200~\x1b[18~ny\x1b[201~','paste does not execute exit')
            send(b'\x1b[18;1:3~','F7 release does not execute exit')
            send(b'q\x11\x13','q CtrlQ CtrlS unsupported')
            fcntl.ioctl(slave,termios.TIOCSWINSZ,struct.pack('HHHH',30,110,0,0))
            proc.send_signal(signal.SIGWINCH)
            collect()
            send(b'\x1b[21~','F10 prefilled save')
            send(b'\r','observe same original')
            send(b'y','explicit same-file no-op')
            send(b'\x1b[21~','F10 alternate name')
            send(b'OTHER','existing separate inode')
            send(b'\r','replacement question')
            send(b'y','actual replacement refused')
            send(b'n','decline replacement returns retained filename')
            send(b'COPY','first character restarts filename')
            send(b'\r','actual no-edit new-name publication')
            assert (work/'COPY').read_bytes()==native
            send(b'\x1b[18~','F7 save question')
            send(b'\x1bOP','F1 retain document')
            send(b'\x1b[18~','F7 save question again')
            send(b'n','No advances exit question')
            send(b'\x1bOP','F1 retain at exit question')
            send(b'\x1b[18~','F7 final save question')
            send(b'n','No at save')
            send(b'y','Yes exit original bounded workflow')
        proc.wait(timeout=5)
        collect(.1)
        stderr = proc.stderr.read()
        assert proc.returncode == (1 if interrupt else 0), stderr
        if interrupt: assert b'host interruption' in stderr
        assert termios.tcgetattr(slave)==before,'actual termios restoration failed'
        assert (work/'ORIGIN').read_bytes()==native
        assert (work/'OTHER').read_bytes()==native
        assert not list(work.glob('.wordling-candidate-*'))
        for label,cue in [('retrieve',b'Document to be retrieved:'),('qualification',b'UNQUALIFIED')]:
            assert cue in wire,(label,cue)
            checks.append(label)
        if not interrupt:
            for cue in (b'Document to be saved:',b'Replace ',b'Save document?',b'Exit WP?',b'[BOLD]',b'[bold]'):
                assert cue in wire,cue
            checks+=['same-file-no-op','refused-replacement','new-name-bytes','F1-retains','original-exit']
        (folder/'wire-output.bin').write_bytes(wire)
        (folder/'stderr.txt').write_bytes(stderr)
        (folder/'injected.json').write_text(json.dumps(sent,indent=2)+'\n')
        report = {'scope':'synthetic-pty-only','physical_qualified':False,'returncode':proc.returncode,'termios_restored':True,'argv':argv,'checks':checks,'before':digest(native),'after':{p.name:digest(p.read_bytes()) for p in sorted(work.iterdir())},'binary':digest(binary.read_bytes()),'TERM':env['TERM'],'LANG':env['LANG']}
        (folder/'result.json').write_text(json.dumps(report,indent=2)+'\n')
    except Exception as exc:
        (folder/'failure.txt').write_text(repr(exc)+'\n')
        (folder/'wire-output.bin').write_bytes(wire)
        (folder/'injected.json').write_text(json.dumps(sent,indent=2)+'\n')
        raise
    finally:
        if proc.poll() is None:
            proc.kill();proc.wait()
        proc.stderr.close();os.close(master);os.close(slave)

if __name__=='__main__':
    binary=Path(sys.argv[1]).resolve();output=Path(sys.argv[2]).resolve();output.mkdir()
    execute(binary,output,'workflow')
    execute(binary,output,'host-signal',True)
    refused=subprocess.run([str(binary),'-root',str(output),'-profile','local-flat'],input=b'',capture_output=True)
    assert refused.returncode!=0 and b'requires terminal' in refused.stderr
    (output/'non-tty-stderr.txt').write_bytes(refused.stderr)
    files={str(p.relative_to(output)):digest(p.read_bytes()) for p in sorted(output.rglob('*')) if p.is_file()}
    (output/'manifest.json').write_text(json.dumps({'scope':'synthetic-pty-only','physical_qualified':False,'files':files},indent=2)+'\n')
    print('Actual wordling PTY workflow, refused replacement, bytes, signal/restoration and non-TTY refusal PASS; physical unqualified')
