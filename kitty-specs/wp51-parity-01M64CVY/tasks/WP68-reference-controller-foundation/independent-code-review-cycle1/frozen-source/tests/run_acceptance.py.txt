"""Finite OS coordinator, preserving each attempt and its exact source/argv pins."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import uuid
from deployment import deploy, preflight, pin, run, FILES, configure_deadline, remaining, configure_home

SOURCE = Path(__file__).resolve().parent.parent


def execute(label, full=False, all_checks=False, targeted=False):
    existing_files=sum(1 for p in (SOURCE/'evidence').rglob('*') if p.is_file())
    if existing_files + 650 > 2048:
        raise RuntimeError('finite fresh-suite evidence headroom insufficient')
    evidence = SOURCE/'evidence'/label
    evidence.mkdir()  # attempts are never overwritten
    roster = json.loads((SOURCE/'tests/roster.json').read_text())
    source = {str(p.relative_to(SOURCE)): pin(p) for p in sorted(SOURCE.rglob('*'))
              if p.is_file() and 'evidence' not in p.relative_to(SOURCE).parts and '__pycache__' not in p.parts}
    taskroot = Path('/tmp')/('wordling-WP68-'+label+'-'+uuid.uuid4().hex[:8])
    configure_home(taskroot)
    (evidence/'frozen-input.json').write_text(json.dumps(dict(source=source, roster=roster,
        cwd=str(taskroot), environment=dict(HOME=str(taskroot),PATH='/usr/local/go/bin:/usr/bin:/bin', LANG='C.UTF-8', LC_ALL='C.UTF-8', GOCACHE='/home/lynn/.cache/go-build', GOMODCACHE='/home/lynn/go/pkg/mod', GOPATH='/home/lynn/go', GOTOOLCHAIN='local', GOPROXY='off', GOSUMDB='off'),
        argv_template=['<pinned-copied-interpreter>','-I','-B','-m','reference_controller','<closed-command>'],
        limits=dict(cases=64, case_seconds=30, cleanup_seconds=2, suite_seconds=300,
                    output_per_case=2097152, evidence_files=2048, evidence_bytes=33554432),
        tools={x:pin(Path(x)) for x in ('/usr/bin/python','/usr/bin/strace','/usr/local/go/bin/go')}), indent=2)+'\n')
    if full:
        from functional import plans
        names=(['installed-transaction','canonical-json','full-phase-book','parent-symlink','fd-reuse','source-generation-kind-lock'] if targeted else roster['functional'])
        roots={name:'/tmp/wordling-reference-TEST-'+uuid.uuid4().hex[:16] for name in names}
        caseplans=plans(SOURCE,taskroot/'venv/bin/python',roots,names)
        (evidence/'exact-case-plans.json').write_text(json.dumps(caseplans,indent=2)+'\n')
        if all_checks:
            from mutants import freeze_mutants
            mutant_roots={name:'/tmp/wordling-reference-TEST-'+uuid.uuid4().hex[:16] for name in roster['semantic_mutants']}
            mutant_plan=freeze_mutants(SOURCE,taskroot/'mutants',mutant_roots)
            if targeted:mutant_plan={k:v for k,v in mutant_plan.items() if k=='forge-permitguard'}
            (evidence/'exact-mutant-plans.json').write_text(json.dumps(mutant_plan,indent=2)+'\n')
            (evidence/'configured-plan.json').write_text(json.dumps(dict(argv=['/usr/bin/python','-B','scripts/review_checks.py','--junitxml',str(evidence/'configured/checks.xml')],cwd=str(SOURCE.parents[3]),timeout=30,cleanup=2),indent=2)+'\n')
    interpreter, inventory = deploy(SOURCE, taskroot, evidence/'deployment')
    preflight(interpreter, inventory)
    if full:
        from functional import functional
        results=functional(SOURCE,interpreter,inventory,roots,caseplans,evidence,names)
        failed=any(x['status']!='PASS' for x in results)
        if all_checks:
            from mutants import execute_mutants
            mutant_results=execute_mutants(SOURCE,taskroot/'mutants',evidence/'mutants',mutant_plan,mutant_roots)
            failed=failed or any(x['status']!='KILLED' for x in mutant_results)
            # Configured adapter remains untouched. Its real seven check outcomes
            # are kept whole; the outer suite enforces this task's tighter bound.
            if not targeted:
                r=run(['/usr/bin/python','-B','scripts/review_checks.py','--junitxml',str(evidence/'configured/checks.xml')],SOURCE.parents[3],evidence/'configured/adapter')
                failed=failed or bool(r.returncode)
        return int(failed)
    root = '/tmp/wordling-reference-TEST-'+uuid.uuid4().hex[:16]
    args = [str(interpreter), '-I', '-B', '-m', 'reference_controller']
    admin = run(args+['test-admin','--root',root,'--generation','wp68-v1'], taskroot,evidence/'admin')
    if admin.returncode:
        return 1
    preflight(interpreter, inventory)
    result = run(args+['test-transaction','--root',root,'--generation','wp68-v1','--grant-id','first'],taskroot,evidence/'installed-transaction')
    (evidence/'result.json').write_text(json.dumps(dict(returncode=result.returncode, root=root,
                interpreter=str(interpreter), inventory_path=str(evidence/'deployment/deployment-inventory.json')),indent=2)+'\n')
    return result.returncode

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('label')
    parser.add_argument('--full',action='store_true')
    parser.add_argument('--all-checks',action='store_true')
    parser.add_argument('--targeted',action='store_true')
    args=parser.parse_args()
    started=time.monotonic()
    configure_deadline(started+300)
    outcome=1
    try:
        outcome=execute(args.label,args.full,args.all_checks,args.targeted)
        remaining()
    except Exception:
        import traceback
        raw=traceback.format_exc()
        print(raw,file=sys.stderr,end='')
        folder=SOURCE/'evidence'/args.label
        if folder.is_dir(): (folder/'coordinator.stderr').write_text(raw)
    finally:
        import resource
        folder=SOURCE/'evidence'/args.label
        if folder.is_dir():
            (folder/'whole.json').write_text(json.dumps(dict(argv=sys.argv,exit_code=outcome,elapsed_seconds=time.monotonic()-started,cumulative_child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,shared_deadline_seconds=300,case_seconds=30,cleanup_seconds=2),indent=2)+'\n')
    raise SystemExit(outcome)
