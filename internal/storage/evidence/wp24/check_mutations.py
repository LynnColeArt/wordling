"""Run three bounded assertion-quality probes, restoring every source in finally.

Run from the lane root. These are deliberate source faults, not production code.
An invalid/noncompiling probe is not counted as an assertion kill.
"""
from pathlib import Path
import hashlib
import subprocess

ROOT = Path(__file__).resolve().parents[4]
NATIVE = ROOT / 'internal/storage/storage_linux.go'
PUBLICATION = ROOT / 'internal/storage/publication_linux.go'
sha = lambda b: hashlib.sha256(b).hexdigest()
probes = [
    ('payload-uses-source-hash', NATIVE,
     'checked.identity.SHA256 != payloadHash',
     'checked.identity.SHA256 != doc.identity.SHA256',
     'TestEditedPublicationOwnsPayloadAndPreservesSource'),
    ('late-source-guard-removed', NATIVE,
     'if err = checkSource(doc); err != nil {',
     'if err = nil; err != nil {',
     'TestEditedPublicationFailureBoundaries/source_(mutation|replacement)'),
    ('expected-operation-revision-ignored', PUBLICATION,
     ' || expectedID != p.id', '',
     'TestPublicationRejectsUnboundAndUnsupportedRequests'),
]
for name, path, old, new, test in probes:
    original = path.read_bytes()
    text = original.decode()
    assert text.count(old) == 1, (name, 'source anchor drift')
    try:
        path.write_text(text.replace(old, new))
        result = subprocess.run(['go', 'test', './internal/storage', '-count=1', '-run', test], cwd=ROOT, capture_output=True, text=True)
        output = result.stdout + result.stderr
        assert result.returncode != 0 and '--- FAIL:' in output and '[build failed]' not in output, (name, result.returncode, output)
        print(name, 'assertion-killed; exit', result.returncode)
        print(output.rstrip())
    finally:
        path.write_bytes(original)
    assert sha(path.read_bytes()) == sha(original), name
    print('source restored byte-exactly', sha(original))
print('three compiling mutations killed by contract assertions; sources restored')
