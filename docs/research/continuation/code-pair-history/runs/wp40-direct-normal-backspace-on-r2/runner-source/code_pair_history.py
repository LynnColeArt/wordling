#!/usr/bin/env python3
"""WP40 bounded original code-pair history; check/plan are offline, run needs release."""
import argparse
from contextlib import redirect_stdout, nullcontext
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
PRIMARY=Path('/home/lynn/projects/wordling')
OUT=ROOT/'docs/research/continuation/code-pair-history'
BASE='14e4ca34236212d57cdad08f573b19c3cd5f7d7d'
BOLD_ON=bytes.fromhex('c30cc3');BOLD_OFF=bytes.fromhex('c40cc4')
SOURCE=b'SA'+BOLD_ON+b'BC'+BOLD_OFF+b'D'
PLAIN=b'ABCD';PAIRED=b'A'+BOLD_ON+b'BC'+BOLD_OFF+b'D'
LIMIT=65536;TOKENS=64;PREVIOUS=3;GUEST_CAP=18
PIN_FILES=['kitty-specs/wp51-parity-01M64CVY/contracts/editing.md',
           'kitty-specs/wp51-parity-01M64CVY/contracts/session.md',
           'docs/research/continuation/native-edits/contract.md',
           'docs/research/continuation/native-edits/field-ledger.json',
           'docs/research/continuation/native-edits/reader_probe.go.txt',
           'docs/research/continuation/native-edits/print_audit.py',
           'docs/research/continuation/native-edits/codepane_cursor.py',
           'docs/research/continuation/native-edits/runs/wp23-b-deletions-r1/N0001.WP5',
           'docs/research/continuation/native-edits/runs/wp23-a-blocks-r1/N0025.WP5',
           'docs/research/command-scenarios.json',
           'docs/research/reference-environment/environment.json',
           'docs/research/reference-environment/resource-profile.json',
           'docs/research/reference-environment/installed-files.json']
PRIVATE_PINS={'reference.txt':'f1d786f3ea0697f652bdfb2c13cb7745a01e9fbe9abb64042e517f1a85c4304c',
              'toolkit.txt':'8ed26dae470713efd51c62de51686168a0ee0127efd428f50c5a622862269c8f',
              'WP51DevelopersToolkit.pdf':'5c5cf43f919ed08ffbcddd7c7380c6cabc26be181d588b44b9b66b9a8fd2c754',
              'WPDOS51Reference.pdf':'ca028c9dd8527bddc88975225dcf9888dc85f765706ef3486e89502542f8f531'}


class Refusal(ValueError):
    def __init__(self,code,detail):self.code=code;super().__init__(detail)
def need(ok,code,detail):
    if not ok:raise Refusal(code,detail)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def blob(path):return subprocess.check_output(['git','--no-optional-locks','-C',str(ROOT),'cat-file','blob',BASE+':'+path])


def cases():
    rows=[]
    registry=json.loads((ROOT/'docs/research/command-scenarios.json').read_text())
    for view in ['normal','reveal']:
        for key,boundary,gap,outgoing in [('delete','on',1,1),('backspace','on',2,1),('delete','off',4,3),('backspace','off',5,3)]:
            cid='CMD51-200'if key=='delete'else'CMD51-201'
            rows.append({'id':'direct-'+view+'-'+key+'-'+boundary,'view':view,'key':key,'target':boundary,
                         'incoming_gap':gap,'outgoing_gap':outgoing,'case_id':cid,'target_body_hex':PLAIN.hex(),
                         'confirmation':'Yes'if view=='normal'else'observed Reveal bypass'})
    rows.append({'id':'closing-block-repair-yes','view':'reveal','key':'backspace','target':'closing-only-block',
                 'incoming_gap':4,'range':[4,5],'outgoing_gap':5,'case_id':'CMD51-203','target_body_hex':PAIRED.hex(),'confirmation':'Delete Block? Yes'})
    for r in rows:
        source=next(c for c in registry if c['id']==r['case_id'])
        r.update(title=source['title'],feature_ids=source['feature_ids'],source_locators=source['source_locators'],
                 repetitions=2,source_native_hash='unavailable prelaunch: original typing/F6 creates and saves source before seed',
                 source_body_hex=SOURCE.hex(),seed='view first; Delete only S atg0; F1/Previous2×3/F1 preview-cancel; then Right×incoming_gap',
                 grouping_scope='explicitly pre-browsed and Right-separated only',
                 critical='target→Yes/bypass→immediate F1; no Save/navigation/pane/clear/retrieve interleaving',
                 history='newest+3Previous cycle; F1 cancel; reopen/newest Restore1; immediate post-Restore F1+3Previous/F1cancel; then X without navigation',
                 output='source native; post-history unique-X native; declared later Retrieve/Z/print/Save chain; no invented pre-X export',
                 status='unexecuted-template')
    return rows


def source_inputs():
    paths=sorted(str(p.relative_to(ROOT))for p in (ROOT/'scripts/reference').glob('*.py'))+PIN_FILES+['go.mod','go.sum']+sorted(str(p.relative_to(ROOT))for p in(ROOT/'internal/wp51').glob('*.go'))
    rows=[]
    for path in paths:
        raw=(ROOT/path).read_bytes()
        if path!='scripts/reference/code_pair_history.py':need(raw==blob(path),'SourceChanged',path)
        rows.append({'path':path,'size':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    # Fixed prelaunch controls; later offline audit files are not falsely claimed
    # to have executed in a guest or made part of the executing source identity.
    for name in ['scheduler.py','test_offline.py','run_checks.py']:
        p=OUT/name
        raw=p.read_bytes();rows.append({'path':str(p.relative_to(ROOT)),'size':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    return rows


def private_sources():
    rows=[]
    for name,want in PRIVATE_PINS.items():
        p=PRIMARY/'research/cache'/name;raw=p.read_bytes();need(hashlib.sha256(raw).hexdigest()==want,'PrivateSourceChanged',name)
        record={'path':str(p),'size':len(raw),'sha256':want,'publication':'metadata only',
                'applicability':'later documentary source; actual March behavior needs original observation'}
        if name.endswith('.txt'):
            pages=[129,130,577,578,579,714,715]if name=='reference.txt'else[24,37,38]
            texts=raw.decode().split('\f')
            record['page_text_hashes']=[{'pdf_page':n,'printed_page':n-(17 if name=='reference.txt'else 13),
                                         'sha256':hashlib.sha256(texts[n-1].encode()).hexdigest()}for n in pages]
        rows.append(record)
    return rows


def baseline_identities():
    profile=json.loads((ROOT/'docs/research/reference-environment/environment.json').read_text())
    private=PRIMARY/'research/cache/reference'
    pins=[(private/'master/boot.img',profile['master_boot_sha256']),
          (private/'master/harddisk.img',profile['master_disk_sha256']),
          (Path(profile['qemu_binary']['path']),profile['qemu_binary']['sha256'])]+[(Path(x['path']),x['sha256'])for x in profile['firmware']]
    rows=[]
    for path,want in pins:
        need(sha(path)==want,'BaselineChanged',str(path))
        rows.append({'path':str(path),'size':path.stat().st_size,'sha256':want,'publication':'metadata only'})
    return rows


def check():
    return {'scope':'original-reference-only-code-pair-history','vm_launched':False,'wordling_tested':False,'full_m1_accepted':False,
            'sources':source_inputs(),'private_sources':private_sources(),'baseline_identities':baseline_identities(),'cases':cases(),
            'guest_cap':GUEST_CAP,'preview_previous_limit':PREVIOUS,'native_byte_limit':LIMIT,'literal_token_limit':TOKENS,
            'runtime':'primary research/cache/reference/runtime/wp40/qmp.sock','lock':'primary research/cache/reference/session1.lock',
            'engine':'approved23 native_edits.execute; owned callback/global bindings only; approved39 captured final exit',
            'seed_preview_authorized':'root explicitly authorized same9contexts/18cap; no seed Restore/save; no unbrowsed grouping claim'}


def literal_tokens(body):
    need(len(body)<=LIMIT,'BodyLimit','Bounded diagnostic body exceeded')
    rows=[];p=0
    while p<len(body):
        need(len(rows)<TOKENS,'TokenLimit','Bounded literal analysis exceeded')
        if 32<=body[p]<=126:part=body[p:p+1];kind='ASCII'
        elif body[p:p+3]in [BOLD_ON,BOLD_OFF]:part=body[p:p+3];kind='BoldOn'if part==BOLD_ON else'BoldOff'
        else:raise Refusal('OpaqueLiteralShape','Unknown/truncated literal shape retained, not writer-admitted')
        rows.append({'offset':p,'hex':part.hex(),'kind':kind});p+=len(part)
    return rows


def inferred_fragment(marker_body,case):
    tokens=literal_tokens(marker_body);xs=[(i,t)for i,t in enumerate(tokens)if t['hex']=='58']
    need(len(xs)==1,'MarkerIdentity','Need exactly one declared X continuation')
    index,token=xs[0];p=token['offset'];before=marker_body[:p]+marker_body[p+1:]
    target=bytes.fromhex(case['target_body_hex']);target_tokens=literal_tokens(target)
    gap=case['outgoing_gap'];offset=len(target)if gap==len(target_tokens)else target_tokens[gap]['offset']
    left,right=target[:offset],target[offset:]
    need(before.startswith(left)and before.endswith(right),'RestoreRelationship','Not a literal insertion at the established target gap')
    fragment=before[len(left):len(before)-len(right)]if right else before[len(left):]
    return {'restored_fragment_hex':fragment.hex(),'post_restore_reopen_cancel_gap':index,'post_marker_gap':index+1,
            'pre_marker_body_hex_inferred':before.hex(),'pre_marker_export_exists':False,
            'basis':'unique X after Restore plus reopen/cycle/cancel removed from later actual native; not a direct isolated Restore gap or separate pre-X save',
            'permission':'literal diagnostic only; no history count/stack rule or production writer admission inferred'}


def literal_gap(body,directory,reveal):
    tokens=literal_tokens(body);vga=(directory/'vram.bin').read_bytes()
    need(len(vga)==4000,'VGAExtent','Complete80x25raw VGA required')
    if not reveal:
        need(all(t['kind']=='ASCII'for t in tokens)and len(body)<80 and not body.endswith(b' '),
             'AmbiguousNormalGap','No normal-view semantic gap inferred across hidden codes')
        cursor=json.loads((directory/'cursor.json').read_text())
        need(vga[:160:2].replace(b'\0',b' ').rstrip()==body and cursor['display_start_word']==0 and cursor['row']==0
             and 0<=cursor['column']<=len(body),'CursorMismatch','Whole plain body/hardware cursor disagree')
        return {'gap':cursor['column'],'basis':'exact entire short plain native body/raw row0/hardware cursor'}
    labels=[bytes.fromhex(t['hex']).decode()if t['kind']=='ASCII'else'[BOLD]'if t['kind']=='BoldOn'else'[bold]'for t in tokens]
    display=''.join(labels);need(len(display)<80,'CodePaneExtent','Code pane may wrap')
    row=vga[13*160:14*160]
    need(row[::2].replace(b'\0',b' ').decode('cp437').rstrip()==display,'CodePaneMismatch','Literal native labels differ from actual code pane')
    columns=[i for i in range(80)if row[2*i+1]==0x47];offset=0
    for i,label in enumerate(labels):
        if columns==list(range(offset,offset+len(label))):return {'gap':i,'active_columns':columns,'basis':'exact native labels and actual VGA code highlight'}
        offset+=len(label)
    need(columns==[offset],'AmbiguousCodeGap','Missing/ambiguous highlight cannot prove a code gap')
    return {'gap':len(tokens),'active_columns':columns,'basis':'actual native EOF label boundary and highlighted blank'}


def browse(p,label,previous=PREVIOUS,restore=False):
    start=len(p.trace);p.key('f1');screen=p.capture(label+'-opened');active='Undelete:'in screen
    captures=[label+'-opened'];lines=[screen.splitlines()[0]]
    if active:
        if not restore:
            for i in range(previous):
                p.key('2');s=p.capture(label+'-previous-'+str(i+1));captures.append(label+'-previous-'+str(i+1));lines.append(s.splitlines()[0])
        p.key('1'if restore else'f1');p.q.wait_absent('Undelete:');p.capture(label+'-returned')
    return {'label':label,'active':active,'restore':restore and active,'captures':captures,'overlaid_first_lines':lines,
            'trace_range':[start,len(p.trace)],'interpretation':'whole overlaid row, never an isolated hidden entry'}


def callback(case):
    def recipe(p):
        row={'id':case['id'],'case_id':case['case_id'],'plan':case,'history':[]};p.cases.append(row)
        p.type('S');row['source']=p.fixture(True);row['source_created_at']=datetime.now(timezone.utc).isoformat()
        row['native_source_hash_timing']='hash recorded only after original creation and stopped-image extraction; not a prelaunch seed hash'
        p.at(0,case['view']=='reveal');p.capture('view-before-sentinel')
        p.key('delete');p.capture('sentinel-S-deleted')
        seed=browse(p,'seed-only');row['history'].append(seed)
        need(seed['active']and any('S'in s for s in seed['overlaid_first_lines']),'UnprovedSeed','Unique S prior entry not visible in bounded seed preview')
        p.key(','.join(['right']*case['incoming_gap']));p.capture('target-incoming')
        if case['target']=='closing-only-block':
            p.key('alt-f4');p.q.wait_for('Block');p.key('right');p.capture('closing-only-selection')
        row['target_trace_start']=len(p.trace);p.key(case['key']);screen=p.capture('target-action')
        if case['view']=='normal':
            need('Delete ['in screen and '? No (Yes)'in screen,'ConfirmationChanged','Normal code Yes question missing')
            row['question']=screen.splitlines()[-1];p.key('y');p.q.wait_absent('? No (Yes)');screen=p.capture('target-confirmed')
        elif case['target']=='closing-only-block':
            need('Delete Block?'in screen,'ConfirmationChanged','Closing block question missing')
            row['question']=screen.splitlines()[-1];p.key('y');p.q.wait_absent('Delete Block?');screen=p.capture('target-confirmed')
        else:need('Delete ['not in screen and 'Delete Block?'not in screen,'ConfirmationChanged','Required Reveal bypass not observed')
        need('Block on'not in screen and '[Block]'not in screen,'BlockStillActive','No cleanup F1 may replace immediate history')
        row['first_history_trace']=len(p.trace);row['history'].append(browse(p,'immediate-target-history'))
        row['history'].append(browse(p,'newest-restore',previous=0,restore=True));p.capture('after-restore-before-any-save')
        if row['history'][-1]['restore']:row['history'].append(browse(p,'post-restore-history'))
        p.capture('pre-X-no-navigation');row['marker_trace']=len(p.trace);p.type('X');p.capture('unique-X-after-history')
        row['final']=p.snapshot('post-history-X-native');p.normal()
        row['interop']=p.interop(row['final'],'code-history-restored')
    return recipe


def trace_check(report):
    need(len(report['cases'])==1,'CaseCount','One finite context per fresh guest')
    c=report['cases'][0];trace=report['trace'];a=c['target_trace_start'];b=c['first_history_trace']
    actions=[x['key']for x in trace[a:b]if 'key'in x]
    need(actions in [[c['plan']['key']],[c['plan']['key'],'y']],'HistoryInterleaving','Editing/navigation/save inserted before immediate F1')
    need(trace[b].get('key')=='f1','HistoryInterleaving','First history action must be immediate F1')
    source_end=next(i for i,x in enumerate(trace)if x.get('capture')=='view-before-sentinel')
    need(not any(any(k in ['f10','shift-f10','shift-f3','alt-f3','f7']for k in x.get('key','').split(','))or 'type'in x for x in trace[source_end:c['marker_trace']]),
            'HistoryInterleaving','Save/retrieve/pane/clear interleaved in history interval')
    need(not any('type'in x for x in trace[a:b]),'HistoryInterleaving','Typed data before first history preview')
    need(trace[c['marker_trace']].get('type')=='X','MarkerIdentity','Only the declared unique X may follow the history interval')
    return c


def run(args):
    need(args.allow_vm and args.authorization_note.strip(),'AuthorizationRequired','No VM: explicit exclusive root grant and both flags required')
    need(re.fullmatch('[A-Za-z0-9_-]{1,80}',args.run_id),'RunIdentity','Safe new run identity required')
    prep=check();case=next(c for c in prep['cases']if c['id']==args.case)
    need(len(list((OUT/'runs').glob('*/run.json')))<GUEST_CAP,'GuestBudget','Initial18attempt cap reached; no automatic retries')
    # Approved modules are adapted in this process only. Files remain byte-identical.
    sys.path.insert(0,str(ROOT/'scripts/reference'))
    import native_edits as n
    import macro_quit as quit_probe
    import macro_session as session
    q,g,private=session.configure(PRIMARY,'wp40');n.OUT=OUT;n.PRIVATE=private;n.PROFILE=ROOT/'docs/research/reference-environment/environment.json'
    n.configure=lambda:None
    original_class=n.MutationProbe;original_start=g.start;original_stop=g.stop
    holder={}
    class OwnedProbe(original_class):
        def __init__(self,q,out):super().__init__(q,out);holder['probe']=self
        def snapshot(self,label):
            name=super().snapshot(label);full='C:\\OUT\\'+Path(name).stem
            self.q.wait_until(lambda s:full in s and 'Saving'not in s and 'Document to be saved:'not in s,'named completed native save '+full,timeout=20)
            self.capture(label+'-save-complete');return name
        def clear(self):
            # Later interoperability only. Declining a CAPTURED ExitWP keeps the
            # original app open with a blank doc; it is not final shutdown/history reset.
            self.capture('interop-clear-before');self.key('f7')
            self.q.wait_until(lambda s:quit_probe.exit_state(s)in ['save','exit-wp'],'actual interop clear question')
            screen=self.capture('interop-clear-question')
            if quit_probe.exit_state(screen)=='save':
                self.key('n');self.q.wait_until(lambda s:quit_probe.exit_state(s)=='exit-wp','captured interop ExitWP')
                screen=self.capture('interop-clear-exit-question')
            need(quit_probe.exit_state(screen)=='exit-wp','UnknownClearState','No blind No to an unrecognized exit question')
            self.key('n');self.q.wait_until(lambda s:s.splitlines()[0]==''and 'Doc 1'in s,'blank doc for declared later Retrieve')
            self.capture('interop-clear-blank')
    def finish(probe):
        holder['exit_actions']=quit_probe.finish_original(probe)
        return holder['exit_actions']
    n.MutationProbe=OwnedProbe;n.clean_exit=finish
    # execute's inner guard borrows this explicitly held identical shared lock;
    # the outer guard remains held through incomplete-run recovery extraction.
    n.exclusive=lambda:nullcontext()
    with session.exclusive(private):
        directory=OUT/'runs'/args.run_id;work=private/'native-edit-runs'/args.run_id
        def start(path):
            session.QMP_AUDIT_FILE=directory/'qmp-wire.jsonl'
            for pin in prep['sources']:
                target=directory/'prelaunch-source'/pin['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((ROOT/pin['path']).read_bytes())
            write(directory/'prelaunch.json',{'argv':sys.argv,'authorization_note':args.authorization_note,'preparation':prep,'case':case,
                                           'qemu_argv':g.arguments(path/'boot.img',path/'harddisk.img'),'source_native':'created later by original typing/F6; no prelaunch bytes/hash'})
            return session.fresh_start(q,g,path,[])
        def stop():
            class Original:
                def stop(self):return original_stop()
            holder['stop_method']=session.stop_owned(q,Original())
        g.start=start;g.stop=stop;log=io.StringIO();old=signal.signal(signal.SIGALRM,session.timeout_signal)
        try:
            signal.setitimer(signal.ITIMER_REAL,600)
            with redirect_stdout(log):report=n.execute(args.run_id,'code-pair-history',custom=callback(case))
        finally:
            signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,old)
            g.start=original_start;g.stop=original_stop;n.MutationProbe=original_class
        (directory/'engine.stdout.txt').write_text(log.getvalue())
        report['owned_adapter']={'approved23_execute':True,'approved39_final_exit':True,'short_runtime':str(q.SOCKET),'stop_method':holder.get('stop_method'),'outer_shared_lock_held_through_all_extraction':True,'final_exit_actions':holder.get('exit_actions',[])}
        report['guest_stopped']=not q.SOCKET.exists();need(report['guest_stopped'],'GuestStillActive','Do not extract/audit a live guest')
        p=holder.get('probe');report['stopped_exports']=[]
        if p:
            for name,host in p.exports:
                target=directory/host
                if not target.exists():
                    proc=subprocess.run(['mcopy','-i',str(work/'harddisk.img')+'@@1048576','::OUT/'+name,str(target)],capture_output=True,timeout=20)
                    status=proc.returncode
                else:status=0
                report['stopped_exports'].append({'name':name,'host':host,'exit':status,'size':target.stat().st_size if target.exists()else None,'sha256':sha(target)if target.exists()else None})
    report['oracle_released_before_offline_audit']=True
    report['artifacts']=[n.record(p,directory)for p in sorted(directory.rglob('*'))if p.is_file()and p.name not in ['run.json','result.xml']]
    write(directory/'run.json',report)
    suite=ET.Element('testsuite',name='WP40-original-context',tests='1');test=ET.SubElement(suite,'testcase',name=case['id'])
    if report['result']!='observed':ET.SubElement(test,'failure',message=report.get('error','incomplete original observation'))
    ET.indent(suite);ET.ElementTree(suite).write(directory/'result.xml',encoding='utf-8',xml_declaration=True)
    return {'run_manifest':str(directory/'run.json'),'result':report['result'],'error':report.get('error'),'guest_stopped':True,'oracle_released':True,'wordling_tested':False,'full_m1_accepted':False}


def reader_check(paths):
    # Compile the unchanged approved read-only client inside OWNED temporary space;
    # never write a scratch Go file into approved23's evidence namespace.
    source=ROOT/'docs/research/continuation/native-edits/reader_probe.go.txt'
    with tempfile.TemporaryDirectory(prefix='.reader-replay-',dir=OUT)as temporary:
        program=Path(temporary)/'main.go';program.write_bytes(source.read_bytes())
        result=subprocess.run(['go','run',str(program),*[str(p.resolve())for p in paths]],
                              cwd=ROOT,capture_output=True,text=True,timeout=90)
        need(result.returncode==0,'ReaderExecutionFailed',result.stderr)
        return {'reader_client_sha256':sha(source),'actual_reader_source_sha256':sha(ROOT/'internal/wp51/native.go'),
                'files':json.loads(result.stdout),'scope':'actual approved Go Parse/Export only, no serializer or semantic admission'}


def result(path):
    r=json.loads(path.read_text());base=path.parent
    need(r['scope']=='original-reference-only'and r['wordling_tested']is False,'ScopeChanged','Original-only scope differs')
    need(r['result']=='observed'and r['clean_exit']is True and r['guest_stopped']is True and r['oracle_released_before_offline_audit']is True,'IncompleteRun','No complete original witness')
    need(r['master_before']==r['master_after'],'MasterChanged','Master changed')
    for item in r['artifacts']:
        p=base/item['path'];need(p.resolve().is_relative_to(base.resolve())and p.stat().st_size==item['size']and sha(p)==item['sha256'],'ArtifactChanged',item['path'])
    pre=json.loads((base/'prelaunch.json').read_text());need(pre['preparation']['sources']==source_inputs(),'SourceChanged','Executing source/helper identities differ')
    case=trace_check(r);expected=next(c for c in cases()if c['id']==case['id']);need(case['plan']==expected,'CaseChanged','View/gap/action/confirmation/source identity differs')
    import native_edits as n
    import macro_quit as qp
    source=n.inspect(n.bounded_native(base/case['source']),False);need(bytes.fromhex(source['body_hex'])==SOURCE,'SourceNativeChanged','Actual original source not S A On BC Off D')
    target_capture=base/('target-confirmed'if 'question'in case else'target-action')
    target_proof=literal_gap(bytes.fromhex(expected['target_body_hex']),target_capture,expected['view']=='reveal')
    need(target_proof['gap']==expected['outgoing_gap'],'OutgoingGapChanged','Actual target result/body/gap differs from approved lead')
    if expected['view']=='reveal':
        incoming=literal_gap(PAIRED,base/'target-incoming',True)
        need(incoming['gap']==expected['incoming_gap'],'IncomingGapChanged','Actual incoming code boundary differs')
    else:
        boundary='[BOLD]'if expected['target']=='on'else'[bold]'
        need('Delete '+boundary in case.get('question',''),'ConfirmationChanged','Normal question identifies wrong attribute boundary')
    final=n.inspect(n.bounded_native(base/case['final']),False)
    inference=inferred_fragment(bytes.fromhex(final['body_hex']),expected)
    try:
        inferred_body=bytes.fromhex(inference['pre_marker_body_hex_inferred'])
        pre_gap=literal_gap(inferred_body,base/'pre-X-no-navigation',expected['view']=='reveal')
        need(pre_gap['gap']==inference['post_restore_reopen_cancel_gap'],'MarkerGapChanged','Raw pre-X gap and unique native X differ')
        inference['raw_pre_X_gap']=pre_gap
    except Refusal as error:
        inference['raw_pre_X_gap_unqualified']={'code':error.code,'detail':str(error)}
    need(qp.exit_state((base/'clean-exit/screen.txt').read_text())=='dos','FakeExit','Actual clear DOS required')
    commands=[]
    for line in(base/'qmp-wire.jsonl').read_text().splitlines():
        item=json.loads(line)
        if item['direction']=='tx-buffer':commands.append(json.loads(bytes.fromhex(item['raw_hex'])))
    actions=r['owned_adapter']['final_exit_actions'];need(0<len(actions)<8,'FakeExit','Missing captured final exit actions')
    for i,action in enumerate(actions):
        label='exit-state-'+str(i);state=qp.exit_state((base/label/'screen.txt').read_text())
        key='f7'if state=='main'else'n'if state=='save'else'y'
        need(state not in ['unknown','dos']and action=={'state':state,'key':key,'capture':label},'FakeExit','Final shutdown key differs from actual prompt')
        captured=[j for j,c in enumerate(commands)if '/'+label+'/'in json.dumps(c)]
        need(bool(captured),'FakeExit','No raw final exit capture')
        keys=[c.get('arguments',{}).get('command-line','')for c in commands[max(captured)+1:]if c.get('arguments',{}).get('command-line','').startswith('sendkey ')]
        need(keys and keys[0]=='sendkey '+key+' 80','FakeExit','Raw next key does not answer captured final question')
    for name in ['retrieved','edited','after_print']:
        raw=n.inspect(n.bounded_native(base/case['interop'][name]),False);body=bytes.fromhex(raw['body_hex'])
        wanted=bytes.fromhex(final['body_hex'])+(b''if name=='retrieved'else b'Z')
        need(body==wanted,'InteropChanged','Declared actual original Retrieve/edit/print/Save body differs')
    stream=base/case['interop']['print_stream'];need(stream.is_file()and stream.stat().st_size>0,'PrintMissing','Full original print stream missing')
    jobs=(base/('settings-print-'+stream.stem+'-job-status/screen.txt')).read_text()
    need(all(s in jobs for s in ['No print jobs','Job Number: None','Additional Jobs Not Shown: 0']),
         'PrintIncomplete','Actual original print queue completion proof missing')
    sys.path.insert(0,str(ROOT/'docs/research/continuation/native-edits'))
    from print_audit import audit as print_audit
    try:printed={'literal_semantics':print_audit(base/case['interop']['after_print'],stream)}
    except ValueError as e:printed={'qualified':False,'opaque_print_interpretation':str(e),'sha256':sha(stream),'bytes':stream.stat().st_size}
    paths=[base/case[k]for k in ['source','final']]+[base/case['interop'][k]for k in ['retrieved','edited','after_print']]
    actual_reader=reader_check(paths)
    return {'scope':'original-reference-only','result':'complete-bounded-observation-needs-independent-interpretation','case':case['id'],
            'history':case['history'],'target_body_gap_proof':target_proof,'literal_restore':inference,'print':printed,'actual_read_only_reader':actual_reader,'source':{'size':source['size'],'sha256':source['sha256']},
            'marker_native':{'size':final['size'],'sha256':final['sha256']},'history_effect_qualified':False,
            'reason':'UI overlay/cycle rows are not isolated entries; pair agreement and independent branch interpretation still required',
            'wordling_tested':False,'full_m1_accepted':False}


def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('check');sub.add_parser('plan')
    a=sub.add_parser('run');a.add_argument('run_id');a.add_argument('--case',choices=[c['id']for c in cases()],required=True);a.add_argument('--allow-vm',action='store_true');a.add_argument('--authorization-note',default='')
    a=sub.add_parser('result');a.add_argument('manifest',type=Path);args=p.parse_args()
    try:
        value=check()if args.command=='check'else{'cases':cases(),'guests':18,'vm_launched':False}if args.command=='plan'else run(args)if args.command=='run'else result(args.manifest)
        print(json.dumps(value,indent=2));return 1 if args.command=='run'and value['result']!='observed'else 0
    except Exception as e:
        print(json.dumps({'result':'refused-or-failed','code':getattr(e,'code',type(e).__name__),'error':str(e),'full_m1_accepted':False}));return 1


if __name__=='__main__':sys.exit(main())
