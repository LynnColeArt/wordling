import contextlib,hashlib,io,json,runpy,shutil,tempfile
from pathlib import Path
root=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-p');source=root/'docs/research/continuation/macro-session';results=[]
for variant in ['rehashed-native-target','rehashed-wrapped-heartbeat','rehashed-F1-before-live-witness']:
 with tempfile.TemporaryDirectory(prefix='wp38-review-')as tmp:
  out=Path(tmp)
  for path in source.iterdir():
   if path.name not in ['audit.json','audit.xml','runs']:(out/path.name).symlink_to(path,target_is_directory=path.is_dir())
  (out/'runs').mkdir();chosen='wp38-stop-on-02'
  for path in (source/'runs').iterdir():
   if path.name==chosen:shutil.copytree(path,out/'runs'/path.name)
   else:(out/'runs'/path.name).symlink_to(path,target_is_directory=True)
  base=out/'runs'/chosen;manifest=base/'run.json';r=json.loads(manifest.read_text());case=base/'stop-on-1'
  if variant=='rehashed-native-target':
   changed=case/'D1AFTER.WP5';data=changed.read_bytes();assert b'USERREADY'in data;changed.write_bytes(data.replace(b'USERREADY',b'USERREADQ'))
  elif variant=='rehashed-wrapped-heartbeat':
   changed=case/'running-heartbeat-b/screen.txt';lines=changed.read_text().splitlines();lines[1]='extra document row';changed.write_text('\n'.join(lines)+'\n')
  else:
   changed=case/'qmp-wire.jsonl';lines=changed.read_text().splitlines();i=next(i for i,line in enumerate(lines)if json.loads(line)['direction']=='tx-buffer'and 'sendkey f1 80'in bytes.fromhex(json.loads(line)['raw_hex']).decode());f1=lines.pop(i);j=next(i for i,line in enumerate(lines)if 'running-heartbeat-b/'in bytes.fromhex(json.loads(line)['raw_hex']).decode(errors='replace'));lines.insert(j,f1);changed.write_text('\n'.join(lines)+'\n')
  relative=str(changed.relative_to(base));entry=next(x for x in r['artifacts']if x['path']==relative);entry.update(size=changed.stat().st_size,sha256=hashlib.sha256(changed.read_bytes()).hexdigest());manifest.write_text(json.dumps(r))
  module=runpy.run_path(str(source/'audit_results.py'));module['main'].__globals__['OUT']=out
  try:
   with contextlib.redirect_stdout(io.StringIO()):module['main']()
  except AssertionError as error:
   message=str(error);assert 'Raw evidence changed'not in message,message;results.append({'variant':variant,'rehash_valid':True,'rejected':True,'reason':message})
  else:raise AssertionError('False evidence accepted '+variant)
print(json.dumps(results,indent=2))
