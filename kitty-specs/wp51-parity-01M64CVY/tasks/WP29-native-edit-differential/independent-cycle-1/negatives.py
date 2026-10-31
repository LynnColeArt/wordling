from pathlib import Path
import sys,json,shutil,os,copy,tempfile
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-l');sys.path.insert(0,str(R/'scripts/reference'));import wordling_edits as w
O=Path('/tmp/wordling-wp29-independent');d=w.ORACLE/'runs/wp29-s01-no-edit-two-pair-r1';original=json.loads((d/'run.json').read_text());w.n.OUT=w.ORACLE
results=[]
for kind in ['rehash-native-body','rehash-full-print','owned-stop-still-live','foreign-owned-startticks']:
 with tempfile.TemporaryDirectory(prefix='wp29-review-negative-')as t:
  c=Path(t)/'run';shutil.copytree(d,c,copy_function=os.link);run=copy.deepcopy(original)
  def replace(p,data):
   q=p.with_name(p.name+'.independent');q.write_bytes(data);os.replace(q,p)
  if kind in ['rehash-native-body','rehash-full-print']:
   name=run['cases'][0]['edited'if kind=='rehash-native-body'else'print_stream'];p=c/name;raw=p.read_bytes();raw=raw[:-1]+bytes([raw[-1]^1]);replace(p,raw)
   for item in run['artifacts']:
    if item['path']==name:item.update(w.identity(p))
   for item in run['exports']:
    if item['path']==name:item.update(w.identity(p))
  else:
   stop=run['owned_adapter']['stop'];last=stop['observations'][-1]
   last['process']=dict(run['owned_adapter']['pid'],state='S')
   if kind=='foreign-owned-startticks':last['process']['start_ticks']+=1;last['process']['state']='Z'
   replace(c/'owned-stop.json',(json.dumps(stop,indent=2)+'\n').encode())
  v=w.safe_original_compare(c,run);assert v.get('accepted')is False,(kind,v)
  results.append({'kind':kind,'rejected':True,'reason':v.get('evidence_refusal')or v.get('errors')or v.get('checks')})
# Actual failed save wire must not become successful from an edited frame descriptor.
f=w.OUT/'preparations/app-a/normal-paired-delete-r1';frames=w.replay_frames(f)
try:w.publication_witness(frames,'CANDIDA',1)
except w.Failure as e:assert e.code=='FalseSuccess';results.append({'kind':'original-real-failed-F10-not-publication','rejected':True,'reason':str(e)})
else:raise AssertionError('false success accepted')
with tempfile.TemporaryDirectory(prefix='wp29-review-frame-')as t:
 c=Path(t);shutil.copyfile(f/'wire-output.bin',c/'wire-output.bin');frames=copy.deepcopy(frames);frames[-1]['state']['save']='NewNamePublished';frames[-1]['state']['dirty']=False;(c/'frames.json').write_text(json.dumps(frames))
 try:w.replay_frames(c)
 except w.Failure as e:assert e.code=='RawFrameMismatch';results.append({'kind':'forged-clean-frame-against-real-failed-wire','rejected':True,'reason':str(e)})
 else:raise AssertionError('forged frame accepted')
(O/'negative-results.json').write_text(json.dumps(results,indent=2)+'\n');print('PASS6 independent authentic comparator/wire negatives; rehashed native/PRN, live/reused PID, real failed F10 and forged clean descriptor')
