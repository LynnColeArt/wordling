#!/usr/bin/env python3
"""Authorized finite WP38 series; serial guests only, with durable child logs."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'docs/research/continuation/macro-session'
CASES=['run-doc1','repeat-doc2','missing-name','pending-save','internal-cancel','stop-default','stop-on','stop-off']


def main():
    rows=[]
    drivers=OUT/'drivers';drivers.mkdir(exist_ok=True)
    report={'controller_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'authorization':'Explicit root oracle release after WP23 final stop/extraction; WP38 owns shared lock exclusively for this finite series.',
            'scope':'original-reference-only','wordling_tested':False,'results':rows}
    for case in CASES:
        run_id='wp38-'+case+'-01'
        stdout=drivers/(run_id+'.stdout.json');stderr=drivers/(run_id+'.stderr.txt')
        if stdout.exists()or stderr.exists():raise FileExistsError('Refusing to overwrite driver evidence')
        argv=[sys.executable,str(ROOT/'scripts/reference/macro_session.py'),'run',run_id,'--case',case,
              '--allow-vm','--authorization-note',report['authorization']]
        row={'case':case,'run_id':run_id,'argv':argv,'started_at':datetime.now(timezone.utc).isoformat()}
        print(case,'START',flush=True)
        with stdout.open('w')as so,stderr.open('w')as se:
            result=subprocess.run(argv,cwd=ROOT,stdout=so,stderr=se)
        row['exit_code']=result.returncode
        manifest=OUT/'runs'/run_id/'run.json'
        if manifest.exists():
            data=json.loads(manifest.read_text());row['outcomes']=[(r['id'],r['outcome'],r.get('error'))for r in data['results']]
            row['all_guests_stopped']=all(r.get('guest_stopped')for r in data['results'])
            row['master_unchanged']=data.get('master_before')==data.get('master_after')
        rows.append(row)
        (OUT/'series-execution.json').write_text(json.dumps(report,indent=2)+'\n')
        print(case,'EXIT',result.returncode,row.get('outcomes'),flush=True)
        if result.returncode or not row.get('all_guests_stopped'):
            raise SystemExit('Driver/stop failure: stop series and report; never launch another guest')
    print('FINITE SERIES FINISHED; all guests stopped; shared lock released before offline reporting',flush=True)


if __name__=='__main__':main()
