#!/usr/bin/env python3
"""Offline-first four-leaf successor; old eight executions/source stay immutable."""
import argparse
from datetime import datetime,timezone
import importlib.util
import json
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import traceback

HERE=Path(__file__).resolve().parent;BASE=HERE.parent;ROOT=BASE.parents[3];PRIMARY=Path('/home/lynn/projects/wordling');PRIVATE=PRIMARY/'research/cache/reference'
spec=importlib.util.spec_from_file_location('wp46_frozen_edit_adapter',BASE/'oracle.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
Refusal=old.Refusal;require=old.require;sha=old.sha;canonical=old.canonical;dump=old.dump
OLD_PLAN='e5e4f76a37ee4fdd60dc974016722253afbbcc8086557c1e03108cfa94ec0884'
BASELINE=BASE/'runs/wp46-phase01/wp46-empty-edit-candidate-r1/input-normal/screen.txt'

def transition():
 path=HERE/'transition.json';t=json.loads(path.read_text())
 require(type(t['old_accepted_complete'])is int and t['old_accepted_complete']==8 and type(t['new_required_leaves'])is int and t['new_required_leaves']==4 and type(t['cumulative_maximum_including_failures'])is int and t['cumulative_maximum_including_failures']==12 and t['old_plan_sha256']==OLD_PLAN,'TransitionAccounting','accepted old8 + fresh4 = cumulative12, not a cap reset')
 verify_predecessor(t)
 return t,sha(path)

def verify_predecessor(t):
 for name,pin in t['files'].items():
  original=Path(pin['original_path']);archive=ROOT/pin['archive_path']
  require(original.is_file()and archive.is_file()and original.stat().st_size==archive.stat().st_size==pin['size']and sha(original)==sha(archive)==pin['sha256'],'PredecessorIdentity',name+' old accepted input changed')
 for label in ['source','phase01','phase02']:
  seal_name='source-seals.json'if label=='source'else label+'-seals.json';manifest=json.loads((ROOT/t['files'][seal_name]['archive_path']).read_text())['files'];directory=ROOT if label=='source'else Path(t['files'][label+'-report.json']['original_path']).parent
  for name,pin in manifest.items():
   path=directory/name;require(path.is_file()and path.stat().st_size==pin['size']and sha(path)==pin['sha256'],'PredecessorRawIdentity','accepted old '+label+' raw/source seal changed: '+name)
 ledger=json.loads(Path(t['files']['private-ledger.json']['original_path']).read_text());snapshot=json.loads((ROOT/t['files']['phase02-ledger.json']['archive_path']).read_text())
 require(canonical(ledger)==canonical(snapshot)and ledger['plan_sha256']==OLD_PLAN and type(ledger['maximum'])is int and ledger['maximum']==12 and len(ledger['attempts'])==8,'PredecessorAccounting','old private/public8 completion must remain exact')
 allrows=[]
 for phase in ['phase01','phase02']:
  report=json.loads((ROOT/t['files'][phase+'-report.json']['archive_path']).read_text());pre=json.loads((ROOT/t['files'][phase+'-prelaunch.json']['archive_path']).read_text())
  require(report['complete']is True and report['oracle_released']is True and report['guard_released']is True and report['master_unchanged']is True and report['plan_sha256']==canonical(pre['plan'])==OLD_PLAN,'PredecessorCompletion','old actual source/complete/release binding')
  require(len(report['results'])==4 and all(x['outcome']=='complete-observation'and x['case']in ['empty-edit','ascii-edit']and x['normal_DOS']is True and x['guest_stopped']is True for x in report['results']),'PredecessorCompletion','no old empty-print leaf may be reclassified')
  allrows.extend(report['results'])
 require(len({x['id']for x in allrows})==8,'PredecessorIdentity','old eight identities unique')
 for row,entry in zip(allrows,ledger['attempts']):require(entry['id']==row['id']and entry['outcome']=='complete-observation'and entry['result_sha256']==canonical(row),'PredecessorIdentity','old row checksum no longer exact')

def expected_empty_status():
 t=json.loads((HERE/'transition.json').read_text());sealed=ROOT/t['files']['phase01-seals.json']['archive_path'];require(sha(sealed)==t['files']['phase01-seals.json']['sha256'],'BaselineIdentity','pinned historical frame manifest changed');seal=json.loads(sealed.read_text())['files'];pin=seal['wp46-empty-edit-candidate-r1/input-normal/screen.txt']
 require(BASELINE.stat().st_size==pin['size']and sha(BASELINE)==pin['sha256'],'BaselineIdentity','sealed actual old empty normal frame changed')
 lines=BASELINE.read_text().splitlines();require(len(lines)==25 and all(set(x)<=set(' ')for x in lines[:24]),'BaselineIdentity','actual empty reference must have blank24 body rows')
 status=lines[24];suffix='Doc 1 Pg 1 Ln 1" Pos 1"';column=status.find('Doc 1');prefix='C:\\OUT\\C46INPUT'
 require(0<column<=60 and status==prefix.ljust(column)+suffix,'BaselineIdentity','closed normal status/path/gap ruler layout differs from actual source')
 return 'C:\\OUT\\C46PRE'.ljust(column)+suffix

def strict_empty_frame(screen,expected):
 # Real approved helpers are necessary but intentionally insufficient: they
 # recognize a session, not an empty body or absence of arbitrary modals.
 session,_,_,quit_module,_,_=old.helpers();lines=screen.splitlines()
 require(session.main_document(screen)and quit_module.exit_state(screen)=='main','EmptyPrintUnknownState','actual helper does not identify normal document')
 require(len(lines)==25 and all(len(x)<=80 and set(x)<=set(' ')for x in lines[:24])and lines[24]==expected,'EmptyPrintUnknownState','all24 body rows must be empty ASCII spaces and exact source-bound Doc1/name/page/line/gap status; unknown modal/ruler/body/status halts')
 return {'rows':25,'all24_body_rows_empty':True,'status':lines[24],'actual_main_document':True,'actual_exit_state':'main'}

def print_empty(p,session,quit_module):
 expected=expected_empty_status();before=p.capture('strict-empty-before-print');proof=strict_empty_frame(before,expected)
 p.screen_step('shift-f7,s','print-C46PRN-printer-list','Standard Printer')
 p.key('3');p.setting('print-C46PRN-printer-edit');p.key('2');p.capture('print-C46PRN-ports');p.key('8');p.capture('print-C46PRN-other-path')
 p.type('C:\\OUT\\C46PRN.PRN');p.key('ret');p.setting('print-C46PRN-other-accepted');p.key('f7,f7');p.setting('print-C46PRN-menu')
 p.key('1');p.q.wait_for('Doc 1');submitted=p.capture('strict-empty-submit-classifier');strict_empty_frame(submitted,expected)
 # No key after submit until the complete body/status proof above succeeds.
 p.key('shift-f7,4');p.q.wait_for('No print jobs');jobs=p.setting('print-C46PRN-job-status')
 require('Job Number: None'in jobs and 'Additional Jobs Not Shown: 0'in jobs,'PrintQueueIncomplete','actual completed queue required')
 p.key('f7');p.q.wait_for('Doc 1');returned=p.capture('strict-empty-print-return');strict_empty_frame(returned,expected)
 p.check('source-bound full empty frame before/submit/return',proof['all24_body_rows_empty']);p.exports.append(('C46PRN.PRN','C46PRN.PRN'))

def owned_attempt(*args):
 # Explicit adaptation in this owned module instance; no old source/helper
 # file or installed runtime is patched. Frozen old eight used the old callback.
 original=old.print_empty
 try:old.print_empty=print_empty;return old.attempt(*args)
 finally:old.print_empty=original

def sources(base):
 rows=list(base['sources']);paths=[HERE/'adapter.py',HERE/'test_adapter.py',HERE/'mutants.py',HERE/'transition.json',ROOT/'internal/document/evidence/wp44/test_oracle.py',BASELINE,*sorted((HERE/'diagnosis').glob('*')),HERE/'history/cycle1/receipt.json',HERE/'history/cycle1/review/report.md',HERE/'history/cycle1/review/seals.json',HERE/'cycle2-correction.json']
 known={x['path']for x in rows}
 for path in paths:
  rel=str(path.relative_to(ROOT))
  if rel not in known:rows.append({'path':rel,'size':path.stat().st_size,'sha256':sha(path)});known.add(rel)
 return sorted(rows,key=lambda x:x['path'])

def plan():
 t,digest=transition();base=old.check();require(canonical(base)==OLD_PLAN,'HistoricalSourceIdentity','old eight source/producer/plan must remain exactly frozen')
 case=next(x for x in base['cases']if x['id']=='empty-print');attempts=[]
 for mode in ['control','candidate']:
  for repeat in [1,2]:
   ident=f'wp46ev2-empty-print-{mode}-r{repeat}';work=PRIVATE/'runs'/ident
   import guest
   prior=guest.RUNTIME,guest.SOCKET
   try:guest.RUNTIME=PRIVATE/'runtime/wp46ev2';guest.SOCKET=guest.RUNTIME/'qmp.sock';argv=guest.arguments(work/'boot.img',work/'harddisk.img')
   finally:guest.RUNTIME,guest.SOCKET=prior
   attempts.append({'id':ident,'case':'empty-print','mode':mode,'repetition':repeat,'private_work':str(work),'qemu_argv':argv})
 return {'schema':'wordling.wp46.empty-successor-plan/v1','old_accepted_complete':8,'new_required_leaves':4,'cumulative_maximum_including_failures':12,'transition':t,'transition_receipt_sha256':digest,'sources':sources(base),'cases':[case],'attempts':attempts,'master':base['master'],'tools':base['tools'],'manuals':base['manuals'],'preboot_resources':base['preboot_resources'],'profile_id':base['profile_id'],'profile_sha256':base['profile_sha256'],'shared_lock':base['shared_lock'],'socket':str(PRIVATE/'runtime/wp46ev2/qmp.sock'),'ledger':str(PRIVATE/'wp46-empty-v2-attempts.json'),'expected_empty_status':expected_empty_status(),'empty_frame_contract':'actual helpers PLUS exact25lines,24empty ASCII-space rows,source-bound closed C46PRE/Doc1/Pg1/Ln1/Pos1 status before print,after submit BEFORE another key,and after return; any unknown modal/ruler/body/status halts','original_case_expectations':'UNCHANGED frozen empty-print C46PRE/C46FIN/native/PRN/presence/absence/profile expectations; no guessed NoText dismissal','timeout_per_attempt_seconds':900,'full_M1_accepted':False}

def transition_fields(p):return {'transition_receipt_sha256':p['transition_receipt_sha256'],'predecessor_plan_sha256':OLD_PLAN,'predecessor_ledger_sha256':p['transition']['files']['private-ledger.json']['sha256'],'old_accepted_complete':8,'new_required_leaves':4,'cumulative_maximum_including_failures':12}
def check():return plan()
def selected(args,p,g):
 ids=args.attempt;lookup={x['id']:x for x in p['attempts']};require(re.fullmatch(r'wp46ev2-[a-z0-9-]{1,20}',args.grant_id or '')and bool(ids)and len(ids)==len(set(ids))and all(i in lookup for i in ids),'GrantSelection','only new four fresh IDs/subsets')
 require(g.get('authorized')is True and g.get('grant_id')==args.grant_id and g.get('plan_sha256')==canonical(p)and g.get('attempt_ids')==ids and type(g.get('maximum_aggregate_attempts'))is int and g['maximum_aggregate_attempts']==12 and isinstance(g.get('authorization_note'),str)and bool(g['authorization_note']),'GrantMismatch','exact separate root source/plan/IDs/cap/note required')
 ack=g.get('transition_authorization',{});require(ack.get('authorized_by_root')is True and canonical({k:v for k,v in ack.items()if k!='authorized_by_root'})==canonical(transition_fields(p)),'TransitionAuthorization','explicit root acknowledgement of old8 plus new4, no cap reset')
 if 'argv'in g:require(g['argv']==[sys.executable,*sys.argv],'GrantArgv','exact root argv required')
 return [lookup[x]for x in ids]

def empty_ledger(p):return {'schema':'wordling.wp46.empty-successor-ledger/v1','plan_sha256':canonical(p),'transition_receipt_sha256':p['transition_receipt_sha256'],'old_accepted_complete':8,'new_required_leaves':4,'cumulative_maximum_including_failures':12,'halted':False,'attempts':[]}
def validate_ledger(p,ledger):
 require(canonical({k:v for k,v in ledger.items()if k not in ['attempts','halted','failure_code']})==canonical({k:v for k,v in empty_ledger(p).items()if k not in ['attempts','halted','failure_code']}),'LedgerIdentity','source/transition/budget header changed')
 require(type(ledger.get('halted'))is bool and ledger['halted']is False,'PriorFailure','any first predecessor/source/control/guest failure halts this successor plan');prior=ledger.get('attempts');require(isinstance(prior,list)and len(prior)<=4 and 8+len(prior)<=12,'AttemptLimit','old8 count remains spent/accepted')
 ids=[x['id']for x in prior];require(len(ids)==len(set(ids))and all(x in {a['id']for a in p['attempts']}for x in ids),'LedgerIdentity','unknown/old/duplicate new leaf')
 require(all(x['outcome']=='complete-observation'for x in prior),'PriorFailure','first successor failure halts whole plan permanently');return prior

def bind_control(p,leaf,prior):
 if leaf['mode']=='control':return None
 ident=f"wp46ev2-empty-print-control-r{leaf['repetition']}";rows=[x for x in prior if x['id']==ident];require(len(rows)==1 and rows[0]['outcome']=='complete-observation','MissingControl','fresh same-repetition successor control required before boot');entry=rows[0]
 directory=BASE/'runs'/entry['grant_id']/ident;file=directory/'result.json';require(file.is_file()and sha(file)==entry['result_file_sha256'],'ControlResultChanged','control result file changed');row=json.loads(file.read_text());require(canonical(row)==entry['result_sha256']and row['id']==ident and row['case']=='empty-print'and row['mode']=='control'and row['repetition']==leaf['repetition']and row['plan_sha256']==canonical(p),'ControlIdentity','control source/case/repetition differs');old.normal_dos(directory);old.print_value(directory,row)
 for export in row['exports']:
  if export['present']:old.guard.checked_export_bytes(export['path'],export['size'],export['sha256'])
 return {'directory':str(directory),'report':str(file),'result_sha256':entry['result_sha256'],'result_file_sha256':entry['result_file_sha256'],'plan_sha256':canonical(p)}

def run(args):
 # Authority is checked against the locally sealed proposal WITHOUT running the
 # mutable prerequisite/source checks. Only that exact granted proposal may
 # write its own permanent failure record; malformed requests write nothing.
 require(args.allow_vm,'AuthorizationRequired','offline default, no VM grant')
 frozen=json.loads((HERE/'preflight.json').read_text());p=frozen['plan']
 require(frozen['plan_sha256']==canonical(p),'SealedPlanIdentity','local frozen proposal checksum')
 g=json.loads(Path(args.grant).read_text());leaves=selected(args,p,g)
 ledger=Path(p['ledger']);out=BASE/'runs'/args.grant_id
 if ledger.exists():validate_ledger(p,json.loads(ledger.read_text()))
 try:
  actual=check();require(canonical(actual)==canonical(p),'SealedPlanIdentity','current check differs from exact root-granted frozen plan')
  return authorized_run(args,p,g,leaves)
 except Exception as error:
  # No guest is invented for setup faults. Preserve any actual in-flight row.
  aggregate=json.loads(ledger.read_text())if ledger.exists()else empty_ledger(p)
  require(aggregate['plan_sha256']==canonical(p)and aggregate['transition_receipt_sha256']==p['transition_receipt_sha256'],'LedgerIdentity','cannot overwrite another proposal ledger')
  aggregate['halted']=True;aggregate['failure_code']=getattr(error,'code',type(error).__name__)
  failure={'plan_sha256':canonical(p),'grant_id':args.grant_id,'batch_error':str(error),'batch_error_code':aggregate['failure_code'],'halted_before_next_guest':True,'old_accepted_complete':8,'cumulative_spent':8+len(aggregate['attempts']),'recorded_at':datetime.now(timezone.utc).isoformat(),'complete':False,'durable_halt':False,'full_M1_accepted':False}
  try:
   dump(ledger,aggregate)
   require(json.loads(ledger.read_text())==aggregate,'HaltPersistenceFailed','halt readback differs')
  except Exception as write_error:
   raise Refusal('HaltPersistenceFailed','authorized failure could not be durably recorded: '+str(write_error))from error
  failure['durable_halt']=True;out.mkdir(parents=True,exist_ok=True);dump(out/'authorized-prelaunch-failure.json',failure)
  print(json.dumps(failure));return 1

def authorized_run(args,p,g,leaves):
 out=BASE/'runs'/args.grant_id;require(not out.exists(),'PriorEvidence','fresh successor output only');out.mkdir(parents=True)
 for pin in p['sources']:
  src=ROOT/pin['path'];dst=out/'runner-source'/pin['path'];dst=dst.with_name(dst.name+'.txt')if dst.suffix in ['.go','.py']else dst;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 for name,pin in p['transition']['files'].items():dst=out/'predecessor'/name;dst.parent.mkdir(exist_ok=True);shutil.copyfile(ROOT/pin['archive_path'],dst);require(sha(dst)==pin['sha256'],'PredecessorIdentity','preboot archive mismatch')
 case=p['cases'][0];(out/'inputs').mkdir();shutil.copyfile(ROOT/case['candidate'],out/'inputs/empty.WP5');dump(out/'prelaunch.json',{'plan':p,'plan_sha256':canonical(p),'grant':g,'argv':[sys.executable,*sys.argv]})
 session,n,fields,quit_module,layout,genesis=old.helpers();qmp,guest,private=session.configure(PRIMARY,'wp46ev2');report={'plan_sha256':canonical(p),'grant_id':args.grant_id,'old_accepted_complete':8,'selected_attempt_ids':[x['id']for x in leaves],'results':[],'guard_released':False,'oracle_released':False,'full_M1_accepted':False};previous_signal=signal.signal(signal.SIGALRM,session.timeout_signal)
 try:
  with session.exclusive(private):
   try:
    verify_predecessor(p['transition']);require({k:sha(guest.MASTER/k)for k in p['master']}==p['master'],'MasterChanged','before run');ledger=Path(p['ledger']);aggregate=json.loads(ledger.read_text())if ledger.exists()else empty_ledger(p);prior=validate_ledger(p,aggregate)
    require(len(prior)+len(leaves)<=4 and 8+len(prior)+len(leaves)<=12 and not({x['id']for x in prior}&{x['id']for x in leaves}),'AttemptLimit','no retry/overbudget/new historical count')
    for leaf in leaves:
     verify_predecessor(p['transition'])
     for pin in p['sources']:require(sha(ROOT/pin['path'])==pin['sha256'],'SourceDrift',pin['path'])
     require(sha(ROOT/case['candidate'])==case['candidate_sha256'],'CandidateDrift','unchanged generated empty');control=bind_control(p,leaf,prior);target=out/leaf['id'];target.mkdir();work=Path(leaf['private_work']);require(not work.exists()and not qmp.SOCKET.exists(),'ForeignRuntime','fresh disks/no owned socket')
     if control:(target/'control-custody').mkdir();shutil.copyfile(control['report'],target/'control-custody/result.json')
     entry={'id':leaf['id'],'case':'empty-print','mode':leaf['mode'],'repetition':leaf['repetition'],'grant_id':args.grant_id,'outcome':'incomplete','started_at':datetime.now(timezone.utc).isoformat()};prior.append(entry);dump(ledger,aggregate)
     row=owned_attempt(session,qmp,guest,n,case,leaf,target,work);row['plan_sha256']=canonical(p)
     try:
      if row['outcome']=='complete-observation':row['required_output_qualification']=old.qualify(target,case,row,control)
      row['master_after']={k:sha(guest.MASTER/k)for k in p['master']};require(row['master_after']==p['master'],'MasterChanged','after stopped exports');verify_predecessor(p['transition'])
     except Exception as error:row.update(outcome='required-output-or-master-unproven',qualification_error=str(error),qualification_error_code=getattr(error,'code',type(error).__name__))
     entry['outcome']=row['outcome'];entry['result_sha256']=canonical(row);dump(target/'result.json',row);entry['result_file_sha256']=sha(target/'result.json');report['results'].append(row);report['cumulative_spent']=8+len(prior);dump(ledger,aggregate);dump(out/'aggregate-ledger.json',aggregate);dump(out/'run.json',report)
     if row['outcome']!='complete-observation':
      aggregate['halted']=True;aggregate['failure_code']=row.get('qualification_error_code')or row.get('error_code')or row.get('stop_error_code')or row.get('extraction_error_code')or'incomplete';dump(ledger,aggregate);dump(out/'aggregate-ledger.json',aggregate);report['halted_before_next_guest']=True;break
   except Exception as error:
    report.update(batch_error=str(error),batch_error_code=getattr(error,'code',type(error).__name__),halted_before_next_guest=True)
    aggregate=aggregate if'aggregate'in locals()else empty_ledger(p);aggregate['halted']=True;aggregate['failure_code']=report['batch_error_code'];dump(Path(p['ledger']),aggregate);dump(out/'aggregate-ledger.json',aggregate)
   finally:
    try:report['master_after']={k:sha(guest.MASTER/k)for k in p['master']};report['master_unchanged']=report['master_after']==p['master']
    except Exception as error:report['master_error']=str(error)
    dump(out/'run.json',report)
  report['guard_released']=True;report['oracle_released']=bool(report['results'])and all(x['guest_stopped']for x in report['results'])and not qmp.SOCKET.exists()
 finally:
  signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,previous_signal);report['complete']=len(report['results'])==len(leaves)and all(x['outcome']=='complete-observation'for x in report['results'])and report.get('master_unchanged')is True;dump(out/'run.json',report)
 print(json.dumps({'complete':report['complete'],'oracle_released':report['oracle_released'],'new_attempts':len(report['results']),'old_accepted_complete':8,'cumulative_spent':report.get('cumulative_spent',8)}));return 0 if report['complete']else 1

def result(path):
 report=json.loads(Path(path).read_text());pre=json.loads((Path(path).parent/'prelaunch.json').read_text());p=pre['plan'];require(report.get('complete')is True and report.get('oracle_released')is True and report.get('guard_released')is True and report['plan_sha256']==canonical(p),'IncompleteBatch','source-bound complete released batch required');verify_predecessor(p['transition']);aggregate=json.loads((Path(path).parent/'aggregate-ledger.json').read_text());prior=validate_ledger(p,aggregate);checks=[]
 require(report['selected_attempt_ids']==[x['id']for x in report['results']],'AttemptIdentity','exact selected/result sequence')
 for row in report['results']:
  leaf=next(x for x in p['attempts']if x['id']==row['id']);entry=next(x for x in prior if x['id']==row['id']);directory=Path(path).parent/row['id'];require(row['outcome']=='complete-observation'and canonical(row)==entry['result_sha256']and sha(directory/'result.json')==entry['result_file_sha256'],'ResultIdentity','actual leaf/ledger/result custody');old.normal_dos(directory)
  for export in row['exports']:
   if export['present']:old.guard.checked_export_bytes(export['path'],export['size'],export['sha256'])
  require(row['guest_stopped']is True and row['exports_complete']is True and row['normal_DOS']is True and row['master_after']==p['master'],'IncompleteAttempt','required normal stop/exports/master')
  import tempfile
  with tempfile.TemporaryDirectory(prefix='wp46ev2-reedit-')as tmp:
   native=old.product('-verify',directory/'C46PRE.WP5','-require-preprint','-reedit-out',Path(tmp)/'Q.WP5');native['all72_fields']=old.profile_fields(directory/'C46PRE.WP5',native['inspection']);require(native['body_hex']=='','OriginalBodyMismatch','required empty original native')
  control=bind_control(p,leaf,prior)
  if control:
   reference=json.loads(Path(control['report']).read_text());require(old.print_value(directory,row)==old.print_value(Path(control['directory']),reference),'PrintControlMismatch','full raw stream/presence comparison');require((directory/'C46PRE.WP5').read_bytes()==(Path(control['directory'])/'C46PRE.WP5').read_bytes()and(directory/'C46FIN.WP5').read_bytes()==(Path(control['directory'])/'C46FIN.WP5').read_bytes(),'NativeControlMismatch','full native PRE/FIN comparison')
  checks.append({'id':row['id'],'actual_native':native,'full_PRN_control_equal':bool(control)})
 return {'qualified_new_observations':checks,'old_accepted_complete_unchanged':8,'cumulative_spent':8+len(prior),'all12_complete':len(prior)==4,'full_M1_accepted':False}

def main():
 parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
 for name in ['check','plan']:sub.add_parser(name)
 p=sub.add_parser('run');p.add_argument('--allow-vm',action='store_true');p.add_argument('--grant',required=True);p.add_argument('--grant-id',required=True);p.add_argument('--attempt',action='append',required=True);r=sub.add_parser('result');r.add_argument('path');args=parser.parse_args()
 if args.command=='run':return run(args)
 if args.command=='result':print(json.dumps(result(args.path),indent=2));return 0
 print(json.dumps(check(),indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
