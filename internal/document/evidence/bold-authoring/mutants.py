"""One finite WP74 semantic campaign in an exact Git-derived component closure."""
import base64
import difflib
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import time

ROOT = Path(__file__).resolve().parents[4]
EVIDENCE = Path(__file__).resolve().parent
FILE = 'internal/document/bold_authoring.go'
ENV = dict(os.environ, GOTOOLCHAIN='local', GOPROXY='off', PYTHONDONTWRITEBYTECODE='1')
SOURCE = 'c254b4f5'
MAX_SECONDS = 180

MUTANTS = (
    ('omit-off', 'body = append(body, nativeBoldOff...)', '',
     'TestBoldNativePair', 'begin paired native Bold'),
    ('cursor-after-off', 'd.publishBody(c, body, count+2, count+1, false)',
     'd.publishBody(c, body, count+2, count+2, false)',
     'TestBoldBeginCursor', 'cursor is not immediately before Off'),
    ('rebind-stale-span', '''if !s.matches(d.state) {
		return unchanged, failure(InvalidBoldSpan, c.gap, noSpan)
	}''', '''if s == nil || s.phase != boldActive {
		return unchanged, failure(InvalidBoldSpan, c.gap, noSpan)
	}
	if s.owner != d.state {
		stale := *s
		stale.owner = d.state
		stale.off = c.gap
		stale.inserted = stale.off - stale.on - 1
		s = &stale
	}''', 'TestBoldStaleSpan', 'stale active span closed current revision'),
    ('allow-empty-close', 'if s.inserted == 0 {', 'if s.inserted < 0 {',
     'TestBoldCloseRequiresText', 'empty Bold span should refuse'),
    ('accept-foreign-result', ' || h.state.document != a.before {', ' {',
     'TestBoldAuthenticHistory', 'unowned/replayed Bold result advanced history'),
    ('qualify-history', 'next.effectUnqualified = true', 'next.effectUnqualified = false',
     'TestBoldNativePair', 'Bold incorrectly qualified or changed stored history'),
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def snapshot(root):
    files = []
    for p in sorted(root.rglob('*')):
        if p.is_file():
            b = p.read_bytes()
            files.append(dict(path=str(p.relative_to(root)), mode=oct(p.stat().st_mode),
                              bytes=len(b), sha256=sha(b)))
    return files


def execute():
    started = time.monotonic()
    records = []
    results = []
    summary = {'source': SOURCE, 'commands': records, 'mutants': results, 'limit_seconds': MAX_SECONDS}
    active = None

    def run(args, cwd, env=ENV):
        then = time.monotonic()
        remaining = MAX_SECONDS - (then - started)
        assert remaining > 0, 'campaign time exhausted'
        try:
            p = subprocess.run(args, cwd=cwd, env=env, capture_output=True, timeout=remaining)
        except subprocess.TimeoutExpired as err:
            records.append(dict(argv=args, cwd=str(cwd), timeout=remaining,
                                stdout_hex=(err.stdout or b'').hex(), stderr_hex=(err.stderr or b'').hex()))
            raise
        records.append(dict(argv=args, cwd=str(cwd), exit=p.returncode,
                            elapsed=time.monotonic()-then, stdout_hex=p.stdout.hex(), stderr_hex=p.stderr.hex()))
        return p

    try:
        revision = run(['git','rev-parse',SOURCE], ROOT)
        assert revision.returncode == 0
        summary['source'] = revision.stdout.decode().strip()
        listed = run(['git','ls-tree','-r','--name-only',summary['source'],'--',
                      'internal/document','internal/wp51','go.mod','go.sum'], ROOT)
        assert listed.returncode == 0
        paths = [p for p in listed.stdout.decode().splitlines()
                 if p in {'go.mod','go.sum'} or
                 (p.endswith('.go') and p.rsplit('/',1)[0] in {'internal/document','internal/wp51'})]
        # Archive by literal approved source paths. Focused targets create their
        # own native inputs and do not select the historical fixture suite.
        archive = run(['git','archive','--format=tar',summary['source'],'--',*paths], ROOT)
        assert archive.returncode == 0
        records[-1]['stdout_base64'] = base64.b64encode(archive.stdout).decode()
        del records[-1]['stdout_hex']
        with tempfile.TemporaryDirectory(prefix='wordling-wp74-mutant-') as scratch:
            active = Path(scratch)
            summary['scratch'] = str(active)
            with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as contents:
                contents.extractall(active,filter='data')
            frozen = snapshot(active)
            assert set(paths) == {x['path'] for x in frozen}
            summary['closure'] = frozen
            tooltmp = active/'tooltmp'
            tooltmp.mkdir()
            env = dict(ENV, GOTMPDIR=str(tooltmp))
            path = active/FILE
            old = path.read_text()
            for name, before, after, target, diagnostic in MUTANTS:
                assert old.count(before) == 1, name
                changed = old.replace(before,after)
                item = dict(name=name, target=target, diagnostic=diagnostic,
                            source_sha256=sha(changed.encode()),
                            diff=''.join(difflib.unified_diff(old.splitlines(True), changed.splitlines(True),
                                                           fromfile=FILE,tofile=FILE)))
                results.append(item)
                path.write_text(changed)
                try:
                    compile_check = run(['go','test','-run','^$','./internal/document'],active,env)
                    item['compile_exit'] = compile_check.returncode
                    assert compile_check.returncode == 0, name
                    target_check = run(['go','test','-v','-count=1','-run',f'^{target}$','./internal/document'],active,env)
                    item['target_exit'] = target_check.returncode
                    item['intended_failure'] = target_check.returncode == 1 and diagnostic.encode() in target_check.stdout
                    assert item['intended_failure'], name
                finally:
                    path.write_text(old)
            assert snapshot(active) == frozen
            summary['restored_exact_closure'] = True
        summary['scratch_removed'] = not active.exists()
        summary['campaign_seconds'] = time.monotonic()-started
        assert len(results) == 6 and summary['campaign_seconds'] <= MAX_SECONDS
        print(json.dumps({k:summary[k] for k in ['source','scratch_removed','campaign_seconds']}))
    finally:
        summary['elapsed'] = time.monotonic()-started
        packed = gzip.compress(json.dumps(summary, separators=(',',':')).encode(),mtime=0)
        used = sum(p.stat().st_size for p in EVIDENCE.iterdir() if p.is_file())
        assert used+len(packed) <= 3*1024*1024
        (EVIDENCE/'mutant-campaign.json.gz').write_bytes(packed)

if __name__ == '__main__':
    execute()
