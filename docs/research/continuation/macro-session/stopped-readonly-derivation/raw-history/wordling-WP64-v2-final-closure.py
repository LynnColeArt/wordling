from pathlib import Path
import json,subprocess,os,sys,time,hashlib,ast
root=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-p');out=Path('/tmp/wordling-WP64-v2-final');out.mkdir(exist_ok=False)
paths=['scripts/reference/startup_transport.py']+[str(p.relative_to(root)) for p in sorted((root/'scripts/reference/startup_family').glob('*.py'))]+[str(p.relative_to(root)) for p in sorted((root/'tests/reference/stopped-readonly-derivation').glob('*.py'))]
current={p:dict(bytes=len((root/p).read_bytes()),sha256=hashlib.sha256((root/p).read_bytes()).hexdigest()) for p in paths}
assert len(current)==18,len(current)
for p in current:ast.parse((root/p).read_bytes(),filename=p)
Path('/tmp/wordling-WP64-v2-final-inputs.json').write_text(json.dumps(current,indent=2)+'\n');(out/'inputs.json').write_text(json.dumps(current,indent=2)+'\n')
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',DERIVATION_CLI_RESULTS=str(out/'new-cli'),DERIVATION_PUBLICATION_RESULTS=str(out/'new-publication'),DERIVATION_LOSS_RESULTS=str(out/'new-helper-loss'),DERIVATION_LARGE_RESULTS=str(out/'large.json'),DERIVATION_JOURNAL_RESULTS=str(out/'new-journals'),MEASUREMENT_RESULTS=str(out/'measurement'),STARTUP_PUBLICATION_RESULTS=str(out/'prior-publication'),ENVELOPE_CLI_RESULTS=str(out/'envelope-unit-cli'),ENVELOPE_BACKPRESSURE_RESULTS=str(out/'envelope-publication'),ENVELOPE_LARGE_RESULTS=str(out/'envelope-large.json'))
runner='tests/reference/stopped-readonly-derivation/run_suite.py';commands=[]
for name,count,limit in (('derivation',97,150),('envelope',42,60),('family',57,50),('legacy',62,40)):
 commands.append((name,[sys.executable,'-B',runner,'--suite',name,'--expect',str(count),'--junit',str(out/(name+'.xml'))],limit))
commands += [('old-cli',[sys.executable,'-B','tests/reference/stopped-readonly-derivation/capture_cli.py',str(out/'old-cli')],60),('old-mutants',[sys.executable,'-B','tests/reference/stopped-readonly-derivation/mutate.py',str(out/'old-mutants')],45),('measurement-mutants',[sys.executable,'-B','tests/reference/stopped-readonly-derivation/mutate_measurement.py',str(out/'measurement-mutants')],45),('configured',[sys.executable,'-B','scripts/review_checks.py','--junitxml='+str(out/'configured.xml')],20)]
(out/'frozen-command-roster.json').write_text(json.dumps({'commands':commands,'total_seconds_bound':300,'individual_fixture_seconds_bound':30,'input_count':18,'no_retry':True},indent=2)+'\n')
start=time.monotonic();rows=[]
for name,argv,limit in commands:
 remaining=300-(time.monotonic()-start);assert remaining>0
 began=time.monotonic()
 try:p=subprocess.run(argv,cwd=root,env=env,capture_output=True,timeout=min(limit,remaining))
 except subprocess.TimeoutExpired as error:
  (out/(name+'.stdout')).write_bytes(error.stdout or b'');(out/(name+'.stderr')).write_bytes(error.stderr or b'');rows.append(dict(name=name,argv=argv,timeout=True,seconds=time.monotonic()-began));break
 (out/(name+'.stdout')).write_bytes(p.stdout);(out/(name+'.stderr')).write_bytes(p.stderr)
 rows.append(dict(name=name,argv=argv,exit=p.returncode,seconds=time.monotonic()-began));print(name,p.returncode,round(rows[-1]['seconds'],3),flush=True)
 (out/'commands.json').write_text(json.dumps(dict(commands=rows,elapsed=time.monotonic()-start,current_inputs=current),indent=2)+'\n')
 if p.returncode:break
assert all(hashlib.sha256((root/p).read_bytes()).hexdigest()==r['sha256'] for p,r in current.items())
sys.exit(0 if len(rows)==len(commands) and all(r.get('exit')==0 for r in rows) else 1)
