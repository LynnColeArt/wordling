#!/usr/bin/env python3
"""Verify the owned WP47 seal; --git additionally checks committed object bytes."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
manifest = json.loads((HERE / 'manifest.json').read_text())
for name, expected in manifest['files'].items():
    data = (ROOT / name).read_bytes()
    actual = {'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    assert actual == expected, (name, actual, expected)
    if '--git' in sys.argv:
        blob = subprocess.check_output(['git', 'show', 'HEAD:' + name], cwd=ROOT)
        assert blob == data, ('Git blob mismatch', name)
print(f"WP47: {len(manifest['files'])} exact files verified" + (' including committed Git blobs' if '--git' in sys.argv else ''))
