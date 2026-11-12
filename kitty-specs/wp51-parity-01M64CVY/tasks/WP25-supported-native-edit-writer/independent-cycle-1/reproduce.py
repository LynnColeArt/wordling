import contextlib,hashlib,io,json,runpy,shutil,subprocess
from pathlib import Path
root=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-e');out=Path('/tmp/wordling-wp25-independent');here=root/'internal/document/evidence/wp25'
mod=runpy.run_path(str(here/'audit.py'))
# Preserve actual input paths and the original helper's internal-import placement.
# Redirect only the audit's known derived write targets to /tmp.
original_write=Path.write_text
protected={here/'revision-fix-document-reopen.json',here/'revision-fix-audit.json'}
def redirected_write(path,*args,**kwargs):
 target=out/path.name if path in protected else path
 return original_write(target,*args,**kwargs)
Path.write_text=redirected_write
try:
 with (out/'audit-run.txt').open('w')as log,contextlib.redirect_stdout(log):result=mod['audit'](True)
finally:Path.write_text=original_write
(out/'revision-fix-audit.json').write_text(json.dumps(result,indent=2)+'\n')
module=out/'producer-module';module.mkdir();(module/'internal/document/evidence/wp25/producer').mkdir(parents=True);(module/'internal/wp51').mkdir(parents=True)
for filename in ['go.mod','go.sum']:
 path=root/filename
 if path.exists():shutil.copyfile(path,module/filename)
copy_paths=list((root/'internal/document').glob('*.go'))+[root/'internal/wp51/native.go',here/'producer/main.go'];sources=[]
for path in copy_paths:
 relative=path.relative_to(root);destination=module/relative;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,destination);assert destination.read_bytes()==path.read_bytes();sources.append({'path':str(relative),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(module/'docs').symlink_to(root/'docs',target_is_directory=True)
argv=['go','run','./internal/document/evidence/wp25/producer','--out','internal/document/evidence/wp25/independent-candidates']
p=subprocess.run(argv,cwd=module,capture_output=True,text=True);(out/'producer.txt').write_text(p.stdout+p.stderr);assert p.returncode==0
candidates=[]
for path in sorted((module/'internal/document/evidence/wp25/independent-candidates').glob('*/candidate.WP5')):
 kind=path.parent.name;raw=path.read_bytes();old=(here/'candidates'/kind/'candidate.WP5').read_bytes();fixed=(here/'revision-fixed-candidates'/kind/'candidate.WP5').read_bytes();assert raw==old==fixed
 candidates.append({'kind':kind,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'independent_final_source_emission_equal_to_tested_and_fixed':True})
assert len(candidates)==5
(out/'reproduction-summary.json').write_text(json.dumps({'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'audit':result,'producer_command':argv,'temporary_module_production_source_copies':sources,'candidates':candidates},indent=2)+'\n')
print(result)
