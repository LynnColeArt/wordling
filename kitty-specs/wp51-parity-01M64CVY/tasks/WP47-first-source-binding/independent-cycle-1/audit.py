import hashlib,json,subprocess
from pathlib import Path
R=Path.cwd(); O=Path('/tmp/wordling-wp47-independent')
def sha(b):return hashlib.sha256(b).hexdigest()
def git(p,rev='HEAD'):return subprocess.check_output(['git','show',rev+':'+p])
before=json.loads(Path('/tmp/wordling-WP47-before-currency-source.json').read_text());n=0
for p,e in before['inputs'].items():
 b=(R/p).read_bytes();assert len(b)==e['size'] and sha(b)==e['sha256'],p;assert git(p)==b,p;n+=1
m=json.loads((R/'internal/editor/evidence/wp47/manifest.json').read_text())
for p,e in m['files'].items():
 b=(R/p).read_bytes();assert {'size':len(b),'sha256':sha(b)}==e and git(p)==b,p
s=json.loads((R/'internal/editor/evidence/wp47/source-and-execution.json').read_text());f=json.loads((R/'internal/editor/evidence/wp47/final-source-sealed.json').read_text());changed=[]
for p,e in f['Go_and_module_inputs'].items():assert sha((R/p).read_bytes())==e['sha256'],p
for p,e in s['Go_and_module_inputs'].items():
 if sha((R/p).read_bytes())!=e['sha256']:changed.append(p)
assert changed==['internal/editor/new_binding_test.go'],changed
for pkg in s['compiled_project_packages']:
 for p in pkg['GoFiles']:
  name=str((Path(pkg['Dir'])/p).relative_to(R));assert sha((R/name).read_bytes())==s['Go_and_module_inputs'][name]['sha256']
assert sha((R/'internal/editor/evidence/wp47/component-producer.bin').read_bytes())==s['binary']['sha256']
for out in s['native_outputs']:
 b=(R/out['path']).read_bytes();assert len(b)==out['size'] and sha(b)==out['sha256']
for tree,rev in [('internal/storage','0df934ce3185d73ec53be6d887fba513b44ab803'),('internal/document','44aab36accdf14a370a67fd73945907871ab7193')]:
 names=subprocess.check_output(['git','ls-tree','-r','--name-only',rev,tree],text=True).splitlines()
 for p in names:
  if p.endswith('.go') and '/evidence/' not in p:assert git(p,rev)==(R/p).read_bytes(),p
print(json.dumps({'source_inputs':n,'manifest_records':len(m['files']),'final_Go_module_inputs':len(f['Go_and_module_inputs']),'compiled_files':sum(len(p['GoFiles']) for p in s['compiled_project_packages']),'postbuild_test_only_changes':changed,'source':'3937a3d549ea2933745a82118147654824698f25','code':'09db703822a97d41d9c4e4cd7a5e2f3c10d5f131','all_exact':True},indent=2))
