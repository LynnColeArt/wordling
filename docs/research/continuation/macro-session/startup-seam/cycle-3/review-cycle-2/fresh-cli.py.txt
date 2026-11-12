from pathlib import Path
import json,subprocess,sys,time,os,hashlib
O=Path(__file__).resolve().parent;S=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-p/scripts/reference/startup_transport.py');rows=[]
for case in ['success','nonzero','stdout','stderr','hang','orphan','observer-fail','readiness']:
 argv=[sys.executable,'-B',str(S),'fixture',case];start=time.monotonic()
 with(O/f'cli-{case}.stdout.json').open('wb')as out,(O/f'cli-{case}.stderr.log').open('wb')as err:
  p=subprocess.run(argv,stdout=out,stderr=err,timeout=6)
 b=(O/f'cli-{case}.stdout.json').read_bytes();d=json.loads(b);expected=0 if case in ['success','readiness']else 1;assert p.returncode==expected and d['ok']==(expected==0)and len(b)<=65536;rows.append(dict(case=case,argv=argv,cwd=os.getcwd(),exit=p.returncode,expected_exit=expected,bytes=len(b),elapsed=time.monotonic()-start,source_sha256=hashlib.sha256(S.read_bytes()).hexdigest()))
(O/'fresh-cli.json').write_text(json.dumps(rows,indent=2)+'\n');print('8 real closed CLI cases have expected exits, bounded raw output retained')
