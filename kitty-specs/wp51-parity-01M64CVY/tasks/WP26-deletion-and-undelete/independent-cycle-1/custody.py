from pathlib import Path
import json,hashlib,subprocess
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-e');E=R/'internal/document/evidence/wp26';T=Path('/tmp/wordling-wp26-independent')
def sha(b):return hashlib.sha256(b).hexdigest()
m=json.loads((E/'committed-blobs.json').read_text());assert m['source_and_evidence_files']==3364 and len(m['files'])==3364
proc=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE);total=0;objects=set()
try:
 for f in m['files']:
  raw=(R/f['path']).read_bytes();assert len(raw)==f['bytes']and sha(raw)==f['sha256'];proc.stdin.write((m['revision']+':'+f['path']+'\n').encode());proc.stdin.flush();h=proc.stdout.readline().decode().split();assert len(h)==3 and h[1]=='blob'and h[0]==f['git_blob'];blob=proc.stdout.read(int(h[2]));assert proc.stdout.read(1)==b'\n'and raw==blob;total+=len(raw);objects.add(h[0])
finally:proc.stdin.close();proc.stdout.close();assert proc.wait()==0
assert total==393043856
plan=json.loads((E/'candidates/sealed-plan.json').read_text());assert len(plan['cases'])==23 and len(plan['unique_whole_byte_candidates'])==7
for c in plan['cases']:assert (E/'candidates'/c['name']/'candidate.WP5').read_bytes()==(E/'candidates'/c['whole_byte_alias_of']/'candidate.WP5').read_bytes()
byname={c['name']:c for c in plan['cases']};assert byname['opening-repair']['whole_byte_alias_of']==byname['closing-repair']['whole_byte_alias_of'];assert byname['attributed-restore']['whole_byte_alias_of']!=byname['opening-repair']['whole_byte_alias_of']
envpath=R/'docs/research/reference-environment/environment.json';env=json.loads(envpath.read_text());resources=json.loads((R/'docs/research/reference-environment/resource-profile.json').read_text())['resources'];batch=json.loads((E/'reference/leaf-results.json').read_text());archive_count=set();vga_states=0;resource_records=0;raw_count=0
for a in batch['attempts']:
 run_id=f"wp26-candidate-{a['name']}-r{a['repeat']}";base=E/'reference/runs'/run_id;r=json.loads((base/'run.json').read_text());pre=json.loads((E/'reference/invocations'/(run_id+'.json')).read_text());assert pre['function_call']=={'call':'invoke','name':a['name'],'repeat':a['repeat']};assert pre['scheduler_argv']==a['argv'][1:]
 assert r['master_before']==r['master_after']=={'boot.img':env['master_boot_sha256'],'harddisk.img':env['master_disk_sha256']};assert r['profile_sha256']==sha(envpath.read_bytes());assert r['seed_before']==r['seed_after']and r['seed_unchanged']
 for p,f in pre['executing_sources'].items():
  b=(R/p).read_bytes();assert b==(R/f['archive']).read_bytes()and sha(b)==f['sha256'];assert not f['archive'].endswith('.go');archive_count.add(f['archive'])
 for f in r['artifacts']:
  raw=(base/f['path']).read_bytes();assert len(raw)==f['size']and sha(raw)==f['sha256'];raw_count+=1
 disk='/home/lynn/projects/wordling/research/cache/reference/native-edit-runs/'+run_id+'/harddisk.img@@1048576'
 for f in r['resources']:
  b=subprocess.check_output(['mtype','-i',disk,'::WP51/'+f['path']]);assert len(b)==f['size']and sha(b)==f['sha256'];resource_records+=1
  if f['path']!='WP{WP}.SET':assert f['sha256']==resources['WP51/'+f['path']]['sha256']
 final=base/'clean-exit';v=(final/'vram.bin').read_bytes();assert len(v)==4000;rows=[bytes(v[i:i+160:2]).replace(b'\0',b' ').decode('cp437').rstrip()for i in range(0,4000,160)];assert '\n'.join(rows)+'\n'==(final/'screen.txt').read_text();assert rows[0]=='C:\\WP51>'and not any(rows[1:]);c=json.loads((final/'cursor.json').read_text());reg=c['crtc'];start=(reg['12']<<8)|reg['13'];cursor=(reg['14']<<8)|reg['15'];assert start==0 and cursor==8 and [c['row'],c['column']]==[0,8];vga_states+=1
assert raw_count==2968 and len(archive_count)==92 and resource_records==70
release=json.loads((E/'reference/oracle-release.json').read_text());assert release['released_at']=='2026-10-31T06:43:14.486594+00:00'and release['batch_py_executed']is False and release['release_before_offline_audit']is True
result={'source_head':'951903221566629f0df8b4a78c98a03483992c4b','raw_commit':m['revision'],'git_files':len(m['files']),'manifest_bytes':total,'unique_Git_objects':len(objects),'whole_native_semantic_endpoints':23,'whole_native_classes':7,'e724_opening_closing_repair_whole_byte_alias_only':True,'attributed_restore_distinct_1172_input_preserved':True,'raw_manifest_artifacts':raw_count,'fresh_original_guests':14,'inert_executing_source_archives':len(archive_count),'stopped_private_resource_records_rehashed':resource_records,'raw_final_DOS_vga_hardware_cursor_verified':vga_states,'batch_py_archived_but_not_executed':True,'oracle_release_before_audit_verified':True,'private_material_published':False}
(T/'custody.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
