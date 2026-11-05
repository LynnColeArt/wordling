#!/usr/bin/env python3
"""Compare authored native outputs from two successful original-app runs."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
from qmp import ROOT


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('first');p.add_argument('second');p.add_argument('output',type=Path)
    a=p.parse_args()
    if a.output.exists():raise FileExistsError('Existing comparisons are immutable')
    runs=[json.loads((ROOT/'docs/research/reference-runs'/name/'run.json').read_text()) for name in [a.first,a.second]]
    for run in runs:
        if any(r['result']!='observed-matches-smoke-expectations' for r in run['results']):
            raise ValueError('Comparison requires successful run recipes')
    indexed=[{(r['case_id'],Path(f['path']).name):f for r in run['results'] for f in r.get('native_outputs',[])} for run in runs]
    if indexed[0].keys()!=indexed[1].keys():raise ValueError('Different output sets')
    comparisons=[]
    for key,meta in indexed[0].items():
        other=indexed[1][key]
        paths=[ROOT/f['path'] for f in [meta,other]]
        data=[f.read_bytes() for f in paths]
        for content,expected in zip(data,[meta,other]):
            if hashlib.sha256(content).hexdigest()!=expected['sha256']:raise ValueError('Evidence changed')
        comparisons.append({'case_id':key[0],'filename':key[1],'paths':[f['path'] for f in [meta,other]],
                            'sha256':[f['sha256'] for f in [meta,other]],'byte_identical':data[0]==data[1],
                            'size':len(data[0]),'prefix_hex':data[0][:16].hex(),
                            'document_offset':struct.unpack_from('<I',data[0],4)[0],
                            'product_type':data[0][8],'file_type':data[0][9],
                            'stored_version_bytes':list(data[0][10:12])})
    report={'scope':'Repeated original-app scratch output only; no Wordling round-trip or format implementation claim',
            'runs':[a.first,a.second],'outputs':comparisons,'all_byte_identical':all(f['byte_identical'] for f in comparisons)}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(len(comparisons),'outputs; all byte-identical:',report['all_byte_identical'])
    if not report['all_byte_identical']:raise SystemExit(1)


if __name__=='__main__':main()
