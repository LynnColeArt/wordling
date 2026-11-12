#!/usr/bin/env python3
"""WP42 original-resave field research. Offline by default; no native writer."""
import argparse
import atexit
import ast
from datetime import datetime, timezone
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import struct
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
PRIMARY = Path('/home/lynn/projects/wordling')
OUT = ROOT/'docs/research/continuation/resaved-prefix'
SCRIPT = ROOT/'scripts/reference/resaved_prefix.py'
PROFILE = ROOT/'docs/research/reference-environment/environment.json'
SCOPE = 'original-only-resaved-prefix-research-v1'
LIMIT = 65536
MAX_BLOCKS = 8
MAX_ATTEMPTS = 12
BRIDGE_BINARY = None
BODY = {'ascii':'41424344', 'one-bold':'41c30cc34243c40cc444',
        'two-bold':'41c30cc342c40cc443c30cc344c40cc445'}
INPUT = {'ascii':[('type','ABCD')],
         'one-bold':[('type','A'),('key','f6'),('type','BC'),('key','f6'),('type','D')],
         'two-bold':[('type','A'),('key','f6'),('type','B'),('key','f6'),('type','C'),
                     ('key','f6'),('type','D'),('key','f6'),('type','E')]}
NAMES = ['W42S0','W42G1','W42G2','W42G3','W42EDIT','W42FIN']

class Refusal(ValueError):
    def __init__(self, code, detail):
        self.code, self.detail = code, detail
        super().__init__(detail)

def require(ok, code, detail):
    if not ok:
        raise Refusal(code, detail)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def dump(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')

def bounded(path):
    with Path(path).open('rb') as stream:
        data = stream.read(LIMIT+1)
    require(len(data)<=LIMIT, 'InputLimit', 'research native input exceeds65536 bytes')
    return data

def closure():
    """Static local Python import closure, including modules imported only by helpers."""
    found, pending = {}, [SCRIPT, *[ROOT/'scripts/reference'/x for x in
                                  ['native_edits.py','text_layout.py','macro_quit.py']]]
    while pending:
        p = pending.pop()
        rel = str(p.relative_to(ROOT))
        if rel in found:
            continue
        raw = p.read_bytes()
        found[rel] = {'path':rel,'size':len(raw),'sha256':digest(raw)}
        require(len(found)<=40, 'HelperLimit', 'unexpected transitive Python closure')
        for node in ast.walk(ast.parse(raw)):
            names = [n.name for n in node.names] if isinstance(node,ast.Import) else \
                    [node.module] if isinstance(node,ast.ImportFrom) and node.module else []
            for name in names:
                candidate = ROOT/'scripts/reference'/(name.split('.')[0]+'.py')
                if candidate.is_file():
                    pending.append(candidate)
    return sorted(found.values(),key=lambda x:x['path'])

def sources():
    result = closure()
    for rel in ['internal/wp51/native.go','go.mod','go.sum',
                'docs/research/sources.json','docs/research/reference-baseline.json',
                'docs/research/reference-environment/environment.json',
                'docs/research/reference-environment/installed-files.json',
                'docs/research/continuation/native-edits/field-ledger.json',
                'docs/research/continuation/native-edits/manual-locators.json',
                'docs/research/continuation/native-edits/approved-prefix-warning.json',
                'docs/research/continuation/native-edits/contract.md',
                'docs/research/continuation/character-identity/native-comparison.json',
                'docs/research/continuation/resaved-prefix/readerbridge/main.go',
                'docs/research/continuation/resaved-prefix/tests/test_resaved_prefix.py']:
        p = ROOT/rel
        result.append({'path':rel,'size':p.stat().st_size,'sha256':sha(p)})
    return result

def recipes():
    result = []
    for grammar in BODY:
        for mode in ['baseline','disabled']:
            result.append({'id':grammar+'-'+mode,'grammar':grammar,'fast_save':mode,
                           'fresh_repetitions':[1,2],'input_actions':INPUT[grammar],
                           'expected_initial_body_hex':BODY[grammar],
                           'native_exports':[n+'.WP5' for n in NAMES],
                           'print_export':'W42PRN.PRN',
                           'generation_count':3,'run_id':'w42-'+grammar+'-'+mode})
    return result

def plan():
    profile = json.loads(PROFILE.read_text())
    manual = json.loads((ROOT/'docs/research/sources.json').read_text())
    # Metadata only: do not publish manual/settings/program/resource contents.
    manuals = []
    for ident, pages in [('REF51',[214]),('SDK51',list(range(16,32))+[116,117,118])]:
        item = next(x for x in manual if x['id']==ident)
        p = PRIMARY/'research/cache'/item['filename']
        require(sha(p)==item['sha256'],'ManualIdentity','pinned manual differs')
        manuals.append({'id':ident,'sha256':item['sha256'],'pdf_pages_one_based':pages,
                        'publication':'private source; metadata/locators only'})
    tools = []
    for name in ['qemu-system-i386','mcopy','mdir','mtype']:
        p = Path(shutil.which(name) or '/missing')
        require(p.is_file(),'ToolMissing',name)
        tools.append({'name':name,'sha256':sha(p),'path':str(p)})
    private = PRIMARY/'research/cache/reference'
    for name,expected in [('boot.img',profile['master_boot_sha256']),
                          ('harddisk.img',profile['master_disk_sha256'])]:
        require(sha(private/'master'/name)==expected,'MasterIdentity','private master differs')
    installed=json.loads((ROOT/'docs/research/reference-environment/installed-files.json').read_text())['files']
    resources=[]
    for basename in ['WP.EXE','WP.FIL','WP.DRS','STANPRIN.PRS','WP{WP}.SET']:
        path='WP51/'+basename
        raw=subprocess.check_output(['mtype','-i',str(private/'master/harddisk.img')+'@@1048576','::'+path],timeout=15)
        expected=next(x for x in installed if x['path']==path)
        require(digest(raw)==expected['sha256'] and len(raw)==expected['size'],'InstalledIdentity','preboot master resource differs from registry')
        resources.append({'path':path,'size':len(raw),'sha256':digest(raw),'publication':'preboot private bytes; metadata only'})
    cases=recipes()
    guest=importlib.import_module('guest')
    previous=(guest.RUNTIME,guest.SOCKET)
    try:
        guest.RUNTIME=private/'runtime/wp42';guest.SOCKET=guest.RUNTIME/'qmp.sock'
        for case in cases:
            case['run_argv']=[sys.executable,str(SCRIPT),'run','--run-id',case['run_id'],'--case',case['id'],'--allow-vm','--grant',str(private/'grants'/(case['run_id']+'.json'))]
            case['qemu_argv']=[guest.arguments(private/'runs'/('wp42-'+case['run_id'])/('r'+str(i))/'boot.img',private/'runs'/('wp42-'+case['run_id'])/('r'+str(i))/'harddisk.img') for i in [1,2]]
    finally:
        guest.RUNTIME,guest.SOCKET=previous
    return {'schema':'wordling.wp42.plan/v1','scope':SCOPE,'sources':sources(),
            'profile_id':profile['profile_id'],'profile_sha256':sha(PROFILE),
            'master':{'boot.img':profile['master_boot_sha256'],
                      'harddisk.img':profile['master_disk_sha256']},
            'manuals':manuals,'tools':tools,'preboot_resources':resources,'cases':cases,
            'maximum_guest_attempts_including_failures':MAX_ATTEMPTS,
            'source_seed':'original typing/F6 inside each fresh guest; no host native seed',
            'actions':['capture approved23 release/resource settings before source typing',
                       'ShiftF1; assert Setup Environment3;3; capture FastSave5 and actual Yes/No',
                       'baseline: leave captured value; disabled:5, capture question, n; F7 to document',
                       'perform exact input_actions; F10 save W42S0 to new absent name',
                       'three generations: captured F7 Save? n, captured ExitWP? n, assert blank; retrieve previous saved name; F10 distinct W42G1/2/3',
                       'Home3 Up then type X at body beginning; F10 W42EDIT',
                       'approved14 print_disk W42PRN, capture actual empty job queue; F10 W42FIN',
                       'approved39 finish_original with captured states, actual final DOS',
                       'stop owned guest, extract declared native/print only from stopped disk'],
            'fixed_runtime':str(private/'runtime/wp42/qmp.sock'),
            'shared_lock':str(private/'session1.lock'),
            'custody':'archive complete source closure/argv/plan/profile before launch; record guest resources as metadata; SET bytes stay private',
            'normal_exit':'macro_quit.finish_original/exit_state; unknown stops; host containment is not normal exit',
            'oracle_release':'after all stopped extraction, before offline result audit',
            'corpus_inputs':[{'path':str(p.relative_to(ROOT)),'size':p.stat().st_size,'sha256':sha(p)} for p in corpus()],
            'wordling_tested':False,'mutation_permission':False,'full_m1_accepted':False}

def plan_hash(value):
    return digest(json.dumps(value,sort_keys=True,separators=(',',':')).encode())

def bridge():
    global BRIDGE_BINARY
    if BRIDGE_BINARY is None:
        directory=Path(tempfile.mkdtemp(prefix='wordling-wp42-reader-'))
        atexit.register(shutil.rmtree,directory,ignore_errors=True)
        binary=directory/'reader'
        subprocess.run(['go','build','-trimpath','-buildvcs=false','-o',str(binary),
                        './docs/research/continuation/resaved-prefix/readerbridge'],
                       cwd=ROOT,check=True,capture_output=True,timeout=120)
        BRIDGE_BINARY=binary
    return BRIDGE_BINARY

def actual_reader(path):
    proc = subprocess.run([str(bridge()),str(Path(path).resolve())],cwd=ROOT,
                          capture_output=True,timeout=15,check=True)
    value=json.loads(proc.stdout)
    value['research_bridge']={'sha256':sha(bridge()),'bridge_source_sha256':sha(OUT/'readerbridge/main.go'),
                              'reader_source_sha256':sha(ROOT/'internal/wp51/native.go'),
                              'build_flags':['-trimpath','-buildvcs=false']}
    return value

def inspector():
    return importlib.import_module('native_edits')

def regions(info):
    spans = [(0,16,'header')]
    spans += [(b['offset'],b['offset']+50,'index@'+str(b['offset'])) for b in info['blocks']]
    spans += [(p['offset'],p['offset']+p['length'],
               ('deleted' if p['type']==65535 else 'packet'+str(p['type']))+'@'+str(p['index_offset']))
              for p in info['packets'] if p['length']]
    boundary = info['body_offset']
    edges = sorted({0,boundary,*[n for a,b,_ in spans for n in [a,b]]})
    return [{'offset':a,'length':b-a,'owners':[owner for x,y,owner in spans if x<=a and b<=y],
             'status':'unowned-unknown' if not any(x<=a and b<=y for x,y,_ in spans) else
                      'overlapping-unknown' if sum(x<=a and b<=y for x,y,_ in spans)>1 else 'owned-span'}
            for a,b in zip(edges,edges[1:]) if a<b]

def audit(path):
    raw = bounded(path)
    reader = actual_reader(path)
    report = {'size':len(raw),'sha256':digest(raw),'actual_go_reader':reader,
              'mutation_permission':False,'wordling_tested':False}
    if not reader['accepted']:
        report['status']='framing-refused'
        return report
    require(reader['exact_export'] and reader['sha256']==digest(raw),
            'ReaderIdentity','actual reader did not preserve exact input')
    try:
        info = inspector().inspect(raw,False)
    except ValueError as error:
        report.update(status='diagnostic-refused-read-only',diagnostic=str(error))
        return report
    require(len(info['blocks'])<=MAX_BLOCKS,'IndexLimit','research inspector bound')
    require(info['body_offset']==reader['inspection']['Body']['Offset'],
            'ReaderDisagreement','diagnostic body offset disagrees')
    ledger = json.loads((ROOT/'docs/research/continuation/native-edits/field-ledger.json').read_text())
    fields, links = [], []
    for field in ledger['field_coverage']:
        if field['owner']=='header':
            owners = [{'offset':0,'length':16,'type':None}]
        else:
            k = int(field['owner'].split('-')[1])
            owners = [p for p in info['packets'] if p['type']==k]
        for packet in owners:
            offset,width = packet['offset']+field['offset'],field['width']
            if field['offset']+width>packet['length']:
                continue
            fields.append({'owner':field['owner'],'offset':offset,'width':width,
                           'name':field['name'],'raw_hex':raw[offset:offset+width].hex(),
                           'documentary_references':field['references'],
                           'interpretation':'inherited23 field locator; no new-family write permission'})
    pools = [p for p in info['packets'] if p['type']==7]
    fonts = [p for p in info['packets'] if p['type']==15]
    if len(pools)==len(fonts)==1 and fonts[0]['length']==86:
        pool,font = pools[0],fonts[0]
        pointer = struct.unpack_from('<H',raw,font['offset']+18)[0]
        valid = pointer<pool['length'] and b'\0' in raw[pool['offset']+pointer:pool['offset']+pool['length']]
        links.append({'kind':'font-name-pool-local','source':font['offset']+18,
                      'target':pool['offset']+pointer,'bounds_valid':valid,
                      'authority':'approved23/SDK WP103–105; does not establish every new-family relationship'})
        afc = raw[font['offset']+50:font['offset']+86]
        links.append({'kind':'font-AFC-row-index','raw_hex':afc.hex(),
                      'bounds_valid':all(n in [254,255] or n<font['length']//86 for n in afc),
                      'body_reference':False,'authority':'approved23 literal one-row resource scope'})
    report.update(status='read-only-field-observation',body_offset=info['body_offset'],
                  body_sha256=digest(raw[info['body_offset']:]),body_hex=info['body_hex'],
                  diagnostic_body_grammar_refusal=info['body_grammar_refusal'],
                  blocks=info['blocks'],packets=[{k:v for k,v in p.items() if k!='hex'} for p in info['packets']],
                  prefix_regions=regions(info),inherited_field_observations=fields,
                  candidate_relationships=links,
                  blockers=['no WP42 fresh original field experiments yet',
                            'deleted payloads and unowned/slack relationships unqualified',
                            'field locator success is not semantic mutation permission'])
    return report

def assert_report(path, report):
    """Recompute semantic observations, so rehashing a forged claim cannot bless it."""
    require(report==audit(path),'SemanticMismatch','field/ownership/relationship report differs from actual bytes/source')

def corpus():
    warning = json.loads((ROOT/'docs/research/continuation/native-edits/approved-prefix-warning.json').read_text())
    result = [ROOT/'docs/research/reference-runs/2026-10-29-advanced-04/CMD51-204/ORIGIN.WP5']
    for run in warning['runs']:
        for row in run['native']:
            p = ROOT/'docs/research/continuation/character-identity/runs'/run['run_id']/'CMD51-138'/row['name']
            require(p.is_file() and sha(p)==row['sha256'],'CorpusIdentity','approved22 corpus mismatch '+str(p))
            result.append(p)
    # Actual approved23 post-print family; exact hash is frozen by check/plan output.
    p=ROOT/'docs/research/continuation/native-edits/runs/wp23-a-modes-r1/N0006.WP5'
    require(sha(p)=='b0367baef80fcf27afdaff61090971d462a96e9f9476fb304cb35e21e1f6813b','CorpusIdentity','approved23 post-print seed differs')
    result.append(p)
    return result

def check():
    current = plan()
    observed=[]
    for p in corpus():
        observed.append({'path':str(p.relative_to(ROOT)),'audit':audit(p)})
    return {'status':'offline-prepared','plan':current,'plan_sha256':plan_hash(current),
            'corpus':observed,'vm_launched':False,'oracle_lock_acquired':False,
            'guest_attempts':0,'mutation_permission':False,'full_m1_accepted':False}

def validate_grant(args, current):
    require(args.allow_vm,'AuthorizationRequired','guest launch disabled; root grant required')
    require(args.grant is not None,'AuthorizationRequired','root-authored frozen grant JSON required')
    grant=json.loads(Path(args.grant).read_text())
    require(set(grant)=={'schema','plan_sha256','run_id','case','repetitions','authorization_note'},
            'GrantShape','unknown/missing grant field')
    require(grant['schema']=='wordling.wp42.grant/v1' and
            grant['plan_sha256']==plan_hash(current) and grant['run_id']==args.run_id and
            grant['case']==args.case and grant['repetitions']==[1,2] and
            isinstance(grant['authorization_note'],str) and bool(grant['authorization_note'].strip()),
            'GrantMismatch','grant does not bind this frozen plan/case/two fresh attempts')
    return grant

def capture_fast_save(p, mode):
    p.key('shift-f1');screen=p.capture('fast-save-setup')
    require(re.search(r'3[^\n]*Environment',screen,re.I),'UnknownSetup','no captured Environment3')
    p.key('3');screen=p.capture('fast-save-environment-before')
    lines=[line for line in screen.splitlines() if re.search(r'5[^\n]*Fast Save',line,re.I)]
    require(len(lines)==1 and re.search(r'\b(Yes|No)\b',lines[0],re.I),
            'UnknownFastSave','must capture explicit actual FastSave5 Yes/No; no default guessed')
    before=re.findall(r'\b(Yes|No)\b',lines[0],re.I)[-1].lower()
    if mode=='disabled':
        p.key('5');screen=p.capture('fast-save-answer-question')
        require('Fast Save' in screen and re.search(r'\b(Yes|No)\b',screen),
                'UnknownFastSaveQuestion','no guessed answer in unknown menu')
        p.key('n');screen=p.capture('fast-save-environment-after')
        line=next((x for x in screen.splitlines() if re.search(r'5[^\n]*Fast Save',x,re.I)),'')
        require(re.search(r'\bNo\b',line,re.I),'FastSaveNotDisabled','disabled value not observed')
    p.key('f7');screen=p.capture('fast-save-return')
    require(importlib.import_module('macro_quit').exit_state(screen)=='main',
            'UnknownSettingsReturn','manual F7 did not return to document')
    return {'before':before,'requested':mode,'after':'no' if mode=='disabled' else before}

def save_named(p,name):
    p.key('f10');p.q.wait_for('Document to be saved:');p.capture(name+'-save-prompt')
    p.type('C:\\OUT\\'+name);p.key('ret');p.q.wait_absent('Document to be saved:')
    screen=p.capture(name+'-saved')
    require(importlib.import_module('macro_quit').exit_state(screen)=='main',
            'SaveIncomplete','save did not return to main document')
    p.exports.append((name,name+'.WP5'))

def clear_retrieve(p,name,label):
    quit_module=importlib.import_module('macro_quit')
    p.key('f7');screen=p.capture(label+'-clear-save-question')
    require(quit_module.exit_state(screen)=='save','UnknownClear','expected captured Save question')
    p.key('n');screen=p.capture(label+'-clear-exit-question')
    require(quit_module.exit_state(screen)=='exit-wp','UnknownClear','single-document ExitWP question required')
    p.key('n');screen=p.capture(label+'-cleared')
    require(quit_module.exit_state(screen)=='main' and not screen.splitlines()[0].strip(),
            'UnknownClear','approved No-clear branch did not yield blank document')
    p.retrieve('C:\\OUT\\'+name,label+'-retrieved')

def commands(trace):
    output=[]
    for item in trace:
        if 'key' in item:
            output.extend([['key',x.strip()] for x in item['key'].split(',')])
        if 'type' in item:
            output.append(['type',item['type']])
    return output

def phase(p,name,call):
    start=len(p.trace)
    value=call()
    p.phases.append({'name':name,'commands':commands(p.trace[start:])})
    return value

def expected_phases(recipe):
    key=lambda *items:[['key',x] for x in items]
    save=lambda name:key('f10')+[['type','C:\\OUT\\'+name]]+key('ret')
    value=[('initial-settings',None),('fast-save',key('shift-f1','3')+
             (key('5','n') if recipe['fast_save']=='disabled' else [])+key('f7')),
           ('source',[list(x) for x in recipe['input_actions']]),('save-'+NAMES[0],save(NAMES[0]))]
    for i in range(1,4):
        value += [('retrieve-'+str(i),key('f7','n','n','shift-f10')+
                   [['type','C:\\OUT\\'+NAMES[i-1]]]+key('ret')),('save-'+NAMES[i],save(NAMES[i]))]
    value += [('X-edit',key('home','home','home','up')+[['type','X']]),('save-'+NAMES[4],save(NAMES[4])),
              ('print',key('shift-f7','s','3','2','8')+[['type','C:\\OUT\\W42PRN.PRN']]+
               key('ret','f7','f7','1','shift-f7','4','f7')),('save-'+NAMES[5],save(NAMES[5]))]
    return value

def verify_actions(recipe,row):
    expected=expected_phases(recipe)
    require([p['name'] for p in row['phases']]==[n for n,_ in expected], 'PhaseScope','wrong/missing action phase')
    for observed,(name,wanted) in zip(row['phases'],expected):
        if name=='initial-settings':
            # The approved helper leaves each captured menu in 1..4 F7 steps.
            tokens=observed['commands']
            variants=[]
            for a in range(1,5):
                for b in range(1,5):
                    variant=['f3','spc','shift-f7','s']+['f7']*a+['shift-f8','3','3']+['f7']*b+['shift-f8','2','f7','shift-f8','1','f7']
                    variants.append([['key',x] for x in variant])
            require(tokens in variants,'HiddenInterleaving','unplanned initial settings command')
        else:
            require(observed['commands']==wanted,'HiddenInterleaving','unplanned key/typing in '+name)
    observed=[x for p in row['phases'] for x in p['commands']]
    observed += [['key',x['key']] for x in row['exit_actions']]
    require(observed==commands(row['trace']),'HiddenInterleaving','commands outside planned phases/exit')

def perform(p, recipe):
    p.phases=[]
    phase(p,'initial-settings',lambda:inspector().settings(p))
    state=phase(p,'fast-save',lambda:capture_fast_save(p,recipe['fast_save']))
    def type_source():
        for action,value in recipe['input_actions']:
            getattr(p,action)(value)
        p.capture('source-original-typed')
    phase(p,'source',type_source)
    phase(p,'save-'+NAMES[0],lambda:save_named(p,NAMES[0]))
    previous=NAMES[0]
    for generation in range(1,4):
        phase(p,'retrieve-'+str(generation),lambda:clear_retrieve(p,previous,'generation-'+str(generation)))
        phase(p,'save-'+NAMES[generation],lambda:save_named(p,NAMES[generation]))
        previous=NAMES[generation]
    def edit():
        p.key('home,home,home,up');p.type('X');p.capture('original-X-edit')
    phase(p,'X-edit',edit)
    phase(p,'save-'+NAMES[4],lambda:save_named(p,NAMES[4]))
    phase(p,'print',lambda:importlib.import_module('text_layout').print_disk(p,'W42PRN'))
    phase(p,'save-'+NAMES[5],lambda:save_named(p,NAMES[5]))
    return state

def run(args):
    # Authorization is checked before creating output, locks, imports or guests.
    require(args.allow_vm,'AuthorizationRequired','no guest grant yet; offline preparation only')
    require(re.fullmatch(r'[a-zA-Z0-9_-]{1,32}',args.run_id or ''),'RunID','safe fresh run ID required')
    current=plan();grant=validate_grant(args,current)
    recipe=next((x for x in current['cases'] if x['id']==args.case),None)
    require(recipe is not None,'UnknownCase','exact frozen case required')
    require(args.run_id==recipe['run_id'],'RunID','must use the frozen exact case run identity')
    directory=OUT/'runs'/args.run_id
    require(not directory.exists(),'PriorEvidence','run output exists')
    directory.mkdir(parents=True)
    for row in current['sources']:
        p=directory/'runner-source'/row['path'];p.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/row['path'],p)
    shutil.copyfile(PROFILE,directory/'environment.json')
    dump(directory/'prelaunch.json',{'plan':current,'plan_sha256':plan_hash(current),'grant':grant,'argv':sys.argv})
    session=importlib.import_module('macro_session');qmp,guest,private=session.configure(PRIMARY,'wp42')
    quit_module=importlib.import_module('macro_quit');module=inspector()
    report={'schema':'wordling.wp42.run/v1','scope':SCOPE,'run_id':args.run_id,'case':args.case,
            'plan_sha256':plan_hash(current),'preparation':current,'grant':grant,'results':[],
            'mutation_permission':False,'wordling_tested':False,'full_m1_accepted':False}
    old=signal.signal(signal.SIGALRM,session.timeout_signal)
    try:
        with session.exclusive(private):
            ledger=private/'wp42-attempts.json'
            attempts=json.loads(ledger.read_text()) if ledger.exists() else []
            require(len(attempts)+2<=MAX_ATTEMPTS,'AttemptLimit','12-attempt cap includes failures and prior plans')
            report['master_before']={n:sha(guest.MASTER/n) for n in ['boot.img','harddisk.img']}
            for repetition in [1,2]:
                row={'repetition':repetition,'outcome':'incomplete','guest_stopped':False}
                target=directory/('r'+str(repetition));target.mkdir()
                work=private/'runs'/('wp42-'+args.run_id)/target.name
                require(not work.exists() and not qmp.SOCKET.exists(),'ForeignRuntime','existing run/runtime never stopped/reused')
                attempts.append({'run_id':args.run_id,'case':args.case,'repetition':repetition,
                                 'plan_sha256':plan_hash(current),'started_at':datetime.now(timezone.utc).isoformat()})
                dump(ledger,attempts);p=None;owned=False
                try:
                    session.QMP_AUDIT_FILE=target/'qmp-wire.jsonl';owned=True
                    row['qemu_argv']=session.fresh_start(qmp,guest,work,[])
                    require(row['qemu_argv']==recipe['qemu_argv'][repetition-1],'LaunchArgv','actual launch differs from frozen argv')
                    row['settings_before']={'private_path':str(work/'settings-before.SET'),'sha256':sha(work/'settings-before.SET')}
                    signal.setitimer(signal.ITIMER_REAL,900)
                    with qmp.QMP() as q:
                        p=module.MutationProbe(q,target)
                        row['fast_save']=perform(p,recipe)
                        row['exit_actions']=quit_module.finish_original(p)
                        row['outcome']='complete-observation'
                except Exception as error:
                    row['error']=str(error)
                finally:
                    signal.setitimer(signal.ITIMER_REAL,0)
                    if owned:
                        row['stop_method']=session.stop_owned(qmp,guest)
                        row['guest_stopped']=True
                        require(not qmp.SOCKET.exists(),'LiveDisk','refuse extraction until stopped')
                        if work.exists() and (work/'harddisk.img').exists():
                            row['settings_after']=session.settings_snapshot(work,'after')
                            row['exports']=[]
                            for name,host in p.exports if p else []:
                                output=target/host
                                proc=subprocess.run(['mcopy','-i',str(work/'harddisk.img')+'@@1048576',
                                                     '::OUT/'+name,str(output)],capture_output=True,timeout=15)
                                row['exports'].append({'path':str(output.relative_to(directory)),'exit':proc.returncode,
                                    'sha256':sha(output) if output.exists() else None,
                                    'size':output.stat().st_size if output.exists() else None})
                        if p:
                            row.update(trace=p.trace,checks=p.checks,settings=p.settings,phases=getattr(p,'phases',[]))
                    report['results'].append(row)
            report['master_after']={n:sha(guest.MASTER/n) for n in ['boot.img','harddisk.img']}
            require(report['master_before']==report['master_after'],'MasterChanged','immutable master differs')
        report['oracle_released_before_offline_audit']=True
    finally:
        signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,old)
        dump(directory/'run.json',report)
    return {'run_manifest':str(directory/'run.json'),'oracle_released':report.get('oracle_released_before_offline_audit',False)}

def result(path):
    path=Path(path);data=json.loads(path.read_text())
    require(data['schema']=='wordling.wp42.run/v1' and data['scope']==SCOPE,'RunSchema','wrong run')
    current=plan()
    require(data['plan_sha256']==plan_hash(data['preparation'])==plan_hash(current),
            'SourceMismatch','run source/helper/profile plan differs')
    recipe=next(x for x in recipes() if x['id']==data['case'])
    require(data['oracle_released_before_offline_audit'] and data['master_before']==data['master_after']==current['master'],
            'Custody','oracle/master custody incomplete')
    require([r['repetition'] for r in data['results']]==[1,2],'Repetitions','two fresh runs required')
    rows=[]
    quit_module=importlib.import_module('macro_quit')
    for row in data['results']:
        require(row['outcome']=='complete-observation' and row['guest_stopped'] and
                row['stop_method']=='QMP quit; own socket terminated','NormalExit','contained/incomplete run not accepted')
        verify_actions(recipe,row)
        folder=path.parent/('r'+str(row['repetition']))
        actual_before=(folder/'fast-save-environment-before/screen.txt').read_text()
        lines=[x for x in actual_before.splitlines() if re.search(r'5[^\n]*Fast Save',x,re.I)]
        require(len(lines)==1,'FastSaveCapture','missing exact menu row')
        values=re.findall(r'\b(Yes|No)\b',lines[0],re.I)
        require(values and values[-1].lower()==row['fast_save']['before'],'FastSaveCapture','baseline observation differs from captured menu')
        if recipe['fast_save']=='disabled':
            after=(folder/'fast-save-environment-after/screen.txt').read_text()
            require(any(re.search(r'5[^\n]*Fast Save[^\n]*\bNo\b',x,re.I) for x in after.splitlines()),'FastSaveCapture','disabled No not captured')
        for action in row['exit_actions']:
            screen=(folder/action['capture']/'screen.txt').read_text()
            state=quit_module.exit_state(screen)
            require(state==action['state'],'NormalExit','exit state differs from actual capture')
            expected='f7' if state=='main' else 'n' if state=='save' else 'y' if state in ['exit-doc1','exit-doc2','exit-wp'] else None
            require(expected==action['key'],'NormalExit','exit key not justified by capture')
        require(quit_module.exit_state((folder/'clean-exit/screen.txt').read_text())=='dos',
                'NormalExit','actual captured final DOS required')
        require(all(x['passed'] for x in row['checks']),'ProbeCheck','probe check failed')
        require(row['fast_save']['requested']==recipe['fast_save'] and
                row['fast_save']['before'] in ['yes','no'] and
                (row['fast_save']['after']=='no' if recipe['fast_save']=='disabled' else
                 row['fast_save']['after']==row['fast_save']['before']), 'FastSaveScope','wrong setting observation')
        exports={Path(x['path']).name:x for x in row['exports']}
        require(set(exports)==set(recipe['native_exports']+[recipe['print_export']]),'Exports','missing/extra named export')
        observations=[]
        for name,meta in exports.items():
            require(meta['path']==str(Path('r'+str(row['repetition']))/name),'OutputPath','unexpected export path')
            p=path.parent/meta['path']
            require(meta['exit']==0 and p.is_file() and sha(p)==meta['sha256'] and p.stat().st_size==meta['size'],
                    'OutputIdentity','stopped native/stream bytes differ')
            if name.endswith('.WP5'):
                record=audit(p)
                expected=('58' if name in ['W42EDIT.WP5','W42FIN.WP5'] else '')+recipe['expected_initial_body_hex']
                require(record.get('body_hex')==expected,'BodyMismatch','actual original body differs')
                observations.append({'name':name,'audit':record})
        rows.append({'repetition':row['repetition'],'observations':observations})
    return {'status':'bounded-original-observations','rows':rows,'mutation_permission':False,
            'wordling_tested':False,'full_m1_accepted':False,
            'remaining':'field/reference/deleted/slack positive argument still requires reviewed handoff; no automatic writer admission'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    for name in ['check','plan']:
        p=sub.add_parser(name);p.add_argument('--output',type=Path)
    p=sub.add_parser('run');p.add_argument('--run-id');p.add_argument('--case',choices=[x['id'] for x in recipes()]);p.add_argument('--allow-vm',action='store_true');p.add_argument('--grant',type=Path)
    p=sub.add_parser('result');p.add_argument('manifest',type=Path);p.add_argument('--output',type=Path)
    args=parser.parse_args()
    try:
        value=check() if args.command=='check' else plan() if args.command=='plan' else run(args) if args.command=='run' else result(args.manifest)
        if getattr(args,'output',None):dump(args.output,value)
        else:print(json.dumps(value,indent=2,sort_keys=True))
    except (Refusal,OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as error:
        print(json.dumps({'status':'refused','code':getattr(error,'code',type(error).__name__),'detail':str(error),'mutation_permission':False}),file=sys.stderr)
        return 1
    return 0

if __name__=='__main__':
    sys.exit(main())
