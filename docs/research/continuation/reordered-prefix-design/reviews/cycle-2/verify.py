from pathlib import Path
import json,hashlib,subprocess,yaml
A=Path('/tmp/wordling-prefix-expansion-architecture');T=Path('/tmp/wordling-prefix-expansion-architecture-review/cycle-2');P=Path('/home/lynn/projects/wordling');S=P/'.worktrees/wp51-parity-01M64CVY-lane-s';h=lambda b:hashlib.sha256(b).hexdigest();m=json.loads((A/'manifest.json').read_text());seals=json.loads((A/'seals.json').read_text())
for f,d in seals['files'].items():b=(A/f).read_bytes();assert h(b)==d['sha256'] and len(b)==d['size']
assert h((A/'seals.json').read_bytes())=='8c1d987743c328b9948235c34e6f8d9b7610982df33f4dd9285ced27fa42defa'
for pin in m['source_pins']:
 b=(Path(pin['checkout'])/pin['path']).read_bytes();assert h(b)==pin['sha256'] and len(b)==pin['size'],pin
for p,v in m['protected_all43_prompt_hashes'].items():assert h((P/p).read_bytes())==v
for pin in m['original_image_pins']:
 b=(S/pin['path']).read_bytes();assert h(b)==pin['sha256'] and len(b)==pin['size']
proof=m['dag_proof'];deps=proof['proposed_dependency_map'];assert len(deps)==45
for p in m['protected_all43_prompt_hashes']:
 text=(P/p).read_text();front=yaml.safe_load(text.split('---',2)[1]);assert set(front.get('dependencies',[]))==set(deps[front['work_package_id']])
def topo(d):
 out=[];pending=set(d)
 while pending:
  ready=sorted(k for k in pending if set(d[k])<=set(out));assert ready,'cycle';out+=ready;pending-=set(ready)
 return out
assert len(topo(deps))==45;assert len(topo(proof['lane_dependencies']))==22
# Independently recompute every residual-byte match against actual approved42 native images.
prov=json.loads((A/'existing-564-provenance-observations.json').read_text());assert len(prov['rows'])==63
for row in prov['rows']:
 d=S/'docs/research/continuation/resaved-prefix/runs'/('w42-'+row['case']);raw=(d/'r1'/row['stage']).read_bytes();assert raw==(d/'r2'/row['stage']).read_bytes();e=row['extent'];b=raw[e['offset']:e['offset']+e['length']];assert h(b)==row['sha256'] and b.hex()==row['literal_hex']
 for v in row['matches_known_live_payloads']:
  p=(d/'r1'/v['stage']).read_bytes();assert p[v['absolute_offset']:v['absolute_offset']+len(b)]==b
# Pins already bind approved model/research, but verify actual bodies are preserved across new-prefix layout.
sum42=json.loads((S/'docs/research/continuation/resaved-prefix/evidence/matrix-summary.json').read_text());new=[]
for c in sum42['cases']:
 if c['case'].endswith('disabled'):
  for a in c['artifacts']:
   if a['name']=='W42S0.WP5':continue
   ps={p['type']:p for p in a['live_packets']};raw=(S/'docs/research/continuation/resaved-prefix/runs'/c['run_id']/'r1'/a['name']).read_bytes()
   flag=raw[ps[6]['offset']];counter=raw[ps[6]['offset']+8];cache=raw[ps[15]['offset']+21:ps[15]['offset']+23].hex()
   assert flag==0 and (cache,counter)==(('1172',2) if a['name']=='W42FIN.WP5' else ('e724',1))
   assert [p['type'] for p in a['live_packets']]==[6,7,15,12,8]
   new.append({'case':c['case'],'stage':a['name'],'counter':counter,'flag':flag,'cache':cache,'proposed_predicate_admits':cache=='e724' and counter==1})
(T/'verification.json').write_text(json.dumps({'seals_exact':True,'source_pins':len(m['source_pins']),'original_image_pins':len(m['original_image_pins']),'protected_prompts':43,'package_DAG':45,'lane_DAG':22,'residual_extents':63,'residual_interpretation':'byte provenance only; no active-reference/deadness inference','actual_reordered_stages':new,'source_policy':'unchanged; architecture review only'},indent=2)+'\n');print('PASS frozen seals/source/image pins43prompts45package22laneDAG63residuals/newactualfieldvalues')
