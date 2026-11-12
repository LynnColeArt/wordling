"""Only the two ROOT-authorized affected F2 controls; no other case repeats."""
import json
from pathlib import Path
import sys
import time
from runtime_qualification_supervisor import supervise

ROOT=Path('/tmp/wordling-WP70-helper-controls-cycle2-02')
TREE='''import os,signal,time,json
signal.signal(signal.SIGTERM,signal.SIG_IGN)
child=os.fork()
print(json.dumps(dict(pid=os.getpid(),child=child,pgid=os.getpgrp())),flush=True)
time.sleep(10)
'''

def main():
    start=time.monotonic();end=start+30;ROOT.mkdir(mode=0o700,exist_ok=False);results=[]
    env=dict(PATH='/usr/bin:/bin',HOME=str(ROOT),LANG='C.UTF-8',LC_ALL='C.UTF-8',PYTHONDONTWRITEBYTECODE='1')
    for name in ('coordinator-kill','whole-deadline'):
        outcome=supervise(['/usr/bin/python3','-I','-B','-c',TREE],ROOT,env,ROOT/name,seconds=min(.35 if name=='whole-deadline' else 2,end-time.monotonic()),control='kill-coordinator' if name=='coordinator-kill' else None)
        events=outcome['leader_identity_events']
        assert outcome['cleanup_qualified'] and not outcome['owned_children_remaining'] and outcome['cleanup_seconds']<=2
        assert outcome['escalated'] and outcome['elapsed']<=2.5 and outcome['coordinator_reaped_last']
        assert events and events[-1]['event']=='leader_reaped_LAST' and events[-1]['other_owned_children']==[]
        assert all(e['event']=='before_group_signal' and e['retained_direct_child'] for e in events[:-1])
        assert any(e['waitid_WNOWAIT'] and e['waitid_WNOWAIT']['pid']==e['leader'] for e in events[:-1])
        assert outcome['reaped'][-1]['pid']==events[-1]['leader']
        results.append(dict(case=name,status='PASS',outcome=outcome));(ROOT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',cases=2,elapsed=time.monotonic()-start,P=False,TCB_qualification=False)))
    return 0

if __name__=='__main__':
    try:result=main()
    except SystemExit as e:result=e.code
    except BaseException:
        import traceback;traceback.print_exc();result=2
    raise SystemExit(result)
