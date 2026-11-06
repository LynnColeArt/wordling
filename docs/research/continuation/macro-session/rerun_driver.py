#!/usr/bin/env python3
"""Root-authorized five-recipe corrected series; originals never overwritten."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'docs/research/continuation/macro-session'
PRIVATE=Path('/home/lynn/projects/wordling/research/cache/reference')


def main():
    plan=json.loads((OUT/'rerun-prelaunch.json').read_text())
    code=ROOT/'scripts/reference/macro_session.py'
    rows=[]
    report={'controller_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'prelaunch_source_sha256':plan['runner_sha256'],'root_authorization':plan['root_authorization'],
            'scope':'original-reference-only','wordling_tested':False,'results':rows}
    for spec in plan['cases']:
        assert hashlib.sha256(code.read_bytes()).hexdigest()==plan['runner_sha256'],'Source changed after prelaunch'
        run_id=spec['new_run_id'];case=spec['case'];drivers=OUT/'drivers'
        stdout=drivers/(run_id+'.stdout.json');stderr=drivers/(run_id+'.stderr.txt')
        if stdout.exists()or stderr.exists():raise FileExistsError('Immutable driver evidence')
        argv=[sys.executable,str(code),'run',run_id,'--case',case,'--allow-vm',
              '--authorization-note',plan['root_authorization']]
        row={'run_id':run_id,'case':case,'argv':argv,'started_at':datetime.now(timezone.utc).isoformat()}
        print(case,'START',flush=True)
        with stdout.open('w')as so,stderr.open('w')as se:
            proc=subprocess.run(argv,cwd=ROOT,stdout=so,stderr=se)
        row['exit_code']=proc.returncode
        manifest=OUT/'runs'/run_id/'run.json'
        if manifest.exists():
            data=json.loads(manifest.read_text());row['outcomes']=[(r['id'],r['outcome'],r.get('error'))for r in data['results']]
            row['all_guests_stopped']=all(r.get('guest_stopped')for r in data['results'])
            row['master_unchanged']=data.get('master_before')==data.get('master_after')
            asset=manifest.parent/'input/M38.WPM'
            if asset.exists()and row['all_guests_stopped']:
                assert hashlib.sha256(asset.read_bytes()).hexdigest()==spec['input_sha256']
                row['stopped_macro_exports']=[]
                destdir=OUT/'post-extraction-02';destdir.mkdir(exist_ok=True)
                for sample in data['results']:
                    work=PRIVATE/'runs'/('wp38-'+run_id)/sample['id'];dest=destdir/(run_id+'-'+sample['id']+'.WPM')
                    extract=subprocess.run(['mcopy','-i',str(work/'harddisk.img')+'@@1048576','::OUT/M38.WPM',str(dest)],capture_output=True,text=True,timeout=15)
                    row['stopped_macro_exports'].append({'exit_code':extract.returncode,'stderr':extract.stderr,
                        'path':str(dest.relative_to(OUT)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()if dest.exists()else None})
        assert hashlib.sha256(code.read_bytes()).hexdigest()==plan['runner_sha256'],'Source edited during guest run'
        rows.append(row);(OUT/'rerun-execution.json').write_text(json.dumps(report,indent=2)+'\n')
        print(case,'EXIT',proc.returncode,row.get('outcomes'),flush=True)
        if proc.returncode or not row.get('all_guests_stopped'):
            raise SystemExit('Driver or stop failure; no further guest launches')
    print('CORRECTED FINITE SERIES COMPLETE; all guests stopped and authored WPMs extracted',flush=True)


if __name__=='__main__':main()
