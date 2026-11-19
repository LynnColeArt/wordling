"""Compiled production mutations via Go overlays; on-disk source stays frozen."""
from pathlib import Path
import tempfile,subprocess,json,hashlib,os,time
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent;PACKAGE=ROOT/'internal/merge/native'
mutants=[
 ('lossy-unknown-export','image.go','return i.state.image.Export()','return i.state.image.Export()[:i.state.size-1]','TestAll104OriginalPublicSpansAndRoles'),
 ('cross-source-span-retarget','image.go',' || span.source != i.state','','TestOwnershipCapturedProgramAndWrapperSubstitution'),
 ('operand-terminator-retarget','semantic.go','Terminator: t.Raw','Terminator: span(s, start, end)','TestAll104OriginalPublicSpansAndRoles'),
 ('count-as-visible-end-fields','semantic.go','StoredCount: c.RawCount','StoredCount: uint16(len(b.fields))','TestRecordsKeepCountsFieldsAndInterstitialUnknowns'),
 ('drop-genuine-empty-field','semantic.go','b.fields = append(b.fields, f)','if !f.Empty { b.fields = append(b.fields, f) }','TestRecordsKeepCountsFieldsAndInterstitialUnknowns'),
 ('swallow-next-command','semantic.go','return Operand{}, index, nil','return Operand{}, index+1, nil','TestMalformedOperandNeverSwallowsFollowingNativeCommand'),
 ('admit-Result','view.go','return v.Valid() && !v.state.blocked','return v.Valid() && (v.state.info.Role == Result || !v.state.blocked)','TestAll104OriginalPublicSpansAndRoles'),
 ('skip-real-token-traversal-limit','image.go','if len(s.tokens) >= limits.Tokens {','if false {','TestExactAndOneOverLimits'),
]
results=[]
for name,file,old,new,test in mutants:
 source=PACKAGE/file;raw=source.read_text();assert old in raw,(name,old);changed=raw.replace(old,new);archive=OUT/('mutant-'+name+'.go.txt');archive.write_text(changed)
 with tempfile.TemporaryDirectory(prefix='wp50-mutant-')as tmp:
  code=Path(tmp)/file;code.write_text(changed);overlay=Path(tmp)/'overlay.json';overlay.write_text(json.dumps({'Replace':{str(source):str(code)}}));target='./internal/merge/native/evidence/contracts'if name=='swallow-next-command'else'./internal/merge/native';argv=['go','test','-overlay='+str(overlay),target,'-run','^'+test+'$','-count=1','-json'];start=time.monotonic();p=subprocess.run(argv,cwd=ROOT,env=dict(os.environ,GOMAXPROCS='2'),capture_output=True,text=True,timeout=60);log=p.stdout+p.stderr;(OUT/('mutant-cycle2-'+name+'.log')).write_text(log);events=[]
  for line in p.stdout.splitlines():
   try:events.append(json.loads(line))
   except json.JSONDecodeError:pass
  killed=p.returncode!=0 and any(e.get('Action')=='fail'and e.get('Test','').startswith(test)for e in events)
  row={'name':name,'source_path':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw.encode()).hexdigest(),'mutant_sha256':hashlib.sha256(changed.encode()).hexdigest(),'actual_test':test,'argv':argv,'GOMAXPROCS':2,'elapsed_seconds':time.monotonic()-start,'exit':p.returncode,'compiled_and_test_assertion_killed':killed};results.append(row);(OUT/'mutation-results-cycle2.json').write_text(json.dumps(results,indent=2)+'\n');print(name,killed,flush=True)
  assert killed,(name,log[-2500:])
 assert source.read_text()==raw
