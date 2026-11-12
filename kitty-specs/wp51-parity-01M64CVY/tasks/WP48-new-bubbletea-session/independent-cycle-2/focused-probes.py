"""Fresh raw-result and actual approved public-reader falsifiers; no VM or tracked writes."""
import json,copy,tempfile,shutil,importlib.util,hashlib,subprocess
from pathlib import Path
R=Path.cwd();H=R/'docs/research/continuation/new-session/interop-z-01';O=Path('/tmp/wordling-wp48-independent-cycle-2');s=importlib.util.spec_from_file_location('wp48_cycle2_probe',H/'adapter.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a);p=json.loads((H/'preflight.json').read_text())['plan'];run=R/p['public_output'];rows=json.loads((run/'run.json').read_text())['results'];ledger=json.loads((run/'aggregate-ledger.json').read_text());observed=[]
def refusal(label,fn):
 try:fn()
 except Exception as e:observed.append({'case':label,'exception':type(e).__name__,'code':getattr(e,'code',None)});return
 raise AssertionError(('unsafe control accepted',label))
row=rows[0];leaf=p['attempts'][0];assert a.custody_record(p,leaf,row)
for key,value in [('normal-stop','Host containment'),('wrong-startticks','1'),('socket-still-live',True),('after-deadline',True)]:
 d=copy.deepcopy(row)
 if key=='normal-stop':d['stop_method']=value
 elif key=='wrong-startticks':d['owned_start_identity']['startticks']=value
 elif key=='socket-still-live':d['stop_proof']['observations'][-1]['socket_present']=True
 else:d['stop_proof']['observations'][-1]['observation_complete_monotonic']=d['stop_proof']['observations'][-1]['deadline_monotonic']+1
 refusal(key,lambda:a.custody_record(p,leaf,d))
for label,entries in [('missing-second-control',ledger['attempts'][:1]),('rehashed-wrong-control-reference',copy.deepcopy(ledger['attempts'][:2]))]:
 if label.startswith('rehashed'):entries[0]['result_file_sha256']='0'*64
 refusal(label,lambda:a.control_rows(p,entries))
source=run/a.ids()[0]
for mode in ['FIN-body','full-PRN','SEED-flag']:
 with tempfile.TemporaryDirectory(prefix='wp48-native-refusal-')as tmp:
  d=Path(tmp)
  for name in ['C48SEED.WP5','C48PRE.WP5','C48FIN.WP5','C48PRN.PRN']:shutil.copyfile(source/name,d/name)
  assert a.qualify(d,leaf,emit_Q=False)['full_M1_accepted']is False
  if mode=='FIN-body':f=d/'C48FIN.WP5';b=bytearray(f.read_bytes());b[-1]^=1;f.write_bytes(b)
  elif mode=='full-PRN':f=d/'C48PRN.PRN';f.write_bytes(f.read_bytes()+b'X')
  else:
   f=d/'C48SEED.WP5';v=a.old.product('-verify',f,'-require-preprint');offset=next(x['Data']['Offset']for x in v['inspection']['Packets']if x['Type']==6);b=bytearray(f.read_bytes());b[offset]=8;f.write_bytes(b)
  refusal(mode,lambda:a.qualify(d,leaf,emit_Q=False))
(O/'focused-probes.json').write_text(json.dumps(observed,indent=2)+'\n');print(json.dumps(observed,indent=2))
