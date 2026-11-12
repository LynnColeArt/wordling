from pathlib import Path
import importlib.util,sys,subprocess,unittest,json,io,hashlib
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-s');T=Path('/tmp/wordling-wp42-independent');sys.path.insert(0,str(R/'scripts/reference'))
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
raw=subprocess.check_output(['git','show','504343e:scripts/reference/resaved_prefix.py'],cwd=R);p=T/'old-runner.py.txt';p.write_bytes(raw)
s=importlib.util.spec_from_loader('old_control',loader=None);old=importlib.util.module_from_spec(s);old.__file__=str(R/'scripts/reference/resaved_prefix.py');exec(compile(raw,str(p),'exec'),old.__dict__)
t=load('test_control',R/'docs/research/continuation/resaved-prefix/tests/test_resaved_prefix.py');current=t.r
results=[]
for label,mod,wanted in [('old504',old,1),('fixed',current,0)]:
 t.r=mod;stream=io.StringIO();res=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.TestSuite([t.Tests('test_first_protocol_failure_stops_batch_after_guarded_extraction')]))
 (T/(label+'-stop.log')).write_text(stream.getvalue());assert len(res.failures)==wanted and not res.errors
 results.append({'source':label,'tests':res.testsRun,'failures':len(res.failures),'errors':len(res.errors)})
(T/'stop-control.json').write_text(json.dumps({'old_source_sha256':hashlib.sha256(raw).hexdigest(),'adaptation':'old __file__ bound to actual workspace for test module constants only; same actual test/synthetic ports','results':results,'VM':False},indent=2)+'\n')
