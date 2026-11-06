"""Bounded actual Go source-overlay mutants; source files never changed."""
import json,subprocess,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
mutants=[('unknown-profile-accept','new.go','config.Profile != HistoricalUS51DosTextStandardPrinter','false'),('New-acquires-Loaded-birth','new.go','parseRevision(raw, &birthLineage{kind: newBirth})','parseRevision(raw, nil)'),('publisher-drops-New-birth','mutation.go','parseRevision(candidate, d.state.birth)','Parse(candidate)'),('cached-DOS-date-changes','new.go','cachedDosStamp(1992, 3, 9, 12, 4, 20)','cachedDosStamp(1993, 3, 9, 12, 4, 20)')]
rows=[]
with tempfile.TemporaryDirectory(prefix='wp46-mutants-')as tmp:
 for name,file,old,new in mutants:
  path=ROOT/'internal/document'/file;text=path.read_text();assert text.count(old)==1,(name,'exact source scope');replacement=Path(tmp)/file;replacement.write_text(text.replace(old,new));overlay=Path(tmp)/'overlay.json';overlay.write_text(json.dumps({'Replace':{str(path):str(replacement)}}));argv=['go','test','-overlay',str(overlay),'./internal/document','-run','TestNew','-count=1'];p=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True);log=HERE/'checks'/str('mutant-'+name+'.log');log.write_text(p.stdout+p.stderr);assert p.returncode!=0 and ('--- FAIL' in p.stdout or 'panic:' in p.stdout)and 'build failed'not in (p.stdout+p.stderr),(name,p.stdout,p.stderr);rows.append({'name':name,'source':str(path.relative_to(ROOT)),'exact_edit':{'from':old,'to':new},'argv':argv,'exit':p.returncode,'public_test_failure_not_build_error':True,'log':str(log.relative_to(ROOT))})
(HERE/'mutation-results.json').write_text(json.dumps(rows,indent=2)+'\n');print(len(rows),'meaningful mutants detected')
