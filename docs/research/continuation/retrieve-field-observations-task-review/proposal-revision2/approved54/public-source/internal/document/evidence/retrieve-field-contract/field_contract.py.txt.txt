"""Closed transition-specific text/VGA/cursor contract, independent of source hashes.
Nothing here sends a real key, retrieves a native file or grants editing permission.
"""
import json
from bounded import require
from sources import sha,canonical
PREFIX='Document to be retrieved: ';CUE='(List Files)'
KINDS=('fresh-empty','fresh-whole-field-typed','missing-file-error-return')
def expected_line(kind,literal):
 require(kind in KINDS,'ContextKind','unsupported transition')
 require(type(literal)is str and all(' '<=c<='~'for c in literal)and len(literal)<=14,'LiteralBudget','closed short ASCII field')
 if kind=='fresh-empty':require(literal=='','ContextLiteral','fresh empty has no value')
 else:require(bool(literal),'ContextLiteral','populated state needs exact trace literal')
 line=PREFIX+literal
 return line.ljust(67)+CUE if kind!='fresh-whole-field-typed'else line

def classify(packet,expected,decoder):
 require(type(packet)is dict and set(packet)=={'id','authority','kind','literal','source_context','trace','text','vga_hex','cursor','custody'},'PacketSchema','exact packet fields')
 require(packet['authority']in ['existing-original','diagnostic','synthetic'],'PacketAuthority','explicit evidence class')
 require(packet['id']==expected['id'],'SourceWrapper','observation wrapper differs')
 require(packet['source_context']==expected['source_context'],'SourceContext','caller source/body/gap/mode/status/capture identity differs')
 require(packet['trace']==expected['trace'],'TraceContext','actual immutable source trace prefix differs')
 require(packet['kind']==expected['kind']and packet['literal']==expected['literal'],'TransitionContext','transition/literal must match source-bound caller')
 if expected['authority']=='diagnostic':require(packet['authority']!='existing-original','DiagnosticRelabel','failed51 captures never qualified reference positives')
 require(type(packet['text'])is str and len(packet['text'].encode())<=8192,'FrameBudget','text <=8KiB')
 require(type(packet['vga_hex'])is str and len(packet['vga_hex'])==8000,'VGAEnvelope','exact4000 bytes encoded hex')
 try:vga=bytes.fromhex(packet['vga_hex'])
 except ValueError:require(False,'VGAEnvelope','invalid hex')
 require(len(vga)==4000,'VGAEnvelope','exact4000 bytes')
 require(type(packet['cursor'])is dict and len(canonical(packet['cursor']))<=8192,'CursorSchema','cursor object <=8KiB')
 custody=dict(text_sha256=sha(packet['text'].encode()),vga_sha256=sha(vga),cursor_sha256=sha(canonical(packet['cursor'])))
 require(packet['custody']==custody,'LocalIntegrity','payload checksum mismatch')
 if packet['authority']!='synthetic':
  require(all(packet[k]==expected[k]for k in ['text','vga_hex','cursor']),'OriginalSourceBinding','rehashed payload differs from actual immutable original object')
 text=packet['text'];rows=text.split('\n');require(len(rows)==26 and rows[-1]=='' and '\r'not in text,'FrameShape','exact25 LF rows and trailingLF; RS is not a row')
 require(all(r==''for r in rows[:24]),'DocumentRows','body/status/modal/ruler rows differ')
 line=expected_line(expected['kind'],expected['literal']);require(rows[24]==line,'PromptShape','exact transition-specific field/cue differs')
 require(decoder.text(vga)==text,'VGAText','actual approved QMP.text disagrees with complete source text')
 require(vga[::2]==b' '*1920+line.ljust(80).encode('ascii'),'VGACharacters','raw padded characters differ; no NUL/space normalization authority')
 attrs=bytearray([0x17]*2000);bright=len(PREFIX+expected['literal']);attrs[1920:1920+bright]=bytes([0x1f])*bright
 if expected['kind']!='fresh-whole-field-typed':attrs[1920+68:1920+72]=bytes([0x1f])*4
 require(vga[1::2]==attrs,'VGAAttributes','closed original prompt/style cells differ')
 c=packet['cursor'];column=26+(len(expected['literal'])if expected['kind']=='fresh-whole-field-typed'else 0)
 for k,value in [('row',24),('column',column),('display_start_word',0),('cursor_word',1920+column),('selected_index',15)]:require(type(c.get(k))is int and c[k]==value,'CursorFrame',k)
 want={'10':13,'11':14,'12':0,'13':0,'14':(1920+column)>>8,'15':(1920+column)&255}
 require(type(c.get('crtc'))is dict and set(c['crtc'])==set(want)and all(type(c['crtc'][k])is int and c['crtc'][k]==v for k,v in want.items()),'CursorRegisters','CRTC fields disagree with source-bound field cursor')
 return dict(id=expected['id'],kind=expected['kind'],literal=expected['literal'],cursor=dict(row=24,column=column),all25_rows_VGA4000_CRTC_trace_context_match=True,evidence_class=packet['authority'],original_qualification=False,diagnosis_only=expected['authority']=='diagnostic',native_document_gap_inferred=False,original_source_bound=packet['authority']=='existing-original')

def rehash(packet):
 """Payload integrity only; callers cannot make original or semantic authority with it."""
 packet['custody']=dict(text_sha256=sha(packet['text'].encode()),vga_sha256=sha(bytes.fromhex(packet['vga_hex'])),cursor_sha256=sha(canonical(packet['cursor'])));return packet

def observations(idx,cache):
 records={};ref=idx['refs']['approved13']
 def raw(r,p):return cache[(r,p)]
 def make(ident,authority,r,path,kind,literal,trace,context):
  d=dict(id=ident,authority=authority,kind=kind,literal=literal,trace=trace,source_context=context,text=raw(r,path+'/screen.txt').decode(),vga_hex=raw(r,path+'/vram.bin').hex(),cursor=json.loads(raw(r,path+'/cursor.json')),custody={});records[ident]=rehash(d)
 for i in [1,2]:
  base=f'docs/research/continuation/session1/runs/2026-10-31-session1-b00-r{i}';run=json.loads(raw(ref,base+'/run.json'));env=json.loads(raw(ref,base+'/environment.json'));require(run['environment_manifest_sha256']==sha(raw(ref,base+'/environment.json')),'EnvironmentIdentity','recorded profile hash');require(run['run_id']==base.rsplit('/',1)[1]and run['branch']=='retrieve'and run['baseline_id']=='wp51-dos-us-1992-03-09'and not run['wordling_tested'],'RunIdentity','exact original-only recipe')
  require(all(run[k]is True for k in ['master_unchanged','fixture_unchanged','seed_unchanged']),'OriginalCustody','historical master/fixture/seed flags')
  trace=run['results'][0]['trace']
  for key in ['f1','esc']:
   for suffix,kind in [('prompt','fresh-empty'),('draft','fresh-whole-field-typed')]:
    label=f'retrieve-{key}-{suffix}';n=next(n for n,t in enumerate(trace)if t.get('capture')==label);prefix=trace[:n+1]
    if suffix=='prompt':require(trace[n-1]=={'key':'shift-f10'},'TracePredecessor','fresh prompt requires preceding ShiftF10');literal=''
    else:require(trace[n-1]=={'type':'B:\\MISSING'}and trace[n-2].get('capture')==f'retrieve-{key}-prompt','TracePredecessor','whole field typing from this fresh prompt');literal=trace[n-1]['type']
    ctx=dict(commit=ref,run_id=run['run_id'],case_id='CMD51-065',capture=label,profile_id=env['profile_id'],profile_sha256=run['environment_manifest_sha256'],available_seed_native=run['fixture'],document_source='blank original buffer; no successful Retrieve yet',document_body='',document_gap=None,document_mode='not witnessed in prompt',document_status='hidden by prompt',document_name=None)
    make(f'r{i}/{key}/{suffix}','existing-original',ref,base+'/CMD51-065/'+label,kind,literal,prefix,ctx)
  label='retrieve-retry-name';n=next(n for n,t in enumerate(trace)if t.get('capture')==label);require(trace[n-1].get('capture')=='retrieve-missing'and trace[n-2]=={'key':'ret'},'TracePredecessor','error-return requires failed Enter and error capture');require(b'ERROR: File not found'in raw(ref,base+'/CMD51-065/retrieve-missing/screen.txt'),'ErrorSource','actual missing-file context')
  ctx=dict(ctx,capture=label);make(f'r{i}/retry','existing-original',ref,base+'/CMD51-065/'+label,'missing-file-error-return','B:\\MISSING',trace[:n+1],ctx)
 ref=idx['refs']['frozen51'];b='internal/document/evidence/h1-admission-contract';run=json.loads(raw(ref,b+'/runs/wp51-h1-phase01/run.json'));handoff=json.loads(raw(ref,b+'/postrun/wp51-h1-phase01/failure-handoff-final.json'));require(run['new_attempts_spent']==1 and run['complete']is False and run['results'][0]['normal_DOS']is False and handoff['new_native_exports']==0,'FailureAccounting','permanent incomplete source, not a retrieval/edit witness')
 for label,kind,literal in [('013-retrieve-name-before','fresh-empty',''),('014-retrieve-name-after','fresh-whole-field-typed','C:\\OUT\\H1INPUT')]:
  trace=run['results'][0]['trace'];n=next(n for n,t in enumerate(trace)if t.get('capture')==label)
  ctx=dict(commit=ref,run_id='wp51-h1-phase01',case_id='wp51-empty-insert-and-reload-r1',capture=label,profile_id='historical51 frozen run only',document_source='NOT retrieved; failed before Enter',document_body='',document_gap=None,document_mode='not witnessed in prompt',document_status='hidden by prompt',document_name=None,whole_plan_permanently_halted=True)
  make('diagnosis/'+label,'diagnostic',ref,b+'/runs/wp51-h1-phase01/wp51-empty-insert-and-reload-r1/'+label,kind,literal,trace[:n+1],ctx)
 return records
