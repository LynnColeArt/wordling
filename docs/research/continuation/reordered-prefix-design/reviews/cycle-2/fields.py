from pathlib import Path
import json,hashlib,sys,struct
A=Path('/tmp/wordling-prefix-expansion-architecture');S=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-s');T=Path('/tmp/wordling-prefix-expansion-architecture-review/cycle-2');sys.path.insert(0,str(S/'scripts/reference'));import native_edits
h=lambda b:hashlib.sha256(b).hexdigest();m=json.loads((A/'manifest.json').read_text());p=m['reordered_source_predicate_R1'];rules=p['field_rules'];assert len(rules)==72
approved=json.loads((S/'docs/research/continuation/native-edits/field-ledger.json').read_text())['field_coverage'];assert len(approved)==72
for new,old in zip(rules,approved,strict=True):
 assert all(new[k]==old[k] for k in ['owner','name','width','representation']) and new['relative_offset']==old['offset']
def qualify(raw):
 info=native_edits.inspect(raw,False);pack=info['packets'];blocks=info['blocks'];assert [x['type'] for x in pack]==[6,7,15,12,8]
 assert len(blocks)==2 and blocks[0]['offset']==16
 assert blocks[0]['next']==blocks[1]['offset'] and blocks[1]['next']==0
 # Full index framing and ignored unused bytes are checked independently of diagnostics.
 assert all(struct.unpack_from('<H',raw,b['offset']+2)[0]==5 for b in blocks)
 assert raw[blocks[1]['offset']+20:blocks[1]['offset']+50]==bytes(30)
 types=[6,7,15,12,8];sizes=[16,14,86,90,2]
 for i,(x,k,n) in enumerate(zip(pack,types,sizes,strict=True)):
  assert x['type']==k and x['length']==n and x['index_offset']==(blocks[0]['offset']+10*(i+1) if i<4 else blocks[1]['offset']+10)
 owners={x['type']:x for x in pack};spans=[(0,16)]+[(b['offset'],50) for b in blocks]+[(x['offset'],x['length']) for x in pack];end=0
 for a,n in sorted(spans):assert a==end;end+=n
 assert end==info['body_offset']==int.from_bytes(raw[4:8],'little');assert owners[8]['offset']+2==end
 vals=[]
 for f in rules:
  start=0 if f['owner']=='header' else owners[int(f['owner'].split('-')[1])]['offset'];off=start+f['relative_offset'];v=raw[off:off+f['width']]
  if f['owner']=='header' and f['relative_offset']==4:assert int.from_bytes(v,'little')==end
  elif f['owner']=='packet-6' and f['relative_offset']==0:assert v in [b'\0',b'\x08']
  else:assert v.hex()==f['raw_hex']
  vals.append(v.hex())
 pool=owners[7];font=owners[15];ptr=int.from_bytes(raw[font['offset']+18:font['offset']+20],'little');assert ptr<pool['length'] and 0 in raw[pool['offset']+ptr:pool['offset']+pool['length']]
 assert all(v in [254,255,0] for v in raw[font['offset']+50:font['offset']+86]);assert raw[font['offset']+62]==255
 assert info['body_grammar_refusal'] is None and len(raw)<=65536
 return vals
positive=[]
for item in p['positive_original_preprint_sources']:
 raw=(S/item['path']).read_bytes();assert h(raw)==item['sha256'];values=qualify(raw);positive.append({'path':item['path'],'sha256':h(raw),'fields_exact':len(values)})
assert len(positive)==24
neg=[]
for item in p['negative_original_FIN_sources']:
 raw=(S/item['path']).read_bytes();assert h(raw)==item['sha256']
 try:qualify(raw)
 except AssertionError:neg.append(item['path'])
 else:raise AssertionError('FIN accepted')
assert len(neg)==6
scalar=[]
for x in p['negative_unobserved_combinations_and_emitter_state']:
 actual=x['cache_hex']=='e724' and x['counter_hex']=='01' and x['flag_hex'] in ['00','08'];assert actual==x['scalar_field_predicate_accepts'];scalar.append({'cache':x['cache_hex'],'counter':x['counter_hex'],'flag':x['flag_hex'],'accepts':actual})
(T/'fields.json').write_text(json.dumps({'scope':'independent in-memory architecture predicates only, not product or original execution','positive24':positive,'actual_FIN6_rejected':neg,'scalar_cases':scalar,'all72_rules_match_approved_field_types_offsets':True},indent=2)+'\n');print('PASS24 actual native full structure+72 fields,6actualFINreject,7declaredscalarcases; no native output or VM')
