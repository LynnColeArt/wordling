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

def inspect(data,admit=False):
    if len(data)>LIMIT or len(data)<16:raise ValueError('Input budget/header')
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
        if ended:break
        index=nxt
    ordered=sorted(spans);p=0
    for a,b,kind in ordered:
        if a!=p:raise ValueError('Unowned/overlapping prefix span at '+str(p))
        p=b
    if p!=B:raise ValueError('Unowned prefix tail')
    tokens=body_tokens(data[B:])
    result={'size':len(data),'sha256':hashlib.sha256(data).hexdigest(),'body_offset':B,'blocks':blocks,'packets':packets,'coverage':ordered,'body_hex':data[B:].hex(),'tokens':tokens}
    if admit:
        if len(blocks)!=2 or [x['type'] for x in packets]!=[7,15,12,6,8]:raise ValueError('Unsupported packet set/order')
        by={x['type']:x for x in packets}
        for k,size in [(7,14),(15,86),(12,90),(6,16),(8,2)]:
            if by[k]['length']!=size:raise ValueError('Unsupported packet size')
        source=ORIGIN.read_bytes()
        if sha(ORIGIN)!=ORIGIN_SHA:raise ValueError('Pinned source changed')
        baseline=inspect(source,False);base={x['type']:bytes.fromhex(x['hex']) for x in baseline['packets']}
        for k in (7,15,12,8):
            if bytes.fromhex(by[k]['hex'])!=base[k]:raise ValueError('Unqualified resource packet '+str(k))
        flags=bytes.fromhex(by[6]['hex'])
        if flags[0] not in (0,8) or flags[1:]!=base[6][1:]:raise ValueError('Unqualified document flags')
        font=bytes.fromhex(by[15]['hex']);pool=bytes.fromhex(by[7]['hex'])
        pointer=struct.unpack_from('<H',font,18)[0]
        if pointer>=len(pool) or b'\0' not in pool[pointer:]:raise ValueError('Font pool reference')
        for entry in font[50:86]:
            if entry not in (254,255) and entry>=by[15]['length']//86:raise ValueError('Font AFC reference')
        if font[50+12]!=255:raise ValueError('Unqualified Bold font chaining')
        if bytes.fromhex(by[8]['hex'])!=b'\0\0' or by[8]['offset']+2!=B:raise ValueError('Graphics count/extent')
        result['admission']='conditional-on-independent-WP23-contract-approval; not production writer authority'
    return result

class MutationProbe(SessionProbe,LayoutProbe):
    def __init__(self,q,out):
        LayoutProbe.__init__(self,q,out);self.counter=0;self.cases=[]
    def snapshot(self,label):
        self.capture(label)
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
      source=p.fixture();p.at(gap,view);p.capture(label+'-before');p.key(key);p.capture(label+'-after');final=p.snapshot(label+'-final');p.normal()
      p.cases.append({'id':label,'case_id':'CMD51-200' if key=='delete' else 'CMD51-201','source':source,'final':final,'gap':gap,'key':key,'view':'reveal' if view else 'normal','interop':p.interop(final,label)})


def run_blocks(p):
    for start,width,cid in [(1,1,'CMD51-202'),(4,1,'CMD51-203'),(1,4,'CMD51-204')]:
     for answer in ('y','n','f1','esc'):
      label=f'block-{start}-{width}-{answer}'
      if p.cases:p.normal();p.clear()
      source=p.fixture();p.at(start,True);p.key('alt-f4');p.q.wait_for('Block');p.key(','.join(['right']*width));p.capture(label+'-selection');p.key('backspace');p.q.wait_for('Delete Block?');p.capture(label+'-question')
      p.key(answer);p.q.wait_absent('Delete Block?');p.capture(label+'-result');final=p.snapshot(label+'-final');p.normal()
      p.cases.append({'id':label,'case_id':cid,'source':source,'final':final,'range':[start,start+width],'answer':answer,'interop':p.interop(final,label)})


def configure():
    for module in (guest,qmp):module.RUNTIME=PRIVATE/'runtime';module.SOCKET=PRIVATE/'runtime/qmp.sock'
    guest.MASTER=PRIVATE/'master';guest.PROFILE=PROFILE

@contextmanager
def exclusive():
    configure();PRIVATE.mkdir(exist_ok=True,parents=True)
    with (PRIVATE/'session1.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);yield

def execute(run_id,recipe,custom=None):
    if not re.fullmatch('[A-Za-z0-9_-]+',run_id):raise ValueError('Unsafe run identity')
    directory=OUT/'runs'/run_id;work=PRIVATE/'native-edit-runs'/run_id
    if directory.exists() or work.exists():raise FileExistsError('Fresh identity required')
    directory.mkdir(parents=True)
    r={'run_id':run_id,'recipe':recipe,'started_at':datetime.now(timezone.utc).isoformat(),'scope':'original-reference-only','wordling_tested':False,'result':'incomplete','source_baseline':'wp51-dos-us-1992-03-09','master_before':{n:sha(PRIVATE/'master'/n) for n in ('boot.img','harddisk.img')},'profile_sha256':sha(PROFILE),'runtime':{'socket':str(qmp.SOCKET),'lock':str(PRIVATE/'session1.lock')},'runner_sources':[]}
    for source in sorted((ROOT/'scripts/reference').glob('*.py')):
        target=directory/'runner-source'/source.name;target.parent.mkdir(exist_ok=True);shutil.copyfile(source,target);r['runner_sources'].append(record(target,directory))
    shutil.copyfile(PROFILE,directory/'environment.json');p=None
    try:
      with exclusive():
        r['qemu_argv']=guest.start(work)
        try:
          with qmp.QMP() as q:
            p=MutationProbe(q,directory);settings(p)
            (custom or {'modes':run_modes,'boundaries':run_boundaries,'deletions':run_deletions,'blocks':run_blocks}[recipe])(p)
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
        if p:r.update(trace=p.trace,checks=p.checks,settings=p.settings,cases=p.cases)
        r['master_after']={n:sha(PRIVATE/'master'/n) for n in ('boot.img','harddisk.img')};r['master_unchanged']=r['master_before']==r['master_after']
        r['artifacts']=[record(x,directory) for x in sorted(directory.rglob('*')) if x.is_file()]
        (directory/'run.json').write_text(json.dumps(r,indent=2)+'\n')
    print(run_id,r['result'],r.get('error',''),flush=True)
    return r


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    run=sub.add_parser('run');run.add_argument('run_id');run.add_argument('recipe',choices=['modes','boundaries','deletions','blocks'])
    check=sub.add_parser('inspect');check.add_argument('path');check.add_argument('--admit',action='store_true')
    args=parser.parse_args();configure()
    if args.command=='inspect':print(json.dumps(inspect(Path(args.path).read_bytes(),args.admit),indent=2))
    else:raise SystemExit(0 if execute(args.run_id,args.recipe)['result']=='observed' else 1)

if __name__=='__main__':main()
