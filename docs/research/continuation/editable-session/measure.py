#!/usr/bin/env python3
"""Host cumulative View allocation observation, not a peak-memory/product SLO."""
from pathlib import Path
import json,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
source=(ROOT/'internal/tui/original_editable_test.go').read_text().replace('"testing"','"testing"\n"runtime"')
source+='''
func TestViewAllocationObservation(t *testing.T) {
 _,m,_,_:=testModel(t);m=retrieve(m);m=key(t,m,'x',0,strings.Repeat("x",4090))
 for _,reveal:=range []bool{false,true}{
  if reveal {m=key(t,m,tea.KeyF3,tea.ModAlt,"")}
  var b,a runtime.MemStats;runtime.ReadMemStats(&b)
  allocs:=testing.AllocsPerRun(100,func(){_ =m.View()});runtime.ReadMemStats(&a)
  t.Logf("tokens=%d reveal=%t view_bytes=%d allocs_per_call=%g cumulative_TotalAlloc_delta=%d (101calls+measurementoverhead; not peak/RSS or hard cap)",m.Session().Document().TokenCount(),reveal,len(m.View().Content),allocs,a.TotalAlloc-b.TotalAlloc)
 }
}
'''
archive=HERE/'view-measure_test.go.txt';archive.write_text(source)
with tempfile.TemporaryDirectory(prefix='wp28-view-measure-') as temp:
 overlay=Path(temp)/'overlay.json';overlay.write_text(json.dumps({'Replace':{str(ROOT/'internal/tui/original_editable_test.go'):str(archive)}}))
 p=subprocess.run(['go','test','-overlay',str(overlay),'./internal/tui','-run','^TestViewAllocationObservation$','-count=1','-v'],cwd=ROOT,capture_output=True)
 (HERE/'view-measure.txt').write_bytes(p.stdout+p.stderr);raise SystemExit(p.returncode)
