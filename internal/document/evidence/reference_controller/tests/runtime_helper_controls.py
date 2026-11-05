"""Six closed pregrant helper controls. No runtime qualification or product import."""
import argparse
import base64
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import signal
import sys
import time
import zipfile
from runtime_qualification import Preparation,parse_trace,pin,rights
from runtime_qualification_supervisor import supervise
from controller_deployment import review_wheel,SOURCE_NAMES

ROOT=Path('/tmp/wordling-WP70-helper-controls-cycle2-01')
S=Path(__file__).resolve().parent
OLD=Path('/tmp/wordling-WP70-runtime-qualification-source-freeze/runtime_qualification.py.txt')
ENV=dict(PATH='/usr/bin:/bin',HOME=str(ROOT),LANG='C.UTF-8',LC_ALL='C.UTF-8',PYTHONDONTWRITEBYTECODE='1')
SHELL='/usr/bin/sh'
EXACT="printf '%4096s' x; printf '%4096s' y >&2"
OVER=EXACT+'; printf z'
BURST=EXACT+'; i=0; while [ "$i" -lt 5000 ]; do : </dev/null; i=$((i+1)); done'
TREE='''import os,signal,time,json
signal.signal(signal.SIGTERM,signal.SIG_IGN)
child=os.fork()
print(json.dumps(dict(pid=os.getpid(),child=child,pgid=os.getpgrp())),flush=True)
time.sleep(10)
'''
CASES=('parser-data','wheel-data','exact-and-overflow','trace-burst','coordinator-kill','whole-deadline')


def expected():
    t=Path('/usr/bin/true').resolve()
    return dict(files={str(t):dict(**pin(t),**rights(t))},directories={},links={},closed_roots=[],tool_startup_hook_sets={})


def worker(kind,root):
    root=Path(root)
    if kind=='parser-data':
        # Normal import of a byte-exact old helper copy in a separate DATA
        # consumer process. No provider, runtime overlay or P API is involved.
        oldcopy=root/'old_runtime_qualification.py';oldcopy.write_bytes(OLD.read_bytes())
        import importlib.util
        spec=importlib.util.spec_from_file_location('old_control_helper',oldcopy)
        old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
        true=str(Path('/usr/bin/true').resolve())
        bad='11 execve('+json.dumps(true)+', ["true"], 0x0 /* 0 vars */) = 0\n22 execve("/outside/unavailable-child", ["child"], 0x0 <unfinished ...>\n22 <... execve resumed>) = 0\n'
        oldctx=old.Preparation(root/'old',root/'old/raw',expected());q=root/'trace.data';q.write_text(bad)
        oldctx.tool_origins(q,'old-counterexample')
        ctx=Preparation(root/'new',root/'new/raw',expected())
        refused=[]
        variants=dict(unfinished_foreign=bad,relative_after_chdir='11 chdir("/outside") = 0\n11 execve("relative", [], 0x0) = 0\n',unavailable_absolute='11 execve("/outside/unavailable-child", [], 0x0) = 0\n',truncated='11 execve("/outside"... , [], 0x0) = 0\n',unknown_actor='execve("/outside", [], 0x0) = 0\n',unmatched_resumed='22 <... execve resumed>) = 0\n',truncated_tail='11 execve("/outside", [], 0x0) = 0')
        for name,data in variants.items():
            q.write_text(data)
            try:ctx.tool_origins(q,'negative-'+name)
            except RuntimeError as e:refused.append(dict(name=name,reason=str(e)))
            else:raise AssertionError('UnresolvedOriginAccepted:'+name)
        good='11 execve('+json.dumps(true)+', [], 0x0 <unfinished ...>\n11 <... execve resumed>) = 0\n11 openat2(AT_FDCWD, "relative", {}, 24) = 3<'+true+'>\n'
        records=parse_trace(good);assert len(records)==2 and all(x['path']==true for x in records)
        print(json.dumps(dict(status='PASS',old_unfixed_data_RED='old parser accepted unresolved successful child',new_refusals=refused,new_joined_kernel_origins=records)))
    elif kind=='wheel-data':
        dist='wordling_reference_controller_test-0.2.0.dist-info'
        wanted={n:('DATA-'+n).encode() for n in SOURCE_NAMES}
        wanted.update({'reference_controller/testdata/master.bin':b'EXACT SOURCE MASTER DATA','reference_controller/testdata/fixture':b'NONEXECUTED COMPILED-OUTPUT STANDIN DATA'})
        def make(name,change=None):
            payload=dict(wanted)
            if change:payload[change]=payload[change]+b'X'
            payload[dist+'/METADATA']=b'Name: wordling-reference-controller-test\nVersion: 0.2.0\nRequires-Python: >=3.12\n'
            payload[dist+'/WHEEL']=b'Wheel-Version: 1.0\n';payload[dist+'/top_level.txt']=b'reference_controller\n'
            text=io.StringIO();csv.writer(text,lineterminator='\n').writerows([(n,'sha256='+base64.urlsafe_b64encode(hashlib.sha256(b).digest()).rstrip(b'=').decode(),len(b)) for n,b in payload.items()]+[(dist+'/RECORD','','')])
            payload[dist+'/RECORD']=text.getvalue().encode();p=root/name
            with zipfile.ZipFile(p,'w',compression=zipfile.ZIP_DEFLATED) as z:
                for n,b in payload.items():z.writestr(n,b)
            return p
        original=make('genuine-data.whl');review_wheel(original,wanted)
        results=[]
        for label in ('master.bin','fixture'):
            path=make(label+'.whl','reference_controller/testdata/'+label)
            # The OLD actual preinstall predicate compared only SOURCE_NAMES.
            # Execute that exact equality oracle on DATA: no mocked build or install.
            with zipfile.ZipFile(path) as z:
                assert all(z.read(n)==wanted[n] for n in SOURCE_NAMES)
            try:review_wheel(path,wanted)
            except RuntimeError as e:results.append(dict(member=label,old_predicate_RED='accepted changed data with consistent RECORD',new_refusal=str(e)))
            else:raise AssertionError('ChangedReviewedDataAdopted')
        print(json.dumps(dict(status='PASS',data_only=True,fixture_executed=False,results=results)))
    elif kind in ('exact','overflow','trace'):
        ctx=Preparation(root/'prepared',root/'prepared/raw',expected(),internal_earlier_output_cap=32768 if kind=='trace' else 8192)
        command=EXACT if kind=='exact' else OVER if kind=='overflow' else BURST
        try:result=ctx.run([SHELL,'-c',command],kind,tool=kind=='trace')
        except RuntimeError:
            if kind=='exact':raise
            # Actual supervisor abort owns cleanup; bounded raw child receipt is
            # the oracle. This worker is allowed to terminate before this print.
            print(json.dumps(dict(status='EXPECTED_REFUSAL',kind=kind)),flush=True)
            return 0
        if kind!='exact':raise AssertionError('OverflowAccepted')
        assert len(result.stdout)==4096 and len(result.stderr)==4096
        print(json.dumps(dict(status='PASS',exact_boundary=8192)),flush=True)
    else:raise ValueError(kind)
    return 0


def main():
    a=argparse.ArgumentParser();a.add_argument('--worker');a.add_argument('--root');a.add_argument('--run',action='store_true');args=a.parse_args()
    if args.worker:return worker(args.worker,args.root)
    if not args.run:raise SystemExit('DISABLED: ROOT finite helper-control authorization and frozen roster required')
    start=time.monotonic();end=start+30;results=[]
    ROOT.mkdir(mode=0o700,exist_ok=False)
    for name in CASES:
        case=ROOT/name;case.mkdir()
        if time.monotonic()>=end:raise RuntimeError('ControlSuiteDeadline')
        if name in ('parser-data','wheel-data'):
            outcome=supervise(['/usr/bin/python3','-B',str(Path(__file__).resolve()),'--worker',name,'--root',str(case)],ROOT,ENV,case/'supervisor',seconds=min(5,end-time.monotonic()))
            assert outcome['exit']==0 and outcome['cleanup_qualified'] and not outcome['partial_prefix'],outcome
        elif name=='exact-and-overflow':
            values=[]
            for sub in ('exact','overflow'):
                r=case/sub;r.mkdir()
                outcome=supervise(['/usr/bin/python3','-B',str(Path(__file__).resolve()),'--worker',sub,'--root',str(r)],ROOT,ENV,r/'supervisor',seconds=min(5,end-time.monotonic()))
                record=json.loads((r/'prepared/raw'/ (sub+'.whole.json')).read_text())
                assert record['combined_retained_bytes']==8192
                assert record['partial_prefix']==(sub=='overflow')
                assert outcome['cleanup_qualified']
                assert outcome['exit']==0 if sub=='exact' else outcome['reason']=='CoordinatorAbort'
                values.append(dict(sub=sub,helper=record,supervisor=outcome))
            outcome=values
        elif name=='trace-burst':
            outcome=supervise(['/usr/bin/python3','-B',str(Path(__file__).resolve()),'--worker','trace','--root',str(case)],ROOT,ENV,case/'supervisor',seconds=min(5,end-time.monotonic()))
            q=case/'prepared/raw';record=json.loads((q/'trace.whole.json').read_text());assert record['partial_prefix'] and record['combined_retained_bytes']==32768
            assert all((q/('trace.'+n)).stat().st_size>0 for n in ('stdout','stderr','trace'))
            assert sum((q/('trace.'+n)).stat().st_size for n in ('stdout','stderr','trace'))==32768
            assert outcome['cleanup_qualified']
        else:
            outcome=supervise(['/usr/bin/python3','-I','-B','-c',TREE],ROOT,ENV,case/'supervisor',seconds=min(.35 if name=='whole-deadline' else 2,end-time.monotonic()),control='kill-coordinator' if name=='coordinator-kill' else None)
            assert outcome['cleanup_qualified'] and not outcome['owned_children_remaining'] and outcome['cleanup_seconds']<=2
            assert outcome['escalated'] and outcome['elapsed']<=2.5
        results.append(dict(case=name,status='PASS',outcome=outcome));(ROOT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',cases=len(results),elapsed=time.monotonic()-start,actual_root=str(ROOT),TCB_qualification=False,P_effects=False)))
    return 0

if __name__=='__main__':
    try:result=main()
    except SystemExit as e:result=e.code
    except BaseException:
        import traceback;traceback.print_exc();result=2
    raise SystemExit(result)
