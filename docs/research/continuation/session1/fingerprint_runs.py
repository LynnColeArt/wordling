#!/usr/bin/env python3
"""Read-only post-stop resource fingerprints; never publish resource contents."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[4]
PRIVATE=Path('/home/lynn/projects/wordling/research/cache/reference')
NAMES=['WP51/WP.EXE','WP51/WP.FIL','WP51/WP.DRS','WP51/STANDARD.PRS','WP51/STANPRIN.PRS','WP51/WP.LRS','WP51/WP{WP}.SET']


def collect(prefix):
    resources=json.loads((ROOT/'docs/research/reference-environment/resource-profile.json').read_text())['resources']
    records=[]
    for path in sorted((Path(__file__).parent/'runs').glob(prefix+'*/run.json')):
        run=json.loads(path.read_text())
        disk=PRIVATE/'session1-runs'/run['run_id']/'guest/harddisk.img'
        # Only closed run manifests are eligible, never the currently live disk.
        record={'run_id':run['run_id'],'run_manifest_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'resources':[]}
        for name in NAMES:
            data=subprocess.check_output(['mtype','-i',str(disk)+'@@1048576','::/'+name])
            item={'path':name,'size':len(data),'sha256':hashlib.sha256(data).hexdigest()}
            if name!='WP51/WP{WP}.SET':
                assert all(item[k]==resources[name][k] for k in ('path','size','sha256')),name
            else:
                item['baseline_sha256']=resources[name]['sha256']
                item['matches_master_setup']=item['sha256']==resources[name]['sha256']
                item['meaning']='Raw mutable setup fingerprint; no normalization or resource-equivalence inference.'
            record['resources'].append(item)
        records.append(record)
    return {'scope':'Read-only metadata from stopped private SESSION1 disks; no proprietary payload','runs':records}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('prefix');a=p.parse_args()
    print(json.dumps(collect(a.prefix),indent=2))
