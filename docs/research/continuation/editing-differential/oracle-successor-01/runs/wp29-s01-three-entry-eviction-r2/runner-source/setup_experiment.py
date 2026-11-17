#!/usr/bin/env python3
"""Change only a copied printer FAT timestamp; observe original WP's SET cache."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import struct
import subprocess
from inspect_setup import FAT16, inspect
import guest
from qmp import ROOT, QMP


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('experiment_id')
    a=parser.parse_args()
    if not a.experiment_id.replace('-','').isalnum():
        parser.error('Use an alphanumeric/hyphen experiment ID')
    work=ROOT/'research/cache/reference/setup-experiments'/a.experiment_id
    out=ROOT/'docs/research/reference-environment'/a.experiment_id
    if work.exists() or out.exists():raise FileExistsError('Choose a new experiment ID')
    work.mkdir(parents=True);out.mkdir()
    report={'scope':'Original SET cache investigation; not Wordling conformance',
            'source_locator':{'source_id':'SDK51','section':'Appendix A, Default Printer packet 54h','printed_page':'AP8','pdf_page':507},
            'original':inspect(guest.MASTER/'harddisk.img'),
            'independent_rebuild':inspect(ROOT/'research/cache/reference/build/rebuild-02/harddisk.img'),
            'trials':[]}
    original_master,original_profile=guest.MASTER,guest.PROFILE
    for name,changed in [('control',False),('printer-time-only',True),('printer-time-reselect',True)]:
        master=work/name/'master';master.mkdir(parents=True)
        for f in ['boot.img','harddisk.img']:shutil.copyfile(original_master/f,master/f)
        capture=master/'release-identification';capture.mkdir()
        shutil.copyfile(ROOT/'docs/research/reference-environment/release-identification.txt',capture/'screen.txt')
        before=(master/'harddisk.img').read_bytes()
        fs=FAT16(master/'harddisk.img');offset,_=fs.entry('WP51/STANPRIN.PRS')
        if changed:
            data=bytearray(before);struct.pack_into('<H',data,offset+22,0x60E0) #12:07:00
            (master/'harddisk.img').write_bytes(data)
        after=(master/'harddisk.img').read_bytes()
        differences=[{'offset':i,'before':b,'after':c} for i,(b,c) in enumerate(zip(before,after)) if b!=c]
        subprocess.run(['python3',str(ROOT/'scripts/reference/fingerprint.py'),str(master),str(work/name/'profile')],check=True,capture_output=True)
        guest.MASTER,guest.PROFILE=master,work/name/'profile/environment.json'
        (out/name).mkdir()
        shutil.copyfile(guest.PROFILE,out/name/'environment.json')
        trial={'name':name,'mutation_byte_differences':differences,'before_launch':inspect(master/'harddisk.img')}
        run=work/name/'run'
        try:
            trial['qemu_argv']=guest.start(run)
            with QMP() as q:
                if name == 'printer-time-reselect':
                    q.key('shift-f7');q.wait_for('Select Printer');q.key('s')
                    q.wait_for('Print: Select Printer');q.capture(out/name/'before-selection')
                    q.key('1');q.wait_for('Options');q.key('f7');q.wait_for('Doc 1')
                    trial['printer_action_trace']=['Shift+F7','S: Select Printer','1: Select current Standard Printer','F7: return to document']
                q.key('f7');q.wait_for('Save document?');q.key('n');q.wait_for('Exit WP?');q.key('y')
                q.wait_for('C:\\WP51>');q.capture(out/name)
            trial['exit_trace']=['F7','Save document? -> n','Exit WP? -> y','C:\\WP51>']
        finally:guest.stop()
        trial['after_exit']=inspect(run/'harddisk.img')
        setup_before=FAT16(master/'harddisk.img').read_file('WP51/WP{WP}.SET')
        setup_after=FAT16(run/'harddisk.img').read_file('WP51/WP{WP}.SET')
        trial['setup_byte_differences']=[{'offset':i,'before':b,'after':c} for i,(b,c) in enumerate(zip(setup_before,setup_after)) if b!=c]
        trial['setup_length_unchanged']=len(setup_before)==len(setup_after)
        report['trials'].append(trial)
        (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    guest.MASTER,guest.PROFILE=original_master,original_profile
    report['checks']={
        'same_printer_contents':len({report['original']['printer_sha256'],report['independent_rebuild']['printer_sha256'],*[t['after_exit']['printer_sha256'] for t in report['trials']]})==1,
        'control_cache_unchanged':report['trials'][0]['before_launch']['cached_timestamp']==report['trials'][0]['after_exit']['cached_timestamp'],
        'timestamp_mutation_confined_to_fat_time':bool(report['trials'][1]['mutation_byte_differences']) and all(offset+22<=d['offset']<offset+24 for d in report['trials'][1]['mutation_byte_differences']),
        'idle_session_does_not_refresh_cache':report['trials'][1]['before_launch']['cached_timestamp']==report['trials'][1]['after_exit']['cached_timestamp'],
        'selection_refreshes_cache_to_fat_time':report['trials'][2]['after_exit']['cached_matches_printer_timestamp'] and report['trials'][2]['after_exit']['cached_timestamp']['time_word']==0x60E0,
        'selection_changes_only_cached_time':bool(report['trials'][2]['setup_byte_differences']) and all(1366<=d['offset']<1368 for d in report['trials'][2]['setup_byte_differences']) and report['trials'][2]['setup_length_unchanged'],
        'master_unchanged':inspect(original_master/'harddisk.img')['image_sha256']==report['original']['image_sha256']}
    report['capture_artifacts']=[{'path':str(f.relative_to(ROOT)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'size':f.stat().st_size} for f in sorted(out.rglob('*')) if f.is_file() and f.name!='report.json']
    report['runner_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    report['inspector_sha256']=hashlib.sha256((ROOT/'scripts/reference/inspect_setup.py').read_bytes()).hexdigest()
    for filename in ['setup_experiment.py','inspect_setup.py','guest.py','qmp.py','fingerprint.py']:
        target=out/'runner-source'/filename;target.parent.mkdir(exist_ok=True)
        shutil.copyfile(ROOT/'scripts/reference'/filename,target)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['checks'],indent=2))
    if not all(report['checks'].values()):raise SystemExit(1)


if __name__=='__main__':main()
