#!/usr/bin/env python3
"""Verify sealed raw evidence matches the Git index or committed blobs byte for byte."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[4]
RAW = 'docs/research/continuation/session1/runs/'


def audit(revision):
    paths = subprocess.check_output(['git', 'ls-files', '-z', RAW], cwd=ROOT).decode().split('\0')
    paths = [p for p in paths if p]
    if not paths:
        raise ValueError('No staged raw evidence')
    specs = [((':' if revision == 'index' else revision + ':') + p) for p in paths]
    # Use a temporary input file and stream blobs; raster evidence is large.
    import tempfile
    source = tempfile.TemporaryFile()
    source.write(('\n'.join(specs)+'\n').encode()); source.seek(0)
    process = subprocess.Popen(['git', 'cat-file', '--batch'], stdin=source, stdout=subprocess.PIPE, cwd=ROOT)
    hashes = {}
    for path in paths:
        header = process.stdout.readline().split()
        if len(header) != 3 or header[1] != b'blob':
            raise ValueError((path, header))
        size = int(header[2])
        data = process.stdout.read(size)
        if process.stdout.read(1) != b'\n': raise ValueError('Missing blob separator')
        if data != (ROOT/path).read_bytes():
            raise ValueError('Git evidence bytes differ: '+path)
        hashes[path] = hashlib.sha256(data).hexdigest()
    if process.wait() != 0: raise ValueError('git cat-file failed')
    source.close()
    checked = 0
    def walk(value):
        nonlocal checked
        if isinstance(value, dict):
            if isinstance(value.get('path'), str) and value['path'].startswith(RAW) and 'sha256' in value:
                if hashes.get(value['path']) != value['sha256']:
                    raise ValueError('Manifest/Git hash mismatch: '+value['path'])
                checked += 1
            for item in value.values(): walk(item)
        elif isinstance(value, list):
            for item in value: walk(item)
    for manifest in sorted((ROOT/RAW).glob('*/run.json')):
        walk(json.loads(manifest.read_text()))
    return {'revision': revision, 'raw_blobs_equal_worktree': len(paths), 'manifest_hash_references_checked': checked}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision', default='HEAD', help='HEAD, commit, or index')
    print(json.dumps(audit(parser.parse_args().revision), indent=2))
