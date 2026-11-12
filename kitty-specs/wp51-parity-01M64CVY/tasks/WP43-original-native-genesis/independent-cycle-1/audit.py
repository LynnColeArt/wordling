from pathlib import Path
import sys,json,hashlib,subprocess
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-t');O=R/'docs/research/continuation/native-genesis';T=Path('/tmp/wordling-wp43-independent');sys.path[:0]=[str(R/'scripts/reference'),str(O/'analysis')]
import native_genesis as g,probe_audit as a
h=lambda b:hashlib.sha256(b).hexdigest()
def save(n,v):(T/n).write_text(json.dumps(v,indent=2)+'\n')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()=='90ea1d4f4912e032061baccc6500f4d9ea232415'
# Actual unchanged public result/audit invokes the production Go reader and strict raw-Git/state auditor.
x=a.audit();assert x['reader_paths']==20 and x['Git_raw_files_verified']==2862;save('actual-audit.json',x)
seal=json.loads((O/'analysis/final-source-seals.json').read_text());files=seal['files'];assert len(files)==3004
byid={}
for f in files:byid.setdefault(f['git_blob'],[]).append(f)
p=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
for oid,rows in byid.items():
 p.stdin.write((oid+'\n').encode());p.stdin.flush();head=p.stdout.readline().split();assert len(head)==3 and head[1]==b'blob';size=int(head[2]);b=p.stdout.read(size);assert p.stdout.read(1)==b'\n'
 for f in rows:
  assert (R/f['path']).read_bytes()==b and len(b)==f['size'] and h(b)==f['sha256']
  actual=subprocess.check_output(['git','rev-parse','HEAD:'+f['path']],cwd=R,text=True).strip();assert actual==oid
p.stdin.close();assert p.wait()==0
save('git-seals.json',{'files':len(files),'bytes':sum(x['size'] for x in files),'unique_objects':len(byid),'all_actual_HEAD_git_bytes_exact':True,'raw_commit':seal['raw_commit'],'executing_source':seal['executing_source_commit'],'executing_driver_sha256':seal['executing_driver_sha256']})
# Independent field/type/width/reference instantiation against original approved ledger and raw native images.
ledger=json.loads((O/'analysis/genesis-ledger.json').read_text());approved=json.loads((R/'docs/research/continuation/native-edits/field-ledger.json').read_text())['field_coverage'];fields=[];custody=[];pids=set();drives=set()
prep=g.check();assert len(prep['sources'])==54 and len(prep['private_sources'])==15
for plan in g.cases():
 base=O/'runs'/('wp43-genesis-01-'+plan['id']);run=json.loads((base/'run.json').read_text());assert g.same(run['preparation'],prep)
 assert run['shared_guard_acquired'] and run['shared_guard_released'] and run['oracle_released_before_offline_audit']
 for pin in prep['sources']:
  b=(base/'runner-source'/pin['path']).read_bytes();assert len(b)==pin['size'] and h(b)==pin['sha256']
 for row in run['results']:
  d=base/('r'+str(row['repetition']));work=Path(row['owned_process']['private_work']);disk=work/'harddisk.img';assert disk.is_file();drives.add(str(disk));pids.add(row['owned_process']['pid'])
  assert row['qemu_argv']==row['planned_qemu_argv'] and row['stop_method']=='QMP quit; own socket terminated'
  g.validate_owned_identity(Path(row['owned_process']['socket']),work,row['owned_process']);assert row['stop_proof']['pid']==row['owned_process']['pid']
  assert row['master_before']==row['master_after']==run['master_before']==run['master_after']
  assert row['outcome']=='complete-observation' and row['required_extraction_validated'] and row['normal_original_exit']
  # Strict raw VGA-to-text+CRTC audit runs via g.result/a.audit, independently check final clear DOS.
  raw=(d/'clean-exit/vram.bin').read_bytes();text='\n'.join(raw[i:i+160:2].replace(b'\0',b' ').decode('cp437').rstrip()for i in range(0,4000,160))+'\n';assert len(raw)==4000 and text==(d/'clean-exit/screen.txt').read_text();assert text.splitlines()[0]=='C:\\WP51>' and all(not x for x in text.splitlines()[1:]);cur=json.loads((d/'clean-exit/cursor.json').read_text());assert (cur['row'],cur['column'])==(0,8)
  exports=[]
  for e in row['exports']:
   b=subprocess.check_output(['mtype','-i',str(disk)+'@@1048576','::OUT/'+e['name']],timeout=15);assert b==(d/e['host']).read_bytes();exports.append({'host':e['host'],'size':len(b),'sha256':h(b)})
   if e['host'].endswith('.WP5') and e['name']==plan['first_save_name']:
    f=g.field_report(b);assert len(f['fields'])==72 and not f['unmapped'];owners={p['type']:p['offset'] for p in __import__('native_edits').inspect(b,False)['packets']};coverage=set()
    for old,new in zip(approved,f['fields'],strict=True):
     assert all(new[k]==old[k] for k in ['owner','name','width','representation','units','references']);offset=(0 if old['owner']=='header' else owners[int(old['owner'].split('-')[1])])+old['offset'];assert offset==new['absolute_offset'];assert b[offset:offset+old['width']].hex()==new['hex'];coverage.update(range(offset,offset+old['width']));assert not new['constructor_encoding_permission']
    assert len(coverage)==224;fields.append({'case':plan['id'],'repetition':row['repetition'],'fields':72,'size':len(b),'body_offset':f['body_offset'],'body_hex':f['body_hex']})
  # Validate private custody as hashes only, no private contents saved.
  settings=[]
  for label,pth in [('before',work/'settings-before.SET'),('after',Path(row['settings_after']['private_path']))]:
   b=pth.read_bytes();assert h(b)==row['settings_'+label]['sha256'];settings.append({'phase':label,'sha256':h(b),'size':len(b)})
  for item in row['resources']:
   b=subprocess.check_output(['mtype','-i',str(disk)+'@@1048576','::WP51/'+item['name']],timeout=15);assert h(b)==item['sha256'] and len(b)==item['size']
  listing=subprocess.check_output(['mdir','-b','-i',str(disk)+'@@1048576','::OUT/'],timeout=15);assert listing==(d/'OUT-after.txt').read_bytes()
  if plan['id']=='empty-f10-cancel':assert not exports and listing==(d/'OUT-before-bare.txt').read_bytes()
  custody.append({'case':plan['id'],'repetition':row['repetition'],'owned_pid':row['owned_process']['pid'],'start_ticks':row['owned_process']['start_ticks'],'stopped_exports':exports,'privateSET':settings,'finalDOS_cursor_exact':True,'stopped_listing_exact':True})
assert len(fields)==8 and len(custody)==10 and len(pids)==10 and len(drives)==10
save('field-custody.json',{'first_native':fields,'custody':custody,'54sources_each_prelaunch_exact':True,'15privatepins_current_exact':True,'50stopped_resource_hashes_exact':True,'new_VM':False,'constructor_permission':False})
print('PASS actual20Go reopens/2862raw;3004finalGit seals;8first×72typedfields;10stoppeddrives26exports20SET50resources10DOS+cursor/source54private15')
