#!/usr/bin/env python3
"""WP29 actual executable/native differential. Oracle disabled without frozen grant.

Only this owned driver/test evidence changes. Actual product and original helpers
are immutable inputs; native expectations are validators, never product emitters.
"""
import argparse
from datetime import datetime,timezone
import errno,fcntl,hashlib,json,os,pty,select,shutil,signal,struct,subprocess,sys,time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PRIMARY=Path('/home/lynn/projects/wordling')
OUT=ROOT/'docs/research/continuation/editing-differential'
APPROVED=ROOT/'docs/research/continuation/native-edits'
sys.path[:0]=[str(ROOT/'tests/compatibility/editing'),str(APPROVED)]
from terminal import Screen,TerminalFailure
import native_edits as n
import candidate_mode as cm

WP28='8916f81f0ea5dd3ff1daafb26ec239b399df7a98'
WP36='b184049a223e346588641ebf4434cc9d88f4977e'
WP23='eb86058f1cc94a9b9b84c37ad488647ec119b584'
ORACLE=OUT/'oracle-successor-01'
SUCCESSOR=OUT/'protocol-successor-01'
OLD_DRIVER='3ec527c9ef99246147294d46fbf7774ffc229f8dcd0c7b5c2be03b0d667900f1'
OLD_PLAN='b0a9fed826daa895dbb708cea69c9f04c54b4aef03f15bf8a15bbed4377b161f'
OLD_LEDGER='b73fe3405e4443c16636a3a8771699a520446760fdc6bd31275610b02c5f7303'
BASE='docs/research/continuation/native-edits/runs/'
FORTY='docs/research/continuation/code-pair-history/runs/'
BOLD='41c30cc34243c40cc444'
KEYS={'retrieve':b'\x1b[21;2~','save':b'\x1b[21~','f1':b'\x1bOP','f7':b'\x1b[18~','reveal':b'\x1b[13;3~','block':b'\x1b[14;3~','right':b'\x1b[C','left':b'\x1b[D','delete':b'\x1b[3~','backspace':b'\x7f','insert':b'\x1b[2~','enter':b'\r','escape':b'\x1b','home':b'\x1b[1~','up':b'\x1b[A'}
class Failure(ValueError):
    def __init__(self,code,detail):self.code=code;super().__init__(code+': '+detail)
def need(ok,code,detail):
    if not ok:raise Failure(code,detail)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def identity(path):
    p=Path(path);raw=p.read_bytes();return {'size':len(raw),'sha256':sha(raw)}
def write(path,value):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,indent=2)+'\n')
def stamp():return datetime.now(timezone.utc).isoformat()
def paths_go():return sorted([*ROOT.glob('internal/**/*.go'),*(ROOT/'cmd/wordling').glob('*.go'),ROOT/'go.mod',ROOT/'go.sum'])
def go_closure():
    raw=subprocess.check_output(['go','list','-deps','-json','./cmd/wordling'],cwd=ROOT,text=True);dec=json.JSONDecoder();rows=[]
    while raw.strip():
        v,end=dec.raw_decode(raw.lstrip());raw=raw.lstrip()[end:]
        if v['ImportPath'].startswith('github.com/lynncoleart/wordling/'):
            directory=Path(v['Dir']);need(directory.is_relative_to(ROOT),'ForeignGoSource',str(directory))
            rows.append({'import':v['ImportPath'],'relative_directory':str(directory.relative_to(ROOT)),'go_files':{f:identity(directory/f)for f in v['GoFiles']}})
    return rows

def pins():
    # Normal runtime re-entry composes approved36 with approved28's live UI.
    # Inspect exact immutable Git trees, including additions; never use a moving tip.
    expected={};origins={}
    for ref in [WP28,WP36]:
        subprocess.run(['git','merge-base','--is-ancestor',ref,'HEAD'],cwd=ROOT,check=True)
        for relative in subprocess.check_output(['git','ls-tree','-r','--name-only',ref],cwd=ROOT,text=True).splitlines():
            if not ((relative.startswith(('internal/','cmd/wordling/'))and relative.endswith('.go'))or relative in ['go.mod','go.sum']):continue
            raw=subprocess.check_output(['git','show',ref+':'+relative],cwd=ROOT)
            expected[relative]={'size':len(raw),'sha256':sha(raw)};origins[relative]=ref
    actual={str(p.relative_to(ROOT)):identity(p)for p in paths_go()}
    need(set(actual)==set(expected),'GoInventoryDrift',str({'added':sorted(set(actual)-set(expected)),'removed':sorted(set(expected)-set(actual))}))
    need(actual==expected,'GoSourceDrift','Actual Go/module bytes differ from approved28+36 composition')
    closure=go_closure()
    old=json.loads((ROOT/'docs/research/continuation/editable-session/actual-build-package-inputs.json').read_text())
    oldroot=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-h')
    expected_packages={row['import'] for row in old}|{'github.com/lynncoleart/wordling/internal/macro/runtime','github.com/lynncoleart/wordling/internal/macro/wpm'}
    need({row['import']for row in closure}==expected_packages,'CompilePackageDrift','Added/removed actual local package')
    compiled={}
    for item in json.loads((ROOT/'internal/editor/evidence/wp36/save-history/compiled-source-inventory.json').read_text())['files']:
        if item['kind']=='GoFiles':compiled[item['path']]=item['sha256']
    for row in old:
        directory=Path(row['directory']);need(directory.is_relative_to(oldroot),'BadApprovedPath',str(directory));relative=str(directory.relative_to(oldroot))
        if relative.startswith(('internal/input','internal/tui','cmd/wordling')):
            for f,h in row['go_files'].items():compiled[relative+'/'+f]=h
    want={relative:h for relative,h in compiled.items()if any(str(Path(relative).parent)==row['relative_directory'] for row in closure)}
    got={row['relative_directory']+'/'+f:h['sha256']for row in closure for f,h in row['go_files'].items()}
    need(got==want,'CompileClosureDrift','Added/removed/changed actual compiled local Go file')
    gomod=subprocess.check_output(['go','env','GOMOD'],cwd=ROOT,text=True).strip();need(gomod==str(ROOT/'go.mod'),'WrongGOMOD',gomod)
    scripts=[Path(__file__),ROOT/'tests/compatibility/editing/terminal.py',*sorted((ROOT/'scripts/reference').glob('*.py')),*sorted(APPROVED.glob('*.py')),*sorted(APPROVED.glob('*.json')),APPROVED/'reader_probe.go.txt']
    return {'actual_checkout':str(ROOT),'actual_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'GOMOD':gomod,'GOFLAGS':subprocess.check_output(['go','env','GOFLAGS'],cwd=ROOT,text=True).strip(),'GOWORK':subprocess.check_output(['go','env','GOWORK'],cwd=ROOT,text=True).strip(),'go_version':subprocess.check_output(['go','version'],text=True).strip(),'go_binary':identity(shutil.which('go')),'approved_composition':{'WP28':WP28,'WP36':WP36,'path_origins':origins},'product_inputs':actual,'compiled_local_packages':closure,'helper_sources':{str(p.relative_to(ROOT)):identity(p)for p in sorted(set(scripts))},'profile':identity(ROOT/'docs/research/reference-environment/environment.json'),'physical_qualified':False,'vcs_note':'Automatic Go build stamp may identify primary parent; actual cwd/GOMOD/package paths/file hashes above are the compiled-source authority, not that stamp.'}

def key(name,expect=None,label=None):return {'key':name,'label':label or name,'expect':expect or {}}
def text(value,expect=None,label=None):return {'text':value,'label':label or 'type '+value,'expect':expect or {}}
def browse(previous):return [key('f1',{'mode':'HistoryPreview'}),*[text('2',{'mode':'HistoryPreview'})for _ in range(previous)],key('f1',{'mode':'Editing'})]
def seed(reveal,target):
    return ([key('reveal')]if reveal else[])+[key('delete')]+browse(3)+[key('right')for _ in range(target)]
def block(width):return [key('block'),*[key('right')for _ in range(width)],key('backspace',{'mode':'DeleteQuestion','cue':'Delete Block? No (Yes)'}),text('y',{'mode':'Editing'})]

def recipes(word_source=None):
    rows=[
      {'id':'no-edit-two-pair','cases':['CMD51-048','CMD51-149'],'source':BASE+'wp23-b-history-follow-repair-restore-r1/N0001.WP5','reference':BASE+'wp23-b-history-follow-repair-restore-r1/P0004.PRN','body':'41c30cc3c40cc4c30cc3584243c40cc444','gap':0,'no_edit':True,'steps':[key('reveal'),key('reveal')]},
      {'id':'ascii-modes','cases':['CMD51-046'],'source':BASE+'wp23-a-modes-r1/N0000.WP5','reference':BASE+'wp23-a-modes-r1/P0005.PRN','body':'61585963','gap':3,'steps':[key('right'),key('insert',{'typeover':True}),text('X'),key('insert',{'typeover':False}),text('Y')]},
      {'id':'typeover-before-code','cases':['CMD51-047'],'source':BASE+'wp23-a-boundaries-r1/N0000.WP5','reference':BASE+'wp23-a-boundaries-r1/P0028.PRN','body':'4158c30cc34243c40cc444','gap':2,'steps':[key('right'),key('insert',{'typeover':True}),text('X'),key('insert',{'typeover':False})]},
      {'id':'normal-paired-delete','cases':['CMD51-200'],'source':FORTY+'wp40-direct-normal-delete-on-r1/N0000.WP5','reference':BASE+'wp23-b-deletions-r1/P0004.PRN','body':'41424344','gap':1,'steps':seed(False,1)+[key('delete',{'mode':'DeleteQuestion','cue':'Delete [BOLD]? No (Yes)'}),text('y',{'mode':'Editing','history_count':None})]},
      {'id':'reveal-paired-backspace','cases':['CMD51-201'],'source':FORTY+'wp40-direct-reveal-backspace-off-r1/N0000.WP5','reference':BASE+'wp23-b-deletions-r1/P0004.PRN','body':'41424344','gap':3,'steps':seed(True,5)+[key('backspace',{'mode':'Editing','history_count':None})]},
      {'id':'opening-repair','cases':['CMD51-202'],'source':BASE+'wp23-a-blocks-r1/N0000.WP5','reference':BASE+'wp23-a-blocks-r1/P0004.PRN','body':BOLD,'gap':2,'steps':[key('reveal'),key('right')]+block(1)},
      {'id':'closing-repair','cases':['CMD51-203'],'source':FORTY+'wp40-closing-block-repair-yes-r1/N0000.WP5','reference':BASE+'wp23-a-blocks-r1/P0028.PRN','body':BOLD,'gap':5,'steps':seed(True,4)+block(1)},
      {'id':'attributed-restore','cases':['CMD51-204'],'source':BASE+'wp23-a-blocks-r1/N0048.WP5','reference':BASE+'wp23-a-blocks-r1/P0004.PRN','body':BOLD,'gap':5,'steps':[key('reveal'),key('right')]+block(4)+[key('f1',{'mode':'HistoryPreview'}),text('1',{'mode':'Editing','history_qualified':False})]},
      {'id':'plain-seeded-restore','cases':['CMD51-200'],'local_scope':'Approved40 seeded plain S restoration; CMD200 applies to preceding pair deletion only, not invented three-entry CMD043 closure.','source':FORTY+'wp40-direct-normal-delete-on-r1/N0000.WP5','reference':FORTY+'wp40-direct-normal-delete-on-r1/P0004.PRN','body':'415358424344','gap':3,'steps':seed(False,1)+[key('delete'),text('y')]+browse(3)+[key('f1'),text('1')]+browse(3)+[text('X',{'history_qualified':False})]},
    ]
    steps=[]
    for i,word in enumerate(['ONE','TWO','THREE']):
        steps += [key('delete')for _ in word]
        if i<2:steps.append(key('right'))
    steps+=browse(2)+[key('right')]+[key('delete')for _ in 'FOUR']+[{'save_name':'BASE','gap':3,'body_hex':'202020'}]+browse(3)+[{'save_name':'BROWSED','gap':3,'body_hex':'202020'}]+[key('f1'),text('2'),text('2'),text('1')]
    rows.append({'id':'three-entry-eviction','cases':['CMD51-043','CMD51-211'],'source':word_source,'reference_control':'history-eviction','body':'20202054574f','gap':6,'steps':steps,'local_scope':'Three-entry preview/cancel before fourth group, fourth eviction and first Restore TWO; two original controls required for exact recipe/complete +Z stream. No later retention query.'})
    return rows

class App:
    def __init__(self,binary,folder,source):
        self.binary=Path(binary);self.folder=Path(folder);need(not self.folder.exists(),'FreshAppPath',str(folder));self.folder.mkdir(parents=True);self.files=self.folder/'files';self.files.mkdir();self.source=Path(source).read_bytes();(self.files/'ORIGIN').write_bytes(self.source)
        self.master,self.slave=pty.openpty();fcntl.ioctl(self.slave,termios_TIOCSWINSZ(),struct.pack('HHHH',32,140,0,0))
        import termios
        self.before=termios.tcgetattr(self.slave);self.screen=Screen(140,32);self.wire=bytearray();self.events=[];self.frames=[];self.stderr=b''
        argv=[str(self.binary),'-root',str(self.files.resolve()),'-profile','local-flat'];env=dict(os.environ,TERM='xterm-256color',LANG='C.UTF-8');self.argv=argv
        self.proc=subprocess.Popen(argv,stdin=self.slave,stdout=self.slave,stderr=subprocess.PIPE,env=env);self.pid_identity=proc_identity(self.proc.pid)
        try:self.collect(.5);self.capture('startup');self.send_raw(b'\x1b[?31u','synthetic enhancement response (unqualified physical delivery)')
        except Exception as e:self.close(e);raise
    def collect(self,seconds=.12):
        end=time.monotonic()+seconds
        while time.monotonic()<end:
            if select.select([self.master],[],[],.01)[0]:
                try:raw=os.read(self.master,65536)
                except OSError as error:
                    if error.errno==errno.EIO:return
                    raise
                if not raw:return
                self.wire.extend(raw);need(len(self.wire)<=4*1024*1024,'AppWireBudget','4MiB diagnostic wire limit');self.screen.feed(raw)
    def capture(self,label):
        frame=self.screen.snapshot();state=self.screen.state();item={'label':label,'event_index':len(self.events)-1,'monotonic':time.monotonic(),'state':state,'screen':frame,'wire_bytes_through':len(self.wire)};self.frames.append(item);return item
    def send_raw(self,raw,label,expect=None):
        os.write(self.master,raw);self.events.append({'label':label,'hex':raw.hex()});deadline=time.monotonic()+5;last=None
        while time.monotonic()<deadline:
            self.collect()
            try:item=self.capture(label)
            except TerminalFailure as e:last=e;continue
            expected=expect or {};state=item['state'];whole='\n'.join(item['screen']['rows'])
            if all((v in whole if k=='cue'else state.get(k)==v)for k,v in expected.items()):return item
            last=Failure('AppStateMismatch',str({'expected':expected,'actual':state}))
        raise last or Failure('AppDeadline',label)
    def step(self,step):
        raw=KEYS[step['key']]if 'key'in step else step['text'].encode('ascii');return self.send_raw(raw,step['label'],step.get('expect'))
    def retrieve(self):
        self.step(key('retrieve',{'mode':'RetrieveName'}));self.step(text('ORIGIN'));self.step(key('enter',{'mode':'Editing','name':'ORIGIN','gap':0,'dirty':False}))
    def save(self,name,gap):
        self.step(key('save',{'mode':'SaveName'}));self.step(text(name,{'cue':'Document to be saved: '+name}));self.step(key('enter',{'mode':'Editing','name':name,'gap':gap,'save':'NewNamePublished','dirty':False}));need((self.files/name).exists(),'MissingAppNative',name);return (self.files/name).read_bytes()
    def finish(self):
        self.step(key('f7',{'mode':'ExitSaveQuestion'}));self.step(key('f1',{'mode':'Editing'}));self.step(key('f7',{'mode':'ExitSaveQuestion'}));self.step(text('n',{'mode':'ExitQuestion'}))
        os.write(self.master,b'y');self.events.append({'label':'Yes actual original exit','hex':'79'});self.proc.wait(timeout=8);self.collect(.1);self.stderr=self.proc.stderr.read();need(self.proc.returncode==0,'AppExit',self.stderr.decode(errors='replace'))
        import termios
        need(termios.tcgetattr(self.slave)==self.before,'TermiosNotRestored','actual equality assertion')
    def close(self,error=None):
        if self.proc.poll()is None:
            need(proc_identity(self.proc.pid)==self.pid_identity,'AppPIDReused','Do not signal another process');self.proc.terminate()
            try:self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:self.proc.kill();self.proc.wait(timeout=5)
        if not self.stderr:self.stderr=self.proc.stderr.read()
        (self.folder/'wire-output.bin').write_bytes(self.wire);(self.folder/'stderr.txt').write_bytes(self.stderr);write(self.folder/'injected.json',self.events);write(self.folder/'frames.json',self.frames)
        write(self.folder/'process.json',{'argv':self.argv,'binary':identity(self.binary),'pid':self.proc.pid,'pid_identity':self.pid_identity,'returncode':self.proc.returncode,'error':None if error is None else str(error),'before_source':{'size':len(self.source),'sha256':sha(self.source)},'physical_qualified':False,'scope':'actual executable with synthetic Linux PTY; semantic displayed gap and terminal cursor are distinct'})
        self.proc.stderr.close();os.close(self.master);os.close(self.slave)
def termios_TIOCSWINSZ():
    import termios
    return termios.TIOCSWINSZ

def proc_identity(pid):
    p=Path('/proc')/str(pid);stat=(p/'stat').read_text();suffix=stat.rsplit(') ',1)[1].split();return {'pid':pid,'start_ticks':int(suffix[19]),'argv_hex':(p/'cmdline').read_bytes().hex()}

def prefix_check(source,candidate,no_edit=False):
    if no_edit:need(candidate==source,'NoEditMismatch','whole source bytes changed');return {'whole_no_edit_exact':True}
    a,b=n.inspect(source,True),n.inspect(candidate,True);old=int.from_bytes(source[4:8],'little');new=int.from_bytes(candidate[4:8],'little');need(old==new,'BodyOffsetChanged','prefix address must stay')
    p6=next(p for p in a['packets']if p['type']==6)['offset'];diff=[i for i,(x,y)in enumerate(zip(source[:old],candidate[:new]))if x!=y]
    need(all(i==p6 and source[i]in[0,8]and candidate[i]==8 for i in diff),'UnrelatedPrefixChanged',str(diff))
    return {'input_prefix_bytes':old,'output_prefix_bytes':new,'indexed_packet6':p6,'prefix_diff_offsets':diff,'all_other_prefix_bytes_exact':True}

def run_app(binary,folder,recipe,marker=True):
    app=None;error=None
    try:
        folder=Path(folder);need(not folder.exists(),'FreshAppPath',str(folder))
        # Per-run executing producer/decoder is archived before the real child.
        frozen=folder.parent/(folder.name+'-inputs');need(not frozen.exists(),'FreshInputArchive',str(frozen));frozen.mkdir(parents=True)
        for name,path in [('wordling_edits.py.txt',Path(__file__)),('terminal.py.txt',ROOT/'tests/compatibility/editing/terminal.py')]:shutil.copyfile(path,frozen/name)
        write(frozen/'invocation.json',{'argv':sys.argv,'function':'run_app','binary':identity(binary),'recipe':recipe,'source':identity(ROOT/recipe['source']if not Path(recipe['source']).is_absolute()else recipe['source']),'product':pins()})
        app=App(binary,folder,ROOT/recipe['source']if not Path(recipe['source']).is_absolute()else recipe['source']);app.retrieve()
        for step in recipe['steps']:
            if 'save_name'in step:
                snap=app.save(step['save_name'],step['gap']);need(n.inspect(snap,True)['body_hex']==step['body_hex'],'IntermediateNativeMismatch',step['save_name'])
            else:app.step(step)
        final=app.capture('before real SaveAs');need(final['state']['gap']==recipe['gap'],'AppGap',recipe['id'])
        candidate=app.save('CANDIDA',recipe['gap']);inspection=n.inspect(candidate,True);need(inspection['body_hex']==recipe['body'],'AppBodyMismatch',recipe['id']);prefix=prefix_check(app.source,candidate,recipe.get('no_edit',False))
        marker_result=None
        if marker:
            app.step(text('~'));witness=app.save('MARKER',recipe['gap']+1);tokens=n.body_tokens(bytes.fromhex(recipe['body']));offset=tokens[recipe['gap']]['body_offset']if recipe['gap']<len(tokens)else len(bytes.fromhex(recipe['body']));body=bytes.fromhex(recipe['body']);want=(body[:offset]+b'~'+body[offset:]).hex();need(n.inspect(witness,True)['body_hex']==want,'NativeCursorMarker','Native marker does not corroborate declared gap');marker_result={'expected_body_hex':want,'native':identity(app.files/'MARKER'),'scope':'later actual-app native cursor witness only; not an additional original-interop candidate'}
        app.finish();need((app.files/'ORIGIN').read_bytes()==app.source,'SourceModified','actual app changed loaded source');need((app.files/'CANDIDA').read_bytes()==candidate,'CandidateChanged','later marker changed first publication')
        result={'id':recipe['id'],'outcome':'app-emitted','candidate':identity(app.files/'CANDIDA'),'body_hex':recipe['body'],'declared_final_gap':recipe['gap'],'prefix':prefix,'marker':marker_result,'source':identity(app.files/'ORIGIN'),'termios_restored_assertion':True};write(Path(folder)/'result.json',result);return result
    except Exception as e:error=e;raise
    finally:
        if app:app.close(error)

def owned_process(pidfile,expected_argv):
    need(pidfile.is_file()and not pidfile.is_symlink(),'MissingOwnedPID','No positive private PID file; no stop/extraction authority')
    try:
        with pidfile.open('rb') as stream:raw=stream.read(33)
        need(0<len(raw)<=32,'InvalidPIDFile','Bounded positive decimal PID required');pid=int(raw.strip())
    except (ValueError,OSError)as e:raise Failure('MissingOwnedPID',str(e))from e
    need(pid>0,'MissingOwnedPID','PID must be positive');observed=proc_identity(pid)
    need(bytes.fromhex(observed['argv_hex']).split(b'\0')[:-1]==[os.fsencode(x)for x in expected_argv],'ForeignGuestArgv','Actual PID argv differs from exact fresh private launch')
    return observed

def read_process(pid):
    try:
        p=Path('/proc')/str(pid);stat=(p/'stat').read_text();state=stat.rsplit(') ',1)[1].split()[0];return proc_identity(pid)|{'state':state}
    except FileNotFoundError:return None

def wait_owned_stop(owned,socket,timeout=10,read=read_process,clock=time.monotonic,pause=time.sleep):
    need(isinstance(owned,dict)and isinstance(owned.get('pid'),int)and owned['pid']>0 and owned.get('start_ticks',0)>0 and bool(owned.get('argv_hex')),'MissingOwnedPID','Socket absence alone never proves termination')
    deadline=clock()+timeout;observations=[]
    while True:
        current=read(owned['pid']);present=socket.exists();now=clock()
        if current is not None:
            need(all(current.get(k)==owned[k]for k in ['pid','start_ticks'])and(not current.get('argv_hex')or current['argv_hex']==owned['argv_hex']),'PIDIdentityChanged','PID reused/rebound; do not signal or extract')
        observations.append({'monotonic':now,'socket_exists':present,'process':current})
        if not present and (current is None or current['state']=='Z'):
            return {'confirmed':True,'positive_owned_identity':owned,'observations':observations,'reason':'owned PID absent/zombie AND own socket absent after bounded completion poll'}
        need(now<deadline,'StopDeadline','Known owned guest not confirmed stopped; no extraction or next attempt')
        pause(min(.05,max(0,deadline-now)))

def candidate_metadata(folder,recipe,app_result):
    candidate=folder/'files/CANDIDA';data=candidate.read_bytes()
    provenance={'rights':'project-authored scratch','producer':'actual cmd/wordling Linux PTY; pinned approved28 compiled source, original16 keys, actual41 candidate publication','source_sha256':sha(data),'description':recipe['id']+' actual app-emitted existing-document edit/no-edit output; not a serializer helper','loaded_source':recipe['source'],'loaded_source_identity':identity(folder/'files/ORIGIN'),'app_result_path':str(folder/'result.json'),'app_argv':json.loads((folder/'process.json').read_text())['argv'],'binary':json.loads((folder/'process.json').read_text())['binary'],'final_gap_corrobated_by_later_native_marker':app_result['marker']}
    expected={'schema_version':1,'candidate_sha256':sha(data),'input_body_hex':recipe['body'],'subsequent_edit':{'command':'append-ascii-at-end','text':'Z','expected_body_hex':recipe['body']+'5a'},'environment_sha256':identity(ROOT/'docs/research/reference-environment/environment.json')['sha256']}
    if recipe.get('reference'):
        ref=ROOT/recipe['reference'];expected['reference_print']={'path':str(ref),'size':ref.stat().st_size,'sha256':identity(ref)['sha256']}
    else:expected['reference_control_required']={'case':'history-eviction','fresh_repetitions':2,'required_stream_equality':'whole raw bytes, no tolerances; seal only after both controls and before candidate run','expected_original_edited_body_hex':recipe['body']+'5a'}
    write(folder/'provenance.json',provenance);write(folder/'expectations.json',expected)
    return {'id':recipe['id'],'folder':str(folder.relative_to(ROOT)),'cases':recipe['cases'],'source':recipe['source'],'candidate':identity(candidate),'body_hex':recipe['body'],'gap':recipe['gap'],'reference':recipe.get('reference'),'reference_control':recipe.get('reference_control'),'provenance':identity(folder/'provenance.json'),'expectations':identity(folder/'expectations.json')}

def prepare(name):
    need(Path.cwd()==ROOT,'WrongCheckout','Run from assigned actual checkout')
    need(name.replace('-','').isalnum()and len(name)<48,'BadIdentity','Safe fresh preparation identity required')
    target=OUT/'preparations'/name;need(not target.exists(),'FreshPreparation','Do not overwrite any attempt');target.mkdir(parents=True)
    pin=pins();write(target/'inputs.json',pin)
    for relative in [*pin['helper_sources'],*pin['product_inputs']]:
        src=ROOT/relative;dest=target/'source'/relative
        if dest.suffix=='.go':dest=dest.with_name(dest.name+'.txt')
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
    import tempfile
    binary=Path(tempfile.mkdtemp(prefix='wordling-wp29-build-'))/'wordling'
    build=['go','build','-o',str(binary),'./cmd/wordling'];p=subprocess.run(build,cwd=ROOT,capture_output=True);(target/'build.stdout').write_bytes(p.stdout);(target/'build.stderr').write_bytes(p.stderr);need(p.returncode==0,'BuildFailed','Actual app build failed')
    verify=subprocess.run(['go','mod','verify'],cwd=ROOT,capture_output=True);(target/'module-verify.txt').write_bytes(verify.stdout+verify.stderr);need(verify.returncode==0,'ModuleCacheDrift','Actual cached dependencies differ')
    (target/'binary-buildinfo.txt').write_bytes(subprocess.check_output(['go','version','-m',str(binary)]));write(target/'build.json',{'argv':build,'binary_path':str(binary),'binary':identity(binary),'actual_source':pin,'stamp_is_not_compiled_commit':True})
    words=[]
    builder={'id':'word-source-builder','source':BASE+'wp23-a-modes-r1/N0000.WP5','body':b'ONE TWO THREE FOUR'.hex(),'gap':18,'steps':[key('insert'),text('ONE TWO THREE FOUR'),key('insert')]}
    for repeat in [1,2]:
        folder=target/('word-source-r'+str(repeat));run_app(binary,folder,builder,marker=False);words.append(folder/'files/CANDIDA')
    need(words[0].read_bytes()==words[1].read_bytes(),'WordSetupMismatch','Two independent sourced app fixture publications differ')
    rows=[];rs=recipes(str(words[0]));write(target/'recipes.json',rs)
    for recipe in rs:
        pair=[]
        for repeat in [1,2]:
            folder=target/(recipe['id']+'-r'+str(repeat));result=run_app(binary,folder,recipe);record=candidate_metadata(folder,recipe,result);record['repeat']=repeat;rows.append(record);pair.append(folder/'files/CANDIDA')
        need(pair[0].read_bytes()==pair[1].read_bytes(),'FreshAppPairMismatch',recipe['id'])
    unique=[]
    for row in rows:
        data=(ROOT/row['folder']/'files/CANDIDA').read_bytes();found=None
        for other in unique:
            od=(ROOT/other['folder']/'files/CANDIDA').read_bytes()
            if data==od and row['candidate']==other['candidate']:found=other;break
        row['whole_byte_alias_of']=(found or row)['id']
        if found is None:unique.append(row)
    need(all(row['reference_control']is None or row['id']=='three-entry-eviction'for row in unique),'UnplannedControl','Only finite history control may be pending')
    leaves=[{'id':'history-control-r'+str(r),'kind':'control','case':'history-eviction','repeat':r}for r in [1,2]]
    leaves += [{'id':c['id']+'-r'+str(r),'kind':'candidate','case':c['id'],'repeat':r,'folder':c['folder']}for c in unique for r in [1,2]]
    plan={'schema':'wordling.wp29.plan/v1','status':'offline app emitted; NO oracle grant or original execution','product':pin,'binary':identity(binary),'binary_path':str(binary),'preparation':str(target.relative_to(ROOT)),'source_builder':'actual sourced WP28 app publication, then separate fresh process; no new-document constructor or synthetic native source','cases':rows,'unique_whole_native_classes':unique,'original_leaves':leaves,'original_guest_cap_including_failures':len(leaves),'fresh_repetitions':2,'failure_policy':'sticky halt ENTIRE grant at first failure/incomplete/unknown/provenance/PID/stop/export/comparison; no retry or next leaf','marker_outputs':'actual app native cursor witnesses, not additional original-qualified candidates','reference_controls':'Both actual original history-control complete streams must match strictly and be sealed before any candidate; no expectation repair','shared_runtime':'primary research/cache/reference/runtime/wp29/qmp.sock','shared_lock':'primary research/cache/reference/session1.lock','physically_qualified':False,'full_m1_accepted':False}
    write(target/'plan.json',plan);write(OUT/'selected-preparation.json',{'path':str(target.relative_to(ROOT)),'plan':identity(target/'plan.json')})
    print(json.dumps({'preparation':str(target),'plan':identity(target/'plan.json'),'app_recipes':len(rs),'whole_native_classes':len(unique),'guest_cap':len(leaves),'oracle_launched':False}))
    return plan

def selected():
    sel=json.loads((OUT/'selected-preparation.json').read_text());target=ROOT/sel['path'];need(identity(target/'plan.json')==sel['plan'],'PlanChanged','Selected plan bytes changed');return target,json.loads((target/'plan.json').read_text())

def check_emission():
    target,plan=selected();current=pins();original=plan['product']
    for field in ['product_inputs','compiled_local_packages','profile','go_binary','go_version','GOMOD','GOFLAGS','GOWORK']:need(current[field]==original[field],'FrozenInputDrift',field)
    need(identity(target/'plan.json')['sha256']==OLD_PLAN,'EmissionPlanChanged','Original app/control plan remains immutable')
    old=dict(original['helper_sources']);now=dict(current['helper_sources']);driver='scripts/reference/wordling_edits.py'
    need(old.pop(driver)['sha256']==OLD_DRIVER and identity(SUCCESSOR/'predecessor-driver.py.txt')['sha256']==OLD_DRIVER,'HistoricalDriverChanged','Explicit predecessor source custody')
    now.pop(driver);need(now==old,'FrozenHelperDrift','Only this owned protocol driver may change')
    binary=Path(plan['binary_path']);need(identity(binary)==plan['binary'],'BinaryChanged','Actual frozen app binary differs')
    for row in plan['cases']:
        folder=ROOT/row['folder'];need(identity(folder/'files/CANDIDA')==row['candidate'],'AppCandidateChanged',row['id']);need(identity(folder/'provenance.json')==row['provenance']and identity(folder/'expectations.json')==row['expectations'],'AppMetadataChanged',row['id'])
        alias=next(c for c in plan['unique_whole_native_classes']if c['id']==row['whole_byte_alias_of']);need((folder/'files/CANDIDA').read_bytes()==(ROOT/alias['folder']/'files/CANDIDA').read_bytes(),'WholeNativeAliasMismatch',row['id'])
        if row['reference']:cm.prepare(folder/'files/CANDIDA',folder/'provenance.json',folder/'expectations.json')
    return target,plan

def regular_exact(path,expected,code):
    import stat
    path=Path(path)
    need(path.exists()and not path.is_symlink()and stat.S_ISREG(path.stat().st_mode),'MissingComparisonInput',str(path))
    need(path.stat().st_size==expected['size']and identity(path)==expected,code,str(path))

def approved_config():
    result={}
    for name in ['field-ledger.json','reader_probe.go.txt']:
        relative=str((APPROVED/name).relative_to(ROOT));raw=subprocess.check_output(['git','show',WP23+':'+relative],cwd=ROOT)
        need((APPROVED/name).read_bytes()==raw,'ApprovedConfigurationChanged',name)
        result[name]=raw
    need(len(result['field-ledger.json'])==31234 and sha(result['field-ledger.json'])=='b34180f9bbec1bc7c6a4bd4c4bee4a19d774f46d71df53e2841b615b4fa5a834','ApprovedLedgerChanged','Immutable approved23 schema')
    return result

def comparison_preflight(configuration,product):
    """No guest/attempt allocation. Strict static transitive lookup validation."""
    import final_state,classify_reader
    configuration=Path(configuration);known=approved_config()
    for name,path in [('field-ledger.json',configuration/'field-ledger.json'),('reader_probe.go.txt',configuration/'reader/reader_probe.go.txt')]:
        regular_exact(path,{'size':len(known[name]),'sha256':sha(known[name])},'ChangedComparisonInput')
    need(final_state.HERE==APPROVED and final_state.ROOT==ROOT and cm.HERE==APPROVED and cm.ROOT==ROOT and classify_reader.ROOT==ROOT,'WrongComparisonRoot','Original helper roots must stay exact')
    golden_path=APPROVED/'final-state-golden.json';expected=product['helper_sources'][str(golden_path.relative_to(ROOT))];regular_exact(golden_path,expected,'ChangedFinalGolden')
    golden=json.loads(golden_path.read_text())
    for name,row in golden['files'].items():
        regular_exact(ROOT/row['path'],{k:row[k]for k in ['size','sha256']},'ChangedFinalGoldenSource')
    for path in [ROOT/'docs/research/reference-environment/environment.json',PRIMARY/'docs/research/reference-environment/environment.json']:
        regular_exact(path,product['profile'],'ChangedProfile')
    # Reader imports internal/wp51: writable scratch must be inside this module.
    need(configuration.resolve().is_relative_to(ROOT)and(configuration/'reader').resolve().is_relative_to(ROOT),'ReaderOutsideModule','Use owned in-module scratch')
    import tempfile
    with tempfile.TemporaryDirectory(prefix='reader-preflight-',dir=configuration/'reader')as folder:
        witness=Path(folder)/'write-test';witness.write_bytes(b'project-owned preflight');need(witness.read_bytes()==b'project-owned preflight','ReaderNotWritable','No guest before actual reader scratch is usable')
    return {'ledger':identity(configuration/'field-ledger.json'),'reader':identity(configuration/'reader/reader_probe.go.txt'),'exact_golden_sources':golden['files']}

def predecessor_receipt():
    paths=[OUT/'oracle/ledger.json',OUT/'oracle-fault-01/root-grant.json',OUT/'oracle/history-control-seal.json',OUT/'oracle-fault-01/artifact-manifest.json']
    need(identity(paths[0])['sha256']==OLD_LEDGER,'PredecessorLedgerChanged','Historical failed3 ledger stays exact')
    ledger=json.loads(paths[0].read_text());grant=json.loads(paths[1].read_text())
    need(ledger['halted']is True and len(ledger['attempts'])==3 and [a['outcome']for a in ledger['attempts']]==['accepted','accepted','incomplete-or-failed'],'BadPredecessorAccounting','Two controls, one incomplete, no retroacceptance')
    need(grant['plan_sha256']==OLD_PLAN and grant['runner_sha256']==OLD_DRIVER and ledger['grant_sha256']==identity(paths[1])['sha256'],'PredecessorGrantChanged','Original source/plan/grant identity')
    for r in json.loads(paths[3].read_text())['records']:regular_exact(ROOT/r['path'],{k:r[k]for k in ['size','sha256']},'PredecessorRawChanged')
    streams=[]
    for repeat in [1,2]:
        d=OUT/'oracle/runs'/('wp29-history-control-r'+str(repeat));run=json.loads((d/'run.json').read_text());result=control_compare(d,run);streams.append(Path(result['reference_print']['path']))
        paths +=[d/'run.json',d/'comparison.json',d/'leaf-complete.json',d/'oracle-slot-release.json']
    need(streams[0].read_bytes()==streams[1].read_bytes(),'PredecessorControlMismatch','Exact two observed streams required')
    seal=json.loads((OUT/'oracle/history-control-seal.json').read_text())
    need(seal['plan_sha256']==OLD_PLAN and seal['strict_whole_raw_equality']is True and all(identity(Path(row['path']))=={k:row[k]for k in ['size','sha256']}for row in seal['both_streams']),'PredecessorControlSealChanged','Original controls remain original, never relabeled successor runs')
    return {'prior_spent_attempts':3,'qualified_control_count':2,'candidate_incomplete_count':1,'old_ledger_halted':True,'old_grant_max_attempts':18,'maximum_new_attempts':16,'cumulative_cap':19,'custody':{str(p.relative_to(ROOT)):identity(p)for p in paths},'control_streams':[{'path':str(p),'identity':identity(p)}for p in streams],'no_retroacceptance':True}

def host_preflight(product):
    import importlib.metadata
    profile=json.loads((PRIMARY/'docs/research/reference-environment/environment.json').read_text());private=PRIMARY/'research/cache/reference';files=[(private/'master/boot.img',profile['master_boot_sha256']),(private/'master/harddisk.img',profile['master_disk_sha256']),(Path(profile['qemu_binary']['path']),profile['qemu_binary']['sha256'])]
    files +=[(Path(row['path']),row['sha256'])for row in profile['firmware']]
    for p,h in files:need(p.is_file()and identity(p)['sha256']==h,'PrivateHostIdentityChanged',str(p))
    tools={}
    for name in ['mformat','mcopy','mtype','qemu-system-i386']:
        p=shutil.which(name);need(p,'MissingHostTool',name);tools[name]={'path':p,**identity(p)}
    return {'tools':tools,'Pillow':importlib.metadata.version('Pillow'),'master_hashes':{p.name:h for p,h in files[:2]},'profile':identity(PRIMARY/'docs/research/reference-environment/environment.json')}

def successor_shape(plan):
    want=[{'id':c['id']+'-r'+str(r),'kind':'candidate','case':c['id'],'repeat':r,'folder':c['folder']}for c in plan['unique_whole_native_classes']for r in [1,2]]
    need(plan['original_leaves']==want and len(want)==16 and plan['original_guest_cap_including_failures']==16 and plan['prior_spent_attempts']==3 and plan['cumulative_cap']==19,'SuccessorAccounting','Exactly16 fresh candidates plus3 historical spent, no reset/retry allowance')
    need(plan['oracle_root']==str(ORACLE.relative_to(ROOT)),'WrongSuccessorNamespace','Never replace historical directories or ledger')

def consume_successor(ledger,grant_sha,plan,leaf,argv):
    successor_shape(plan)
    need(ledger.get('prior_spent_attempts')==3 and ledger.get('cumulative_cap')==19 and ledger.get('predecessor')==plan['predecessor'],'PredecessorAccountingChanged','Old3 remain counted and byte-bound')
    need(all(a.get('outcome')=='accepted'and a['leaf']==plan['original_leaves'][i]for i,a in enumerate(ledger['attempts'])),'PriorSuccessorFault','No retry, out-of-order/duplicate or previous incomplete leaf')
    return consume_leaf(ledger,grant_sha,plan,leaf,argv)

def reader_preflight(configuration):
    import classify_reader,tempfile
    old=classify_reader.HERE
    try:
        classify_reader.HERE=configuration/'reader'
        with tempfile.TemporaryDirectory(prefix='native-preflight-',dir=configuration/'reader')as folder:
            malformed=Path(folder)/'malformed.WP5';malformed.write_bytes(b'not native')
            source=ROOT/(BASE+'wp23-a-modes-r1/N0000.WP5')
            result=classify_reader.classify([source,malformed])
            need(result['files'][0]['accepted']and result['files'][0]['exact_no_edit_export']and not result['files'][1]['accepted'],'ActualReaderPreflightFailed','Known native must reopen losslessly, malformed framing must refuse')
            return result
    finally:classify_reader.HERE=old

def check_plan():
    pointer=OUT/'selected-successor.json';need(pointer.is_file(),'SuccessorNotSealed','Old grant permanently halted; stage/review a separately frozen successor')
    selection=json.loads(pointer.read_text());target=ROOT/selection['path'];regular_exact(target/'plan.json',selection['plan'],'SuccessorPlanChanged');plan=json.loads((target/'plan.json').read_text())
    _,emission=check_emission();current=pins();successor_shape(plan)
    for field in ['product_inputs','compiled_local_packages','helper_sources','profile','go_binary','go_version','GOMOD','GOFLAGS','GOWORK']:need(current[field]==plan['product'][field],'FrozenSuccessorInputDrift',field)
    need(plan['emission_plan']==identity(ROOT/emission['preparation']/'plan.json')and plan['cases']==emission['cases']and plan['unique_whole_native_classes']==emission['unique_whole_native_classes']and plan['binary']==emission['binary']and plan['emission_product']==emission['product'],'SuccessorSemanticChange','No product/candidate/expectation/recipe changes')
    need(predecessor_receipt()==plan['predecessor'],'PredecessorChanged','Original custody/control source facts must stay exact before each new leaf')
    comparison_preflight(ORACLE,plan['product']);need(host_preflight(plan['product'])==plan['host'],'ChangedHostConfiguration','No tool/master/profile changes')
    regular_exact(target/'recipes.json',identity(ROOT/emission['preparation']/'recipes.json'),'RecipeCopyChanged')
    for c in plan['unique_whole_native_classes']:prepared_candidate(c)
    n.OUT=ORACLE
    return target,plan

def prepare_successor():
    need(not(OUT/'selected-successor.json').exists(),'SuccessorAlreadySealed','Do not overwrite protocol/source/expectations')
    _,emission=check_emission();product=pins();predecessor=predecessor_receipt()
    need(identity(SUCCESSOR/'independent-diagnosis.md')['sha256']=='56557b7507ebd5f01457c08ba149aa4fd84a7e5403379f25a6a34a2ed0f20fa5','DiagnosisChanged','Exact independent report, no rewriting')
    known=approved_config()
    for name,destination in [('field-ledger.json',ORACLE/'field-ledger.json'),('reader_probe.go.txt',ORACLE/'reader/reader_probe.go.txt')]:
        need(not destination.exists(),'ExistingConfiguration','Fresh owned protocol staging only');destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(known[name])
    configuration=comparison_preflight(ORACLE,product);host=host_preflight(product)
    write(SUCCESSOR/'actual-reader-preflight.json',reader_preflight(ORACLE))
    shutil.copyfile(ROOT/emission['preparation']/'recipes.json',SUCCESSOR/'recipes.json')
    leaves=[{'id':c['id']+'-r'+str(r),'kind':'candidate','case':c['id'],'repeat':r,'folder':c['folder']}for c in emission['unique_whole_native_classes']for r in [1,2]]
    plan={**emission,'schema':'wordling.wp29.successor-plan/v1','status':'offline configuration correction; NO successor VM grant','product':product,'preparation':str(SUCCESSOR.relative_to(ROOT)),'emission_preparation':emission['preparation'],'emission_product':emission['product'],'emission_plan':identity(ROOT/emission['preparation']/'plan.json'),'predecessor':predecessor,'configuration':configuration,'host':host,'original_leaves':leaves,'original_guest_cap_including_failures':16,'prior_spent_attempts':3,'cumulative_cap':19,'fresh_repetitions':2,'oracle_root':str(ORACLE.relative_to(ROOT)),'root_offline_ack':'Explicit root authorized16 fresh candidates only, prior2 qualified controls as immutable predecessor inputs, cumulative19=old3spent+new16. NO VM until separately sealed/reviewed root grant.','reference_controls':'Already qualified original first-grant controls; original commands/profile/master/helper/reference bytes remain exact and revalidated before every leaf; never relabeled new executions.'}
    for row in emission['unique_whole_native_classes']:prepared_candidate(row)
    write(SUCCESSOR/'plan.json',plan);write(OUT/'selected-successor.json',{'path':str(SUCCESSOR.relative_to(ROOT)),'plan':identity(SUCCESSOR/'plan.json')})
    write(SUCCESSOR/'transition-receipt.json',{'historical_driver':identity(SUCCESSOR/'predecessor-driver.py.txt'),'new_driver':identity(Path(__file__)),'old_plan':plan['emission_plan'],'predecessor':predecessor,'successor_plan':identity(SUCCESSOR/'plan.json'),'root_offline_ack':plan['root_offline_ack'],'old_candidate_incomplete':True,'no_original_started':True,'expected_semantic_change':False,'only_correction':'Exact approved ledger/reader config staged before launch, strict transitive preflight, fresh namespace/accounting/immutable predecessor controls'})
    print(json.dumps({'successor_plan':identity(SUCCESSOR/'plan.json'),'new_attempts':16,'historical_spent':3,'cumulative_cap':19,'original_started':False}))


def control_recipe(p):
    p.type('ONE TWO THREE FOUR');p.capture('control-words-typed-no-invented-native-presave');p.key('home,home,home,up');p.capture('control-before-deletions');history=[]
    for i,word in enumerate(['ONE','TWO','THREE']):
        p.key(','.join(['delete']*len(word)));p.capture('control-deleted-'+word)
        if i<2:p.key('right')
    h=n.browse(p,'control-three-before-fourth',previous=2);need([s.rstrip()for s in h['preview_first_lines']]==['  THREE FOUR','  TWO FOUR','  ONE FOUR'],'ControlPreviewMismatch','Exact pre-fourth preview differs');history.append(h)
    p.key('right');p.key(','.join(['delete']*4));p.capture('control-fourth-deleted');base=p.snapshot('control-base-before-preview')
    h=n.browse(p,'control-after-fourth',previous=3);need([s.rstrip()for s in h['preview_first_lines']]==['   FOUR','   THREE','   TWO','   FOUR'],'ControlEvictionMismatch','Exact fourth/Previous cycle differs');history.append(h);browsed=p.snapshot('control-browsed-noedit')
    p.key('f1');p.capture('control-reopened-newest');p.key('2,2');p.capture('control-restore-choice-TWO');p.key('1');p.capture('control-restored-TWO-before-save')
    final=p.snapshot('control-restored-native');interop=p.interop(final,'control-final')
    p.cases.append({'id':'history-eviction-control','canonical_leads':['CMD51-043','CMD51-211'],'scope':'new finite exact four-word recipe control; no original predelete native hash exists','typed_source':'ONE TWO THREE FOUR','history':history,'base':base,'browsed':browsed,'final':final,'interop':interop,'expected_final_body_hex':'20202054574f','expected_edited_body_hex':'20202054574f5a'})

def control_compare(directory,run):
    validate_owned_run(directory,run)
    import final_state
    need(run.get('result')=='observed'and run.get('clean_exit')and run.get('master_unchanged')and run.get('guest_stopped'),'IncompleteControl','Original control protocol incomplete')
    c=run['cases'][0];need(c['id']=='history-eviction-control'and c['canonical_leads']==['CMD51-043','CMD51-211'],'WrongControlCase','Control semantic association changed')
    final_state.require_final_state(directory)
    for entry in run['artifacts']:
        path=directory/entry['path'];need(path.is_file()and path.stat().st_size==entry['size']and identity(path)['sha256']==entry['sha256'],'ControlArtifactChanged',entry['path'])
    for key,body in [('base','202020'),('browsed','202020'),('final','20202054574f'),('retrieved','20202054574f'),('edited','20202054574f5a'),('after_print','20202054574f5a')]:
        name=c[key]if key in ['base','browsed','final']else c['interop'][key];need(n.inspect((directory/name).read_bytes(),False)['body_hex']==body,'ControlNativeMismatch',key)
    stream=directory/c['interop']['print_stream'];need(stream.is_file()and stream.stat().st_size>0,'MissingControlPrint','Complete raw stream required')
    job=directory/('settings-print-'+stream.stem+'-job-status')/'screen.txt';need(all(x in job.read_text()for x in ['Job Number: None','No print jobs','Additional Jobs Not Shown: 0']),'ControlPrintIncomplete','No actual empty-job capture')
    return {'accepted':True,'reference_print':{'path':str(stream),'size':stream.stat().st_size,'sha256':identity(stream)['sha256']},'full_m1_accepted':False,'scope':'actual original finite control; no Wordling process was launched in this stage'}

def seal_controls(plan):
    pairs=[]
    for repeat in [1,2]:
        d=OUT/'oracle/runs'/('wp29-history-control-r'+str(repeat));r=json.loads((d/'run.json').read_text());result=control_compare(d,r);pairs.append(result['reference_print'])
    a,b=[Path(x['path']).read_bytes()for x in pairs];need(a==b,'ControlStreamMismatch','Two complete original streams differ; no tolerance/expectation repair allowed')
    seal={'control':'history-eviction','plan_sha256':identity(ROOT/plan['preparation']/'plan.json')['sha256'],'observed_at':stamp(),'reference_print':pairs[0],'both_streams':pairs,'strict_whole_raw_equality':True,'must_precede_candidate_runs':True}
    path=OUT/'oracle/history-control-seal.json';need(not path.exists(),'ExistingControlSeal','Do not replace control observations');write(path,seal);return seal

def prepared_candidate(row):
    folder=ROOT/row['folder']
    if row['reference']:return cm.prepare(folder/'files/CANDIDA',folder/'provenance.json',folder/'expectations.json')
    seal=json.loads((OUT/'oracle/history-control-seal.json').read_text());expect=json.loads((folder/'expectations.json').read_text());need(expect.pop('reference_control_required')['case']==seal['control'],'WrongControlSeal','Conditional control is not this candidate');expect['reference_print']=seal['reference_print']
    bound=ORACLE/'expectations'/('bound-'+row['id']+'.json')
    if bound.exists():need(json.loads(bound.read_text())==expect,'BoundExpectationChanged','Never replace a materialized input')
    else:write(bound,expect)
    return cm.prepare(folder/'files/CANDIDA',folder/'provenance.json',bound)

def consume_leaf(ledger,grant_sha,plan,leaf,argv):
    # Pure admission: failed/start-incomplete attempts remain sticky and count.
    result=json.loads(json.dumps(ledger))
    need(result['grant_sha256']==grant_sha and not result['halted'],'GrantHalted','No automatic retry/new grant substitution')
    index=len(result['attempts']);need(index<plan['original_guest_cap_including_failures']and plan['original_leaves'][index]==leaf,'LeafOrder','No retries/skips/out-of-order leaves')
    attempt={'leaf':leaf,'started_at':stamp(),'outcome':'started','argv':argv};result['attempts'].append(attempt);result['halted']=True
    return result,attempt

def persist_fault(ledger_path,ledger,attempt,error,holder):
    attempt.update(outcome='incomplete-or-failed',error=str(error),failed_at=stamp(),owned_pid=holder.get('owned_pid'),stop=holder.get('stop'))
    ledger['halted']=True;write(ledger_path,ledger)

def run_oracle(args):
    from contextlib import nullcontext
    need(args.allow_vm and args.grant,'AuthorizationRequired','No oracle without explicit root grant')
    target,plan=check_plan();grant_path=Path(args.grant);grant=json.loads(grant_path.read_text());required={'schema','plan_sha256','runner_sha256','source_commit','leaf_ids','max_attempts','authorization_note'}
    need(set(grant)==required and grant['schema']=='wordling.wp29.grant/v2','GrantShape','Root grant must bind exact finite plan/runner/commit/leaves/cap')
    need(grant['plan_sha256']==identity(target/'plan.json')['sha256']and grant['runner_sha256']==identity(Path(__file__))['sha256']and grant['leaf_ids']==[x['id']for x in plan['original_leaves']]and grant['max_attempts']==plan['original_guest_cap_including_failures']and bool(grant['authorization_note'].strip()),'GrantMismatch','Wrong source/plan/order/cap')
    subprocess.run(['git','merge-base','--is-ancestor',grant['source_commit'],'HEAD'],cwd=ROOT,check=True)
    for path,ident in plan['product']['helper_sources'].items():need(sha(subprocess.check_output(['git','show',grant['source_commit']+':'+path],cwd=ROOT))==ident['sha256'],'UncommittedExecutingSource',path)
    leaf=next((x for x in plan['original_leaves']if x['id']==args.leaf),None);need(leaf is not None,'UnknownLeaf','No guest outside frozen enumeration')
    import macro_session as session,macro_quit as quit_probe,classify_reader
    q,g,private=session.configure(PRIMARY,'wp29');n.PRIVATE=private;n.PROFILE=PRIMARY/'docs/research/reference-environment/environment.json';n.OUT=ORACLE;n.configure=lambda:None
    need(identity(n.PROFILE)==plan['product']['profile'],'ProfileChanged','Private primary profile differs')
    ledger_path=n.OUT/'ledger.json';directory=n.OUT/'runs'/('wp29-s01-'+leaf['id']);work=private/'native-edit-runs'/('wp29-s01-'+leaf['id'])
    with (private/'session1.lock').open('a') as shared_lock:
        fcntl.flock(shared_lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        ledger=json.loads(ledger_path.read_text())if ledger_path.exists()else{'grant_sha256':identity(grant_path)['sha256'],'attempts':[],'halted':False,'predecessor':plan['predecessor'],'prior_spent_attempts':3,'cumulative_cap':19}
        ledger,attempt=consume_successor(ledger,identity(grant_path)['sha256'],plan,leaf,sys.argv)
        write(ledger_path,ledger) # sticky BEFORE any guest operation; no automatic retry
        need(not directory.exists()and not work.exists()and not q.SOCKET.exists(),'ExistingGuestOrRun','Never stop/reuse another or earlier guest')
        original_start,original_stop=g.start,g.stop;original_class=n.MutationProbe;holder={};report=None
        class OwnedProbe(original_class):
            def snapshot(self,label):
                name=super().snapshot(label);full='C:\\OUT\\'+Path(name).stem
                self.q.wait_until(lambda s:full in s and 'Saving'not in s and 'Document to be saved:'not in s,'actual completed original native SaveAs',timeout=20);self.capture(label+'-save-complete');return name
            def clear(self):
                self.capture('interop-clear-before');self.key('f7');self.q.wait_until(lambda s:quit_probe.exit_state(s)in ['save','exit-wp'],'captured interop clear question');screen=self.capture('interop-clear-question')
                if quit_probe.exit_state(screen)=='save':self.key('n');self.q.wait_until(lambda s:quit_probe.exit_state(s)=='exit-wp','captured Exit WP');screen=self.capture('interop-clear-exit-question')
                need(quit_probe.exit_state(screen)=='exit-wp','UnknownClear','No blind No');self.key('n');self.q.wait_until(lambda s:s.splitlines()[0]==''and 'Doc 1'in s,'blank original document after observed clear');self.capture('interop-clear-blank')
        def start(path):
            argv=g.arguments(path/'boot.img',path/'harddisk.img');holder['expected_argv']=argv;session.QMP_AUDIT_FILE=directory/'qmp-wire.jsonl'
            need(not (q.RUNTIME/'qemu.pid').exists(),'StalePIDFile','No unknown PID reuse')
            write(directory/'owned-prelaunch.json',{'root_grant':grant,'exact_qemu_argv':argv,'actual_leaf_argv':sys.argv,'frozen_product':plan['product'],'private_fresh_work':str(path),'logical_reference_reservation':'WP29 root grant; actual primary session1.lock held through stop/extraction'})
            for source in [*sorted(APPROVED.glob('*.py')),*sorted(APPROVED.glob('*.json')),APPROVED/'reader_probe.go.txt']:
                archive=directory/'approved-helper-inputs'/source.name;archive.parent.mkdir(exist_ok=True);shutil.copyfile(source,archive)
            for source in [ORACLE/'field-ledger.json',ORACLE/'reader/reader_probe.go.txt']:
                archive=directory/'comparison-configuration'/source.name;archive.parent.mkdir(exist_ok=True);shutil.copyfile(source,archive)
            attempt['guest_start_requested_at']=stamp();write(ledger_path,ledger)
            result=original_start(path);holder['owned_pid']=owned_process(q.RUNTIME/'qemu.pid',argv);write(directory/'owned-pid.json',holder['owned_pid']);return result
        def stop():
            if 'owned_pid'not in holder:holder['owned_pid']=owned_process(q.RUNTIME/'qemu.pid',holder['expected_argv'])
            current=read_process(holder['owned_pid']['pid']);need(current is not None and all(current.get(k)==holder['owned_pid'][k]for k in ['pid','start_ticks','argv_hex']),'UnexpectedGuestIdentity','No stop command without positive current ownership')
            original_stop();holder['stop']=wait_owned_stop(holder['owned_pid'],q.SOCKET);write(directory/'owned-stop.json',holder['stop'])
        def finish(p):holder['exit_actions']=quit_probe.finish_original(p);return holder['exit_actions']
        try:
            n.MutationProbe=OwnedProbe;n.clean_exit=finish;n.exclusive=lambda:nullcontext();g.start=start;g.stop=stop
            pre=None
            if leaf['kind']=='candidate':
                row=next(x for x in plan['unique_whole_native_classes']if x['id']==leaf['case']);pre=prepared_candidate(row)
            old_handler=signal.signal(signal.SIGALRM,session.timeout_signal);signal.setitimer(signal.ITIMER_REAL,600)
            try:report=n.execute('wp29-s01-'+leaf['id'],'candidate'if leaf['kind']=='candidate'else'history-eviction-control',(lambda p:cm.run(p,pre))if pre else control_recipe,pre)
            finally:signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,old_handler)
            need(holder.get('stop',{}).get('confirmed'),'NoPositiveStop','No stopped export acceptance')
            report['guest_stopped']=True;report['owned_adapter']={'pid':holder['owned_pid'],'stop':holder['stop'],'exit_actions':holder.get('exit_actions'),'unchanged_engine':identity(ROOT/'scripts/reference/native_edits.py'),'configuration_only':'private short runtime/root output; subclass adds completion waits/captures and captured clear; approved39 final exit; actual guest stop plus bounded positive-identity poll','shared_lock_held_through_extraction':True};write(directory/'run.json',report)
            # Positive stop and stopped extraction are complete. Release actual
            # shared lock BEFORE offline Go reader/relationship/print auditing.
            fcntl.flock(shared_lock,fcntl.LOCK_UN)
            release={'released_at':stamp(),'owned_process_stop_confirmed':True,'engine_result':report['result'],'before_offline_comparison':True,'logical_reservation_continues':len(ledger['attempts'])<grant['max_attempts']}
            write(directory/'oracle-slot-release.json',release)
            if not release['logical_reservation_continues']:print(json.dumps({'phase':'last-owned-guest-stopped-extracted-oracle-released','leaf':leaf['id'],'before_offline_comparison':True}),flush=True)
            need(report['result']=='observed'and report['master_unchanged'],'IncompleteOriginal',report.get('error','unknown original protocol failure'))
            if leaf['kind']=='control':comparison=control_compare(directory,report)
            else:
                validate_owned_run(directory,report)
                classify_reader.HERE=n.OUT/'reader'
                comparison=cm.compare(directory,report)
            write(directory/'comparison.json',comparison);need(comparison['accepted'],'OriginalComparisonFailed','No next guest or expectation repair')
            attempt.update(outcome='accepted',completed_at=stamp(),run=str(directory/'run.json'),comparison=str(directory/'comparison.json'))
            if leaf['kind']=='control'and leaf['repeat']==2:seal_controls(plan)
            ledger['halted']=False;write(ledger_path,ledger)
        except BaseException as e:
            persist_fault(ledger_path,ledger,attempt,e,holder);raise
        finally:g.start=original_start;g.stop=original_stop;n.MutationProbe=original_class
    # Lock released only after actual stop, extraction, provenance/comparison.
    write(directory/'leaf-complete.json',{'outcome':'accepted','actual_leaf_argv':sys.argv,'positive_owned_stop':True,'shared_lock_released_after_exports':True,'completed_at':stamp(),'logical_reservation_continues':len(ledger['attempts'])<grant['max_attempts']})
    print(json.dumps({'leaf':leaf['id'],'outcome':'accepted','consumed_attempts':len(ledger['attempts']),'cap':grant['max_attempts'],'guest_stopped':True,'logical_reservation_complete':len(ledger['attempts'])==grant['max_attempts']}))

def replay_frames(folder):
    wire=(folder/'wire-output.bin').read_bytes();frames=json.loads((folder/'frames.json').read_text());screen=Screen(140,32);position=0
    for f in frames:
        end=f['wire_bytes_through'];need(isinstance(end,int)and position<=end<=len(wire),'WireFrameBoundary','Bad capture boundary');screen.feed(wire[position:end]);position=end
        need(screen.snapshot()==f['screen']and screen.state()==f['state'],'RawFrameMismatch','Stored current frame/state differs from exact emitted VT bytes')
    screen.feed(wire[position:]);screen.snapshot()
    return frames

def publication_witness(frames,name,gap):
    matches=[f for f in frames if f['state']['mode']=='Editing'and f['state']['name']==name and f['state']['save']=='NewNamePublished'and f['state']['dirty']is False and f['state']['gap']==gap]
    need(matches,'FalseSuccess','No actual current clean matching publication frame');return matches[-1]

def expected_events(recipe,marker=True):
    events=[b'\x1b[?31u',KEYS['retrieve'],b'ORIGIN',KEYS['enter']]
    for step in recipe['steps']:
        if 'save_name'in step:events +=[KEYS['save'],step['save_name'].encode(),KEYS['enter']]
        else:events.append(KEYS[step['key']]if'key'in step else step['text'].encode('ascii'))
    events +=[KEYS['save'],b'CANDIDA',KEYS['enter']]
    if marker:events +=[b'~',KEYS['save'],b'MARKER',KEYS['enter']]
    return [b.hex()for b in events+[KEYS['f7'],KEYS['f1'],KEYS['f7'],b'n',b'y']]

def verify_app(folder,recipe,row=None,marker=True):
    folder=Path(folder);frames=replay_frames(folder);process=json.loads((folder/'process.json').read_text());result=json.loads((folder/'result.json').read_text())
    if row:need(row['cases']==recipe['cases'],'WrongSemanticCase','Valid same-feature ID is not this recipe')
    need(result['id']==recipe['id']and result['outcome']=='app-emitted'and process['returncode']==0 and process['error']is None,'AppIncomplete','Actual executable did not finish admitted workflow')
    need([x['hex']for x in json.loads((folder/'injected.json').read_text())]==expected_events(recipe,marker),'AppEventMismatch','Actual key stream differs from declared original-command recipe')
    publication_witness(frames,'CANDIDA',recipe['gap']);need(frames[-1]['state']['mode']=='ExitQuestion','MissingAppFinalCapture','No captured pre-Yes original exit question')
    source=(folder/'files/ORIGIN').read_bytes();candidate=(folder/'files/CANDIDA').read_bytes();need(identity(folder/'files/ORIGIN')==process['before_source'],'AppSourceChanged','Loaded source differs')
    need(n.inspect(candidate,True)['body_hex']==recipe['body'],'AppBodyMismatch',recipe['id']);prefix_check(source,candidate,recipe.get('no_edit',False))
    need(identity(folder/'files/CANDIDA')==result['candidate'],'AppCandidateChanged','Candidate descriptor mismatch')
    if marker:
        publication_witness(frames,'MARKER',recipe['gap']+1);need(n.inspect((folder/'files/MARKER').read_bytes(),True)['body_hex']==result['marker']['expected_body_hex'],'NativeCursorMarker','Missing/wrong native gap witness')
    return {'accepted':True,'id':recipe['id'],'actual_key_events':len(expected_events(recipe,marker)),'raw_current_frames':len(frames),'candidate':identity(folder/'files/CANDIDA'),'scope':'actual executable/PTy native integration; original stage still separately required','physical_qualified':False}

def diagnostics(name):
    target,plan=selected();binary=plan['binary_path'];folder=OUT/'diagnostics'/name;need(not folder.exists(),'FreshDiagnostic','Preserve all attempts');folder.mkdir(parents=True);results=[]
    source=ROOT/(BASE+'wp23-a-blocks-r1/N0000.WP5')
    for kind in ['existing-target','source-change','create-permission','ec045-unsupported','paste-release']:
        app=None;error=None
        try:
            app=App(binary,folder/kind,source);app.retrieve()
            if kind=='ec045-unsupported':
                app.step(key('right'));app.step(key('delete',{'mode':'DeleteQuestion'}));app.step(text('y',{'mode':'DeleteQuestion','dirty':False,'cue':'UnsupportedHistoryEffect'}));app.step(key('f1',{'mode':'Editing','gap':2,'dirty':False}));copy=app.save('CANDIDA',2);need(copy==app.source,'RefusalMutatedNative','Unsupported EC045 intermediate changed native');app.finish()
            elif kind=='paste-release':
                before=app.screen.state();app.send_raw(b'\x1b[200~\x1b[18~ny\x1b[201~','paste is not key commands',{'mode':'Editing','gap':0,'dirty':False});app.send_raw(b'\x1b[18;1:3~','F7 release is not exit',{'mode':'Editing','gap':0,'dirty':False});need(app.save('CANDIDA',0)==app.source,'PasteMutated','Paste/release changed source image');app.finish()
            else:
                app.step(text('X',{'dirty':True}));app.step(key('save',{'mode':'SaveName'}));app.step(text('CANDIDA'))
                if kind=='existing-target':
                    (app.files/'CANDIDA').write_bytes(app.source);app.step(key('enter',{'mode':'ReplaceQuestion'}));app.step(text('y',{'mode':'ReplaceQuestion','dirty':True,'cue':'UnsupportedReplacement'}));app.step(text('n',{'mode':'SaveName'}));app.step(key('f1',{'mode':'Editing'}));need((app.files/'CANDIDA').read_bytes()==app.source,'ReplacementOverwrote','Existing inode changed')
                else:
                    external=app.source+b'Z'if kind=='source-change'else app.source
                    if kind=='source-change':(app.files/'ORIGIN').write_bytes(external)
                    else:os.chmod(app.files,0o555)
                    try:app.step(key('enter',{'mode':'SaveName','save':'SaveFailed','dirty':True,'name':'ORIGIN','cue':'StaleSource'if kind=='source-change'else'CandidateFailed'}))
                    finally:
                        if kind=='create-permission':os.chmod(app.files,0o700)
                    need(not(app.files/'CANDIDA').exists(),'FalseSuccess','Failed publication created destination');need((app.files/'ORIGIN').read_bytes()==external,'FailureDamagedSource','App changed expected external source');app.step(key('f1',{'mode':'Editing'}))
                app.finish()
            item={'case':kind,'accepted_diagnostic':True,'scope':'actual executable boundary, deliberate user No-save exit after definitive failure/refusal; no forced-success save','physical_qualified':False};write(app.folder/'diagnostic.json',item);results.append(item)
        except Exception as e:error=e;raise
        finally:
            if app:app.close(error)
    p=subprocess.run([binary,'-root',str(folder),'-profile','local-flat'],input=b'',capture_output=True);need(p.returncode==1 and b'requires terminal'in p.stderr,'NonTTYAccepted','No invented headless product mode');(folder/'non-tty.stderr').write_bytes(p.stderr)
    write(folder/'results.json',{'diagnostics':results,'short_write':'not deterministically injectable through CLI; actual lower-level storage failure tests remain separately scoped; no claimed executable short-write observation','stale_and_uncertainty':'public actual Model/Runtime tests hold real Cmd/results and host detach; no private receipt fabrication or physical-key alias'});print('Five real executable failure/refusal/transport diagnostics pass')

def verify_all():
    target,plan=check_plan();recipes_by_id={r['id']:r for r in json.loads((target/'recipes.json').read_text())};results=[]
    for row in plan['cases']:results.append(verify_app(ROOT/row['folder'],recipes_by_id[row['id']],row))
    ledger_path=ORACLE/'ledger.json';original=[]
    if ledger_path.exists():
        ledger=json.loads(ledger_path.read_text());need(not ledger['halted']and len(ledger['attempts'])==plan['original_guest_cap_including_failures'],'IncompleteGrant','Finite original run set incomplete or halted')
        for leaf in plan['original_leaves']:
            d=ORACLE/'runs'/('wp29-s01-'+leaf['id']);r=json.loads((d/'run.json').read_text())
            if leaf['kind']=='control':comparison=control_compare(d,r)
            else:
                import classify_reader
                classify_reader.HERE=ORACLE/'reader';validate_owned_run(d,r);comparison=cm.compare(d,r)
            need(comparison['accepted'],'OriginalRecheckFailed',leaf['id']);original.append({'leaf':leaf['id'],'accepted':True})
    report={'app_cases':results,'predecessor_qualified_controls':plan['predecessor']['qualified_control_count'],'historical_spent_attempts':3,'historical_candidate_incomplete':True,'new_candidate_attempts':len(original),'cumulative_attempt_cap':19,'original_leaves':original,'original_status':'not-run'if not original else'finite-accepted','executable_differential_accepted':bool(original),'full_m1_accepted':False,'physical_qualified':False};write(OUT/'verification.json',report);print(json.dumps({'app_cases':len(results),'original':len(original),'original_status':report['original_status']}));return report

def reopen_outputs(name):
    target,plan=check_plan();ledger=json.loads((ORACLE/'ledger.json').read_text());need(not ledger['halted']and len(ledger['attempts'])==plan['original_guest_cap_including_failures'],'IncompleteOriginalBatch','No live-app reopening substituted for missing original run')
    folder=OUT/'reopen'/name;need(not folder.exists(),'FreshReopen','Do not replace prior attempts');folder.mkdir(parents=True);paths=[]
    directories=[ORACLE/'runs'/('wp29-s01-'+leaf['id'])for leaf in plan['original_leaves']]+[OUT/'oracle/runs'/('wp29-history-control-r'+str(r))for r in [1,2]]
    for directory in directories:
        r=json.loads((directory/'run.json').read_text())
        for item in r['exports']:
            if item['path'].upper().endswith('.WP5'):paths.append(directory/item['path'])
    unique=[];aliases=[]
    for path in paths:
        raw=path.read_bytes();other=next((x for x in unique if identity(path)==x['identity']and raw==Path(x['source']).read_bytes()),None)
        if other:aliases.append({'source':str(path),'whole_native_alias_of':other['source'],'identity':identity(path)});continue
        app=None;error=None;sub=folder/('native-'+str(len(unique)+1))
        try:
            app=App(plan['binary_path'],sub,path);app.retrieve();copy=app.save('CANDIDA',0);need(copy==raw,'OriginalReopenLoss','No-edit actual app roundtrip must preserve entire original image')
            app.step(text('X'));frame=app.capture('actual mutation admission probe, not saved');state=frame['state'];view='\n'.join(frame['screen']['rows'])
            if state['dirty']and state['gap']==1:admission='mutation-admitted-at-this-specific-gap'
            else:
                need(not state['dirty']and state['gap']==0 and 'document:'in view,'UnknownMutationProbe','No fabricated readonly classification');admission='recognized-readonly-refused-edit'
            app.finish();need((app.files/'ORIGIN').read_bytes()==raw and(app.files/'CANDIDA').read_bytes()==raw,'OriginalReopenSourceChanged','Source/no-edit copy changed')
            record={'source':str(path),'identity':identity(path),'folder':str(sub.relative_to(ROOT)),'recognized':True,'whole_noedit_roundtrip_exact':True,'actual_mutation_probe':admission,'probe_frame':frame,'scope':'actual original-resaved output through runnable Wordling; probe edit discarded, no new interoperable candidate claim'};unique.append(record);write(sub/'reopen-result.json',record)
        except Exception as e:error=e;raise
        finally:
            if app:app.close(error)
    report={'paths':len(paths),'unique_whole_native_inputs':unique,'aliases':aliases,'alias_policy':'size+SHA AND full bytes with distinct original source provenance, never body-only','original_vm_reused':False,'all_lossless_app_reopens':True,'physical_qualified':False};write(folder/'reopen-report.json',report);write(OUT/'selected-reopen.json',{'path':str(folder.relative_to(ROOT)),'report':identity(folder/'reopen-report.json')});print(json.dumps({'actual_paths':len(paths),'unique_actual_app_reopens':len(unique),'all_roundtrip_exact':True}));return report

def source_associations():
    registry=ROOT/'docs/research/command-scenarios.json';rows={r['id']:r for r in json.loads(registry.read_text())};ids=['CMD51-046','CMD51-047','CMD51-048','CMD51-149','CMD51-200','CMD51-201','CMD51-202','CMD51-203','CMD51-204','CMD51-045','CMD51-043','CMD51-211'];fields=['id','title','feature_ids','requirement_ids','source_locators','oracle_status','implementation_status']
    return {'registry':str(registry.relative_to(ROOT)),'registry_identity':identity(registry),'registry_not_modified':True,'rows':[{k:rows[i][k]for k in fields}for i in ids],'scope':'semantic leads, not canonical closure. EC045 is explicit unsupported diagnostic;043 preview-only portion and211 finite control remain qualified by actual local recipe.'}

def safe_original_compare(directory,run):
    try:
        import classify_reader
        classify_reader.HERE=ORACLE/'reader';validate_owned_run(directory,run);return cm.compare(directory,run)
    except (ValueError,OSError,KeyError)as e:return {'accepted':False,'evidence_refusal':str(e)}

def negative_checks(name):
    import tempfile
    target,plan=check_plan();recipes_by_id={r['id']:r for r in json.loads((target/'recipes.json').read_text())};row=next(x for x in plan['cases']if x['id']=='ascii-modes');wrong=dict(row);wrong['cases']=['CMD51-047'];checks=[]
    need(source_associations()['rows'][0]['feature_ids']==source_associations()['rows'][1]['feature_ids'],'BadNegativeControl','046/047 must be valid same-feature but different semantics')
    try:verify_app(ROOT/row['folder'],recipes_by_id[row['id']],wrong)
    except Failure as e:need(e.code=='WrongSemanticCase','WrongNegativeReason',str(e));checks.append({'case':'wrong-valid-same-feature-app-case','rejected':True,'reason':str(e)})
    else:raise Failure('NegativeAccepted','Same-feature unrelated case accepted')
    permission=OUT/'diagnostics'/name/'create-permission';frames=replay_frames(permission)
    try:publication_witness(frames,'CANDIDA',1)
    except Failure as e:need(e.code=='FalseSuccess','WrongNegativeReason',str(e));checks.append({'case':'simulated-false-success-over-real-failed-app-save','rejected':True,'reason':str(e)})
    else:raise Failure('NegativeAccepted','Real failed-save frames accepted as clean publication')
    _,plan=check_plan();leaf=next(x for x in plan['original_leaves']if x['kind']=='candidate');original=ORACLE/'runs'/('wp29-s01-'+leaf['id']);base=json.loads((original/'run.json').read_text())
    for kind in ['wrong-same-feature-original-case','missing-final-capture','missing-print','missing-native','tampered-native-rehashed']:
        with tempfile.TemporaryDirectory(prefix='wp29-negative-')as temp:
            clone=Path(temp)/'run';shutil.copytree(original,clone,copy_function=os.link);run=json.loads(json.dumps(base));case=run['cases'][0]
            if kind=='wrong-same-feature-original-case':case['canonical_leads'][1]='CMD51-069' # actual existing same WP51-020 feature, wrong command
            elif kind=='missing-final-capture':shutil.rmtree(clone/'clean-exit')
            elif kind=='missing-print':(clone/case['print_stream']).unlink()
            elif kind=='missing-native':(clone/case['retrieved']).unlink()
            else:
                file=clone/case['edited'];raw=file.read_bytes();need(raw[-1:]==b'Z','BadTamperControl','Actual edited native must end Z');replacement=file.with_name(file.name+'.new');replacement.write_bytes(raw[:-1]+b'Y');os.replace(replacement,file)
                for item in run['artifacts']:
                    if item['path']==case['edited']:item.update(size=file.stat().st_size,sha256=identity(file)['sha256'])
            result=safe_original_compare(clone,run);need(result.get('accepted')is False,'NegativeAccepted',kind);checks.append({'case':kind,'rejected':True,'result':result})
    output=OUT/'negative-results.json';need(not output.exists(),'FreshNegatives','Do not replace prior checks');write(output,{'synthetic_mutations_of_actual_evidence_only':True,'all_rejected':True,'checks':checks,'original_raw_unchanged':True});print('Seven semantic/missing/tamper/false-success evidence controls rejected')

# Final CLI definition: finite commands only; no VM on import/offline commands.
def main():
    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='command',required=True)
    for x in ['pins','check','verify','associations','successor']:s.add_parser(x)
    for x in ['prepare','diagnostics','reopen','negatives']:a=s.add_parser(x);a.add_argument('name')
    a=s.add_parser('oracle');a.add_argument('--leaf',required=True);a.add_argument('--allow-vm',action='store_true');a.add_argument('--grant',type=Path)
    args=p.parse_args()
    if args.command=='pins':print(json.dumps(pins(),indent=2))
    elif args.command=='successor':prepare_successor()
    elif args.command=='prepare':prepare(args.name)
    elif args.command=='check':target,plan=check_plan();print(json.dumps({'status':'frozen offline input checks pass','oracle_launched':False,'classes':len(plan['unique_whole_native_classes']),'guests':plan['original_guest_cap_including_failures']}))
    elif args.command=='oracle':run_oracle(args)
    elif args.command=='verify':verify_all()
    elif args.command=='diagnostics':diagnostics(args.name)
    elif args.command=='reopen':reopen_outputs(args.name)
    elif args.command=='associations':print(json.dumps(source_associations(),indent=2))
    elif args.command=='negatives':negative_checks(args.name)

def validate_owned_run(directory,run):
    adapter=run.get('owned_adapter',{});owner=adapter.get('pid',{});stop=adapter.get('stop',{});observations=stop.get('observations',[])
    need(run.get('guest_stopped')is True and stop.get('confirmed')is True and isinstance(owner.get('pid'),int)and owner['pid']>0 and owner.get('start_ticks',0)>0 and bool(owner.get('argv_hex'))and observations,'MissingOwnedEvidence','Positive PID/argv/start ticks/stop completion required')
    need(stop.get('positive_owned_identity')==owner,'OwnedIdentityMismatch','Stop bound to another process')
    need(bytes.fromhex(owner['argv_hex']).split(b'\0')[:-1]==[os.fsencode(x)for x in run['qemu_argv']],'WrongOwnedArgv','Kernel-observed process is not the actual launch')
    need(json.loads((directory/'owned-pid.json').read_text())==owner and json.loads((directory/'owned-stop.json').read_text())==stop,'OwnedRawMismatch','Stored process witness differs')
    for event in observations:
        proc=event['process']
        need(proc is None or all(proc.get(k)==owner[k]for k in ['pid','start_ticks'])and(not proc.get('argv_hex')or proc['argv_hex']==owner['argv_hex']),'PIDIdentityChanged','Stop crossed process reuse')
    last=observations[-1];need(last['socket_exists']is False and(last['process']is None or last['process']['state']=='Z'),'StillLiveGuest','QMP return alone is not stopped evidence')
    need([x['monotonic']for x in observations]==sorted(x['monotonic']for x in observations),'StopClockReversed','Invalid completion sequence')
    profile=ROOT/'docs/research/reference-environment/environment.json';p=json.loads(profile.read_text());masters={'boot.img':p['master_boot_sha256'],'harddisk.img':p['master_disk_sha256']}
    need(run['master_before']==masters==run['master_after']and run['master_unchanged']is True and run['profile_sha256']==identity(profile)['sha256'],'MasterProfileMismatch','Must preserve actual pinned private masters/profile')
    need(run['runtime']['lock']==str(PRIMARY/'research/cache/reference/session1.lock')and run['runtime']['socket']==str(PRIMARY/'research/cache/reference/runtime/wp29/qmp.sock'),'WrongSharedRuntime','No parallel/foreign lock/runtime')
    for item in run['artifacts']:
        path=directory/item['path'];need(path.resolve().is_relative_to(directory.resolve())and path.is_file()and identity(path)=={'size':item['size'],'sha256':item['sha256']},'OriginalArtifactChanged',item['path'])
    need({x['path']for x in run['resources']}=={'WP.EXE','WP.FIL','WP.DRS','STANPRIN.PRS','WP{WP}.SET'},'MissingResources','All actual stopped installation fingerprints required')
    need(adapter.get('shared_lock_held_through_extraction')is True and adapter.get('exit_actions'),'MissingProtocolEvidence','No inferred normal exit/export lock')
    return {'positive_process_stop':True,'master_profile_runtime_and_artifacts_exact':True}

if __name__=='__main__':main()
