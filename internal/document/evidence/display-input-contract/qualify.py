#!/usr/bin/env python3
"""Read-only display INPUT roles and source-phase applicability; no geometry API."""
from pathlib import Path
import argparse,json,re,resource,sys
sys.dont_write_bytecode=True
from boundaries import Refusal,read,parse,sha,require,canonical,publish
from source import HERE,ROOT,Sources
import bridge
REPORT='docs/research/continuation/text-flow-contract/offline-result.json'
GENESIS='docs/research/continuation/native-genesis/analysis/genesis-ledger.json'
DEFINITIONS='docs/research/continuation/native-edits/field-ledger.json'
SCHEMA='wordling.wp56.display-input/v1'
class Qualifier:
 def __init__(self):
  self.sources=Sources();self.reference=self.sources.json(REPORT)['data'];self.genesis=self.sources.json(GENESIS);self.references={};self.observations={};self.unselected14=0
  for run in self.reference['runs']:
   for state in run['states']:
    for which in ['before','after']:
     p=state[which+'_path'];self.references[p]=dict(id=p,document=p,profile=run['profile_sha256'],phase='native-'+state['id']+'-'+which,run=run['run_id'])
   for setting in run['actual_settings']:
    ident=setting['path']
    if ident not in self.sources.pins:self.unselected14+=1;continue
    actual=self.sources.data(ident);require(actual.decode()==setting['text']and sha(actual)==setting['screen_sha256'],'CaptureCorroboration',ident)
    self.observations[ident]=dict(id=ident,run=run['run_id'],profile=run['profile_sha256'],document_family='wp14/'+run['variant'],phase='capture:'+setting['label'],trace_index=next((i for i,t in enumerate(run['trace'])if t.get('capture')==setting['capture']),None),role='captured_setting',label=setting['label'],text=setting['text'],source=ident,sha256=setting['screen_sha256'],observed_unit='inch-suffixed menu/argument where explicitly shown; not selected GENERAL/STATUS',selected_GENERAL=False,selected_STATUS=False)
  for row in self.sources.rows:
   path=row['path']
   if '/native-genesis/runs/'in path and path.endswith('.WP5')and('/G43TEXT.'in path or'/G43EMPTY.'in path):
    self.references[path]=dict(id=path,document=path,profile=None,phase='first-save',run=path.rsplit('/',1)[0])
   if '/native-genesis/runs/wp43-genesis-01-ascii-first-retrieve/'in path and '/settings-'in path and path.endswith('/screen.txt'):
    run=path.split('/settings-')[0];text=self.sources.data(path).decode();ident=path;self.observations[ident]=dict(id=ident,run=run,profile=None,document_family='wp43-ascii-first-retrieve',phase='settings-after',role='captured_setting',label=path.split('/settings-')[1].split('/')[0],text=text,source=path,sha256=row['sha256'],observed_unit='inch-suffixed menu where explicitly shown; not selected GENERAL/STATUS',selected_GENERAL=False,selected_STATUS=False)
  # Actual13 source-bound status observations; associated native output is later saved,
  # not a claim that raw hardware coordinates identify a current native gap.
  for rep in ['r1','r2']:
   base='docs/research/continuation/session1/runs/2026-10-31-session1-b01-'+rep
   record=self.sources.json(base+'/run.json');ref=base+'/CMD51-049/CURSOR.WP5';self.references[ref]=dict(id=ref,document=ref,profile=record['environment_manifest_sha256'],phase='native-output-after-cursor',run=base)
   for row in self.sources.rows:
    path=row['path']
    if path.startswith(base+'/CMD51-049/normal-gap-')and path.endswith('/screen.txt'):
     capture=path.split('/')[-2];text=self.sources.data(path).decode();self.observations[path]=dict(id=path,run=base,profile=record['environment_manifest_sha256'],document_family='wp13-CURSOR',phase='capture:'+capture,role='observed_status_unit',label=capture,text=text,source=path,sha256=row['sha256'],observed_unit='inch suffix as captured only',selected_GENERAL=False,selected_STATUS=False)
  for obs in self.observations.values():
   obs['roles']=[obs['role']]
   obs['unit_evidence_lines']=[line for line in obs['text'].splitlines()if chr(34)in line]
   if obs['unit_evidence_lines']and obs['role']=='captured_setting':obs['roles'].append('observed_menu_unit')
   obs['observed_unit']=('inch suffix on exact status lines only'if obs['role']=='observed_status_unit'else'inch suffix on exact menu lines only')if obs['unit_evidence_lines']else None
  # Captured status suffix is its own source role, never selected STATUS setup.
  case=next(c for c in self.genesis['facts']['cases']if c['plan']['id']=='ascii-first-retrieve')
  for sample in case['samples']:
   name='wp43-status-r'+str(sample['repetition']);state=sample['actual_state_ledger']['actual_states']['first-ascii-before-save'];self.observations[name]=dict(id=name,run='docs/research/continuation/native-genesis/runs/wp43-genesis-01-ascii-first-retrieve/r'+str(sample['repetition']),profile=None,document_family='wp43-ascii-first-retrieve',phase='before-first-save',role='observed_status_unit',label='literal status suffix',text=state['footer'],source=GENESIS,sha256=self.sources.pins[GENESIS]['sha256'],observed_unit='inch suffix as captured only',selected_GENERAL=False,selected_STATUS=False,roles=['observed_status_unit'],unit_evidence_lines=[state['footer']])
 def catalog(self):
  native=next(p for p in self.references if '/native-genesis/'in p and '/r1/'in p and p.endswith('/G43TEXT.WP5'))
  later=next(p for p,o in self.observations.items()if '/r1/'in p and o['label']=='line-settings'and '/native-genesis/'in p)
  return dict(schema=SCHEMA+'/catalog',references=self.references,observations=self.observations,examples=dict(native=dict(native=native,reference=native,phase='first-save'),later43=dict(native=native,reference=native,phase='settings-after',observation=later,requested_role='captured_setting')),source_count=len(self.sources.rows),source_bytes=self.sources.total,unselected_report_only14=self.unselected14,runtime_display_ready=False)
 def native(self,raw):
  checked,proof=bridge.inspect(raw);tokenizer,analyzer,extractor=self.sources.load_extractors();defs=self.sources.json(DEFINITIONS)['field_coverage']
  font=extractor.prefix_font_fields(raw,tokenizer,defs);outer=extractor.observe_native(raw,tokenizer,analyzer);inspection=checked['inspection'];packets=inspection['Packets']
  for field in font:
   owners=[p for p in packets if p['Type']==int(field['owner'].split('-')[1])];require(len(owners)==1,'NativeOwner','exact packet owner');owner=owners[0];span=owner['Data'];require(span['Offset']==field['owner_offset']and 0<=field['relative_offset']<=span['Length']-field['width'],'NativeOwner','reader-owned data span');field['index_span']=owner['Index'];field['data_span']=span
  require(outer['document_offset']==inspection['Body']['Offset'],'NativeBodyOwner','approved extractor/reader agree')
  prefix_fields=[]
  for field in defs:
   if field['owner']not in {'packet-6','packet-12','packet-15'}:continue
   owners=[p for p in packets if p['Type']==int(field['owner'].split('-')[1])]
   if len(owners)!=1:continue
   owner=owners[0];offset=owner['Data']['Offset']+field['offset'];width=field['width']
   require(0<=field['offset']<=owner['Data']['Length']-width,'LiteralBounds',field['name']);bits=raw[offset:offset+width]
   prefix_fields.append(dict(name=field['name'],owner=field['owner'],index_span=owner['Index'],data_span=owner['Data'],absolute_offset=offset,relative_offset=field['offset'],width=width,representation=field['representation'],unit=field['units'],references=field.get('references'),raw_hex=bits.hex(),value=int.from_bytes(bits,'little')if width<=4 else None,scope='literal documentary field only; resource/pool contents not metrics authority'))
  return dict(sha256=sha(raw),inspection=inspection,prefix_fields=prefix_fields,font_fields=font,format_fields=outer['format_fields'],packet3_present=any(p['Type']==3 for p in packets),body_sha256=outer['body_sha256'],meaning='known stored literals/complete outer operand frames; not effective cursor values'),proof
 def qualify(self,request):
  require(isinstance(request,dict)and set(request)<=set(['native','reference','phase','observation','requested_role','claim','current']),'RequestShape','closed request keys');require(isinstance(request.get('native'),str),'NativePath','required regular native path')
  raw=read(ROOT/request['native']if not Path(request['native']).is_absolute()else Path(request['native']),1<<20)
  native,proof=self.native(raw);ref=request.get('reference');context=None
  if ref is not None:
   require(isinstance(ref,str)and ref in self.references,'ReferenceSelector',ref);require(self.sources.data(ref)==raw,'ReferenceNativeMismatch','valid stored values do not prove original captured source identity');context=self.references[ref]
  phase=request.get('phase','unknown');require(isinstance(phase,str),'PhaseSelector','string only');require(phase in {'unknown','first-save','before-first-save','settings-after'}|{o['phase']for o in self.observations.values()}|{r['phase']for r in self.references.values()},'PhaseSelector',phase)
  result=dict(schema=SCHEMA,native=native,reader=proof,reference_context=context,requested_phase=phase,observation=None,selected_GENERAL=dict(status='unresolved',reason='no bound selected GENERAL unit setup authority'),selected_STATUS=dict(status='unresolved',reason='no bound selected STATUS unit setup authority'),current_applicability=dict(status='unresolved',reason='no bound current configuration revision/resource/initial-code/effect state'),runtime_display_ready=False,guest_attempts=0,native_mutation_permission=False)
  if 'current'in request:
   c=request['current'];require(isinstance(c,dict)and set(c)=={'native_sha256','configuration_revision'},'CurrentShape','native identity and distinct revision only');require(c['native_sha256']==sha(raw),'CurrentNativeMismatch','different current native');require(isinstance(c['configuration_revision'],str)and 0<len(c['configuration_revision'])<=128,'CurrentRevision','bounded identifier');result['current_applicability']['claimed_configuration_revision']=c['configuration_revision'];result['current_applicability']['reason']='caller revision names identity; no source proves selected configuration applicability'
  if 'observation'in request:
   ident=request['observation'];require(isinstance(ident,str)and ident in self.observations,'ObservationSelector',ident);obs=self.observations[ident]
   if 'claim'in request:require(request['claim']==obs,'ForgedObservation','rehashed caller payload is not the immutable observed source')
   role=request.get('requested_role',obs['role']);require(role in {'captured_setting','observed_menu_unit','observed_argument_unit','observed_status_unit','selected_GENERAL','selected_STATUS','current_default'},'RoleSelector',role)
   same_family=context is not None and (('/native-genesis/'in context['id']and obs['document_family']=='wp43-ascii-first-retrieve'and context['run']==obs['run'])or(context['run']==obs['run']and context['profile']==obs['profile']))
   if not same_family:raise Refusal('ObservationBinding','observation document/run/profile differs from requested native reference context')
   applicable=phase==obs['phase']and role in obs['roles']
   reason='captured source role at its actual phase; not current runtime configuration'if applicable else 'supported source is insufficient for requested phase or unit/setup/default role'
   result['observation']=dict(status=role if applicable else'supported_but_insufficient',requested_role=role,source_fact=obs,reason=reason)
  else:require('claim'not in request and'requested_role'not in request,'ObservationRequired','role/claim needs observed source')
  return result
 def check(self):
  # Every original native and entire PRN remains bound; field recomputation is real.
  paths=sorted({s[k]for r in self.reference['runs']for s in r['states']for k in ['before_path','after_path']});rows=[]
  for p in paths:
   value,_=self.native(self.sources.data(p));rows.append(dict(path=p,native=value))
  streams=[dict(path=s['print_path'],size=len(self.sources.data(s['print_path'])),sha256=sha(self.sources.data(s['print_path'])))for r in self.reference['runs']for s in r['states']]
  return dict(schema=SCHEMA+'/check',source_count=len(self.sources.rows),source_bytes=self.sources.total,native_snapshots=rows,complete_PRN=streams,known_literals_preserved=True,runtime_display_ready=False,guest_attempts=0)
def main():
 p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
 for name in ['catalog','check']:
  q=sub.add_parser(name);q.add_argument('--output',type=Path)
 q=sub.add_parser('qualify');q.add_argument('request',type=Path);q.add_argument('--output',type=Path);args=p.parse_args()
 try:
  qualifier=Qualifier();value=qualifier.catalog()if args.command=='catalog'else qualifier.check()if args.command=='check'else qualifier.qualify(parse(read(args.request,65536)))
  require(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024<=512<<20,'RSSLimit','host runtime ceiling')
  if args.output:publish(args.output,value,HERE)
  else:
   raw=json.dumps(value,sort_keys=True).encode();require(len(raw)<=4<<20,'ReportLimit',len(raw));sys.stdout.buffer.write(raw+b'\n')
  return 0
 except (Refusal,OSError,ValueError,KeyError,TypeError,ImportError)as e:
  print(json.dumps(dict(status='refused',code=getattr(e,'code',type(e).__name__),detail=str(e),runtime_display_ready=False,guest_attempts=0)),file=sys.stderr);return 1
if __name__=='__main__':raise SystemExit(main())
