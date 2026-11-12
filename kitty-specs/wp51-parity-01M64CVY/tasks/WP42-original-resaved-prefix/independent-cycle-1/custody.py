from pathlib import Path
import json,hashlib,subprocess,sys
R=Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-s');O=R/'docs/research/continuation/resaved-prefix';T=Path('/tmp/wordling-wp42-independent');h=lambda b:hashlib.sha256(b).hexdigest();plan=json.loads((O/'frozen-plan.json').read_text());report=[]
for recipe in plan['cases']:
 folder=O/'runs'/recipe['run_id'];run=json.loads((folder/'run.json').read_text())
 for row in run['results']:
  f=folder/('r'+str(row['repetition']));raw=(f/'clean-exit/vram.bin').read_bytes();assert len(raw)==4000
  text='\n'.join(raw[i:i+160:2].replace(b'\0',b' ').decode('cp437').rstrip() for i in range(0,4000,160))+'\n';assert text==(f/'clean-exit/screen.txt').read_text();assert text.splitlines()[0]=='C:\\WP51>' and all(not l for l in text.splitlines()[1:]);cur=json.loads((f/'clean-exit/cursor.json').read_text());assert cur['row']==0 and cur['column']==8 and (cur['crtc']['14']<<8|cur['crtc']['15'])==8
  argv=row['qemu_argv'];disk=next(v.split('file=',1)[1].split(',')[0] for v in argv if 'harddisk.img' in v);assert Path(disk).is_file()
  for e in row['exports']:
   name=Path(e['path']).name;guestname=name[:-4] if name.endswith('.WP5') else name
   data=subprocess.check_output(['mtype','-i',disk+'@@1048576','::OUT/'+guestname],timeout=15);assert data==(folder/e['path']).read_bytes()
  settings=[]
  for key in ['settings_before','settings_after']:
   item=row[key];b=Path(item['private_path']).read_bytes();assert h(b)==item['sha256'];settings.append({'phase':key,'sha256':h(b),'size':len(b)})
  wire=[json.loads(x) for x in (f/'qmp-wire.jsonl').read_text().splitlines()];tx=[]
  for e in wire:
   if e['direction']=='tx-buffer':
    for line in bytes.fromhex(e['raw_hex']).splitlines():
     try:tx.append(json.loads(line))
     except json.JSONDecodeError:pass
  assert any(x.get('execute')=='quit' for x in tx)
  prn=(f/'W42PRN.PRN').read_bytes(); grammar=recipe['grammar'];body=b'XABCD' if grammar!='two-bold' else b'XABCDE';over=b'' if grammar=='ascii' else b'\r            BC' if grammar=='one-bold' else b'\r            B D'
  expected=b'\r'+b'\r\n'*6+b' '*10+body+over+b'\r'+b'\r\n'*60
  # Full exact selected-profile stream; no whitespace/control normalization.
  assert prn==expected,(recipe['id'],len(prn),len(expected))
  report.append({'case':recipe['id'],'repetition':row['repetition'],'settings':settings,'stopped_exports_disk_exact':7,'raw_vga_text_cursor_exact':True,'wire_QMP_quit':True,'complete_prn_sha256':h(prn)})
for name,sha in plan['master'].items():
 with (Path('/home/lynn/projects/wordling/research/cache/reference/master')/name).open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==sha
(T/'stopped-custody.json').write_text(json.dumps({'rows':report,'private_contents_published':False,'new_VM':False,'master_current_exact':True},indent=2)+'\n');print('PASS12stopped disks84exports24privateSET hashes12rawDOS+cursor12fullPRN12wirequit/master')
