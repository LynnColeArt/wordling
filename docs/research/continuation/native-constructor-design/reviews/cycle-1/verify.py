from pathlib import Path
import sys,json,hashlib,subprocess,struct
A=Path('/tmp/wordling-native-constructor-architecture');T=Path('/tmp/wordling-native-constructor-architecture-review');P=Path('/home/lynn/projects/wordling');R=P/'.worktrees/wp51-parity-01M64CVY-lane-t';O=R/'docs/research/continuation/native-genesis';h=lambda b:hashlib.sha256(b).hexdigest();m=json.loads((A/'manifest.json').read_text());s=json.loads((A/'schema.json').read_text());seals=json.loads((A/'seals.json').read_text())
assert h((A/'decision.md').read_bytes())=='9e3b55431e0b840a2c9cd675ccd4779680a191cd8983ac34186cacf6612c9513';assert h((A/'schema.json').read_bytes())=='7a0241af10147535fee623eefd1406b8b25d1f5ccd93600d60189bdd8b22a766';assert h((A/'manifest.json').read_bytes())=='6e2cccee808d5b0f99e50ea7fa309767591667bc0a2affbcf6d93dff3b4fbcc7';assert h((A/'seals.json').read_bytes())=='56b42767a7e08348fe5627857ed46fc91b71c7c7caa329a8afb7d33f2bae81be'
for n,v in seals['files'].items():b=(A/n).read_bytes();assert len(b)==v['size'] and h(b)==v['sha256']
for pin in m['source_pins']:
 b=(Path(pin['checkout'])/pin['path']).read_bytes();assert len(b)==pin['size'] and h(b)==pin['sha256']
ledger=json.loads((O/'analysis/genesis-ledger.json').read_text());old=json.loads((R/'docs/research/continuation/native-edits/field-ledger.json').read_text())['field_coverage'];assert len(s['fields'])==len(old)==72
for a,b in zip(s['fields'],old,strict=True):
 assert all(a[k]==b[k] for k in ['owner','name','width','representation','units','references']);assert a['relative_owner_offset']==b['offset'] and a['generation_permission'] is False and a['constructor_encoding_permission'] is False
rows=[]
for f in ledger['facts']['first_native_images']:
 b=(O/f['path']).read_bytes();assert len(b)==f['size'];covered=set()
 for v in s['fields']:
  a=v['absolute_offset'];z=a+v['width'];assert b[a:z].hex()==v['hex'];covered.update(range(a,z))
 assert len(covered)==224 and int.from_bytes(b[4:8],'little')==324
 rows.append({'path':f['path'],'size':len(b),'sha256':h(b),'fields':72})
assert len(rows)==8
sys.path.insert(0,str(R/'scripts/reference'));import inspect_setup
master=P/'research/cache/reference/master/harddisk.img';fs=inspect_setup.FAT16(master);setup=fs.read_file('WP51/WP{WP}.SET');md=inspect_setup.inspect(master);pack={x['type']:setup[x['offset']:x['offset']+x['length']] for x in md['packets']};native=(O/ledger['facts']['first_native_images'][0]['path']).read_bytes()
prov=json.loads((A/'resource-provenance-comparisons.json').read_text());assert h(setup)==prov['private_setup_sha256'] and h(fs.data)==prov['master_sha256'];assert h(native[:324])==prov['actual_native_sha256']
comparisons=[(pack[0x57],native[80:166]),(pack[0x59],native[66:80]),(pack[0x54][:74]+pack[0x54][77:85]+pack[0x54][85:86]+pack[0x54][237:241]+pack[0x54][74:77],native[166:256]),(pack[0x56][6:10],native[256:260]),(pack[0x56][2:4],native[262:264]),(pack[0x57][8:10],native[260:262])]
metadata=[]
for (left,right),claim in zip(comparisons,prov['comparisons'],strict=True):
 assert left==right and h(left)==claim['left_sha256'] and h(right)==claim['right_sha256'] and len(left)==claim['bytes'];metadata.append({'comparison':claim['comparison'],'bytes':len(left),'sha256':h(left),'exact':True})
assert pack[0x55][70:72].hex()==prov['SET55h_wysiwyg_scale_plus70']=='0001';assert native[266:268].hex()==prov['document_display_pitch_plus10']=='0000';assert native[264]==1 and native[268:270]==bytes(2)
date,time=struct.unpack_from('<HH',pack[0x54],237);assert inspect_setup.dos_stamp(date,time)['date']=='1992-03-09' and inspect_setup.dos_stamp(date,time)['time']=='12:04:20'
(T/'verification.json').write_text(json.dumps({'all_input_seals_and_26pins_exact':True,'eight_first_native_72fields':rows,'profile_comparisons_metadata_only':metadata,'SDK_checked_pages':[24,25,507,508],'private_bytes_published':False,'new_VM':False,'constructor_permission':False},indent=2)+'\n');print('PASS inputseals/26pins/8×72fields/6private-metadata matches/remap/datepitch; no private content publication or VM')
