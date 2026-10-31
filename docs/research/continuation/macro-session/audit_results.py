#!/usr/bin/env python3
"""Offline WP38 artifact/native/interaction audit. Never imports/starts a guest."""
from pathlib import Path
import hashlib
import json
import re
import struct
import sys
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'docs/research/continuation/macro-session'
sys.path.insert(0,str(ROOT/'scripts/reference'))
from document import plain_merge

SELECTED={'name-cancel':'wp38-name-cancel-02','run-doc1':'wp38-run-doc1-01',
          'repeat-doc2':'wp38-repeat-doc2-02','missing-name':'wp38-missing-name-02',
          'pending-save':'wp38-pending-save-01','internal-cancel':'wp38-internal-cancel-02',
          'stop-default':'wp38-stop-default-02','stop-on':'wp38-stop-on-02','stop-off':'wp38-stop-off-01'}
DOC1,DOC2='D1SENT DIRTY1','D2SENT DIRTY2'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(condition,message):
    if not condition:raise AssertionError(message)
def screen(case,label):return (case/label/'screen.txt').read_text()
def body(s):return s.splitlines()[0]
def beats(s):
    match=re.fullmatch(re.escape(DOC1+'MSLIVE')+r'(\.*)(?:USERREADY)?',body(s))
    check(match is not None,'Unexpected/possibly wrapped heartbeat body')
    check(all(not x.strip()for x in s.splitlines()[1:-1]),'Wrapped/extra document rows cannot prove stop')
    check(len(body(s))<64 and len(match[1])<=16,'Heartbeat region may wrap/saturate; no stop acceptance')
    return len(match[1])
def tx_commands(case):
    result=[]
    for line in (case/'qmp-wire.jsonl').read_text().splitlines():
        item=json.loads(line);raw=bytes.fromhex(item['raw_hex'])
        if item['direction']=='tx-buffer':result.append((item,json.loads(raw)))
        elif raw:json.loads(raw)  # includes raw greetings/events, without modifying bytes
    return result


def main():
    files=0;all_runs=[];rows=[]
    for stem in ['series','rerun']:
        execution=json.loads((OUT/(stem+'-execution.json')).read_text())
        check(sha(OUT/(stem+'_driver.py'))==execution['controller_sha256'],'Executing controller changed')
    for path in sorted((OUT/'runs').glob('*/run.json')):
        report=json.loads(path.read_text());base=path.parent
        check(report['scope']=='original-reference-only'and report['wordling_tested']is False,'Scope drift')
        check(len(report['results'])==2 and [x['repetition']for x in report['results']]==[1,2],'Fresh pair incomplete')
        check(report['master_before']==report['master_after'],'Master changed')
        check(report['lock_released_before_offline_audit']is True,'Lock held during audit')
        for x in report['sources']:
            p=base/'runner-source'/x['path'];check(sha(p)==x['sha256'],'Executing source archive changed')
        for x in report['artifacts']:
            p=base/x['path'];check(p.resolve().is_relative_to(base.resolve())and p.stat().st_size==x['size']and sha(p)==x['sha256'],'Raw evidence changed: '+str(p));files+=1
        check(all(r['guest_stopped']is True for r in report['results']),'Unstopped guest')
        all_runs.append({'run_id':report['run_id'],'cases':[{'id':r['id'],'outcome':r['outcome'],'error':r.get('error')}for r in report['results']]})
    check(len(all_runs)==15 and sum(len(x['cases'])for x in all_runs)==30,'Historical calibration/run missing')
    for recipe,run_id in SELECTED.items():
        report=json.loads((OUT/'runs'/run_id/'run.json').read_text());base=OUT/'runs'/run_id
        for sample in report['results']:
            case=base/sample['id'];commands=tx_commands(case)
            f1=[i for i,(_,cmd)in enumerate(commands)if cmd.get('arguments',{}).get('command-line')=='sendkey f1 80']
            observed={'recipe':recipe,'run_id':run_id,'sample':sample['id'],'retained_outcome':sample['outcome'],'operator_f1_count':len(f1),'limits':'original-only bounded fixture; no parent/full scenario/product/physical closure'}
            if recipe not in ['name-cancel','pending-save']:
                if (case/'macro-name-exact-before-return/screen.txt').exists():
                    exact=screen(case,'macro-name-exact-before-return');observed['exact_pre_submit_name']=exact.splitlines()[-1]
                    check(observed['exact_pre_submit_name'].startswith('Macro: C:'),'Name not proved')
                else:
                    check(recipe in ['run-doc1','stop-off'],'Missing corrected exact invocation capture')
                    observed['invocation_binding']='Pinned unique input WPM + visible fixture effect + typed path/raw QMP; original earlier protocol retained'
            if recipe=='stop-off':
                a,b,c,d=[screen(case,x)for x in ['running-heartbeat-a','running-heartbeat-b','after-user-f1','manual-recovery-after-user-f1']]
                check(beats(b)>beats(a)>=1 and beats(d)>beats(c)>=beats(b),'OFF did not continue within observed window')
                check('USERREADY'not in body(d)and len(f1)==1,'OFF recovery/source disambiguation')
                observed.update(status='bounded-original-continuation-after-operator-F1',heartbeat_counts=list(map(beats,[a,b,c,d])),native_after='unavailable by intentional host containment; no native partial proof invented')
            else:
                native={n:plain_merge((case/(n+'.WP5')).read_bytes())for n in ['D1AFTER','D2AFTER']}
                e1=DOC1+('ABC'if recipe=='run-doc1'else'INTERNALMSTAIL'if recipe=='internal-cancel'else'')
                e2=DOC2+('ABCABCABC'if recipe=='repeat-doc2'else'')
                if recipe in ['stop-default','stop-on']:
                    a,b,c,d=[screen(case,x)for x in ['running-heartbeat-a','running-heartbeat-b','after-user-f1','manual-recovery-after-user-f1']]
                    check(beats(b)>=beats(a)+2 and beats(a)>=1,'Running pre-F1 proof incomplete')
                    check(beats(c)==beats(d)and body(d)==DOC1+'MSLIVE'+'.'*beats(c)+'USERREADY','Recovery body not exact')
                    check(len(f1)==1,'Operator F1 not separate')
                    beat_capture=max(i for i,(_,cmd)in enumerate(commands)if 'running-heartbeat-b/'in json.dumps(cmd))
                    check(f1[0]>beat_capture,'F1 preceded live witness')
                    e1=body(d);observed['heartbeat_counts']=list(map(beats,[a,b,c,d]))
                    observed['exact_expected_native_text']=e1
                check(native['D1AFTER']['ascii_text']==e1 and native['D2AFTER']['ascii_text']==e2,'Exact native target/other-buffer mismatch')
                if recipe=='missing-name':
                    msg=screen(case,'missing-name-raw-settled').splitlines()[-1]
                    check(msg.startswith('ERROR: File not found -- ')and msg.endswith('M38NONE.WPM'),'Unexpected missing-name error')
                    observed['exact_error']=msg;observed['operator_recovery_keys']=len(f1)
                if recipe=='internal-cancel':
                    check(len(f1)==0 and body(screen(case,'stored-cancel-word-no-user-f1'))==e1,'Stored Cancel conflated with operator F1')
                    observed['stored_word']='8020; INTERNALMSTAIL continues, no operator F1'
                if recipe=='pending-save':
                    check('Document to be saved:'in screen(case,'pending-save-after-macro-key'),'Save modal changed')
                observed.update(status='bounded-original-observation-audited',native=native)
            rows.append(observed)
    # Re-extracted authored WPM sources must remain exact input bytes in both series.
    post=json.loads((OUT/'post-extraction/extraction.json').read_text())
    for item in post['authored_WPM_extractions']:
        check(sha(OUT/item['path'])==item['sha256']==item['input_sha256'],'Initial WPM changed')
    rerun=json.loads((OUT/'rerun-execution.json').read_text())
    for r in rerun['results']:
        input_file=OUT/'runs'/r['run_id']/'input/M38.WPM'
        for item in r.get('stopped_macro_exports',[]):check(sha(OUT/item['path'])==item['sha256']==sha(input_file),'Rerun WPM changed')
    result={'scope':'original-reference-only','wordling_tested':False,'all_raw_runs_retained':all_runs,
            'fresh_guest_count':sum(len(x['cases'])for x in all_runs),'raw_artifacts_verified':files,
            'selected_pair_count':len(SELECTED),'selected_observations':rows,
            'full_m1_accepted':False,'physical_input_qualified':False,'parent_groups_closed':False}
    (OUT/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    suite=ET.Element('testsuite',name='WP38-bounded-original-audit',tests=str(len(rows)))
    for row in rows:
        test=ET.SubElement(suite,'testcase',name=row['run_id']+'/'+row['sample'])
        if row['recipe']=='stop-off':ET.SubElement(test,'skipped',message='Original continuation observed; native AFTER unavailable under host containment, not a stop pass')
    ET.indent(suite);ET.ElementTree(suite).write(OUT/'audit.xml',encoding='utf-8',xml_declaration=True)
    print(json.dumps({'fresh_guests':result['fresh_guest_count'],'raw_artifacts_verified':files,'selected_pairs':len(SELECTED),'selected_observations':len(rows),'product_tested':False,'full_m1_accepted':False}))


if __name__=='__main__':main()
