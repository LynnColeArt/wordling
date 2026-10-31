#!/usr/bin/env python3
"""Reproduce source lineage, actual immutable dependencies and artifact Git seals."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
checks=[]
for commit,directory in [('5d5c767','internal/editor'),('9519032','internal/document'),('5ad84e4','internal/storage')]:
    subprocess.run(['git','merge-base','--is-ancestor',commit,'HEAD'],cwd=ROOT,check=True)
    for p in sorted((ROOT/directory).glob('*.go')):
        if p.name.endswith('_test.go'):continue
        path=str(p.relative_to(ROOT));approved=subprocess.check_output(['git','show',commit+':'+path],cwd=ROOT)
        assert p.read_bytes()==approved,path;checks.append({'path':path,'approved_commit':commit,'sha256':hashlib.sha256(approved).hexdigest()})
for name in ['go.mod','go.sum']:
    assert (ROOT/name).read_bytes()==subprocess.check_output(['git','show','72369db:'+name],cwd=ROOT),name
manifest=HERE/'artifact-manifest.json'
if manifest.exists():
    for row in json.loads(manifest.read_text())['records']:
        p=ROOT/row['path'];raw=p.read_bytes();assert len(raw)==row['size'] and hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
        blob=subprocess.check_output(['git','hash-object','--stdin'],input=raw,cwd=ROOT).decode().strip();assert blob==row['git_blob'],row['path']
        assert subprocess.check_output(['git','show','HEAD:'+row['path']],cwd=ROOT)==raw,row['path']
print(json.dumps({'approved_production_dependencies':checks,'module_72369db_exact':True,'artifact_seals_checked':manifest.exists()},indent=2))
