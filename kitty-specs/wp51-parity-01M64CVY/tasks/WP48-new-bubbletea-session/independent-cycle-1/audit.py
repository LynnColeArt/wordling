import json,subprocess,hashlib
from pathlib import Path
r=Path.cwd();o=Path('/tmp/wordling-wp48-independent');h=r/'docs/research/continuation/new-session'
def d(b):return {'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
e=json.loads(Path('/tmp/wordling-WP48-before-currency-source.json').read_text())
for p,w in e['inputs'].items():
 b=(r/p).read_bytes();assert d(b)=={k:w[k] for k in ['size','sha256']};assert subprocess.check_output(['git','show','HEAD:'+p])==b
s=json.loads((h/'build-final/source.json').read_text());assert d((h/'build-final/wordling.bin').read_bytes())==s['binary']
for p,w in s['actual_compiled_project_inputs'].items():assert d((r/p).read_bytes())==w
assert {str(p.relative_to(r)):d(p.read_bytes()) for pre in ['internal','cmd'] for p in (r/pre).rglob('*.go')}==s['complete_local_Go_SET']
for pre,rev in [('internal/editor','3937a3d549ea2933745a82118147654824698f25'),('internal/document','44aab36accdf14a370a67fd73945907871ab7193'),('internal/storage','0df934ce3185d73ec53be6d887fba513b44ab803')]:
 for p in subprocess.check_output(['git','ls-tree','-r','--name-only',rev,pre],text=True).splitlines():
  if p.endswith('.go') and '/evidence/'not in p:assert subprocess.check_output(['git','show',rev+':'+p])==(r/p).read_bytes(),p
process=[]
for stage in ['pty-01','pty-02','pty-final']:
 for p in sorted((h/stage).glob('*/result.json')):
  a=json.loads(p.read_text());process.append((stage,p.parent.name,a['failure']))
  for n,w in a['files'].items():assert d((p.parent/'files'/n).read_bytes())==w
  assert a['binary']==d(Path(a['argv'][0]).read_bytes())
  if a['failure'] is None:assert a['termios_restored'] and a['returncode']==a['expected_exit']
  assert (p.parent/'wire-output.bin').stat().st_size>0 and (p.parent/'frames.json').exists()
print(json.dumps({'source_inputs':len(e['inputs']),'current_Go_SET':len(s['complete_local_Go_SET']),'compiled_project_module_inputs':len(s['actual_compiled_project_inputs']),'historical_and_final_processes':len(process),'successes':sum(x[2]is None for x in process),'preserved_failures':[x[:2] for x in process if x[2]is not None],'all_source_and_raw_pins_exact':True},indent=2))
