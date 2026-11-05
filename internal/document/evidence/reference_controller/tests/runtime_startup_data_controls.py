"""Twelve closed synthetic DATA controls of genuine old/new source predicates.
No runtime/proc/source-origin qualification; empty maps/modules isolate startup.
"""
from pathlib import Path
import importlib.util,importlib.machinery,json,copy,hashlib
T=Path(__file__).parent
F=Path('/tmp/wordling-WP70-startup-DATA-freeze-01')
def load(name,path):
 loader=importlib.machinery.SourceFileLoader(name,str(path));spec=importlib.util.spec_from_loader(name,loader);m=importlib.util.module_from_spec(spec);loader.exec_module(m);return m
old=load('historical_startup_V5',F/'old-helper.py.txt')
new=load('candidate_startup_V6',F/'new-helper.py.txt')
recorded=json.loads((F/'recorded-stdlib-before.stdout.raw').read_text())
base=copy.deepcopy(recorded);base['modules']={};base['maps']={};base['project']=None
interpreter=Path(recorded['executable']);expected=dict(files={},runtime_elf=[],runtime_mapped_data=[])
rows=[]
for n in range(12):
 d=copy.deepcopy(base);fn=new.compare_observation;want='RuntimeStartup';stage='startup'
 if n==0:fn=old.compare_observation
 elif n==1:want=None;stage='startup-with-synthetic-empty-origins'
 elif n in (2,3,4):d['flags']['int_max_str_digits']=(-1,0,4301)[n-2]
 elif n==5:del d['flags']['quiet']
 elif n==6:d['flags']['extra']=0
 elif n==7:d['flags']['isolated']=0
 elif n==8:d['default_excepthook']=False
 elif n==9:d['customize']['sitecustomize']=True
 elif n==10:d['features']['pidfd_open']=False
 elif n==11:
  d['modules']={'synthetic_unknown':{'__file__':{'exists':True,'path':'/definitely-unadmitted-synthetic-source.py','size':1,'sha256':'0'*64}}};want='UnexpectedModuleOrigin:synthetic_unknown:/definitely-unadmitted-synthetic-source.py';stage='later-module-origin'
 try:fn(d,interpreter,expected,{},False);actual=None
 except RuntimeError as ex:actual=str(ex)
 assert actual==want,(n,want,actual)
 rows.append(dict(id=n+1,status='EXPECTED_RED' if n==0 else 'PASS',reason=actual,stage=stage,input_sha256=hashlib.sha256(json.dumps(d,sort_keys=True).encode()).hexdigest()))
print(json.dumps(dict(groups=1,variants=rows,actual_recorded_projection_only=True,synthetic_empty_modules_maps=True,production_capture=False,TCB=False,P=False)))
