#!/usr/bin/env python3
"""Original SESSION1 probes, immutable evidence and read-only validation.

No Wordling application is exercised. Master/media remain private and unchanged.
One shared runtime lock serializes this runner with other SESSION1 invocations;
existing guest.start also refuses an already-running reference QMP socket.
"""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import time
import unittest

import guest
import qmp
from smoke import Probe

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/research/continuation/session1'
PRIVATE = Path(os.environ.get('WORDLING_REFERENCE_PRIVATE', '/home/lynn/projects/wordling/research/cache/reference')).resolve()
MASTER = PRIVATE / 'master'
PROFILE = ROOT / 'docs/research/reference-environment/environment.json'
FIXTURE = ROOT / 'docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5'
FIXTURE_SHA = 'c6cffde251e03b1f884c8e209afb426fced87d8c633ee4d1e3e4eb7e7c34aa3d'
BASELINE = 'wp51-dos-us-1992-03-09'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def fixture():
    data = FIXTURE.read_bytes()
    manifest = json.loads((FIXTURE.parent.parent / 'run.json').read_text())
    case = next(x for x in manifest['results'] if x['case_id']=='CMD51-204')
    recorded = next(x for x in case['evidence'] if x['path'].endswith('/ORIGIN.WP5'))
    if sha(FIXTURE) != FIXTURE_SHA or recorded['sha256'] != FIXTURE_SHA or len(data)!=recorded['size']:
        raise ValueError('Pinned original fixture differs from its original run')
    if data[struct.unpack_from('<I', data, 4)[0]:].hex() != '41c30cc34243c40cc444':
        raise ValueError('Unexpected fixture body')
    return data


def configure():
    # Use the existing shared short QMP path: lane paths exceed AF_UNIX length.
    runtime = PRIVATE / 'runtime'
    for module in (guest, qmp):
        module.RUNTIME = runtime
        module.SOCKET = runtime / 'qmp.sock'
    guest.MASTER, guest.PROFILE = MASTER, PROFILE
    qmp.ROOT = ROOT


@contextmanager
def exclusive():
    configure()
    PRIVATE.mkdir(parents=True, exist_ok=True)
    with (PRIVATE/'session1.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield


def seed_disk(work):
    seed = work/'seed.img'
    seed.parent.mkdir(parents=True, exist_ok=True)
    with seed.open('wb') as f:
        f.truncate(1474560)
    subprocess.run(['mformat','-i',str(seed),'-f','1440','::'],check=True,capture_output=True)
    subprocess.run(['mcopy','-i',str(seed),str(FIXTURE),'::ORIGIN'],check=True,capture_output=True)
    return seed


class SessionProbe(Probe):
    def capture(self, label):
        screen = super().capture(label)
        # Read VGA CRTC cursor/display registers while paused; restore selected index.
        running = self.q.execute('query-status')['running']
        if running:self.q.execute('stop')
        original = None
        try:
            read = lambda port:int(re.findall(r'0x([0-9a-fA-F]+)', self.q.hmp('i /b '+hex(port)))[-1],16)
            original = read(0x3d4)
            registers = {}
            for index in (10,11,12,13,14,15):
                self.q.hmp('o /b 0x3d4 '+str(index))
                registers[str(index)] = read(0x3d5)
            start = registers['12']*256+registers['13']
            address = registers['14']*256+registers['15']
            offset = (address-start)%32768
            (self.out/label/'cursor.json').write_text(json.dumps({'crtc':registers,'selected_index':original,
                'display_start_word':start,'cursor_word':address,'row':offset//80,'column':offset%80,
                'note':'Hardware text cursor only; semantic token gaps are not inferred from this alone.'},indent=2)+'\n')
        finally:
            if original is not None:self.q.hmp('o /b 0x3d4 '+str(original))
            if running:self.q.execute('cont')
        return screen


EXPECTED_CUES = {
    'prefilled-filename':('Document to be saved: B:\\ORIGIN',),
    'filename-edited':('Document to be saved: B:\\OXIGIN',),
    'character-first-name':('Document to be saved: C:\\OUT\\CHARFST',),
    'replacement-question':('Replace C:\\OUT\\CHARFST? No (Yes)',),
    'replacement-refused':('Document to be saved: C:\\OUT\\CHARFST',),
    'exit-save-question':('Save document? Yes (No)',),
    'exit-application-question':('Exit WP? No (Yes)',),
    'retrieve-missing':('ERROR: File not found -- B:\\MISSING',),
    'retrieve-retry-name':('Document to be retrieved: B:\\MISSING',),
}


def state(p, label, needles=()):
    screen = p.capture(label)
    needles = tuple(needles)+EXPECTED_CUES.get(label,())
    for needle in needles:
        p.check(label+': '+needle, needle in screen)
    return screen


def retrieve(p):
    p.key('shift-f10');p.q.wait_for('Document to be retrieved:')
    state(p,'retrieve-prompt',['Document to be retrieved:'])
    p.type('B:\\ORIGIN');p.key('ret');p.q.wait_for('ABCD')
    state(p,'retrieved',['ABCD'])


def normal(p, marker='ABCD'):
    p.q.wait_for(marker)
    return state(p,'editing-'+str(len(p.trace)),[marker])


def exit_clean(p):
    p.key('f7');p.q.wait_for('Save document?');state(p,'cleanup-save')
    p.key('n');p.q.wait_for('Exit WP?');state(p,'cleanup-exit')
    p.key('y');p.q.wait_for('C:\\WP51>');state(p,'clean-exit',['C:\\WP51>'])


def calibration(p):
    # Capture unknown wording before turning it into a recipe assertion.
    p.key('shift-f10');state(p,'retrieve-unknown')
    p.type('B:\\ORIGIN');p.key('ret');state(p,'retrieved-unknown')
    p.key('f10');state(p,'filename-unknown');p.key('f1')
    exit_clean(p)


def retrieval(p):
    for key in ('f1','esc'):
        p.key('shift-f10');p.q.wait_for('Document to be retrieved:')
        state(p,'retrieve-'+key+'-prompt')
        p.type('B:\\MISSING');state(p,'retrieve-'+key+'-draft')
        p.key(key);p.q.wait_absent('Document to be retrieved:')
        s=state(p,'retrieve-'+key+'-cancel')
        p.check('Blank buffer after Retrieve '+key, not any(t in s for t in ('ABCD','MISSING')))
    p.key('shift-f10');p.type('B:\\MISSING');p.key('ret')
    p.q.wait_until(lambda screen:'not found' in screen.lower(), 'missing-file error');state(p,'retrieve-missing')
    p.q.wait_for('Document to be retrieved:')
    state(p,'retrieve-retry-name',['B:\\MISSING'])
    p.type('B:\\ORIGIN');p.key('ret');p.q.wait_for('ABCD')
    state(p,'retrieve-retry-success',['ABCD'])
    p.key('f10');p.type('C:\\OUT\\RETRIEV');p.key('ret')
    p.q.wait_absent('Document to be saved:');state(p,'retrieved-saved',['ABCD'])
    p.exports.append(('RETRIEV','RETRIEV.WP5'))
    exit_clean(p)


def cursor(p):
    retrieve(p)
    for view in ('normal','codes'):
        if view=='codes':p.key('alt-f3');p.q.wait_for('[BOLD]')
        p.key('home,home,up');state(p,view+'-after-initial')
        p.key('home,home,home,up');state(p,view+'-before-initial')
        for gap in range(7):
            state(p,view+'-gap-'+str(gap),['ABCD','Pos '+('1','1.1','1.1','1.2','1.3','1.3','1.4')[gap]+'\"'])
            if gap<6:p.key('right')
    p.key('alt-f3');p.q.wait_absent('Press Reveal Codes to restore screen')
    p.key('f10');p.type('C:\\OUT\\CURSOR');p.key('ret');p.q.wait_absent('Document to be saved:')
    p.exports.append(('CURSOR','CURSOR.WP5'))
    p.key('f7');p.q.wait_for('Save document?');p.key('n');p.q.wait_for('Exit WP?');p.key('n')
    p.q.wait_absent('Exit WP?')
    p.key('f6');p.type('LEAD');p.key('f6')
    p.key('f10');p.type('C:\\OUT\\LEAD');p.key('ret');p.q.wait_absent('Document to be saved:')
    p.exports.append(('LEAD','LEAD.WP5'))
    for view in ('leading-normal','leading-codes'):
        if view=='leading-codes':p.key('alt-f3');p.q.wait_for('[BOLD]')
        p.key('home,home,up');state(p,view+'-after-initial',['LEAD'])
        p.key('home,home,home,up');state(p,view+'-before-initial',['LEAD'])
    p.key('alt-f3');p.q.wait_absent('Press Reveal Codes to restore screen')
    p.key('f10');p.type('C:\\OUT\\LEADPOST');p.key('ret');p.q.wait_absent('Document to be saved:')
    p.exports.append(('LEADPOST','LEADPOST.WP5'))
    exit_clean(p)


def filenames(p):
    retrieve(p)
    p.key('f10');p.q.wait_for('Document to be saved:');state(p,'prefilled-filename')
    p.key('right,right,right,right,right');state(p,'filename-right')
    p.key('backspace');state(p,'filename-backspace')
    p.type('X');state(p,'filename-edited')
    p.key('f1');normal(p)
    p.key('f10');p.type('C:\\OUT\\CHARFST');state(p,'character-first-name')
    p.key('ret');p.q.wait_absent('Document to be saved:')
    p.exports.append(('CHARFST','CHARFST.WP5'))
    p.type('CHANGED');p.key('f10');p.key('ret');p.q.wait_for('Replace')
    state(p,'replacement-question')
    p.key('n');p.q.wait_for('Document to be saved:');state(p,'replacement-refused')
    p.key('f1');state(p,'replacement-name-cancel',['CHANGED'])
    exit_clean(p)


def prepare_context(p, named, changed):
    if named:retrieve(p)
    else:p.type('UNNAMED');p.q.wait_for('UNNAMED')
    if not named and not changed:
        # Saved then clear filename? There is no assumed unnamed-saved original state.
        # A fresh empty unnamed document is the original unmodified context instead.
        raise ValueError('Use fresh blank document for unnamed unmodified context')
    if named and changed:p.type('CHANGED');p.q.wait_for('CHANGED')


def exits(p, context, action):
    named=context.startswith('named');changed=context.endswith('changed') and not context.endswith('unchanged')
    if context!='unnamed-unchanged':prepare_context(p,named,changed)
    initial=state(p,'exit-start')
    first=initial.splitlines()[0]
    p.check('Exit starting buffer matches declared context', first==({'named-unchanged':'ABCD','named-changed':'CHANGEDABCD','unnamed-unchanged':'','unnamed-changed':'UNNAMED'}[context]))
    p.key('f7');p.q.wait_for('Save document?');state(p,'exit-save-question')
    if action in ('save-f1','save-esc'):
        p.key('f1' if action=='save-f1' else 'esc');p.q.wait_absent('Save document?')
        if action=='save-esc':
            advanced=state(p,'exit-save-escape-advance',['Document to be saved:'])
            p.check('Escape follows default Save choice, not F1 cancel',advanced.splitlines()[0]==first)
            # The separately observed F1 filename cancel safely unwinds this state.
            # Never answer Yes to an existing destination/replacement question.
            p.key('f1');p.q.wait_absent('Document to be saved:')
            cancelled=state(p,'escape-filename-f1-return',[first] if first else [])
        else:
            cancelled=state(p,'exit-save-cancel')
        p.check('F1 cancellation retains the original editing buffer',cancelled.splitlines()[0]==first)
        p.check('F1 returns to editing state', 'Doc 1 Pg' in cancelled)
        exit_clean(p)
    else:
        p.key('n');p.q.wait_for('Exit WP?');state(p,'exit-application-question')
        p.key({'exit-f1':'f1','exit-esc':'esc','continue':'n','quit':'y'}[action])
        p.q.wait_absent('Exit WP?');choice=state(p,'exit-choice-result')
        if action=='exit-f1':p.check('F1 Exit-prompt cancellation retains buffer',choice.splitlines()[0]==first)
        if action=='exit-esc':p.check('Escape follows default No and clears document',choice.splitlines()[0]=='' and 'Doc 1 Pg' in choice)
        if action=='continue':p.check('Declining application exit clears buffer',choice.splitlines()[0]=='')
        if action=='quit':p.q.wait_for('C:\\WP51>')
        else:exit_clean(p)


def normal_prefix(p):
    p.key('f6');p.type('LEAD');p.key('f6')
    p.key('f10');p.type('C:\\OUT\\PREFIX0');p.key('ret');p.q.wait_absent('Document to be saved:')
    p.exports.append(('PREFIX0','PREFIX0.WP5'))
    for view in ('normal','codes'):
        if view=='codes':p.key('alt-f3');p.q.wait_for('[BOLD]')
        p.key('home,home,up');state(p,'prefix-'+view+'-after',['LEAD'])
        p.key('right');state(p,'prefix-'+view+'-after-right',['LEAD','Pos 1.1"'])
        p.key('home,home,home,up');state(p,'prefix-'+view+'-before',['LEAD'])
        p.key('right');state(p,'prefix-'+view+'-before-right',['LEAD','Pos 1"'])
    p.key('alt-f3');p.q.wait_absent('Press Reveal Codes to restore screen')
    p.key('f10');p.type('C:\\OUT\\PREFIX1');p.key('ret');p.q.wait_absent('Document to be saved:')
    p.exports.append(('PREFIX1','PREFIX1.WP5'))
    exit_clean(p)


# The registry IDs are allocated only after calibration; local branches remain explicit.
BRANCHES={'retrieve':retrieval,'cursor':cursor,'filenames':filenames,'prefix-normal':normal_prefix}
for context in ('named-unchanged','named-changed','unnamed-unchanged','unnamed-changed'):
    for action in ('save-f1','save-esc','exit-f1','exit-esc','continue','quit'):
        BRANCHES[context+'-'+action]=lambda p,c=context,a=action:exits(p,c,a)


def execute(run_id, branch, case_id, public=True):
    if not re.fullmatch(r'[A-Za-z0-9_-]+',run_id):raise ValueError('Unsafe run ID')
    if not re.fullmatch(r'CMD51-\d{3}',case_id):raise ValueError('Unsafe canonical case ID')
    fixture();configure()
    out=(OUT/'runs' if public else PRIVATE/'session1-calibration')/run_id
    work=PRIVATE/'session1-runs'/run_id
    if out.exists() or work.exists():raise FileExistsError('Existing run/evidence is immutable')
    out.mkdir(parents=True);work.mkdir(parents=True)
    sources=[Path(__file__),ROOT/'scripts/reference/guest.py',ROOT/'scripts/reference/qmp.py',ROOT/'scripts/reference/smoke.py',ROOT/'scripts/reference/extended.py']
    # smoke imports additional families even though SESSION1 does not execute them.
    sources += [ROOT/'scripts/reference'/name for name in ('advanced.py','document.py','history_loops.py','iteration_nesting.py','value_secondary.py')]
    driver=ROOT/'docs/research/continuation/session1/rerun_contexts.py'
    if driver.exists():sources.append(driver)
    source_records=[]
    for source in sources:
        target=out/'runner-source'/source.name;target.parent.mkdir(exist_ok=True);shutil.copyfile(source,target)
        source_records.append({'path':str(source.relative_to(ROOT)),'sha256':sha(source)})
    shutil.copyfile(PROFILE,out/'environment.json')
    shutil.copyfile(ROOT/'docs/research/command-scenarios.json',out/'scenario-registry.json')
    run={'schema_version':1,'run_id':run_id,'started_at':datetime.now(timezone.utc).isoformat(),
         'baseline_id':BASELINE,'scope':'original-reference-only','wordling_tested':False,
         'branch':branch,'master_disk_sha256':sha(MASTER/'harddisk.img'),'master_boot_sha256':sha(MASTER/'boot.img'),
         'runner_sources':source_records,'environment_manifest_sha256':sha(PROFILE),
         'environment_profile_archive':str((out/'environment.json').relative_to(ROOT)) if public else str(out/'environment.json'),
         'scenario_registry_sha256':sha(ROOT/'docs/research/command-scenarios.json'),
         'fixture':{'path':str(FIXTURE.relative_to(ROOT)),'sha256':FIXTURE_SHA,'size':FIXTURE.stat().st_size},
         'runtime_configuration':{'private_root':str(PRIVATE),'socket':str(qmp.SOCKET),'exclusive_lock':str(PRIVATE/'session1.lock')},'results':[]}
    result={'case_id':case_id,'subcase_id':branch,'result':'error','observed_scope':'Original SESSION1 branch only; no Wordling comparison'}
    p=None;original_arguments=guest.arguments
    try:
        seed=seed_disk(work);run['seed_disk_sha256']=sha(seed)
        guest.arguments=lambda boot,disk:original_arguments(boot,disk)+['-drive',f'file={seed},format=raw,if=floppy,index=1,readonly=on']
        result['qemu_argv']=guest.start(work/'guest')
        with qmp.QMP() as q:
            p=SessionProbe(q,out/case_id)
            (calibration if branch=='calibrate' else BRANCHES[branch])(p)
            p.check('Branch captured a completed original state', bool(p.checks) and bool(p.trace))
        result['result']='observed-matches-smoke-expectations'
    except Exception as error:
        result['error']=str(error)
        try:
            with qmp.QMP() as q:q.capture(out/case_id/'error-screen')
        except Exception:pass
    finally:
        guest.arguments=original_arguments;guest.stop()
        if p:
            result['trace'],result['checks']=p.trace,p.checks
            result['native_outputs']=[]
            if result['result']!='error':
                try:
                    for source,name in p.exports:
                        target=out/case_id/name
                        subprocess.run(['mcopy','-i',str(work/'guest/harddisk.img')+'@@1048576','::OUT/'+source,str(target)],check=True,capture_output=True)
                        b=target.read_bytes();p.check('Native export signature '+name,b[:4]==bytes.fromhex('ff575043'))
                        result['native_outputs'].append({'path':str(target.relative_to(ROOT)) if public else str(target),'size':len(b),'sha256':sha(target)})
                except Exception as error:result['result']='error';result['error']=str(error)
        result['evidence']=[{'path':str(x.relative_to(ROOT)) if public else str(x),'size':x.stat().st_size,'sha256':sha(x)} for x in sorted((out/case_id).rglob('*')) if x.is_file()]
        aliases = {'retrieve':['CMD51-237','CMD51-238','CMD51-239'],
                   'cursor':['CMD51-019','CMD51-020'],
                   'prefix-normal':['CMD51-019'],
                   'filenames':['CMD51-067','CMD51-070']}.get(branch,[])
        run['results'].append(result)
        for alias in aliases:
            run['results'].append({**result,'case_id':alias,
                'observed_scope':'Related bounded SESSION1 subcase; see branch table for exact assertions and remaining limits'})
        # Read-only seed medium is never modified by WP; audit underlying fixture too.
        run['master_unchanged']=sha(MASTER/'harddisk.img')==run['master_disk_sha256'] and sha(MASTER/'boot.img')==run['master_boot_sha256']
        run['fixture_unchanged']=sha(FIXTURE)==FIXTURE_SHA
        run['seed_unchanged']=sha(seed)==run['seed_disk_sha256']
        run['seed_fixture_sha256']=hashlib.sha256(subprocess.check_output(['mtype','-i',str(seed),'::ORIGIN'])).hexdigest()
        (out/'run.json').write_text(json.dumps(run,indent=2)+'\n')
    print(run_id,branch,result['result'],result.get('error',''),flush=True)
    return result['result']!='error'


def verify(prefix):
    registry={x['id']:x for x in json.loads((ROOT/'docs/research/command-scenarios.json').read_text())}
    manifests=sorted((OUT/'runs').glob(prefix+'*/run.json'))
    if not manifests:raise ValueError('No immutable runs selected')
    selection=json.loads((OUT/'accepted-branches.json').read_text())
    accepted=set(selection['accepted_run_ids'])
    if not accepted:raise ValueError('No accepted run selection')
    paired={};errors=[];rejected=[];seen=set()
    for path in manifests:
        run=json.loads(path.read_text());branch=run['branch'];selected=run['run_id'] in accepted
        seen.add(run['run_id'])
        if branch not in BRANCHES:raise ValueError('Unknown branch')
        if run['scope']!='original-reference-only' or run['wordling_tested']:raise ValueError('Wrong evidence scope')
        for key in ('master_unchanged','fixture_unchanged','seed_unchanged'):
            if not run[key]:raise ValueError('Source changed: '+key)
        if run['seed_fixture_sha256']!=FIXTURE_SHA:raise ValueError('Seed fixture mismatch')
        if sha(path.parent/'environment.json')!=run['environment_manifest_sha256']:raise ValueError('Environment archive changed')
        if sha(path.parent/'scenario-registry.json')!=run['scenario_registry_sha256']:raise ValueError('Scenario archive changed')
        for source in run['runner_sources']:
            if sha(path.parent/'runner-source'/Path(source['path']).name)!=source['sha256']:raise ValueError('Runner archive changed')
        for result in run['results']:
            cid=result['case_id'];feature='WP51-019' if branch=='retrieve' else ('WP51-008' if branch in ('cursor','prefix-normal') else ('WP51-020' if branch=='filenames' else 'WP51-029'))
            if feature not in registry[cid]['feature_ids']:raise ValueError('Case-feature mismatch')
            if result['result']!='observed-matches-smoke-expectations' or not result['checks'] or not all(x['passed'] for x in result['checks']):
                (errors if selected else rejected).append((run['run_id'],cid,result.get('error','failed checks')))
            for artifact in result['evidence']:
                f=ROOT/artifact['path']
                if (f.stat().st_size,sha(f))!=(artifact['size'],artifact['sha256']):raise ValueError('Evidence checksum mismatch')
            for native in result.get('native_outputs',[]):
                f=ROOT/native['path'];data=f.read_bytes();offset=struct.unpack_from('<I',data,4)[0]
                if not 16<=offset<=len(data):raise ValueError('Bad captured document offset')
                if f.name in ('PREFIX0.WP5','PREFIX1.WP5') and data[offset:].hex()!='c30cc34c454144c40cc4':raise ValueError('Leading native content changed')
                if f.name in ('RETRIEV.WP5','CURSOR.WP5','CHARFST.WP5') and data[offset:].hex()!='41c30cc34243c40cc444':raise ValueError('Original document content changed')
        canonical=run['results'][0]
        # Compare textual session state and hardware cursor fields; blinking raster may differ.
        states={}
        directory=path.parent/canonical['case_id']
        for capture in directory.glob('*/screen.txt'):
            cursor_file=capture.with_name('cursor.json')
            if not cursor_file.exists():raise ValueError('Missing hardware cursor capture')
            cursor=json.loads(cursor_file.read_text())
            states[capture.parent.name]={'screen':capture.read_text(),'cursor':{k:cursor[k] for k in ('row','column','cursor_word','display_start_word')}}
        if not selected:continue
        paired.setdefault(branch,[]).append({'run_id':run['run_id'],'states':states,'manifest_sha256':sha(path)})
    report={'scope':'Original-only SESSION1 evidence audit; no Wordling acceptance','pairs':{},'errors':errors,'retained_diagnostic_attempts':rejected}
    if not accepted<=seen:raise ValueError('Selected run missing')
    if set(paired)!=set(BRANCHES):raise ValueError('Accepted branch coverage incomplete')
    for branch,pair in paired.items():
        if len(pair)!=2:raise ValueError('Need exactly two fresh runs for '+branch)
        differences=[name for name in set(pair[0]['states'])|set(pair[1]['states']) if pair[0]['states'].get(name)!=pair[1]['states'].get(name)]
        report['pairs'][branch]={'runs':[x['run_id'] for x in pair],'manifest_sha256':[x['manifest_sha256'] for x in pair],'state_differences':differences}
        if differences:errors.append((branch,'repetition state differs',differences))
    print(json.dumps(report,indent=2))
    return not errors


class BoundaryTests(unittest.TestCase):
    def test_immutable_run_id(self):
        for value in ('../escape','a/b','', 'x;rm'):
            with self.assertRaises(ValueError):execute(value,'retrieve','CMD51-065')
    def test_fixture_matches_sealed_manifest(self):
        self.assertEqual(hashlib.sha256(fixture()).hexdigest(),FIXTURE_SHA)
    def test_case_path_cannot_escape_evidence_directory(self):
        for value in ('../outside','CMD51-X','CMD51-001/../../escape'):
            with self.assertRaises(ValueError):execute('safe-run','retrieve',value)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_id');parser.add_argument('branch',choices=['verify','self-test','suite','calibrate',*BRANCHES]);parser.add_argument('--case-id',default='CMD51-065');parser.add_argument('--private',action='store_true')
    args=parser.parse_args()
    if args.branch=='verify':return 0 if verify(args.run_id) else 1
    if args.branch=='self-test':return 0 if unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(BoundaryTests)).wasSuccessful() else 1
    with exclusive():
        if args.branch=='suite':
            mapping={'retrieve':'CMD51-065','cursor':'CMD51-049','filenames':'CMD51-069','prefix-normal':'CMD51-020'}
            actions={'save-f1':'CMD51-240','save-esc':'CMD51-241','exit-f1':'CMD51-242','exit-esc':'CMD51-243','continue':'CMD51-087','quit':'CMD51-244'}
            okay=True
            for index,branch in enumerate(BRANCHES):
                cid=mapping.get(branch)
                if cid is None:cid=next(value for suffix,value in actions.items() if branch.endswith('-'+suffix))
                for repetition in (1,2):
                    passed=execute(args.run_id+f'-b{index:02d}-r{repetition}',branch,cid,not args.private)
                    okay=passed and okay
        else:okay=execute(args.run_id,args.branch,args.case_id,not args.private)
    return 0 if okay else 1


if __name__=='__main__':raise SystemExit(main())
