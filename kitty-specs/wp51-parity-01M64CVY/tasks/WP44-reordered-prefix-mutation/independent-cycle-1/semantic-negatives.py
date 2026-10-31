from pathlib import Path
import importlib.util,json,shutil,hashlib
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-e');B=R/'internal/document/evidence/wp44';O=Path('/tmp/wordling-wp44-independent');spec=importlib.util.spec_from_file_location('actual_wp44',B/'oracle.py');o=importlib.util.module_from_spec(spec);spec.loader.exec_module(o);D=B/'runs/wp44-v2-phase01';pre=json.load(open(D/'prelaunch.json'));leaf=pre['plan']['attempts'];leaf=next(x for x in leaf if x['id']=='wp44-v2-c09-candidate-r1');case=next(x for x in pre['plan']['cases']if x['id']==leaf['case']);rows=[]
for name in ['positive','PRE-counter02','PRE-body-changed','PRN-one-byte-changed']:
 target=O/'negatives'/name;target.mkdir(parents=True)
 for n in ['C44PRE.WP5','C44FIN.WP5','C44PRN.PRN']:shutil.copyfile(D/leaf['id']/n,target/n)
 if name=='PRE-counter02':
  raw=bytearray((target/'C44PRE.WP5').read_bytes());info=json.load(open(D/'run.json'))['results'][0]['required_output_qualification']['preprint']['inspection'];packet=next(p for p in info['Packets']if p['Type']==6);raw[packet['Data']['Offset']+8]=2;(target/'C44PRE.WP5').write_bytes(raw)
 if name=='PRE-body-changed':
  raw=bytearray((target/'C44PRE.WP5').read_bytes());raw[-1]=ord('R');(target/'C44PRE.WP5').write_bytes(raw)
 if name=='PRN-one-byte-changed':
  p=target/'C44PRN.PRN';raw=bytearray(p.read_bytes());raw[-1]^=1;p.write_bytes(raw)
 pins={n:hashlib.sha256((target/n).read_bytes()).hexdigest()for n in ['C44PRE.WP5','C44FIN.WP5','C44PRN.PRN']};(target/'rehashed.json').write_text(json.dumps(pins,indent=2)+'\n')
 try:q=o.qualify_exports(target,case,leaf,None);error=None
 except Exception as e:error={'category':getattr(e,'code',type(e).__name__),'text':str(e)}
 assert(error is None)==(name=='positive'),(name,error)
 rows.append({'case':name,'fresh_hashes':pins,'actual_qualification_boundary_error':error,'not_an_integrity_only_negative':True})
(O/'semantic-negatives.json').write_text(json.dumps(rows,indent=2)+'\n');print('actual positive and3 meaningful preprint-body/cache/PRN semantic negatives passed')
