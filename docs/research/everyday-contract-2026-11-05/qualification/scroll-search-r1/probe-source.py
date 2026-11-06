#!/usr/bin/env python3
"""Narrow fresh-copy Reveal scrolling and transient-search qualification."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
from run import ROOT, BASE, perform, configure, digest, guest, qmp

private_master = ROOT / 'research/cache/reference/wp78-flow-fixture-master'
original = ROOT / 'research/cache/reference/master'
fixture = BASE / 'flow-reliable/exports/FLOW.WP'
profile = json.loads((ROOT/'docs/research/reference-environment/environment.json').read_text())
if not private_master.exists():
    assert digest(original/'harddisk.img') == profile['master_disk_sha256']
    assert digest(original/'boot.img') == profile['master_boot_sha256']
    private_master.mkdir()
    for name in ['harddisk.img','boot.img']:
        shutil.copyfile(original/name,private_master/name)
    subprocess.run(['mcopy','-i',str(private_master/'harddisk.img')+'@@1048576',str(fixture),'::/OUT/FLOW.WP'],check=True)
    profile['parent_profile_id']=profile['profile_id']; profile['profile_id']+='-authored-flow-fixture'
    profile['master_disk_sha256']=digest(private_master/'harddisk.img')
    profile['added_fixture']={'path':'C:\\OUT\\FLOW.WP','source':str(fixture.relative_to(ROOT)),'sha256':digest(fixture),'change':'Only add authored original native document to OUT; no app/resource/settings changes.'}
    (private_master/'profile.json').write_text(json.dumps(profile,indent=2)+'\n')
guest.MASTER=private_master;guest.PROFILE=private_master/'profile.json'
run=sys.argv[1]
perform(run,[['start'],['key','f3'],['wait','03/09/92'],['capture','01-release'],['key','ret,shift-f10'],['wait','Document to be retrieved:'],['type','C:\\OUT\\FLOW.WP'],['key','ret'],['wait','A faithful reconstruction'],['capture','02-retrieved'],['key','alt-f3'],['wait','Reveal Codes to restore'],['capture','03-reveal-start'],['key','pgdn'],['wait','Pg 2'],['capture','04-reveal-page-two'],['key','pgdn'],['wait','Pg 3'],['capture','05-reveal-page-three'],['key','pgup'],['wait','Pg 2'],['capture','06-reveal-page-up'],['key','home,home,down'],['wait','LAST PAGE alpha EDIT MORE'],['capture','07-reveal-end'],['top'],['repeat-key','down',14],['capture','08-reveal-line-scroll'],['key','alt-f3'],['capture','09-normal-restored'],['top'],['key','f2'],['wait','Srch:'],['type','zzzzmissing'],['capture','10-search-entry']])
out,_=configure(run)
(out/'probe-source.py').write_bytes(Path(__file__).read_bytes())
# Capture immediately after dispatch then bounded successive settled VRAM/pixels;
# retain every frame, not only a selected message.
with qmp.QMP() as q:
    start=time.monotonic();q.hmp('sendkey f2 80')
    samples=[]
    for n in range(8):
        time.sleep(.04 if n==0 else .10)
        label=f'11-not-found-burst-{n:02d}'
        screen=q.capture(out/label)
        samples.append({'path':label,'elapsed_host_seconds':time.monotonic()-start,'text':screen})
    (out/'search-burst.json').write_text(json.dumps({'key':'f2','source_sha256':digest(Path(__file__)),'samples':samples},indent=2)+'\n')
perform(run,[['capture','12-search-settled'],['key','f2'],['wait','Srch:'],['type','unfinished'],['key','f1'],['capture','13-search-cancel'],['key','alt-f3'],['wait','Reveal Codes to restore'],['key','f2'],['wait','Srch:'],['type','zzzzmissing']])
with qmp.QMP() as q:
    q.hmp('sendkey f2 80');time.sleep(.04)
    q.capture(out/'14-reveal-not-found')
perform(run,[['capture','15-reveal-search-settled'],['key','alt-f3'],['capture','16-final-normal'],['stop'],['export']])
