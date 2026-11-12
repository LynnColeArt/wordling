#!/usr/bin/env python3
"""Bounded, offline original-app research; never touches product or master bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts/reference'))
import guest
import qmp

BASE = ROOT / 'docs/research/everyday-contract-2026-11-05/qualification'


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def configure(run):
    if not run or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in run):
        raise ValueError('Run must be a lowercase slug')
    out = BASE / run
    private = ROOT / 'research/cache/reference' / ('wp78-' + run)
    runtime = Path('/tmp/wp78-' + run)
    qmp.RUNTIME = guest.RUNTIME = runtime
    qmp.SOCKET = guest.SOCKET = runtime / 'qmp.sock'
    return out, private


def type_text(q, value):
    extra = {'!': 'shift-1', '*': 'shift-8', '?': 'shift-slash', "'": 'apostrophe', '(': 'shift-9', ')': 'shift-0', '%': 'shift-5'}
    for char in value:
        if char in extra:
            q.key(extra[char])
        else:
            q.type(char)


def capture(q, out):
    if out.exists():
        raise FileExistsError(out)
    time.sleep(1.5)
    screen = q.capture(out)
    # Keep raw BIOS cursor observations; WP may program its hardware cursor directly.
    # This is not silently promoted into a semantic-caret oracle.
    q.hmp(f'pmemsave 0x450 16 "{out / "bios-cursors.bin"}"')
    return screen


def perform(run, steps):
    out, private = configure(run)
    for step in steps:
        action = step[0]
        value = step[1] if len(step) > 1 else ''
        record = {'action': action, 'value': value, 'runner_sha256': digest(Path(__file__)), 'arguments': step[1:]}
        if out.exists():
            version = out / ('runner-' + record['runner_sha256'] + '.py')
            if not version.exists():
                version.write_bytes(Path(__file__).read_bytes())
        try:
            if action == 'start':
                out.mkdir(parents=True, exist_ok=False)
                (out / 'runner-source.py').write_bytes(Path(__file__).read_bytes())
                record['command'] = guest.start(private)
                (out / 'environment.json').write_bytes(guest.PROFILE.read_bytes())
                paths = ['scripts/reference/guest.py', 'scripts/reference/qmp.py', 'scripts/reference/document.py']
                (out / 'source.json').write_text(json.dumps({'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(), 'dependencies': [{'path': p, 'sha256': digest(ROOT / p)} for p in paths]}, indent=2) + '\n')
            elif action == 'stop':
                guest.stop()
            elif action == 'export':
                if qmp.SOCKET.exists():
                    raise RuntimeError('Refusing to export live image')
                image = str(private / 'harddisk.img') + '@@1048576'
                files = subprocess.run(['mdir', '-i', image, '::/OUT/'], capture_output=True, text=True, check=True).stdout
                (out / 'directory.txt').write_text(files)
                exports = out / 'exports'
                exports.mkdir(exist_ok=False)
                subprocess.run(['mcopy', '-s', '-i', image, '::/OUT/*', str(exports)], check=True)
                from document import prefix
                items = []
                for file in sorted(exports.rglob('*')):
                    if not file.is_file():
                        continue
                    raw = file.read_bytes()
                    item = {'path': str(file.relative_to(exports)), 'bytes': len(raw), 'sha256': digest(file)}
                    if raw.startswith(b'\xffWPC'):
                        offset = prefix(raw)['document_offset']
                        item.update(document_offset=offset, body_hex=raw[offset:].hex(), body_repr=repr(raw[offset:]))
                    items.append(item)
                (out / 'files.json').write_text(json.dumps(items, indent=2) + '\n')
            else:
                with qmp.QMP() as q:
                    if action == 'resume':
                        q.execute('cont')
                    elif action == 'key':
                        for key in value.split(','):
                            q.key(key)
                            time.sleep(.12)
                    elif action == 'type':
                        type_text(q, value)
                    elif action == 'wait':
                        q.wait_for(value)
                    elif action == 'absent':
                        q.wait_absent(value)
                    elif action == 'capture':
                        print(capture(q, out / value))
                    elif action == 'top':
                        for key in ['home', 'home', 'home', 'up']:
                            q.key(key)
                        q.wait_for('Pos 1"')
                    elif action == 'save':
                        q.key('f10')
                        q.wait_for('Document to be saved:')
                        if value:
                            type_text(q, value)
                        q.key('ret')
                        q.wait_absent('Document to be saved:')
                        if len(step) > 2:
                            q.wait_for('Replace ')
                            q.key(step[2])
                            q.wait_absent('Replace ')
                        time.sleep(.5)
                    elif action == 'dos':
                        q.key('ctrl-f1'); q.wait_for('DOS Command')
                        q.key('2'); q.wait_for('DOS Command:')
                        type_text(q, value); q.key('ret'); q.wait_for('Press any key')
                        label = 'dos-' + str(len(list(out.glob('dos-*'))) + 1).zfill(2)
                        print(capture(q, out / label)); record['capture'] = label
                        q.key('spc'); q.wait_absent('Press any key')
                    elif action == 'repeat-key':
                        for _ in range(int(step[2])):
                            q.key(value)
                    else:
                        raise ValueError(action)
            record['outcome'] = 'completed'
        except BaseException as error:
            record.update(outcome='failed', error=repr(error))
            if qmp.SOCKET.exists():
                try:
                    with qmp.QMP() as q:
                        label = 'failure-' + str(len(list(out.glob('failure-*'))) + 1).zfill(2)
                        capture(q, out / label); record['capture'] = label
                except BaseException as capture_error:
                    record['capture_error'] = repr(capture_error)
            raise
        finally:
            out.mkdir(parents=True, exist_ok=True)
            with (out / 'trace.jsonl').open('a') as stream:
                stream.write(json.dumps(record) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run')
    parser.add_argument('steps', help='JSON array of actions')
    args = parser.parse_args()
    perform(args.run, json.loads(args.steps))
