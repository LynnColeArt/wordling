#!/usr/bin/env python3
"""WP23 bounded original mutation witnesses and read-only writer admission audit.

No production serializer/new-document writer. Original resources stay private.
"""
import argparse
from collections import Counter
from contextlib import contextmanager
from datetime import datetime,timezone
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
import time
import unittest

import guest,qmp
from smoke import Probe
from session1 import SessionProbe
from text_layout import LayoutProbe,print_disk
from extended import clean_exit

ROOT=Path(__file__).resolve().parents[2]
PRIMARY=Path(os.environ.get('WORDLING_REFERENCE_PRIMARY','/home/lynn/projects/wordling')).resolve()
PRIVATE=PRIMARY/'research/cache/reference'
OUT=ROOT/'docs/research/continuation/native-edits'
PROFILE=ROOT/'docs/research/reference-environment/environment.json'
ORIGIN=ROOT/'docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5'
ORIGIN_SHA='c6cffde251e03b1f884c8e209afb426fced87d8c633ee4d1e3e4eb7e7c34aa3d'
LIMIT=65536
TOKEN_LIMIT=16384
PACKET_HASHES={7:'',15:'',12:'',6:'',8:''}

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def record(path,base):return {'path':str(Path(path).relative_to(base)),'size':Path(path).stat().st_size,'sha256':sha(path)}
def body_tokens(body):
    if len(body)>TOKEN_LIMIT*3:raise ValueError('Body budget')
    tokens=[];bold=False;p=0;pairs=0
    while p<len(body):
        if len(tokens)>=TOKEN_LIMIT:raise ValueError('Token budget')
        c=body[p]
        if 32<=c<=126:token=body[p:p+1];kind='ASCII'
        elif body[p:p+3]==bytes.fromhex('c30cc3'):
            if bold or pairs:raise ValueError('Nested/repeated Bold outside first grammar')
            bold=True;pairs+=1;token=body[p:p+3];kind='BoldOn'
        elif body[p:p+3]==bytes.fromhex('c40cc4'):
            if not bold:raise ValueError('Unmatched Bold Off')
            bold=False;token=body[p:p+3];kind='BoldOff'
        else:raise ValueError('Unsupported body token at '+str(p))
        tokens.append({'body_offset':p,'kind':kind,'hex':token.hex()});p+=len(token)
    if bold:raise ValueError('Unclosed Bold')
    return tokens

def _inspect(data,admit=False):
    if len(data)>LIMIT:raise ValueError('Input budget')
    if len(data)<16:raise ValueError('Short header')
    if data[:4]!=bytes.fromhex('ff575043') or data[8:16]!=bytes.fromhex('010a000100000000'):raise ValueError('Unsupported header tuple')
    B=struct.unpack_from('<I',data,4)[0]
    if not 16<=B<=len(data):raise ValueError('Body offset bounds')
    spans=[(0,16,'header')];blocks=[];packets=[];seen=set();index=16;ended=False
    while index:
        if index in seen or len(seen)>=8 or not 16<=index<=B-50:raise ValueError('Index cycle/bounds/budget')
        seen.add(index);kind,count,size,nxt=struct.unpack_from('<HHHI',data,index)
        if (kind,count,size)!=(65531,5,50):raise ValueError('Unsupported index header')
        spans.append((index,index+50,'index'));entries=[]
        for n in range(1,5):
            k,length,offset=struct.unpack_from('<HII',data,index+10*n);entries.append({'slot':n,'type':k,'length':length,'offset':offset})
            if ended:
                if (k,length,offset)!=(0,0,0):raise ValueError('Nonzero unused index slot')
                continue
            if k==0:
                if length or offset:raise ValueError('Unsupported terminator payload')
                ended=True;continue
            if not 16<=offset<=B or length>B-offset:raise ValueError('Packet range')
            if k in (65531,65532,65533,65534):raise ValueError('Reserved packet')
            if k==65535 and admit:raise ValueError('Deleted/Fast Save packet is not writer-admitted')
            packets.append({'type':k,'offset':offset,'length':length,'index_offset':index+10*n,'hex':data[offset:offset+length].hex()})
            if length:spans.append((offset,offset+length,'packet'+str(k)))
        blocks.append({'offset':index,'next':nxt,'entries':entries})
        if ended:
            if nxt:raise ValueError('Nonzero next pointer after terminator')
            break
        index=nxt
    ordered=sorted(spans);p=0;coverage_issues=[]
    for a,b,kind in ordered:
        if a!=p:coverage_issues.append({'expected':p,'actual':[a,b],'kind':kind})
        p=max(p,b)
    if p!=B:coverage_issues.append({'expected':p,'tail_end':B})
    if admit and coverage_issues:raise ValueError('Unowned/overlapping prefix span')
    body_refusal=None
    try:tokens=body_tokens(data[B:])
    except ValueError as error:
        if admit:raise
        tokens=[];body_refusal=str(error)
    result={'size':len(data),'sha256':hashlib.sha256(data).hexdigest(),'body_offset':B,'blocks':blocks,'packets':packets,'coverage':ordered,'coverage_issues':coverage_issues,'body_hex':data[B:].hex(),'tokens':tokens,'body_grammar_refusal':body_refusal}
    if admit:
        if len(blocks)!=2 or [x['type'] for x in packets]!=[7,15,12,6,8]:raise ValueError('Unsupported packet set/order')
        by={x['type']:x for x in packets}
        for k,size in [(7,14),(15,86),(12,90),(6,16),(8,2)]:
            if by[k]['length']!=size:raise ValueError('Unsupported packet size')
        source=bounded_native(ORIGIN)
        if len(source)!=334 or hashlib.sha256(source).hexdigest()!=ORIGIN_SHA:raise ValueError('Pinned source changed')
        baseline=inspect(source,False);base={x['type']:bytes.fromhex(x['hex']) for x in baseline['packets']}
        for k in (7,15,12,8):
            actual=bytes.fromhex(by[k]['hex'])
            allowed=[base[k]]
            if k==15:
                alternate=bytearray(base[k]);alternate[21:23]=bytes.fromhex('1172');allowed.append(bytes(alternate))
            if actual not in allowed:raise ValueError('Unqualified resource packet '+str(k))
        flags=bytes.fromhex(by[6]['hex'])
        if flags[0] not in (0,8) or flags[1:8]!=base[6][1:8] or flags[9:]!=base[6][9:]:raise ValueError('Unqualified document flags')
        if flags[8]!=1:raise ValueError('Unqualified printer-select counter')
        font=bytes.fromhex(by[15]['hex']);pool=bytes.fromhex(by[7]['hex'])
        pointer=struct.unpack_from('<H',font,18)[0]
        if pointer>=len(pool) or b'\0' not in pool[pointer:]:raise ValueError('Font pool reference')
        for entry in font[50:86]:
            if entry not in (254,255) and entry>=by[15]['length']//86:raise ValueError('Font AFC reference')
        if font[50+12]!=255:raise ValueError('Unqualified Bold font chaining')
        if bytes.fromhex(by[8]['hex'])!=b'\0\0' or by[8]['offset']+2!=B:raise ValueError('Graphics count/extent')
        result['admission']='conditional-on-independent-WP23-contract-approval; not production writer authority'
    return result

class AdmissionRefusal(ValueError):
    """Research admission refusal; distinct from the approved Go reader Failure."""
    def __init__(self,code,detail):
        self.code=code;self.detail=detail;super().__init__(detail)

def bounded_native(path):
    path=Path(path)
    if not path.is_file():raise AdmissionRefusal('InvalidNativeFraming','Regular native input required')
    with path.open('rb') as stream:return stream.read(LIMIT+1)

def inspect(data,admit=False):
    try:return _inspect(data,admit)
    except AdmissionRefusal:raise
    except ValueError as error:
        text=str(error);lower=text.lower()
        if 'budget' in lower:code='ResourceLimit'
        elif 'header' in lower or 'body offset' in lower:code='InvalidNativeFraming'
        elif 'index' in lower and 'prefix' not in lower:code='InvalidPrefixIndex'
        elif 'packet range' in lower:code='InvalidPrefixExtent'
        elif 'unowned' in lower or 'overlapping' in lower:code='UnsafePrefixOwnership'
        elif any(word in lower for word in ('body token','bold')):code='UnsupportedBodyGrammar'
        elif 'document flags' in lower or 'printer-select counter' in lower:code='UnsupportedDocumentMetadata'
        elif any(word in lower for word in ('font','resource','pinned source')):code='UnsupportedResourceProfile'
        else:code='UnsupportedPrefixVariant'
        raise AdmissionRefusal(code,text) from error

class MutationProbe(SessionProbe,LayoutProbe):
    def __init__(self,q,out):
        LayoutProbe.__init__(self,q,out);self.counter=0;self.cases=[]
    def snapshot(self,label):
        screen=self.capture(label)
        if 'Block on' in screen or '[Block]' in screen or 'Undelete:' in screen:raise ValueError('Whole-document snapshot requires no block/history preview')
        name=f'N{self.counter:04d}';self.counter+=1
        self.key('f10');self.q.wait_for('Document to be saved:');self.capture(label+'-save-prompt')
        self.type('C:\\OUT\\'+name);self.key('ret');self.q.wait_absent('Document to be saved:');self.capture(label+'-saved')
        self.exports.append((name,name+'.WP5'))
        return name+'.WP5'
    def clear(self):
        self.key('f7');self.q.wait_for('Save document?');self.capture('clear-save-'+str(self.counter));self.key('n');self.q.wait_for('Exit WP?');self.key('n');self.q.wait_until(lambda s:s.splitlines()[0]=='','blank editing after clear')
    def retrieve(self,path,label):
        self.key('shift-f10');self.q.wait_for('Document to be retrieved:');self.type(path);self.key('ret');self.q.wait_absent('Document to be retrieved:');self.capture(label)
    def interop(self,native,label):
        self.clear();self.retrieve('C:\\OUT\\'+Path(native).stem,label+'-retrieve')
        retrieved=self.snapshot(label+'-retrieved-native')
        self.key('home,home,home,up,end');self.type('Z');self.capture(label+'-subsequent-edit')
        edited=self.snapshot(label+'-edited-native')
        name=f'P{self.counter:04d}';self.counter+=1
        print_disk(self,name)
        printed=self.snapshot(label+'-after-print-native')
        return {'input':native,'retrieved':retrieved,'edited':edited,'after_print':printed,'print_stream':name+'.PRN','edit':'Home3 Up End then insert Z; no semantic/layout normalization'}
    def fixture(self,bold=True):
        if bold:self.type('A');self.key('f6');self.type('BC');self.key('f6');self.type('D')
        else:self.type('abc')
        self.q.wait_for('ABCD' if bold else 'abc')
        return self.snapshot('source-'+str(self.counter))
    def at(self,gap,reveal):
        self.key('home,home,home,up')
        if gap:self.key(','.join(['right']*gap))
        if reveal:self.key('alt-f3');self.q.wait_for('Reveal Codes to restore')
    def cancel_block(self,label):
        screen=self.capture(label+'-before-block-cleanup')
        if 'Block on' in screen or '[Block]' in screen:
            self.key('f1');screen=self.capture(label+'-F1-block-cleanup')
            if 'Block on' in screen or '[Block]' in screen or 'Undelete:' in screen:raise ValueError('Unresolved block cancellation context')
    def normal(self):
        if 'Reveal Codes to restore' in self.q.text(qmp.RUNTIME/'inspect'):self.key('alt-f3')

def settings(p):
    p.key('f3');p.q.wait_for('WP 5.1   03/09/92');p.setting('release');p.key('spc')
    # Capture the actual unchanged profile instead of injecting layout codes.
    for keys,label in [('shift-f7,s','printer'),('shift-f8,3,3','initial-font')]:
        p.key(keys);p.setting(label)
        for level in range(4):
            screen=p.q.text(qmp.RUNTIME/'inspect')
            if 'Doc 1 Pg' in screen and 'Selection:' not in screen:break
            if 'Save document?' in screen:raise ValueError('Unexpected exit while leaving settings')
            p.key('f7');p.capture('settings-return-'+label+'-'+str(level))
        else:raise ValueError('Settings did not return to editing')
    p.key('shift-f8,2');p.setting('paper-margins');p.key('f7');p.q.wait_for('Doc 1')
    p.key('shift-f8,1');p.setting('line-settings');p.key('f7');p.q.wait_for('Doc 1')


def run_modes(p):
    source=p.fixture(False);p.at(1,False);p.key('insert');p.q.wait_for('Typeover');p.type('X');p.q.wait_for('aXc');middle=p.snapshot('ascii-typeover')
    p.key('insert');p.q.wait_absent('Typeover');p.type('Y');p.q.wait_for('aXYc');final=p.snapshot('ascii-insert')
    p.cases.append({'id':'ascii-modes','case_id':'CMD51-046','source':source,'intermediate':middle,'final':final,'expected_body_hex':b'aXYc'.hex(),'interop':p.interop(final,'ascii')})


def run_boundaries(p):
    for view in (False,True):
      for mode in ('insert','typeover'):
       for gap in (1,2,4,5):
        label=f'boundary-{int(view)}-{mode}-g{gap}'
        if p.cases:p.normal();p.clear()
        source=p.fixture();p.at(gap,view);p.capture(label+'-before')
        if mode=='typeover':p.key('insert');p.q.wait_for('Typeover')
        p.type('X');p.capture(label+'-after')
        if mode=='typeover':p.key('insert');p.q.wait_absent('Typeover')
        final=p.snapshot(label+'-final');p.normal()
        p.cases.append({'id':label,'case_id':'CMD51-047','source':source,'final':final,'gap':gap,'view':'reveal' if view else 'normal','mode':mode,'interop':p.interop(final,label)})


def run_deletions(p):
    for view in (False,True):
     for gap,key in [(1,'delete'),(4,'delete'),(2,'backspace'),(5,'backspace')]:
      label=f'delete-{int(view)}-{key}-g{gap}'
      if p.cases:p.normal();p.clear()
      source=p.fixture();p.at(gap,view);p.capture(label+'-before');p.key(key);p.capture(label+'-after')
      question=p.q.text(qmp.RUNTIME/'inspect')
      if 'Delete [' in question and '? No (Yes)' in question:
          p.capture(label+'-code-question');p.key('y');p.q.wait_absent('? No (Yes)');p.capture(label+'-confirmed')
      final=p.snapshot(label+'-final');p.normal()
      p.cases.append({'id':label,'case_id':'CMD51-200' if key=='delete' else 'CMD51-201','source':source,'final':final,'gap':gap,'key':key,'view':'reveal' if view else 'normal','interop':p.interop(final,label)})


def run_blocks(p):
    for start,width,cid in [(1,1,'CMD51-202'),(4,1,'CMD51-203'),(1,4,'CMD51-204')]:
     for answer in ('y','n','f1','esc'):
      label=f'block-{start}-{width}-{answer}'
      if p.cases:p.normal();p.clear()
      source=p.fixture();p.at(start,True);p.key('alt-f4');p.q.wait_for('Block');p.key(','.join(['right']*width));p.capture(label+'-selection');p.key('backspace');p.q.wait_for('Delete Block?');p.capture(label+'-question')
      p.key(answer);p.q.wait_absent('Delete Block?');p.capture(label+'-result');p.cancel_block(label);final=p.snapshot(label+'-final');p.normal()
      p.cases.append({'id':label,'case_id':cid,'source':source,'final':final,'range':[start,start+width],'answer':answer,'interop':p.interop(final,label)})


def browse(p,label,previous=0,restore=False):
    p.key('f1');screen=p.capture(label+'-opened');previews=[]
    active='Undelete:' in screen
    if active:
        previews.append(screen.splitlines()[0])
        for i in range(previous):
            p.key('2');screen=p.capture(label+'-previous-'+str(i));previews.append(screen.splitlines()[0])
        p.key('1' if restore else 'f1');p.q.wait_absent('Undelete:');p.capture(label+'-returned')
    return {'label':label,'history_prompt':active,'preview_first_lines':previews,'restore':restore}

def run_history(p,variant):
    # Each history variant starts on its own fresh master: no clear/retrieve
    # assumption can erase earlier deletions. Snapshot/save actions are explicit.
    source=p.fixture(variant in ('repair','refuse'))
    records=[];stages=[]
    if variant=='empty':
        records.append(browse(p,'no-history'))
    elif variant in ('one','two','save-nav','consume'):
        p.at(0,False);p.key('delete');p.capture('first-delete')
        if variant=='save-nav':stages.append(p.snapshot('after-delete-save'))
        if variant in ('two','save-nav','consume'):
            p.key('right,delete');p.capture('second-delete')
        records.append(browse(p,'fewer-entries',previous=2))
        records.append(browse(p,'restore-first',restore=True));p.capture('first-restored-before-save')
        records.append(browse(p,'after-restore-consumption-before-save',previous=1));stages.append(p.snapshot('first-restored-after-history-browse'))
        if variant=='consume':
            records.append(browse(p,'restore-again-after-save',restore=True));p.capture('second-restored-before-save')
            records.append(browse(p,'after-second-restore-before-save',previous=2));stages.append(p.snapshot('second-restored-after-history-browse'))
    else:
        p.at(1,True);p.key('alt-f4,right,backspace');p.q.wait_for('Delete Block?');p.capture('history-block-question')
        p.key('y' if variant=='repair' else 'n');p.q.wait_absent('Delete Block?');p.capture('history-block-result')
        records.append(browse(p,'history-after-'+variant))
        p.capture('history-context-after-first-F1')
        if variant=='refuse':records.append(browse(p,'normal-F1-after-block-cancel'))
    final=p.snapshot('history-final');p.normal()
    p.cases.append({'id':'history-'+variant,'case_id':'CMD51-043' if variant not in ('repair','refuse') else 'CMD51-202','source':source,'intermediates':stages,'final':final,'history':records,'interop':p.interop(final,'history-'+variant)})

def run_cal_block(p):
    source=p.fixture();p.at(1,True);p.key('alt-f4,right,backspace');p.q.wait_for('Delete Block?');p.capture('cal-block-question');p.key('n');p.q.wait_absent('Delete Block?');p.capture('cal-block-no');p.cancel_block('cal-no')
    final=p.snapshot('cal-block-final');p.normal()
    p.cases.append({'id':'cal-block-no','case_id':'CMD51-202','source':source,'final':final,'interop':p.interop(final,'cal-block')})


def configure():
    for module in (guest,qmp):module.RUNTIME=PRIVATE/'runtime';module.SOCKET=PRIVATE/'runtime/qmp.sock'
    guest.MASTER=PRIVATE/'master';guest.PROFILE=PROFILE

@contextmanager
def exclusive():
    configure();PRIVATE.mkdir(exist_ok=True,parents=True)
    with (PRIVATE/'session1.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);yield

def execute(run_id,recipe,custom=None,prepared=None):
    if not re.fullmatch('[A-Za-z0-9_-]+',run_id):raise ValueError('Unsafe run identity')
    directory=OUT/'runs'/run_id;work=PRIVATE/'native-edit-runs'/run_id
    if directory.exists() or work.exists():raise FileExistsError('Fresh identity required')
    directory.mkdir(parents=True)
    if prepared:
        inputs=directory/'inputs';inputs.mkdir()
        for name,key in [('candidate.WP5','candidate_bytes'),('provenance.json','provenance_bytes'),('expectations.json','expectations_bytes'),('reference.PRN','reference_bytes')]:
            (inputs/name).write_bytes(prepared[key])
    r={'run_id':run_id,'recipe':recipe,'started_at':datetime.now(timezone.utc).isoformat(),'scope':'original-reference-only','wordling_tested':False,'result':'incomplete','source_baseline':'wp51-dos-us-1992-03-09','master_before':{n:sha(PRIVATE/'master'/n) for n in ('boot.img','harddisk.img')},'profile_sha256':sha(PROFILE),'runtime':{'socket':str(qmp.SOCKET),'lock':str(PRIVATE/'session1.lock')},'runner_sources':[]}
    for source in sorted((ROOT/'scripts/reference').glob('*.py')):
        target=directory/'runner-source'/source.name;target.parent.mkdir(exist_ok=True);shutil.copyfile(source,target);r['runner_sources'].append(record(target,directory))
    for source in sorted(OUT.glob('*.py')):
        target=directory/'runner-source'/('wp23-'+source.name);shutil.copyfile(source,target);r['runner_sources'].append(record(target,directory))
    shutil.copyfile(PROFILE,directory/'environment.json');p=None
    original_arguments=guest.arguments;seed=None
    if prepared:
        work.mkdir(parents=True);seed=work/'candidate.img'
        subprocess.run(['mformat','-C','-i',str(seed),'-f','1440','::'],check=True,capture_output=True)
        subprocess.run(['mcopy','-i',str(seed),str(directory/'inputs/candidate.WP5'),'::CANDIDAT'],check=True,capture_output=True)
        r['candidate']=prepared['metadata'];r['candidate_source_path']=str(prepared['candidate_path']);r['seed_before']=sha(seed)
        guest.arguments=lambda boot,disk:original_arguments(boot,disk)+['-drive',f'file={seed},format=raw,if=floppy,index=1,readonly=on']
    try:
      with exclusive():
        r['qemu_argv']=guest.start(work)
        try:
          with qmp.QMP() as q:
            p=MutationProbe(q,directory);settings(p)
            if custom:custom(p)
            elif recipe.startswith('history-'):run_history(p,recipe.removeprefix('history-'))
            else:{'modes':run_modes,'boundaries':run_boundaries,'deletions':run_deletions,'blocks':run_blocks,'cal-block':run_cal_block}[recipe](p)
            clean_exit(p);r['clean_exit']=True;r['result']='observed'
        except Exception:
            try:
                with qmp.QMP() as q:q.capture(directory/'diagnostic-error')
            except Exception as capture_error:r['diagnostic_capture_error']=str(capture_error)
            raise
        finally:guest.stop()
        r['exports']=[]
        for src,name in p.exports:
            target=directory/name
            subprocess.run(['mcopy','-i',str(work/'harddisk.img')+'@@1048576','::OUT/'+src,str(target)],check=True,capture_output=True)
            r['exports'].append(record(target,directory))
        r['resources']=[]
        for name in ['WP.EXE','WP.FIL','WP.DRS','STANPRIN.PRS','WP{WP}.SET']:
            raw=subprocess.check_output(['mtype','-i',str(work/'harddisk.img')+'@@1048576','::WP51/'+name]);r['resources'].append({'path':name,'size':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    except Exception as error:
        r['error']=str(error);r['result']='incomplete'
    finally:
        guest.arguments=original_arguments
        if seed:r['seed_after']=sha(seed);r['seed_unchanged']=r['seed_before']==r['seed_after']
        if p:r.update(trace=p.trace,checks=p.checks,settings=p.settings,cases=p.cases)
        r['master_after']={n:sha(PRIVATE/'master'/n) for n in ('boot.img','harddisk.img')};r['master_unchanged']=r['master_before']==r['master_after']
        r['artifacts']=[record(x,directory) for x in sorted(directory.rglob('*')) if x.is_file()]
        (directory/'run.json').write_text(json.dumps(r,indent=2)+'\n')
    print(run_id,r['result'],r.get('error',''),flush=True)
    return r


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    run=sub.add_parser('run');run.add_argument('run_id');run.add_argument('recipe',choices=['modes','boundaries','deletions','blocks','cal-block',*['history-'+x for x in ('empty','one','two','save-nav','consume','repair','refuse')]])
    candidate=sub.add_parser('candidate');candidate.add_argument('run_id');candidate.add_argument('--candidate',required=True);candidate.add_argument('--provenance',required=True);candidate.add_argument('--expectations',required=True)
    check=sub.add_parser('inspect');check.add_argument('path');check.add_argument('--admit',action='store_true')
    args=parser.parse_args();configure()
    if args.command=='candidate':
        sys.path.insert(0,str(OUT));import candidate_mode
        prepared=candidate_mode.prepare(args.candidate,args.provenance,args.expectations)
        r=execute(args.run_id,'candidate',lambda p:candidate_mode.run(p,prepared),prepared)
        comparison=candidate_mode.compare(OUT/'runs'/args.run_id,r) if r['result']=='observed' else {'accepted':False,'run_error':r.get('error')}
        (OUT/'runs'/args.run_id/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
        raise SystemExit(0 if comparison['accepted'] else 1)
    elif args.command=='inspect':
        try:result=inspect(bounded_native(args.path),args.admit)
        except AdmissionRefusal as error:
            print(json.dumps({'admission':'refused','code':error.code,'detail':error.detail},indent=2));raise SystemExit(2)
        print(json.dumps(result,indent=2))
    else:raise SystemExit(0 if execute(args.run_id,args.recipe)['result']=='observed' else 1)

if __name__=='__main__':main()
