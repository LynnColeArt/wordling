"""Read-only closed observation labels. NEVER a mutation/admission predicate."""
import json
from pathlib import Path
import stage1
from frames import require
ROOT=stage1.ROOT
# Finite prospective vectors, declared from accepted complete metadata facts.
VECTORS={
 ('H1-R-e72402','H1-R-e72402','FIN-R-117202'):'uniform-H1-reload-known-print-transition',
 ('H1-R-e72402','H1-R-e72402','H1-R-e72402'):'uniform-H1-reload-counter-retained',
 ('C-R-e72401','C-R-e72401','FIN-R-117202'):'uniform-known-reordered01-alternate',
 ('C-L-e72401','C-L-e72401','FIN-R-117202'):'uniform-known-legacy01-alternate',
}
def classify(row,expected_body):
 fact=stage1.facts(row);info=row['Inspection'];raw=(ROOT/row['Path']).read_bytes();require(row['BodyHex']==expected_body.encode('ascii').hex(),'BodyMismatch','exact original operation/checkpoint body required')
 packets=info['Packets'];order=[p['Type']for p in packets];require(order in [[6,7,15,12,8],[7,15,12,6,8]],'UnknownFamily','closed complete five-packet graph only')
 blocks=info['Blocks'];require(len(blocks)==2,'UnknownFamily','exact two linked blocks');first,last=blocks;require(first['Data']=={'Offset':16,'Length':50}and first['Count']==last['Count']==5 and last['Data']['Length']==50 and first['Next']==last['Data']['Offset']and last['Next']==0,'UnknownFamily','all linked index facts required')
 sizes={6:16,7:14,15:86,12:90,8:2};owners=[(0,16),*( (b['Data']['Offset'],b['Data']['Length'])for b in blocks)]
 for j,p in enumerate(packets):
  require(p['Data']['Length']==sizes[p['Type']]and p['Index']=={'Offset':first['Data']['Offset']+10*(j+1)if j<4 else last['Data']['Offset']+10,'Length':10},'UnknownFamily','actual ordered indexed packet facts');owners.append((p['Data']['Offset'],p['Data']['Length']))
 end=0
 for offset,length in sorted(owners):require(offset==end,'UnknownFamily','no deleted/slack/overlap/unowned prefix');end+=length
 require(end==info['Body']['Offset']and raw[last['Data']['Offset']+20:last['Data']['Offset']+50]==bytes(30),'UnknownFamily','complete prefix ownership and zero unused slots')
 schema=json.loads((ROOT/'docs/research/continuation/native-constructor-design/schema.json').read_text())['fields'];cache=None;counter=None;flags=None;counter_offset=None
 for field,actual in zip(schema,fact['all72_fields']):
  value=bytes.fromhex(actual['hex']);expected=bytes.fromhex(field['hex']);owner=field['owner'];offset=field['relative_owner_offset']
  if owner=='header'and field['name']=='body start':expected=info['Body']['Offset'].to_bytes(4,'little')
  if owner=='packet-15'and offset==21:cache=value.hex();continue
  if owner=='packet-6'and offset==8:counter=int.from_bytes(value,'little');counter_offset=actual['absolute'];continue
  if owner=='packet-6'and offset==0:flags=value.hex();require(value in [b'\0',b'\x08'],'UnknownField','document flag must remain known00/08; observation only');continue
  require(value==expected,'UnknownField',owner+' '+field['name'])
 reordered=order[0]==6;family={ (True,'e724',2):'H1-R-e72402',(True,'e724',1):'C-R-e72401',(False,'e724',1):'C-L-e72401',(False,'1172',1):'C-L-117201',(True,'1172',2):'FIN-R-117202'}.get((reordered,cache,counter))
 require(family is not None,'UnknownFamily','new tuple is NOT a lazy known alternate')
 if counter==2:
  failure=row['Failure'];require(row['Admitted']is False and failure is not None and failure['Category']=='UnsupportedMetadata'and failure['TokenIndex']==-1 and failure['Span']=={'Offset':counter_offset,'Length':1},'ReadonlyRefusalMismatch','actual unchanged full gate must still refuse counter02')
 else:require(row['Admitted']is True,'CurrentGateMismatch','known01 family must satisfy actual unchanged full gate')
 return {'family':family,'flags':flags,'fact':fact,'mutation_permission':False}
def qualify(rows,case,repeat):
 require(len(rows)==3,'MissingCheckpoints','all3 actual native checkpoints required');names=['H51S0.WP5','H51S1.WP5','H51FIN.WP5'];expected=[case['S0_body'],case['S1_FIN_body'],case['S1_FIN_body']];classified=[classify(row,body)for row,body in zip(rows,expected)];vector=tuple(x['family']for x in classified);require(vector in VECTORS,'UnknownOrMixedFamily','prospective finite source/reload/final vector only');return {'family_vector':list(vector),'prospective_branch':VECTORS[vector],'native_checkpoints':classified,'repetition':repeat,'initial_contract_independently_sufficient':False,'future_B_permission':False}
def decision(results):
 require(len(results)==8,'MissingLeaves','ALL8 required; not partial qualification');branches={x['qualification']['prospective_branch']for x in results};require(len(branches)==1,'MixedBranches','all8 uniform finite metadata branch required')
 h1=next(iter(branches)).startswith('uniform-H1')
 return {'observations':'all8 uniformly H1 reload'if h1 else'all8 known alternate; nonempty H1 reload NOT proved','independent_initial_contract_sufficiency':'NOT adjudicated by this owned checker','future_structural_or_fallback_permission':False,'B_disposition':'BLOCKED pending independent sufficiency/design review and separate B candidate/original proof','authoritative_four_way_table':'N2 revision2 decision-table.json','full_M1_accepted':False}

def VECTORS_as_json():return [{"families":list(k),"name":v}for k,v in VECTORS.items()]
