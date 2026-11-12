#!/usr/bin/env python3
"""WP44 bounded candidate interoperability adapter. check/plan/result never boot.

The actual original engine, reference field audit, print and captured-exit helpers
are inherited unchanged. This file owns routing, declared actions and fail-closed
custody, not a second native parser, document constructor or emulator engine.
"""
import argparse
from datetime import datetime,timezone
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import traceback
import tempfile
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PRIMARY=Path('/home/lynn/projects/wordling')
PRIVATE=PRIMARY/'research/cache/reference'
sys.path.insert(0,str(ROOT/'scripts/reference'))
NAMES=['C44PRE','C44FIN','C44PRN.PRN']
class Refusal(ValueError):
 def __init__(self,code,detail):self.code=code;super().__init__(detail)
def require(ok,code,detail):
 if not ok:raise Refusal(code,detail)
def sha(p):
 with Path(p).open('rb')as s:return hashlib.file_digest(s,'sha256').hexdigest()
def dump(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def canonical(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def producer(*args):
 r=subprocess.run([str(HERE/'bin/producer'),*map(str,args)],cwd=ROOT,capture_output=True,timeout=30)
 require(r.returncode==0,'PublicProducerRefusal',r.stderr.decode(errors='replace'))
 return json.loads(r.stdout)
def helpers():
 return tuple(importlib.import_module(n)for n in ['macro_session','native_edits','resaved_prefix','macro_quit','text_layout'])
def sources():
 # Approved42's actual transitive closure plus this real public Go producer.
 r=importlib.import_module('resaved_prefix').sources()
 paths=[HERE/'oracle.py',HERE/'test_oracle.py',HERE/'test_stop_protocol.py',HERE/'stop-correction-v2/transition.json',HERE/'producer/main.go',HERE/'producer/verify.go',HERE/'bin/producer',HERE/'producer-execution.json',HERE/'go-env.json',HERE/'go-list.json',HERE/'candidates/sealed-plan.json',*sorted((ROOT/'internal/document').glob('*.go'))]
 known={x['path']for x in r}
 for p in paths:
  rel=str(p.relative_to(ROOT))
  if rel not in known:r.append({'path':rel,'size':p.stat().st_size,'sha256':sha(p)});known.add(rel)
 return sorted(r,key=lambda x:x['path'])
def cases():
 measured=json.loads((HERE/'candidates/sealed-plan.json').read_text());result=[]
 for i,c in enumerate(measured['unique_whole_byte_candidates'],1):
  directory=HERE/'candidates'/c['name'];v=json.loads((directory/'provenance.json').read_text());actual=producer('-verify',directory/'candidate.WP5');require(actual['admitted'],'CandidateRefused','real producer must admit actual candidate')
  require(actual['body_hex']==c['body_hex'],'CandidateBody','native public consumer differs')
  require(sha(ROOT/v['loaded_source'])==v['loaded_source_sha256'],'OriginalSourceIdentity','approved original source differs')
  require(v['rights']=='project-authored scratch'and v['producer']and v['commands'],'ProducerProvenance','real public operation provenance required')
  require(sha(directory/'candidate.WP5')==c['candidate_sha256'],'CandidateIdentity','candidate modified')
  existing=c['reference_print']
  # Existing full PRN controls are only used where the producer has separately
  # bound exact original endpoint/command provenance, never by body resemblance.
  control={'kind':'new-original-control','case':'c%02d'%i}
  if existing:
   second=existing.replace('-r1/','-r2/');require(second!=existing and(ROOT/second).is_file(),'ControlRepetition','two actual independently fresh approved control paths required')
   require((ROOT/existing).read_bytes()==(ROOT/second).read_bytes(),'ControlRepetition','actual approved fresh full streams differ')
   control={'kind':'approved-existing','path':existing,'sha256':sha(ROOT/existing),'fresh_witnesses':[{'path':x,'sha256':sha(ROOT/x),'size':(ROOT/x).stat().st_size}for x in [existing,second]],'logical_original_endpoint':v['source_reference_endpoint']}
  case={'id':'c%02d'%i,'name':c['name'],'candidate':str((directory/'candidate.WP5').relative_to(ROOT)),'candidate_sha256':c['candidate_sha256'],'bytes':c['bytes'],'input_body_hex':c['body_hex'],'expected_edited_body_hex':c['body_hex']+'5a','source':v['loaded_source'],'source_sha256':v['loaded_source_sha256'],'provenance':str((directory/'provenance.json').relative_to(ROOT)),'provenance_sha256':sha(directory/'provenance.json'),'print_control':control,'exports':['C44PRE.WP5','C44FIN.WP5','C44PRN.PRN'],'required_preprint':'actual complete72-field e724/01 new-order predicate; second public Go edit Q; failure blocks','subsequent_original_edit':'normal Home3 Up End then insert Z','save_names':['C44PRE','C44FIN'],'print_name':'C44PRN','fresh_repetitions':[1,2]}
  result.append(case)
 return result

def frozen_qemu_argv(work):
 guest=importlib.import_module('guest');old=(guest.RUNTIME,guest.SOCKET)
 try:
  guest.RUNTIME=PRIVATE/'runtime/wp44';guest.SOCKET=guest.RUNTIME/'qmp.sock'
  return guest.arguments(work/'boot.img',work/'harddisk.img')
 finally:guest.RUNTIME,guest.SOCKET=old

def transition_receipt():
 path=HERE/'stop-correction-v2/transition.json';t=json.loads(path.read_text())
 require(t.get('schema')=='wordling.wp44.transition/v2'and type(t.get('historical_spent'))is int and t['historical_spent']==1 and type(t.get('new_required_positive_leaves'))is int and t['new_required_positive_leaves']==48 and type(t.get('cumulative_maximum_attempts_including_failures'))is int and t['cumulative_maximum_attempts_including_failures']==49,'TransitionAccounting','explicit49=1 spent incomplete+48 fresh positives required')
 require(t.get('protocol')=='wp44-v2'and t.get('successor_ledger_path')==str(PRIVATE/'wp44-attempts-v2.json'),'TransitionAccounting','exact new protocol and private ledger path required')
 require('executing_source'in t['predecessor']and'source_seals'in t['predecessor'],'PredecessorIdentity','actual archived predecessor source/seal bindings required')
 verify_predecessor(t)
 return t,sha(path)

def verify_predecessor(t):
 pins=t['predecessor']
 for key,pin in pins.items():
  path=Path(pin['path']);require(path.is_file()and path.stat().st_size==pin['size']and sha(path)==pin['sha256'],'PredecessorIdentity','immutable predecessor '+key+' changed')
 ledger=json.loads(Path(pins['private_ledger']['path']).read_text());report=json.loads(Path(pins['report']['path']).read_text());pre=json.loads(Path(pins['prelaunch']['path']).read_text())
 require(pins['private_ledger']['sha256']==pins['archived_ledger']['sha256']and ledger['plan_sha256']==t['predecessor_plan_sha256']and ledger['maximum']==48 and len(ledger['attempts'])==1,'PredecessorIdentity','old ledger must remain exactly one spent48-plan attempt')
 entry=ledger['attempts'][0];rows=report['results']
 require(entry['id']==t['failed_attempt_id']and entry['outcome']==t['historical_outcome']=='incomplete'and entry['result_sha256']==t['failed_result_sha256']and len(rows)==1 and canonical(rows[0])==entry['result_sha256']and report.get('complete')is False,'PredecessorIdentity','historical failed result must stay checksum-bound incomplete')
 require(report['plan_sha256']==pre['plan_sha256']==canonical(pre['plan'])==t['predecessor_plan_sha256'],'PredecessorIdentity','old source/prelaunch/plan differ')
 if 'executing_source'in pins:
  source=[x for x in pre['plan']['sources']if x['path']=='internal/document/evidence/wp44/oracle.py'];require(len(source)==1 and source[0]['sha256']==pins['executing_source']['sha256'],'PredecessorIdentity','old executing controller differs from archived prelaunch source pin')


def transition_grant_fields(t,digest):
 return {'receipt_sha256':digest,'predecessor_ledger_sha256':t['predecessor']['private_ledger']['sha256'],'predecessor_plan_sha256':t['predecessor_plan_sha256'],'historical_spent':t['historical_spent'],'new_required_positive_leaves':t['new_required_positive_leaves'],'cumulative_maximum_attempts_including_failures':t['cumulative_maximum_attempts_including_failures']}

def empty_successor_ledger(p):
 return {'schema':'wordling.wp44.ledger/v2','protocol':'wp44-v2','plan_sha256':canonical(p),'transition_receipt_sha256':p['transition_receipt_sha256'],'predecessor':p['transition']['predecessor'],'historical_spent':p['historical_spent'],'historical_failed_attempt':{'id':p['transition']['failed_attempt_id'],'outcome':'incomplete','result_sha256':p['transition']['failed_result_sha256'],'qualified':False},'required_current_positives':p['new_required_positive_leaves'],'cumulative_maximum':p['cumulative_maximum_attempts_including_failures'],'attempts':[]}

def validate_successor_ledger(p,aggregate):
 expected=empty_successor_ledger(p)
 require(canonical({k:v for k,v in aggregate.items()if k!='attempts'})==canonical({k:v for k,v in expected.items()if k!='attempts'}),'AggregatePlanMismatch','successor ledger plan/transition/accounting differs')
 prior=aggregate.get('attempts');require(isinstance(prior,list),'AggregatePlanMismatch','current attempts list required')
 ids=[x['id']for x in prior];allowed={x['id']for x in p['attempts']}
 require(len(set(ids))==len(ids)and all(i in allowed and i!=p['transition']['failed_attempt_id']for i in ids),'PriorAttempt','duplicate/historical/unknown current leaf forbidden')
 require(type(aggregate['historical_spent'])is int and aggregate['historical_spent']==1 and aggregate['historical_spent']+len(prior)<=aggregate['cumulative_maximum']and len(prior)<=aggregate['required_current_positives'],'AttemptLimit','historical+current failure-inclusive cap exceeded')
 require(all(x.get('outcome')=='complete-observation'for x in prior),'PriorIncomplete','new-protocol first failure is sticky; no implicit continuation')
 return prior

def plan():
 base=importlib.import_module('resaved_prefix').plan() # private read-only metadata checks; no VM/lock
 listing=subprocess.run(['mdir','-i',str(PRIVATE/'master/harddisk.img')+'@@1048576','::OUT/'],capture_output=True,timeout=15,check=True).stdout
 require(not any(n in listing.upper()for n in [b'C44PRE',b'C44FIN',b'C44PRN',b'C44INPUT',b'C44SEED']),'PreexistingOutput','declared scratch input/output names must be absent from immutable master')
 t,transition_hash=transition_receipt();cs=cases();attempts=[]
 for c in cs:
  modes=['control','candidate']if c['print_control']['kind']=='new-original-control'else['candidate']
  for mode in modes:
   for repeat in [1,2]:
    ident='wp44-v2-'+c['id']+'-'+mode+'-r'+str(repeat);work=PRIVATE/'runs'/ident
    attempts.append({'id':ident,'case':c['id'],'mode':mode,'repetition':repeat,'private_work':str(work),'qemu_argv':frozen_qemu_argv(work),'leaf_selection_argv':['--attempt',ident]})
 require(len(attempts)==48,'TransitionAccounting','all48 fresh current proof leaves remain required')
 return {'schema':'wordling.wp44.plan/v2','protocol':'wp44-v2','transition':t,'transition_receipt_sha256':transition_hash,'required_grant_transition_fields':transition_grant_fields(t,transition_hash),'historical_spent':1,'new_required_positive_leaves':48,'cumulative_maximum_attempts_including_failures':49,'status':'offline; no grant','run_id':'wp44-c-v2','chunk_contract':{'grant_id':'safe unique wp44-v2-* identifier','exact_attempt_ids':'explicit subset of frozen48, no automatic continuation/retry','aggregate_ledger':str(PRIVATE/'wp44-attempts-v2.json'),'first_requested_subset':['wp44-v2-c09-candidate-r1','wp44-v2-c09-candidate-r2']},'sources':sources(),'cases':cs,'attempts':attempts,'master_OUT_listing_sha256':hashlib.sha256(listing).hexdigest(),'declared_scratch_names_absent_from_master':True,'maximum_current_attempts_including_failures':len(attempts),'first_request_argv':[sys.executable,str(HERE/'oracle.py'),'run','--grant-id','wp44-v2-phase01','--attempt','wp44-v2-c09-candidate-r1','--attempt','wp44-v2-c09-candidate-r2','--allow-vm','--grant','/tmp/wordling-WP44-root-grant-v2.json'],'fresh_repetitions':2,'producer_execution':json.loads((HERE/'producer-execution.json').read_text()),'master':base['master'],'manuals':base['manuals'],'tools':base['tools'],'preboot_resources':base['preboot_resources'],'profile_id':base['profile_id'],'profile_sha256':base['profile_sha256'],'shared_lock':str(PRIVATE/'session1.lock'),'socket':str(PRIVATE/'runtime/wp44/qmp.sock'),'timeout_per_attempt_seconds':900,'order':['read-only initial settings capture (native_edits.settings; no baseline_settings)','captured explicit FastSaveNo (approved42)','retrieve exact Go candidate, OR exact approved42 source and original-only logical producer commands','normal and Reveal/cursor captures; return normal without Save','declared original EOF Z','distinct C44PRE Save; no print-port/path changes before this Save','approved14 text_layout.print_disk C44PRN Other-port setup, full completed queue','distinct C44FIN Save','approved39 captured exit_state protocol to actual DOS','positive owned PID/argv/private disks/startticks; same identity before stop','exact normal QMP stop then identity-aware monotonic5s/.05s bounded observations; gone/sameZ plus absent socket before extraction','all required exports successful nonempty actual size/SHA; per-attempt master equality; first fault halts ENTIRE grant'],'rights':'project-authored scratch and Go output; private programs/manuals/settings/resources never published','limits':'selected StandardPrinter/QEMU/FreeDOS; operator-injected QMP keys, no physical Linux keys/font metrics/historicalDOS/fullM1 claim','on_first_incomplete':'retain report/raw/private disk; no retry or next guest; root adjudicates','full_M1_accepted':False}

def check():
 p=plan();measured=json.loads((HERE/'candidates/sealed-plan.json').read_text())
 for c in measured['cases']:
  d=HERE/'candidates'/c['name'];alias=HERE/'candidates'/c['whole_byte_alias_of']
  require((d/'candidate.WP5').read_bytes()==(alias/'candidate.WP5').read_bytes(),'AliasIdentity','whole-byte alias mismatch')
 for name,want in measured['source_hashes'].items():require(sha(ROOT/name)==want,'ProducerSourceDrift',name)
 return p

def owned_identity(qmp,work,expected_argv):
 pidfile=qmp.RUNTIME/'qemu.pid'
 require(pidfile.is_file(),'MissingOwnedPID','no actual positive owned PID; do not stop/extract')
 try:pid=int(pidfile.read_text())
 except ValueError:raise Refusal('MissingOwnedPID','PID not integer')
 require(pid>0,'MissingOwnedPID','PID must be positive')
 proc=Path('/proc')/str(pid);argv=(proc/'cmdline').read_bytes().split(b'\0');argv=[os.fsdecode(x)for x in argv if x]
 require(all(any(str(work/n)in a for a in argv)for n in ['boot.img','harddisk.img']),'ForeignOwnedDisks','actual process does not bind both private disks')
 require(any(a.startswith('unix:'+str(qmp.SOCKET)+',')for a in argv),'ForeignOwnedSocket','actual process socket differs')
 require((proc/'exe').resolve()==Path(shutil.which(expected_argv[0])or expected_argv[0]).resolve(),'ForeignOwnedBinary','actual QEMU executable differs')
 require(argv[1:]==expected_argv[1:],'ForeignOwnedArgv','actual process flags/resources differ from frozen launch')
 start=(proc/'stat').read_text().split(') ',1)[1].split()[19]
 require(start.isdigit()and int(start)>0,'MissingStartIdentity','actual startticks unavailable')
 return {'pid':pid,'argv':argv,'startticks':start,'executable':str((proc/'exe').resolve(strict=True)),'private_disks':[str(work/n)for n in ['boot.img','harddisk.img']],'socket':str(qmp.SOCKET)}
def same_identity(identity):
 require(isinstance(identity,dict)and type(identity.get('pid'))is int and identity['pid']>0,'MissingOwnedPID','owned start identity missing')
 proc=Path('/proc')/str(identity['pid'])
 require((proc/'stat').is_file(),'OwnedDiedEarly','owned guest died before normal stop')
 require((proc/'stat').read_text().split(') ',1)[1].split()[19]==identity['startticks'],'PIDReused','owned PID start identity changed')
 argv=[os.fsdecode(x)for x in(proc/'cmdline').read_bytes().split(b'\0')if x]
 require(argv==identity['argv'],'OwnedArgvChanged','actual process argv changed')
 require(str((proc/'exe').resolve(strict=True))==identity['executable'],'ForeignOwnedIdentity','actual owned executable changed before stop')
def validate_stop_identity(qmp,identity):
 require(isinstance(identity,dict)and type(identity.get('pid'))is int and identity['pid']>0,'MissingOwnedPID','positive captured owned PID required before observation')
 require(isinstance(identity.get('startticks'),str)and identity['startticks'].isdigit()and int(identity['startticks'])>0 and isinstance(identity.get('argv'),list)and bool(identity['argv'])and all(isinstance(x,str)for x in identity['argv'])and isinstance(identity.get('executable'),str)and bool(identity['executable']),'MissingOwnedIdentity','captured startticks/argv/executable required before observation')
 require(identity.get('socket')==str(qmp.SOCKET)and isinstance(identity.get('private_disks'),list)and len(identity['private_disks'])==2 and all(isinstance(d,str)and any(d in a for a in identity['argv'])for d in identity['private_disks'])and any(a.startswith('unix:'+str(qmp.SOCKET)+',')for a in identity['argv']),'MissingOwnedIdentity','captured private disk/socket identity required before observation')

def observe_owned_stop(qmp,identity):
 row={'pid':identity['pid'],'pid_present':None,'socket_present':None,'state':None,'startticks':None}
 try:return observe_owned_stop_files(qmp,identity,row)
 except Exception as error:
  row.update(classification='observation-error',reason=str(error),error_code=getattr(error,'code',type(error).__name__));return row

def observe_owned_stop_files(qmp,identity,row):
 try:qmp.SOCKET.lstat();row['socket_present']=True
 except FileNotFoundError:row['socket_present']=False
 proc=Path('/proc')/str(identity['pid'])
 try:proc.stat();row['pid_present']=True
 except FileNotFoundError:row.update(pid_present=False,classification='gone',reason='owned PID directory absent');return row
 try:raw=(proc/'stat').read_text()
 except FileNotFoundError:row.update(classification='resample',reason='PID/stat disappeared between directory and stat read');return row
 row['raw_stat']=raw;parts=raw.split(') ',1)
 require(len(parts)==2,'StopStatMalformed','owned /proc stat has no complete command delimiter')
 fields=parts[1].split();require(len(fields)>19 and len(fields[0])==1 and fields[19].isdigit(),'StopStatMalformed','owned /proc stat truncated or malformed')
 row.update(state=fields[0],startticks=fields[19],raw_stat=raw)
 if row['startticks']!=identity['startticks']:row.update(classification='pid-reused',reason='owned PID now has different startticks');return row
 if row['state']=='Z':row.update(classification='zombie',reason='same captured identity is zombie');return row
 require(row['state']in 'RSDTtXxKWPI','StopStatMalformed','unknown owned PID state')
 try:
  argv=[os.fsdecode(x)for x in(proc/'cmdline').read_bytes().split(b'\0')if x]
  # A teardown race may empty cmdline before Z. It is NOT positive evidence;
  # record and resample until a terminal observation or the deadline.
  if not argv:row.update(classification='resample',reason='same startticks but empty live cmdline; terminal state unproved');return row
  row['argv']=argv
  if argv!=identity['argv']:row.update(classification='foreign-identity',reason='same PID live argv differs from captured private guest');return row
  exe=str((proc/'exe').resolve(strict=True));row['executable']=exe
  if exe!=identity['executable']:row.update(classification='foreign-identity',reason='live executable differs from captured private guest');return row
 except FileNotFoundError:row.update(classification='resample',reason='PID disappeared while checking live argv/executable');return row
 row.update(classification='live',reason='same captured startticks/argv/executable remains live');return row

def stopped(qmp,identity,*,observations=None,observe=None,clock=None,pause=None,timeout=5.0,interval=.05):
 """Observe bounded shutdown completion; never signal, unlink or guess grace."""
 validate_stop_identity(qmp,identity)
 require(0<interval<=timeout<=5.0,'StopPollBudget','fixed maximum5s observation budget required')
 observe=observe or observe_owned_stop;clock=clock or time.monotonic;pause=pause or time.sleep
 log=observations if observations is not None else [];start=clock();deadline=start+timeout
 for _ in range(102):
  now=clock();entry={'monotonic':now,'elapsed_seconds':now-start,'deadline_monotonic':deadline};log.append(entry)
  try:entry.update(observe(qmp,identity))
  except Exception as error:
   entry.update(classification='observation-error',reason=str(error),error_code=getattr(error,'code',type(error).__name__))
   raise Refusal(getattr(error,'code','StopObservationError'),'owned stop observation refused: '+str(error))from error
  entry['observation_complete_monotonic']=clock();kind=entry.get('classification')
  require(kind!='observation-error',entry.get('error_code','StopObservationError'),'owned observation error: '+entry.get('reason','unknown'))
  require(kind!='pid-reused','OwnedPIDReused','PID reused/changed startticks; refuse immediately')
  require(kind!='foreign-identity','ForeignOwnedIdentity','live process differs from captured guest; refuse immediately')
  require(kind in ['gone','zombie','live','resample']and type(entry.get('socket_present'))is bool,'StopObservationError','unclassified stop observation')
  if kind in ['gone','zombie']and not entry['socket_present']:
   require(entry['observation_complete_monotonic']<=deadline,'OwnedStopDeadline','terminal observation occurred after deadline')
   require(kind!='gone'or entry.get('pid_present')is False,'StopObservationError','PID absence not actually observed')
   require(kind!='zombie'or(entry.get('state')=='Z'and entry.get('startticks')==identity['startticks']),'OwnedPIDReused','zombie is not captured identity')
   return {'pid':identity['pid'],'startticks':identity['startticks'],'gone_or_same_zombie':True,'socket_absent':True,'elapsed_seconds':clock()-start,'observations':log}
  remaining=deadline-clock()
  require(remaining>0,'OwnedStopDeadline','owned PID/socket completion not proved within5s; no extraction')
  pause(min(interval,remaining)) # scheduling between observations, never proof
 raise Refusal('StopObservationLimit','bounded observer count exhausted; no extraction')

def original_control(p,c,n):
 name=c['name'];p.retrieve('C:\\OUT\\C44SEED','control-source-retrieved')
 if name.startswith('ascii-insert-'):
  n.MutationProbe.at(p,int(name.rsplit('-',1)[1]),False);p.type('X')
 elif name.startswith('code-typeover-'):
  n.MutationProbe.at(p,int(name.rsplit('-',1)[1]),True);p.key('insert');p.type('XY');p.key('insert')
 elif name=='two-pair-insert':
  p.key('home,home,home,up,end');p.type('X')
 elif name=='opening-literal-empty-restore':
  n.MutationProbe.at(p,1,True);p.key('alt-f4,right,backspace');p.q.wait_for('Delete Block?');p.capture('control-block-question');p.key('y');p.q.wait_absent('Delete Block?')
  n.browse(p,'control-before-Restore',previous=1);n.browse(p,'control-Restore',restore=True)
 elif name=='closing-literal-empty-restore':
  # Exactly the measured seeded/pre-browsed/Right-separated closing context;
  # no hidden Save/clear/retrieve/pane switch between target and immediate F1.
  p.key('home,home,home,up');p.type('S');p.key('home,home,home,up,delete');n.browse(p,'control-seed',previous=3);p.key('right')
  p.key('right,right,right,alt-f3,alt-f4,right,backspace');p.q.wait_for('Delete Block?');p.capture('control-closing-question');p.key('y');p.q.wait_absent('Delete Block?');n.browse(p,'control-immediate-target',previous=3);n.browse(p,'control-closing-Restore',restore=True)
 else:raise Refusal('UnknownControl','no declared missing-control recipe')
 p.normal();p.capture('control-derived-result-normal')

def perform(p,c,mode):
 session,n,fields,quit_module,layout=helpers()
 n.settings(p);settings=fields.capture_fast_save(p,'disabled')
 if mode=='control':original_control(p,c,n)
 else:p.retrieve('C:\\OUT\\C44INPUT','candidate-exact-retrieved')
 p.capture('input-normal');p.key('home,home,home,up,alt-f3');p.q.wait_for('Reveal Codes to restore');p.capture('input-reveal-gap0');p.key('alt-f3')
 p.key('home,home,home,up,end');p.capture('before-subsequent-Z');p.type('Z');p.capture('after-subsequent-Z')
 session.save_complete(p,'C44PRE',fields.save_named)
 layout.print_disk(p,'C44PRN')
 session.save_complete(p,'C44FIN',fields.save_named)
 exits=quit_module.finish_original(p)
 return {'fast_save':settings,'exit_actions':exits}

def extract(session,work,target,p,row,case,leaf):
 require(row.get('guest_stopped')is True,'StopUnproven','no stopped extraction')
 row['settings_after']=session.settings_snapshot(work,'after');exports=[]
 for name,host in p.exports:
  out=target/host;r=subprocess.run(['mcopy','-i',str(work/'harddisk.img')+'@@1048576','::OUT/'+name,str(out)],capture_output=True,timeout=15)
  ent={'name':name,'path':str(out),'exit':r.returncode,'stderr':r.stderr.decode(errors='replace')};exports.append(ent);row['exports']=exports
  require(r.returncode==0,'RequiredExportFailed',name)
  require(out.is_file()and out.stat().st_size>0,'RequiredExportMissing',name)
  ent.update(size=out.stat().st_size,sha256=sha(out))
 require({x['path'].rsplit('/',1)[-1]for x in exports}==set(case['exports']),'RequiredExportMissing','exact declared native/stream export set required')
 for name in case['exports']:require((target/name).is_file()and(target/name).stat().st_size>0,'RequiredExportMissing',name)
 asset='C44INPUT'if leaf['mode']=='candidate'else'C44SEED';seed=target/'input-after.WP5';r=subprocess.run(['mcopy','-i',str(work/'harddisk.img')+'@@1048576','::OUT/'+asset,str(seed)],capture_output=True,timeout=15)
 require(r.returncode==0 and seed.is_file(),'RequiredInputMissing','stopped source asset must be exported')
 expected=case['candidate_sha256']if leaf['mode']=='candidate'else case['source_sha256'];require(sha(seed)==expected,'InputChanged','original changed readonly scratch input')
 row['input_after']={'path':str(seed),'size':seed.stat().st_size,'sha256':sha(seed),'exact_prelaunch_input':True}
 row['exports_complete']=True

def qualify_exports(target,case,leaf=None,control_path=None):
 pre=producer('-verify',target/'C44PRE.WP5','-reedit-out',target/'second-Go-edit.WP5')
 require(pre['admitted'],'RequiredPreprintRefused','required actual e724/01 preprint did not qualify')
 changes=native_delta(ROOT/case['candidate'],target/'C44PRE.WP5',pre['inspection'],case['expected_edited_body_hex'])
 post=producer('-verify',target/'C44FIN.WP5')
 require(post['exact_no_edit']and post['body_hex']==case['expected_edited_body_hex']and not post['admitted'],'RequiredPostprintRefusal','post-print raw output/body/refusal differs')
 if leaf is not None and leaf['mode']=='candidate':
  ctl=case['print_control']
  if ctl['kind']=='approved-existing':
   witness=next(x for x in ctl['fresh_witnesses']if x['path']==ctl['path']);reference=checked_export_bytes(ROOT/ctl['path'],witness['size'],witness['sha256'])
  else:reference=pinned_control_bytes(control_path)
  require((target/'C44PRN.PRN').read_bytes()==reference,'RequiredPrintControlMismatch','full original print stream differs')
 return {'preprint':pre,'postprint':post,'indexed_prefix_deltas':changes,'new_original_control_binding':control_path,'purpose':'required stopped-export qualification, not full post-release audit or M1 claim'}

def attempt(session,qmp,guest,n,case,leaf,target,work):
 row={'id':leaf['id'],'case':leaf['case'],'mode':leaf['mode'],'repetition':leaf['repetition'],'outcome':'incomplete','guest_stopped':False};p=None;identity=None
 try:
  assets=[('C44INPUT',ROOT/case['candidate'])]if leaf['mode']=='candidate'else[('C44SEED',ROOT/case['source'])]
  session.QMP_AUDIT_FILE=target/'qmp-wire.jsonl';signal.setitimer(signal.ITIMER_REAL,900)
  argv=session.fresh_start(qmp,guest,work,assets);row['qemu_argv']=argv
  require(argv==leaf['qemu_argv'],'LaunchArgv','actual launch differs from exact frozen argv')
  identity=owned_identity(qmp,work,argv);row['owned_start_identity']=identity
  with qmp.QMP()as q:
   p=n.MutationProbe(q,target);row['observations']=perform(p,case,leaf['mode'])
   require((target/'clean-exit/screen.txt').read_text().splitlines()[0]=='C:\\WP51>','NormalDOSMissing','actual clear DOS capture required')
   row['normal_DOS']=True
 except Exception as error:row.update(error=str(error),error_code=getattr(error,'code',type(error).__name__),traceback=traceback.format_exc())
 finally:
  signal.setitimer(signal.ITIMER_REAL,0)
  if identity is None and qmp.SOCKET.exists():
   try:identity=owned_identity(qmp,work,row.get('qemu_argv')or guest.arguments(work/'boot.img',work/'harddisk.img'));row['owned_start_identity']=identity
   except Exception as error:row['identity_error']=str(error)
  if identity is not None:
   try:
    validate_stop_identity(qmp,identity);same_identity(identity);row['stop_method']=session.stop_owned(qmp,guest)
    require(row['stop_method']=='QMP quit; own socket terminated','HostContained','host containment is not normal original completion; no stop proof/extraction')
    row['stop_observations']=[];row['stop_proof']=stopped(qmp,identity,observations=row['stop_observations']);row['guest_stopped']=True
   except Exception as error:row.update(stop_error=str(error),stop_error_code=getattr(error,'code',type(error).__name__))
  else:row['stop_error']='positive owned PID/argv/disks/startticks unavailable; no stop/extraction claim'
  if row['guest_stopped']and p is not None:
   try:extract(session,work,target,p,row,case,leaf)
   except Exception as error:row.update(extraction_error=str(error),extraction_error_code=getattr(error,'code',type(error).__name__))
  else:row['extraction_skipped']='owned stop or probe/export list unproven; retain private disk'
  if p is not None:row.update(trace=p.trace,checks=p.checks,settings=p.settings)
  if row.get('normal_DOS')and row['guest_stopped']and row.get('exports_complete')and not any(k in row for k in ['error','stop_error','extraction_error']):row['outcome']='complete-observation'
 return row

def selected_attempts(args,p,grant):
 require(re.fullmatch(r'wp44-v2-[a-z0-9-]{1,20}',args.grant_id or ''),'GrantID','unique safe explicit chunk ID required')
 ids=args.attempt
 require(bool(ids)and len(set(ids))==len(ids),'AttemptSelection','nonempty unique exact attempt subset required')
 lookup={leaf['id']:leaf for leaf in p['attempts']}
 require(all(i in lookup for i in ids),'AttemptSelection','only frozen leaves allowed')
 require(grant.get('authorized')is True and grant.get('plan_sha256')==canonical(p)and grant.get('grant_id')==args.grant_id and grant.get('attempt_ids')==ids and type(grant.get('maximum_aggregate_attempts'))is int and grant['maximum_aggregate_attempts']==p['cumulative_maximum_attempts_including_failures'],'GrantMismatch','explicit grant must bind exact source/plan/subset/49 cumulative cap')
 transition=grant.get('transition_authorization',{});require(transition.get('authorized_by_root')is True and canonical({k:v for k,v in transition.items()if k!='authorized_by_root'})==canonical(p['required_grant_transition_fields']),'TransitionAuthorization','separate exact root transition authorization required')
 if 'argv'in grant:require(grant['argv']==[sys.executable,*sys.argv],'GrantArgv','actual invocation differs from root grant')
 return [lookup[i]for i in ids]

def checked_export_bytes(path,size,digest):
 path=Path(path)
 require(type(size)is int and size>0 and isinstance(digest,str)and re.fullmatch('[0-9a-f]{64}',digest)and path.is_file()and not path.is_symlink(),'ControlExportIdentity','pinned control export metadata/file missing or invalid')
 raw=path.read_bytes()
 require(len(raw)==size and hashlib.sha256(raw).hexdigest()==digest,'ControlExportIdentity','control export differs from recorded size/SHA')
 return raw

def pinned_control_bytes(pin):
 require(isinstance(pin,dict)and pin.get('kind')=='recorded-original-control','ControlResultIdentity','recorded control pin required')
 # The report may gain later attempt rows between chunks. A pin binds its exact
 # current report bytes during THIS candidate, and its checksum-bound control row
 # is resolved again from the ledger for each later candidate/chunk.
 for key in ['report','prelaunch']:
  path=Path(pin[key]);require(path.is_file()and sha(path)==pin[key+'_sha256'],'ControlResultIdentity','referenced control '+key+' changed during candidate')
 report=json.loads(Path(pin['report']).read_text());rows=[x for x in report['results']if x.get('id')==pin['leaf_id']]
 require(len(rows)==1 and canonical(rows[0])==pin['result_sha256'],'ControlResultIdentity','referenced checksum-bound control result changed')
 return checked_export_bytes(pin['path'],pin['size'],pin['sha256'])

def archive_control_pin(pin,target):
 if pin is None:return None
 pinned_control_bytes(pin)
 archive=target/'control-custody';archive.mkdir()
 pin=dict(pin);pin['archived_inputs']={}
 for name,key in [('control-run.json','report'),('control-prelaunch.json','prelaunch'),('control.PRN','path')]:
  source=Path(pin[key]);destination=archive/name;destination.write_bytes(source.read_bytes())
  digest=pin['sha256']if key=='path'else pin[key+'_sha256']
  require(sha(destination)==digest,'ControlExportIdentity'if key=='path'else'ControlResultIdentity','control custody changed during preboot archival')
  pin['archived_inputs'][key]={'path':str(destination),'sha256':digest}
 return pin

def control_from_ledger(case,leaf,prior,expected_plan_sha256=None):
 if leaf['mode']!='candidate' or case['print_control']['kind']=='approved-existing':return None
 wanted='wp44-v2-'+case['id']+'-control-r'+str(leaf['repetition'])
 matches=[x for x in prior if x['id']==wanted and x.get('outcome')=='complete-observation']
 require(len(matches)==1,'MissingControl','corresponding frozen original-only control not yet complete')
 entry=matches[0];grant_id=entry.get('grant_id')
 require(isinstance(grant_id,str)and re.fullmatch(r'wp44-[a-z0-9-]{1,24}',grant_id),'ControlResultIdentity','control grant identity invalid')
 require(entry.get('case')==case['id']and entry.get('mode')=='control'and type(entry.get('repetition'))is int and entry['repetition']==leaf['repetition'],'ControlResultIdentity','ledger control case/mode/repetition differs')
 directory=HERE/'runs'/grant_id;report_path=directory/'run.json';prelaunch_path=directory/'prelaunch.json'
 require(report_path.is_file()and prelaunch_path.is_file(),'ControlResultMissing','recorded completed control result/prelaunch required')
 report=json.loads(report_path.read_text());prelaunch=json.loads(prelaunch_path.read_text());grant=prelaunch.get('grant',{})
 require(expected_plan_sha256 is not None and report.get('plan_sha256')==expected_plan_sha256 and report.get('grant_id')==grant_id and prelaunch.get('plan_sha256')==expected_plan_sha256 and canonical(prelaunch['plan'])==expected_plan_sha256,'ControlResultIdentity','control result/source plan differs from active grant')
 require(grant.get('authorized')is True and grant.get('grant_id')==grant_id and grant.get('plan_sha256')==expected_plan_sha256 and wanted in grant.get('attempt_ids',[])and wanted in report.get('selected_attempt_ids',[]),'ControlResultIdentity','control leaf was not bound to the archived exact grant')
 declared=[x for x in prelaunch['plan']['attempts']if x.get('id')==wanted]
 require(len(declared)==1 and declared[0]['case']==case['id']and declared[0]['mode']=='control'and type(declared[0]['repetition'])is int and declared[0]['repetition']==leaf['repetition'],'ControlResultIdentity','archived control leaf/case/repetition differs')
 rows=[x for x in report.get('results',[])if x.get('id')==wanted]
 require(len(rows)==1 and canonical(rows[0])==entry.get('result_sha256'),'ControlResultIdentity','ledger checksum does not bind the recorded prior result')
 row=rows[0]
 require(row.get('case')==case['id']and row.get('mode')=='control'and type(row.get('repetition'))is int and row['repetition']==leaf['repetition']and row.get('outcome')=='complete-observation','ControlResultIdentity','recorded control case/mode/repetition/outcome differs')
 exports=[x for x in row.get('exports',[])if x.get('name')=='C44PRN.PRN'];path=directory/wanted/'C44PRN.PRN'
 require(len(exports)==1 and exports[0].get('path')==str(path)and type(exports[0].get('exit'))is int and exports[0]['exit']==0,'ControlExportIdentity','exact successful recorded control PRN export required')
 export=exports[0];pin={'kind':'recorded-original-control','leaf_id':wanted,'case':case['id'],'repetition':leaf['repetition'],'grant_id':grant_id,'result_sha256':entry['result_sha256'],'plan_sha256':expected_plan_sha256,'report':str(report_path),'report_sha256':sha(report_path),'prelaunch':str(prelaunch_path),'prelaunch_sha256':sha(prelaunch_path),'path':str(path),'size':export.get('size'),'sha256':export.get('sha256')}
 pinned_control_bytes(pin) # Under the actual guard, BEFORE recording/booting candidate.
 return pin

def run(args):
 require(args.allow_vm,'AuthorizationRequired','offline only; explicit root grant required')
 p=check();grant=json.loads(Path(args.grant).read_text());selected=selected_attempts(args,p,grant)
 out=HERE/'runs'/args.grant_id;require(not out.exists(),'PriorEvidence','fresh chunk only');out.mkdir(parents=True)
 for source in p['sources']:
  src=ROOT/source['path'];dst=out/'runner-source'/source['path'];dst=dst.with_name(dst.name+'.txt')if dst.suffix=='.go'else dst;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 for c in p['cases']:
  for key in ['candidate','source','provenance']:
   src=ROOT/c[key];dst=out/'inputs'/c['id']/key;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
  for control in c['print_control'].get('fresh_witnesses',[]):
   dst=out/'inputs'/c['id']/Path(control['path']).parent.name/Path(control['path']).name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/control['path'],dst)
 for key,pin in p['transition']['predecessor'].items():
  source=Path(pin['path']);dest=out/'predecessor'/(key+('.py.txt'if key=='executing_source'else'.json'));dest.parent.mkdir(exist_ok=True);shutil.copyfile(source,dest);require(sha(dest)==pin['sha256'],'PredecessorIdentity','predecessor archive differs')
 dump(out/'prelaunch.json',{'plan':p,'plan_sha256':canonical(p),'grant':grant,'argv':[sys.executable,*sys.argv]})
 session,n,fields,quit_module,layout=helpers();qmp,guest,private=session.configure(PRIMARY,'wp44');n.qmp=qmp
 report={'protocol':'wp44-v2','transition_receipt_sha256':p['transition_receipt_sha256'],'historical_spent':p['historical_spent'],'cumulative_maximum':p['cumulative_maximum_attempts_including_failures'],'grant_id':args.grant_id,'selected_attempt_ids':[x['id']for x in selected],'plan_sha256':canonical(p),'results':[],'guard_released':False,'oracle_released':False,'full_M1_accepted':False}
 old=signal.signal(signal.SIGALRM,session.timeout_signal)
 try:
  with session.exclusive(private):
   try:
    report['master_before']={name:sha(guest.MASTER/name)for name in p['master']};require(report['master_before']==p['master'],'MasterChanged','master differs before start')
    verify_predecessor(p['transition'])
    ledger=private/'wp44-attempts-v2.json';aggregate=json.loads(ledger.read_text())if ledger.exists()else empty_successor_ledger(p)
    prior=validate_successor_ledger(p,aggregate)
    require(not any(x['id']in report['selected_attempt_ids']for x in prior),'PriorAttempt','no repeated leaf/retry')
    require(p['historical_spent']+len(prior)+len(selected)<=p['cumulative_maximum_attempts_including_failures']and len(prior)+len(selected)<=p['new_required_positive_leaves'],'AttemptLimit','49 cumulative ceiling includes original spent1 and all new failures')
    dump(ledger,aggregate)
    for leaf in selected:
     verify_predecessor(p['transition'])
     for src in p['sources']:require(sha(ROOT/src['path'])==src['sha256'],'SourceDrift',src['path'])
     case=next(c for c in p['cases']if c['id']==leaf['case']);control_path=control_from_ledger(case,leaf,prior,canonical(p))
     for key in ['candidate','source','provenance']:require(sha(ROOT/case[key])==case[key+'_sha256'],'InputSourceDrift',case[key])
     for control in case['print_control'].get('fresh_witnesses',[]):require(sha(ROOT/control['path'])==control['sha256'],'ControlDrift',control['path'])
     target=out/leaf['id'];target.mkdir();control_path=archive_control_pin(control_path,target);work=Path(leaf['private_work'])
     require(not work.exists()and not qmp.SOCKET.exists(),'ForeignRuntime','never reuse/stop foreign guest')
     entry={'id':leaf['id'],'case':leaf['case'],'mode':leaf['mode'],'repetition':leaf['repetition'],'grant_id':args.grant_id,'outcome':'incomplete','started_at':datetime.now(timezone.utc).isoformat()};prior.append(entry);dump(ledger,aggregate)
     row=attempt(session,qmp,guest,n,case,leaf,target,work);report['results'].append(row)
     try:
      if row['outcome']=='complete-observation':row['required_output_qualification']=qualify_exports(target,case,leaf,control_path)
      row['master_after']={name:sha(guest.MASTER/name)for name in p['master']};require(row['master_after']==p['master'],'MasterChanged','master changed after attempt')
     except Exception as error:row.update(outcome='required-output-or-master-unproven',required_output_or_master_error=str(error),required_output_or_master_error_code=getattr(error,'code',type(error).__name__))
     entry['outcome']=row['outcome'];entry['result_sha256']=canonical(row);report['cumulative_spent']=p['historical_spent']+len(prior);dump(ledger,aggregate);dump(out/'aggregate-ledger.json',aggregate);dump(out/'run.json',report)
     if row['outcome']!='complete-observation':report['halted_before_next_guest']=True;break
   except Exception as error:report.update(batch_error=str(error),batch_error_code=getattr(error,'code',type(error).__name__),halted_before_next_guest=True)
   finally:
    try:report['master_after']={name:sha(guest.MASTER/name)for name in p['master']};report['master_unchanged']=report.get('master_before')==report['master_after']
    except Exception as error:report['master_error']=str(error)
    dump(out/'run.json',report)
  report['guard_released']=True;report['oracle_released']=bool(report['results'])and all(r['guest_stopped']for r in report['results'])and not qmp.SOCKET.exists()
 finally:
  signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,old);report['complete']=len(report['results'])==len(selected)and all(r['outcome']=='complete-observation'for r in report['results'])and report.get('master_unchanged')is True;report['current48_complete']=len(prior)==p['new_required_positive_leaves']and all(x.get('outcome')=='complete-observation'for x in prior)if 'prior'in locals()else False;dump(out/'run.json',report)
 print(json.dumps({'complete':report['complete'],'oracle_released':report['oracle_released'],'attempted':len(report['results']),'current48_complete':report['current48_complete'],'historical_spent':p['historical_spent'],'cumulative_spent':p['historical_spent']+len(prior)if 'prior'in locals()else p['historical_spent']}));return 0 if report['complete']else 1

def native_delta(candidate,original,inspection,expected_body):
 raw=Path(candidate).read_bytes();after=Path(original).read_bytes();body=inspection['Body'];B=body['Offset']
 require(after[B:].hex()==expected_body,'OriginalBodyMismatch','declared subsequent original edit differs')
 flags=next(p['Data']['Offset']for p in inspection['Packets']if p['Type']==6)
 require(len(raw[:B])==len(after[:B]),'PrefixDelta','prefix size changed')
 changes=[]
 for i,(a,b)in enumerate(zip(raw[:B],after[:B])):
  if a!=b:
   require(i==flags and a==8 and b==0,'PrefixDelta','unexplained prefix delta at '+str(i));changes.append({'offset':i,'input':a,'original':b,'reason':'indexed must-format08 input; original disabled save00'})
 return changes

def result(path):
 report=json.loads(Path(path).read_text());require(report.get('complete')is True,'IncompleteBatch','not complete')
 pre=json.loads((Path(path).parent/'prelaunch.json').read_text());p=pre['plan'];require(canonical(p)==report['plan_sha256'],'PlanIdentity','plan changed');checks=[]
 selected=[next(x for x in p['attempts']if x['id']==i)for i in report['selected_attempt_ids']]
 for leaf,row in zip(selected,report['results']):
  require(row['id']==leaf['id']and row['outcome']=='complete-observation'and row['exports_complete']and row['guest_stopped'],'IncompleteAttempt','exact complete attempt required')
  c=next(x for x in p['cases']if x['id']==leaf['case']);target=Path(path).parent/leaf['id']
  for export in row['exports']:require(Path(export['path']).stat().st_size==export['size']and sha(export['path'])==export['sha256'],'RawIdentity','export changed')
  # The actual product checks/read-only reopen and second Go edit are separate
  # from original timing: this audit runs only after oracle release.
  require(report['oracle_released']and report['guard_released'],'OracleNotReleased','release before offline audit')
  native=producer('-verify',target/'C44PRE.WP5','-reedit-out',Path(tempfile.gettempdir())/('wp44-second-edit-'+leaf['id']+'.WP5'));require(native['body_hex']==c['expected_edited_body_hex'],'OriginalBodyMismatch','preprint actual original body differs')
  deltas=native_delta(ROOT/c['candidate'],target/'C44PRE.WP5',native['inspection'],c['expected_edited_body_hex'])
  post=producer('-verify',target/'C44FIN.WP5');require(post['body_hex']==c['expected_edited_body_hex']and not post['admitted'],'PostprintRefusal','postprint must remain exact read-only')
  if leaf['mode']=='candidate':
   control=c['print_control'];reference=ROOT/control['path']if control['kind']=='approved-existing'else control_from_ledger(c,leaf,json.loads((Path(path).parent/'aggregate-ledger.json').read_text())['attempts'],canonical(p))
   if control['kind']=='approved-existing':
    witness=next(x for x in control['fresh_witnesses']if x['path']==control['path']);reference_bytes=checked_export_bytes(reference,witness['size'],witness['sha256'])
   else:reference_bytes=pinned_control_bytes(reference)
   require((target/'C44PRN.PRN').read_bytes()==reference_bytes,'PrinterMismatch','full raw resource-matched original control differs')
  checks.append({'attempt':leaf['id'],'native':native,'postprint':post,'full_PRN_control_equal':leaf['mode']=='candidate','preprint_native_prefix_deltas':deltas})
 return {'qualified_attempts':checks,'full_M1_accepted':False,'physical_resources_qualified':False}

def main():
 parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
 for name in ['check','plan']:sub.add_parser(name)
 p=sub.add_parser('run');p.add_argument('--grant-id',required=True);p.add_argument('--attempt',action='append',required=True);p.add_argument('--allow-vm',action='store_true');p.add_argument('--grant',required=True)
 p=sub.add_parser('result');p.add_argument('path');args=parser.parse_args()
 if args.command=='run':return run(args)
 if args.command=='result':print(json.dumps(result(args.path),indent=2));return 0
 value=check();print(json.dumps(value if args.command=='plan'else{'status':'offline checked; no VM','cases':len(value['cases']),'attempts':len(value['attempts']),'plan_sha256':canonical(value)},indent=2));return 0
if __name__=='__main__':sys.exit(main())
