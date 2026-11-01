#!/usr/bin/env python3
"""WP43 original genesis research. Offline by default; no serializer/constructor."""
import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

import native_edits as native
import macro_quit as exit_protocol
import macro_session as session

ROOT=Path(__file__).resolve().parents[2]
PRIMARY=Path('/home/lynn/projects/wordling')
OUT=ROOT/'docs/research/continuation/native-genesis'
BASE='1543ac66460b6575b5eec35d53c273a95e641538'
SCOPE='original-reference-only-native-genesis'
LIMIT=65536
ASCII='G43ASCII'


class Refusal(ValueError):
    def __init__(self,code,detail):self.code=code;super().__init__(detail)


def need(ok,code,detail):
    if not ok:raise Refusal(code,detail)


def sha(path):
    with Path(path).open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()


def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def write(path,x):path.write_text(json.dumps(x,indent=2)+'\n')
def same(a,b):return json.dumps(a,sort_keys=True,separators=(',',':'))==json.dumps(b,sort_keys=True,separators=(',',':'))


def cases():
    rows=[('empty-f10-cancel','',None,'F1 at empty filename prompt; no Escape'),
          ('empty-first-save','','G43EMPTY','No cancellation selected'),
          ('ascii-first-retrieve',ASCII,'G43TEXT','No cancellation selected'),
          ('ascii-name-cancel',ASCII,'G43RETRY','Type C:\\OUT\\G43DRAFT; capture caret; F1 at filename; retry distinct G43RETRY'),
          ('ascii-dirty-exit-return',ASCII,'G43DIRTY','F7 then captured Save question F1; no Escape; later explicit F10')]
    return [{'id':name,'repetitions':2,'initial_text':text,'first_save_name':dest,'cancel_branch':cancel,
             'status':'unexecuted-template','native_seed':'none; original typing only; output hash unavailable before guest creation',
             'initial_views':'normal capture, AltF3 empty Reveal, AltF3 return normal; no save/typing',
             'settings_order':'help release before input; read-only printer/font/page/line/tabs/setup AFTER sensitive first-save/cancel interval',
             'interop':bool(text),'constructor_permission':False}for name,text,dest,cancel in rows]


def source_inputs():
    # Actual local import closure; configure dynamically imports qmp/guest explicitly.
    pending=['native_edits','macro_quit','macro_session','qmp','guest'];seen=set()
    while pending:
        name=pending.pop()
        if name in seen:continue
        path=ROOT/'scripts/reference'/str(name+'.py');need(path.is_file(),'MissingHelper',str(path));seen.add(name)
        for node in ast.walk(ast.parse(path.read_text())):
            names=[a.name.split('.')[0]for a in node.names]if isinstance(node,ast.Import)else[node.module.split('.')[0]]if isinstance(node,ast.ImportFrom)and node.module else[]
            pending.extend(n for n in names if(ROOT/'scripts/reference'/str(n+'.py')).is_file()and n not in seen)
    paths=['scripts/reference/'+n+'.py'for n in sorted(seen)]
    paths+=json.loads((OUT/'source-plan.json').read_text())['bound_paths']
    result=[]
    for name in dict.fromkeys(paths):
        raw=subprocess.check_output(['git','--no-optional-locks','-C',str(ROOT),'show',BASE+':'+name])
        need((ROOT/name).read_bytes()==raw,'SourceChanged',name)
        result.append({'path':name,'size':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'git_blob':blob(raw),'commit':BASE})
    for path in [Path(__file__),*sorted(OUT.glob('*.py')),*sorted(OUT.glob('*.go.txt')),*sorted(OUT.glob('*.md')),OUT/'.gitattributes',OUT/'source-plan.json',OUT/'approved-prerequisites.json']:
        raw=path.read_bytes();result.append({'path':str(path.relative_to(ROOT)),'size':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'git_blob':blob(raw),'stage':'owned prelaunch tooling; frozen by reviewed grant'})
    return result


def private_inputs():
    plan=json.loads((OUT/'source-plan.json').read_text());rows=[]
    for row in plan['private_sources']:
        path=PRIMARY/row['path'];need(path.is_file()and sha(path)==row['sha256'],'PrivateSourceChanged',row['path']);rows.append(row)
    profile=json.loads((ROOT/'docs/research/reference-environment/environment.json').read_text())
    for path,want in [(PRIMARY/'research/cache/reference/master/boot.img',profile['master_boot_sha256']),
                      (PRIMARY/'research/cache/reference/master/harddisk.img',profile['master_disk_sha256']),
                      (Path(profile['qemu_binary']['path']),profile['qemu_binary']['sha256']),
                      *[(Path(x['path']),x['sha256'])for x in profile['firmware']]]:
        need(sha(path)==want,'PrivateBaselineChanged',str(path));rows.append({'path':str(path),'size':path.stat().st_size,'sha256':want,'publication':'metadata only'})
    return rows


def check():
    return {'result':'offline-preparation-valid','vm_launched':False,'original_runs_this_invocation':0,'scope':SCOPE,
            'wordling_tested':False,'full_m1_accepted':False,'constructor_ready':False,
            'guest_cap_including_failures':10,'per_guest_seconds':480,'stop_on_first_incomplete':True,
            'cases':cases(),'sources':source_inputs(),'private_sources':private_inputs(),
            'shared_lock':str(PRIMARY/'research/cache/reference/session1.lock'),
            'profile_limits':'Linux/QEMU8.2.2/FreeDOS1.4/March1992 US program/July1992 Standard Printer; no physical input/metrics qualification'}


def state(screen):
    lines=screen.splitlines();need(bool(lines),'UnknownState','No captured original state')
    if exit_protocol.exit_state(screen)=='dos':return 'dos'
    status=lines[-1]
    if status.startswith('Document to be saved:'):return 'filename'
    known=exit_protocol.exit_state(screen)
    need(known!='unknown','UnknownState','Unexpected original state; no guessed key')
    return known


def field_report(raw):
    need(isinstance(raw,bytes)and 16<=len(raw)<=LIMIT,'NativeBounds','Bounded native bytes required')
    info=native.inspect(raw,False)
    ledger=json.loads((ROOT/'docs/research/continuation/native-edits/field-ledger.json').read_text())
    fields=[];unmapped=[]
    for owner,start,end in [('header',0,16),*[(f'packet-{p["type"]}',p['offset'],p['offset']+p['length'])for p in info['packets']]]:
        covered=set()
        for f in ledger['field_coverage']:
            if f['owner']!=owner:continue
            a,b=start+f['offset'],start+f['offset']+f['width']
            if b>end:continue
            covered.update(range(a,b));fields.append({'owner':owner,'absolute_offset':a,'width':b-a,'name':f['name'],
                'representation':f['representation'],'units':f['units'],'references':f['references'],'hex':raw[a:b].hex(),
                'authority':'approved23 field_coverage; SDK locators in its manual-locators.json',
                'genesis_default_classification':'unqualified observed value; not a universal constant',
                'constructor_encoding_permission':False})
        missing=[i for i in range(start,end)if i not in covered]
        if missing:unmapped.append({'owner':owner,'absolute_byte_offsets':missing})
    return {'size':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'body_offset':info['body_offset'],
            'body_hex':info['body_hex'],'blocks':info['blocks'],'coverage_issues':info['coverage_issues'],
            'fields':fields,'unmapped':unmapped,'constructor_ready':False,
            'blocking':'All genesis default classifications/resource/time/command dependencies require independent field argument; matching repeats alone grant no constants'}


def enforce_field_claims(rows):
    # D can report observations; it cannot promote coincidences to constructor defaults.
    for row in rows:
        need(row.get('constructor_encoding_permission')is False,'UnsupportedDefaultInference','No constructor field admission in this observation ledger')
        need(row.get('genesis_default_classification')=='unqualified observed value; not a universal constant',
             'UnsupportedDefaultInference','Observed equality does not prove an original default')


def reader(paths):
    import tempfile
    with tempfile.TemporaryDirectory(prefix='.reader-',dir=OUT)as tmp:
        source=Path(tmp)/'main.go';source.write_bytes((OUT/'reader.go.txt').read_bytes())
        r=subprocess.run(['go','run',str(source),*[str(p)for p in paths]],cwd=ROOT,capture_output=True,text=True,timeout=60)
        need(r.returncode==0,'ReaderExecution',r.stderr);rows=json.loads(r.stdout)
    need(len(rows)==len(paths)and all(x['accepted']is True and x['exact_no_edit_export']is True for x in rows),'ReaderRefusal','Actual approved Go reader failed a required native')
    return rows


def normal(p,label):
    s=p.capture(label);need(state(s)=='main','UnknownState','Expected main document '+label);return s


def save(p,name,label):
    p.key('f10');p.q.wait_for('Document to be saved:');prompt=p.capture(label+'-filename')
    need(state(prompt)=='filename','WrongFilenameState',label)
    p.type('C:\\OUT\\'+name);draft=p.capture(label+'-typed-name');p.key('ret')
    p.q.wait_until(lambda s:state_or_unknown(s)=='main'and 'C:\\OUT\\'+name in s.splitlines()[-1]and'Saving'not in s,'stable named completion '+name,timeout=20)
    normal(p,label+'-complete');p.exports.append((name,name+'.WP5'))
    return {'name':name,'host':name+'.WP5','prompt':label+'-filename','draft':label+'-typed-name','completion':label+'-complete'}


def state_or_unknown(s):
    try:return state(s)
    except Refusal:return 'unknown'


def settings_after(p):
    # approved23 readonly menu observations, NOT text_layout.baseline_settings.
    native.settings(p)
    p.key('shift-f8,1,8');p.setting('tabs-readonly');p.key('f7');p.setting('tabs-return-line');p.key('f7');normal(p,'tabs-return-main')
    p.key('shift-f1');p.setting('setup-readonly');p.key('f7');normal(p,'setup-return-main')


def clear_for_retrieve(p):
    actions=[]
    for i in range(8):
        label='interop-clear-'+str(i);s=p.capture(label);st=state(s)
        if i and st=='main':return actions
        need(st in ['main','save','exit-doc1','exit-doc2','exit-wp'],'UnknownClearState','No clear key guessed')
        key='f7'if st=='main'else'n'if st in ['save','exit-wp']else'y'
        actions.append({'state':st,'key':key,'capture':label});p.key(key)
        p.q.wait_until(lambda x:state_or_unknown(x)not in [st,'unknown'],'captured clear transition',timeout=15)
    raise Refusal('ClearBudget','No original clear/main completion')


def act(plan,p):
    normal(p,'startup-normal');p.key('f3');p.q.wait_for('WP 5.1   03/09/92');p.capture('release');p.key('spc');normal(p,'after-release')
    p.key('alt-f3');p.q.wait_for('Reveal Codes to restore');p.capture('startup-empty-reveal');p.key('alt-f3');normal(p,'startup-empty-normal-restored')
    need((p.out/'startup-normal/screen.txt').read_text().splitlines()[0]=='','NonemptyGenesis','Fresh startup not empty')
    observations={'first':None,'cancelled_name':None,'selected_cancel':'F1 only; no Escape'}
    if plan['initial_text']:p.type(plan['initial_text']);normal(p,'first-ascii-before-save')
    if plan['id']=='empty-f10-cancel':
        p.key('f10');p.q.wait_for('Document to be saved:');p.capture('empty-filename-before-F1');p.key('f1');normal(p,'empty-filename-after-F1')
        observations['expected_absent']=['G43DRAFT'];settings_after(p);return observations
    if plan['id']=='ascii-name-cancel':
        p.key('f10');p.q.wait_for('Document to be saved:');p.capture('cancel-filename-initial');p.type('C:\\OUT\\G43DRAFT');p.capture('cancel-filename-draft');p.key('f1');normal(p,'cancel-return');observations['cancelled_name']='G43DRAFT'
    if plan['id']=='ascii-dirty-exit-return':
        p.key('f7');p.q.wait_for('Save document?');p.capture('dirty-save-question-before-F1');p.key('f1');normal(p,'dirty-save-question-after-F1')
    observations['first']=save(p,plan['first_save_name'],'first-save')
    # First sensitive interval is now complete. No printer/font/settings selection is made.
    settings_after(p)
    observations['expected_absent']=['G43DRAFT']
    if plan['interop']:
        observations['clear_actions']=clear_for_retrieve(p)
        p.retrieve('C:\\OUT\\'+plan['first_save_name'],'original-retrieved')
        observations['resaved']=save(p,'R'+plan['first_save_name'][1:],'retrieve-resave')
        p.key('home,home,home,up,end');p.type('Z');normal(p,'after-subsequent-Z')
        from text_layout import print_disk
        print_disk(p,'G43PRINT');observations['print_stream']='G43PRINT.PRN'
        observations['edited']=save(p,'A'+plan['first_save_name'][1:],'after-print-save')
    return observations


def process_gone(pid):
    f=Path('/proc')/str(pid)/'stat'
    return not f.exists()or f.read_text().split(') ',1)[1].startswith('Z')


def bare_names(text):return {s.rstrip('/').rsplit('/',1)[-1].split('.')[0].upper()for s in text.splitlines()if s.strip()}


def export_stopped(work,directory,exports,rows=None):
    disk=str(work/'harddisk.img')+'@@1048576'
    listing=subprocess.run(['mdir','-b','-i',disk,'::OUT/'],capture_output=True,timeout=15)
    (directory/'OUT-after.txt').write_bytes(listing.stdout);(directory/'OUT-after.stderr').write_bytes(listing.stderr)
    need(listing.returncode==0,'StoppedDirectoryRead','Stopped directory cannot be listed')
    if rows is None:rows=[]
    for name,host in dict(exports).items():
        need(Path(host).name==host and re.fullmatch(r'[A-Z0-9.]{1,12}',name),'ExportPath','Safe declared basename required')
        argv=['mcopy','-i',disk,'::OUT/'+name,str(directory/host)]
        item={'name':name,'host':host,'exit':None,'size':None,'sha256':None};rows.append(item)
        try:r=subprocess.run(argv,capture_output=True,timeout=15)
        except Exception as e:
            item['error']=str(e);write(directory/('extract-'+host+'-failure.json'),{'argv':argv,'error':str(e),'code':type(e).__name__});raise
        (directory/('extract-'+host+'.stdout')).write_bytes(r.stdout);(directory/('extract-'+host+'.stderr')).write_bytes(r.stderr)
        f=directory/host;item.update(exit=r.returncode,size=f.stat().st_size if f.exists()else None,sha256=sha(f)if f.exists()else None)
    return rows


def master_identity(guest):return {n:sha(guest.MASTER/n)for n in ['boot.img','harddisk.img']}


def validate_owned_identity(socket,work,proof):
    need(isinstance(proof,dict)and type(proof.get('pid'))is int and proof['pid']>1
         and proof.get('ownership_validated')is True and proof.get('socket')==str(socket)
         and proof.get('private_work')==str(work)and str(proof.get('start_ticks','')).isdigit(),
         'UnprovenPID','No positively captured owned process; do not infer termination')
    argv=bytes.fromhex(proof.get('cmdline_hex','')).split(b'\0');marker=b'unix:'+str(socket).encode()+b','
    need(any(a.startswith(marker)for a in argv)and
         any(a.startswith(('file='+str(work/'boot.img')+',').encode())for a in argv)and
         any(a.startswith(('file='+str(work/'harddisk.img')+',').encode())for a in argv),
         'UnprovenPID','Captured argv must bind the exact owned socket and both private disks')


def capture_owned_pid(qmp,work):
    pid=int((qmp.RUNTIME/'qemu.pid').read_text())
    need(pid>1,'UnprovenPID','A positive owned PID must be captured')
    proc=Path('/proc')/str(pid);raw=(proc/'cmdline').read_bytes();argv=raw.split(b'\0')
    marker=b'unix:'+str(qmp.SOCKET).encode()+b','
    need(any(a.startswith(marker)for a in argv)and
         any(a.startswith(('file='+str(work/'boot.img')+',').encode())for a in argv)and
         any(a.startswith(('file='+str(work/'harddisk.img')+',').encode())for a in argv),
         'UnprovenPID','Live PID does not identify this exact socket and private disks')
    ticks=(proc/'stat').read_text().split(') ',1)[1].split()[19]
    return {'pid':pid,'cmdline_hex':raw.hex(),'start_ticks':ticks,'socket':str(qmp.SOCKET),
            'private_work':str(work),'ownership_validated':True}


def verify_owned_stop(qmp,work,proof):
    validate_owned_identity(qmp.SOCKET,work,proof)
    deadline=time.monotonic()+5
    while not process_gone(proof['pid'])and time.monotonic()<deadline:time.sleep(.05)
    stat=Path('/proc')/str(proof['pid'])/'stat'
    if stat.exists():
        need(stat.read_text().split(') ',1)[1].split()[19]==proof['start_ticks'],
             'PIDReused','Captured PID now identifies another process')
    need(process_gone(proof['pid'])and not qmp.SOCKET.exists(),'GuestStillRunning',
         'Both captured owned PID gone/zombie and absent own socket required before extraction')
    return {'pid':proof['pid'],'pid_gone_or_zombie':True,'socket_absent':True,
            'ownership_proof':'captured live argv/socket/private-disks/start-ticks before stop'}


def expected_exports(plan):
    name=plan['first_save_name']
    if name is None:return {}
    rows={name:name+'.WP5'}
    if plan['interop']:rows.update({'R'+name[1:]:'R'+name[1:]+'.WP5',
                                   'A'+name[1:]:'A'+name[1:]+'.WP5','G43PRINT.PRN':'G43PRINT.PRN'})
    return rows


def validate_extraction(directory,row,plan,declared):
    expected=expected_exports(plan)
    need(len(declared)==len(expected)and dict(declared)==expected,'RequiredExportMissing',
         'Executed recipe must declare every required native/stream exactly once')
    rows=row.get('exports',[])
    need(len(rows)==len(expected)and {x['name']:x['host']for x in rows}==expected,
         'RequiredExportMissing','Stopped extraction did not return every required output')
    for item in rows:
        f=directory/item['host']
        need(type(item.get('exit'))is int and item['exit']==0 and f.is_file()
             and type(item.get('size'))is int and item['size']>0 and f.stat().st_size==item['size']
             and item.get('sha256')==sha(f),'ExportFailed','Missing/nonzero/empty/unsealed stopped output '+item['host'])
    before=(directory/'OUT-before-bare.txt').read_text();after=(directory/'OUT-after.txt').read_text()
    need('G43DRAFT'not in bare_names(after),'UnexpectedCancelledOutput','Cancelled/unused draft exists')
    if plan['id']=='empty-f10-cancel':
        need(sorted(before.splitlines())==sorted(after.splitlines()),'UnexpectedEmptyOutput',
             'Canceled empty Save must retain the entire original stopped directory')
    row['directory_delta_empty']=sorted(before.splitlines())==sorted(after.splitlines())
    row['required_extraction_validated']=True


def note_error(row,phase,error):
    detail={'phase':phase,'code':getattr(error,'code',type(error).__name__),'detail':str(error)}
    row.setdefault('errors',[]).append(detail)
    row.setdefault('error',str(error));row.setdefault('error_code',detail['code'])
    row['outcome']='incomplete'


def attempt(qmp,guest,private,out,args,prep,plan,repetition):
    directory=out/('r'+str(repetition));directory.mkdir();work=private/'runs'/args.run_id/directory.name
    row={'repetition':repetition,'attempted':True,'outcome':'incomplete','launch_boundary_reached':False,
         'planned_qemu_argv':guest.arguments(work/'boot.img',work/'harddisk.img')}
    p=None;start_called=False
    write(directory/'before-launch.json',{'planned_qemu_argv':row['planned_qemu_argv'],'preparation':prep,'case':args.case,'repetition':repetition})
    try:
        row['master_before']=master_identity(guest)
        need(not qmp.SOCKET.exists()and not work.exists(),'ForeignRuntime','Unknown socket/work exists')
        session.QMP_AUDIT_FILE=directory/'qmp-wire.jsonl'
        signal.setitimer(signal.ITIMER_REAL,480)
        original_arguments=guest.arguments
        def before_boot(boot,disk):
            argv=original_arguments(boot,disk)
            listing=subprocess.run(['mdir','-b','-i',str(disk)+'@@1048576','::OUT/'],capture_output=True,check=True,timeout=15)
            (directory/'OUT-before-bare.txt').write_bytes(listing.stdout)
            need(not(bare_names(listing.stdout.decode())&{'G43DRAFT','G43EMPTY','G43TEXT','G43RETRY','G43DIRTY','R43TEXT','R43RETRY','R43DIRTY','A43TEXT','A43RETRY','A43DIRTY','G43PRINT'}),'TargetExists','All declared targets must be absent in the actual preboot directory')
            row['resources_before']=resource_metadata(work)
            need(argv==row['planned_qemu_argv'],'ArgvChanged','Actual launch differs from sealed argv')
            write(directory/'before-launch.json',{'planned_qemu_argv':argv,'preparation':prep,'case':args.case,'repetition':repetition,'resources_before':row['resources_before'],'preboot_directory_sha256':sha(directory/'OUT-before-bare.txt')})
            row['launch_boundary_reached']=True
            return argv
        guest.arguments=before_boot
        start_called=True
        try:row['qemu_argv']=session.fresh_start(qmp,guest,work,[]);row['fresh_start_returned']=True
        finally:guest.arguments=original_arguments
        row['owned_process']=capture_owned_pid(qmp,work)
        write(directory/'owned-process.json',row['owned_process'])
        with qmp.QMP()as q:
            p=native.MutationProbe(q,directory)
            row['observed']=act(plan,p)
            row['exit_actions']=exit_protocol.finish_original(p);row['normal_original_exit']=True
    except Exception as e:note_error(row,'original/start',e)
    finally:
        signal.setitimer(signal.ITIMER_REAL,0)
        if p:row.update(trace=p.trace,settings=p.settings,checks=p.checks)
        row['no_start_proven']=not row['launch_boundary_reached']and not row.get('fresh_start_returned',False)
        if start_called and not row['no_start_proven']:
            if 'owned_process'not in row:
                try:
                    row['owned_process']=capture_owned_pid(qmp,work)
                    write(directory/'owned-process.json',row['owned_process'])
                except Exception as e:note_error(row,'capture-owned-PID',e)
            if 'owned_process'in row:
                if row.get('errors')and qmp.SOCKET.exists():
                    try:
                        with qmp.QMP()as q:q.capture(directory/'failure-state')
                    except Exception as e:row['failure_capture_error']=str(e)
                stop_ok=False
                try:row['stop_method']=session.stop_owned(qmp,guest);stop_ok=True
                except Exception as e:note_error(row,'stop',e)
                try:
                    row['stop_proof']=verify_owned_stop(qmp,work,row['owned_process'])
                    row.update(guest_stopped=True,pid_gone_or_zombie=True,socket_absent=True)
                    write(directory/'stop-proof.json',row['stop_proof'])
                except Exception as e:note_error(row,'verify-stop',e)
                if stop_ok and row.get('guest_stopped')is True:
                    try:
                        need((work/'settings-before.SET').is_file(),'MissingPrebootSET','Cannot invent initial settings after execution')
                        row['settings_before']={'sha256':sha(work/'settings-before.SET'),'publication':'private preboot bytes only'}
                        row['settings_after']=session.settings_snapshot(work,'after')
                        (directory/'OUT-before.txt').write_bytes((work/'OUT-before.txt').read_bytes())
                        row['exports']=[]
                        export_stopped(work,directory,p.exports if p else[],row['exports'])
                        row['resources']=resource_metadata(work)
                        if row.get('normal_original_exit')is True:
                            validate_extraction(directory,row,plan,p.exports if p else[])
                    except Exception as e:note_error(row,'stopped-extraction',e)
                else:row['extraction_skipped']='Stop failed or positive PID/socket stop proof missing'
            else:row['extraction_skipped']='No positively captured owned PID; no termination or safe extraction claimed'
        else:row['extraction_skipped']='Prelaunch/no-start; no termination invented'
        try:
            row['master_after']=master_identity(guest)
            need(row.get('master_before')==row['master_after'],'MasterChanged','Per-attempt immutable master changed')
            row['master_unchanged']=True
        except Exception as e:note_error(row,'master-after',e)
        if not row.get('errors')and row.get('normal_original_exit')is True and row.get('guest_stopped')is True \
                and row.get('required_extraction_validated')is True and row.get('master_unchanged')is True:
            row['outcome']='complete-observation'
        else:row['outcome']='incomplete'
        row['artifacts']=[]
        for path in sorted(directory.rglob('*')):
            if path.is_file():
                try:row['artifacts'].append({'path':str(path.relative_to(out)),'size':path.stat().st_size,'sha256':sha(path)})
                except Exception as e:note_error(row,'seal-raw',e)
    row['oracle_safe_release']=row.get('guest_stopped')is True or(row.get('no_start_proven')is True and not qmp.SOCKET.exists())
    return row


def resource_metadata(work):
    rows=[]
    for name in ['WP.EXE','WP.FIL','WP.DRS','STANPRIN.PRS','WP{WP}.SET']:
        raw=subprocess.check_output(['mtype','-i',str(work/'harddisk.img')+'@@1048576','::WP51/'+name],timeout=15)
        rows.append({'name':name,'size':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'publication':'metadata only'})
    return rows


def run(args):
    need(args.allow_vm and bool(args.authorization_note.strip()),'AuthorizationRequired','No VM before explicit root grant; two controls are mandatory')
    need(args.case in [c['id']for c in cases()]and re.fullmatch(r'wp43-[a-z0-9-]{1,45}',args.run_id),'InvalidRunID','Safe new WP43 identity/case required')
    prep=check();out=OUT/'runs'/args.run_id;need(not out.exists(),'PriorEvidence','Never overwrite an attempt')
    previous=[json.loads(p.read_text())for p in(OUT/'runs').glob('*/run.json')]
    need(all(r.get('complete')is True for r in previous),'PreviousIncomplete','Stop before another guest after any incomplete attempt')
    need(not any(r['case']==args.case for r in previous),'RepeatedContext','No silent case repetition')
    need(sum(len(r['results'])for r in previous)+2<=10,'GuestBudget','At most ten attempts including failures')
    out.mkdir(parents=True);write(out/'prelaunch.json',prep)
    for pin in prep['sources']:
        f=out/'runner-source'/pin['path'];f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes((ROOT/pin['path']).read_bytes())
    report={'scope':SCOPE,'case':args.case,'run_id':args.run_id,'preparation':prep,'argv':sys.argv,'results':[],
            'complete':False,'wordling_tested':False,'constructor_ready':False,'full_m1_accepted':False}
    old=signal.signal(signal.SIGALRM,session.timeout_signal)
    write(out/'run.json',report)
    try:
        qmp,guest,private=session.configure(PRIMARY,'wp43')
        try:
            with session.exclusive(private):
                report['shared_guard_acquired']=True
                report['master_before']=master_identity(guest)
                try:
                    for repetition in [1,2]:
                        # Count the attempt durably before touching any launch boundary.
                        report['results'].append({'repetition':repetition,'attempted':True,'outcome':'incomplete'})
                        write(out/'run.json',report)
                        row=attempt(qmp,guest,private,out,args,prep,next(c for c in cases()if c['id']==args.case),repetition)
                        report['results'][-1]=row;write(out/'run.json',report)
                        if row['outcome']!='complete-observation':break
                finally:
                    try:
                        report['master_after']=master_identity(guest)
                        need(report['master_after']==report['master_before'],'MasterChanged','Immutable master differs after guarded extraction')
                    except Exception as e:report.setdefault('errors',[]).append({'phase':'master-after','code':getattr(e,'code',type(e).__name__),'detail':str(e)})
        finally:
            if report.get('shared_guard_acquired'):report['shared_guard_released']=True
            else:report['shared_guard_not_acquired']=True
        report['oracle_released_before_offline_audit']=all(r.get('oracle_safe_release')is True for r in report['results'])
        report['released_at']=datetime.now(timezone.utc).isoformat()
        report['complete']=len(report['results'])==2 and not report.get('errors')and all(x['outcome']=='complete-observation'for x in report['results'])
    except Exception as e:
        report.setdefault('errors',[]).append({'phase':'run','code':getattr(e,'code',type(e).__name__),'detail':str(e)})
        report['complete']=False
    finally:
        signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,old);write(out/'run.json',report)
    return {'run_manifest':str(out/'run.json'),'complete':report['complete'],'oracle_released':report.get('oracle_released_before_offline_audit',False)}


def result(path):
    need(path.is_file()and path.stat().st_size<=16*1024*1024,'ManifestBounds','Bounded16MiB manifest required')
    report=json.loads(path.read_text());base=path.parent
    need(len(report.get('results',[]))==2,'PairMissing','Exactly two result rows required')
    need(report['scope']==SCOPE and report['wordling_tested']is False and report['constructor_ready']is False,'ScopeChanged','No product/constructor claim')
    need(report['complete']is True and report.get('oracle_released_before_offline_audit')is True,'IncompleteRun','Complete stopped/released pair required')
    need(same(report['preparation'],check()),'SourceChanged','Source/profile/default authority differs')
    need(same(report['preparation'],json.loads((base/'prelaunch.json').read_text())),'PrelaunchChanged','Envelope differs from immutable prelaunch')
    need(same(report['preparation']['cases'],cases()),'CaseChanged','Declared state matrix changed')
    need(report['master_before']==report['master_after'],'MasterChanged','Master not unchanged')
    for pin in report['preparation']['sources']:
        archived=base/'runner-source'/pin['path']
        need(archived.is_file()and archived.stat().st_size==pin['size']and sha(archived)==pin['sha256'],'SourceArchiveChanged',pin['path'])
    pairs=[]
    for row in report['results']:
        directory=base/('r'+str(row['repetition']))
        preboot=json.loads((directory/'before-launch.json').read_text())
        need(same(preboot['preparation'],report['preparation'])and same(preboot['planned_qemu_argv'],row['qemu_argv'])and same(row['planned_qemu_argv'],row['qemu_argv']),'PrebootChanged','Actual argv/profile differs from prelaunch archive')
        need(preboot['preboot_directory_sha256']==sha(directory/'OUT-before-bare.txt')and same(preboot['resources_before'],row['resources_before']),'PrebootChanged','Initial resource/directory witness differs')
        need(row['normal_original_exit']is True and row['guest_stopped']is True and row['pid_gone_or_zombie']is True and row['socket_absent']is True,'IncompleteRun','Normal exit and actual host stop required')
        process=row['owned_process'];work=PRIMARY/'research/cache/reference/runs'/report['run_id']/('r'+str(row['repetition']))
        validate_owned_identity(PRIMARY/'research/cache/reference/runtime/wp43/qmp.sock',work,process)
        need(same(process,json.loads((directory/'owned-process.json').read_text()))and same(row['stop_proof'],json.loads((directory/'stop-proof.json').read_text())),'StopProofChanged','Positive process/stop archives differ')
        need(row['stop_proof']['pid']==process['pid']and row['master_unchanged']is True and row['master_before']==row['master_after']and row['required_extraction_validated']is True,'IncompleteRun','Per-attempt master/output completion proof required')
        for item in row['artifacts']:
            f=base/item['path'];need(f.resolve().is_relative_to(base.resolve())and f.is_file()and f.stat().st_size==item['size']and sha(f)==item['sha256'],'ArtifactChanged',item['path'])
        need(state((directory/'clean-exit/screen.txt').read_text())=='dos','FakeExit','Actual clear DOS required')
        expected=next(c for c in cases()if c['id']==report['case'])
        validate_extraction(directory,row,expected,list(expected_exports(expected).items()))
        # A predeclared exact sensitive trace is an independent command-order witness.
        from_path=OUT/'state_audit.py';import importlib.util
        spec=importlib.util.spec_from_file_location('wp43_state_audit',from_path);aud=importlib.util.module_from_spec(spec);spec.loader.exec_module(aud)
        states=aud.audit(directory,row,expected)
        files=[]
        for item in row['exports']:
            need(item['exit']==0,'MissingNative','Expected actual stopped export failed')
            if item['host'].endswith('.WP5'):
                raw=native.bounded_native(directory/item['host']);fields=field_report(raw);enforce_field_claims(fields['fields']);files.append({'path':item['host'],'field_report':fields})
        absent=[]
        listing=(directory/'OUT-after.txt').read_text().upper()
        for name in row['observed']['expected_absent']:
            need(not any(s.rstrip('/').rsplit('/',1)[-1].split('.')[0]==name for s in listing.splitlines()),'FabricatedAbsence','Cancelled name is present in stopped directory')
            absent.append({'name':name,'exists':False,'native_size':None,'native_hash':None})
        if report['case']=='empty-f10-cancel':
            need(not files,'FabricatedEmpty','No native output may be invented for cancellation')
            before=(directory/'OUT-before-bare.txt').read_text()
            # Same directory listing format is needed for an exact cancellation absence check.
            need(sorted(before.splitlines())==sorted(listing.splitlines())and row.get('directory_delta_empty')is True,'FabricatedAbsence','Stopped directory must exactly retain the original preboot entries')
        else:
            first=next(x for x in files if x['path']==row['observed']['first']['host'])
            need(first['field_report']['body_hex']==expected['initial_text'].encode().hex(),'FirstTextChanged','First actual ASCII/empty body differs')
        if expected['interop']:
            by={f['path']:f for f in files}
            for key,wanted in [('resaved',expected['initial_text']),('edited',expected['initial_text']+'Z')]:
                found=by[row['observed'][key]['host']]['field_report']
                need(found['body_hex']==wanted.encode().hex(),'InteropChanged','Original Retrieve/resave/edit changed the declared body')
            need((directory/row['observed']['print_stream']).stat().st_size>0,'PrintMissing','Full raw original print stream required')
            jobs=(directory/'settings-print-G43PRINT-job-status/screen.txt').read_text()
            need(all(x in jobs for x in ['No print jobs','Job Number: None','Additional Jobs Not Shown: 0']),'PrintIncomplete','Actual completed original print queue required')
        native_paths=[directory/x['path']for x in files]
        comparisons=[]
        if expected['interop']:
            source=native.bounded_native(directory/row['observed']['first']['host'])
            for role in ['resaved','edited']:
                changed=native.bounded_native(directory/row['observed'][role]['host'])
                comparisons.append({'role':role,'lengths':[len(source),len(changed)],'whole_equal':source==changed,
                    'changed_absolute_offsets':[i for i in range(max(len(source),len(changed)))if source[i:i+1]!=changed[i:i+1]],
                    'policy':'literal differences only; relocation/deleted/slack/metadata interpretation deferred to B/C; never normalized'})
        pairs.append({'repetition':row['repetition'],'files':files,'absent':absent,'actual_reader':reader(native_paths)if native_paths else[],'literal_lifecycle_differences':comparisons,'actual_state_ledger':states})
    need(len(pairs)==2 and[p['repetition']for p in pairs]==[1,2],'PairMissing','Exactly two independent fresh repetitions required')
    # Equality is reported, never promoted into default permission.
    return {'scope':SCOPE,'case':report['case'],'observations':pairs,'fresh_pair_same_first_native_sha256':([f['field_report']['sha256']for f in pairs[0]['files'][:1]]==[f['field_report']['sha256']for f in pairs[1]['files'][:1]]),'pair_equality_is_not_default_admission':True,'constructor_ready':False,'full_m1_accepted':False,'wordling_tested':False,
            'unknowns_block_future_E':True,'universal_defaults_established':False}


def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('check');sub.add_parser('plan')
    r=sub.add_parser('run');r.add_argument('run_id');r.add_argument('--case',required=True);r.add_argument('--allow-vm',action='store_true');r.add_argument('--authorization-note',default='')
    r=sub.add_parser('result');r.add_argument('path',type=Path)
    a=p.parse_args()
    try:
        x=check()if a.command=='check'else{'cases':cases(),'attempt_cap':10,'vm_launched':False}if a.command=='plan'else run(a)if a.command=='run'else result(a.path)
        print(json.dumps(x,indent=2));return 0 if x.get('complete',True)else 1
    except Exception as e:print(json.dumps({'result':'refused','code':getattr(e,'code',type(e).__name__),'detail':str(e),'full_m1_accepted':False}));return 1


if __name__=='__main__':sys.exit(main())
