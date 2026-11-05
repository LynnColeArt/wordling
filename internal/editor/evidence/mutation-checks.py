#!/usr/bin/env python3
"""Scoped compiling mutations through Go overlays; production bytes never change."""
import json
from pathlib import Path
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[3]
source=ROOT/'internal/editor/session.go'
text=source.read_text()
mutants=[('accept-old-operation','result.Operation != s.pending.Operation','false'),('retain-on-Escape-exit','case No, Escape:\n\t\t\treturn s.clear(), nil, nil','case No, Escape:\n\t\t\ts.mode=Editing;return s,nil,nil'),('lose-uncertainty','s.lastSave = SaveUncertain','s.lastSave = SaveFailed'),('ignore-save-error','if result.Err != nil {','if false {')]
for name,old,new in mutants:
 assert text.count(old)==1,(name,text.count(old))
 with tempfile.TemporaryDirectory() as folder:
  root=Path(folder);mutated=root/'session.go';mutated.write_text(text.replace(old,new))
  overlay=root/'overlay.json';overlay.write_text(json.dumps({'Replace':{str(source):str(mutated)}}))
  result=subprocess.run(['go','test','-overlay',str(overlay),'./internal/editor','-count=1'],cwd=ROOT,capture_output=True,text=True)
  print(name+': exit'+str(result.returncode));print(result.stdout+result.stderr)
  assert result.returncode!=0,name
assert source.read_text()==text
print('Four scoped compiling safety mutants rejected; production source unchanged.')
