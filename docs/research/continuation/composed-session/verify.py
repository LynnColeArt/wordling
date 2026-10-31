#!/usr/bin/env python3
"""Check sealed source, original bindings and synthetic raw captures offline."""
import hashlib
import json
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]

def fingerprint(data):
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def verify():
    sealed=json.loads((HERE/'source-manifest.json').read_text())
    assert not sealed['physical_qualified'] and not sealed['full_parity_verified']
    for name,expected in sealed['files'].items():
        assert fingerprint((ROOT/name).read_bytes())==expected,name
    for directory,commit in sealed['dependency_commits'].items():
        subprocess.run(['git','diff','--exit-code',commit,'HEAD','--',directory],cwd=ROOT,check=True,capture_output=True)
    for run in ['run-01','run-02','run-03-final','run-04-final']:
        folder=HERE/run
        manifest=json.loads((folder/'manifest.json').read_text())
        assert manifest['scope']=='synthetic-pty-only' and not manifest['physical_qualified']
        for name,expected in manifest['files'].items():
            assert fingerprint((folder/name).read_bytes())==expected,(run,name)
        for scenario in ['workflow','host-signal']:
            result=json.loads((folder/scenario/'result.json').read_text())
            assert result['scope']=='synthetic-pty-only' and not result['physical_qualified']
            assert result['termios_restored']
            assert result['returncode']==(0 if scenario=='workflow' else 1)
            assert result['before']==result['after']['ORIGIN']==result['after']['OTHER']
            if scenario=='workflow':assert result['before']==result['after']['COPY']
            if run.endswith('final'):assert result['binary']==sealed['final_binary']
    subprocess.run(['python3','internal/editor/evidence/audit.py'],cwd=ROOT,check=True)
    assert len(json.loads((HERE/'mutation-results.json').read_text())['results'])==4
    print('Owned/dependency sources, four raw synthetic PTY runs, exact native length/SHA and original state associations PASS; physical/full parity remain unqualified')

if __name__=='__main__':verify()
