#!/usr/bin/env python3
"""Independently assert exact bodies/text of the authored advanced native outputs."""
import argparse
import hashlib
import json
from pathlib import Path
from document import prefix, plain_merge
from qmp import ROOT

BODIES={
    'CMD51-204':{'DELETED.WP5':b'AD'},
    'CMD51-045':{'DELETED.WP5':b'AD','RESTORED.WP5':b'ABCD'},
    'CMD51-205':{'FLOWOUT.WP5':b'TRUEFALSETAIL'},
    'CMD51-178':{'ERROROUT.WP5':b'BEFOREREADY'},
    'CMD51-206':{'ERROROUT.WP5':b'BEFOREHANDLED'},
    'CMD51-210':{'ERROROUT.WP5':b'HANDLED'}}
MERGES={
    'CMD51-207':(1,'Hello Alice\n\fHello Bob\n'),
    'CMD51-208':(0,'Hello Alice\nHello Bob\n'),
    'CMD51-209':(1,'FILLED Alice\fEMPTY Bob')}


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('run_ids',nargs='+');p.add_argument('--output',required=True,type=Path)
    a=p.parse_args()
    if a.output.exists():raise FileExistsError('Existing evidence is immutable')
    checks=[];inputs=[]
    for run_id in a.run_ids:
        directory=ROOT/'docs/research/reference-runs'/run_id
        manifest=directory/'run.json';run=json.loads(manifest.read_text())
        if run['scope']!='original-reference-only' or run['wordling_tested']:
            raise ValueError('Expected original-reference-only evidence')
        cases={r['case_id']:r for r in run['results']}
        if any(r['result']!='observed-matches-smoke-expectations' for r in cases.values()):
            raise ValueError('Run contains an unsuccessful recipe')
        inputs.append({'run_id':run_id,'manifest_sha256':sha(manifest)})
        for case_id in sorted(set(BODIES)|set(MERGES)):
            names=BODIES.get(case_id,{'MERGED.WP5':None})
            for filename,expected in names.items():
                f=directory/case_id/filename;data=f.read_bytes();info=prefix(data)
                recorded=next(x for x in cases[case_id]['native_outputs'] if Path(x['path']).name==filename)
                if sha(f)!=recorded['sha256']:raise ValueError('Native evidence changed')
                item={'run_id':run_id,'case_id':case_id,'path':str(f.relative_to(ROOT)),
                      'sha256':sha(f),'document_offset':info['document_offset']}
                if expected is not None:
                    body=data[info['document_offset']:]
                    item.update(expected_body_hex=expected.hex(),actual_body_hex=body.hex(),passed=body==expected)
                else:
                    count,text=MERGES[case_id];actual=plain_merge(data)
                    item.update(expected_text=text,actual_text=actual['ascii_text'],
                                expected_hard_pages=count,actual_hard_pages=actual['hard_page_count'],
                                passed=actual['ascii_text']==text and actual['hard_page_count']==count)
                checks.append(item)
    report={'scope':'Exact original-app authored-fixture bodies only; no Wordling conformance claim',
            'inputs':inputs,'checks':checks,'all_passed':all(c['passed'] for c in checks),
            'runner_sha256':sha(Path(__file__)),
            'inspector_sha256':sha(Path(__file__).with_name('document.py'))}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(len(checks),'native body/text assertions; all passed:',report['all_passed'])
    if not report['all_passed']:raise SystemExit(1)


if __name__=='__main__':main()
