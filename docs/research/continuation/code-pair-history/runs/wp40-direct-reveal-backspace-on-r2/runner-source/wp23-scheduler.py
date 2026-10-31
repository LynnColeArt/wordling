#!/usr/bin/env python3
"""Serial predeclared eighteen-attempt schedule; no implicit release or retry."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[4]
CLI=ROOT/'scripts/reference/code_pair_history.py'
OUT=Path(__file__).resolve().parent


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--allow-vm',action='store_true');p.add_argument('--authorization-note',default='')
    a=p.parse_args()
    if not a.allow_vm or not a.authorization_note.strip():
        print('No guest: explicit root release and both controls required');return 1
    plan=json.loads(subprocess.check_output([sys.executable,str(CLI),'plan'],text=True));records=[]
    drivers=OUT/'drivers';drivers.mkdir(exist_ok=True)
    for case in plan['cases']:
        for repetition in [1,2]:
            run_id='wp40-'+case['id']+'-r'+str(repetition)
            argv=[sys.executable,str(CLI),'run',run_id,'--case',case['id'],'--allow-vm','--authorization-note',a.authorization_note]
            with(drivers/(run_id+'.stdout')).open('x')as stdout,(drivers/(run_id+'.stderr')).open('x')as stderr:
                result=subprocess.run(argv,cwd=ROOT,stdout=stdout,stderr=stderr)
            records.append({'id':run_id,'case':case['id'],'repetition':repetition,'argv':argv,'exit':result.returncode})
            (OUT/'execution.json').write_text(json.dumps(records,indent=2)+'\n')
            print(run_id,'exit',result.returncode,flush=True)
            if result.returncode:return result.returncode
    return 0


if __name__=='__main__':sys.exit(main())
