from pathlib import Path
import os,sys,json,subprocess
P=Path(__file__).resolve().parent
W=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-p');rows=[]
for variant,source in [('old935','/tmp/wordling-WP58-cycle3-disposables/old935.py'),('new676',str(W/'scripts/reference/startup_transport.py'))]:
 out=P/variant;out.mkdir()
 for case,script in [('I2','readiness-exec-adversary.py'),('I1-process','replay-process.py'),('I1-deadline','replay-deadline.py')]:
  env=dict(os.environ,WP58_REVIEW_PROVIDER=source,WP58_REVIEW_OUTPUT=str(out));argv=[sys.executable,'-B',str(P/script)]
  with(out/(case+'.stdout.log')).open('wb')as a,(out/(case+'.stderr.log')).open('wb')as b:r=subprocess.run(argv,cwd=W,env=env,stdout=a,stderr=b,timeout=12)
  assert r.returncode==0,(case,r.returncode);rows.append(dict(variant=variant,case=case,argv=argv,exit=r.returncode))
a=json.loads((P/'old935/readiness-exec-adversary.json').read_text());b=json.loads((P/'new676/readiness-exec-adversary.json').read_text());assert a['observations'][0]['error']=='identity-changed';assert all(x['outcome']=='returned-success'for x in a['observations'][1:]);assert all(x['outcome']=='refused'and not x['result']['ready']and x['error']in('unknown-identity','identity-changed')for x in b['observations'])
for n in ['old935','new676']:
 a=json.loads((P/n/'readiness-adversary-v2.json').read_text());assert all(x['error']=='process-limit'and x['result']['peak_processes']>=3 for x in a['observations'][1:]);b=json.loads((P/n/'readiness-deadline-adversary.json').read_text());assert all(x['error']=='readiness-deadline'for x in b['observations'])
(P/'regression-results.json').write_text(json.dumps(dict(commands=rows,I2_oldRED_newGREEN_two_fast_plus_delayed_control=True,I1_stays_closed_both_versions=True),indent=2)+'\n');print('I2 oldRED/newGREEN twice; delayed control; I1 process/deadline closed')
