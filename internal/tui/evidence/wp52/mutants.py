#!/usr/bin/env python3
"""Serial compiling production mutations; exact source always restored.
No Go dependency/core/test expectation changes, no original reference runtime.
"""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def main():
 paths=[ROOT/'internal/tui/model.go',ROOT/'internal/tui/reveal.go'];base={p:p.read_bytes() for p in paths};out=HERE/'mutants';out.mkdir();results=[]
 model=base[paths[0]].decode();reveal=base[paths[1]].decode()
 first='''
 // DELIBERATE MUTANT: rediscover current label through its first text match.
 var flat strings.Builder
 target := ""
 for _, run := range lower { flat.WriteString(run.text); if run.role == revealActive { target = run.text } }
 if target != "" {
  first := strings.Index(flat.String(), target)
  var wrong []revealRun
  at := 0
  for _, run := range lower {
   role := run.role; if role == revealActive { role = revealBase; if len(run.text)==6 { role=revealCode } }
   for j:=0;j<len(run.text);j++ { r:=role; if at>=first && at<first+len(target) { r=revealActive };wrong=append(wrong,revealRun{text:run.text[j:j+1],role:r});at++ }
  };lower=wrong
 }
'''
 cases=[('one-cell-code',model.replace('lower = append(lower, revealRun{text: rt, role: role})','''if role==revealActive && len(rt)==6 { lower=append(lower,revealRun{text:rt[:1],role:role},revealRun{text:rt[1:],role:revealCode}) } else { lower = append(lower, revealRun{text: rt, role: role}) }'''),reveal,'TestRevealActiveNativeRangesPublicModel'),
 ('first-matching-text',model.replace('\tif nativeActive && p.CursorGap == d.TokenCount() {',first+'\n\tif nativeActive && p.CursorGap == d.TokenCount() {'),reveal,'TestRevealLiteralDuplicateAndEdgeTokens'),
 ('lower-width-upper-caret',model.replace('x = nx - ns','x = rx - rs'),reveal,'TestRevealActiveNativeRangesPublicModel'),
 ('window-end-EOF',model.replace('p.CursorGap == d.TokenCount()','p.CursorGap == count'),reveal,'TestRevealWindowEndIsNotEOFAndOpaqueRefusal'),
 ('lost-clipped-role',model,reveal.replace('if run.role != lastRole {','if run.role != lastRole && startCell == position {'),'TestRevealClippingAllLogicalRoles'),
 ('missing-reset',model.replace('out += "\\x1b[0m"','out += ""'),reveal.replace('out.WriteString("\\x1b[0m")','out.WriteString("")'),'TestRevealClipContainsStyles')]
 try:
  for name,m,r,test in cases:
   assert m!=model or r!=reveal
   folder=out/name;folder.mkdir();paths[0].write_text(m);paths[1].write_text(r)
   for p in paths:(folder/(p.name+'.txt')).write_bytes(p.read_bytes())
   build=subprocess.run(['go','test','./internal/tui','-run','^$'],cwd=ROOT,capture_output=True);(folder/'build.stdout').write_bytes(build.stdout);(folder/'build.stderr').write_bytes(build.stderr);assert build.returncode==0,name+' did not compile'
   argv=['go','test','./internal/tui','-run','^'+test+'$','-count=1'];run=subprocess.run(argv,cwd=ROOT,capture_output=True);(folder/'test.stdout').write_bytes(run.stdout);(folder/'test.stderr').write_bytes(run.stderr);assert run.returncode!=0,name+' survived'
   results.append({'name':name,'compile_exit':build.returncode,'test_exit':run.returncode,'test_argv':argv,'production_sources':{str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in paths},'killed':True})
 finally:
  for p,b in base.items():p.write_bytes(b)
 green=subprocess.run(['go','test','./internal/tui','-run','^TestReveal','-count=1'],cwd=ROOT,capture_output=True);(out/'restored.stdout').write_bytes(green.stdout);(out/'restored.stderr').write_bytes(green.stderr);assert green.returncode==0
 (out/'result.json').write_text(json.dumps({'mutants':results,'exact_source_restored':all(p.read_bytes()==b for p,b in base.items()),'restored_green_exit':green.returncode},indent=2)+'\n')
if __name__=='__main__':main()
