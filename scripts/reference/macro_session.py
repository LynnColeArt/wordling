#!/usr/bin/env python3
"""WP38 original-only session experiments. Offline by default; VM needs release.

This is a bounded research harness, never a product WPM writer or compatibility claim.
"""
import argparse
import ast
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import struct
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
PRIMARY = Path('/home/lynn/projects/wordling')
OUT = ROOT/'docs/research/continuation/macro-session'
PINS = [
  {
    "path": "scripts/reference/qmp.py",
    "sha256": "dcb3aaa83c72b695f63a86529b25bc70fe26dd7e197fc27052effe8218f82304"
  },
  {
    "path": "scripts/reference/guest.py",
    "sha256": "b153fdf898a425c46f57cb2daa743ad0f83b01372c7918d6687c85fa92edcc37"
  },
  {
    "path": "scripts/reference/smoke.py",
    "sha256": "36297bcedfe66a6c2de6ecf6de118ca2ff6d938fcc4d815cde0c650515e02fb9"
  },
  {
    "path": "scripts/reference/extended.py",
    "sha256": "ac58afcef32b0fa2d6bf7eff6129a7108b7e65ec8bc8d5119faaf3678c64e2a8"
  },
  {
    "path": "scripts/reference/advanced.py",
    "sha256": "837cdcb8aa85531c7dff873f3705f52b81e4ae6a9c1c419f5891d1336eb9203f"
  },
  {
    "path": "scripts/reference/document.py",
    "sha256": "dfb646f08ec21c8549b3e0d99e0efe285185ffa178e2b65b2df02a6b7e22296d"
  },
  {
    "path": "scripts/reference/history_loops.py",
    "sha256": "d788b84952f971a2e3d1b1512a5ad75b480943931a3266251db548c92f60a87b"
  },
  {
    "path": "scripts/reference/iteration_nesting.py",
    "sha256": "a534c7c72332ca31ff1eb747343d3f11de96543cb352651af82db29620aaaac5"
  },
  {
    "path": "scripts/reference/value_secondary.py",
    "sha256": "36c0dcaf31d94d522e1dc19c2eb64a3fb0415c3927127b64bb1415b3d7a784fa"
  },
  {
    "path": "kitty-specs/wp51-parity-01M64CVY/contracts/macro-framing.md",
    "commit": "4eb851eac3096d27d4743616ce3ae74f7a9edc05",
    "sha256": "3409954e3d492ea5498eda0a0a6783a26fea7c2c0ffb8d157d4c990c900d52e7"
  },
  {
    "path": "kitty-specs/wp51-parity-01M64CVY/contracts/macro-fixtures.json",
    "commit": "4eb851eac3096d27d4743616ce3ae74f7a9edc05",
    "sha256": "fca8446e98ad95ab118fc672e48e821afc65e9e3b2b5a43c27f7759824c2ce5d"
  },
  {
    "path": "kitty-specs/wp51-parity-01M64CVY/tasks/WP32-macro-native-contract/review-evidence-1.md",
    "commit": "754bdccd92120ba75d6c53c1d3f9ba0a061054c8",
    "sha256": "d9993b09c5e154508350b8ad79cc52539919baf71852ec2144021f05ce84de4d"
  },
  {
    "path": "docs/research/reference-baseline.json",
    "sha256": "6ba2f6bd8fa77e4b309b1a81203705c060285707ab07ec6f3432dfa194075ba5"
  },
  {
    "path": "docs/research/sources.json",
    "sha256": "850df4eccc4e4bb17d53aa8c59ab2aa417522a46063d628fd8c8a076d6de9fba"
  },
  {
    "path": "docs/research/reference-environment/environment.json",
    "sha256": "30123ddc32289702c8240bf4e5bef65d0ff979c5d48b558f544271b14c00bfc2"
  },
  {
    "path": "docs/research/reference-environment/resource-profile.json",
    "sha256": "e9498fb1833fac66509b792dacd5ccf3915f26f2a24ff1f0f8cbe72d7aa9645b"
  },
  {
    "path": "docs/research/reference-environment/installed-files.json",
    "sha256": "a8532ce5be7caa5759799841c8c0e3128810f7631f49101978102244139a1238"
  }
]
TEMPLATE = 'docs/research/reference-runs/2026-10-29-extended-04/CMD51-131/TESTMAC.WPM'
TEMPLATE_SHA = 'e0e71258e6dc4c678b27773831105f0e7fca0b0803d451fb58b80ac02bc20b4e'
EXPECTED_EXE = '0734d0734c78c113ddaf40293c2c21b02e2cacc063bca5aa3d02f696de0bdc6a'
DOC1, DOC2 = 'D1SENT DIRTY1', 'D2SENT DIRTY2'
# Explicit SDK WP95/97/98 (PDF108/110/111) identities. Documentary words are
# isolated experiments until actually consumed by the pinned March original.
WORDS = {'DISPLAY_ON': 0xFC0D, 'CANCEL_OFF': 0xFC05, 'CANCEL_ON': 0xFC06,
         'WHILE': 0xFC2B, 'END_WHILE': 0xFC11, 'WAIT': 0xFC2A, 'CANCEL_KEY': 0x8020}


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')


def git_blob(commit, path):
    if not re.fullmatch('[0-9a-f]{40}', commit) or path.startswith('/') or '..' in Path(path).parts:
        raise ValueError('Unsafe pinned Git source')
    return subprocess.check_output(['git', '--no-optional-locks', '-C', str(ROOT),
                                    'cat-file', 'blob', commit+':'+path], timeout=15)


def pinned_inputs():
    for pin in PINS:
        data = git_blob(pin['commit'], pin['path']) if 'commit' in pin else (ROOT/pin['path']).read_bytes()
        if hashlib.sha256(data).hexdigest() != pin['sha256']:
            raise ValueError('Pinned source drift: '+pin['path'])
        yield pin, data


class SDKNativeWords:
    """Reference-fixture emitter/inspector over an exact project-authored prefix.

    This grants no Wordling serialization, opcode admission or producer qualification.
    """
    @staticmethod
    def inspect(data):
        if len(data) < 56 or data[:4] != b'\xffWPC' or data[8:12] != b'\x01\x01\x01\x01':
            raise ValueError('Unsupported reference fixture tuple/prefix')
        offset = struct.unpack_from('<I', data, 4)[0]
        if not 56 <= offset <= len(data) or (len(data)-offset) % 2:
            raise ValueError('Unpaired relative native words')
        values = list(struct.unpack('<'+'H'*((len(data)-offset)//2), data[offset:]))
        if not values or values[-1] != 0 or 0 in values[:-1]:
            raise ValueError('Expected one terminal word')
        return offset, values

    @staticmethod
    def emit(parts):
        original = (ROOT/TEMPLATE).read_bytes()
        if hashlib.sha256(original).hexdigest() != TEMPLATE_SHA:
            raise ValueError('Original project fixture differs')
        offset, _ = SDKNativeWords.inspect(original)
        values = []
        for part in parts:
            if isinstance(part, str):
                if not all(32 <= ord(c) <= 126 for c in part):
                    raise ValueError('Only documentary ASCII fixture arguments')
                values.extend(map(ord, part))
            elif type(part) is int and part in WORDS.values():
                values.append(part)
            else:
                raise ValueError('Unlisted documentary word')
        return original[:offset]+struct.pack('<'+'H'*(len(values)+1), *values, 0)


def recipes():
    common = {'repetitions': 2, 'scope': 'original-reference-only', 'wordling_tested': False,
              'feature_ids': ['WP51-059', 'WP51-060'], 'status': 'not-run'}
    rows = [
        ('name-cancel', ['CMD51-131'], 'Dirty Doc1 and Doc2; Alt-F10 Macro: name then F1; inspect return and native preservation.'),
        ('run-doc1', ['CMD51-131'], 'Run exact original ABC fixture on dirty Doc1; preserve distinct dirty Doc2.'),
        ('repeat-doc2', ['CMD51-132'], 'Esc,3,Alt-F10 on selected dirty Doc2; exact ABCABCABC effect, Doc1 remains separate.'),
        ('missing-name', [], 'Absent M38NONE WPM at invocation; retain exact original error/prompt and recovery, no invented message.'),
        ('pending-save', [], 'Alt-F10 from an observed Save-name prompt; retain nested/cancel behavior, no guessed modal contract.'),
        ('internal-cancel', [], 'Execute stored SDK8020 Cancel word with no user F1; do not equate it with a user stop.'),
        ('stop-default', ['CMD51-133'], 'Observe two evolving loop heartbeats before USER F1, then require stable/manual recovery; host timeout separate.'),
        ('stop-on', ['CMD51-133'], 'Separate documentary CANCEL ON experiment; March behavior unqualified until original execution/source captures.'),
        ('stop-off', ['CMD51-133'], 'Separate documentary CANCEL OFF experiment; no Ctrl-Break alias; containment never becomes original cancellation.'),
    ]
    return [dict(common, id=i, parent_case_ids=parents, recipe=desc,
                 feature_ids=['WP51-059'] if parents else ['WP51-059','WP51-060'],
                 canonical_case_complete=False, canonical_expansion_required=not bool(parents),
                 source_locators=['REF373–393/PDF390–410','REF379/PDF396','SDK95/97/98/PDF108/110/111'])
            for i, parents, desc in rows]


def fixture_for(case):
    if case in ['run-doc1', 'repeat-doc2']:
        return (ROOT/TEMPLATE).read_bytes(), 'exact-original-project-fixture'
    if case == 'internal-cancel':
        return SDKNativeWords.emit([WORDS['DISPLAY_ON'], 'INTERNAL', WORDS['CANCEL_KEY'], 'MSTAIL']), 'documentary-unqualified'
    if case.startswith('stop-'):
        parts = [WORDS['DISPLAY_ON']]
        if case == 'stop-on':
            parts.append(WORDS['CANCEL_ON'])
        if case == 'stop-off':
            parts.append(WORDS['CANCEL_OFF'])
        parts += ['MSLIVE', WORDS['WHILE'], '1~', '.', WORDS['WAIT'], '10~',
                  WORDS['END_WHILE'], 'MSTAIL']
        return SDKNativeWords.emit(parts), 'documentary-unqualified'
    return None, 'no-macro-input'


def offline_check():
    checked = []
    for pin, data in pinned_inputs():
        if pin['path'].endswith('.py'):
            ast.parse(data)
        checked.append(pin)
    tree = ast.parse((ROOT/'scripts/reference/guest.py').read_text())
    names = {x.name for x in tree.body if isinstance(x, ast.FunctionDef)}
    if not {'start','stop','arguments'} <= names:
        raise ValueError('Guest protocol API mismatch')
    baseline=json.loads((ROOT/'docs/research/reference-baseline.json').read_text())
    if baseline['executable_sha256']!=EXPECTED_EXE:raise ValueError('Selected executable identity drift')
    template = (ROOT/TEMPLATE).read_bytes()
    if hashlib.sha256(template).hexdigest() != TEMPLATE_SHA:
        raise ValueError('Original template hash mismatch')
    _, words = SDKNativeWords.inspect(template)
    if words != [0xFC0C, 65, 66, 67, 0]:
        raise ValueError('Original template word identity differs')
    for recipe in recipes():
        data, _ = fixture_for(recipe['id'])
        if data:
            SDKNativeWords.inspect(data)
    return {'result': 'offline-preparation-valid', 'vm_launched': False,
            'original_runs_executed': 0, 'full_m1_accepted': False,
            'pinned_sources': checked, 'recipes': recipes(), 'template_sha256': TEMPLATE_SHA,
            'word_status': 'documentary fixture words do not authorize product execution',
            'shared_lock': str(PRIMARY/'research/cache/reference/session1.lock')}


def configure(primary):
    # Import only after explicit VM authorization. Never borrow WP23/session1 code.
    qmp = importlib.import_module('qmp')
    guest = importlib.import_module('guest')
    private = primary/'research/cache/reference'
    runtime = private/'runtime/wp38'
    for module in [qmp, guest]:
        module.RUNTIME, module.SOCKET = runtime, runtime/'qmp.sock'
    guest.MASTER = private/'master'
    guest.PROFILE = primary/'docs/research/reference-environment/environment.json'
    if len(os.fsencode(str(qmp.SOCKET))) >= 104:
        raise ValueError('QMP Unix socket path too long')
    return qmp, guest, private


@contextmanager
def exclusive(private):
    # Same actual lock as WP13/WP23. No lock is opened by check/result/preparation.
    with (private/'session1.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield


class HostContainment(TimeoutError):
    pass


def timeout_signal(*unused):
    raise HostContainment('Host containment budget expired; not original Cancel')


def settings_snapshot(work, label):
    installed=json.loads((ROOT/'docs/research/reference-environment/installed-files.json').read_text())
    names=[x['path']for x in installed['files']if x['path'].upper().endswith('.SET')]
    if len(names)!=1:raise ValueError('Exact selected SET path is ambiguous')
    target=work/('settings-'+label+'.SET')
    subprocess.run(['mcopy','-i',str(work/'harddisk.img')+'@@1048576','::'+names[0],str(target)],
                   check=True,capture_output=True,timeout=15)
    return {'private_path':str(target),'size':target.stat().st_size,'sha256':sha(target),
            'publication':'private configuration bytes retained; public metadata only'}


def stop_owned(qmp, guest):
    try:
        guest.stop()
        return 'QMP quit; own socket terminated'
    except Exception:
        pidfile=qmp.RUNTIME/'qemu.pid'
        pid=int(pidfile.read_text())
        proc=Path('/proc')/str(pid)
        argv=(proc/'cmdline').read_bytes().split(b'\0')if proc.exists()else []
        marker=b'unix:'+os.fsencode(str(qmp.SOCKET))+b','
        if proc.exists() and not any(x.startswith(marker)for x in argv):
            raise RuntimeError('Cannot prove process ownership; do not signal another guest')
        for sig in [signal.SIGTERM,signal.SIGKILL]:
            if not proc.exists():break
            os.kill(pid,sig)
            deadline=time.monotonic()+3
            while proc.exists() and time.monotonic()<deadline:
                stat=(proc/'stat').read_text()if (proc/'stat').exists()else ''
                if stat and stat.split(') ',1)[1].startswith('Z'):break
                time.sleep(.05)
            if not proc.exists() or stat.split(') ',1)[-1].startswith('Z'):break
        else:
            raise RuntimeError('Owned guest did not terminate; retain failed ownership evidence')
        qmp.SOCKET.unlink(missing_ok=True)
        return 'Host containment: verified own pid termination; not original Cancel'


def fresh_start(qmp, guest, work, assets):
    if sha(guest.PROFILE)!=sha(ROOT/'docs/research/reference-environment/environment.json'):
        raise ValueError('Selected runtime profile differs from pinned preparation')
    profile = json.loads(guest.PROFILE.read_text())
    for file, expected in [(guest.MASTER/'boot.img', profile['master_boot_sha256']),
                           (guest.MASTER/'harddisk.img', profile['master_disk_sha256']),
                           (Path(profile['qemu_binary']['path']), profile['qemu_binary']['sha256'])] + [(Path(x['path']),x['sha256']) for x in profile['firmware']]:
        if sha(file) != expected:
            raise ValueError('Pinned private reference identity mismatch: '+str(file))
    if qmp.SOCKET.exists() or work.exists():
        raise FileExistsError('Prior runtime/run exists; do not replace or stop another guest')
    work.mkdir(parents=True)
    for name in ['boot.img','harddisk.img']:
        shutil.copyfile(guest.MASTER/name,work/name)
    disk = str(work/'harddisk.img')+'@@1048576'
    listing=subprocess.run(['mdir','-i',disk,'::OUT/'],check=True,capture_output=True,timeout=15)
    (work/'OUT-before.txt').write_bytes(listing.stdout)
    if b'M38NONE' in listing.stdout.upper():raise ValueError('Supposed missing macro already exists in scratch source')
    for name, path in assets:
        subprocess.run(['mcopy','-i',disk,str(path),'::OUT/'+name],check=True,capture_output=True,timeout=15)
        roundtrip = work/('seed-check-'+name)
        subprocess.run(['mcopy','-i',disk,'::OUT/'+name,str(roundtrip)],check=True,capture_output=True,timeout=15)
        if roundtrip.read_bytes() != path.read_bytes():
            raise ValueError('Scratch fixture injection changed bytes')
    settings_snapshot(work,'before')
    qmp.RUNTIME.mkdir(parents=True,exist_ok=True)
    argv = guest.arguments(work/'boot.img',work/'harddisk.img')
    subprocess.run(argv,check=True,capture_output=True,timeout=15)
    with qmp.QMP() as q:
        q.wait_for('Doc 1 Pg 1 Ln 1" Pos 1"', timeout=60)
    return argv


def seed_buffers(p, save_as):
    p.type('D1SENT '); save_as(p,'D1BASE'); p.type('DIRTY1')
    p.capture('doc1-dirty')
    p.key('shift-f3');p.q.wait_for('Doc 2')
    p.type('D2SENT ');save_as(p,'D2BASE');p.type('DIRTY2')
    p.capture('doc2-dirty');p.key('shift-f3');p.q.wait_for('Doc 1')


def invoke(p, name='M38'):
    p.key('alt-f10');p.q.wait_for('Macro:');p.capture('macro-name-prompt')
    p.type('C:\\OUT\\'+name);p.key('ret')


def act(case,p):
    if case == 'name-cancel':
        p.key('alt-f10');p.q.wait_for('Macro:');p.type('NOTEXEC')
        p.capture('named-before-user-cancel');p.key('f1');p.q.wait_absent('Macro:')
        p.capture('after-name-cancel');return 'observed-expected-bounded-effect'
    if case == 'run-doc1':
        invoke(p);p.q.wait_for(DOC1+'ABC');p.capture('doc1-after-run')
        return 'observed-expected-bounded-effect'
    if case == 'repeat-doc2':
        p.key('shift-f3');p.q.wait_for('Doc 2');p.key('esc');p.type('3')
        p.capture('repeat-before-macro');invoke(p);p.q.wait_for(DOC2+'ABCABCABC')
        p.capture('doc2-after-repeat');return 'observed-expected-bounded-effect'
    if case == 'missing-name':
        invoke(p,'M38NONE');time.sleep(.5);p.q.capture(p.out/'missing-name-raw')
        p.key('f1');p.q.capture(p.out/'missing-name-after-f1')
        return 'observed-needs-review'
    if case == 'pending-save':
        p.key('f10');p.q.wait_for('Document to be saved:');p.capture('pending-save-name')
        p.key('alt-f10');time.sleep(.4);p.q.capture(p.out/'pending-save-after-macro-key')
        p.key('f1');p.q.capture(p.out/'pending-save-after-f1')
        return 'observed-needs-review'
    if case == 'internal-cancel':
        invoke(p);time.sleep(.6);p.q.capture(p.out/'stored-cancel-word-no-user-f1')
        return 'observed-needs-review'
    invoke(p)
    p.q.wait_for('MSLIVE',timeout=5)
    a = p.q.capture(p.out/'running-heartbeat-a')
    p.q.wait_until(lambda screen: screen.count('.') > a.count('.')+1,
                   'evolving live-loop heartbeat before user F1',timeout=8)
    b = p.q.capture(p.out/'running-heartbeat-b')
    p.check('Two evolving heartbeats before USER F1', b.count('.') > a.count('.')+1 and 'MSTAIL' not in b)
    p.trace.append({'user_cancel_key':'f1','monotonic':time.monotonic(),'program_still_running_witness':True})
    p.key('f1');time.sleep(1.2)
    after=p.q.capture(p.out/'after-user-f1')
    p.type('USERREADY');time.sleep(1.5)
    recovered=p.q.capture(p.out/'manual-recovery-after-user-f1')
    if 'USERREADY' in recovered and recovered.count('.') == after.count('.') and 'MSTAIL' not in recovered:
        p.check('User input resumes with stable partial result; no loop tail',True)
        return 'observed-running-user-F1-stop'
    raise HostContainment('No proved original user-stop recovery; retain partial raw state and contain host')


def exports_after(p, save_as):
    # Capture actual selected document, never infer a semantic position from Pos.
    screen=p.q.text(p.out/'before-export-status')
    if 'Macro:' in screen or 'Document to be saved:' in screen:
        raise ValueError('Modal prompt still pending; native after export unavailable')
    if 'Doc 2' in screen:
        save_as(p,'D2AFTER');p.key('shift-f3');p.q.wait_for('Doc 1');save_as(p,'D1AFTER')
    else:
        save_as(p,'D1AFTER');p.key('shift-f3');p.q.wait_for('Doc 2');save_as(p,'D2AFTER')


def seal(out, report):
    report['artifacts']=[{'path':str(p.relative_to(out)),'size':p.stat().st_size,'sha256':sha(p)}
                         for p in sorted(out.rglob('*')) if p.is_file() and p.name not in ['run.json','results.xml']]
    write_json(out/'run.json',report)
    suite=ET.Element('testsuite',name='WP38-original-only',tests=str(len(report['results'])))
    for row in report['results']:
        case=ET.SubElement(suite,'testcase',name=row['id'])
        status=row['outcome']
        if status.startswith('observed-expected') or status == 'observed-running-user-F1-stop':
            continue
        if status == 'error':
            ET.SubElement(case,'failure',message=row.get('error','original experiment failed'))
        else:
            ET.SubElement(case,'skipped',message=status+'; not original/product acceptance')
    ET.indent(suite);ET.ElementTree(suite).write(out/'results.xml',encoding='utf-8',xml_declaration=True)


def run(args):
    if not args.allow_vm or not args.authorization_note.strip():
        raise PermissionError('No VM launch: explicit root release, --allow-vm and --authorization-note required')
    offline_check()
    if not re.fullmatch('[A-Za-z0-9_-]{1,48}',args.run_id) or not 8 <= args.timeout_seconds <= 30:
        raise ValueError('Invalid unique run ID or 8–30 second probe budget')
    qmp,guest,private=configure(args.primary_root.resolve())
    out=OUT/'runs'/args.run_id
    if out.exists():raise FileExistsError('Prior evidence is immutable; choose a new run ID')
    out.mkdir(parents=True)
    sources=[{'path':'scripts/reference/macro_session.py','sha256':sha(Path(__file__))}]+PINS
    for pin in sources:
        raw=git_blob(pin['commit'],pin['path']) if 'commit'in pin else (ROOT/pin['path']).read_bytes()
        target=out/'runner-source'/pin['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
    report={'run_id':args.run_id,'scope':'original-reference-only','wordling_tested':False,
            'full_parity':False,'physical_input_qualified':False,'authorization_note':args.authorization_note,
            'started_at':datetime.now(timezone.utc).isoformat(),'baseline_id':'wp51-dos-us-1992-03-09',
            'sources':sources,'shared_lock':str(private/'session1.lock'),'results':[]}
    macro,status=fixture_for(args.case)
    assets=[]
    if macro:
        f=out/'input/M38.WPM';f.parent.mkdir();f.write_bytes(macro);assets=[('M38.WPM',f)]
    report['fixture_status']=status
    old_handler=signal.signal(signal.SIGALRM,timeout_signal)
    try:
        with exclusive(private):
            report['master_before']={n:sha(guest.MASTER/n)for n in ['boot.img','harddisk.img']}
            for repetition in [1,2]:
                directory=out/(args.case+'-'+str(repetition));directory.mkdir()
                work=private/'runs'/('wp38-'+args.run_id)/(args.case+'-'+str(repetition))
                row={'id':directory.name,'case':args.case,'repetition':repetition,'outcome':'error'}
                p=None;started=False
                try:
                    if qmp.SOCKET.exists() or work.exists():raise RuntimeError('Prior own runtime/run exists; do not borrow or stop unknown guest')
                    started=True;row['qemu_argv']=fresh_start(qmp,guest,work,assets)
                    from smoke import Probe
                    from extended import save_as
                    with qmp.QMP() as q:
                        p=Probe(q,directory)
                        signal.setitimer(signal.ITIMER_REAL,120)
                        p.key('f3');p.q.wait_for('WP 5.1   03/09/92');p.capture('selected-release')
                        p.key('spc');p.q.wait_absent('Press any letter')
                        seed_buffers(p,save_as)
                        signal.setitimer(signal.ITIMER_REAL,args.timeout_seconds)
                        row['outcome']=act(args.case,p)
                        exports_after(p,save_as)
                except HostContainment as e:
                    row['outcome']='host-contained';row['error']=str(e)
                except Exception as e:
                    row['outcome']='error';row['error']=str(e)
                finally:
                    signal.setitimer(signal.ITIMER_REAL,0)
                    if started:
                        if row['outcome'] in ['error','host-contained'] and qmp.SOCKET.exists():
                            try:
                                with qmp.QMP() as q:q.capture(directory/'failure-or-containment-raw')
                            except Exception as e:row['failure_capture_error']=str(e)
                        try:row['stop_method']=stop_owned(qmp,guest);row['guest_stopped']=True
                        except Exception as e:
                            row['stop_error']=str(e);raise
                    if (work/'settings-before.SET').exists():
                        row['private_settings']=[{'private_path':str(work/'settings-before.SET'),'sha256':sha(work/'settings-before.SET'),'publication':'metadata only'}]
                        row['private_settings'].append(settings_snapshot(work,'after'))
                    if p:
                        row['trace'],row['checks']=p.trace,p.checks
                        row['native_exports']=[]
                        for name,host in dict(p.exports).items():
                            target=directory/host
                            proc=subprocess.run(['mcopy','-i',str(work/'harddisk.img')+'@@1048576','::OUT/'+name,str(target)],capture_output=True,timeout=15)
                            if proc.returncode:
                                row['outcome']='error';row['error']='Native export failed: '+name
                            row['native_exports'].append({'guest_name':name,'host':str(target.relative_to(out)),
                                'exit_code':proc.returncode,'sha256':sha(target)if target.exists()else None,
                                'stderr':proc.stderr.decode(errors='replace')})
                    report['results'].append(row)
            report['master_after']={n:sha(guest.MASTER/n)for n in ['boot.img','harddisk.img']}
            if report['master_before']!=report['master_after']:raise RuntimeError('Master identity drift')
        # Lock released immediately after final stop/extraction, before offline audit.
        report['lock_released_before_offline_audit']=True
        from document import plain_merge
        for row in report['results']:
            if row['outcome'].startswith('observed-expected') or row['outcome']=='observed-running-user-F1-stop':
                try:
                    data={}
                    for n in ['D1AFTER','D2AFTER']:
                        item=next(x for x in row['native_exports']if x['guest_name']==n and x['exit_code']==0)
                        data[n]=plain_merge((out/item['host']).read_bytes())
                    expected1=DOC1+('ABC'if args.case=='run-doc1'else '')
                    expected2=DOC2+('ABCABCABC'if args.case=='repeat-doc2'else '')
                    if row['outcome']=='observed-running-user-F1-stop':
                        if not data['D1AFTER']['ascii_text'].startswith(DOC1+'MSLIVE') or 'USERREADY'not in data['D1AFTER']['ascii_text'] or 'MSTAIL'in data['D1AFTER']['ascii_text']:
                            raise ValueError('Partial native stop result differs from bounded witnesses')
                    elif data['D1AFTER']['ascii_text']!=expected1:
                        raise ValueError('Doc1 native target effect mismatch')
                    if data['D2AFTER']['ascii_text']!=expected2:raise ValueError('Doc2 native target/preservation mismatch')
                    row['offline_native_inspections']=data
                except Exception as e:
                    row['outcome']='error';row['error']='Offline native audit: '+str(e)
    finally:
        signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,old_handler)
        seal(out,report)
    return report


def result(path):
    report=json.loads(path.read_text());base=path.parent
    if report.get('scope')!='original-reference-only' or report.get('wordling_tested') is not False:
        raise ValueError('Unexpected evidence scope')
    for record in report['artifacts']:
        p=base/record['path']
        if not p.resolve().is_relative_to(base.resolve()) or p.is_symlink() or p.stat().st_size!=record['size'] or sha(p)!=record['sha256']:
            raise ValueError('Evidence drift: '+record['path'])
    return {'result':'sealed-original-only-artifacts-valid','repetitions':len(report['results']),
            'outcomes':[r['outcome']for r in report['results']],'wordling_tested':False,'full_m1_accepted':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('check')
    sub.add_parser('plan')
    p=sub.add_parser('result');p.add_argument('manifest',type=Path)
    p=sub.add_parser('run');p.add_argument('run_id');p.add_argument('--case',choices=[r['id']for r in recipes()],required=True)
    p.add_argument('--allow-vm',action='store_true');p.add_argument('--authorization-note',default='')
    p.add_argument('--primary-root',type=Path,default=PRIMARY);p.add_argument('--timeout-seconds',type=int,default=20)
    args=parser.parse_args()
    try:
        value=offline_check()if args.command=='check'else {'recipes':recipes(),'vm_launched':False}if args.command=='plan'else result(args.manifest)if args.command=='result'else run(args)
        print(json.dumps(value,indent=2,sort_keys=True));return 0
    except Exception as e:
        print(json.dumps({'result':'refused-or-failed','error':str(e),'full_m1_accepted':False}));return 1


if __name__=='__main__':
    sys.exit(main())
