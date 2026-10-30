#!/usr/bin/env python3
"""Build branch/state metadata from completed immutable original runs."""
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).parent
ROOT=HERE.parents[3]


def build(prefix):
    selection=json.loads((HERE/'accepted-branches.json').read_text())
    accepted=set(selection['accepted_run_ids']);branches={};diagnostics=[]
    for path in sorted((HERE/'runs').glob(prefix+'*/run.json')):
        run=json.loads(path.read_text());result=run['results'][0]
        if run['run_id'] not in accepted:
            diagnostics.append({'run_id':run['run_id'],'branch':run['branch'],'result':result['result'],'error':result.get('error'),'reason':'Initial expectation/cleanup revision or superseded repetition; raw record retained unchanged.'})
            continue
        row=branches.setdefault(run['branch'],{'case_ids':[x['case_id'] for x in run['results']],'runs':[],'states':{},'native_outputs':[]})
        row['runs'].append({'run_id':run['run_id'],'manifest':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'started_at':run['started_at']})
        directory=path.parent/result['case_id']
        for screen in sorted(directory.glob('*/screen.txt')):
            cursor=json.loads(screen.with_name('cursor.json').read_text());lines=screen.read_text().splitlines()
            facts={'first_line':lines[0],'bottom_nonempty':[s for s in lines[20:] if s],'hardware_cursor':{'row':cursor['row'],'column':cursor['column']},'screen_sha256':hashlib.sha256(screen.read_bytes()).hexdigest(),'screen_path':str(screen.relative_to(ROOT)),'cursor_path':str(screen.with_name('cursor.json').relative_to(ROOT))}
            row['states'].setdefault(screen.parent.name,[]).append(facts)
        row['native_outputs'].extend(result.get('native_outputs',[]))
    for branch,data in branches.items():assert len(data['runs'])==2,branch
    return {'scope':'Repeated original-only SESSION1 branches; no Wordling or full scenario verification','run_id_prefix_is_label_only':'2026-10-31 is a run label; started_at fields record actual UTC execution on2026-10-30.','branches':branches,'retained_diagnostics':diagnostics}


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('prefix');a=p.parse_args();print(json.dumps(build(a.prefix),indent=2))
