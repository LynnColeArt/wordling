#!/usr/bin/env python3
"""Bounded original text-layout/print experiments; no Wordling layout claims.

Uses fresh fingerprinted guest copies and the existing short shared QMP runtime.
Every accepted observation needs two fresh repetitions. Diagnostic calibration
captures are explicitly incomplete and never substitute for accepted probes.
"""
import argparse
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import random
import shutil
import struct
import subprocess
import time
import unittest
import tracemalloc

import guest
import qmp
from smoke import Probe
from document import prefix
from extended import clean_exit

ROOT = Path(__file__).resolve().parents[2]
PRIMARY = Path(os.environ.get('WORDLING_REFERENCE_PRIMARY', '/home/lynn/projects/wordling')).resolve()
PRIVATE = PRIMARY / 'research/cache/reference'
PROFILE = ROOT / 'docs/research/reference-environment/environment.json'
OUT = ROOT / 'docs/research/continuation/text-layout'
MASTER = PRIVATE / 'master'
LIMIT = 16 << 20
TOKEN_LIMIT = 65536
WIDTHS = (4, 9, 11, 3, 3, 5, 6, 7, 4, 5, 6, 6, 8, 10, 10, 12)
SINGLE = {0x0a:'hard-return',0x0b:'soft-page',0x0c:'hard-page',0x0d:'soft-return',
          0x8c:'hard-return-soft-page',0x90:'deletable-soft-return',
          0x91:'deletable-soft-page',0x92:'forward-format-deletable-page',0x99:'dormant-hard-return'}

# These are entered test inputs, never inferred original defaults. Fixed line
# height remains a requested document setting, not a claim about printer output.
INTENDED = {'paper':'original Standard definition with Letter dimensions', 'width_inches':'8.5','height_inches':'11',
            'orientation':'portrait','left_inches':'1','right_inches':'1',
            'top_inches':'1','bottom_inches':'1','justification':'Left',
            'hyphenation':False,'line_spacing':'1','line_height_inches':'0.2',
            'baseline_placement':False,'leading_adjustment':'0',
            'printer':'Standard Printer','base_font':'Courier 10cpi',
            'page_number_position':'Bottom Center','page_number_start':'1'}

VARIANTS = {
 'L1-HR':{'cases':['CMD51-111','CMD51-197'],'text':'alpha\nbeta','kind':'returns'},
 'L1-WRAP-L3-LR':{'cases':['CMD51-111','CMD51-197','CMD51-162'],'text':'word '*80,'kind':'lr'},
 'L2-HP':{'cases':['CMD51-112','CMD51-197','CMD51-165'],'text':'BEFORE','kind':'hard-page'},
 'L2-HP-LONG':{'cases':['CMD51-112','CMD51-197','CMD51-165'],'text':'BEFORE','kind':'hard-page-prepend','prepend':'word '*80},
 'L2-AUTO':{'cases':['CMD51-197','CMD51-165'],'text':''.join(f'P{i:03}\n' for i in range(1,101)),'kind':'automatic-pages'},
 'L2-DORMANT':{'cases':['CMD51-111','CMD51-197'],'text':''.join(f'P{i:03}\n' for i in range(1,101)),'kind':'dormant-return','variation':'Insert an empty paragraph at the observed first line of page2, then change top margin1 to1.2 inches to move its boundary; stop if no actual dormant return is observed.'},
 'L3-TB':{'cases':['CMD51-163'],'text':'word '*80,'kind':'tb'},
 'L4-ABS':{'cases':['CMD51-101','CMD51-103'],'kind':'tabs','mode':'absolute','stops':['2','3']},
 'L4-REL':{'cases':['CMD51-101','CMD51-103'],'kind':'tabs','mode':'relative','stops':['1','2']},
}


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def entry(path, root):
    return {'path':str(Path(path).relative_to(root)),'bytes':Path(path).stat().st_size,'sha256':sha(path)}


def configure():
    runtime = PRIVATE/'runtime'
    for module in (guest,qmp):
        module.RUNTIME=runtime
        module.SOCKET=runtime/'qmp.sock'
    guest.MASTER,guest.PROFILE=MASTER,PROFILE


@contextmanager
def exclusive():
    configure()
    PRIVATE.mkdir(parents=True,exist_ok=True)
    with (PRIVATE/'session1.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        yield


def annotate(data):
    """Read only complete outer tokens; never scan arbitrary opaque payload.

    This diagnostic is not the Go reader or a general semantic decoder. Exact
    outer widths/limits follow approved WP01; only listed one-byte identities and
    D4/00 page-number fields are annotated. All complete opaque bytes survive.
    """
    if len(data)>LIMIT or len(data)<16:
        raise ValueError('Native input bounds')
    try:info=prefix(data)
    except (struct.error,StopIteration,IndexError) as exc:raise ValueError('Unsupported prefix metadata') from exc
    start=info['document_offset']
    tokens=[];counts=Counter();pages=[];text=[];q=start
    while q<len(data):
        if len(tokens)>=TOKEN_LIMIT:raise ValueError('Token budget')
        code=data[q]
        if code in (0,0x7f):raise ValueError('Malformed standalone native token')
        if code<0xc0:
            width=1
        elif code<0xd0:
            width=WIDTHS[code-0xc0]
            if width>len(data)-q or data[q+width-1]!=code:raise ValueError('Malformed fixed frame')
        else:
            if len(data)-q<4:raise ValueError('Short variable header')
            length=struct.unpack_from('<H',data,q+2)[0]
            if length<4 or length+4>len(data)-q:raise ValueError('Variable frame bounds')
            width=length+4
            if data[q+length:q+width]!=struct.pack('<HBB',length,data[q+1],code):raise ValueError('Variable trailer')
        raw=data[q:q+width]
        kind=SINGLE.get(code,'ascii' if 0x20<=code<=0x7e else 'opaque') if width==1 else 'opaque-function'
        token={'offset':q,'bytes':width,'hex':raw.hex(),'kind':kind}
        if kind=='ascii':text.append(chr(code))
        elif width==1 and code in SINGLE:text.append('['+kind+']')
        if code==0xd4 and len(raw)>=14 and raw[1]==0:
            number=struct.unpack_from('<H',raw,8)[0]
            token['formatter_page_number']=number
            pages.append({'offset':q,'page':number})
        counts[kind]+=1
        tokens.append(token);q+=width
    return {'scope':'outer-token-diagnostic-only','document_offset':start,
            'body_sha256':hashlib.sha256(data[start:]).hexdigest(),
            'counts':dict(counts),'formatter_pages':pages,'annotated_text':''.join(text),
            'tokens':tokens,'unresolved':'Opaque payloads, field-specific units and physical geometry remain unvalidated.'}


def stream_diagnostic(data):
    """Retain exact text-only stream bytes; FF chunks are not inferred pages."""
    if len(data)>LIMIT:raise ValueError('Print stream diagnostic budget')
    controls=Counter(byte for byte in data if byte<0x20 or byte>0x7e)
    return {'scope':'raw-stream-diagnostic-only','bytes':len(data),
            'sha256':hashlib.sha256(data).hexdigest(),
            'control_byte_counts':{f'{key:02x}':value for key,value in sorted(controls.items())},
            'hex':data.hex(),'ascii_if_all_ascii':data.decode('ascii') if data.isascii() else None,
            'form_feed_chunk_lengths':[len(chunk) for chunk in data.split(b'\x0c')],
            'unresolved':'CR/LF/FF segmentation is a raw byte observation, not proof of physical origin/advance or page count; initialization/terminators remain in the stream.'}


class LayoutProbe(Probe):
    def __init__(self,q,out):
        super().__init__(q,out)
        self.states=[]
        self.settings=[]

    def capture(self,label):
        self.trace.append({'capture':label,'stable_text_seconds':0.4,'timeout_seconds':60})
        last=since=None
        def stable(screen):
            nonlocal last,since
            if 'Repositioning' in screen:last=since=None;return False
            if screen!=last:last,since=screen,time.monotonic();return False
            return time.monotonic()-since>=0.4
        self.q.wait_until(stable,'stable text before '+label,timeout=60)
        return self.q.capture(self.out/label)

    def setting(self,label):
        screen=self.capture('settings-'+label)
        self.settings.append({'label':label,'capture':'settings-'+label+'/screen.txt','screen_sha256':sha(self.out/('settings-'+label)/'screen.txt')})
        return screen

    def screen_step(self,keys,label,needle=None):
        self.key(keys)
        if needle:self.q.wait_for(needle)
        return self.setting(label)


def save_native(p,name):
    p.key('f10');p.q.wait_for('Document to be saved:');p.capture(name+'-save-prompt')
    p.type('C:\\OUT\\'+name);p.key('ret');p.q.wait_absent('Document to be saved:')
    p.capture(name+'-saved');p.exports.append((name,name+'.WP5'))


def format_screen(p,section,label):
    return p.screen_step('shift-f8,'+section,label)


def set_lr(p,left,right,label):
    format_screen(p,'1',label+'-line')
    p.key('7');p.capture(label+'-left-prompt');p.type(left+'"');p.key('ret')
    p.capture(label+'-right-prompt');p.type(right+'"');p.key('ret')
    screen=p.setting(label+'-accepted')
    p.check('Accepted '+label+' exact left/right inches',bool(re.search(r'Margins - Left\s+'+re.escape(left)+r'"\n\s+Right\s+'+re.escape(right)+r'"',screen)))
    p.key('f7');p.q.wait_for('Doc 1')


def set_tb(p,top,bottom,label):
    format_screen(p,'2',label+'-page')
    p.key('5');p.capture(label+'-top-prompt');p.type(top+'"');p.key('ret')
    p.capture(label+'-bottom-prompt');p.type(bottom+'"');p.key('ret')
    screen=p.setting(label+'-accepted')
    p.check('Accepted '+label+' exact top/bottom inches',bool(re.search(r'Margins - Top\s+'+re.escape(top)+r'"\n\s+Bottom\s+'+re.escape(bottom)+r'"',screen)))
    p.key('f7');p.q.wait_for('Doc 1')


def baseline_settings(p):
    """Strict captured inputs; calibrated menu choices must remain visible."""
    p.key('f3');p.q.wait_for('WP 5.1   03/09/92');p.setting('help-release');p.key('spc')
    # Printer selection/list and initial font are captured before choosing.
    p.screen_step('shift-f7,s','printer-list','Standard Printer')
    p.key('1');p.setting('printer-selected');p.key('f7');p.q.wait_for('Doc 1')
    format_screen(p,'3','document-format')
    p.key('3');p.q.wait_for('Courier 10cpi');p.setting('initial-base-font-list')
    p.key('1');font=p.setting('initial-base-font-selected')
    p.check('Initial base font selected Courier10cpi','Initial Base Font         Courier 10cpi' in font)
    p.key('f7');p.q.wait_for('Doc 1')
    format_screen(p,'2','paper-page-format')
    p.key('7');p.q.wait_for('Paper');p.setting('paper-list')
    # Selection of the actual Letter definition is calibrated before acceptance.
    p.key('1');paper=p.setting('paper-selected')
    p.check('Selected original paper has Letter dimensions and Standard type','8.5" x 11"' in paper and 'Standard' in paper)
    p.key('f7');p.q.wait_for('Doc 1')
    set_lr(p,'1','1','baseline-lr');set_tb(p,'1','1','baseline-tb')
    format_screen(p,'1','baseline-line')
    p.key('1');p.capture('hyphenation-prompt');p.key('n');p.setting('hyphenation-off')
    p.key('3');p.capture('justification-choice');p.key('1');p.setting('justification-left')
    p.key('4');p.capture('line-height-choice');p.key('2');p.type('0.2"');p.key('ret');p.setting('line-height-fixed')
    p.key('6');p.type('1');p.key('ret');line=p.setting('line-spacing-single')
    for field,value in [('Hyphenation','No'),('Justification','Left'),('Line Height','0.2"'),('Line Spacing','1')]:
        p.check('Accepted line setting '+field,bool(re.search(re.escape(field)+r'\s+'+re.escape(value)+r'(?:\n|$)',line)))
    p.key('f7');p.q.wait_for('Doc 1')
    format_screen(p,'4','other-format');p.key('6');p.setting('printer-functions')
    p.key('5');p.key('n');p.setting('baseline-placement-no')
    p.key('6');p.capture('leading-primary-prompt');p.type('0');p.key('ret')
    p.capture('leading-secondary-prompt');p.type('0');p.key('ret');functions=p.setting('leading-zero')
    p.check('Baseline placementNo and both leading adjustments zero',bool(re.search(r'Baseline Placement for Typesetters\s+No',functions)) and bool(re.search(r'Primary\s+- \[SRt\]\s+0"',functions)) and bool(re.search(r'Secondary - \[HRt\]\s+0"',functions)))
    p.key('f7');p.q.wait_for('Doc 1')
    format_screen(p,'2','numbering-page');p.key('6');p.setting('numbering-menu')
    p.key('1');p.type('1');p.key('ret');p.setting('number-start-one')
    p.key('4');p.capture('number-position-choice');p.key('6');numbering=p.setting('number-position-bottom-center')
    p.check('Arabic number1 and Bottom Center selected',bool(re.search(r'New Page Number\s+1\n',numbering)) and 'Page Number Position Bottom Center' in numbering and 'Page Number Style    ^B' in numbering)
    p.key('f7');p.q.wait_for('Doc 1')


def tab_settings(p,mode,stops):
    format_screen(p,'1','tabs-line');p.key('8');p.setting('tabs-before')
    p.key('t');p.capture('tab-type-choice');p.key('1' if mode=='absolute' else '2')
    p.key('home,home,left,ctrl-end');p.setting('tabs-cleared-'+mode)
    for index,stop in enumerate(stops):
        p.type(stop+'"');p.key('ret');p.setting('tab-stop-'+str(index)+'-'+mode)
    p.key('f7');accepted=p.setting('tabs-accepted-'+mode)
    p.check('Tab mode accepted '+mode,('Abs;' if mode=='absolute' else 'Rel;') in accepted)
    p.key('f7');p.q.wait_for('Doc 1')


def print_disk(p,name):
    p.screen_step('shift-f7,s','print-'+name+'-printer-list','Standard Printer')
    p.key('3');p.setting('print-'+name+'-printer-edit')
    p.key('2');p.capture('print-'+name+'-ports');p.key('8');p.capture('print-'+name+'-other-path')
    p.type('C:\\OUT\\'+name+'.PRN');p.key('ret');p.setting('print-'+name+'-other-accepted')
    p.key('f7,f7');p.setting('print-'+name+'-menu')
    p.key('1');p.q.wait_for('Doc 1');p.capture('print-'+name+'-submitted')
    # Capture the original job status; no elapsed delay is proof of completion.
    p.key('shift-f7,4');p.q.wait_for('No print jobs');jobs=p.setting('print-'+name+'-job-status')
    p.check('Print completed with empty job queue '+name,'Job Number: None' in jobs and 'Additional Jobs Not Shown: 0' in jobs)
    p.key('f7');p.q.wait_for('Doc 1')
    p.exports.append((name+'.PRN',name+'.PRN'))


def state(p,name):
    p.capture(name+'-normal')
    p.key('alt-f3');p.q.wait_for('Reveal Codes to restore');p.capture(name+'-reveal');p.key('alt-f3')
    save_native(p,name+'B')
    print_disk(p,name)
    save_native(p,name+'A')
    p.states.append({'id':name,'native_before_print':name+'B.WP5','native_after_print':name+'A.WP5','print_stream':name+'.PRN'})


def recipe(p,variant):
    baseline_settings(p)
    v=VARIANTS[variant]
    if v['kind']=='tabs':
        tab_settings(p,v['mode'],v['stops'])
        p.type('A');p.key('tab');p.type('B');p.key('tab');p.type('C');p.key('ret')
        p.type('AA');p.key('tab');p.type('BB');p.key('tab');p.type('CC')
    elif v['kind'] in ('automatic-pages','dormant-return'):
        # Let each unique marker reach the original screen before submitting the
        # next paragraph. Long scrolling input otherwise outpaces guest redraw.
        for paragraph in v['text'].splitlines():
            p.type(paragraph);p.q.wait_for(paragraph,timeout=30);p.key('ret')
    else:p.type(v['text'])
    if v['kind'] in ('hard-page','hard-page-prepend'):p.key('ctrl-ret');p.type('AFTER')
    state(p,'BASE')
    if v['kind']=='hard-page-prepend':
        p.key('home,home,up');p.type(v['prepend']);state(p,'CHANGE')
    if v['kind']=='dormant-return':
        p.key('home,home,up,pgdn');p.capture('observed-page-two-first-line')
        p.key('home,home,left,ret');p.capture('blank-at-soft-boundary')
        p.key('alt-f3');p.q.wait_for('Dorm');p.capture('dormant-reveal');p.key('alt-f3')
        state(p,'DORMANT')
        p.key('home,home,up');set_tb(p,'1.2','1','dormant-shift-top')
        state(p,'CHANGE')
    if v['kind'] in ('lr','tb','tabs'):
        p.key('home,home,up')
        if v['kind']=='tb':set_tb(p,'1','1.25','changed-tb')
        else:set_lr(p,'1.25','1.5' if v['kind']=='lr' else '1','changed-lr')
        state(p,'CHANGE')


def archive_sources(out):
    paths=[Path(__file__).resolve(),ROOT/'scripts/reference/guest.py',ROOT/'scripts/reference/qmp.py',ROOT/'scripts/reference/smoke.py',ROOT/'scripts/reference/extended.py',ROOT/'scripts/reference/document.py']
    dest=out/'runner-source';dest.mkdir()
    rows=[]
    for path in paths:
        target=dest/path.name;shutil.copyfile(path,target)
        rows.append({'path':str(path.relative_to(ROOT)),'archive':str(target.relative_to(out)),'sha256':sha(path)})
    return rows


def execute(run_id,variant=None,steps=None):
    if not re.fullmatch('[A-Za-z0-9_-]+',run_id):raise ValueError('Unsafe run ID')
    diagnostic=steps is not None
    out=OUT/('calibration' if diagnostic else 'runs')/run_id
    work=PRIVATE/'text-layout-runs'/run_id
    if out.exists() or work.exists():raise FileExistsError('Choose a fresh run ID')
    out.mkdir(parents=True)
    result={'schema_version':1,'scope':'original-reference-only','wordling_tested':False,
            'run_id':run_id,'variant':variant,'diagnostic_calibration':diagnostic,
            'result':'incomplete','started_at':datetime.now(timezone.utc).isoformat(),
            'intended_settings':INTENDED,'variant_input':VARIANTS.get(variant),
            'source_baseline':'wp51-dos-us-1992-03-09',
            'master_before':{'harddisk.img':sha(MASTER/'harddisk.img'),'boot.img':sha(MASTER/'boot.img')},
            'environment_manifest_sha256':sha(PROFILE),'runner_sources':archive_sources(out),
            'unresolved':['historical DOS unavailable','graphics L5/L7 unavailable','physical geometry and NFR-005 unqualified']}
    shutil.copyfile(PROFILE,out/'environment.json')
    p=None
    try:
        with exclusive():
            result['qemu_argv']=guest.start(work)
            try:
                with qmp.QMP() as q:
                    p=LayoutProbe(q,out)
                    p.capture('initial')
                    if diagnostic:
                        for i,step in enumerate(steps):
                            if step.startswith('type:'):p.type(step[5:])
                            else:p.key(step)
                            p.capture(f'step-{i:02}')
                        result['result']='diagnostic-only-unclean-shutdown'
                    else:
                        recipe(p,variant);clean_exit(p)
                        result['clean_original_exit']=True
                        result['result']='observed-local-variant'
            except Exception:
                try:
                    with qmp.QMP() as q:q.capture(out/'error-screen')
                except Exception as capture_error:result['error_capture_failure']=str(capture_error)
                raise
            finally:
                guest.stop()
            if not diagnostic:
                result['exports']=[]
                for source,name in p.exports:
                    path=out/name
                    subprocess.run(['mcopy','-i',str(work/'harddisk.img')+'@@1048576','::OUT/'+source,str(path)],check=True,capture_output=True)
                    result['exports'].append(entry(path,out))
                    if name.endswith('.WP5'):
                        (out/(name+'.annotation.json')).write_text(json.dumps(annotate(path.read_bytes()),indent=2)+'\n')
                    elif name.endswith('.PRN'):
                        (out/(name+'.annotation.json')).write_text(json.dumps(stream_diagnostic(path.read_bytes()),indent=2)+'\n')
                result['states']=p.states
    except Exception as exc:
        result['error']=str(exc)
        result['result']='incomplete'
    finally:
        if p:result.update(trace=p.trace,checks=p.checks,settings=p.settings)
        result['master_after']={name:sha(MASTER/name) for name in ['harddisk.img','boot.img']}
        result['master_unchanged']=result['master_before']==result['master_after']
        result['evidence']=[entry(path,out) for path in sorted(out.rglob('*')) if path.is_file()]
        (out/'run.json').write_text(json.dumps(result,indent=2)+'\n')
    print(run_id,result['result'],result.get('error',''),flush=True)
    return result


def verify(directory):
    directory=Path(directory)
    run=json.loads((directory/'run.json').read_text())
    if run['scope']!='original-reference-only' or run['wordling_tested'] is not False:raise ValueError('Evidence scope')
    if not run['master_unchanged']:raise ValueError('Master changed')
    if sha(directory/'environment.json')!=run['environment_manifest_sha256']:raise ValueError('Environment changed')
    for row in run['evidence']:
        path=directory/row['path']
        if path.stat().st_size!=row['bytes'] or sha(path)!=row['sha256']:raise ValueError('Evidence changed: '+row['path'])
    for row in run['runner_sources']:
        if sha(directory/row['archive'])!=row['sha256']:raise ValueError('Runner archive changed')
    return run


def fuzz(seconds,output):
    """Reproducible seeded mutation workload, separate from original evidence."""
    if not 0<seconds<=60:raise ValueError('Fuzz duration must be in (0,60] seconds')
    path=Path(output)
    if path.exists():raise FileExistsError('Do not replace fuzz evidence')
    source=ROOT/'docs/research/reference-runs/2026-10-29-advanced-03/CMD51-203/ORIGIN.WP5'
    data=source.read_bytes();start=struct.unpack_from('<I',data,4)[0]
    seed=16614;rng=random.Random(seed);deadline=time.monotonic()+seconds
    accepted=refused=max_body=0
    tracemalloc.start()
    while time.monotonic()<deadline:
        body=bytearray(data[start:])
        for _ in range(rng.randrange(1,8)):
            mode=rng.randrange(3)
            if mode==0 and body:body[rng.randrange(len(body))]=rng.randrange(256)
            elif mode==1:body[rng.randrange(len(body)+1):]=rng.randbytes(rng.randrange(64))
            elif body:del body[rng.randrange(len(body)):]
        native=data[:start]+body
        max_body=max(max_body,len(body))
        try:a=annotate(native)
        except ValueError:refused+=1;continue
        accepted+=1
        assert b''.join(bytes.fromhex(t['hex']) for t in a['tokens'])==body
        assert a['body_sha256']==hashlib.sha256(body).hexdigest()
        assert len(a['tokens'])<=TOKEN_LIMIT
    _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    result={'scope':'synthetic-mutated-native-diagnostic-only','wordling_tested':False,
            'random_seed':seed,'seconds_budget':seconds,'accepted':accepted,'refused':refused,
            'peak_tracemalloc_bytes':peak,'source_fixture_sha256':sha(source),
            'runner_sha256':sha(Path(__file__).resolve()),'max_native_bytes':LIMIT,
            'max_diagnostic_tokens':TOKEN_LIMIT,'max_mutated_body_bytes':451,
            'observed_max_mutated_body_bytes':max_body,
            'checks':['no uncaught error','exact opaque/token body reconstruction','exact body hash','bounded token index'],
            'limitations':'Small seeded body mutations only; not exhaustive native validation, original behavior or product memory measurements.'}
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


class Tests(unittest.TestCase):
    def test_known_outer_identities_and_opaque_payload(self):
        source=ROOT/'docs/research/reference-runs/2026-10-29-advanced-03/CMD51-203/ORIGIN.WP5'
        data=source.read_bytes();start=struct.unpack_from('<I',data,4)[0]
        variable=bytes.fromhex('d00108000a0b0c0d080001d0')
        inspected=annotate(data[:start]+variable+bytes([10,11,12,13,0x8c,0x99]))
        self.assertEqual(inspected['counts'],{'opaque-function':1,'hard-return':1,'soft-page':1,'hard-page':1,'soft-return':1,'hard-return-soft-page':1,'dormant-hard-return':1})
        self.assertEqual(inspected['tokens'][0]['hex'],variable.hex())

    def test_bad_framing_and_input_refused(self):
        source=ROOT/'docs/research/reference-runs/2026-10-29-advanced-03/CMD51-203/ORIGIN.WP5'
        data=source.read_bytes();start=struct.unpack_from('<I',data,4)[0]
        for body in [b'\0',b'\x7f',b'\xc3\x0c',b'\xc3\x0c\xc4',bytes.fromhex('d0010300030001d0'),bytes.fromhex('d0010400040002d0')]:
            with self.assertRaises(ValueError):annotate(data[:start]+body)
        for bad in [b'',bytes(LIMIT+1)]:
            with self.assertRaises(ValueError):annotate(bad)

    def test_diagnostic_token_limit(self):
        source=ROOT/'docs/research/reference-runs/2026-10-29-advanced-03/CMD51-203/ORIGIN.WP5'
        data=source.read_bytes();start=struct.unpack_from('<I',data,4)[0]
        a=annotate(data[:start]+b'A'*TOKEN_LIMIT)
        self.assertEqual(len(a['tokens']),TOKEN_LIMIT)
        with self.assertRaises(ValueError):annotate(data[:start]+b'A'*(TOKEN_LIMIT+1))

    def test_print_bytes_not_normalized(self):
        data=b'\x1b@A  \r\nB\rC\n\x0c'
        result=stream_diagnostic(data)
        self.assertEqual(bytes.fromhex(result['hex']),data)
        self.assertEqual(result['form_feed_chunk_lengths'],[len(data)-1,0])
        self.assertEqual(result['control_byte_counts'],{'0a':2,'0c':1,'0d':2,'1b':1})
        self.assertEqual(result['ascii_if_all_ascii'],data.decode('ascii'))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    c=sub.add_parser('calibrate');c.add_argument('run_id');c.add_argument('steps',nargs='*')
    r=sub.add_parser('run');r.add_argument('run_id');r.add_argument('variant',choices=VARIANTS)
    v=sub.add_parser('verify');v.add_argument('directories',nargs='+')
    f=sub.add_parser('fuzz');f.add_argument('--seconds',type=float,default=10);f.add_argument('--output',required=True)
    sub.add_parser('self-test')
    args=parser.parse_args()
    if args.command=='self-test':
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
        raise SystemExit(not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful())
    if args.command=='verify':
        for path in args.directories:verify(path);print(path,'immutable evidence valid')
    elif args.command=='fuzz':fuzz(args.seconds,args.output)
    elif args.command=='calibrate':execute(args.run_id,steps=args.steps)
    else:
        result=execute(args.run_id,args.variant)
        if result['result']!='observed-local-variant':raise SystemExit(1)


if __name__=='__main__':main()
