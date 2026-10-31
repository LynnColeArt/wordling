import hashlib,json,subprocess
from pathlib import Path
ROOT=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-g');HERE=ROOT/'internal/editor/evidence/wp27';rows=[]
for item in json.loads((HERE/'artifact-manifest.json').read_text())['records']:
 raw=(ROOT/item['path']).read_bytes();blob=subprocess.check_output(['git','show','8b0a8ed6aa4cde4bff6a1efc15750b3125e6d17e:'+item['path']],cwd=ROOT)
 assert raw==blob and len(raw)==item['size']and hashlib.sha256(raw).hexdigest()==item['sha256'];assert subprocess.check_output(['git','hash-object','--stdin'],input=raw,cwd=ROOT,text=False).decode().strip()==item['git_blob'];rows.append(item['path'])
for item in json.loads((HERE/'dependency-equality.json').read_text()):
 raw=(ROOT/item['path']).read_bytes();blob=subprocess.check_output(['git','show',item['approved_commit']+':'+item['path']],cwd=ROOT);assert raw==blob and hashlib.sha256(raw).hexdigest()==item['sha256']
for path,digest in json.loads((HERE/'final-inputs.json').read_text()).items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
print(json.dumps({'source':'8b0a8ed6aa4cde4bff6a1efc15750b3125e6d17e','artifact_Git_seals':len(rows),'all_dependencies_and_final_inputs_match':True}))
