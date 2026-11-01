#!/usr/bin/env python3
"""Compile-valid actual H mutants; raw reds retained, exact source restored."""
import hashlib,json,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent;source=ROOT/'internal/tui/reveal_inspection.go';model=ROOT/'internal/tui/model.go';original={p:p.read_bytes()for p in [source,model]}
cases=[
 ('Present-before-preflight',source,'catalogue, err := document.InspectRevealCatalogue','_ = m.legacyFrame()\n catalogue, err := document.InspectRevealCatalogue','TestInspectionBoundsPreflightBeforePresent'),
 ('wrong-preflight-window',source,'s.NativeRevision, 0, count)','s.NativeRevision, 0, count-count)','TestInspectionOriginal|TestInspectionBounds'),
 ('omit-source-binding',source,'s.NativeRevision, 0, count)','document.Revision{}, 0, count)','TestInspectionOriginal'),
 ('clear-upper-error',source,'frame.reveal = renderReveal','frame.err=nil\n frame.reveal = renderReveal','TestInspectionOriginal'),
 ('drop-unknown-marker',source,'text = "?" + strconv.Itoa(e.TokenIndex)','text = "" + strconv.Itoa(e.TokenIndex)','TestInspectionOriginal'),
 ('invent-active-fallback',source,'text, role := e.Text, revealBase','text, role := e.Text, revealActive','TestInspectionOriginal'),
 ('State-alias-frozen',source,'x.Elements = append([]document.Element(nil), x.Elements...)','// deliberately follows captured slice','TestInspectionIneligibleAndFrozenDiagnostics'),
 ('live-over-frozen',source,'if m.macroStatus.DisplaySuppressed && m.macroFrozen != nil {','if false && m.macroStatus.DisplaySuppressed && m.macroFrozen != nil {','TestInspectionIneligibleAndFrozenDiagnostics'),
 ('bypass-expanded-cap',source,'if n > MaxInspectionRenderBytes-size {','if false && n > MaxInspectionRenderBytes-size {','TestInspectionExpandedBoundsAndEOF'),
 ('window-end-as-EOF',source,'TrueEOF: catalogue.TrueEOF','TrueEOF: true','TestInspectionExpandedBoundsAndEOF')]
results=[]
try:
 for name,path,old,new,test in cases:
  text=original[path].decode();assert old in text,(name,old);path.write_text(text.replace(old,new,1));start=time.monotonic();p=subprocess.run(['go','test','./internal/tui','-run',test,'-count=1'],cwd=ROOT,capture_output=True,timeout=60);(HERE/(name+'.mutant.stdout')).write_bytes(p.stdout);(HERE/(name+'.mutant.stderr')).write_bytes(p.stderr)
  compiled=b'build failed'not in p.stdout+p.stderr and b'undefined:'not in p.stdout+p.stderr and b'syntax error'not in p.stdout+p.stderr
  record=dict(name=name,argv=p.args,exit=p.returncode,compiled=compiled,killed=compiled and p.returncode!=0,duration=time.monotonic()-start,source_sha256=hashlib.sha256(path.read_bytes()).hexdigest());results.append(record);path.write_bytes(original[path]);assert record['killed'],record
finally:
 for p,b in original.items():p.write_bytes(b)
 (HERE/'mutants.json').write_text(json.dumps(dict(results=results,source_restored=all(p.read_bytes()==b for p,b in original.items()),scope='actual compile-valid H production mutants; no integer-to-opaque compile failure counted'),indent=2)+'\n')
print(json.dumps(dict(compiled_killed=len(results),restored=True)))
