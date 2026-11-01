"""Exact provenance + read-only public API facts; no guest/candidate/mutation."""
from pathlib import Path
import hashlib,json,subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];PROV=ROOT/'kitty-specs/wp51-parity-01M64CVY/tasks/WP51-h1-ascii-operation-contract/provenance'
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def dump(path,obj):Path(path).write_text(json.dumps(obj,indent=2)+'\n')
def provenance():
 mapping=json.loads((PROV/'path-map.json').read_text());rows=[]
 expected={'N2-revision2':'60e38bae8c72f33ea71c5e453b249e3e979f6557078ece0ed0b2be22d8e9bcfb','N2-cycle2-review':'25ba067e67bea2a26de31ff707135cd80ce4a2554fe9ebbb834e423771156ac1','H1-recon':'fb9ea4d145dbcb958ebe3ea8e9830c63f8c5beffe738085fc9c6af371abb95dd'}
 for group,digest in expected.items():assert sha(PROV/group/'seals.json')==digest,group
 for pin in mapping['files']:
  path=PROV/pin['archive_relative_path'];assert path.stat().st_size==pin['size']and sha(path)==pin['sha256'],str(path);rows.append({'path':str(path.relative_to(ROOT)),**pin})
 sources=json.loads((PROV/'N2-revision2/source-map.json').read_text())['sources']
 for pin in sources:
  raw=subprocess.check_output(['git','show',pin['commit']+':'+pin['path']],cwd=ROOT);assert len(raw)==pin['bytes']and hashlib.sha256(raw).hexdigest()==pin['sha256'];assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==pin['git_blob']
  # Caller sources are immutable Git context only, never imports/build overlays.
 return {'mirrored_artifacts':rows,'actual_Git_sources':sources}
def inventory():
 families=json.loads((ROOT/'docs/research/continuation/resaved-prefix-relationships/family-field-ledger.json').read_text())['families'];paths=[]
 for family in families:
  for stage in family['stages']:
   for w in stage['witnesses']:
    raw=(ROOT/w['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==w['sha256'];assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==w['git_blob'];assert subprocess.check_output(['git','show',family['source_commit']+':'+w['path']],cwd=ROOT)==raw;paths.append(w['path'])
 assert len(paths)==72 and len(set(paths))==72
 q=json.loads((PROV/'H1-recon/source-proof.json').read_text())['qualified_H1']
 for row in q:
  directory=Path(row['FIN']['path']).parent
  paths.extend([row['PRE']['path'],row['FIN']['path'],str(directory/'second-Go-edit.WP5')])
 return paths

def facts(row):
 raw=(ROOT/row['Path']).read_bytes();assert len(raw)==row['Bytes']and sha(ROOT/row['Path'])==row['SHA256'];assert row['Parsed']and row['ExportExact']and row['OriginalExact']
 info=row['Inspection'];schema=json.loads((ROOT/'docs/research/continuation/native-constructor-design/schema.json').read_text())['fields'];owners={'header':{'Offset':0,'Length':16}}
 required={f['owner']for f in schema}
 for packet in info['Packets']:
  key='packet-'+str(packet['Type'])
  if key not in required:continue
  if key in owners:raise ValueError('ambiguous native packet owner; no last-packet overwrite')
  owners[key]=packet['Data']
 fields=[]
 for f in schema:
  owner=owners.get(f['owner']);assert owner is not None,f['owner'];offset=owner['Offset']+f['relative_owner_offset'];width=f['width'];assert 0<=f['relative_owner_offset'] and width>0 and f['relative_owner_offset']+width<=owner['Length'];value=raw[offset:offset+width]
  fields.append({'owner':f['owner'],'name':f['name'],'absolute':offset,'width':width,'hex':value.hex(),'representation':f['representation'],'units':f['units'],'source':f.get('source',f.get('authority'))})
 assert len(fields)==72
 return {'path':row['Path'],'sha256':row['SHA256'],'bytes':len(raw),'exact_native_framing_and_export':True,'actual_admission':row['Admitted'],'actual_refusal':row['Refusal'],'actual_failure':row['Failure'],'body_hex':row['BodyHex'],'native_graph':info,'all72_fields':fields}
def run(probe):
 p=provenance();paths=inventory();raw=subprocess.check_output([str(probe),*paths],cwd=ROOT);rows=json.loads(raw);assert len(rows)==84
 result={'authority':'existing immutable source/read-only API facts ONLY','provenance':p,'images':[facts(x)for x in rows],'new_candidates':0,'semantic_mutation_calls':0,'new_guests':0,'H1_ASCII_permission':False,'nonempty_H1_reload_proved':False,'Stage2_discriminating_missing_facts':['initial emptyH1 Insert/Typeover source→target operations','same-byte original operation/mode/cursor/native dirty effects','actual nonempty S0 Save-clear-Retrieve family before next ASCII','all8 uniform operation/reload outcome with full72/native/custody evidence'],'Stage2_justified':True,'whole_M1_accepted':False};return result
if __name__=='__main__':
 import sys
 dump(HERE/'stage1-facts.json',run(Path(sys.argv[1]).resolve()))
