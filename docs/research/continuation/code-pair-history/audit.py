#!/usr/bin/env python3
"""Read-only WP40 original facts/Git audit; no guest or product/history policy."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts/reference'))
import code_pair_history as driver
import native_edits as native
from print_literal import audit as print_audit

RAW_COMMIT='b606fd4707cb7f033b0217a4eb4eee1a7e4f7d11'
RUNNER_SHA='0d02ae3573712e18cc7e67eb82281faf2ddbc1ed79a90a68673fc34b5ac31104'

def need(ok,code,detail):driver.need(ok,code,detail)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def same_facts(a,b):return json.dumps(a,sort_keys=True,separators=(',',':'))==json.dumps(b,sort_keys=True,separators=(',',':'))


def raw_commands(base):
    result=[]
    for line in(base/'qmp-wire.jsonl').read_text().splitlines():
        x=json.loads(line)
        if x['direction']=='tx-buffer':result.append(json.loads(bytes.fromhex(x['raw_hex'])))
    return result


def menu_records(base,case,trace):
    rows=[]
    for h in case['history']:
        screens=[(base/label/'screen.txt').read_text()for label in h['captures']]
        first=[s.splitlines()[0]for s in screens]
        captions=[[line.strip()for line in s.splitlines()if 'Undelete:'in line]for s in screens]
        active=bool(captions[0]);need(active==h['active']and first==h['overlaid_first_lines'],'MenuSemanticChanged','Whole actual menu rows differ from reported observations')
        a,b=h['trace_range'];keys=[k for e in trace[a:b]for k in e.get('key','').split(',')if k]
        expected=['f1']+(['1']if h['restore']else['2']*3+['f1'])if active else['f1']
        need(keys==expected,'HistoryInterleaving','Actual declared browse/Restore/cancel sequence differs')
        need(len(first)==(1 if h['restore']or not active else 4),'MenuExtent','Missing bounded cycle capture')
        if active and not h['restore']:
            need('Undelete:'not in(base/(h['label']+'-returned')/'screen.txt').read_text(),'MenuCancelChanged','Preview did not cancel')
        rows.append({'label':h['label'],'active':active,'restore_performed':h['restore'],
                     'whole_overlaid_rows':first,'whole_modal_captions':captions,
                     'observed_row_period':1 if len(set(first))==1 else 2 if len(first)==4 and first[:2]==first[2:]else None,
                     'entry_count':None,'unobserved_order':None,
                     'scope':'row/caption cycle only; identical hidden/visible rows do not establish absence/count/global stack order'})
    need([x['label']for x in rows]==['seed-only','immediate-target-history','newest-restore','post-restore-history'],
         'MenuSequenceChanged','Required seed/immediate/Restore/post-Restore observations differ')
    need(rows[0]['active']and any('S'in s for s in rows[0]['whole_overlaid_rows']),'SeedChanged','Known prior S not corroborated')
    return rows


def observe(evidence_root=OUT):
    need(sha(ROOT/'scripts/reference/code_pair_history.py')==RUNNER_SHA,'SourceChanged','Frozen original runner changed')
    cases=[];total_reader=0
    for plan in driver.cases():
        samples=[]
        for repetition in [1,2]:
            run_id='wp40-'+plan['id']+'-r'+str(repetition);base=evidence_root/'runs'/run_id
            report=json.loads((base/'run.json').read_text());result=driver.result(base/'run.json');case=report['cases'][0]
            need(case['id']==plan['id']and case['plan']==plan,'CaseChanged','Source/view/gap/action branch differs')
            menus=menu_records(base,case,report['trace'])
            commands=raw_commands(base);label='target-confirmed'if 'question'in case else'target-action'
            captured=[i for i,c in enumerate(commands)if '/'+label+'/'in json.dumps(c)]
            need(captured,'HistoryInterleaving','No actual target capture')
            keys=[c.get('arguments',{}).get('command-line','')for c in commands[max(captured)+1:]if c.get('arguments',{}).get('command-line','').startswith('sendkey ')]
            need(keys and keys[0]=='sendkey f1 80','HistoryInterleaving','First actual key after target capture is not F1')
            if 'question'in case:
                actual=(base/'target-action/screen.txt').read_text().splitlines()[-1]
                need(actual==case['question'],'ConfirmationChanged','Reported original question/footer differs from raw capture')
                text=(base/'target-action/screen.txt').read_text()
                question='Delete Block?'if plan['id']=='closing-block-repair-yes'else'Delete '+('[BOLD]'if plan['target']=='on'else'[bold]')+'? No (Yes)'
                need(question in text,'ConfirmationChanged','Actual original code/block question differs')
            inferred=result['literal_restore'];body=bytes.fromhex(inferred['pre_marker_body_hex_inferred'])
            immediate=driver.literal_gap(body,base/'after-restore-before-any-save',plan['view']=='reveal')
            prex=driver.literal_gap(body,base/'pre-X-no-navigation',plan['view']=='reveal')
            need(immediate['gap']==prex['gap']==inferred['post_restore_reopen_cancel_gap'],
                 'RestoreGapChanged','Actual immediate Restore/pre-X cursor/native marker do not corroborate the same gap')
            info={};native_paths=[]
            for role,path in [('source',case['source']),('marker',case['final']),*[(k,case['interop'][k])for k in ['retrieved','edited','after_print']]]:
                f=base/path;x=native.inspect(native.bounded_native(f),False);native_paths.append(f)
                packet6=next(p for p in x['packets']if p['type']==6)
                info[role]={'path':path,'size':x['size'],'sha256':x['sha256'],'body_hex':x['body_hex'],
                            'body_grammar_refusal':x['body_grammar_refusal'],'indexed_packet6_flag':bytes.fromhex(packet6['hex'])[0],
                            'writer_admission':'not granted by this original-only observation'}
            stream=base/case['interop']['print_stream']
            printed=print_audit(plan['id'],bytes.fromhex(info['after_print']['body_hex']),stream.read_bytes())
            reader=result['actual_read_only_reader'];need(len(reader['files'])==5 and all(x['accepted']is True and x['exact_no_edit_export']is True for x in reader['files']),
                                                       'ReaderPrerequisite','Actual approved Go reader cannot reopen/export a required original artifact')
            total_reader+=len(reader['files'])
            need(report['owned_adapter']['outer_shared_lock_held_through_all_extraction']is True,'CustodyChanged','Shared guard declaration differs')
            need(len(report['resources'])==5,'ResourceChanged','Missing actual stopped resource fingerprints')
            samples.append({'run_id':run_id,'native':info,'menus':menus,'target_gap':result['target_body_gap_proof'],
                            'restored_fragment_hex':inferred['restored_fragment_hex'],'pre_X_body_hex_inferred':body.hex(),
                            'pre_X_export_exists':False,'immediate_restore_gap':immediate,'post_browse_pre_X_gap':prex,
                            'post_X_gap':inferred['post_marker_gap'],'print':printed,
                            'legacy_print_audit_result_retained':result['print'],'reader':reader,
                            'resources':report['resources'],'final_exit_actions':report['owned_adapter']['final_exit_actions']})
        def signature(s):
            return {'native':{k:{p:v[p]for p in ['size','sha256','body_hex','indexed_packet6_flag']}for k,v in s['native'].items()},
                    'menus':s['menus'],'target_gap':s['target_gap'],'fragment':s['restored_fragment_hex'],
                    'restore_gap':s['immediate_restore_gap'],'pre_X':s['post_browse_pre_X_gap'],'print':s['print']}
        need(same_facts(signature(samples[0]),signature(samples[1])),'RepetitionDisagrees','Fresh literal/native/menu/gap/print witnesses differ; no normalization allowed')
        direct=plan['id'].startswith('direct-')
        fact=('newest actual Restore inserts literal prior S; S-overlaid bounded cycles remain after one Restore'if direct else
              'newest actual Restore inserts literal On+Off; prior-S whole preview remains reachable; same bounded cycle reopens after one Restore')
        cases.append({'local_case_id':'WP40-'+plan['id']+'-v1','revision':1,'plan':plan,'samples':samples,
                      'measured_history_fact':fact,'absolute_entry_count':None,'global_history_update_rule':None,
                      'no_unbrowsed_or_uninterrupted_permission':True,'no_repeat_Restore_executed':True})
    return {'cases':cases,'completed_original_guests':18,'actual_reader_artifact_paths':total_reader,
            'scope':'only seeded, pre-browsed, Right-separated exact contexts; no global Add/Skip/Clear/count/order rule',
            'wordling_tested':False,'full_m1_accepted':False}


def git_files(evidence_root,expected):
    process=subprocess.Popen(['git','--no-optional-locks','-C',str(ROOT),'cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    rows=[]
    try:
        for item in expected:
            relative=Path(item['path']);path=evidence_root/relative
            need(not relative.is_absolute()and '..'not in relative.parts and path.resolve().is_relative_to(evidence_root.resolve()),'EvidencePath','Unsafe evidence path')
            repo_path=str((OUT/relative).relative_to(ROOT));process.stdin.write((RAW_COMMIT+':'+repo_path+'\n').encode());process.stdin.flush()
            header=process.stdout.readline().decode().strip().split();need(len(header)==3 and header[1]=='blob','GitCustodyChanged',repo_path)
            raw=process.stdout.read(int(header[2]));need(process.stdout.read(1)==b'\n','GitProtocol','Unexpected blob framing')
            current=path.read_bytes()
            need(current==raw and len(raw)==item['size']and hashlib.sha256(raw).hexdigest()==item['sha256']and header[0]==item['git_blob'],
                 'GitCustodyChanged',repo_path)
            rows.append(item)
    finally:
        process.stdin.close();process.stdout.close();process.wait()
    return len(rows)


def inventory(expected):
    prefix=OUT.relative_to(ROOT).as_posix()+'/'
    result=subprocess.run(['git','--no-optional-locks','-C',str(ROOT),'ls-tree','-rz','--name-only',RAW_COMMIT,'--',prefix+'runs'],check=True,capture_output=True)
    committed=[x.decode().removeprefix(prefix)for x in result.stdout.split(b'\0')if x]
    declared=[x['path']for x in expected]
    need(len(committed)==9252 and sorted(committed)==sorted(declared)and len(set(declared))==len(declared),
         'GitInventoryChanged','Raw custody list must cover every original committed file exactly once')
    return len(committed)


def audit(evidence_root=OUT):
    ledger=json.loads((OUT/'observations.json').read_text())
    need(ledger['raw_commit']==RAW_COMMIT and ledger['executing_runner_sha256']==RUNNER_SHA,'LedgerIdentity','Immutable original identity differs')
    need(ledger['wordling_tested']is False and ledger['full_m1_accepted']is False and ledger['entry_count_and_global_history_policy_unqualified']is True,
         'ScopeChanged','Original-only and unqualified global-history scope changed')
    actual=observe(evidence_root)
    need(same_facts(actual,ledger['observations']),'RecordedSemanticChanged','Actual native/menu/cursor/print findings differ from recorded original facts')
    inventory(ledger['raw_files'])
    verified=git_files(evidence_root,ledger['raw_files'])
    return {'complete_original_guests':18,'fresh_pairs':9,'actual_reader_artifact_paths':90,'raw_Git_files_verified':verified,
            'scope':actual['scope'],'entry_counts_or_global_history_rules_qualified':False,
            'wordling_tested':False,'full_m1_accepted':False,'raw_commit':RAW_COMMIT}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--evidence-root',type=Path,default=OUT);a=p.parse_args()
    try:print(json.dumps(audit(a.evidence_root),indent=2));return 0
    except Exception as e:print(json.dumps({'result':'audit-rejected','code':getattr(e,'code',type(e).__name__),'error':str(e),'full_m1_accepted':False}));return 1


if __name__=='__main__':sys.exit(main())
