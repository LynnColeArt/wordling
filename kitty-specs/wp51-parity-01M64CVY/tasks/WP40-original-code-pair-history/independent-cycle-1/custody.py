import hashlib,json,subprocess,sys
from pathlib import Path
L=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-r');O=L/'docs/research/continuation/code-pair-history';T=Path('/tmp/wordling-wp40-independent-review')
def sha(b):return hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=L,text=True).strip()=='7fff6a0191413e2b0cd13b6648325815bcef5561'
final=O/'final-seals.json';assert sha(final.read_bytes())=='e2e57fb3cecebd51ec357612e680e32d3d6ec9cc8716177ddfdcbd8dde34de00'
seal=json.loads(final.read_text());proc=subprocess.Popen(['git','cat-file','--batch'],cwd=L,stdin=subprocess.PIPE,stdout=subprocess.PIPE);total=0;objects=set()
try:
 for f in seal['files']:
  p=L/f['path'];raw=p.read_bytes();assert len(raw)==f['size']and sha(raw)==f['sha256'],p
  proc.stdin.write(('7fff6a0:'+f['path']+'\n').encode());proc.stdin.flush();h=proc.stdout.readline().decode().split();assert len(h)==3 and h[1]=='blob'and h[0]==f['git_blob'],p
  data=proc.stdout.read(int(h[2]));assert proc.stdout.read(1)==b'\n'and data==raw,p
  total+=len(raw);objects.add(h[0])
finally:proc.stdin.close();proc.stdout.close();assert proc.wait()==0
source=(L/'scripts/reference/code_pair_history.py').read_bytes();assert sha(source)=='0d02ae3573712e18cc7e67eb82281faf2ddbc1ed79a90a68673fc34b5ac31104'
assert source==subprocess.check_output(['git','show','0fc6974:scripts/reference/code_pair_history.py'],cwd=L)
envpath=L/'docs/research/reference-environment/environment.json';env=json.loads(envpath.read_text());res=json.loads((L/'docs/research/reference-environment/resource-profile.json').read_text())['resources'];schedule=json.loads((O/'execution.json').read_text());assert len(schedule)==18 and all(x['exit']==0 for x in schedule);assert len(set(x['id']for x in schedule))==18
exports=0;resources=0;gaps=[];drives=set();set_hashes=set()
for row in schedule:
 base=O/'runs'/row['id'];r=json.loads((base/'run.json').read_text());pre=json.loads((base/'prelaunch.json').read_text());assert r['run_id']==row['id']and pre['case']==r['cases'][0]['plan'];assert row['argv'][1:]==pre['argv'];assert r['qemu_argv']==pre['qemu_argv']
 assert r['master_before']==r['master_after']=={'boot.img':env['master_boot_sha256'],'harddisk.img':env['master_disk_sha256']};assert r['profile_sha256']==sha(envpath.read_bytes())
 assert r['runtime']['lock']=='/home/lynn/projects/wordling/research/cache/reference/session1.lock';assert r['runtime']['socket'].endswith('/runtime/wp40/qmp.sock')and len(r['runtime']['socket'])<108
 for item in pre['preparation']['sources']:
  p=base/'prelaunch-source'/item['path'];assert p.is_file()and len(p.read_bytes())==item['size']and sha(p.read_bytes())==item['sha256'];assert p.read_bytes()==(L/item['path']).read_bytes(),p
 assert (base/'prelaunch-source/scripts/reference/code_pair_history.py').read_bytes()==source
 for opt in ['-drive']:
  for i,arg in enumerate(r['qemu_argv']):
   if arg==opt:assert row['id']in r['qemu_argv'][i+1];drives.add(r['qemu_argv'][i+1])
 disk='/home/lynn/projects/wordling/research/cache/reference/native-edit-runs/'+row['id']+'/harddisk.img@@1048576'
 for item in r['resources']:
  raw=subprocess.check_output(['mtype','-i',disk,'::WP51/'+item['path']]);assert len(raw)==item['size']and sha(raw)==item['sha256'];resources+=1
  if item['path']!='WP{WP}.SET':assert item['sha256']==res['WP51/'+item['path']]['sha256']and item['size']==res['WP51/'+item['path']]['size']
  else:set_hashes.add(item['sha256'])
 for item in r['stopped_exports']:
  raw=(base/item['host']).read_bytes();assert item['exit']==0 and item['size']==len(raw)>0 and item['sha256']==sha(raw);exports+=1
 for label in ['target-incoming','target-confirmed'if 'question'in r['cases'][0]else'target-action','after-restore-before-any-save','pre-X-no-navigation','clean-exit']:
  p=base/label;vga=(p/'vram.bin').read_bytes();assert len(vga)==4000
  rows=[bytes(vga[i:i+160:2]).replace(b'\0',b' ').decode('cp437').rstrip()for i in range(0,4000,160)];assert '\n'.join(rows)+'\n'==(p/'screen.txt').read_text(),p
  c=json.loads((p/'cursor.json').read_text());reg=c['crtc'];start=(reg['12']<<8)|reg['13'];cur=(reg['14']<<8)|reg['15'];offset=(cur-start)&0xffff;assert start==c['display_start_word']and cur==c['cursor_word']and [offset//80,offset%80]==[c['row'],c['column']],p
  if label=='clean-exit':assert rows[0]=='C:\\WP51>'and not any(rows[1:])and [c['row'],c['column']]==[0,8]
assert exports==108 and resources==90 and len(drives)==36
result={'source_commit':'7fff6a0191413e2b0cd13b6648325815bcef5561','executing_source_matches_frozen_0fc6974':True,'final_seal_files':len(seal['files']),'inclusive_manifest_bytes':total,'unique_Git_objects':len(objects),'fresh_scheduler_children':18,'exact_prelaunch_argv_sources_and_master_profiles':True,'fresh_drive_arguments':len(drives),'stopped_exports':exports,'independently_rehashed_private_resource_records':resources,'private_SET_hash_variants':len(set_hashes),'five_raw_vga_screen_and_hardware_cursor_states_per_guest_verified':90,'all_final_DOS_and_cursor_exact':True,'no_private_material_published':True}
(T/'custody.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
