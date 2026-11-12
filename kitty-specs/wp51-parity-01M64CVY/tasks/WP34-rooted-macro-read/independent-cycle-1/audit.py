import hashlib,json,subprocess
from pathlib import Path
root=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-b');p=root/'internal/storage/evidence/macro-read/artifact-manifest.json';raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()=='b6c948adfd85d75d57d935e48727e45f758c28bad543fbdeb1427f8e8201371d'
manifest=json.loads(raw)
for name,row in manifest['files'].items():
 actual=(root/name).read_bytes();assert len(actual)==row['size'] and hashlib.sha256(actual).hexdigest()==row['sha256'];assert subprocess.check_output(['git','rev-parse','HEAD:'+name],cwd=root,text=True).strip()==row['git_blob'];assert subprocess.check_output(['git','cat-file','blob',row['git_blob']],cwd=root)==actual
proof=json.loads((p.parent/'inherited-source-proof.json').read_text())
for row in proof:assert subprocess.check_output(['git','show',row['reference_commit']+':'+row['path']],cwd=root)==(root/row['path']).read_bytes()
ledger=json.loads((root/'internal/macro/wpm/testdata/original-fixtures.json').read_text());hashes=set()
for row in ledger['wpm_exports']:
 raw=(root/row['path']).read_bytes();assert len(raw)==row['size'] and hashlib.sha256(raw).hexdigest()==row['sha256'];assert subprocess.check_output(['git','cat-file','blob',row['git_blob']],cwd=root)==raw;hashes.add(row['sha256'])
assert len(ledger['wpm_exports'])==46 and len(hashes)==22
changed=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r','0793933'],cwd=root,text=True).splitlines();assert all(x.startswith('internal/storage/') for x in changed)
print(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'owned_artifact_seals':len(manifest['files']),'inherited_files_unchanged':len(proof),'original_macro_files':46,'distinct_original_hashes':22,'changed_owned_paths':len(changed),'manifest_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'all_checks_passed':True},indent=2))
