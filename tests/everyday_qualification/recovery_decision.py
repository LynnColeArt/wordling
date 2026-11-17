#!/usr/bin/env python3
"""Fixture-free PTY regression for cancel/restore/re-crash/explicit-discard.

No GNOME session, tracing, or injected storage error is involved. SIGKILL is
sent only to the exact normal executable child owned by this test.
"""
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

from qualification import Run, SWITCH


def main():
    repo, binary, output = (Path(arg).resolve() for arg in sys.argv[1:])
    output.mkdir(parents=True)
    workspace = output / 'workspace'
    workspace.mkdir()
    cache = output / 'cache'
    current = None
    events = []

    def launch(name, cue):
        nonlocal current
        current = Run(repo, binary, output / name)
        current.p.env['XDG_CACHE_HOME'] = str(cache)
        current.p.argv[current.p.argv.index('-root') + 1] = str(workspace)
        current.p.proc = subprocess.Popen(
            current.p.argv, cwd=repo, stdin=current.p.slave, stdout=current.p.slave,
            stderr=subprocess.PIPE, env=current.p.env)
        current.wait(cue)
        return current

    def bodies():
        result = []
        for path in cache.rglob('documents.json'):
            for record in json.loads(path.read_bytes())['Records']:
                raw = base64.b64decode(record['Native'])
                assert raw[:4] == b'\xffWPC'
                result.append(raw[int.from_bytes(raw[4:8], 'little'):].decode('ascii'))
        return sorted(result)

    def crash(run, label):
        pid = run.p.proc.pid
        run.p.proc.kill()
        assert run.p.proc.wait(timeout=5) == -9
        run.p.close()
        events.append({'label': label, 'pid': pid, 'returncode': -9})

    def clean_exit(run):
        run.step(b'\x1b=', 'focus menu')
        run.step('f', 'File menu', 'Quit Wordling')
        run.step('q', 'Quit Wordling')
        # Two restored documents must still be unsaved. Each requires an
        # explicit discard choice; silently treating them clean would fail.
        for screen in (2, 1):
            run.wait(f'Save document {screen} before quitting?')
            run.step('n', f'explicitly discard restored screen {screen}')
        assert run.p.proc.wait(timeout=5) == 0
        run.finish(None, 'explicit discard of both restored unsaved buffers')

    try:
        run = launch('seed', 'Doc 1 Pg')
        run.step('FIRST', 'type first independent buffer', 'FIRST')
        run.step(SWITCH, 'second document', 'Doc 2 Pg')
        run.step('SECOND', 'type second independent buffer', 'SECOND')
        run.until(lambda: bodies() == ['FIRST', 'SECOND'], 'both recovery copies durable', timeout=10)
        crash(run, 'initial interrupted session')

        run = launch('cancel-warning', 'Recover documents')
        assert sum('[x]' in row for row in run.rows()) == 2
        before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in cache.rglob('documents.json')}
        run.step(' ', 'uncheck one recovery copy')
        run.step(b'\r', 'review deletion', 'Permanently delete 1 unchecked copies?')
        run.step('n', 'cancel deletion warning', 'Review deletion of unchecked copies')
        assert sum('[x]' in row for row in run.rows()) == 1
        for name, digest in before.items():
            assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest
        assert bodies() == ['FIRST', 'SECOND']
        run.step('a', 'select all after cancellation')
        start = time.monotonic()
        run.step(b'\r', 'restore both without second decision', 'Doc 1 Pg')
        assert 'Recover documents' not in '\n'.join(run.rows())
        assert bodies() == ['FIRST', 'SECOND'], 'restored copies must remain protected'
        crash(run, 'immediate second crash without edit/save')
        assert time.monotonic() - start < 5, 'must precede first timed autosave'
        assert not list(workspace.iterdir()), 'restoring must not publish a native document'

        run = launch('second-recovery', 'Recover documents')
        assert sum('[x]' in row for row in run.rows()) == 2
        run.step(b'\r', 'restore both eligible copies again', 'Doc 1 Pg')
        restored = []
        for tab in (1, 2):
            x = run.rows()[1].index(f'Doc {tab}') + 1
            run.step(f'\x1b[<0;{x};2M'.encode(), f'inspect restored tab {tab}', f'Doc {tab} Pg')
            restored.append(run.rows()[2].strip())
        assert sorted(restored) == ['FIRST', 'SECOND']
        clean_exit(run)

        run = launch('normal-restart', 'Doc 1 Pg')
        assert 'Recover documents' not in '\n'.join(run.rows())
        assert bodies() == [], 'explicit discard must consume protected copies'
        run.exit_application()
        run.finish(None, 'normal restart does not repeat resolved recovery prompt')
        (output / 'result.json').write_text(json.dumps({
            'result': 'pass', 'transport': 'PTY, not GNOME', 'events': events,
            'source_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip(),
            'binary_sha256': hashlib.sha256(binary.read_bytes()).hexdigest(),
            'no_native_document_published': not list(workspace.iterdir()),
        }, indent=2) + '\n')
    finally:
        if current is not None and current.p.proc is not None and current.p.proc.poll() is None:
            current.p.proc.kill()
            current.p.proc.wait(timeout=5)
            current.p.close()


if __name__ == '__main__':
    main()
