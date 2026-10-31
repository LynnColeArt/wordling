#!/usr/bin/env python3
"""WP51 original-operation contract: offline by default, never a native writer."""
import sys
sys.dont_write_bytecode=True
import argparse,ast,hashlib,math,types,importlib,importlib.util,json,os,re,shutil,signal,subprocess,sys,traceback
from datetime import datetime,timezone
from pathlib import Path
import frames,stage1,protocol,recipes,families
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];PRIMARY=Path('/home/lynn/projects/wordling');PRIVATE=PRIMARY/'research/cache/reference'
spec=importlib.util.spec_from_file_location('approved44_owned_stop',ROOT/'internal/document/evidence/wp44/oracle.py');guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
require=frames.require;Refusal=frames.Refusal
SOURCE=ROOT/'internal/document/evidence/wp46/runs/wp46ev3-phase01/wp46ev3-empty-print-control-r1/C46FIN.WP5';H1='d490c635fa653ec9a9817e291220285e0794aec0f6a29f18e447d70ee23e5629';BIN=HERE/'bin/readonly-probe'
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def canonical(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def dump(path,obj):path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2)+'\n')
def probe(paths):
 p=subprocess.run([str(BIN),*map(str,paths)],cwd=ROOT,capture_output=True,timeout=30);require(p.returncode==0,'ReadonlyProbeFailed',p.stderr.decode(errors='replace'));return json.loads(p.stdout)
def closure():
 pending=[ROOT/'scripts/reference'/str(name+'.py')for name in ['macro_session','native_edits','resaved_prefix','macro_quit','text_layout','native_genesis','qmp','guest']];pending.append(ROOT/'internal/document/evidence/wp44/oracle.py');seen={}
 while pending:
  p=pending.pop();name=str(p.relative_to(ROOT))
  if name in seen:continue
  raw=p.read_bytes();approved=subprocess.check_output(['git','show','44aab36accdf14a370a67fd73945907871ab7193:'+name],cwd=ROOT);require(raw==approved,'ApprovedHelperDrift',name);seen[name]={'path':name,'size':len(raw),'sha256':hashlib.sha256(raw).hexdigest()};require(len(seen)<=50,'HelperBudget','bounded transitive helper closure')
  for node in ast.walk(ast.parse(raw)):
   names=[x.name for x in node.names]if isinstance(node,ast.Import)else[node.module]if isinstance(node,ast.ImportFrom)and node.module else[]
   for module in names:
    candidate=ROOT/'scripts/reference'/str(module.split('.')[0]+'.py')
    if candidate.is_file():pending.append(candidate)
 return list(seen.values())
def source_pins():
 rows=closure();paths=[*HERE.glob('*.py'),*sorted((HERE/'probe').glob('*.go')),BIN,HERE/'compiled-source.json',HERE/'approved-source-preflight.json',HERE/'stage1-facts.json',HERE/'caller-and-permission-gap.json',HERE/'frame-atlas.json',ROOT/'docs/research/continuation/native-constructor-design/schema.json',ROOT/'go.mod',ROOT/'go.sum',ROOT/'docs/research/reference-environment/environment.json',ROOT/'docs/research/reference-environment/installed-files.json']
 paths.extend([ROOT/'internal/document/evidence/wp46/runs/wp46ev3-phase01/run.json',ROOT/'internal/document/evidence/wp46/runs/wp46ev3-phase01/wp46ev3-empty-print-control-r1/qmp-wire.jsonl'])
 baseline=json.loads((HERE/'approved-source-preflight.json').read_text())['all_document_Go_byteexact_approved46']
 for name,digest in baseline.items():require(sha(ROOT/name)==digest,'ApprovedDocumentDrift',name);paths.append(ROOT/name)
 paths.extend(ROOT/x['path']for x in json.loads((HERE/'stage1-facts.json').read_text())['images'])
 paths.append(stage1.PROV/'path-map.json');paths.extend(stage1.PROV/p['archive_relative_path']for p in json.loads((stage1.PROV/'path-map.json').read_text())['files'])
 for pin in frames.atlas()['templates'].values():
  paths.append(ROOT/pin['path']);cursor=(ROOT/pin['path']).with_name('cursor.json')
  if cursor.is_file():paths.append(cursor)
 for pin in frames.atlas()['position_witnesses'].values():paths.append(ROOT/pin['cursor_path'])
 compiled=json.loads((HERE/'compiled-source.json').read_text());require(compiled['binary']['sha256']==sha(BIN),'CompiledBinaryDrift','actual read-only probe build witness');
 for package in compiled['packages']:
  for pin in package['files']:
   require(sha(ROOT/pin['path'])==pin['sha256'],'CompiledSourceDrift',pin['path']);paths.append(ROOT/pin['path'])
 known={x['path']for x in rows}
 for path in paths:
  name=str(path.relative_to(ROOT))
  if name not in known:rows.append({'path':name,'size':path.stat().st_size,'sha256':sha(path)});known.add(name)
 return sorted(rows,key=lambda x:x['path'])
def plan():
 require(SOURCE.stat().st_size==324 and sha(SOURCE)==H1,'InitialH1Identity','exact accepted ORIGINAL H1 FIN, no PRE/constructor/candidate')
 source=probe([SOURCE])[0];require(families.classify(source,'')['family']=='H1-R-e72402','InitialH1Family','all72/nativegraph/currentreadonlyrefusal')
 profile_path=ROOT/'docs/research/reference-environment/environment.json';profile=json.loads(profile_path.read_text());masters={name:sha(PRIVATE/'master'/name)for name in ['boot.img','harddisk.img']};require(masters=={'boot.img':profile['master_boot_sha256'],'harddisk.img':profile['master_disk_sha256']},'MasterDrift','private master metadata only')
 tools=[{'name':'python-interpreter','path':sys.executable,'sha256':sha(Path(sys.executable)),'version':sys.version}]
 for name in ['qemu-system-i386','mcopy','mdir','mtype','mformat']:
  p=Path(shutil.which(name)or'/missing');require(p.is_file(),'ToolMissing',name);tools.append({'name':name,'path':str(p),'sha256':sha(p)})
 firmware=[]
 for pin in profile['firmware']:
  file=Path(pin['path']);require(sha(file)==pin['sha256'],'FirmwareDrift',str(file));firmware.append({'path':str(file),'size':file.stat().st_size,'sha256':pin['sha256'],'publication':'private environment metadata only'})
 require(next(x['sha256']for x in tools if x['name']=='qemu-system-i386')==profile['qemu_binary']['sha256'],'QEMUBinaryDrift','exact selected profile executable')
 installed=json.loads((ROOT/'docs/research/reference-environment/installed-files.json').read_text())['files'];resources=[]
 for name in ['WP.EXE','WP.FIL','WP.DRS','STANPRIN.PRS','WP{WP}.SET']:
  path='WP51/'+name;raw=subprocess.check_output(['mtype','-i',str(PRIVATE/'master/harddisk.img')+'@@1048576','::'+path],timeout=15);pin=next(x for x in installed if x['path']==path);require(len(raw)==pin['size']and hashlib.sha256(raw).hexdigest()==pin['sha256'],'ResourceDrift',path);resources.append({'path':path,'size':len(raw),'sha256':pin['sha256'],'publication':'private resource metadata only'})
 import guest
 runtime=PRIVATE/'runtime/wp51h1';leaves=recipes.leaves(PRIVATE);before=guest.RUNTIME,guest.SOCKET
 try:
  guest.RUNTIME,guest.SOCKET=runtime,runtime/'qmp.sock'
  for leaf in leaves:work=Path(leaf['private_work']);leaf['qemu_argv']=guest.arguments(work/'boot.img',work/'harddisk.img')
 finally:guest.RUNTIME,guest.SOCKET=before
 return {'schema':'wordling.wp51.original-H1-contract/v1','sources':source_pins(),'initial_source':{'path':str(SOURCE.relative_to(ROOT)),'size':324,'sha256':H1},'classes':[recipes.operation_plan(j)for j in range(4)],'attempts':leaves,'maximum_new_attempts_including_failures':8,'historical46_spent_unchanged':13,'historical46_accepted12_incomplete1':True,'ledger':str(PRIVATE/'wp51-h1-contract-attempts.json'),'socket':str(runtime/'qmp.sock'),'shared_lock':str(PRIVATE/'session1.lock'),'master':masters,'tools':tools,'firmware':firmware,'resources':resources,'profile_sha256':sha(profile_path),'profile_id':profile['profile_id'],'binary_sha256':sha(BIN),'prospective_family_vectors':families.VECTORS_as_json(),'authoritative_decision_table_sha256':sha(stage1.PROV/'N2-revision2/decision-table.json'),'limits':{'timeout_seconds_per_leaf':900,'captures_per_leaf':240,'native_or_PRN_bytes':65536,'leaves':8,'input_assets':1,'total_owned_source_pins':500},'vm_authorized':False,'native_mutation_permission':False,'full_M1_accepted':False}
def check():
 p=plan();require(len(p['sources'])<=500,'SourceBudget','source closure must remain bounded');return p
def selected(args,p,g):
 ids=[x['id']for x in p['attempts']];require(args.attempt==ids,'GrantSelection','single exact ordered eight only; no subset/resume/retry')
 require(re.fullmatch(r'wp51-[a-z0-9-]{1,20}',args.grant_id or'')and g.get('authorized')is True and g.get('grant_id')==args.grant_id and g.get('plan_sha256')==canonical(p)and g.get('attempt_ids')==ids and type(g.get('maximum_new_attempts_including_failures'))is int and g['maximum_new_attempts_including_failures']==8 and isinstance(g.get('authorization_note'),str)and bool(g['authorization_note']),'GrantMismatch','separate root exact source/plan/IDs/8 counted controls required')
 require(g.get('historical46_spent_unchanged')==13 and type(g['historical46_spent_unchanged'])is int,'HistoryAccounting','old46 count13 remains immutable, no reset')
 if 'argv'in g:require(g['argv']==[sys.executable,*sys.argv],'GrantArgv','exact root invocation')
 return p['attempts']
def empty_ledger(p):return {'schema':'wordling.wp51.control-attempts/v1','plan_sha256':canonical(p),'historical46_spent':13,'maximum_new_attempts_including_failures':8,'halted':False,'attempts':[]}
def ledger_check(p,l):
 require(canonical({k:v for k,v in l.items()if k not in ['attempts','halted','failure_code']})==canonical({k:v for k,v in empty_ledger(p).items()if k not in ['attempts','halted','failure_code']}),'LedgerIdentity','frozen source/history/cap8 header')
 require(type(l['halted'])is bool and not l['halted'],'PriorFailure','first failure permanently halts this plan');require(isinstance(l['attempts'],list)and len(l['attempts'])<=8 and all(x['outcome']=='complete-observation'for x in l['attempts']),'PriorFailure','no in-flight/incomplete/reset/resume')
def export(work,target,name,host):
 path=target/host;require(not path.exists(),'StaleExport','fresh native/PRN export only');p=subprocess.run(['mcopy','-i',str(work/'harddisk.img')+'@@1048576','::OUT/'+name,str(path)],capture_output=True,timeout=15);require(p.returncode==0 and path.is_file()and 0<path.stat().st_size<=65536,'RequiredExportMissing',name);return {'name':name,'path':str(path),'size':path.stat().st_size,'sha256':sha(path),'exit':p.returncode}
def attempt(session,qmp,guest,n,leaf,target,work,p):
 row={'id':leaf['id'],'case':leaf['case'],'repetition':leaf['repetition'],'outcome':'incomplete','normal_DOS':False,'guest_stopped':False};identity=None;core=None
 try:
  session.QMP_AUDIT_FILE=target/'qmp-wire.jsonl';signal.setitimer(signal.ITIMER_REAL,900);argv=session.fresh_start(qmp,guest,work,[('H1INPUT',SOURCE)]);row['qemu_argv']=argv;require(argv==leaf['qemu_argv'],'LaunchArgv','exact frozen argv');identity=guard.owned_identity(qmp,work,argv);row['owned_start_identity']=identity
  with qmp.QMP()as q:core=n.MutationProbe(q,target);ui=protocol.Protocol(core);row['observations']=ui.perform(leaf['class_index']);last=ui.receipts[-1];require(last['expected']['kind']=='dos','NormalDOSMissing','final captured state must be actualDOS');frames.check((target/last['capture']/'screen.txt').read_text(),{'kind':'dos'});row['normal_DOS']=True
 except Exception as error:row.update(error=str(error),error_code=getattr(error,'code',type(error).__name__),traceback=traceback.format_exc())
 finally:
  signal.setitimer(signal.ITIMER_REAL,0)
  if identity is None and qmp.SOCKET.exists():
   try:identity=guard.owned_identity(qmp,work,leaf['qemu_argv']);row['owned_start_identity']=identity;row['launch_identity_recovered_from_actual_positive_PID']=True
   except Exception as error:row['identity_error']=str(error)
  if identity is not None:
   try:
    guard.validate_stop_identity(qmp,identity);guard.same_identity(identity);row['stop_method']=session.stop_owned(qmp,guest);require(row['stop_method']=='QMP quit; own socket terminated','HostContained','normal QMP method required');row['stop_observations']=[];row['stop_proof']=guard.stopped(qmp,identity,observations=row['stop_observations']);row['guest_stopped']=True;wire=target/'qmp-wire.jsonl';require(wire.is_file(),'WireMissing','complete prelaunch through quit QMP custody required');row['stop_wire']={'path':str(wire),'size':wire.stat().st_size,'sha256':sha(wire)}
   except Exception as error:row.update(stop_error=str(error),stop_error_code=getattr(error,'code',type(error).__name__))
  else:row['stop_error']='no positive owned PID/startticks/argv/disks; no invented termination or extraction'
  if row['guest_stopped']and row['normal_DOS']and'error'not in row and'stop_error'not in row:
   try:
    require({host for name,host in core.exports}=={'H51S0.WP5','H51S1.WP5','H51FIN.WP5','H51PRN.PRN'},'ExportRoster','all three native checkpoints and fullPRN required');row['exports']=[]
    for name,host in core.exports:row['exports'].append(export(work,target,name,host))
    row['input_after']=export(work,target,'H1INPUT','input-after.WP5');require(row['input_after']['sha256']==H1 and row['input_after']['size']==324,'InputChanged','original source file untouched');row['settings_after']=session.settings_snapshot(work,'after');row['exports_complete']=True;row['outcome']='complete-observation'
   except Exception as error:row.update(extraction_error=str(error),extraction_error_code=getattr(error,'code',type(error).__name__))
  else:row['extraction_skipped']='failed/unknown private HD untouched; accepted normalDOS +positive stopped proof required'
  if core is not None:row['trace']=core.trace
 return row

def verify_stop(target,row,leaf,p):
 identity=row.get('owned_start_identity');guard.validate_stop_identity(types.SimpleNamespace(SOCKET=Path(p['socket'])),identity);require(row.get('qemu_argv')==leaf['qemu_argv']and identity['argv'][1:]==leaf['qemu_argv'][1:],'StopLaunchIdentity','actual owned argv must bind frozen launch');require(identity['private_disks']==[str(Path(leaf['private_work'])/name)for name in ['boot.img','harddisk.img']],'StopDiskIdentity','exact both frozen private disks');require(identity['executable']==str(Path(next(x['path']for x in p['tools']if x['name']=='qemu-system-i386')).resolve()),'StopBinaryIdentity','actual owned executable path')
 proof=row.get('stop_proof');observations=row.get('stop_observations');require(row.get('stop_method')=='QMP quit; own socket terminated'and isinstance(proof,dict)and proof.get('pid')==identity['pid']and proof.get('startticks')==identity['startticks']and proof.get('gone_or_same_zombie')is True and proof.get('socket_absent')is True and isinstance(observations,list)and 0<len(observations)<=102 and proof.get('observations')==observations,'StopWitnessMissing','actual bounded identity observation witness required; no passedboolean substitute')
 for obs in observations:
  require(obs.get('pid')==identity['pid']and obs.get('classification')in ['live','resample','gone','zombie']and type(obs.get('socket_present'))is bool,'StopWitnessInvalid','unknown/foreign/reused identity forbidden')
  require(all(type(obs.get(k))in [int,float]and math.isfinite(obs[k])for k in ['monotonic','deadline_monotonic','observation_complete_monotonic']),'StopClockInvalid','actual finite monotonic observations')
 times=[x['monotonic']for x in observations];deadline=observations[0]['deadline_monotonic'];require(0<deadline-times[0]<=5.0 and times==sorted(times)and all(x['deadline_monotonic']==deadline and x['monotonic']<=x['observation_complete_monotonic']for x in observations),'StopClockInvalid','fixed bounded monotonic deadline, no guessed grace')
 last=observations[-1];require(last['classification']in ['gone','zombie']and last['socket_present']is False and last['observation_complete_monotonic']<=last['deadline_monotonic'],'StopTerminalMissing','bounded actual socket absence and owned terminal state');require((last['classification']=='gone'and last.get('pid_present')is False)or(last['classification']=='zombie'and last.get('state')=='Z'and last.get('startticks')==identity['startticks']),'StopTerminalMissing','positive actual absence or same owned zombie')
 wire=row.get('stop_wire',{});require(wire.get('path')==str(target/'qmp-wire.jsonl'),'WireIdentity','exact raw owned wire file');raw=guard.checked_export_bytes(wire['path'],wire['size'],wire['sha256']);messages=[]
 for line in raw.splitlines():
  event=json.loads(line);message=json.loads(bytes.fromhex(event['raw_hex']));messages.append((event['direction'],message))
 require(any(direction=='tx-buffer'and message.get('execute')=='quit'for direction,message in messages)and any(direction=='rx'and message.get('event')=='SHUTDOWN'and message.get('data',{}).get('reason')=='host-qmp-quit'for direction,message in messages),'NormalQMPMissing','actual wire quit and QMP shutdown evidence, no containment')
 return {'actual_wire_quit':True,'bounded_terminal_observations':len(observations),'owned_identity_bound':True}

def verify_observations(target,row,leaf):
 observation=row['observations'];require(observation['recipe']==recipes.operation_plan(leaf['class_index'])and observation['initial_source_sha256']==H1,'OperationSourceMismatch','frozen source and exact logical operation roster');receipts=observation['receipts'];require(isinstance(receipts,list)and 0<len(receipts)<=240,'MissingFrames','all captured source-state receipts required')
 modes=[x['mode_observed']for x in receipts if 'mode_observed'in x];require(len(modes)==3 and all(type(x)is bool for x in modes)and modes[0]is False,'ModeRoster','initial plus clear/reload exact modes required');expected=protocol.preview(leaf['class_index'],modes[1],modes[2]);projection=lambda xs:[{k:v for k,v in x.items()if k in ['capture','expected','mode_observed']}for x in xs];require(projection(receipts)==projection(expected['receipts']),'OperationTraceMismatch','complete frozen original key/state trace required, not asserted recipe only')
 for receipt in receipts:
  label=receipt['capture'];require(re.fullmatch('[0-9]{3}-[A-Za-z0-9-]{1,96}',label),'CaptureIdentity','owned capture label only');directory=target/label;require((directory/'screen.txt').is_file(),'MissingFrames',label);cursor=json.loads((directory/'cursor.json').read_text())if(directory/'cursor.json').exists()else None;frames.check((directory/'screen.txt').read_text(),receipt['expected'],cursor)
 require(receipts[-1]['expected']['kind']=='dos','NormalDOSMissing','last complete frame must be actualDOS, not reportboolean');require(any(x['expected'].get('name')=='H1INPUT'and x['expected']['kind']=='normal'and x['expected']['body']==''for x in receipts),'MissingInitialSourceFrame','initial H1 acquisition must be explicit');require(any(x['expected'].get('name')=='H51S0'and x['expected']['kind']=='reveal'and x['expected']['body']==recipes.EXPECTED[leaf['class_index']][0]for x in receipts),'MissingReloadFrame','actual saved/reloaded source capture before nextASCII')
 return {'raw_frames_rechecked':len(receipts),'reported_pass_booleans_not_authority':True}

def prior_control(p,prior):
 ledger=json.loads(Path(p['ledger']).read_text());entry=next((x for x in ledger['attempts']if x['id']==prior['id']),None);result=Path(prior['directory'])/'result.json';require(ledger['plan_sha256']==canonical(p)and entry is not None and entry['outcome']=='complete-observation'and entry['result_sha256']==canonical(prior)and result.is_file()and sha(result)==entry['result_file_sha256']and canonical(json.loads(result.read_text()))==canonical(prior),'PriorControlIdentity','immutable prior result/ledger/source identity required')
 for pin in prior['exports']:guard.checked_export_bytes(pin['path'],pin['size'],pin['sha256'])
 return True

def qualify(target,row,leaf,p,previous):
 expected_exports={'H51S0':'H51S0.WP5','H51S1':'H51S1.WP5','H51FIN':'H51FIN.WP5','H51PRN.PRN':'H51PRN.PRN'};exports=row.get('exports');require(isinstance(exports,list)and len(exports)==4 and {x.get('name')for x in exports}==set(expected_exports)and all(x.get('path')==str(target/expected_exports[x['name']])for x in exports),'ExportRoster','complete uniquely named native/PRN custody, no reported pass substitute');source=row.get('input_after',{});require(source.get('path')==str(target/'input-after.WP5')and source.get('name')=='H1INPUT'and source.get('size')==324 and source.get('sha256')==H1,'InputCustody','actual untouched H1 input export');guard.checked_export_bytes(source['path'],324,H1)
 stop_proof=verify_stop(target,row,leaf,p);observation_proof=verify_observations(target,row,leaf)
 for pin in row['exports']:guard.checked_export_bytes(pin['path'],pin['size'],pin['sha256'])
 native=probe([target/name for name in ['H51S0.WP5','H51S1.WP5','H51FIN.WP5']]);q=families.qualify(native,recipes.operation_plan(leaf['class_index']),leaf['repetition']);q['raw_observation_proof']=observation_proof;q['raw_stop_proof']=stop_proof;require(row['normal_DOS']is True and row['guest_stopped']is True and row['exports_complete']is True,'IncompleteProof','normalDOS/stopped/complete exports')
 # Full raw observation equality, not normalizing printer/native or key effects.
 for prior in previous:
  prior_control(p,prior)
  require(prior['qualification']['prospective_branch']==q['prospective_branch'],'MixedBranches','no mixed family branch across8')
  if prior['case']==row['case']:
   directory=Path(prior['directory'])
   for name in ['H51S0.WP5','H51S1.WP5','H51FIN.WP5','H51PRN.PRN']:require((directory/name).read_bytes()==(target/name).read_bytes(),'InconsistentRepetition','whole native/PRN same-case controls required')
 return q

def run(args):
 require(args.allow_vm,'AuthorizationRequired','no root grant, offline default');p=json.loads((HERE/'preflight.json').read_text())['plan'];g=json.loads(Path(args.grant).read_text());leaves=selected(args,p,g);ledger=Path(p['ledger']);out=HERE/'runs'/args.grant_id
 if ledger.exists():ledger_check(p,json.loads(ledger.read_text()));require(not json.loads(ledger.read_text())['attempts'],'NoResume','one fresh exact eight-batch only')
 aggregate=empty_ledger(p);guard_acquired=False;report={'plan_sha256':canonical(p),'grant_id':args.grant_id,'results':[],'complete':False,'guard_released':False,'oracle_released':False,'full_M1_accepted':False}
 try:
  require(canonical(check())==canonical(p),'PlanSourceDrift','current transitive checks differ from root frozen plan');require(not out.exists(),'PriorEvidence','fresh public run directory');out.mkdir(parents=True)
  for pin in p['sources']:
   source=ROOT/pin['path'];dest=out/'runner-source'/pin['path'];dest=dest.with_name(dest.name+'.txt')if dest.suffix in ['.go','.py']else dest;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
  dump(out/'prelaunch.json',{'plan':p,'grant':g,'argv':[sys.executable,*sys.argv]});session=importlib.import_module('macro_session');n=importlib.import_module('native_edits');qmp,guest,private=session.configure(PRIMARY,'wp51h1');previous_signal=signal.signal(signal.SIGALRM,session.timeout_signal)
  try:
   with session.exclusive(private):
    guard_acquired=True
    for leaf in leaves:
     for prior in report['results']:prior_control(p,prior)
     for tool in [*p.get('tools',[]),*p.get('firmware',[])]:require(sha(tool['path'])==tool['sha256'],'ToolDrift',tool['path'])
     for pin in p['sources']:require(sha(ROOT/pin['path'])==pin['sha256'],'SourceDrift',pin['path'])
     require({name:sha(guest.MASTER/name)for name in p['master']}==p['master'],'MasterDrift','before leaf');work=Path(leaf['private_work']);require(not work.exists()and not qmp.SOCKET.exists(),'ForeignRuntime','no reused/foreign private work/socket');target=out/leaf['id'];target.mkdir();entry={'id':leaf['id'],'outcome':'incomplete','started_UTC':datetime.now(timezone.utc).isoformat()};aggregate['attempts'].append(entry);dump(ledger,aggregate)
     row=attempt(session,qmp,guest,n,leaf,target,work,p);row['plan_sha256']=canonical(p);row['directory']=str(target)
     try:
      row['master_after']={name:sha(guest.MASTER/name)for name in p['master']};require(row['master_after']==p['master'],'MasterDrift','after every stopped/incomplete attempt before qualification')
      require(row['outcome']=='complete-observation','IncompleteLeaf',row.get('error')or row.get('stop_error')or row.get('extraction_error')or'incomplete');row['qualification']=qualify(target,row,leaf,p,report['results'])
      for pin in p['sources']:require(sha(ROOT/pin['path'])==pin['sha256'],'SourceDrift',pin['path'])
      require({name:sha(guest.MASTER/name)for name in p['master']}==p['master'],'MasterDrift','after stopped accepted qualification')
      for tool in [*p.get('tools',[]),*p.get('firmware',[])]:require(sha(tool['path'])==tool['sha256'],'ToolDrift',tool['path'])
     except Exception as error:row.update(outcome='incomplete',qualification_error=str(error),qualification_error_code=getattr(error,'code',type(error).__name__))
     dump(target/'result.json',row);entry.update(outcome=row['outcome'],result_sha256=canonical(row),result_file_sha256=sha(target/'result.json'));report['results'].append(row);dump(out/'run.json',report);dump(ledger,aggregate)
     if row['outcome']!='complete-observation':raise Refusal(row.get('qualification_error_code','IncompleteLeaf'),'first failing leaf halts WHOLE plan, no next guest')
    report['decision']=families.decision(report['results']);report['complete']=True
   report['guard_released']=True;report['oracle_released']=all(row['guest_stopped']for row in report['results'])and not qmp.SOCKET.exists()
  finally:signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,previous_signal)
 except Exception as error:
  report['complete']=False;aggregate['halted']=True;aggregate['failure_code']=getattr(error,'code',type(error).__name__);report.update(error=str(error),error_code=aggregate['failure_code'],halted_before_next_guest=True,new_attempts_spent=len(aggregate['attempts']))
  out.mkdir(parents=True,exist_ok=True);report['halt_durable']=False
  try:dump(ledger,aggregate);require(json.loads(ledger.read_text())==aggregate,'HaltPersistenceFailed','halt readback');report['halt_durable']=True
  except Exception as write:
   report['halt_write_error']=str(write);raise Refusal('HaltPersistenceFailed','cannot claim durable halt: '+str(write))from error
  # exclusive context has unwound; only release proven by stopped rows/socket.
  if 'qmp'in locals():report['guard_released']=guard_acquired;report['oracle_released']=bool(report['results'])and all(row['guest_stopped']for row in report['results'])and not qmp.SOCKET.exists()
 finally:
  if out.exists():dump(out/'aggregate-ledger.json',aggregate);dump(out/'run.json',report)
 print(json.dumps({'complete':report['complete'],'new_attempts':len(aggregate['attempts']),'halted':aggregate['halted'],'oracle_released':report['oracle_released'],'error_code':report.get('error_code')}));return 0 if report['complete']else 1

def result(directory):
 directory=Path(directory).resolve();launch=json.loads((directory/'prelaunch.json').read_text());p=launch['plan'];ledger=json.loads((directory/'aggregate-ledger.json').read_text());report=json.loads((directory/'run.json').read_text());require(ledger['plan_sha256']==canonical(p)and report['plan_sha256']==canonical(p),'ResultPlanIdentity','frozen plan and result identity');require(report['complete']is True and ledger['halted']is False and len(report['results'])==8 and len(ledger['attempts'])==8,'IncompleteResult','not all eight complete; no qualification or B permission')
 for pin in p['sources']:require(sha(ROOT/pin['path'])==pin['sha256'],'ReplaySourceDrift',pin['path'])
 previous=[]
 for leaf,entry,row in zip(p['attempts'],ledger['attempts'],report['results']):
  target=directory/leaf['id'];require(row['directory']==str(target)and row['id']==leaf['id']==entry['id']and row['case']==leaf['case']and row['repetition']==leaf['repetition']and entry['outcome']==row['outcome']=='complete-observation'and canonical(row)==entry['result_sha256']and sha(target/'result.json')==entry['result_file_sha256']and canonical(json.loads((target/'result.json').read_text()))==canonical(row),'ResultIdentity','exact original leaf/case/repetition/raw result required');require(row['master_after']==p['master'],'MasterDrift','accepted stopped reconciliation')
  for pin in row['exports']:require(Path(pin['path']).resolve().parent==target,'ExportIdentity','exact owned export path');guard.checked_export_bytes(pin['path'],pin['size'],pin['sha256'])
  q=qualify(target,row,leaf,p,[]) # no live oracle ledger accessed during read-only replay
  require(q==row['qualification'],'QualificationMismatch','recomputed actual native/frames');
  for prior in previous:
   require(prior['qualification']['prospective_branch']==q['prospective_branch'],'MixedBranches','all8 uniform')
   if prior['case']==row['case']:
    for name in ['H51S0.WP5','H51S1.WP5','H51FIN.WP5','H51PRN.PRN']:require((Path(prior['directory'])/name).read_bytes()==(target/name).read_bytes(),'InconsistentRepetition','whole native/PRN exact')
  previous.append(row)
 return {'complete_observations':8,'decision':families.decision(previous),'read_only_replay':True,'native_permission':False,'full_M1_accepted':False}

def main():
 parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command');sub.add_parser('check');sub.add_parser('plan');r=sub.add_parser('result');r.add_argument('directory');p=sub.add_parser('run');p.add_argument('--allow-vm',action='store_true');p.add_argument('--grant',required=True);p.add_argument('--grant-id',required=True);p.add_argument('--attempt',action='append',required=True);args=parser.parse_args()
 if args.command=='run':return run(args)
 if args.command=='result':print(json.dumps(result(args.directory),indent=2));return 0
 print(json.dumps(check(),indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
