"""Immutable source gates and actual WP54 PUBLIC CLI only. No private predicates."""
from pathlib import Path
import hashlib,importlib.util,json,sys,tempfile
from boundaries import read,process,parse,require
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
SOURCE54='656110db2f463c775e38809508815684bc44dad2';SOURCE51='5975c5f72775f3b3c07675ecb806c460886c9027';SOURCE13='18d6afe95ffcd676fc3f9e964dcad884c9a8c289'
PREFIX54='internal/document/evidence/retrieve-field-contract/';QMP='scripts/reference/qmp.py';QMP_SHA='dcb3aaa83c72b695f63a86529b25bc70fe26dd7e197fc27052effe8218f82304'
PINS={'oracle.py':'c9d9daef7179a9944df4654c51de4a166a4ce42b3290ec13e5f4a6edee5efa5f','field_contract.py':'ca58d05e5abef46daabf8b4acb2d084f10457cf9366e4ce8a1b648dd9155977f','sources.py':'42c845b1c8454e6bc6b4a8fab54859029d370ee1fa37be74d3661d31a5ac78ce','bounded.py':'b41c8a770e8da5fdc8339c7f6a43ee08a73e59992ea58101d9b19666b280c0f7','source-index.json':'24c9b8922212bd43245a605dc63d04e73eff5bf6722e3b57cc0ff7f4ad9ac2e0'}
def sha(b):return hashlib.sha256(b).hexdigest()
def verify():
 rows=[]
 for path,digest in [(PREFIX54+n,d)for n,d in PINS.items()]+[(QMP,QMP_SHA)]:
  ref=SOURCE13 if path==QMP else SOURCE54;raw=read(ROOT/path,512<<10);require(sha(raw)==digest,'ApprovedSourceDrift',path)
  original,_=process(['git','show',ref+':'+path],ROOT,stdout_limit=512<<10);require(original==raw,'ApprovedSourceGitDrift',path);rows.append(dict(path=path,source=ref,size=len(raw),sha256=digest))
 return rows
def public(*args):
 verify();raw,_=process([sys.executable,str(ROOT/PREFIX54/'oracle.py'),*args],ROOT,timeout=30);return parse(raw)
def packet(ident):return public('packet','--id',ident)
def inspect(packet):
 with tempfile.TemporaryDirectory(prefix='wp55-public54-')as t:
  p=Path(t)/'packet.json';p.write_text(json.dumps(packet));return public('inspect','--packet',str(p))
def decode(vga):
 """Actual approved13 QMP.text, local4000B replay; no guest/key/socket entry."""
 require(type(vga)is bytes and len(vga)==4000,'VGAEnvelope','exact rawVGA4000');require(sha(read(ROOT/QMP,8192))==QMP_SHA,'ApprovedSourceDrift',QMP)
 spec=importlib.util.spec_from_file_location('wp55_approved13_qmp',ROOT/QMP);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 class Replay(mod.QMP):
  def __enter__(self):raise AssertionError('NO GUEST')
  def key(self,*a):raise AssertionError('NO KEY')
  def hmp(self,command):
   require(command==f'pmemsave 0xb8000 4000 "{self.target}"','DecodeBoundary','only exact local replay');self.target.write_bytes(vga);return ''
 with tempfile.TemporaryDirectory(prefix='wp55-vga-')as t:
  q=Replay();q.target=Path(t)/'vram.bin';return q.text(t)
def fact_book():
 book={}
 for i in [1,2]:
  for suffix in ['prompt','draft']:
   ident=f'r{i}/f1/{suffix}';p=packet(ident);result=inspect(p);require(result['original_source_bound']and not result['original_qualification'],'Public54Evidence','fixture-bound evidence not new permission');book[ident]=p
 return book
