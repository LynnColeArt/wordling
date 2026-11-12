#!/usr/bin/env python3
"""Read-only independent WP39 native/state/ledger/Git audit; never starts a guest."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'docs/research/continuation/macro-quit'
sys.path.insert(0,str(ROOT/'scripts/reference'))
import macro_quit as probe
from document import plain_merge

RAW_COMMIT='d7f1d3b572ed98d325d8a160d1a287fb83e3a124'
RUNNER_SHA='2e2f60d522b7b49c508856efb31e352c565584de3001a70d193dd1dd2b7e0915'
INITIAL_SHA='492cc3d6dbfc4bf67e9fc9015f3231ef8bbe8e04bc5733987b2abc82a8a27a35'


def require(condition,code,detail):probe.require(condition,code,detail)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def audit(evidence_root):
    ledger=json.loads((OUT/'observations.json').read_text())
    require(ledger['wordling_tested']is False and ledger['full_m1_accepted']is False and ledger['parent_groups_closed']is False,
            'ScopeChanged','Original-only ledger scope changed')
    require(ledger['raw_commit']==RAW_COMMIT and ledger['executing_runner_sha256']==RUNNER_SHA,
            'LedgerIdentity','Original immutable raw/source identity differs')
    require(sha(ROOT/'scripts/reference/macro_quit.py')==RUNNER_SHA,'SourceChanged','Executing runner changed after originals')
    require([(c['local_case_id'],c['revision'],c['case'],c['run_id'],c['baseline_id'])for c in ledger['cases']]==
            [('WP39-NQ-ROOT-v1',1,'root','wp39-root-02','wp51-dos-us-1992-03-09'),
             ('WP39-NQ-CHILD-v1',1,'nested','wp39-nested-02','wp51-dos-us-1992-03-09')],
            'CaseChanged','Case/revision/baseline identity differs')
    verified=[]
    # Compare independently recorded actual findings before custody checks. Rehashed
    # internally consistent alternative branches cannot rewrite this original ledger.
    for case in ledger['cases']:
        result=probe.result(evidence_root/'runs'/case['run_id']/'run.json')
        require(result['case']==case['case']and result['observations']==case['observations']
                and result['normal_context_qualified']is True,
                'LedgerSemanticChanged','Native/state branch differs from recorded original facts')
        base=evidence_root/'runs'/case['run_id'];report=json.loads((base/'run.json').read_text())
        expected_assets=probe.case_manifest(case['case'])['assets']
        require(case['native_sources']==expected_assets,'InputChanged','Ledger native source/spans differ')
        names=['D1BASE.WP5','D2BASE.WP5','QBEFORE.WP5','QAFTER.WP5','QOTHER.WP5']+[x['name']for x in expected_assets]
        first,second=[base/x['id']for x in report['results']]
        require(all((first/name).read_bytes()==(second/name).read_bytes()for name in names),
                'RepetitionDisagrees','Deterministic original native bytes do not agree')
        require(report['results'][0]['qemu_argv']!=report['results'][1]['qemu_argv'],
                'FreshnessChanged','Fresh guests share identical scratch argv')
        for row in report['results']:
            require('WP 5.1   03/09/92'in(base/row['id']/'selected-release/screen.txt').read_text(),
                    'BaselineChanged','Actual displayed reference release differs')
        verified.append(result)
    # Complete outputs and transitive runner sources must match actual committed
    # original bytes, not only freshly asserted hashes in the submitted envelope.
    for item in ledger['raw_files']:
        relative=Path(item['path']);path=evidence_root/relative
        require(not relative.is_absolute()and '..'not in relative.parts and path.resolve().is_relative_to(evidence_root.resolve()),
                'UnsafeEvidencePath','Evidence path escapes its root')
        raw=path.read_bytes()
        original=subprocess.check_output(['git','--no-optional-locks','-C',str(ROOT),'cat-file','blob',
                                          RAW_COMMIT+':'+str((OUT/relative).relative_to(ROOT))])
        require(raw==original and len(raw)==item['size']and hashlib.sha256(raw).hexdigest()==item['sha256']
                and probe.blob_id(raw)==item['git_blob'],'GitCustodyChanged',item['path'])
    # The first two guests remain incomplete despite useful native observations.
    first=evidence_root/'runs'/ledger['initial_incomplete_run'];initial=json.loads((first/'run.json').read_text())
    require(len(initial['results'])==2 and all(x['outcome']=='error'and x['guest_stopped']is True for x in initial['results']),
            'DiagnosticPromotion','Initial failed root guests must remain incomplete')
    require(sha(first/'runner-source/scripts/reference/macro_quit.py')==INITIAL_SHA,
            'SourceChanged','Initial archived executing source changed')
    require(initial['master_before']==initial['master_after'],'MasterChanged','Initial master changed')
    settings=[]
    for name in [ledger['initial_incomplete_run']]+[x['run_id']for x in ledger['cases']]:
        base=evidence_root/'runs'/name;report=json.loads((base/'run.json').read_text())
        require(report['master_before']==report['master_after']and report['oracle_released_before_offline_audit']is True,
                'IncompleteCustody','Master/release mismatch')
        for row in report['results']:
            for key in ['settings_before','settings_after']:
                item=row[key];p=Path(item['private_path'])
                require(sha(p)==item['sha256'],'SettingsChanged','Retained private profile changed')
                settings.append({'sha256':item['sha256'],'size':p.stat().st_size,'publication':'metadata only'})
    # Original incomplete native observations are independently decoded, not promoted.
    initial_native=[]
    for row in initial['results']:
        case=first/row['id']
        data={name:plain_merge((case/(name+'.WP5')).read_bytes())['ascii_text']for name in ['QBEFORE','QAFTER','QOTHER']}
        require(data=={'QBEFORE':probe.DOC1+'R39','QAFTER':probe.DOC1+'R39READY','QOTHER':probe.DOC2},
                'DiagnosticChanged','Initial native observations changed')
        initial_native.append({'id':row['id'],'native':data,'complete_witness':False})
    return {'scope':probe.SCOPE,'complete_original_observations':4,'incomplete_diagnostic_observations':2,
            'verified_raw_Git_files':len(ledger['raw_files']),'raw_commit':RAW_COMMIT,
            'qualified_cases':verified,'initial_native_diagnostics':initial_native,'private_settings':settings,
            'source_frozen':True,'wordling_tested':False,'full_m1_accepted':False,'parent_groups_closed':False}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--evidence-root',type=Path,default=OUT)
    args=p.parse_args()
    try:
        print(json.dumps(audit(args.evidence_root),indent=2));return 0
    except Exception as e:
        print(json.dumps({'result':'audit-rejected','code':getattr(e,'code',type(e).__name__),
                          'error':str(e),'full_m1_accepted':False}));return 1


if __name__=='__main__':sys.exit(main())
