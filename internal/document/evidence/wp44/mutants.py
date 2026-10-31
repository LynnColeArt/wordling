"""Bounded source overlays, never edit installed product/reference sources."""
import json
from pathlib import Path
import subprocess
import tempfile
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
cases=[('new-cache-Cartesian','admission.go','f.offset == 21 && !reordered','f.offset == 21'),('ignore-unused-index','admission.go','if !bytes.Equal(raw[last.Data.Offset+20:last.Data.Offset+50], make([]byte, 30)) {','if false {'),('skip-field-validation','admission.go','if !allowed {','if false && !allowed {'),('fixed-flag-location','mutation.go','candidate[flags] |= 8','candidate[256] |= 8')]
rows=[]
with tempfile.TemporaryDirectory(prefix='wp44-source-mutants-')as temp:
 for name,file,needle,replacement in cases:
  original=ROOT/'internal/document'/file;raw=original.read_text();assert raw.count(needle)==1
  mutant=Path(temp)/(name+'.go');mutant.write_text(raw.replace(needle,replacement));overlay=Path(temp)/(name+'.json');overlay.write_text(json.dumps({'Replace':{str(original):str(mutant)}}))
  argv=['go','test','-overlay',str(overlay),'./internal/document','-run','TestReordered','-count=1'];r=subprocess.run(argv,cwd=ROOT,capture_output=True,timeout=60);log=HERE/(name+'.log');log.write_bytes(r.stdout+r.stderr)
  assert r.returncode!=0 and b'FAIL' in r.stdout and b'build failed'not in r.stdout,('survived or invalid mutant',name,r.stdout,r.stderr)
  rows.append({'name':name,'source':str(original.relative_to(ROOT)),'exact_edit':{'from':needle,'to':replacement},'argv':argv,'exit':r.returncode,'test_failure_not_build_error':True,'log':str(log.relative_to(ROOT))})
(HERE/'mutation-results.json').write_text(json.dumps({'mutants':rows,'all_detected':True,'actual_source_changes':False},indent=2)+'\n');print('4 meaningful source mutants detected by public reordered tests')
