#!/usr/bin/env python3
"""Require the duplicate-dispatch regression to kill the reviewed defect."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
ROOT=Path(__file__).resolve().parents[5]
target=ROOT/'internal/tui/runtime.go'
source=target.read_text()
needle='return duplicateDispatchMsg{}'
assert source.count(needle)==1
with tempfile.TemporaryDirectory(prefix='wp18-i1-mutant-') as tmp:
    tmp=Path(tmp)
    mutant=tmp/'runtime.go'
    mutant.write_text(source.replace(needle,'result.Err = errors.New("duplicate dispatch mutant"); return resultMsg{result}'))
    overlay=tmp/'overlay.json';overlay.write_text(json.dumps({'Replace':{str(target):str(mutant)}}))
    p=subprocess.run(['go','test','-overlay='+str(overlay),'./internal/tui','-run','^TestDuplicateSaveBeforeAuthenticAtEveryGuard$','-count=1','-v'],cwd=ROOT,text=True,capture_output=True)
    assert p.returncode!=0 and '--- FAIL:' in p.stdout and 'build failed' not in p.stdout+p.stderr,(p.stdout,p.stderr)
    print(json.dumps({'scope':'compiling duplicate-completion regression mutant killed; source unchanged','source_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr},indent=2))
