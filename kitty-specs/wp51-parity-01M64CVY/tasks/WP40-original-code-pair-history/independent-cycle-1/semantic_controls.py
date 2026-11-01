from pathlib import Path
import sys,json,shutil,tempfile,hashlib
L=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-r');O=L/'docs/research/continuation/code-pair-history';sys.path.insert(0,str(O));import audit as a
results=[]
with tempfile.TemporaryDirectory(prefix='wp40-independent-wire-')as tmp:
 root=Path(tmp);(root/'runs').mkdir()
 case='wp40-direct-normal-delete-on-r1'
 for p in (O/'runs').iterdir():
  if p.name==case:shutil.copytree(p,root/'runs'/p.name)
  else:(root/'runs'/p.name).symlink_to(p,target_is_directory=True)
 base=root/'runs'/case;wire=base/'qmp-wire.jsonl';rows=[json.loads(x)for x in wire.read_text().splitlines()];captured=False;changed=False
 for row in rows:
  if row['direction']!='tx-buffer':continue
  cmd=json.loads(bytes.fromhex(row['raw_hex']))
  if '/target-confirmed/'in json.dumps(cmd):captured=True
  elif captured and cmd.get('arguments',{}).get('command-line','').startswith('sendkey '):
   assert cmd['arguments']['command-line']=='sendkey f1 80';cmd['arguments']['command-line']='sendkey right 80';row['raw_hex']=json.dumps(cmd,separators=(',',':')).encode().hex();changed=True;break
 assert changed;wire.write_text(''.join(json.dumps(x)+'\n'for x in rows));report=base/'run.json';r=json.loads(report.read_text())
 for item in r['artifacts']:
  if item['path']=='qmp-wire.jsonl':item['size']=wire.stat().st_size;item['sha256']=hashlib.sha256(wire.read_bytes()).hexdigest()
 report.write_text(json.dumps(r))
 try:a.observe(root)
 except a.driver.Refusal as e:assert e.code=='HistoryInterleaving';results.append({'mutation':'actual next raw QMP key f1→right, envelope rehashed','code':e.code,'assertion':'real observe comparator rejects hidden immediate-input interleaving'})
 else:raise AssertionError('actual wire mutant survived')
base=O/'runs/wp40-closing-block-repair-yes-r1';r=json.loads((base/'run.json').read_text());case=r['cases'][0];stream=(base/case['interop']['print_stream']).read_bytes();body=bytes.fromhex(a.native.inspect(a.native.bounded_native(base/case['interop']['after_print']),False)['body_hex']);assert len(stream)==164
bad=stream.replace(b' '*11+b'BC'+a.print_audit.__globals__['SUFFIX'],b' '*12+b'BC'+a.print_audit.__globals__['SUFFIX'])
assert bad!=stream
try:a.print_audit(case['id'],body,bad)
except ValueError as e:results.append({'mutation':'actual164B closing stream overstrike shifted one space','code':type(e).__name__,'assertion':'owned exact-stream comparator refuses changed BC placement'})
else:raise AssertionError('actual stream mutant survived')
Path('/tmp/wordling-wp40-independent-review/semantic-controls.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
