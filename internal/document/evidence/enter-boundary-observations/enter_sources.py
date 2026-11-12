"""Exact approved public function bindings; own modules deliberately use enter_* names."""
from pathlib import Path
import ast,hashlib,importlib,inspect,json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SAFE=ROOT/'internal/document/evidence/retrieve-field-observations'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def bootstrap():
 manifest=json.loads((HERE/'sources.json').read_bytes());pin=manifest['files']['internal/document/evidence/retrieve-field-observations/boundaries.py'];path=SAFE/'boundaries.py'
 if sha(path.read_bytes())!=pin['sha256']:raise ValueError('BootstrapSourceDrift')
 existing=sys.modules.get('boundaries')
 if existing is not None and Path(existing.__file__).resolve()!=path:raise ValueError('ImportCollision: boundaries')
 sys.path.insert(0,str(SAFE));b=importlib.import_module('boundaries')
 if Path(b.__file__).resolve()!=path:raise ValueError('ImportCollision: boundaries')
 return b
B=bootstrap()
def verify():
 obj=B.parse(B.read(HERE/'sources.json'));pins=obj['files'];B.require(len(pins)<=64 and sum(r['size']for r in pins.values())<=8<<20,'SourceBudget','closed64/8MiB safety/native source roster')
 req=''.join(r['commit']+':'+p+'\n'for p,r in pins.items()).encode();raw,_=B.process(['git','cat-file','--batch'],ROOT,req,stdout_limit=8<<20);pos=0
 for path,pin in pins.items():
  end=raw.index(b'\n',pos);blob,kind,n=raw[pos:end].split();n=int(n);pos=end+1;data=raw[pos:pos+n];pos+=n;B.require(raw[pos:pos+1]==b'\n','SourceGitFrame',path);pos+=1;B.require(kind==b'blob'and blob.decode()==pin['git_blob']and len(data)==pin['size']and sha(data)==pin['sha256'],'SourceGitDrift',path);B.require(B.read(ROOT/path,4<<20)==data,'SourceWorkingDrift',path)
 B.require(pos==len(raw),'SourceGitFrame','exact end');return obj
_loaded=None
def interfaces():
 global _loaded
 verify()
 if _loaded is not None:return _loaded
 # Ordinary approved imports only. Existing collisions refuse rather than patching module registries.
 expected={n:SAFE/(n+'.py')for n in ['boundaries','approved','oracle','peer','stopping','account','native']}
 for n,p in expected.items():
  prior=sys.modules.get(n);B.require(prior is None or Path(prior.__file__).resolve()==p,'ImportCollision',n)
 loaded={n:importlib.import_module(n)for n in expected}
 for n,p in expected.items():B.require(Path(loaded[n].__file__).resolve()==p,'ImportBinding',n)
 cls=loaded['account'].owned_file_class() # Public class-loader only; NO file/ledger constructor here.
 frames=sys.modules['frames'];B.require(Path(frames.__file__).resolve()==ROOT/'internal/document/evidence/h1-admission-contract/frames.py','ImportBinding','approved51 frames')
 session=importlib.import_module('macro_session');B.require(Path(session.__file__).resolve()==ROOT/'scripts/reference/macro_session.py','ImportBinding','macro_session')
 _loaded=dict(**loaded,OwnedFile=cls,session=session);return _loaded

def contract():
 mods=interfaces();fn=mods['session'].fresh_start;sig=inspect.signature(fn);source=inspect.getsource(fn);tree=ast.parse(source);calls=[]
 for node in ast.walk(tree):
  if isinstance(node,ast.Call)and isinstance(node.func,ast.Attribute)and isinstance(node.func.value,ast.Name)and node.func.value.id=='subprocess'and node.func.attr=='run':
   kw={x.arg:ast.unparse(x.value)for x in node.keywords};calls.append(dict(line=fn.__code__.co_firstlineno+node.lineno-1,args=[ast.unparse(a)for a in node.args],keywords=kw,inner_stdout_stderr_byte_cap=None,executor_parameter=False))
 missing=['bounded_runner','launch_observer','prepared_resources'];rejected={}
 for name in missing:
  try:sig.bind(None,None,None,[],**{name:object()});rejected[name]=False
  except TypeError:
   try:fn(None,None,None,[],**{name:object()});raise AssertionError('unsupported keyword unexpectedly entered actual public helper')
   except TypeError as error:B.require('unexpected keyword argument'in str(error),'PublicABI','actual call refused at argument binding before private body');rejected[name]=True
 B.require(all(rejected.values())and bool(calls),'SourceContractChanged','reassess exact public startup contract; never auto-enable originals')
 launch_line=next(x['line']for x in calls if x['args']==['argv']);copies=[fn.__code__.co_firstlineno+n.lineno-1 for n in ast.walk(tree)if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and isinstance(n.func.value,ast.Name)and n.func.value.id=='shutil'and n.func.attr=='copyfile'];B.require(copies and max(copies)<launch_line,'SourceOrder','actual master copy precedes launch')
 return dict(signature=str(sig),source_file=str(Path(inspect.getsourcefile(fn)).relative_to(ROOT)),source_function_sha256=sha(source.encode()),direct_subprocess_calls=calls,unsupported_parameters=rejected,private_master_checks_and_copies_precede_launch=bool(copies and max(copies)<launch_line),launch_callback_after_subprocess_only='StartupQMP.QMP() enters after launch subprocess returned',declaration='timeout15/RSS/outer pipe caps do not establish separate inner captured stdout/stderr byte caps',minimal_prerequisite=['approved public bounded subprocess runner injection for EVERY internal external process, with byte caps/group ownership/cleanup result','source-bound launch-stage observer/receipt BEFORE invocation and after actual owned identity or explicit unknown','public prepared-resource/identity seam or equally safe test mode enabling actual harmless OS startup path without private-master reads/private-global patches'],run_enabled=False)
