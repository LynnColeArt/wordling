"""Immutable public source custody; bounded Git object reads, no private file probing."""
from pathlib import Path
import hashlib,importlib.util,json,re,tempfile
from bounded import read_limited,process,require
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
INDEX_SHA='24c9b8922212bd43245a605dc63d04e73eff5bf6722e3b57cc0ff7f4ad9ac2e0'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(obj):return json.dumps(obj,sort_keys=True,separators=(',',':')).encode()
def index():
 raw=read_limited(HERE/'source-index.json',512*1024);require(sha(raw)==INDEX_SHA,'SourceIndexDrift','immutable finite source roster changed');obj=json.loads(raw)
 require(len(obj['files'])==1346,'SourceRoster','unique original source count');return obj

def pins_for_cases(idx):
 """Explicit small semantic subset; full audit still hashes every original evidence/image."""
 refs=idx['refs'];keys=set()
 for i in [1,2]:
  base=f'docs/research/continuation/session1/runs/2026-10-31-session1-b00-r{i}'
  for p in ['run.json','environment.json']:keys.add((refs['approved13'],base+'/'+p))
  for label in ['retrieve-f1-prompt','retrieve-f1-draft','retrieve-f1-cancel','retrieve-esc-prompt','retrieve-esc-draft','retrieve-esc-cancel','retrieve-missing','retrieve-retry-name']:
   for p in ['screen.txt','vram.bin','cursor.json']:keys.add((refs['approved13'],base+'/CMD51-065/'+label+'/'+p))
 b='internal/document/evidence/h1-admission-contract'
 for p in ['runs/wp51-h1-phase01/run.json','postrun/wp51-h1-phase01/failure-handoff-final.json','protocol.py','frames.py']:keys.add((refs['frozen51'],b+'/'+p))
 for label in ['013-retrieve-name-before','014-retrieve-name-after']:
  for p in ['screen.txt','vram.bin','cursor.json']:keys.add((refs['frozen51'],b+'/runs/wp51-h1-phase01/wp51-empty-insert-and-reload-r1/'+label+'/'+p))
 keys.add((idx['helper']['source_commit'],idx['helper']['path']));return keys

def load(full=False):
 idx=index();needed=pins_for_cases(idx);pins={(p['source_commit'],p['path']):p for p in [*idx['files'],idx['helper']]};require(needed<=pins.keys(),'SourceRoster','selected evidence missing')
 selected=sorted(pins)if full else sorted(needed);require(len(selected)<=1400,'SourceBudget','finite <=1400 public objects')
 request=b''
 for ref,path in selected:
  require(re.fullmatch('[0-9a-f]{40}',ref)is not None and '\n'not in path and '\r'not in path and not path.startswith('/')and'..'not in Path(path).parts,'SourcePath','literal immutable Git object selector')
  request+=(ref+':'+path+'\n').encode()
 total=sum(pins[k]['size']for k in selected);require(total<=40*1024*1024,'SourceBudget','finite accepted source bytes <=40MiB')
 raw,diag=process(['git','cat-file','--batch'],ROOT,request,timeout=30);pos=0;cache={};verified=[]
 for key in selected:
  end=raw.find(b'\n',pos);require(end>=pos,'SourceFraming','missing batch header');header=raw[pos:end].split();require(len(header)==3 and header[1]==b'blob','SourceFraming','expected complete blob');size=int(header[2]);pin=pins[key];require(size==pin['size'],'SourceSize',key[1]);pos=end+1
  require(pos+size<len(raw)and raw[pos+size]==10,'SourceFraming','truncated object');blob=raw[pos:pos+size];pos+=size+1;require(sha(blob)==pin['sha256'],'SourceHash',key[1]);require(not pin.get('git_blob')or header[0].decode()==pin['git_blob'],'SourceBlob',key[1]);verified.append(dict(commit=key[0],path=key[1],size=size,sha256=sha(blob),git_blob=header[0].decode()))
  if key in needed:cache[key]=blob
 require(pos==len(raw),'SourceFraming','unexpected extra object output')
 if full:
  for group in idx['inventory_roots']:
   members=[p for p in idx['files']if p['source_commit']==group['ref']and p['path'].startswith(group['root']+'/')and p['path'].endswith('/screen.txt')]
   require(len(members)==group['screen_count'],'InventoryCount',group['root'])
   # All records in those roots have no Retrieve cue; exact listed text is independently re-read.
   # Repeat a finite subset batch to check content, not just saved absence flags.
   requests=''.join(group['ref']+':'+p['path']+'\n'for p in members).encode();out,_=process(['git','cat-file','--batch'],ROOT,requests,timeout=20,stdout_limit=2*1024*1024)
   require(b'Document to be retrieved:'not in out,'InventoryChanged','intermediate prompt newly present in exact historical inventory')
 return idx,cache,dict(verified_unique_objects=len(selected),verified_bytes=total,inventory_screens=1085 if full else None,inventory_absence='inspected exact39/43/46 roots only'if full else'not audited in this command',git_stdout_bytes=len(raw),git_diagnostics=diag.decode(),selected_custody=verified)

class Decoder:
 """Execute actual approved QMP.text against a local immutable VGA replay only.
 The real helper is imported from its approved working-tree file, not an archive.
 No QMP enter/connection/guest/key/guard/ledger API is called.
 """
 def __init__(self,idx,cache):
  pin=idx['helper'];path=ROOT/pin['path'];raw=read_limited(path,8192);require(sha(raw)==pin['sha256']and raw==cache[(pin['source_commit'],pin['path'])],'HelperSourceDrift','actual QMP source differs from approved bytes')
  spec=importlib.util.spec_from_file_location('wordling_wp54_approved_qmp',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);self.module=module;self.pin=pin
 def text(self,vga):
  require(type(vga)is bytes and len(vga)==4000,'VGAEnvelope','exact4000 bytes')
  module=self.module
  class Replay(module.QMP):
   def hmp(self,command):
    match=re.fullmatch(r'pmemsave 0xb8000 4000 "([^"]+)"',command);require(match is not None,'HelperAPI','only exact local text-decode pmemsave request')
    target=Path(match[1]);require(target==self.allowed,'HelperPath','local replay target');target.write_bytes(vga);return ''
   def __enter__(self):raise AssertionError('NO GUEST')
  with tempfile.TemporaryDirectory(prefix='wordling-retrieve-decode-')as tmp:
   replay=Replay();replay.allowed=Path(tmp)/'vram.bin';text=replay.text(tmp)
  return text
 def provenance(self):return dict(api='QMP.text',actual_file=str(ROOT/self.pin['path']),source=self.pin,adapter='local VGA replay; hmp writes fixed4000B only; QMP.__enter__ never called',private_or_guest_access=False)
