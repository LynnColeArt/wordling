from pathlib import Path
import json,subprocess,tempfile,hashlib
root=Path.cwd();results=[]
with tempfile.TemporaryDirectory(prefix='wp19-independent-negative-') as tmp:
 tmp=Path(tmp);target=root/'tests/performance/main.go';original=target.read_text();assert original.count('s.Error = e.Error()')==1
 mutant=tmp/'main.go';mutant.write_text(original.replace('s.Error = e.Error()','s.Error = ""'))
 overlay=tmp/'overlay.json';overlay.write_text(json.dumps({'Replace':{str(target):str(mutant)}}))
 p=subprocess.run(['go','test','-overlay='+str(overlay),'./tests/performance','-run','^TestMeasurementRetainsFailuresWarmupAndOutlier$','-count=1','-v'],capture_output=True,text=True)
 assert p.returncode!=0 and '--- FAIL:' in p.stdout and 'build failed' not in p.stdout+p.stderr
 results.append({'negative':'drop actual collector failure','compiled':True,'assertion_rejected':True,'output':p.stdout+p.stderr})
 target=root/'tests/performance/measure.py';source=target.read_text();assert source.count("'refused' if error else 'accepted'")==1
 namespace={'__file__':str(target),'__name__':'independent_mutant'};exec(compile(source.replace("'refused' if error else 'accepted'","'accepted'"),str(target),'exec'),namespace)
 rows=namespace['summarize']({'phases':[{'name':'parse','warmup':[{}],'samples':[{'ns':1,'alloc_bytes':0,'allocs':0},{'ns':10000,'alloc_bytes':5,'allocs':1,'error':'TokenLimit'}]}]})
 try:assert [(r['status'],r['ns']['count']) for r in rows]==[('accepted',1),('refused',1)]
 except AssertionError:results.append({'negative':'classify refusal as accepted distribution','compiled':True,'assertion_rejected':True})
 else:raise AssertionError('mixed refusal mutant survived')
print(json.dumps({'independent_negatives':'PASS','results':results},indent=2))
