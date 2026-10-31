from pathlib import Path
import hashlib,json,subprocess
H=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-h');L=H.with_name('wp51-parity-01M64CVY-lane-l');O=Path('/tmp/wordling-WP29-save-diagnosis')
def sha(b):return hashlib.sha256(b).hexdigest()
pins={};traces=[]
for rep in ['r1','r2']:
 base=H/'docs/research/continuation/native-edits/runs'/('wp23-b-deletions-'+rep);j=json.loads((base/'run.json').read_text());t=j['trace'];start=next(i for i,x in enumerate(t)if x.get('capture')=='delete-0-delete-g1-confirmed');end=next(i for i in range(start,len(t))if t[i].get('capture')=='delete-0-delete-g1-final-saved');seg=t[start:end+1]
 assert [x.get('key')for x in seg if 'key'in x]==['f10','ret'];assert 'Document to be saved:'in(base/'delete-0-delete-g1-final-save-prompt/screen.txt').read_text()
 raw=(base/'N0001.WP5').read_bytes();assert raw[-4:]==b'ABCD'
 for path in [base/'run.json',base/'N0001.WP5',base/'delete-0-delete-g1-final-save-prompt/screen.txt',base/'delete-0-delete-g1-final-saved/screen.txt']:
  pins[str(path)]={'size':path.stat().st_size,'sha256':sha(path.read_bytes())}
 traces.append({'repeat':rep,'source_case':j['cases'][0],'original_confirmed_to_saved_trace':seg,'native_body':'ABCD'})
B=L/'docs/research/continuation/editing-differential/preparations/app-a';bug=B/'normal-paired-delete-r1'
for n in ['process.json','injected.json','frames.json','wire-output.bin','stderr.txt','files/ORIGIN']:
 p=bug/n;pins[str(p)]={'size':p.stat().st_size,'sha256':sha(p.read_bytes())}
assert not(bug/'files/CANDIDA').exists();proc=json.loads((bug/'process.json').read_text());binary=Path(proc['binary']if isinstance(proc['binary'],str)else proc['argv'][0]);assert sha(binary.read_bytes())==proc['binary']['sha256'];pins[str(binary)]=proc['binary']
paths=subprocess.check_output(['git','-C',str(H),'ls-files','cmd','internal','go.mod','go.sum'],text=True).splitlines();paths=[p for p in paths if p in ['go.mod','go.sum']or p.endswith('.go') and '/evidence/'not in p];equal=[]
for p in paths:
 assert (H/p).read_bytes()==(L/p).read_bytes(),p;equal.append({'path':p,'sha256':sha((H/p).read_bytes())})
for p in ['internal/editor/session.go','internal/editor/editing.go','internal/document/history.go','internal/document/history_observation.go','scripts/reference/native_edits.py','kitty-specs/wp51-parity-01M64CVY/contracts/editing.md','kitty-specs/wp51-parity-01M64CVY/contracts/session.md']:
 pins[str(H/p)]={'size':(H/p).stat().st_size,'sha256':sha((H/p).read_bytes())}
(O/'original-trace.json').write_text(json.dumps(traces,indent=2)+'\n');(O/'bindings.json').write_text(json.dumps({'source_h':subprocess.check_output(['git','-C',str(H),'rev-parse','HEAD'],text=True).strip(),'source_l':subprocess.check_output(['git','-C',str(L),'rev-parse','HEAD'],text=True).strip(),'equal_product_paths':equal,'pins':pins,'candidate_absent':True,'no_VM_or_privateHD_read':True},indent=2)+'\n');print('original two Save traces/native bodies checked; product equal paths',len(equal))
