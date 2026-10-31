from pathlib import Path
import subprocess,json,hashlib,tempfile
ROOT=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-m');OUT=Path('/tmp/wordling-WP31-independent-review')
paths=['docs/conformance/v1/registry.json','docs/conformance/v1/index.md','docs/conformance/v1/imports/wp29/readiness.json']
original={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
with tempfile.TemporaryDirectory(prefix='WP31-independent-write-') as temp:
 root=Path(temp);subprocess.run(['git','init','-q',str(root)],check=True)
 common=subprocess.check_output(['git','rev-parse','--path-format=absolute','--git-common-dir'],cwd=ROOT,text=True).strip();(root/'.git/objects/info/alternates').write_text(common+'/objects\n')
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();subprocess.run(['git','read-tree',head],cwd=root,check=True)
 for path in paths:
  p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ROOT/path).read_bytes())
 rows=[]
 for i,command in enumerate(['write','write','check']):
  proc=subprocess.run(['python3',str(ROOT/'scripts/conformance/v1/ingest_wp29.py'),'--root',str(root),command],capture_output=True,text=True,timeout=120)
  rows.append({'command':command,'exit':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'hashes':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths}})
  assert proc.returncode==0,rows[-1];assert rows[-1]['hashes']==original
 assert {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}==original
 (OUT/'public-write-results.json').write_text(json.dumps({'isolated_object_store':True,'production_sources_touched':False,'rows':rows},indent=2)+'\n');print(json.dumps({'commands':3,'all_exit0':True,'write_write_check_hashes_unchanged':True}))
