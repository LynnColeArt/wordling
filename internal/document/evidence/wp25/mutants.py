#!/usr/bin/env python3
"""Focused compiling faults via Go overlays; production files never modified."""
import argparse,hashlib,json,subprocess,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
parser=argparse.ArgumentParser();parser.add_argument('--revision-fix',action='store_true');args=parser.parse_args()
prefix='revision-fix-' if args.revision_fix else ''
cases=[
 ('stale-revision','mutation.go','if c.document != d {','if c.document != d && false {','TestASCIICommandSequenceAndRevision'),
 ('unqualified-resource','admission.go','if !allowed {','if !allowed && false {','TestEveryQualifiedPrefixByteAndLiteralVariants'),
 ('fixed-flags-offset','mutation.go','candidate[flags] |= 8','candidate[flags-flags+256] |= 8','TestIndexedFlagLocationAndInputPrefixOwnership'),
 ('third-pair','admission.go','pairs >= MaxBoldPairs','pairs >= MaxBoldPairs+1','TestMutationRefusalIsAtomic'),
 ('rewritten-cache','mutation.go','candidate[flags] |= 8','candidate[flags] |= 8; candidate[101], candidate[102] = 0x11, 0x72','TestEveryQualifiedPrefixByteAndLiteralVariants'),
]
if args.revision_fix:
 cases[0]=('stale-revision','mutation.go','if c.state != d.state {','if c.state != d.state && false {','TestWrapperReplacementCannotRebindCursor')
 cases.append(('mutated-published-state','mutation.go','next.state.original = d.state.original','next.state.original = d.state.original; *d.state = *next.state; next.state = d.state','TestZeroRepeatedAndIndependentWrapperSnapshots'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
before={str(p):sha(p) for p in (ROOT/'internal/document').glob('*.go')};results=[]
for name,file,old,new,test in cases:
 original=ROOT/'internal/document'/file;text=original.read_text()
 if text.count(old)!=1:raise ValueError('Mutation seam changed: '+name)
 with tempfile.TemporaryDirectory(prefix='overlay-',dir=HERE) as tmp:
  directory=Path(tmp);mutant=directory/file;mutant.write_text(text.replace(old,new));overlay=directory/'overlay.json';overlay.write_text(json.dumps({'Replace':{str(original):str(mutant)}}))
  command=['go','test','-overlay',str(overlay),'./internal/document','-run','^'+test+'$','-count=1']
  run=subprocess.run(command,cwd=ROOT,text=True,capture_output=True)
  log=run.stdout+run.stderr;(HERE/(prefix+'mutant-'+name+'.txt')).write_text(log)
  killed=run.returncode!=0 and ('--- FAIL: '+test) in log and '[build failed]' not in log
  results.append({'name':name,'source':str(original.relative_to(ROOT)),'change':[old,new],'target':test,'exit_code':run.returncode,'compiling_fault_killed_by_assertion':killed})
  if not killed:raise ValueError('Surviving/noncompiling mutation: '+name)
if before!={str(p):sha(p) for p in (ROOT/'internal/document').glob('*.go')}:raise ValueError('Production source changed')
(HERE/(prefix+'mutants.json')).write_text(json.dumps({'technique':'Go overlay; actual production source never changed','source_hashes_unchanged':before,'selected_faults':results},indent=2)+'\n')
print(str(len(results))+' compiling semantic faults killed; actual source byte-identical')
