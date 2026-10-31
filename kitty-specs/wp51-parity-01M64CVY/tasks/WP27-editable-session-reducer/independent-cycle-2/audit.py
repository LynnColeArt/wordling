import hashlib,json,subprocess
from pathlib import Path
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-g'); E=R/'internal/editor/evidence/wp27'; out={}
for label,commit,manifest in [('current','5d5c767f834540149467f013ad69301775712777','fix-i1/artifact-manifest.json'),('historical','8b0a8ed6aa4cde4bff6a1efc15750b3125e6d17e','artifact-manifest.json')]:
 m=json.loads((E/manifest).read_text()); rows=m['records']
 for i in rows:
  raw=subprocess.check_output(['git','show',commit+':'+i['path']],cwd=R)
  assert len(raw)==i['size'] and hashlib.sha256(raw).hexdigest()==i['sha256'],i['path']
  assert subprocess.check_output(['git','hash-object','--stdin'],input=raw,cwd=R).decode().strip()==i['git_blob']
  if label=='current':assert (R/i['path']).read_bytes()==raw,i['path']
 out[label]=len(rows)
for p,h in json.loads((E/'fix-i1/final-inputs.json').read_text()).items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h,p
for i in json.loads((E/'dependency-equality.json').read_text()):assert (R/i['path']).read_bytes()==subprocess.check_output(['git','show',i['approved_commit']+':'+i['path']],cwd=R)
print(json.dumps(out|{'final_inputs_and_dependencies_match':True}))
