#!/usr/bin/env python3
"""Verify exact original evidence/pairs and optionally committed Git blob bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'scripts/reference'))
import text_layout


def digest(data):return hashlib.sha256(data).hexdigest()


def git_blobs(ref):
    paths=subprocess.check_output(['git','ls-files','-z','--','scripts/reference/text_layout.py',str(HERE.relative_to(ROOT))],cwd=ROOT).decode().split('\0')
    paths=[x for x in paths if x]
    proc=subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    try:
        for name in paths:
            proc.stdin.write((ref+':'+name+'\n').encode());proc.stdin.flush()
            header=proc.stdout.readline().decode().strip().split()
            if len(header)!=3 or header[1]!='blob':raise ValueError('Missing blob '+name)
            size=int(header[2]);raw=proc.stdout.read(size)
            if proc.stdout.read(1)!=b'\n':raise ValueError('Invalid Git batch framing')
            source=(ROOT/name).read_bytes()
            if len(raw)!=len(source) or digest(raw)!=digest(source):raise ValueError('Git blob differs from raw evidence '+name)
        proc.stdin.close()
        if proc.wait()!=0:raise ValueError('Git batch failed')
    finally:
        if proc.poll() is None:proc.terminate();proc.wait()
    return len(paths)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--git-ref')
    args=p.parse_args()
    runs=list((HERE/'runs').glob('*/run.json'))+list((HERE/'calibration').glob('*/run.json'))
    for run in runs:text_layout.verify(run.parent)
    source=json.loads((HERE/'source-manifest.json').read_text())
    for row in source['sources']:
        raw=(ROOT/row['path']).read_bytes()
        if len(raw)!=row['bytes'] or digest(raw)!=row['sha256']:raise ValueError('Source/summary changed '+row['path'])
    a=json.loads((HERE/'analysis.json').read_text())
    if a['wordling_tested'] is not False or a['normalization'] is not False or a['NFR005_accepted'] is not False:raise ValueError('Evidence scope promoted')
    expected={row['id'] for row in json.loads((HERE/'recipe-plan.json').read_text())['variants']}
    if {x['variant'] for x in a['repeated_variants']}!=expected:raise ValueError('Missing variant')
    count=0
    for pair in a['repeated_variants']:
        if pair['fresh_run_count']!=2 or not pair['same_profile_and_inputs']:raise ValueError('Incomplete fresh pair')
        for state in pair['state_comparisons']:
            count+=1
            if not all(state[k]['equal'] for k in ['native_before_print','native_after_print','raw_print_stream']) or not state['native_counts_equal'] or not state['membership_equal']:
                raise ValueError('Unresolved pair difference')
    if count!=16:raise ValueError('Missing accepted state')
    print(f'Verified {len(runs)} immutable run/calibration manifests, 9 fresh pairs and16 exact native/print states; no Wordling/NFR005 claim')
    if args.git_ref:print('Verified raw SHA-256/length equality for',git_blobs(args.git_ref),'committed Git blobs')


if __name__=='__main__':main()
