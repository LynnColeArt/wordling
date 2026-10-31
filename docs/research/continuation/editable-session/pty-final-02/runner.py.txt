#!/usr/bin/env python3
"""Actual wordling, synthetic Linux PTY only. No original VM/physical claim.
Usage: pty_test.py BINARY NEW_OUTPUT_DIRECTORY
"""
import errno,fcntl,hashlib,json,os,pty,select,signal,struct,subprocess,sys,termios,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
FIXTURE=ROOT/'docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5'
def digest(b):return {'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def body(b):
    # Independent test observation only; product TUI never decodes native data.
    at=int.from_bytes(b[4:8],'little');assert 16<=at<=len(b);return b[at:]
def execute(binary,output,kind):
    folder=output/kind;folder.mkdir();work=folder/'files';work.mkdir()
    native=FIXTURE.read_bytes();assert digest(native)=={'size':334,'sha256':'c6cffde251e03b1f884c8e209afb426fced87d8c633ee4d1e3e4eb7e7c34aa3d'}
    (work/'ORIGIN').write_bytes(native);(work/'OTHER').write_bytes(native)
    master,slave=pty.openpty();fcntl.ioctl(slave,termios.TIOCSWINSZ,struct.pack('HHHH',28,140,0,0));before=termios.tcgetattr(slave)
    argv=[str(binary),'-root',str(work.resolve()),'-profile','local-flat'];env=dict(os.environ,TERM='xterm-256color',LANG='C.UTF-8')
    stderr=b''
    proc=subprocess.Popen(argv,stdin=slave,stdout=slave,stderr=subprocess.PIPE,env=env);wire=bytearray();sent=[];expected=None
    def collect(seconds=.12):
        deadline=time.monotonic()+seconds
        while time.monotonic()<deadline:
            if select.select([master],[],[],.01)[0]:
                try:
                    b=os.read(master,65536)
                    if not b:break
                    wire.extend(b)
                except OSError as e:
                    if e.errno!=errno.EIO:raise
                    break
    def send(raw,label):
        os.write(master,raw);sent.append({'label':label,'hex':raw.hex()});collect()
    def cue(c):assert c.encode() in wire,c
    try:
        collect(.5);cue('bounded native editing');send(b'\x1b[?31u','synthetic enhancement response, no physical qualification')
        send(b'\x1b[21;2~','ShiftF10 retrieve');send(b'ORIGIN','flat basename');send(b'\r','retrieve Enter')
        if kind=='host-signal':proc.send_signal(signal.SIGTERM)
        else:
            if kind=='ascii':
                send(b'q','literal q insertion, not quit alias');send(b'\x1b[2~','Insert typeover');send(b'Q','typeover A');send(b'\x1b[2~','Insert restore insertion')
                expected=bytes.fromhex('7151c30cc34243c40cc444')
                send(b'\x1b[13;3~','AltF3 Reveal same semantic gap');send(b'\x1b[13;3~','AltF3 normal')
                send(b'\x11\x13','CtrlQ CtrlS unsupported');send(b'\x1b[200~NEVER\x1b[201~','paste unsupported');send(b'\x1b[18;1:3~','release not exit');send(b'\x1b[999;8~','unknown CSI')
                fcntl.ioctl(slave,termios.TIOCSWINSZ,struct.pack('HHHH',30,130,0,0));proc.send_signal(signal.SIGWINCH);collect()
            elif kind in ('block-restore','repair-restore'):
                send(b'\x1b[13;3~','Reveal');send(b'\x1b[C','Right gap1');send(b'\x1b[14;3~','AltF4 block')
                steps=4 if kind=='block-restore' else 1
                for _ in range(steps):send(b'\x1b[C','Right extends selection')
                send(b'\x7f','original selected Backspace');cue('Delete Block? No (Yes)')
                send(b'n','No retains block');send(b'\x1bOP','separate F1 block cleanup')
                # Return to g1 through real Reveal navigation, then select again.
                for _ in range(steps):send(b'\x1b[D','Left returns to opening boundary')
                send(b'\x1b[14;3~','AltF4 block again')
                for _ in range(steps):send(b'\x1b[C','Right selection')
                send(b'\x7f','selected Backspace again');send(b'y','Yes confirmed block')
                send(b'\x1bOP','F1 Undelete preview');cue('[Block]');send(b'\x1bOP','F1 preview cancel');send(b'\x1bOP','reopen preview');send(b'1','numeric1 Restore')
                if kind=='block-restore':expected=body(native)
                else:
                    # The approved23 trace browses retained repair entry BEFORE X.
                    send(b'\x1bOP','postRestore preview');send(b'2','Previous retained entry');send(b'\x1bOP','cancel before marker');send(b'X','marker at actual restored gap')
                    expected=bytes.fromhex('41c30cc3c40cc4c30cc3584243c40cc444')
            elif kind=='normal-question':
                send(b'\x1b[C','normal Right before On');send(b'\x1b[3~','Delete asks paired-code question');cue('Delete [BOLD]? No (Yes)');send(b'n','No advances forward gap')
                send(b'\x7f','Backspace targets code at new gap');send(b'\x1bOP','F1 decline backward gap');send(b'\x1b','Esc in Editing remains unsupported')
                expected=body(native)
            send(b'\x1b[21~','F10 edited/noedit Save As');send(b'OTHER','existing different inode');send(b'\r','Observe existing target');cue('Replace ');send(b'y','replacement explicitly refused');send(b'n','return filename');send(b'COPY','first-character filename restart');send(b'\r','fresh publication')
            deadline=time.monotonic()+3
            while not (work/'COPY').exists() and time.monotonic()<deadline:collect(.1)
            actual=(work/'COPY').read_bytes();assert body(actual)==expected,(body(actual).hex(),expected.hex())
            if kind=='normal-question':assert actual==native
            if kind=='block-restore':assert actual==(ROOT/'docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/RESTORED.WP5').read_bytes()
            if kind=='repair-restore':assert actual==(ROOT/'docs/research/continuation/native-edits/runs/wp23-b-history-follow-repair-restore-r1/N0001.WP5').read_bytes()
            send(b'\x1b[18~','F7 save question');send(b'\x1bOP','F1 returns');send(b'\x1b[18~','F7 again');send(b'n','No save');send(b'\x1bOP','F1 retains at exit question');send(b'\x1b[18~','F7 final');send(b'n','No save');send(b'y','Yes original exit')
        proc.wait(timeout=5);collect(.1);stderr=proc.stderr.read();assert proc.returncode==(1 if kind=='host-signal' else 0),stderr
        assert termios.tcgetattr(slave)==before,'termios not restored'
        assert (work/'ORIGIN').read_bytes()==native and (work/'OTHER').read_bytes()==native
        assert not list(work.glob('.wordling-candidate-*'))
        cue('UNQUALIFIED')
        report={'scope':'synthetic-linux-pty-only','physical_qualified':False,'argv':argv,'binary':digest(binary.read_bytes()),'fixture':digest(native),'returncode':proc.returncode,'termios_restored':True,'expected_body_hex':None if expected is None else expected.hex(),'files':{p.name:digest(p.read_bytes()) for p in sorted(work.iterdir())},'TERM':env['TERM'],'LANG':env['LANG']}
        (folder/'result.json').write_text(json.dumps(report,indent=2)+'\n')
    except Exception as e:
        (folder/'failure.txt').write_text(repr(e)+'\n');raise
    finally:
        (folder/'wire-output.bin').write_bytes(wire);(folder/'injected.json').write_text(json.dumps(sent,indent=2)+'\n')
        if proc.poll() is None:proc.kill();proc.wait()
        (folder/'stderr.txt').write_bytes(stderr if stderr else (proc.stderr.read() if proc.stderr else b''));proc.stderr.close();os.close(master);os.close(slave)
if __name__=='__main__':
    binary=Path(sys.argv[1]).resolve();output=Path(sys.argv[2]).resolve();output.mkdir()
    # Archive executing helper and actual source/module bytes BEFORE child launch.
    (output/'runner.py.txt').write_bytes(Path(__file__).read_bytes())
    inputs={str(p.relative_to(ROOT)):digest(p.read_bytes()) for p in sorted(ROOT.glob('internal/**/*.go'))}
    for p in sorted((ROOT/'cmd/wordling').glob('*.go')):inputs[str(p.relative_to(ROOT))]=digest(p.read_bytes())
    for name in ['go.mod','go.sum']:inputs[name]=digest((ROOT/name).read_bytes())
    (output/'inputs.json').write_text(json.dumps({'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'working_source_inputs':inputs,'binary':digest(binary.read_bytes()),'fixture':digest(FIXTURE.read_bytes())},indent=2)+'\n')
    for kind in ['ascii','block-restore','repair-restore','normal-question','host-signal']:execute(binary,output,kind)
    p=subprocess.run([str(binary),'-root',str(output),'-profile','local-flat'],input=b'',capture_output=True);assert p.returncode==1 and b'requires terminal' in p.stderr;(output/'non-tty-stderr.txt').write_bytes(p.stderr)
    (output/'manifest.json').write_text(json.dumps({str(p.relative_to(output)):digest(p.read_bytes()) for p in sorted(output.rglob('*')) if p.is_file()},indent=2)+'\n')
    print('Five actual command PTYs/termios/source/native assertions pass; physical delivery unqualified')
