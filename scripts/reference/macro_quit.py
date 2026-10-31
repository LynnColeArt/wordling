#!/usr/bin/env python3
"""WP39 finite original-only normal-flow QUIT research; offline unless released."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import signal
import struct
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

import macro_session as session

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'docs/research/continuation/macro-quit'
WP32 = '4eb851eac3096d27d4743616ce3ae74f7a9edc05'
WP38 = '58eaf84a7e0ed75ea9c973828f0f9acd3365b3f1'
SESSION_SHA = '6119e4c4d8b4db14eb156001100798a10ec799fa08d6ac64c1d57d361412f616'
WP38_REVIEW = {'commit': 'cde944db51cff3a1379cc1094a0ec62cbcb72a53', 'path': 'kitty-specs/wp51-parity-01M64CVY/tasks/WP38-original-macro-session-probes/independent-cycle-1/review.md', 'sha256': '7e3595cd11a313536d2f51cc70496a04c12cfcc6f6cf1054143eaea70fa68510'}
CORPUS = 'kitty-specs/wp51-parity-01M64CVY/contracts/macro-fixtures.json'
SCOPE = 'original-reference-only-normal-flow-quit'
DOC1, DOC2 = session.DOC1, session.DOC2
WORDS = {'DISPLAY_OFF':0xFC0C,'ON_ERROR':0xFC1C,'GO':0xFC14,'QUIT':0xFC20,
         'LABEL':0xFC16,'RETURN':0xFC22,'NEST':0xFC18}


class ProbeFailure(ValueError):
    def __init__(self, code, detail):
        self.code = code
        super().__init__(detail)


def require(condition, code, detail):
    if not condition:
        raise ProbeFailure(code, detail)


def sha(p):
    return session.sha(p)


def blob_id(raw):
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()


def fixtures(case):
    # Registered handlers are deliberately UNFIRED. No QUIT occurs in a handler.
    emit = session.SDKNativeWords.emit
    handler = lambda label: [WORDS['ON_ERROR'],WORDS['GO'],label+'~~']
    ending = lambda label, marker, child=False: [WORDS['LABEL'],label+'~'+marker]+([WORDS['RETURN']]if child else[])
    # Only child RETURN is source-qualified; root/parent handlers end at EOF0000.
    if case == 'root':
        return {'Q39R.WPM':emit([WORDS['DISPLAY_OFF'],*handler('RH'),'R39',WORDS['QUIT'],
                                'ROOTAFTER',*ending('RH','ROOTERR')])}
    if case == 'nested':
        return {'Q39P.WPM':emit([WORDS['DISPLAY_OFF'],*handler('PH'),'P39',WORDS['NEST'],
                                  'C:\\OUT\\Q39C~','PARENTBACK',WORDS['QUIT'],
                                  'PARENTTAIL',*ending('PH','PARENTERR')]),
                'Q39C.WPM':emit([WORDS['DISPLAY_OFF'],*handler('CH'),'C39',WORDS['QUIT'],
                                  'CHILDTAIL',*ending('CH','CHILDERR',True)])}
    raise ProbeFailure('UnknownCase', 'Only root and nested normal-flow QUIT contexts exist')


def case_manifest(case):
    assets = []
    for name, raw in fixtures(case).items():
        offset, words = session.SDKNativeWords.inspect(raw)
        assets.append({'name':name,'size':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
                       'git_blob':blob_id(raw),'body_offset':offset,
                       'native_words':[f'{w:04X}'for w in words],
                       'quit_offsets':[offset+2*n for n,w in enumerate(words)if w==WORDS['QUIT']]})
    return {'case':case,'display_mode':'DISPLAY OFF FC0C','repetitions':2,'status':'unexecuted-template',
            'registered_handlers':'root RH; nested parent PH and child CH; all must remain unfired',
            'handler_endings':'root/parent terminal0000; child FC22 RETURN',
            'stop_all_hypothesis':DOC1+('R39'if case=='root'else'P39C39'),
            'alternate_child_return':DOC1+'P39C39PARENTBACK'if case=='nested'else None,
            'discriminators':['ROOTAFTER','ROOTERR']if case=='root'else
                ['PARENTBACK','PARENTTAIL','PARENTERR','CHILDTAIL','CHILDERR'],
            'manual_suffix':'READY','doc2_expected':DOC2,'assets':assets}


def inventory():
    require(sha(ROOT/'scripts/reference/macro_session.py')==SESSION_SHA,
            'HelperDrift','Approved WP38 helper differs')
    pins = [{'path':'scripts/reference/macro_quit.py','sha256':sha(Path(__file__))},
            {'path':'scripts/reference/macro_session.py','sha256':SESSION_SHA,'commit':WP38},WP38_REVIEW,{'path':session.TEMPLATE,'sha256':session.TEMPLATE_SHA}]+session.PINS
    rows=[]
    for pin in pins:
        raw=session.git_blob(pin['commit'],pin['path'])if 'commit'in pin else (ROOT/pin['path']).read_bytes()
        require(hashlib.sha256(raw).hexdigest()==pin['sha256'],'HelperDrift',pin['path'])
        if pin['path'].startswith('scripts/'):
            require((ROOT/pin['path']).read_bytes()==raw,'WorkingHelperDrift',pin['path'])
        rows.append({**pin,'size':len(raw),'git_blob':blob_id(raw)})
    return rows


def source_provenance():
    corpus=json.loads(session.git_blob(WP32,CORPUS))
    historical=[]
    for case,name,offset in [('CMD51-206','HANDLER',139),('CMD51-210','ONERROR',141),
                              ('CMD51-212','CHILD',141),('CMD51-212','PARENT',175),
                              ('CMD51-213','PARENT',141)]:
        row=next(x for x in corpus['wpm_exports']if x['case_id']==case and x['path'].endswith('/'+name+'.WPM'))
        raw=(ROOT/row['path']).read_bytes()
        require(len(raw)==row['size']and hashlib.sha256(raw).hexdigest()==row['sha256']
                and blob_id(raw)==row['git_blob']and raw[offset:offset+2]==b'\x20\xfc',
                'HistoricalSourceDrift',row['path'])
        historical.append({'case':case,'path':row['path'],'quit_offset':offset,'size':len(raw),
                           'sha256':row['sha256'],'git_blob':row['git_blob'],
                           'status':'old handler path skips site; NOT normal-flow proof'})
    manuals=[]
    for item in corpus['sources']:
        if not item['path'].startswith('research/cache/'):
            continue
        p=session.PRIMARY/item['path'];raw=p.read_bytes()
        require(len(raw)==item['size']and hashlib.sha256(raw).hexdigest()==item['sha256'],
                'PrivateSourceDrift',item['path'])
        record={'path':str(p),'size':len(raw),'sha256':item['sha256'],'publication':'metadata only'}
        if p.name in ['toolkit.txt','reference.txt']:
            page=111 if p.name=='toolkit.txt'else 869
            text=raw.decode().split('\f')[page-1]
            record.update(pdf_page=page,printed_page=98 if page==111 else 852,
                          page_text_sha256=hashlib.sha256(text.encode()).hexdigest())
        manuals.append(record)
    return {'wp32':WP32,'approved_wp38':WP38,'wp38_review_commit':WP38_REVIEW['commit'],
            'historical_sites':historical,'private_manuals':manuals,
            'reference_fixture_prefix':{'path':session.TEMPLATE,'sha256':session.TEMPLATE_SHA},
            'emitter_permission':'project-authored reference fixtures only; no product writer/editor permission'}


def check():
    return {'result':'offline-inputs-valid','scope':SCOPE,'wordling_tested':False,
            'vm_launched':False,'current_invocation_original_runs':0,'full_m1_accepted':False,
            'sources':inventory(),'provenance':source_provenance(),
            'cases':[case_manifest(x)for x in ['root','nested']],
            'shared_lock':str(session.PRIMARY/'research/cache/reference/session1.lock')}


def observed_branch(case, before, after, other):
    require(after==before+'READY','ManualContinuation','Manual READY must append to exact completed body')
    require(other==DOC2,'OtherBufferChanged','Dirty Doc2 differs')
    require(before.startswith(DOC1),'TargetChanged','Doc1 sentinel differs')
    if before==DOC1+('R39'if case=='root'else'P39C39'):
        return 'stop-all-hypothesis-corroborated'
    if case=='nested'and before==DOC1+'P39C39PARENTBACK':
        return 'child-return-observed-not-stop-all'
    return 'unqualified-observed-discriminator-branch'


def screen_body(text):
    lines=text.splitlines()
    require(bool(lines)and session.main_document(text),'CompletionState','Not an original main-document state')
    require(all(not x.strip()for x in lines[1:-1]),'WrappedBody','Bounded case must occupy one document row')
    require(len(lines[0])<64,'SaturatedBody','Bounded body may wrap/saturate')
    return lines[0]


def act(case,p,save):
    session.invoke(p,'Q39R'if case=='root'else'Q39P')
    # All source programs are finite, with no WAIT/input/loop; observe any branch,
    # not only the stop-all hypothesis. Unexpected markers remain raw evidence.
    time.sleep(.8)
    before=screen_body(p.capture('macro-completed-before-manual'))
    save(p,'QBEFORE')
    p.type('READY')
    p.q.wait_until(lambda s:session.main_document(s)and s.splitlines()[0]==before+'READY',
                   'manual READY after completed macro',timeout=8)
    after=screen_body(p.capture('manual-ready-after-quit'))
    save(p,'QAFTER')
    p.key('shift-f3');p.q.wait_for('Doc 2')
    other=screen_body(p.capture('doc2-preserved-after-quit'));save(p,'QOTHER')
    p.key('shift-f3');p.q.wait_for('Doc 1')
    p.capture('final-main-document')
    return {'before_manual':before,'after_manual':after,'other_buffer':other,
            'branch':observed_branch(case,before,after,other)}


def exit_state(screen):
    lines=screen.splitlines()
    if not lines:return 'unknown'
    # A literal DOS-looking line in a document is not an exited application.
    if lines[0]=='C:\\WP51>' and all(not line.strip()for line in lines[1:]):return 'dos'
    status=lines[-1]
    for prefix,state in [('Save document?','save'),('Exit doc 1?','exit-doc1'),
                         ('Exit doc 2?','exit-doc2'),('Exit WP?','exit-wp')]:
        if status.startswith(prefix):return state
    return 'main'if session.main_document(screen)else'unknown'


def finish_original(p):
    """Bounded captured exit protocol, after all named exports were saved.

    No is sent ONLY to an actually captured Save question. Exit questions get Yes.
    A normal-looking document or process termination cannot substitute for DOS.
    """
    actions=[]
    for step in range(8):
        screen=p.capture('exit-state-'+str(step));state=exit_state(screen)
        require(state!='unknown','UnknownExitState','Unexpected original exit state; no key guessed')
        if state=='dos':
            p.capture('clean-exit');return actions
        key='f7'if state=='main'else'n'if state=='save'else'y'
        action={'state':state,'key':key,'capture':'exit-state-'+str(step)}
        actions.append(action);p.trace.append({'captured_exit_action':action});p.key(key)
        allowed={'save','exit-doc1','exit-doc2','exit-wp','dos'}if state=='main'else \
                {'exit-doc1','exit-doc2','exit-wp','dos'}if state=='save'else \
                {'main','save','exit-doc1','exit-doc2','exit-wp','dos'}-{state}
        p.q.wait_until(lambda s:exit_state(s)in allowed,
                       'observed transition after '+state,timeout=15)
    raise ProbeFailure('ExitBudget','No actual normal DOS exit within eight captured stages')


def write_report(out,report):
    report['artifacts']=[{'path':str(p.relative_to(out)),'size':p.stat().st_size,'sha256':sha(p)}
                         for p in sorted(out.rglob('*'))if p.is_file()and p.name not in ['run.json','results.xml']]
    session.write_json(out/'run.json',report)
    suite=ET.Element('testsuite',name='WP39-original-observations',tests=str(len(report['results'])))
    for row in report['results']:
        t=ET.SubElement(suite,'testcase',name=row['id'])
        if row['outcome']!='complete-observation':ET.SubElement(t,'failure',message=row.get('error',row['outcome']))
        elif row['observed']['branch']=='unqualified-observed-discriminator-branch':
            ET.SubElement(t,'skipped',message='Complete raw observation; normal-flow context remains unqualified')
    ET.indent(suite);ET.ElementTree(suite).write(out/'results.xml',encoding='utf-8',xml_declaration=True)


def run(args):
    require(args.allow_vm and bool(args.authorization_note.strip()),'AuthorizationRequired',
            'No VM launch: explicit root release, --allow-vm and --authorization-note required')
    require(bool(re.fullmatch('[A-Za-z0-9_-]{1,48}',args.run_id)),'InvalidRunID','Use a new safe run ID')
    preparation=check()
    out=OUT/'runs'/args.run_id
    require(not out.exists(),'PriorEvidence','Prior evidence cannot be overwritten')
    out.mkdir(parents=True)
    inputs=[]
    for name,raw in fixtures(args.case).items():
        p=out/'input'/name;p.parent.mkdir(exist_ok=True);p.write_bytes(raw);inputs.append((name,p))
    for pin in preparation['sources']:
        raw=session.git_blob(pin['commit'],pin['path'])if 'commit'in pin else(ROOT/pin['path']).read_bytes()
        p=out/'runner-source'/pin['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
    session.write_json(out/'prelaunch.json',preparation)
    qmp,guest,private=session.configure(session.PRIMARY,'wp39')
    report={'run_id':args.run_id,'case':args.case,'scope':SCOPE,'wordling_tested':False,
            'full_m1_accepted':False,'physical_input_qualified':False,
            'argv':sys.argv,'authorization_note':args.authorization_note,
            'started_at':datetime.now(timezone.utc).isoformat(),'preparation':preparation,'results':[]}
    old=signal.signal(signal.SIGALRM,session.timeout_signal)
    try:
        with session.exclusive(private):
            report['master_before']={n:sha(guest.MASTER/n)for n in ['boot.img','harddisk.img']}
            for repetition in [1,2]:
                directory=out/(args.case+'-'+str(repetition));directory.mkdir()
                work=private/'runs'/('wp39-'+args.run_id)/directory.name
                row={'id':directory.name,'case':args.case,'repetition':repetition,'outcome':'error'}
                p=None;owned=False
                try:
                    require(not qmp.SOCKET.exists()and not work.exists(),'ForeignRuntime','Never stop/reuse an unknown guest')
                    session.QMP_AUDIT_FILE=directory/'qmp-wire.jsonl'
                    owned=True;row['qemu_argv']=session.fresh_start(qmp,guest,work,inputs)
                    from smoke import Probe
                    from extended import save_as
                    def save(probe,name):return session.save_complete(probe,name,save_as)
                    with qmp.QMP()as q:
                        p=Probe(q,directory);signal.setitimer(signal.ITIMER_REAL,180)
                        p.key('f3');p.q.wait_for('WP 5.1   03/09/92');p.capture('selected-release')
                        p.key('spc');p.q.wait_absent('Press any letter')
                        session.seed_buffers(p,save)
                        p.capture('before-macro-invocation')
                        signal.setitimer(signal.ITIMER_REAL,90)
                        row['observed']=act(args.case,p,save)
                        signal.setitimer(signal.ITIMER_REAL,120)
                        row['exit_actions']=finish_original(p);row['outcome']='complete-observation'
                except session.HostContainment as e:
                    row.update(outcome='host-contained',error=str(e))
                except Exception as e:
                    row.update(outcome='error',error=str(e))
                finally:
                    signal.setitimer(signal.ITIMER_REAL,0)
                    if owned:
                        if row['outcome']!='complete-observation'and qmp.SOCKET.exists():
                            try:
                                with qmp.QMP()as q:q.capture(directory/'failure-state')
                            except Exception as e:row['failure_capture_error']=str(e)
                        row['stop_method']=session.stop_owned(qmp,guest);row['guest_stopped']=True
                        if(work/'settings-before.SET').exists():
                            row['settings_before']={'private_path':str(work/'settings-before.SET'),'sha256':sha(work/'settings-before.SET')}
                            row['settings_after']=session.settings_snapshot(work,'after')
                        row['stopped_exports']=[]
                        exports=list(p.exports)if p else[]
                        exports +=[(name,name)for name,_ in inputs]
                        for name,host in dict(exports).items():
                            target=directory/host
                            proc=subprocess.run(['mcopy','-i',str(work/'harddisk.img')+'@@1048576',
                                                 '::OUT/'+name,str(target)],capture_output=True,timeout=15)
                            row['stopped_exports'].append({'name':name,'path':str(target.relative_to(out)),
                                'exit':proc.returncode,'size':target.stat().st_size if target.exists()else None,
                                'sha256':sha(target)if target.exists()else None,'stderr':proc.stderr.decode(errors='replace')})
                        if p:row.update(trace=p.trace,checks=p.checks)
                    report['results'].append(row)
            report['master_after']={n:sha(guest.MASTER/n)for n in ['boot.img','harddisk.img']}
            require(report['master_before']==report['master_after'],'MasterChanged','Private master changed')
        report['oracle_released_before_offline_audit']=True
        report['released_at']=datetime.now(timezone.utc).isoformat()
    finally:
        signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,old)
        write_report(out,report)
    return {'run_manifest':str(out/'run.json'),'results':report['results'],
            'oracle_released':report.get('oracle_released_before_offline_audit',False)}


def result(path):
    report=json.loads(path.read_text());base=path.parent
    require(report['scope']==SCOPE and report['wordling_tested']is False and report['full_m1_accepted']is False,
            'ScopeChanged','Original-only scope changed')
    require(report['case']in ['root','nested'],'CaseChanged','Unknown case')
    case=report['case']
    require(report['physical_input_qualified']is False,'ScopeChanged','Physical qualification invented')
    require(report['preparation']['sources']==inventory(),'SourceChanged','Executing source identity differs from pinned current runner/helpers')
    require(json.loads((base/'prelaunch.json').read_text())==report['preparation'],'CaseChanged','Prelaunch record differs')
    require(report['preparation']['cases']==[case_manifest(x)for x in ['root','nested']],
            'CaseChanged','Predeclared case/input binding differs')
    for pin in report['preparation']['sources']:
        archived=base/'runner-source'/pin['path']
        require(sha(archived)==pin['sha256']and archived.stat().st_size==pin['size'],
                'SourceChanged',pin['path'])
    require(report['master_before']==report['master_after']and report['oracle_released_before_offline_audit']is True,
            'IncompleteCustody','Master or release proof differs')
    actual_artifacts=[{'path':str(p.relative_to(base)),'size':p.stat().st_size,'sha256':sha(p)}
                      for p in sorted(base.rglob('*'))if p.is_file()and p.name not in ['run.json','results.xml']]
    require(report['artifacts']==actual_artifacts,'ArtifactChanged','Artifact set/bytes differ from sealed run')
    for item in report['artifacts']:
        p=base/item['path']
        require(p.resolve().is_relative_to(base.resolve())and not p.is_symlink()and p.stat().st_size==item['size']and sha(p)==item['sha256'],
                'ArtifactChanged',item['path'])
    rows=[]
    from document import plain_merge
    require(len(report['results'])==2,'IncompletePair','Need two fresh observations')
    for n,row in enumerate(report['results'],1):
        require(row['case']==case and row['id']==case+'-'+str(n)and row['repetition']==n,
                'CaseChanged','Sample identity differs')
        require(row['outcome']=='complete-observation'and row['guest_stopped']is True,
                'IncompleteObservation','A failure or host stop cannot qualify QUIT')
        directory=base/row['id']
        for item in row['stopped_exports']:
            target=base/item['path']
            require(target.resolve().is_relative_to(directory.resolve())and item['exit']==0
                    and target.stat().st_size==item['size']and sha(target)==item['sha256'],
                    'MissingNative','Stopped export custody differs')
        for name,raw in fixtures(case).items():
            require((base/'input'/name).read_bytes()==raw and(directory/name).read_bytes()==raw,
                    'InputChanged','Native WPM source/injected/extracted bytes differ')
        before=screen_body((directory/'macro-completed-before-manual/screen.txt').read_text())
        after=screen_body((directory/'manual-ready-after-quit/screen.txt').read_text())
        other=screen_body((directory/'doc2-preserved-after-quit/screen.txt').read_text())
        branch=observed_branch(case,before,after,other)
        require(row['observed']=={'before_manual':before,'after_manual':after,'other_buffer':other,'branch':branch},
                'SemanticChanged','Declared observation and independently decoded raw branch disagree')
        for name,body in [('D1BASE','D1SENT '),('D2BASE','D2SENT '),('QBEFORE',before),('QAFTER',after),('QOTHER',DOC2)]:
            native=plain_merge((directory/(name+'.WP5')).read_bytes())
            require(native['ascii_text']==body,'NativeSemanticChanged',name+' native text differs')
            require(any(x['name']==name and x['exit']==0 for x in row['stopped_exports']),
                    'MissingNative','No successful stopped native extraction')
        final=(directory/'final-main-document/screen.txt').read_text()
        require(screen_body(final)==after and 'Doc 1'in final.splitlines()[-1],
                'CompletionState','Final selected document differs')
        require(exit_state((directory/'clean-exit/screen.txt').read_text())=='dos',
                'CompletionState','Missing normal original shutdown')
        commands=[]
        for line in(directory/'qmp-wire.jsonl').read_text().splitlines():
            x=json.loads(line)
            if x['direction']=='tx-buffer':commands.append(json.loads(bytes.fromhex(x['raw_hex'])))
        require(0<len(row['exit_actions'])<8,'CompletionState','Missing bounded captured exit actions')
        for i,action in enumerate(row['exit_actions']):
            label='exit-state-'+str(i)
            state=exit_state((directory/label/'screen.txt').read_text())
            key='f7'if state=='main'else'n'if state=='save'else'y'
            require(state not in ['unknown','dos']and action=={'state':state,'key':key,'capture':label},
                    'CompletionState','Exit action differs from captured actual prompt')
            require({'captured_exit_action':action}in row['trace'],'CompletionState','Missing exit action trace')
            captured=[n for n,c in enumerate(commands)if '/'+label+'/'in json.dumps(c)]
            require(bool(captured),'CompletionState','Missing raw QMP exit capture')
            next_keys=[c.get('arguments',{}).get('command-line','')for c in commands[max(captured)+1:]
                       if c.get('arguments',{}).get('command-line','').startswith('sendkey ')]
            require(bool(next_keys)and next_keys[0]=='sendkey '+key+' 80',
                    'CompletionState','Captured prompt and next actual keyboard response differ')
        require(exit_state((directory/('exit-state-'+str(len(row['exit_actions'])))/'screen.txt').read_text())=='dos',
                'CompletionState','No captured final exit stage reached actual DOS')
        require(not any(x.get('arguments',{}).get('command-line')=='sendkey f1 80'for x in commands),
                'OperatorStop','Operator F1 cannot substitute for normal QUIT')
        require(any(x.get('key')=='alt-f10'for x in row['trace'])and any(x.get('type')=='READY'for x in row['trace']),
                'MissingInvocation','Missing actual invocation/manual trace')
        invoked='C:\\OUT\\'+('Q39R'if case=='root'else'Q39P')
        require(any(line.strip()=='Macro: '+invoked for line in(directory/'macro-name-exact-before-return/screen.txt').read_text().splitlines()),
                'InvocationChanged','Actual visible original invocation differs')
        rows.append({'id':row['id'],'branch':branch,'before_manual':before,'after_manual':after,'other_buffer':other})
    require(all(rows[0][k]==rows[1][k]for k in ['branch','before_manual','after_manual','other_buffer']),
            'RepetitionDisagrees','Two fresh native/state observations do not agree')
    return {'scope':SCOPE,'result':'two-complete-original-observations-agree','case':case,'observations':rows,
            'normal_context_qualified':rows[0]['branch']!='unqualified-observed-discriminator-branch',
            'wordling_tested':False,'full_m1_accepted':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('check');sub.add_parser('plan')
    p=sub.add_parser('run');p.add_argument('run_id');p.add_argument('--case',choices=['root','nested'],required=True)
    p.add_argument('--allow-vm',action='store_true');p.add_argument('--authorization-note',default='')
    p=sub.add_parser('result');p.add_argument('manifest',type=Path)
    a=parser.parse_args()
    try:
        value=check()if a.command=='check'else{'cases':[case_manifest(x)for x in ['root','nested']],'vm_launched':False}if a.command=='plan'else run(a)if a.command=='run'else result(a.manifest)
        print(json.dumps(value,indent=2,sort_keys=True));return 0
    except Exception as e:
        print(json.dumps({'result':'refused-or-failed','code':getattr(e,'code',type(e).__name__),
                          'error':str(e),'wordling_tested':False,'full_m1_accepted':False}));return 1


if __name__=='__main__':sys.exit(main())
