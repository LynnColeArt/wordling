from pathlib import Path
import os,sys,subprocess,json
sys.dont_write_bytecode=True
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-w');F=R/'docs/research/continuation/secondary-record-contract/fix-cycle-1';O=Path('/tmp/wordling-WP53-independent-review/cycle-2');rows=[]
for name,test,needle in [('reaped-leader-gate','test_exited_leader_timeout','did not become reapable'),('skip-escalation-for-exited-leader','test_exited_leader_ignores_TERM','HelperTimeout')]:
 src=F/'evidence'/('mutant-'+name+'.py.txt');receipt=O/('mutant-'+name+'.json');argv=[sys.executable,'-B',str(F/'test_cleanup.py'),'-k',test];p=subprocess.run(argv,cwd=R,capture_output=True,timeout=15,env={**os.environ,'WP53_CHECKER_SOURCE':str(src),'WP53_CLEANUP_RECEIPT':str(receipt),'PYTHONDONTWRITEBYTECODE':'1'});raw=p.stdout+p.stderr;(O/('mutant-'+name+'.log')).write_bytes(raw);assert p.returncode==1 and b'FAILED (failures=1)'in raw and needle.encode()in raw;data=json.loads(receipt.read_text());assert data['tests']==1 and data['failures']==1 and data['errors']==0;assert data['results'][0]['RED_emergency_cleanup_only_recorded_owned_group'];rows.append({'name':name,'argv':argv,'exit':p.returncode,'actual_OS_semantic_kill':True,'only_recorded_test_group_cleanup':True})
(O/'mutants.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
