#!/usr/bin/env python3
"""Compile Go-overlay mutants; production source remains untouched."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
ROOT=Path(__file__).resolve().parents[4]
CASES=[
 ('modifier-identity','model.go','k.Code == tea.KeyF10 && k.Mod == tea.ModShift','k.Code == tea.KeyF10 && k.Mod == 0','TestActualRetrieveAndSave'),
 ('late-publish-reconciliation','model.go','if !attached && result.Err == nil','if attached && result.Err == nil','TestLatePublicationRequiresReconciliation'),
 ('uncertain-residue','runtime.go','f.DestinationMayExist || f.Candidate != ""','false','TestFailedUncertainResultKeepsNativeAndNeverExits'),
 ('actual-storage-consumer','runtime.go','request.Directory.Save(request.Document, request.Destination, request.Decision)','storage.Outcome{}, errors.New("mutant refuses actual IO")','TestActualRetrieveAndSave'),
]
if __name__=='__main__':
 results=[]
 with tempfile.TemporaryDirectory(prefix='wp18-mutants-') as tmp:
  tmp=Path(tmp)
  for name,filename,old,new,test in CASES:
   target=ROOT/'internal/tui'/filename
   source=target.read_text();assert source.count(old)==1,(filename,old)
   mutant=tmp/filename;mutant.write_text(source.replace(old,new))
   overlay=tmp/'overlay.json';overlay.write_text(json.dumps({'Replace':{str(target):str(mutant)}}))
   p=subprocess.run(['go','test','-overlay='+str(overlay),'./internal/tui','-run','^'+test+'$','-count=1'],cwd=ROOT,text=True,capture_output=True)
   assert p.returncode!=0 and '--- FAIL:' in p.stdout and 'build failed' not in p.stdout+p.stderr,(name,p.stdout,p.stderr)
   results.append({'mutant':name,'production_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'test':test,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
 print(json.dumps({'scope':'four compiling overlay mutants killed by actual assertions; no production mutation','results':results},indent=2))
