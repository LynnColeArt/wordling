#!/usr/bin/env python3
"""Owned WP46 routing/custody adapter; offline by default. No native codec/VM engine."""
import argparse
from datetime import datetime,timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import traceback

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];PRIMARY=Path('/home/lynn/projects/wordling');PRIVATE=PRIMARY/'research/cache/reference'
sys.path.insert(0,str(ROOT/'scripts/reference'))
spec=importlib.util.spec_from_file_location('approved_wp44_custody',HERE.parent/'wp44/oracle.py');guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
require=guard.require;Refusal=guard.Refusal;sha=guard.sha;canonical=guard.canonical;dump=guard.dump

def product(*args):
 p=subprocess.run([str(HERE/'bin/producer'),*map(str,args)],cwd=ROOT,capture_output=True,timeout=30)
 require(p.returncode==0,'PublicProducerRefusal',p.stderr.decode(errors='replace'));return json.loads(p.stdout)
def helpers():
 import native_genesis
 return (*guard.helpers(),native_genesis)
def profile_fields(path,inspection):
 # Offline evidence checker only: offsets/owners come from actual Go Inspect;
 # all individual expected field facts come from reviewed schema, not a prefix.
 raw=Path(path).read_bytes();schema=json.loads((ROOT/'docs/research/continuation/native-constructor-design/schema.json').read_text());owners={'header':(0,16)}
 for packet in inspection['Packets']:owners['packet-'+str(packet['Type'])]=(packet['Data']['Offset'],packet['Data']['Length'])
 require(len(schema['fields'])==72,'FieldRoster','all72 field facts required');seen=[]
 for field in schema['fields']:
  require(field['owner']in owners,'FieldOwner','required native owner missing');start,length=owners[field['owner']];offset=field['relative_owner_offset'];width=field['width'];require(type(offset)is int and type(width)is int and 0<=offset<=length and 0<width<=length-offset,'FieldBounds','field does not fit real owned packet');actual=raw[start+offset:start+offset+width];expected=bytes.fromhex(field['hex'])
  if field['owner']=='header'and field['name']=='body start':expected=inspection['Body']['Offset'].to_bytes(4,'little')
  allowed=actual==expected
  if field['owner']=='packet-6'and field['relative_owner_offset']==0:allowed=actual in [b'\x00',b'\x08']
  require(len(expected)==width and allowed,'ProfileFieldMismatch',field['owner']+' '+field['name']);seen.append({'owner':field['owner'],'name':field['name'],'width':width,'hex':actual.hex(),'representation':field['representation'],'units':field['units'],'source':field.get('source',field['authority'])})
 return seen

def cases():
 provenance=json.loads((HERE/'candidates/provenance.json').read_text());require(provenance['runtime_native_input']=='none'and provenance['new_birth_preserved']is True and provenance['lifetime_NoLoadedOriginal']is True,'GenesisProvenance','real no-input New producer required')
 rows=[]
 for name,kind,text,body in [('empty-edit','empty','G43ASCIIZ','G43ASCIIZ'),('ascii-edit','ascii','Z','G43ASCIIZ'),('empty-print','empty','','')]:
  path=HERE/'candidates'/str(kind+'.WP5');actual=product('-verify',path,'-require-preprint');want=''if kind=='empty'else'G43ASCII';profile_fields(path,actual['inspection'])
  require(actual['body_hex']==want.encode().hex()and actual['admitted']is True,'CandidateBody','actual generated input differs')
  pin=next(x for x in provenance['classes']if x['name']==kind);require(sha(path)==pin['sha256']and path.stat().st_size==pin['bytes'],'CandidateIdentity','actual measured generator output changed')
  rows.append({'id':name,'native_class':kind,'candidate':str(path.relative_to(ROOT)),'candidate_sha256':sha(path),'candidate_size':path.stat().st_size,'original_insert':text,'expected_body_hex':body.encode().hex(),'two_fresh_original_controls_required':True,'print_presence':'either exact original-confirmed empty result (including no file) or full exact stream'if name=='empty-print'else'nonempty exact full original control bytes','postprint':'empty: exact matched original cache/state, admit only unchanged e72401 or refuse1172/02; text:1172/02 refused','normal_Reveal_gap':'Home3 Up gap0 in each view, restore normal then EOF','save_names':['C46PRE','C46FIN'],'print_name':'C46PRN','empty_print_not_previously_qualified':name=='empty-print','empty_submit_classifier':'captured main empty document + completed queue permits measured exact stream/zero/absence; any NoText or other modal is unqualified, retain and halt without dismissal'})
 return rows

def sources():
 import resaved_prefix
 pins=resaved_prefix.sources();known={x['path']for x in pins}
 paths=[HERE/'oracle.py',HERE/'test_oracle.py',HERE/'bin/producer',HERE/'producer-execution.json',HERE/'compiled-project-packages.json',HERE/'producer-go-env.log',HERE/'producer-buildinfo.log',ROOT/'go.mod',HERE/'candidates/provenance.json',HERE/'producer/main.go',HERE/'producer/go.mod',ROOT/'internal/document/evidence/wp44/oracle.py',ROOT/'scripts/reference/native_genesis.py',ROOT/'docs/research/continuation/native-constructor-design/schema.json',ROOT/'docs/research/continuation/native-constructor-design/decision.md',*sorted((ROOT/'internal/document').glob('*.go'))]
 for package in json.loads((HERE/'compiled-project-packages.json').read_text()):
  for name,digest in package['compiled_source_sha256'].items():
   path=ROOT/name;require(sha(path)==digest,'CompiledSourceDrift','actual compiled Go file changed: '+name);paths.append(path)
 for p in paths:
  rel=str(p.relative_to(ROOT))
  if rel not in known:pins.append({'path':rel,'size':p.stat().st_size,'sha256':sha(p)});known.add(rel)
 return sorted(pins,key=lambda x:x['path'])
def frozen_argv(work):
 import guest
 old=guest.RUNTIME,guest.SOCKET
 try:guest.RUNTIME=PRIVATE/'runtime/wp46';guest.SOCKET=guest.RUNTIME/'qmp.sock';return guest.arguments(work/'boot.img',work/'harddisk.img')
 finally:guest.RUNTIME,guest.SOCKET=old

def plan():
 import resaved_prefix
 base=resaved_prefix.plan();cs=cases();attempts=[]
 listing=subprocess.run(['mdir','-b','-i',str(PRIVATE/'master/harddisk.img')+'@@1048576','::OUT'],capture_output=True,timeout=15);require(listing.returncode==0,'MasterScratchDirectory','actual master OUT listing required');names={x.strip().replace('\\','/').rsplit('/',1)[-1].upper()for x in listing.stdout.decode(errors='replace').splitlines()if x.strip()};require(not any(n.split('.')[0]in ['C46INPUT','C46SEED','C46PRE','C46FIN','C46PRN']for n in names),'MasterScratchCollision','declared new native/print names already exist in master')
 for case in cs:
  for mode in ['control','candidate']:
   for repetition in [1,2]:
    ident=f"wp46-{case['id']}-{mode}-r{repetition}";work=PRIVATE/'runs'/ident
    attempts.append({'id':ident,'case':case['id'],'mode':mode,'repetition':repetition,'private_work':str(work),'qemu_argv':frozen_argv(work)})
 return {'schema':'wordling.wp46.plan/v1','sources':sources(),'cases':cs,'attempts':attempts,'master_OUT_listing_sha256':hashlib.sha256(listing.stdout).hexdigest(),'master_declared_scratch_names_absent':True,'maximum_attempts_including_failures':12,'whole_native_classes':2,'candidate_observations':6,'original_control_observations':6,'empty_print_branch':'smallest two fresh original controls plus two generated-empty observations, separately counted; unknown modal stops, never guessed recovery','order':'all controls then corresponding candidates for each case; first incomplete halts entire plan; no retries','master':base['master'],'tools':base['tools'],'manuals':base['manuals'],'preboot_resources':base['preboot_resources'],'profile_id':base['profile_id'],'profile_sha256':base['profile_sha256'],'shared_lock':str(PRIVATE/'session1.lock'),'socket':str(PRIVATE/'runtime/wp46/qmp.sock'),'ledger':str(PRIVATE/'wp46-attempts.json'),'timeout_per_attempt_seconds':900,'source_inputs':'no native input to New; original controls create their own seed in guest, hashed only after stopped extraction','control_setup':'read-only inherited native_edits.settings; explicit FastSaveNo; original empty or typed G43ASCII first Save C46SEED, captured clear/return and Retrieve same actual original file','candidate_setup':'same read-only settings/FastSaveNo, Retrieve exact real generated C46INPUT','sensitive_interval':'normal/Reveal gap0, restore normal, EOF; declared text only; Save PRE before any print-port setup; full print queue; FIN; captured39 normal exit','identity':'unchanged approved44 positive PID/startticks/argv/executable/private drives, exact normal QMP method, bounded monotonic completion, then stopped extraction/master under actual shared lock','rights':'no private EXE/manual/SET/PRS/font/master bytes published','limits':'selected historical closed metadata and actual Standard Printer/QEMU/FreeDOS1.4/QMP injection only; no Linux physical/layout/resource availability claim','full_M1_accepted':False}

def check():
 p=plan();require(len(p['attempts'])==12 and len({x['candidate_sha256']for x in p['cases']})==2,'MeasuredClasses','exact measured classes/branches')
 require(sha(ROOT/'docs/research/continuation/native-constructor-design/decision.md')=='39a400e332f935113cb030bec4c31ca4607bc6a44267c0fe8672e366f7be7ac8'and sha(ROOT/'docs/research/continuation/native-constructor-design/schema.json')=='fa2047edef32c9fdfdd3d1bc728915182375cd4617d9a87c26283a9b227e6b4e','DesignIdentity','reviewed architecture changed')
 return p

def perform(p,case,mode):
 session,n,fields,quit_module,layout,genesis=helpers();n.settings(p);settings=fields.capture_fast_save(p,'disabled');setup=[]
 if mode=='control':
  if case['native_class']=='ascii':p.type('G43ASCII');p.capture('control-original-first-ascii')
  session.save_complete(p,'C46SEED',fields.save_named);setup=genesis.clear_for_retrieve(p);p.retrieve('C:\\OUT\\C46SEED','control-original-exact-retrieve')
 else:p.retrieve('C:\\OUT\\C46INPUT','generated-exact-retrieve')
 p.capture('input-normal');p.key('home,home,home,up,alt-f3');p.q.wait_for('Reveal Codes to restore');p.capture('input-Reveal-gap0');p.key('alt-f3');p.key('home,home,home,up,end');p.capture('before-declared-text')
 if case['original_insert']:p.type(case['original_insert'])
 p.capture('after-declared-text');session.save_complete(p,'C46PRE',fields.save_named)
 (print_empty(p,session,quit_module)if case['id']=='empty-print'else layout.print_disk(p,'C46PRN'));session.save_complete(p,'C46FIN',fields.save_named)
 exits=quit_module.finish_original(p);return {'fast_save':settings,'control_seed_clear_actions':setup,'exit_actions':exits}

def print_empty(p,session,quit_module):
 # Same approved14 menu protocol, but stop on any previously unobserved empty
 # submit modal BEFORE another key. No NoText text/recovery is guessed.
 p.screen_step('shift-f7,s','print-C46PRN-printer-list','Standard Printer')
 p.key('3');p.setting('print-C46PRN-printer-edit');p.key('2');p.capture('print-C46PRN-ports');p.key('8');p.capture('print-C46PRN-other-path')
 p.type('C:\\OUT\\C46PRN.PRN');p.key('ret');p.setting('print-C46PRN-other-accepted');p.key('f7,f7');p.setting('print-C46PRN-menu')
 p.key('1');p.q.wait_for('Doc 1');screen=p.capture('empty-print-submit-classifier')
 require(quit_module.exit_state(screen)=='main'and not screen.splitlines()[0].strip(),'EmptyPrintUnknownState','empty print must return actual empty main state; NoText/other modal retained and halts, no guessed dismissal')
 p.key('shift-f7,4');p.q.wait_for('No print jobs');jobs=p.setting('print-C46PRN-job-status')
 require('Job Number: None'in jobs and 'Additional Jobs Not Shown: 0'in jobs,'PrintQueueIncomplete','actual empty completed queue required')
 p.key('f7');p.q.wait_for('Doc 1');p.capture('empty-print-main-return');p.exports.append(('C46PRN.PRN','C46PRN.PRN'))

def export_one(work,target,name,host,allow_empty_print=False):
 out=target/host;p=subprocess.run(['mcopy','-i',str(work/'harddisk.img')+'@@1048576','::OUT/'+name,str(out)],capture_output=True,timeout=15)
 row={'name':name,'path':str(out),'exit':p.returncode,'stderr':p.stderr.decode(errors='replace')}
 if p.returncode:
  require(allow_empty_print,'RequiredExportFailed',name)
  listing=subprocess.run(['mdir','-b','-i',str(work/'harddisk.img')+'@@1048576','::OUT'],capture_output=True,timeout=15);row['absence_directory']={'exit':listing.returncode,'stdout':listing.stdout.decode(errors='replace'),'stderr':listing.stderr.decode(errors='replace')}
  names={x.strip().replace('\\','/').rsplit('/',1)[-1].upper()for x in listing.stdout.decode(errors='replace').splitlines()if x.strip()}
  require(listing.returncode==0 and name.upper()not in names and not out.exists(),'RequiredAbsenceUnproven','empty-print no-file branch requires actual stopped directory and no local stale file');row['present']=False;return row
 require(out.is_file()and(out.stat().st_size>0 or allow_empty_print),'RequiredExportMissing',name);row.update(present=True,size=out.stat().st_size,sha256=sha(out));return row

def extract(session,work,target,p,row,case,leaf):
 require(row.get('guest_stopped')is True,'StopUnproven','no extraction without positive stop')
 row['settings_after']=session.settings_snapshot(work,'after');row['exports']=[]
 expected={'C46PRE.WP5','C46FIN.WP5','C46PRN.PRN'}|({'C46SEED.WP5'}if leaf['mode']=='control'else set())
 require({host for name,host in p.exports}==expected,'ExportRoster','exact actual save/print export declarations required')
 for name,host in p.exports:row['exports'].append(export_one(work,target,name,host,case['id']=='empty-print'and host=='C46PRN.PRN'))
 if leaf['mode']=='candidate':
  ent=export_one(work,target,'C46INPUT','input-after.WP5');require(ent['sha256']==case['candidate_sha256']and ent['size']==case['candidate_size'],'InputChanged','retrieved generated input changed');row['input_after']=ent
 row['exports_complete']=True

def normal_dos(directory):
 import macro_quit
 require(macro_quit.exit_state((Path(directory)/'clean-exit/screen.txt').read_text())=='dos','NormalDOSMissing','captured clear DOS required; no positive status assertion alone')

def attempt(session,qmp,guest,n,case,leaf,target,work):
 row={'id':leaf['id'],'case':leaf['case'],'mode':leaf['mode'],'repetition':leaf['repetition'],'outcome':'incomplete','guest_stopped':False};p=None;identity=None
 try:
  assets=[('C46INPUT',ROOT/case['candidate'])]if leaf['mode']=='candidate'else[]
  session.QMP_AUDIT_FILE=target/'qmp-wire.jsonl';signal.setitimer(signal.ITIMER_REAL,900);argv=session.fresh_start(qmp,guest,work,assets);row['qemu_argv']=argv
  require(argv==leaf['qemu_argv'],'LaunchArgv','actual launch differs');identity=guard.owned_identity(qmp,work,argv);row['owned_start_identity']=identity
  with qmp.QMP()as q:
   p=n.MutationProbe(q,target);row['observations']=perform(p,case,leaf['mode']);normal_dos(target);row['normal_DOS']=True
 except Exception as error:row.update(error=str(error),error_code=getattr(error,'code',type(error).__name__),traceback=traceback.format_exc())
 finally:
  signal.setitimer(signal.ITIMER_REAL,0)
  if identity is None and qmp.SOCKET.exists():
   try:identity=guard.owned_identity(qmp,work,row.get('qemu_argv')or guest.arguments(work/'boot.img',work/'harddisk.img'));row['owned_start_identity']=identity
   except Exception as error:row['identity_error']=str(error)
  if identity is not None:
   try:
    guard.validate_stop_identity(qmp,identity);guard.same_identity(identity);row['stop_method']=session.stop_owned(qmp,guest);require(row['stop_method']=='QMP quit; own socket terminated','HostContained','no normal-stop proof from host containment')
    row['stop_observations']=[];row['stop_proof']=guard.stopped(qmp,identity,observations=row['stop_observations']);row['guest_stopped']=True
   except Exception as error:row.update(stop_error=str(error),stop_error_code=getattr(error,'code',type(error).__name__))
  else:row['stop_error']='positive owned PID/argv/disks/startticks unavailable; no stop/extraction'
  if row['guest_stopped']and p is not None:
   try:extract(session,work,target,p,row,case,leaf)
   except Exception as error:row.update(extraction_error=str(error),extraction_error_code=getattr(error,'code',type(error).__name__))
  else:row['extraction_skipped']='positive stop/probe absent'
  if p is not None:row.update(trace=p.trace,checks=p.checks,settings=p.settings)
  if row.get('normal_DOS')and row['guest_stopped']and row.get('exports_complete')and not any(k in row for k in ['error','stop_error','extraction_error']):row['outcome']='complete-observation'
 return row

def print_value(target,row):
 x=next(x for x in row['exports']if x['name']=='C46PRN.PRN')
 if not x['present']:require(not Path(x['path']).exists(),'PrintPresenceChanged','absent stream appeared');return None
 raw=guard.checked_export_bytes(x['path'],x['size'],x['sha256']);return raw

def qualify(target,case,row,control=None):
 pre=product('-verify',target/'C46PRE.WP5','-require-preprint','-reedit-out',target/'second-Go-edit.WP5');pre['all72_fields']=profile_fields(target/'C46PRE.WP5',pre['inspection']);require(pre['body_hex']==case['expected_body_hex'],'OriginalBodyMismatch','declared original text differs')
 post=product('-verify',target/'C46FIN.WP5');require(post['body_hex']==case['expected_body_hex'],'PostBodyMismatch','original post-print body differs')
 if post['admitted']:
  require(case['id']=='empty-print'and(target/'C46FIN.WP5').read_bytes()==(target/'C46PRE.WP5').read_bytes(),'PostprintUnexpected','only byte-identical empty PRE may remain admitted')
 else:
  info=post['inspection'];raw=(target/'C46FIN.WP5').read_bytes();font=next(x['Data']['Offset']for x in info['Packets']if x['Type']==15);state=next(x['Data']['Offset']for x in info['Packets']if x['Type']==6)
  require(raw[font+21:font+23]==bytes.fromhex('1172')and raw[state+8]==2,'EmptyPostprintUnexpected','only exact observed post-print02/1172 refusal branch')
 stream=print_value(target,row)
 if control:
  require(sha(control['report'])==control['result_file_sha256'],'ControlResultChanged','prior result file changed after candidate boot');reference=json.loads(Path(control['report']).read_text());require(canonical(reference)==control['result_sha256'],'ControlResultChanged','checksum-bound prior result changed');ctl=print_value(Path(control['directory']),reference)
  for export in reference['exports']:
   if export['present']:guard.checked_export_bytes(export['path'],export['size'],export['sha256'])
  require(stream==ctl,'PrintControlMismatch','full matched logical-original print bytes/presence differ')
  require((target/'C46PRE.WP5').read_bytes()==(Path(control['directory'])/'C46PRE.WP5').read_bytes(),'NativePreControlMismatch','full required preprint differs from exact original control')
  require((target/'C46FIN.WP5').read_bytes()==(Path(control['directory'])/'C46FIN.WP5').read_bytes(),'NativeControlMismatch','full matched original postprint native differs')
 return {'preprint':pre,'postprint':post,'full_PRN_control_equal':bool(control),'print_present':stream is not None,'print_size':len(stream)if stream is not None else None}

def bind_control(plan,case,leaf,prior):
 if leaf['mode']=='control':return None
 wanted=f"wp46-{case['id']}-control-r{leaf['repetition']}";entries=[x for x in prior if x['id']==wanted];require(len(entries)==1 and entries[0]['outcome']=='complete-observation','MissingControl','matching fresh original control required before boot')
 entry=entries[0];directory=HERE/'runs'/entry['grant_id']/wanted;report=directory/'result.json';require(report.is_file()and sha(report)==entry['result_file_sha256'],'ControlResultChanged','prior control result file changed')
 row=json.loads(report.read_text());require(canonical(row)==entry['result_sha256']and row['id']==wanted and row['mode']=='control'and row['repetition']==leaf['repetition']and row['case']==case['id']and row.get('plan_sha256')==canonical(plan),'ControlIdentity','result leaf/case/repetition mismatch');print_value(directory,row)
 for x in row['exports']:
  if x['present']:guard.checked_export_bytes(x['path'],x['size'],x['sha256'])
 return {'directory':str(directory),'report':str(report),'result_sha256':entry['result_sha256'],'result_file_sha256':entry['result_file_sha256'],'plan_sha256':canonical(plan)}

def result(path):
 report=json.loads(Path(path).read_text());require(report.get('complete')is True and report.get('oracle_released')is True and report.get('guard_released')is True,'IncompleteBatch','actual complete released batch required');pre=json.loads((Path(path).parent/'prelaunch.json').read_text());p=pre['plan'];require(canonical(p)==report['plan_sha256'],'PlanIdentity','source/plan differs');checks=[]
 for row in report['results']:
  leaf=next(x for x in p['attempts']if x['id']==row['id']);case=next(x for x in p['cases']if x['id']==leaf['case']);directory=Path(path).parent/row['id'];normal_dos(directory);require(row['outcome']=='complete-observation'and row['guest_stopped']is True and row['normal_DOS']is True,'IncompleteAttempt','required actual completion');control=bind_control(p,case,leaf,json.loads((Path(path).parent/'aggregate-ledger.json').read_text())['attempts'])
  for export in row['exports']:
   if export['present']:guard.checked_export_bytes(export['path'],export['size'],export['sha256'])
  # Use a fresh temporary output for actual consumer replay, not sealed rawlogs.
  with tempfile.TemporaryDirectory(prefix='wp46-reedit-')as tmp:
   native=product('-verify',directory/'C46PRE.WP5','-require-preprint','-reedit-out',Path(tmp)/'Q.WP5');require(native['body_hex']==case['expected_body_hex'],'OriginalBodyMismatch','required actual native differs')
  if control:
   reference=json.loads(Path(control['report']).read_text());require(print_value(directory,row)==print_value(Path(control['directory']),reference),'PrintControlMismatch','full raw control mismatch')
  checks.append({'id':row['id'],'native':native,'full_PRN_control_equal':bool(control)})
 return {'qualified_observations':checks,'full_M1_accepted':False}

def selected(args,p,grant):
 ids=args.attempt;require(re.fullmatch(r'wp46-[a-z0-9-]{1,24}',args.grant_id or '')and bool(ids)and len(ids)==len(set(ids)),'GrantSelection','exact safe subset required')
 require(grant.get('authorized')is True and grant.get('grant_id')==args.grant_id and grant.get('plan_sha256')==canonical(p)and grant.get('attempt_ids')==ids and type(grant.get('maximum_aggregate_attempts'))is int and grant['maximum_aggregate_attempts']==12 and isinstance(grant.get('authorization_note'),str)and bool(grant['authorization_note']),'GrantMismatch','root exact source/plan/subset/cap/note required')
 if 'argv'in grant:require(grant['argv']==[sys.executable,*sys.argv],'GrantArgv','actual argv differs from root grant')
 lookup={x['id']:x for x in p['attempts']};require(all(x in lookup for x in ids),'UnknownAttempt','frozen leaves only');return [lookup[x]for x in ids]

def run(args):
 require(args.allow_vm,'AuthorizationRequired','offline default; root grant required');p=check();grant=json.loads(Path(args.grant).read_text());leaves=selected(args,p,grant);out=HERE/'runs'/args.grant_id;require(not out.exists(),'PriorEvidence','new grant directory only');out.mkdir(parents=True)
 for pin in p['sources']:
  src=ROOT/pin['path'];dst=out/'runner-source'/pin['path'];dst=dst.with_name(dst.name+'.txt')if dst.suffix in ['.go','.py']else dst;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 for c in p['cases']:
  dst=out/'inputs'/str(c['native_class']+'.WP5');dst.parent.mkdir(exist_ok=True);shutil.copyfile(ROOT/c['candidate'],dst)
 dump(out/'prelaunch.json',{'plan':p,'plan_sha256':canonical(p),'grant':grant,'argv':[sys.executable,*sys.argv]})
 session,n,fields,quit_module,layout,genesis=helpers();qmp,guest,private=session.configure(PRIMARY,'wp46');report={'plan_sha256':canonical(p),'grant_id':args.grant_id,'selected_attempt_ids':[x['id']for x in leaves],'results':[],'guard_released':False,'oracle_released':False,'full_M1_accepted':False};old=signal.signal(signal.SIGALRM,session.timeout_signal)
 try:
  with session.exclusive(private):
   try:
    require(all(sha(guest.MASTER/k)==v for k,v in p['master'].items()),'MasterChanged','master changed before start');ledger=Path(p['ledger']);aggregate=json.loads(ledger.read_text())if ledger.exists()else{'plan_sha256':canonical(p),'maximum':12,'attempts':[]};prior=aggregate['attempts']
    require(len({x['id']for x in prior})==len(prior)and all(x['id']in {leaf['id']for leaf in p['attempts']}for x in prior),'LedgerIdentity','unknown or duplicate prior attempt')
    require(aggregate['plan_sha256']==canonical(p)and type(aggregate['maximum'])is int and aggregate['maximum']==12,'LedgerPlan','durable plan/cap mismatch');require(all(x['outcome']=='complete-observation'for x in prior),'PriorFailure','first failure permanently halts this plan');require(len(prior)+len(leaves)<=12 and not({x['id']for x in prior}&{x['id']for x in leaves}),'AttemptLimit','no cap reset/retry/duplicate')
    for leaf in leaves:
     for pin in p['sources']:require(sha(ROOT/pin['path'])==pin['sha256'],'SourceDrift',pin['path'])
     case=next(x for x in p['cases']if x['id']==leaf['case']);require(sha(ROOT/case['candidate'])==case['candidate_sha256'],'CandidateDrift','generated bytes changed');control=bind_control(p,case,leaf,prior);target=out/leaf['id'];target.mkdir();work=Path(leaf['private_work']);require(not work.exists()and not qmp.SOCKET.exists(),'ForeignRuntime','new private disk/absent own socket required')
     if control:
      (target/'control-custody').mkdir();shutil.copyfile(control['report'],target/'control-custody/result.json');control['archived_result']=str(target/'control-custody/result.json');control['archived_result_sha256']=sha(target/'control-custody/result.json')
     entry={'id':leaf['id'],'case':leaf['case'],'mode':leaf['mode'],'repetition':leaf['repetition'],'grant_id':args.grant_id,'outcome':'incomplete','started_at':datetime.now(timezone.utc).isoformat()};prior.append(entry);dump(ledger,aggregate)
     row=attempt(session,qmp,guest,n,case,leaf,target,work);row['plan_sha256']=canonical(p)
     try:
      if row['outcome']=='complete-observation':row['required_output_qualification']=qualify(target,case,row,control)
      row['master_after']={k:sha(guest.MASTER/k)for k in p['master']};require(row['master_after']==p['master'],'MasterChanged','master changed after stopped extraction')
     except Exception as error:row.update(outcome='required-output-or-master-unproven',qualification_error=str(error),qualification_error_code=getattr(error,'code',type(error).__name__))
     entry['outcome']=row['outcome'];entry['result_sha256']=canonical(row);dump(target/'result.json',row);entry['result_file_sha256']=sha(target/'result.json');report['results'].append(row);dump(ledger,aggregate);dump(out/'aggregate-ledger.json',aggregate);dump(out/'run.json',report)
     if row['outcome']!='complete-observation':report['halted_before_next_guest']=True;break
   except Exception as error:report.update(batch_error=str(error),batch_error_code=getattr(error,'code',type(error).__name__),halted_before_next_guest=True)
   finally:
    try:report['master_after']={k:sha(guest.MASTER/k)for k in p['master']};report['master_unchanged']=report['master_after']==p['master']
    except Exception as error:report['master_error']=str(error)
    dump(out/'run.json',report)
  report['guard_released']=True;report['oracle_released']=bool(report['results'])and all(r['guest_stopped']for r in report['results'])and not qmp.SOCKET.exists()
 finally:
  signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,old);report['complete']=len(report['results'])==len(leaves)and all(x['outcome']=='complete-observation'for x in report['results'])and report.get('master_unchanged')is True;dump(out/'run.json',report)
 print(json.dumps({'complete':report['complete'],'oracle_released':report['oracle_released'],'attempts':len(report['results'])}));return 0 if report['complete']else 1

def main():
 parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
 for name in ['check','plan']:sub.add_parser(name)
 r=sub.add_parser('run');r.add_argument('--allow-vm',action='store_true');r.add_argument('--grant',required=True);r.add_argument('--grant-id',required=True);r.add_argument('--attempt',action='append',required=True)
 r=sub.add_parser('result');r.add_argument('path');args=parser.parse_args()
 if args.command=='run':return run(args)
 if args.command=='result':print(json.dumps(result(args.path),indent=2));return 0
 print(json.dumps(check()if args.command=='check'else plan(),indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
