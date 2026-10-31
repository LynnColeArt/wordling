#!/usr/bin/env python3
"""Offline-first four-attempt proposal for one exact live WP48 native class.
No VM action without a separate exact root grant. No native producer/VM engine.
"""
import argparse
from datetime import datetime,timezone
import fcntl,hashlib,importlib.util,json,os,re,shutil,signal,subprocess,sys,traceback
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];PRIMARY=Path('/home/lynn/projects/wordling');PRIVATE=PRIMARY/'research/cache/reference'
sys.path.insert(0,str(ROOT/'scripts/reference'))
spec=importlib.util.spec_from_file_location('approved_wp46_readonly_adapter',ROOT/'internal/document/evidence/wp46/oracle.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
setup_spec=importlib.util.spec_from_file_location('wp48_owned_setup',HERE/'setup_owner.py');setup=importlib.util.module_from_spec(setup_spec);setup_spec.loader.exec_module(setup)
require=old.require;Refusal=old.Refusal;sha=old.sha;canonical=old.canonical
CANDIDATE='docs/research/continuation/new-session/pty-final/reopen-ascii-edit/files/FIRST'
CANDIDATE_SHA='671fa815e2878bfcfc5ddc902e117645432e920e269cfdcae745e8d9a9407807'
PRODUCER='df4714c480836ab19445031b4361d4a07a89bc2826764940dfb29c76bfd5609b'
TEXT='G43ASCIIZ';TAG='wp48z';GRANT_ID='wp48z-01'
NAMES=['C48INPUT','C48SEED','C48PRE','C48FIN','C48PRN.PRN']
BASE=ROOT/'internal/document/evidence/wp46/runs/wp46-phase02/wp46-ascii-edit-candidate-r1'
PRINT_REFERENCE=BASE/'C46PRN.PRN'
RETRIEVE_PROMPT=ROOT/'docs/research/continuation/session1/runs/2026-10-31-session1-b00-r2/CMD51-065/retrieve-f1-prompt/screen.txt'
RETRIEVE_DRAFT=ROOT/'docs/research/continuation/session1/runs/2026-10-31-session1-b00-r2/CMD51-065/retrieve-f1-draft/screen.txt'
MENU_PINS={k:BASE/v/'screen.txt'for k,v in {'list':'settings-print-C46PRN-printer-list','edit':'settings-print-C46PRN-printer-edit','ports':'print-C46PRN-ports','path':'print-C46PRN-other-path','accepted':'settings-print-C46PRN-other-accepted','menu':'settings-print-C46PRN-menu','submit':'print-C46PRN-submitted'}.items()}
FRAME_PINS={'normal9':BASE/'after-declared-text/screen.txt','reveal8':BASE/'input-Reveal-gap0/screen.txt','saved9':BASE/'C46PRE-saved/screen.txt','normal_cursor9':BASE/'after-declared-text/cursor.json','reveal_cursor0':BASE/'input-Reveal-gap0/cursor.json'}
def now():return datetime.now(timezone.utc).isoformat()
def dump(path,value):
 """Atomic fsynced own-namespace write with strict readback; no old evidence edits."""
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_name(path.name+'.tmp-'+str(os.getpid()));data=(json.dumps(value,indent=2,sort_keys=True)+'\n').encode()
 with tmp.open('xb')as f:f.write(data);f.flush();os.fsync(f.fileno())
 os.replace(tmp,path)
 fd=os.open(path.parent,os.O_DIRECTORY);os.fsync(fd);os.close(fd)
 require(path.read_bytes()==data,'PersistenceFailed',str(path))
def pin(path):path=Path(path);return {'path':str(path.relative_to(ROOT)),'size':path.stat().st_size,'sha256':sha(path)}
def ids():return [f'wp48z-{mode}-r{repeat}'for mode in ['control','candidate']for repeat in [1,2]]
def frozen_argv(work):
 import guest
 previous=guest.RUNTIME,guest.SOCKET
 try:guest.RUNTIME=PRIVATE/'runtime'/TAG;guest.SOCKET=guest.RUNTIME/'qmp.sock';return guest.arguments(work/'boot.img',work/'harddisk.img')
 finally:guest.RUNTIME,guest.SOCKET=previous

def screen_rows(screen):
 # VT row delimiter is LF only; Python splitlines also splits literal ruler RS.
 return screen[:-1].split('\n')if screen.endswith('\n')else screen.split('\n')

def expected_frame(name,text=TEXT,pos='1',reveal=False,question=None):
 """Prospective closed frame; only literal recorded substitutions, no observation claim."""
 normal=screen_rows(FRAME_PINS['normal9'].read_text());reveal8=screen_rows(FRAME_PINS['reveal8'].read_text());column=normal[-1].index('Doc 1')
 require(len(normal)==len(reveal8)==25 and normal[0]==TEXT and reveal8[0]==reveal8[13]=='G43ASCII','FrameBaseline','exact9 normal/8 Reveal baselines')
 status=('C:\\OUT\\'+name if name else '').ljust(column)+f'Doc 1 Pg 1 Ln 1" Pos {pos}"'
 lines=['']*25;lines[0]=text
 if reveal:
  require(question is None and pos=='1','FrameContract','only prospective gap0 Reveal');lines[11]=status;lines[12]=reveal8[12];lines[13]=text;lines[24]=reveal8[24]
 else:lines[24]=question if question is not None else status
 return '\n'.join(lines)+'\n'
def strict_frame(screen,name,text=TEXT,pos='1',reveal=False,question=None):
 session,_,_,quit_module,_,_=old.helpers();lines=screen_rows(screen);expected=screen_rows(expected_frame(name,text,pos,reveal,question))
 actual_main=session.main_document(screen);actual_exit=quit_module.exit_state(screen)
 if not reveal and question is None:require(actual_main and actual_exit=='main','UnknownFrame','actual unchanged main/exit helper rejects frame')
 require(lines==expected and len(lines)==25,'UnknownFrame','complete25-row body/ruler/name/Doc1/page/line/position differs; no next key')
 return {'rows':25,'exact_full_frame':True,'actual_main_document':actual_main,'actual_exit_state':actual_exit,'prospective_Reveal9_not_prior_observation':reveal,'expected_name':name,'expected_body':text,'expected_pos':pos}
def assert_frame(p,label,name,text=TEXT,pos='1',reveal=False):
 screen=p.capture(label);proof=strict_frame(screen,name,text,pos,reveal)
 cursor=json.loads((p.out/label/'cursor.json').read_text());want=0 if pos=='1'else 9
 require(cursor['row']==0 and cursor['column']==want,'CursorFrameMismatch','actual hardware cursor differs from declared ASCII frame; no semantic gap inferred from cursor alone')
 p.trace.append({'strict_full_frame':label,'proof':proof,'hardware_row':cursor['row'],'hardware_column':cursor['column']});return proof

def perform(p,mode):
 session,n,fields,quit_module,layout,genesis=old.helpers();n.settings(p);fast=fields.capture_fast_save(p,'disabled')
 assert_frame(p,'closed-startup-main','',text='')
 if mode=='control':
  p.type(TEXT);assert_frame(p,'control-nine-before-first-save','',pos='1.9');session.save_complete(p,'C48SEED',fields.save_named)
  assert_frame(p,'control-first-save-confirmed','C48SEED',pos='1.9');clear=genesis.clear_for_retrieve(p)
  assert_frame(p,'closed-clear-main','',text='');p.retrieve('C:\\OUT\\C48SEED','control-exact-retrieve');name='C48SEED'
 else:
  clear=[];p.retrieve('C:\\OUT\\C48INPUT','actual-ui333-exact-retrieve');name='C48INPUT'
 assert_frame(p,'input-closed-normal',name);p.key('alt-f3');p.q.wait_for('Reveal Codes to restore');assert_frame(p,'input-prospective-nine-Reveal',name,reveal=True)
 # No key follows an unknown Reveal, modal, ruler or wrong status.
 p.key('alt-f3');assert_frame(p,'input-restored-normal',name)
 for index,key in enumerate(['home','home','home','up','end']):
  assert_frame(p,'before-navigation-'+str(index),name);p.key(key)
 assert_frame(p,'input-EOF-noedit',name,pos='1.9');session.save_complete(p,'C48PRE',fields.save_named)
 assert_frame(p,'before-print-closed-main','C48PRE',pos='1.9')
 layout.print_disk(p,'C48PRN') # StrictProbe intercepts submitted frame BEFORE its queue key.
 assert_frame(p,'after-print-closed-main','C48PRE',pos='1.9');session.save_complete(p,'C48FIN',fields.save_named)
 assert_frame(p,'before-normal-exit','C48FIN',pos='1.9');exits=quit_module.finish_original(p)
 return {'fast_save':fast,'clear_actions':clear,'exit_actions':exits,'native_edit_after_retrieve':'none; only declared view/navigation/Save/print/Save'}

def probe_class(n):
 class StrictProbe(n.MutationProbe):
  current_name=''
  filename_target=None
  def retrieve(self,path,label):
   require(path in ['C:\\OUT\\C48SEED','C:\\OUT\\C48INPUT'],'RetrieveIdentity','only declared exact source')
   self.key('shift-f10');self.q.wait_for('Document to be retrieved:')
   screen=super().capture(label+'-closed-retrieve-prompt');strict_frame(screen,'',text='',question=screen_rows(RETRIEVE_PROMPT.read_text())[-1])
   self.type(path);draft=super().capture(label+'-closed-retrieve-draft');strict_frame(draft,'',text='',question='Document to be retrieved: '+path)
   self.key('ret');self.q.wait_absent('Document to be retrieved:');return self.capture(label)
  def key(self,keys):
   if keys=='ret'and self.filename_target is not None:
    target=self.filename_target;screen=super().capture('strict-filename-before-Enter-'+target)
    strict_frame(screen,self.current_name,pos='1.9',question='Document to be saved: C:\\OUT\\'+target)
    self.filename_target=None;self.current_name=target
   return super().key(keys)
  def capture(self,label):
   screen=super().capture(label)
   if re.fullmatch(r'C48(?:SEED|PRE|FIN)-save-prompt',label):
    strict_frame(screen,self.current_name,pos='1.9',question='Document to be saved:'+(' C:\\OUT\\'+self.current_name if self.current_name else ''))
    self.filename_target=label.split('-')[0]
   if re.fullmatch(r'C48(?:SEED|PRE|FIN)-saved',label):strict_frame(screen,self.current_name,pos='1.9')
   if label=='control-exact-retrieve':self.current_name='C48SEED';strict_frame(screen,self.current_name)
   if label=='actual-ui333-exact-retrieve':self.current_name='C48INPUT';strict_frame(screen,self.current_name)
   # Exact full nonempty frame at inherited print-submit capture, BEFORE
   # unchanged print_disk can issue ShiftF7/4. No helper source is patched.
   if label=='print-C48PRN-submitted':strict_frame(screen,'C48PRE',pos='1.9')
   if label.startswith('interop-clear-'):
    state=old.helpers()[3].exit_state(screen)
    if state=='main':
     if label.endswith('-0'):strict_frame(screen,'C48SEED',pos='1.9')
     else:strict_frame(screen,'',text='');self.current_name=''
    elif state=='save':strict_frame(screen,'C48SEED',pos='1.9',question='Save document? Yes (No)                            (Text was not modified)')
    elif state=='exit-wp':strict_frame(screen,'C48SEED',pos='1.9',question='Exit WP? No (Yes)                               (Cancel to return to document)')
    else:raise Refusal('UnknownClearFrame','no full-frame clear action for '+state)
   if label.startswith('exit-state-'):
    state=old.helpers()[3].exit_state(screen)
    if state=='main':strict_frame(screen,'C48FIN',pos='1.9')
    elif state=='save':strict_frame(screen,'C48FIN',pos='1.9',question='Save document? Yes (No)                            (Text was not modified)')
    elif state=='exit-wp':strict_frame(screen,'C48FIN',pos='1.9',question='Exit WP? No (Yes)                               (Cancel to return to document)')
    elif state!='dos':raise Refusal('UnknownExitFrame','no full-frame exit key for '+state)
   return screen
 return StrictProbe

def sources():
 import resaved_prefix
 rows=resaved_prefix.sources();seen={p['path']for p in rows}
 paths=[HERE/'adapter.py',HERE/'setup_owner.py',HERE/'test_setup_entry.py',HERE/'test_adapter.py',HERE/'run_checks.py',HERE/'README.md',HERE/'review-feedback.md',HERE/'review-source.json',HERE/'transition-prelaunch2.json',HERE/'history/prelaunch-cycle1/receipt.json',HERE/'history/prelaunch-cycle1/review/report.md.txt',HERE/'history/prelaunch-cycle1/review/seals.json.txt',ROOT/'internal/document/evidence/wp46/oracle.py',ROOT/'internal/document/evidence/wp44/oracle.py',ROOT/'internal/document/evidence/wp46/bin/producer',ROOT/'internal/document/evidence/wp46/producer-execution.json',ROOT/'internal/document/evidence/wp46/compiled-project-packages.json',ROOT/'internal/document/evidence/wp46/producer/main.go',ROOT/'internal/document/evidence/wp46/producer/go.mod',ROOT/'docs/research/continuation/native-constructor-design/schema.json',*FRAME_PINS.values(),*MENU_PINS.values(),PRINT_REFERENCE,RETRIEVE_PROMPT,RETRIEVE_DRAFT,ROOT/CANDIDATE,ROOT/'docs/research/continuation/new-session/build-final/wordling.bin',ROOT/'docs/research/continuation/new-session/build-final/source.json',ROOT/'docs/research/continuation/new-session/pty-final/reopen-ascii-edit/result.json',ROOT/'docs/research/continuation/new-session/pty-final/reopen-ascii-edit/injected.json',ROOT/'docs/research/continuation/new-session/pty-final/reopen-ascii-edit/wire-output.bin',ROOT/'docs/research/continuation/new-session/pty-final/reopen-ascii-edit/frames.json',ROOT/'docs/research/continuation/new-session/manifest.json',ROOT/'scripts/reference/native_genesis.py',*sorted((ROOT/'internal/document').glob('*.go'))]
 for p in paths:
  if str(p.relative_to(ROOT))not in seen:rows.append(pin(p));seen.add(str(p.relative_to(ROOT)))
 return sorted(rows,key=lambda x:x['path'])
def historical_proposal():
 receipt=json.loads((HERE/'history/prelaunch-cycle1/receipt.json').read_text())
 require(receipt['source_commit']=='d2999d2dbb023e1b9122b64c512a03df757b4505'and receipt['plan_sha256']=='a38e73e8418008c56b41ab5082f241cadf7d8dc997ecc2f1f9c812d8070dc238','ProposalHistory','exact cycle1 authority')
 counts={}
 for row in receipt['files']:
  path=ROOT/row['archive_path'];require(path.is_file()and path.stat().st_size==row['size']and sha(path)==row['sha256'],'ProposalHistory',row['archive_path']);counts[row['role']]=counts.get(row['role'],0)+1
 require(counts=={'complete-proposal21-plus-seal':22,'all90-source-input-pins':90,'exact-independent-review-artifact':16},'ProposalHistory','complete22/90/16 inert copies required')
 require(sha(HERE/'history/prelaunch-cycle1/review/report.md.txt')=='208e4829b0f8860ff9c7dd41ed87b81b8806c49634b6d156152d5a8f6a1eafd1'and sha(HERE/'history/prelaunch-cycle1/review/seals.json.txt')=='b632d4560b2c7a500f8142ff447017d2afe9073408429f5f162b9452b97ff391','ProposalHistory','exact independent prelaunch findings/seals')
 return counts

def provenance():
 historical_proposal()
 require(sha(ROOT/CANDIDATE)==CANDIDATE_SHA and(ROOT/CANDIDATE).stat().st_size==333,'CandidateIdentity','exact actual UI333 required')
 require(subprocess.check_output(['git','rev-parse','46afe8f5dbae0e404e4ab55f07b99cdfdf6aa705:'+CANDIDATE],cwd=ROOT,text=True).strip()=='8f8928ff8b2caaa287db7ac6db1764858e9ae582','CandidateGitIdentity','exact approved original UIblob required')
 require(subprocess.check_output(['git','show','46afe8f5dbae0e404e4ab55f07b99cdfdf6aa705:'+CANDIDATE],cwd=ROOT)==(ROOT/CANDIDATE).read_bytes(),'CandidateGitIdentity','original emitted Gitblob changed')
 report=json.loads((HERE.parent/'pty-final/reopen-ascii-edit/result.json').read_text());build=json.loads((HERE.parent/'build-final/source.json').read_text())
 require(report['failure']is None and report['returncode']==0 and report['termios_restored']is True and report['binary']['sha256']==build['binary']['sha256']==PRODUCER and sha(HERE.parent/'build-final/wordling.bin')==PRODUCER,'UIProducerProvenance','real executable receipt/binary differs')
 output=next(x for x in report['outputs']if x['kind']=='ascii-Z');require(output['sha256']==CANDIDATE_SHA and output['size']==333,'UIProducerProvenance','real output association')
 events=json.loads((HERE.parent/'pty-final/reopen-ascii-edit/injected.json').read_text());require(sum(x['label']=='ordinary subsequent edit at EOF'and x['hex']=='5a'for x in events)==1,'UIProducerProvenance','exact actual Z command required')
 for path,row in build['actual_compiled_project_inputs'].items():require(sha(ROOT/path)==row['sha256']and(ROOT/path).stat().st_size==row['size'],'ProducerSourceDrift',path)
 # Preserve ALL old322 source/raw files, rather than retroactively adding the plan.
 require(subprocess.check_output(['git','show','46afe8f5dbae0e404e4ab55f07b99cdfdf6aa705:docs/research/continuation/new-session/manifest.json'],cwd=ROOT)==(HERE.parent/'manifest.json').read_bytes(),'HistoricalManifestIdentity','old322 seal must remain exact original Gitblob')
 for path,row in json.loads((HERE.parent/'manifest.json').read_text())['files'].items():require(sha(ROOT/path)==row['sha256']and(ROOT/path).stat().st_size==row['size'],'HistoricalEvidenceDrift',path)
 value=old.product('-verify',ROOT/CANDIDATE,'-require-preprint');require(value['admitted']is True and value['body_hex']==TEXT.encode().hex(),'CandidatePublicReader','actual approved public consumer refusal');old.profile_fields(ROOT/CANDIDATE,value['inspection']);return value

def plan():
 import resaved_prefix
 native=provenance();base=resaved_prefix.plan();attempts=[]
 for ref in [RETRIEVE_PROMPT,RETRIEVE_DRAFT]:require(subprocess.check_output(['git','show','18d6afe:'+str(ref.relative_to(ROOT))],cwd=ROOT)==ref.read_bytes(),'RetrieveBaselineGitIdentity','approved13 exact prompt/draft source differs')
 for ref in [*FRAME_PINS.values(),*MENU_PINS.values(),PRINT_REFERENCE]:require(subprocess.check_output(['git','show','44aab36accdf14a370a67fd73945907871ab7193:'+str(ref.relative_to(ROOT))],cwd=ROOT)==ref.read_bytes(),'BaselineGitIdentity','actual approved46 frame/fullPRN differs')
 listing=subprocess.run(['mdir','-b','-i',str(PRIVATE/'master/harddisk.img')+'@@1048576','::OUT'],capture_output=True,timeout=15);require(listing.returncode==0,'MasterDirectory','master OUT unavailable');names={s.strip().replace('\\','/').rsplit('/',1)[-1].upper()for s in listing.stdout.decode(errors='strict').splitlines()if s.strip()};require(not any(n.split('.')[0]in {x.split('.')[0]for x in NAMES}for n in names),'MasterCollision','declared native/print names already in master')
 for mode in ['control','candidate']:
  for repetition in [1,2]:
   ident=f'wp48z-{mode}-r{repetition}';work=PRIVATE/'runs'/ident;attempts.append({'id':ident,'mode':mode,'repetition':repetition,'private_work':str(work),'qemu_argv':frozen_argv(work)})
 return {'schema':'wordling.wp48.ui333-original-plan/v1','candidate':pin(ROOT/CANDIDATE),'candidate_blob':'8f8928ff8b2caaa287db7ac6db1764858e9ae582','actual_UI_binary_sha256':PRODUCER,'body_hex':TEXT.encode().hex(),'whole_native_classes':1,'prior_WP48_original_attempts':0,'maximum_attempts_including_failures':4,'attempts':attempts,'sources':sources(),'master':base['master'],'tools':base['tools'],'manuals':base['manuals'],'preboot_resources':base['preboot_resources'],'profile_id':base['profile_id'],'profile_sha256':base['profile_sha256'],'shared_lock':str(PRIVATE/'session1.lock'),'batch_lease':str(PRIVATE/'wp48z-batch.lock'),'setup_ownership_policy':'non-replaceable ledger-path+.owner O_EXCL claim before batch setup; no foreign ledger overwrite; retained claim blocks restart','socket':str(PRIVATE/'runtime'/TAG/'qmp.sock'),'ledger':str(PRIVATE/'wp48z-attempts.json'),'public_output':str((HERE/'runs'/GRANT_ID).relative_to(ROOT)),'master_OUT_listing_sha256':hashlib.sha256(listing.stdout).hexdigest(),'timeout_per_attempt_seconds':900,'control_recipe':'fresh original type G43ASCIIZ; first Save C48SEED; captured clear; Retrieve C48SEED; normal/Reveal gap0; normal EOF; noedit Save C48PRE; full print C48PRN; Save C48FIN; captured normal DOS','candidate_recipe':'fresh copy exact UI333 as C48INPUT; Retrieve; same normal/Reveal gap0/normal EOF; noedit PRE/print/FIN/normal DOS','prospective_Reveal9':'EXPECTED/DERIVED25-row hypothesis from pinned8char Reveal and9char normal; first counted control measures it; any unknown permanently halts all4 with no repair/retry/calibration','control_seed_relation':'exact entire control C48SEED vs UI333 except checked indexed packet6 must-format00/08; no packet relocation normalization','required_outputs':['C48PRE.WP5','C48FIN.WP5','C48PRN.PRN'],'control_extra':'C48SEED.WP5','controls_before_candidate':'BOTH fresh controls fully qualify and PRE/FIN/fullPRN agree before any candidate boot/consumption','postprint':'closed nonempty1172/counter02 readonly; full72/graph/wholebytes exact same-repetition controls','on_first_fault':'sticky fsynced ledger+raw; stop/extract only proven owned guest; halt entire plan; no retry/subset/resume/relabel; root new plan needed','release':'physical shared guard released immediately after stopped extraction, BEFORE offline qualification; logical root reservation spans all4','rights':'private masters/programs/manuals/settings/fonts hash metadata only; project authored scratch native/PRN/state evidence only','full_M1_accepted':False}
def check():return plan()
def verify_plan(p):
 require(p==check(),'SealedPlanIdentity','current inputs/helpers/profile/master/provenance differ from frozen proposal')
 for src in p['sources']:require((ROOT/src['path']).stat().st_size==src['size']and sha(ROOT/src['path'])==src['sha256'],'SourceDrift',src['path'])
def grant(args,p,g):
 expected={'authorized','grant_id','plan_sha256','attempt_ids','maximum_attempts_including_failures','authorization_note','argv'}
 require(set(g)==expected and g['authorized']is True and g['grant_id']==GRANT_ID and g['plan_sha256']==canonical(p)and g['attempt_ids']==ids()and type(g['maximum_attempts_including_failures'])is int and g['maximum_attempts_including_failures']==4 and isinstance(g['authorization_note'],str)and bool(g['authorization_note'])and g['argv']==[sys.executable,*args],'GrantMismatch','separate root exact7-field/argv/source-plan/all4 grant required')
def empty_ledger(p):return {'schema':'wordling.wp48.ui333-ledger/v1','plan_sha256':canonical(p),'maximum':4,'halted':False,'attempts':[]}
def ledger_ok(p,l):
 require(l.get('schema')==empty_ledger(p)['schema']and l.get('plan_sha256')==canonical(p)and type(l.get('maximum'))is int and l['maximum']==4 and l.get('halted')is False,'LedgerIdentity','unknown/wrong/halted ledger');prior=l.get('attempts');require(isinstance(prior,list)and len(prior)<=4 and[x['id']for x in prior]==ids()[:len(prior)]and all(x['outcome']=='complete-observation'for x in prior),'PriorFailure','only exact ordered completed prefix; first failure permanently halts')
 for index,row in enumerate(prior):require(row.get('mode')==('control'if index<2 else'candidate')and type(row.get('repetition'))is int and row['repetition']==index%2+1 and re.fullmatch('[a-f0-9]{64}',row.get('result_sha256',''))and re.fullmatch('[a-f0-9]{64}',row.get('result_file_sha256','')),'LedgerIdentity','exact typed leaf/repetition/result bindings required')
 return prior

def postprint_relation(pre_path,post_path,pre,post):
 before=Path(pre_path).read_bytes();after=Path(post_path).read_bytes();require(pre['admitted']is True and pre['exact_no_edit']is True and pre['body_hex']==post['body_hex']==TEXT.encode().hex()and post['exact_no_edit']is True and post['admitted']is False,'PostprintState','nonempty preprint admitted/postprint readonly exactbody required')
 require(canonical(pre['inspection'])==canonical(post['inspection'])and len(before)==len(after),'GraphChanged','full checked graph/body spans must remain exact after print')
 fields=old.profile_fields(pre_path,pre['inspection']);owners={'header':(0,16)}
 for p in pre['inspection']['Packets']:owners['packet-'+str(p['Type'])]=(p['Data']['Offset'],p['Data']['Length'])
 cache=owners['packet-15'][0]+21;counter=owners['packet-6'][0]+8
 require(before[cache:cache+2]==bytes.fromhex('e724')and after[cache:cache+2]==bytes.fromhex('1172')and before[counter]==1 and after[counter]==2,'PostprintFields','closed nonempty e72401→117202 only')
 changes={i:(a,b)for i,(a,b)in enumerate(zip(before,after))if a!=b};expected={counter:(1,2),**{cache+i:(a,b)for i,(a,b)in enumerate(zip(bytes.fromhex('e724'),bytes.fromhex('1172')))if a!=b}}
 require(changes==expected,'PostprintWholeBytes','no unexplained native change after print')
 schema=json.loads((ROOT/'docs/research/continuation/native-constructor-design/schema.json').read_text());postfields=[]
 for f in schema['fields']:
  start,length=owners[f['owner']];offset,width=f['relative_owner_offset'],f['width'];require(0<=offset<=length and 0<width<=length-offset,'FieldBounds',f['name']);a=before[start+offset:start+offset+width];b=after[start+offset:start+offset+width];want=a
  if f['owner']=='packet-15'and offset==21:require(width==2,'FieldRoster','cachewidth');want=bytes.fromhex('1172')
  if f['owner']=='packet-6'and offset==8:require(width==1,'FieldRoster','counterwidth');want=b'\x02'
  require(b==want,'PostprintField',f['name']);postfields.append({'owner':f['owner'],'name':f['name'],'hex':b.hex(),'width':width})
 require(len(fields)==len(postfields)==72,'FieldRoster','full72 metadata fields');require(post.get('refusal')==f'document: UnsupportedMetadata at token -1, span {counter}+1','ReadonlyRefusal','exact public indexedcounter readonly failure required')
 return {'PRE_all72':fields,'FIN_all72':postfields,'graph_unchanged':True,'whole_byte_changes':[{'offset':i,'PRE':a,'FIN':b}for i,(a,b)in changes.items()],'actual_public_readonly_refusal':post.get('refusal'),'mutation_permission':False}
def qualify(directory,leaf,emit_Q=True):
 args=['-verify',directory/'C48PRE.WP5','-require-preprint']
 if emit_Q:args+=['-reedit-out',directory/'second-Go-edit.WP5']
 pre=old.product(*args);post=old.product('-verify',directory/'C48FIN.WP5');relation=postprint_relation(directory/'C48PRE.WP5',directory/'C48FIN.WP5',pre,post)
 prn=(directory/'C48PRN.PRN').read_bytes();reference=BASE/'C46PRN.PRN';require(prn==reference.read_bytes()and prn.count(TEXT.encode())==1,'FullPRNMismatch','exact known9char full reference stream required, no normalization')
 seed=None
 if leaf['mode']=='control':
  seedinfo=old.product('-verify',directory/'C48SEED.WP5','-require-preprint');old.profile_fields(directory/'C48SEED.WP5',seedinfo['inspection']);seed=old.guard.native_delta(ROOT/CANDIDATE,directory/'C48SEED.WP5',old.product('-verify',ROOT/CANDIDATE)['inspection'],TEXT.encode().hex());require(len(seed)==1 and seedinfo['bytes']==333,'ControlSeedMismatch','first original seed only indexed must-format08→00 differs from exactUI333')
 return {'PRE':pre,'FIN':post,'full72_graph_byte_relation':relation,'whole_PRN_sha256':sha(directory/'C48PRN.PRN'),'whole_PRN_size':len(prn),'control_seed_only_indexed_mustformat_difference':seed,'full_M1_accepted':False}
def custody_record(p,leaf,row):
 ident=row.get('owned_start_identity',{});proof=row.get('stop_proof',{});observations=proof.get('observations',[])
 require(type(ident.get('pid'))is int and ident['pid']>0 and isinstance(ident.get('startticks'),str)and ident['startticks'].isdigit()and int(ident['startticks'])>0 and bool(ident.get('executable'))and ident.get('argv')==leaf['qemu_argv'] and ident.get('socket')==p['socket']and ident.get('private_disks')==[str(Path(leaf['private_work'])/n)for n in ['boot.img','harddisk.img']],'ControlCustody','positive captured PID/startticks/exe/cmd/private disks/socket required')
 require(row.get('qemu_argv')==leaf['qemu_argv']and row.get('stop_method')=='QMP quit; own socket terminated'and proof.get('pid')==ident['pid']and proof.get('startticks')==ident['startticks']and proof.get('gone_or_same_zombie')is True and proof.get('socket_absent')is True and 0<=proof.get('elapsed_seconds',99)<=5 and bool(observations),'ControlCustody','normal method and bounded positive stop proof')
 last=observations[-1];require(last.get('classification')in ['gone','zombie']and last.get('socket_present')is False and last.get('observation_complete_monotonic',float('inf'))<=last.get('deadline_monotonic',0)and all(x.get('classification')in ['live','resample','gone','zombie']for x in observations),'ControlCustody','actual terminal identity-safe observation, no foreign/error/later-than-deadline proof')
 require((last['classification']=='gone'and last.get('pid_present')is False)or(last['classification']=='zombie'and last.get('state')=='Z'and last.get('startticks')==ident['startticks']),'ControlCustody','PID absence or SAME captured zombie required')
 require(row.get('master_before')==row.get('master_after')==p['master']and row.get('physical_guard_released')is True and row.get('guard_release_utc'),'ControlCustody','master/release receipts required')
 before=row.get('settings_before',{});after=row.get('settings_after',{});known=next(x for x in p['preboot_resources']if x['path'].upper().endswith('.SET'))
 require(before.get('private_path')==str(Path(leaf['private_work'])/'settings-before.SET')and before.get('size')==known['size']and before.get('sha256')==known['sha256']and after.get('private_path')==str(Path(leaf['private_work'])/'settings-after.SET')and type(after.get('size'))is int and after['size']>0 and re.fullmatch('[a-f0-9]{64}',after.get('sha256','')),'ControlCustody','before master SET identity and actual after-SET metadata required')
 return True

def control_rows(p,prior):
 rows=[]
 for repetition in [1,2]:
  ident=f'wp48z-control-r{repetition}';matches=[x for x in prior if x['id']==ident];require(len(matches)==1 and matches[0]['outcome']=='complete-observation','MissingControl','both fully qualified controls required BEFORE candidate input/boot');entry=matches[0];directory=ROOT/p['public_output']/ident;path=directory/'result.json'
  require(path.is_file()and sha(path)==entry['result_file_sha256'],'ControlIdentity','sealed result changed');row=json.loads(path.read_text());require(canonical(row)==entry['result_sha256']and row['id']==ident and row['mode']=='control'and type(row.get('repetition'))is int and row['repetition']==repetition and row['plan_sha256']==canonical(p)and row['guest_stopped']is True and row['normal_DOS']is True and row['exports_complete']is True and row['physical_guard_released']is True,'ControlIdentity','full actual control custody/source/repetition mismatch')
  custody_record(p,next(x for x in p['attempts']if x['id']==ident),row)
  old.normal_dos(directory)
  require(len(row['exports'])==4 and {Path(e['path']).name for e in row['exports']}=={'C48SEED.WP5','C48PRE.WP5','C48FIN.WP5','C48PRN.PRN'},'ControlExportIdentity','complete actual control artifact roles required')
  for export in row['exports']:
   require(Path(export['path'])==directory/Path(export['path']).name and export.get('present')is True and export.get('exit')==0,'ControlExportIdentity','no cross-run/partial/symbolic artifact alias')
   old.guard.checked_export_bytes(export['path'],export['size'],export['sha256'])
  fresh=qualify(directory,next(x for x in p['attempts']if x['id']==ident),emit_Q=False)
  for key in ['full72_graph_byte_relation','whole_PRN_sha256','whole_PRN_size','control_seed_only_indexed_mustformat_difference']:require(row['qualification'][key]==fresh[key],'ControlQualificationChanged','replayed raw public-reader/full-field/print result differs')
  for key,value in fresh['PRE'].items():require(row['qualification']['PRE'].get(key)==value,'ControlQualificationChanged','actual public PRE replay differs')
  require(row['qualification']['FIN']==fresh['FIN'],'ControlQualificationChanged','actual public FIN replay differs')
  rows.append((directory,row))
 for name in ['C48SEED.WP5','C48PRE.WP5','C48FIN.WP5','C48PRN.PRN']:require((rows[0][0]/name).read_bytes()==(rows[1][0]/name).read_bytes(),'ControlRepetitionMismatch','both complete controls must match BEFORE any candidate boot')
 return rows

def extract(work,directory,p,row,leaf,session):
 require(row.get('guest_stopped')is True,'StopUnproven','no stopped export without positive owned completion');row['settings_after']=session.settings_snapshot(work,'after')
 expected={'C48PRE.WP5','C48FIN.WP5','C48PRN.PRN'}|({'C48SEED.WP5'}if leaf['mode']=='control'else set());require({host for _,host in p.exports}<=expected,'ExportRoster','never extract an undeclared/unowned name')
 row['exports']=[old.export_one(work,directory,name,host)for name,host in p.exports]
 if leaf['mode']=='candidate':
  ent=old.export_one(work,directory,'C48INPUT','input-after.WP5');require(ent['sha256']==CANDIDATE_SHA and ent['size']==333,'CandidateInputChanged','original must not alter exact retrieved UIinput');row['input_after']=ent
 require({host for _,host in p.exports}==expected,'ExportRoster','missing required stopped exports; known partial outputs retained diagnostically')
 row['exports_complete']=True

def attempt(session,qmp,guest,n,plan,leaf,directory):
 work=Path(leaf['private_work']);row={**{k:leaf[k]for k in ['id','mode','repetition']},'plan_sha256':canonical(plan),'outcome':'incomplete','guest_stopped':False,'normal_DOS':False,'exports_complete':False,'physical_guard_released':False};probe=None;identity=None
 try:
  assets=[('C48INPUT',directory/'input.WP5')]if leaf['mode']=='candidate'else[];session.QMP_AUDIT_FILE=directory/'qmp-wire.jsonl';signal.setitimer(signal.ITIMER_REAL,900)
  argv=session.fresh_start(qmp,guest,work,assets);row['qemu_argv']=argv;settings=work/'settings-before.SET';row['settings_before']={'private_path':str(settings),'size':settings.stat().st_size,'sha256':sha(settings),'publication':'private SET metadata only'};require(argv==leaf['qemu_argv'],'LaunchArgv','actual argv differs');identity=old.guard.owned_identity(qmp,work,argv);row['owned_start_identity']=identity
  with qmp.QMP()as q:
   probe=probe_class(n)(q,directory);row['observations']=perform(probe,leaf['mode']);old.normal_dos(directory);row['normal_DOS']=True
 except Exception as e:row.update(error=str(e),error_code=getattr(e,'code',type(e).__name__),traceback=traceback.format_exc())
 finally:
  signal.setitimer(signal.ITIMER_REAL,0)
  if identity is None and qmp.SOCKET.exists():
   try:identity=old.guard.owned_identity(qmp,work,row.get('qemu_argv')or leaf['qemu_argv']);row['owned_start_identity']=identity
   except Exception as e:row['identity_error']=str(e)
  if identity is not None:
   try:
    old.guard.validate_stop_identity(qmp,identity);old.guard.same_identity(identity);row['stop_method']=session.stop_owned(qmp,guest);require(row['stop_method']=='QMP quit; own socket terminated','HostContained','normal QMP method required; host containment is incomplete');row['stop_observations']=[];row['stop_proof']=old.guard.stopped(qmp,identity,observations=row['stop_observations']);row['guest_stopped']=True
   except Exception as e:row.update(stop_error=str(e),stop_error_code=getattr(e,'code',type(e).__name__))
  else:row['stop_error']='positive owned PID/argv/executable/startticks/disks unavailable; no stop/extraction'
  if row['guest_stopped']and probe is not None:
   try:extract(work,directory,probe,row,leaf,session)
   except Exception as e:row.update(extraction_error=str(e),extraction_error_code=getattr(e,'code',type(e).__name__))
  if probe is not None:row.update(trace=probe.trace,checks=probe.checks,settings=probe.settings)
 return row

def archive_before_guest(p,directory,leaf,args):
 require(not directory.exists()and not Path(leaf['private_work']).exists(),'PriorAttempt','fresh public/private namespace only');directory.mkdir(parents=True)
 for source in p['sources']:
  src=ROOT/source['path'];dst=directory/'executing-source'/source['path'];dst=dst.with_name(dst.name+'.txt');dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst);require(sha(dst)==source['sha256'],'SourceArchive','archive differs before boot')
 if leaf['mode']=='candidate':
  asset=directory/'input.WP5';shutil.copyfile(ROOT/CANDIDATE,asset);asset.chmod(0o400);require(asset.read_bytes()==(ROOT/CANDIDATE).read_bytes()and sha(asset)==CANDIDATE_SHA,'InputArchive','readonly actual UI input copy differs')
 dump(directory/'prelaunch.json',{'plan':p,'plan_sha256':canonical(p),'leaf':leaf,'actual_argv':[sys.executable,*args],'recorded_before_fresh_start':True,'candidate_assets':[]if leaf['mode']=='control'else[{'source':p['candidate'],'copied_actual_bytes':str(directory/'input.WP5'),'mode':'0400','size':333,'sha256':CANDIDATE_SHA}]})
def failure_state(ledger,report,error):
 ledger['halted']=True;ledger['failure_code']=getattr(error,'code',type(error).__name__);report.update(complete=False,halted_before_next_guest=True,error=str(error),error_code=ledger['failure_code'],charged_attempts_including_failures=len(ledger['attempts']),positive_owned_start_identities=sum(bool(x.get('owned_start_identity'))for x in report['results']))
def halt(p,ledger,report,error,out):
 failure_state(ledger,report,error);dump(Path(p['ledger']),ledger);dump(out/'aggregate-ledger.json',ledger);dump(out/'run.json',report)
class SetupCallbacks:
 canonical=staticmethod(canonical)
 dump=staticmethod(dump)
 failure_state=staticmethod(failure_state)

def run(args,argv):
 require(args.allow_vm,'AuthorizationRequired','default offline; separate ROOT grant required')
 frozen=json.loads((HERE/'preflight.json').read_text());p=frozen['plan'];require(frozen['plan_sha256']==canonical(p),'SealedPlanIdentity','local frozen plan changed');g=json.loads(Path(args.grant).read_text());grant(argv,p,g)
 out=ROOT/p['public_output'];ledger=empty_ledger(p);report={'plan_sha256':canonical(p),'grant':g,'actual_argv':[sys.executable,*argv],'results':[],'complete':False,'logical_root_reservation':'all4; no other authorized original work','full_M1_accepted':False}
 try:
  with setup.claim(p,out,ledger,report,SetupCallbacks()):
   return run_claimed(args,argv,p,g,out,ledger,report)
 except setup.SetupHalted:
  print(json.dumps({'complete':False,'halted':True,'charged_attempts':0,'positive_owned_starts':0,'setup_failure_durable':True}),flush=True);return 1

def run_claimed(args,argv,p,g,out,ledger,report):
 require(not Path(p['ledger']).exists()and not out.exists(),'PriorAttempt','one new complete ordered batch only; no resume or retries')
 try:
  verify_plan(p);out.mkdir(parents=True);dump(Path(p['ledger']),ledger);dump(out/'grant.json',g)
  session,n,fields,quit_module,layout,genesis=old.helpers();qmp,guest,private=session.configure(PRIMARY,TAG);n.qmp=qmp;previous=signal.signal(signal.SIGALRM,session.timeout_signal)
  try:
   for leaf in p['attempts']:
    verify_plan(p);ledger_ok(p,ledger)
    controls=control_rows(p,ledger['attempts'])if leaf['mode']=='candidate'else None
    directory=out/leaf['id'];archive_before_guest(p,directory,leaf,argv)
    with session.exclusive(private):
     require(not qmp.SOCKET.exists()and not(qmp.RUNTIME/'qemu.pid').exists(),'ForeignRuntime','no foreign/reused socket or PID file');master_before={name:sha(guest.MASTER/name)for name in p['master']};require(master_before==p['master'],'MasterChanged','master differs before launch')
     entry={**{k:leaf[k]for k in ['id','mode','repetition']},'outcome':'incomplete','charged_at':now()};ledger['attempts'].append(entry);dump(Path(p['ledger']),ledger)
     row=attempt(session,qmp,guest,n,p,leaf,directory);row['master_before']=master_before;report['results'].append(row);dump(directory/'result.json',row);row['master_after']={name:sha(guest.MASTER/name)for name in p['master']}
    row['physical_guard_released']=True;row['guard_release_utc']=now();dump(directory/'stopped-release.json',{'physical_guard_released':True,'guest_stopped':row['guest_stopped'],'socket_absent':not qmp.SOCKET.exists(),'utc':row['guard_release_utc'],'before_offline_qualification':True})
    print(json.dumps({'event':'stopped-extraction-release','leaf':leaf['id'],'guest_stopped':row['guest_stopped'],'physical_guard_released':True,'before_offline_qualification':True}),flush=True)
    # The shared oracle guard is ALREADY released; no original IO in audit.
    dump(directory/'result.json',row)
    require(row['guest_stopped']and row['normal_DOS']and row['exports_complete']and row['master_after']==p['master']and not qmp.SOCKET.exists()and not any(k in row for k in ['error','stop_error','extraction_error']),'IncompleteAttempt','first fault halts entire4 plan, no NEXT')
    custody_record(p,leaf,row)
    row['qualification']=qualify(directory,leaf)
    if controls:
     control=controls[leaf['repetition']-1][0]
     for name in ['C48PRE.WP5','C48FIN.WP5','C48PRN.PRN']:require((directory/name).read_bytes()==(control/name).read_bytes(),'WholeControlMismatch','same-repetition full PRE/FIN/PRN mismatch')
    if leaf['mode']=='control'and leaf['repetition']==2:
     control=out/ids()[0]
     for name in ['C48SEED.WP5','C48PRE.WP5','C48FIN.WP5','C48PRN.PRN']:require((directory/name).read_bytes()==(control/name).read_bytes(),'ControlRepetitionMismatch','controls disagree, no candidate consumption')
    row['outcome']='complete-observation';dump(directory/'result.json',row);entry.update(outcome=row['outcome'],result_sha256=canonical(row),result_file_sha256=sha(directory/'result.json'));dump(Path(p['ledger']),ledger);dump(out/'aggregate-ledger.json',ledger);dump(out/'run.json',report)
    print(json.dumps({'leaf':leaf['id'],'outcome':row['outcome'],'physical_guard_released':True,'charged_attempts':len(ledger['attempts'])}),flush=True)
   report.update(complete=True,charged_attempts_including_failures=4,positive_owned_start_identities=sum(bool(x.get('owned_start_identity'))for x in report['results']),oracle_released=True);dump(out/'run.json',report);return 0
  finally:signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,previous)
 except Exception as e:
  if report['results']:
   last=report['results'][-1];dump(out/last['id']/'result.json',last)
  halt(p,ledger,report,e,out);print(json.dumps({'complete':False,'halted':True,'error_code':getattr(e,'code',type(e).__name__),'charged_attempts':len(ledger['attempts'])}),flush=True);return 1

def main():
 parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True);sub.add_parser('check');r=sub.add_parser('run');r.add_argument('--allow-vm',action='store_true');r.add_argument('--grant',required=True)
 args=parser.parse_args()
 if args.command=='check':
  p=check();fresh=[setup.owner_path(p),Path(p['batch_lease']),Path(p['ledger']),Path(p['socket']),Path(p['socket']).parent/'qemu.pid',ROOT/p['public_output'],*[Path(x['private_work'])for x in p['attempts']]];print(json.dumps({'plan':p,'plan_sha256':canonical(p),'VM_launched':False,'root_grant_required':True,'initial_paths':{str(x):{'exists':x.exists()}for x in fresh}},indent=2));return 0
 return run(args,sys.argv)
if __name__=='__main__':raise SystemExit(main())
