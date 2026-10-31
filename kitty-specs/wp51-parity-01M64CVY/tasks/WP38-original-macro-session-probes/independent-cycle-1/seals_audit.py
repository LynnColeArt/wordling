import hashlib,json,subprocess,sys
from pathlib import Path
root=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-p');out=root/'docs/research/continuation/macro-session'
seals=json.loads((out/'verification/source-seals.json').read_text())
for row in seals['files']:
 p=root/row['path'];raw=p.read_bytes();assert len(raw)==row['size'] and hashlib.sha256(raw).hexdigest()==row['sha256'],row['path'];blob=subprocess.check_output(['git','show','58eaf84:'+row['path']],cwd=root);assert blob==raw,row['path']
for row in seals['private_settings_verified']:
 p=Path(row['path']);raw=p.read_bytes();assert len(raw)==row['size'] and hashlib.sha256(raw).hexdigest()==row['sha256']
profile=json.loads((root/'docs/research/reference-environment/environment.json').read_text());expected={'boot.img':profile['master_boot_sha256'],'harddisk.img':profile['master_disk_sha256']}
diskpaths=set();sources=set();invocations=[]
for path in (out/'runs').glob('*/run.json'):
 r=json.loads(path.read_text());assert r['master_before']==r['master_after']==expected;assert r['shared_lock']=='/home/lynn/projects/wordling/research/cache/reference/session1.lock'
 sources.add(next(x['sha256'] for x in r['sources'] if x['path']=='scripts/reference/macro_session.py'))
 for sample in r['results']:
  argv=sample['qemu_argv'];drive=[x for x in argv if x.startswith('file=') and 'harddisk.img' in x];assert len(drive)==1 and drive[0] not in diskpaths;diskpaths.add(drive[0]);assert 'format=raw,if=ide,index=0' in drive[0]
  assert any(x=='unix:/home/lynn/projects/wordling/research/cache/reference/runtime/wp38/qmp.sock,server=on,wait=off'for x in argv)
  case=path.parent/sample['id'];exact=case/'macro-name-exact-before-return/screen.txt'
  if exact.exists():
   name='M38NONE'if sample['case']=='missing-name'else'M38';line=exact.read_text().splitlines()[-1];assert line=='Macro: C:\\OUT\\'+name,line;invocations.append({'run':r['run_id'],'sample':sample['id'],'exact_name':line})
assert len(diskpaths)==30 and len(seals['files'])==1869
for name,digest in expected.items():assert hashlib.sha256((Path('/home/lynn/projects/wordling/research/cache/reference/master')/name).read_bytes()).hexdigest()==digest
print(json.dumps({'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'source_seal_entries':len(seals['files']),'private_settings_hashed':len(seals['private_settings_verified']),'distinct_fresh_guest_disk_argv':len(diskpaths),'all_master_hashes_expected':True,'executing_runner_versions':sorted(sources),'exact_full_invocation_checks':invocations},indent=2))
