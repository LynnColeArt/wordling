#!/usr/bin/env python3
"""Selected compiling semantic faults via overlays; real source stays sealed."""
import hashlib,json,subprocess,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cases=[
 ('off-gap','deletion.go','if s.target == s.off {\n\t\t\tgap--\n\t\t}','if s.target == s.off {\n\t\t\tgap -= 0\n\t\t}','TestWP40ExactObservedPaths'),
 ('closing-literal-order','deletion.go','remembered = joinFragments(d.fragment(s.on, s.on+1), d.fragment(s.off, s.off+1))','remembered = joinFragments(d.fragment(s.off, s.off+1), d.fragment(s.on, s.on+1))','TestWP40ExactObservedPaths'),
 ('invented-count','history.go','h.state != nil && h.state.observed == nil && !h.state.effectUnqualified','h.state != nil && !h.state.effectUnqualified','TestWP40ExactObservedPaths'),
 ('unqualified-pair','deletion.go','!h.wp40Target(s)','false','TestWP40UnqualifiedContextsRemainAtomic'),
 ('repeat-Restore','history.go','h.state.observed.restored || !h.state.observed.browsed || p.state.index != 0','p.state.index != 0','TestWP40ExactObservedPaths'),
 ('forged-ascii-receipt','history.go','r.Changed != a.changed','false','TestASCIIReceiptOwnershipAndUnknownHistoryEffects'),
 ('closing-overlay-identity','history_observation.go','return p.state.index % 2','return 0','TestWP40ExactObservedPaths'),
]
before={str(p):sha(p)for p in(ROOT/'internal/document').glob('*.go')};results=[]
for name,file,old,new,test in cases:
 original=ROOT/'internal/document'/file;text=original.read_text()
 if text.count(old)!=1:raise ValueError('Unstable mutation seam: '+name)
 with tempfile.TemporaryDirectory(prefix='mutant-',dir=HERE)as temp:
  directory=Path(temp);mutant=directory/file;mutant.write_text(text.replace(old,new));overlay=directory/'overlay.json';overlay.write_text(json.dumps({'Replace':{str(original):str(mutant)}}))
  argv=['go','test','-overlay',str(overlay),'./internal/document','-run','^'+test+'$','-count=1'];r=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True);log=r.stdout+r.stderr
  (HERE/('mutant-'+name+'.txt')).write_text(log)
  killed=r.returncode!=0 and '--- FAIL: '+test in log and '[build failed]'not in log
  results.append({'name':name,'source':str(original.relative_to(ROOT)),'replacement':[old,new],'target':test,'argv':argv,'exit':r.returncode,'compiling_semantic_fault_killed':killed})
  if not killed:raise ValueError('Survived or noncompiling fault: '+name)
assert before=={str(p):sha(p)for p in(ROOT/'internal/document').glob('*.go')}
(HERE/'mutants.json').write_text(json.dumps({'source_hashes_unchanged':before,'cases':results},indent=2)+'\n')
print(len(results),'compiling domain faults killed; real source unchanged')
