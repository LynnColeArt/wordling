from pathlib import Path
import json,os,subprocess,sys
P=Path(__file__).resolve().parent;rows=[]
for variant,provider in [('old','/tmp/wordling-WP58-cycle2-disposables/old_provider.py'),('new','/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-p/scripts/reference/startup_transport.py')]:
 out=P/('replay-'+variant);out.mkdir()
 for case in ['process','deadline']:
  env={**os.environ,'WP58_REVIEW_PROVIDER':provider,'WP58_REVIEW_OUTPUT':str(out)};argv=[sys.executable,'-B',str(P/('replay-'+case+'.py'))]
  with(out/(case+'.stdout.log')).open('wb')as a,(out/(case+'.stderr.log')).open('wb')as b:q=subprocess.run(argv,env=env,stdout=a,stderr=b,timeout=12)
  assert q.returncode==0;rows.append(dict(variant=variant,case=case,argv=argv,provider=provider,exit=q.returncode))
old=json.loads((P/'replay-old/readiness-adversary-v2.json').read_text());new=json.loads((P/'replay-new/readiness-adversary-v2.json').read_text());assert all(x['outcome']=='returned-success'for x in old['observations'][1:]);assert all(x['outcome']=='refused'and x['error']=='process-limit'and x['result']['peak_processes']>=3 for x in new['observations'][1:])
a=json.loads((P/'replay-old/readiness-deadline-adversary.json').read_text());b=json.loads((P/'replay-new/readiness-deadline-adversary.json').read_text());assert all(x['outcome']=='returned-success'for x in a['observations']);assert all(x['outcome']=='refused'and x['error']=='readiness-deadline'for x in b['observations']);(P/'old-red-new-green.json').write_text(json.dumps(dict(commands=rows,process_3_vs2_oldRED_newGREEN_two_repetitions=True,selected_readiness_point1_vs2_oldRED_newGREEN_two_repetitions=True,new_peak_violating_sample_retained=True,actual_public_API_no_monkeypatch=True),indent=2)+'\n');print('Old RED/new GREEN confirmed for both original I1 repros, each repeated twice')
