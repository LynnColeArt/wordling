#!/usr/bin/env python3
"""WP43 POST-RUN read-only audit. Never a guest source or constructor."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'scripts/reference'))
import native_genesis as g
import native_edits as n
RAW_COMMIT='1312eb7bec11dbe83def789031d9cc0083fdb9bf'
DRIVER_SHA='2e1b6cccc4275a81ca6f27e7eb5525e99655c8279e8e777924f5ef86347c64dc'
PREFIX=b'\r'+b'\r\n'*6
SUFFIX=b'\r'+b'\r\n'*60
PRINT=PREFIX+b' '*10+b'G43ASCIIZ'+SUFFIX


def print_audit(raw):
    g.need(raw==PRINT,'PrintChanged','Exact full153-byte selected-profile G43ASCIIZ control/ink stream required; no normalization')
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'hex':raw.hex(),
            'scope':'six measured one-line Standard Printer outputs only; no physical metrics or generic formatter'}


def facts(evidence_root=OUT):
    g.need(g.sha(ROOT/'scripts/reference/native_genesis.py')==DRIVER_SHA,'ExecutingSourceChanged','Archived executing runner must stay unchanged')
    cases=[];first=[];reader_count=0;prints=[]
    for plan in g.cases():
        base=evidence_root/'runs'/('wp43-genesis-01-'+plan['id']);result=g.result(base/'run.json')
        report=json.loads((base/'run.json').read_text());samples=[]
        for sample,row in zip(result['observations'],report['results']):
            d=base/('r'+str(sample['repetition']));reader_count+=len(sample['actual_reader'])
            if plan['first_save_name']:
                native=d/(plan['first_save_name']+'.WP5');raw=n.bounded_native(native);info=n.inspect(raw,False)
                first.append({'case':plan['id'],'repetition':sample['repetition'],'path':str(native.relative_to(evidence_root)),
                              'size':len(raw),'body_offset':info['body_offset'],'body_hex':info['body_hex'],
                              'prefix_sha256':hashlib.sha256(raw[:info['body_offset']]).hexdigest()})
            printed=None
            if plan['interop']:
                raw=(d/'G43PRINT.PRN').read_bytes();printed=print_audit(raw);prints.append(printed)
            # Keep only metadata from private SET comparison; never publish private bytes.
            a=row['settings_before']['sha256'];b=row['settings_after']['sha256']
            samples.append({'repetition':sample['repetition'],'native':sample['files'],'absence':sample['absent'],
                            'actual_state_ledger':sample['actual_state_ledger'],'reader':sample['actual_reader'],
                            'literal_lifecycle_differences':sample['literal_lifecycle_differences'],'print':printed,
                            'resources_before':row['resources_before'],'resources_after':row['resources'],
                            'private_SET_before_sha256':a,'private_SET_after_sha256':b,'private_SET_changed':a!=b,
                            'normal_exit_actions':row['exit_actions'],'owned_process':row['owned_process'],'stop_proof':row['stop_proof']})
        # Compare literal native findings across fresh repetitions, without dropping differing bytes.
        sig=lambda s:[{'path':f['path'],'size':f['field_report']['size'],'sha256':f['field_report']['sha256'],
                        'body_hex':f['field_report']['body_hex']}for f in s['native']]
        g.need(g.same(sig(samples[0]),sig(samples[1])),'PairDisagrees','Fresh native witnesses differ; no normalization allowed')
        cases.append({'local_id':'WP43-'+plan['id']+'-v1','revision':1,'plan':plan,'samples':samples,
                      'scope':'bounded original-only branch; not complete command/lesson/requirement acceptance'})
    g.need(len(first)==8 and reader_count==20 and len(prints)==6,'MissingWitness','Exact10-guest/20-native/6-print matrix required')
    prefix={x['prefix_sha256']for x in first};g.need(len(prefix)==1,'PrefixDisagrees','Observed first-save prefixes differ')
    baseline=next(c for c in cases if c['plan']['id']=='empty-first-save')['samples'][0]['native'][0]['field_report']
    return {'schema':1,'cases':cases,'first_native_images':first,'first_prefix_sha256':next(iter(prefix)),
            'first_prefix_equality_is_observation_not_universal_default':True,'empty_native_bytes':324,
            'field_table':baseline['fields'],'first_prefix_unmapped':baseline['unmapped'],
            'actual_original_guests':10,'actual_reader_paths':reader_count,'actual_print_streams':len(prints),
            'universal_defaults_established':False,'constructor_ready':False,'wordling_tested':False,'full_m1_accepted':False}


def git_seals(rows,evidence_root=OUT):
    prefix=OUT.relative_to(ROOT).as_posix()+'/'
    tree=subprocess.check_output(['git','ls-tree','-rz','--name-only',RAW_COMMIT,'--',prefix+'runs'])
    committed=[p.decode().removeprefix(prefix)for p in tree.split(b'\0')if p]
    g.need(len(committed)==2862 and sorted(committed)==sorted(r['path']for r in rows),
           'RawInventoryChanged','Raw manifest must cover every original committed file exactly once')
    process=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    try:
        for row in rows:
            relative=Path(row['path']);p=evidence_root/relative
            g.need(not relative.is_absolute()and'..'not in relative.parts and p.resolve().is_relative_to(evidence_root.resolve()),'EvidencePath','Unsafe raw path')
            process.stdin.write((RAW_COMMIT+':'+prefix+row['path']+'\n').encode());process.stdin.flush()
            header=process.stdout.readline().decode().strip().split();g.need(len(header)==3 and header[1]=='blob','RawGitChanged',row['path'])
            raw=process.stdout.read(int(header[2]));g.need(process.stdout.read(1)==b'\n','GitFraming','Unexpected blob framing')
            g.need(p.read_bytes()==raw and len(raw)==row['size']and hashlib.sha256(raw).hexdigest()==row['sha256']and header[0]==row['git_blob'],'RawGitChanged',row['path'])
    finally:process.stdin.close();process.stdout.close();process.wait()
    return len(rows)


def audit(evidence_root=OUT):
    ledger=json.loads((OUT/'analysis/genesis-ledger.json').read_text())
    g.need(ledger['raw_commit']==RAW_COMMIT and ledger['executing_driver_sha256']==DRIVER_SHA,'LedgerIdentity','Original source/Git identity changed')
    actual=facts(evidence_root);g.need(g.same(actual,ledger['facts']),'SemanticFactsChanged','Actual field/state/native/print facts differ from recorded ledger')
    count=git_seals(ledger['raw_files'],evidence_root)
    return {'actual_guests':10,'reader_paths':20,'print_streams':6,'Git_raw_files_verified':count,
            'first_prefix_bytes':324,'constructor_ready':False,'wordling_tested':False,'full_m1_accepted':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--evidence-root',type=Path,default=OUT);a=p.parse_args()
    try:print(json.dumps(audit(a.evidence_root),indent=2))
    except Exception as e:print(json.dumps({'result':'refused','code':getattr(e,'code',type(e).__name__),'detail':str(e)}));raise SystemExit(1)
